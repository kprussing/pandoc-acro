__doc__ = """The module for defining and parsing the key from an
element.
"""

import re

from typing import Optional, Tuple

import panflute


def get(elem: panflute.Element,
        doc: panflute.Doc
        ) -> Tuple[Optional[str], Optional[str]]:
    """Extract the key from an element

    Check if the given element contains a key in the metadata ``acronyms``
    field preceded by ``+``.  If it is, return the key and all trailing
    punctuation and possessive markings.  Otherwise, return None.

    elem: :class:`panflute.Element`
        The element under inspection
    doc: :class:`panflte.Doc`
        The main document

    Returns
    -------

    str:
        The acronym key.
    str:
        The trailing punctuation.

    """
    # Check for the main acronym database
    if "acronyms" not in doc.metadata:
        return None, None

    if isinstance(elem, panflute.Str):
        content = panflute.stringify(elem)
        if isinstance(elem.parent, panflute.Quoted):
            content = re.sub("['\"]", "", content)

    elif isinstance(elem, panflute.Span):
        if len(elem.content) > 1:
            return None, None

        content = panflute.stringify(elem.content[0])
    else:
        return None, None

    if re.search(r"\s", content):
        # Keys cannot have white space, but panflute should have already
        # split this up.
        return None, None

    match = re.match(r"[+](?P<key>\w+)(?P<post>.*)", content)
    if not match:
        return None, None

    return (None, None) if match.group("key") not in doc.metadata["acronyms"] \
        else (match.group("key"), match.group("post"))
