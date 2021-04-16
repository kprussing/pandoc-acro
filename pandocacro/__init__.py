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

from . import keys, options
from .pandocacro import PandocAcro
from .translate import translate
from .list import printacronyms


def prepare(doc: panflute.Doc) -> None:
    """Prepare the document

    If ``acronyms`` map is in the metadata, generate the LaTeX
    definitions of the acronyms and count the number of uses of the
    acronyms in the document.  These details are to be used by the
    writer or the main filter.
    """
    if "acronyms" not in doc.metadata:
        return

    # Store the acronym information as an attribute of the document
    doc.acronyms = PandocAcro(doc.get_metadata("acronyms"))

    # Prepare the LaTeX details.
    header = doc.metadata["header-includes"] \
        if "header-includes" in doc.metadata else []

    LaTeX = lambda l: panflute.MetaInlines( # noqa E731 I just want a short name
        panflute.RawInline(l, format="latex")
    )
    header.append(LaTeX(r"\usepackage{acro}"))
    if doc.acronyms.options:
        header.append(LaTeX(options.acsetup(doc.acronyms.options)))

    for key, values in doc.acronyms.items():
        header.append(LaTeX(fr"\DeclareAcronym{{{key}}}{{"))
        # The short key *must be first*!
        header.append(LaTeX(f"short = {values['short']},\n"))
        header.append(LaTeX(",\n".join(f"{k} = {v}" for k, v
                                       in sorted(values.items())
                                       if k != "short")))
        header.append(LaTeX("}"))

        doc.acronyms[key]["count"] = 0
        doc.acronyms[key]["total"] = 0
        doc.acronyms[key]["list"] = False

    doc.metadata["header-includes"] = header

    # For other outputs, we'll need to tally use of the acronyms
    doc.walk(keys.count)
    return


def finalize(doc: panflute.Doc) -> None:
    """Clear all temporary attributes from the elements

    The utilities can place attributes on the elements that are
    prepended by 'pandocacro-'.  Before we return the
    """
    del doc.acronyms


def main(doc: Optional[panflute.Doc] = None) -> Optional[panflute.Doc]:
    return panflute.run_filters([translate, printacronyms],
                                prepare=prepare, doc=doc)


if __name__ == "__main__":
    main()
