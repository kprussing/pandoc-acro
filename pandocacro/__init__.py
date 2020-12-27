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


def main(doc: Optional[panflute.Doc] = None) -> Optional[panflute.Doc]:
    return panflute.run_filters([translate, printacronyms],
                                prepare=prepare, doc=doc)


if __name__ == "__main__":
    main()
