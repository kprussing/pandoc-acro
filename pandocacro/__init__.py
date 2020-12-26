#!/usr/bin/env python3
__doc__ = r"""Translate acronyms in the Pandoc flavored Markdown to
LaTeX's ``acro`` syntax or just do the replacement directly.  Acronyms
are defined in the ``acronyms`` map in the metadata and used in text
with the key prepended by ``+`` or in a native_span.  Each acronym must
have a ``long`` and ``short`` field.  On first use, the expansion is
``long (short)``.  After that, the replacement is ``short`` unless
overridden by the class of the span.  In LaTeX mode, the markup is
simply translated to the ``acro`` macro.  If a key is not defined in the
metadata, no transformation is done.
"""

from typing import Optional

import panflute

from . import keys


def prepare(doc: panflute.Doc) -> None:
    """Prepare the document

    If ``acronyms`` map is in the metadata, generate the LaTeX
    definitions of the acronyms and count the number of uses of the
    acronyms in the document.  These details are to be used by the
    writer or the main filter.
    """
    if "acronyms" not in doc.metadata:
        return

    # Prepare the LaTeX details.
    header = doc.metadata["header-includes"] \
        if "header-includes" in doc.metadata else []

    LaTeX = lambda l: panflute.MetaInlines( # noqa E731 I just want a short name
        panflute.RawInline(l, format="latex")
    )
    header.append(LaTeX(r"\usepackage{acro}"))
    for key, values in doc.get_metadata("acronyms").items():
        header.append(LaTeX(fr"\DeclareAcronym{{{key}}}{{"))
        header.append(LaTeX(",\n".join(f"{k} = {v}" for k, v
                                       in values.items())))
        header.append(LaTeX("}"))

    doc.metadata["header-includes"] = header

    # For other outputs, we'll need to tally use of the acronyms
    doc.walk(keys.count)
    return


def algorithm(elem: panflute.Element,
              doc: panflute.Doc) -> Optional[panflute.Element]:
    """The core algorithm to substitute the acronym

    This method does the heavy lifting of actually inspecting the
    element and doing the relevant replacement.
    """
    key = keys.get(elem, doc)
    if not key:
        return None

    if isinstance(elem, panflute.Str):
        if isinstance(elem.parent, panflute.Span):
            # Apparently, panflute does the contents of the Span before
            # the Span.  Therefore we should punt to let the Span be
            # evaluated and not the string.
            return None

        return algorithm(panflute.Span(elem), doc)

    acronyms = doc.metadata["acronyms"]
    forms = (
        ("full", "f"),
        ("short", "s"),
        ("long", "l")
    )
    if sum((c in elem.classes) for c in (f for f, _ in forms)) > 1:
        panflute.debug(f"Too many classes for element {elem.classes}")
        return None

    if doc.format in ("latex", "beamer"):
        form = [s for c, s in forms if c in elem.classes]
        macro = "\\" + ("A" if "caps" in elem.classes else "a") + "c" \
                + (form[0] if form else "") \
                + ("p" if "plural" in elem.classes else "") \
                + f"{{{key.value}}}"
        return panflute.RawInline(macro + key.post, format="latex")
    else:
        kwargs = {
            k: panflute.stringify(acronyms[key.value][k])
            for k in acronyms[key.value].content
        }

        long_ = "{long}" + (
            ("{long-plural}" if "long-plural" in kwargs else "s")
            if "plural" in elem.classes else ""
        )
        short_ = "{short}" + (
            ("{short-plural}" if "long-plural" in kwargs else "s")
            if "plural" in elem.classes else ""
        )
        full_ = long_ + " (" + short_ + ")"
        if "full" in elem.classes:
            text = full_
        elif "long" in elem.classes:
            text = long_
        elif "short" in elem.classes:
            text = short_
        else:
            if int(acronyms[key.value]["count"].text) > 1:
                if acronyms[key.value]["used"].boolean:
                    text = short_
                else:
                    text = full_
                    doc.metadata["acronyms"][key.value]["used"] = True

            else:
                text = long_

        head, *tail = (s for s in text.format(**kwargs))
        return panflute.Str((head.upper() if "caps" in elem.classes else head)
                            + "".join(tail) + key.post)


def main(doc: Optional[panflute.Doc] = None) -> Optional[panflute.Doc]:
    return panflute.run_filters([algorithm], prepare=prepare, doc=doc)


if __name__ == "__main__":
    main()
