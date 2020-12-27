__doc__ = """Functions to generate the list of acronyms"""

from typing import Optional

import panflute


def printacronyms(elem: panflute.Element,
                  doc: panflute.Doc) -> Optional[panflute.Block]:
    """Print the list of acronyms.

    Replace the 'acronyms' :class:`panflute.Div` with the list of acronyms

    This is the high level filter to generate a list of acronyms.  It
    checks for a :class:`panflute.Div` that has the :attr:`identifier`
    'acronyms' and replaces it with the appropriate list of acronyms.

    Parameters
    ----------

    elem: :class:`panflute.Element`
        The element to inspect and replace.
    doc: :class:`panflute.Doc`
        The document under consideration.

    Returns
    -------

    :class:`panflute.Block`, optional:
        The replacement block with the acronym list.

    """
    if not isinstance(elem, panflute.Div) \
            or elem.identifier != "acronyms":
        return None

    if doc.format in ("latex", "beamer"):
        return panflute.RawBlock(r"\printacronyms", format="latex")

    return None
