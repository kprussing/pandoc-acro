__doc__ = """The module for defining and parsing the key from an
element.
"""

import re

from typing import ClassVar, Optional, Pattern

import panflute


class Key:
    """The key value and associated details

    A key is an alphanumeric string preceded by a ``+`` either outside
    of or within a :class:`panflute.Span`.  A key may also have a ``*``
    after the leading ``+`` but before the key indicating the use should
    not be counted in regards to the first usage.  A key that is not
    within a :class:`panflute.Span` may also have trailing punctuation
    such as a period, comma, or possessive markings.

    Attributes
    ----------

    value: str
        The acronym key.
    count: bool
        The entry should be counted (True if '*' and False otherwise)
    post: str
        The trailing punctuation.

    """

    PATTERN: ClassVar[Pattern[str]] = re.compile(
        r"[+](?P<count>[*]?)(?P<value>\w+)(?P<post>.*)"
    )
    """The pattern for extracting a key"""

    def __init__(self, value: str, count: str = "*", post: str = ""):
        self.value: str = value
        self.count: bool = count == "*"
        self.post: str = post


def get(elem: panflute.Element, doc: panflute.Doc) -> Optional[Key]:
    """Extract the key from an element

    Check if the given element contains a key in the metadata ``acronyms``
    field preceded by ``+``.  If it is, return the key and all its
    details.  Otherwise, return None.

    elem: :class:`panflute.Element`
        The element under inspection
    doc: :class:`panflte.Doc`
        The main document

    Returns
    -------

    Key:
        The populated :class:`Key` if the value is in the ``acronyms``
        metadata.  Otherwise, None.

    """
    # Check for the main acronym database
    if "acronyms" not in doc.metadata:
        return None

    if isinstance(elem, panflute.Str):
        content = panflute.stringify(elem)
        if isinstance(elem.parent, panflute.Quoted):
            content = re.sub("['\"]", "", content)

    elif isinstance(elem, panflute.Span):
        if len(elem.content) > 1:
            return None

        content = panflute.stringify(elem.content[0])
    else:
        return None

    if re.search(r"\s", content):
        # Keys cannot have white space, but panflute should have already
        # split this up.
        return None

    match = Key.PATTERN.match(content)
    if not match:
        return None

    key = Key(**match.groupdict())
    return key if key.value in doc.metadata["acronyms"] else None
