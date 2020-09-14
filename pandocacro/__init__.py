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

from typing import Union

import panflute

_acronyms = "acronyms"
"""The metadata key to the acronyms map"""


def get_key(elem: panflute.Element, doc: panflute.Doc) -> Union[None, str]:
    """Extract the key from an element

    Check if the given element is a key in the metadata ``acronyms``
    field preceded by ``+``.  If it is, return the key.  Otherwise,
    return ``None``.
    """
    # Check for the main acronym database
    if _acronyms not in doc.metadata:
        return

    if isinstance(elem, panflute.Str):
        pass
    elif isinstance(elem, panflute.Span):
        if len(elem.content) > 1:
            return
    else:
        return

    # Check for the leading marker
    content = panflute.stringify(elem)
    if content[0] != "+":
        return

    return content[1:] if content[1:] in doc.metadata[_acronyms] else None


def prepare(doc: panflute.Doc) -> None:
    """Prepare the document

    If ``acronyms`` map is in the metadata, generate the LaTeX
    definitions of the acronyms and count the number of uses of the
    acronyms in the document.  These details are to be used by the
    writer or the main filter.
    """
    if _acronyms not in doc.metadata:
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
    def count(elem, doc):
        """Helper to count use of acronyms"""
        key = get_key(elem, doc)
        if key:
            doc.metadata[_acronyms][key]["count"] \
                = int(doc.get_metadata(_acronyms)[key].get("count", 0)) + 1
            doc.metadata[_acronyms][key]["used"] = False

    doc.walk(count)
    return


def algorithm(elem: panflute.Element,
              doc: panflute.Doc) -> Union[panflute.Element, None]:
    """The core algorithm to substitute the acronym

    This method does the heavy lifting of actually inspecting the
    element and doing the relevant replacement.
    """
    key = get_key(elem, doc)
    if not key:
        return

    if isinstance(elem, panflute.Str):
        if isinstance(elem.parent, panflute.Span):
            # Apparently, panflute does the contents of the Span before
            # the Span.  Therefore we should punt to let the Span be
            # evaluated and not the string.
            return

        return algorithm(panflute.Span(elem), doc)

    acronyms = doc.metadata[_acronyms]
    forms = (
        ("full", "f"),
        ("short", "s"),
        ("long", "l")
    )
    if sum((c in elem.classes) for c in (f for f, _ in forms)) > 1:
        panflute.debug(f"Too many classes for element {elem.classes}")
        return

    if doc.format in ("latex", "beamer"):
        form = [s for c, s in forms if c in elem.classes]
        macro = "\\" + ("A" if "caps" in elem.classes else "a") + "c" \
                + (form[0] if form else "") \
                + ("p" if "plural" in elem.classes else "") \
                + f"{{{key}}}"
        return panflute.RawInline(macro, format="latex")
    else:
        kwargs = {
            k: panflute.stringify(acronyms[key][k])
            for k in acronyms[key].content
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
            if int(acronyms[key]["count"].text) > 1:
                if acronyms[key]["used"].boolean:
                    text = short_
                else:
                    text = full_
                    doc.metadata[_acronyms][key]["used"] = True

            else:
                text = long_

        head, *tail = text.format(**kwargs)
        return panflute.Str((head.upper() if "caps" in elem.classes else head)
                            + "".join(tail))


def main(doc: Union[panflute.Doc, None] = None) \
        -> Union[panflute.Doc, None]:
    return panflute.run_filters([algorithm], prepare=prepare, doc=doc)


if __name__ == "__main__":
    main()
