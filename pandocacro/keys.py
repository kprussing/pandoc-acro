__doc__ = """The module for defining and parsing the key from an
element.
"""

import re

from typing import ClassVar, Match, Optional, Pattern, Set

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
    count: bool, optional
        The entry should be counted (False if '*' and True otherwise).
    type: str, in {"full", "short", "long"}, optional
        The version of the acronym to typeset.
    capitalize: bool, optional
        Capitalize the first work of the acronym.
    plural: bool, optional
        Use the plural form of the acronym.
    post: str, optional
        The trailing punctuation.

    Arguments
    ---------

    elem: :class:`panflute.Element`
        The document element from which to extract the acronym key.

    """

    PATTERN: ClassVar[Pattern[str]] = re.compile(
        r"[+](?P<count>[*]?)(?P<value>\w+)(?P<post>.*)"
    )
    """The pattern for extracting a key"""

    TYPES: ClassVar[Set] = set((
            "full",
            "long",
            "short",
        ))
    """The valid class options for the type of acronym expansion"""

    def __init__(self, elem: Optional[panflute.Element] = None):
        self.value: str = ""
        self.count: bool = True
        self.type: str = ""
        self.capitalize: bool = False
        self.plural: bool = False
        self.post: str = ""
        if elem is not None:
            self.parse(elem)

    @staticmethod
    def match(elem: panflute.Element) -> Optional[Match[str]]:
        """Pattern match for a key in the element

        We can convert a given element to a string and match it against
        the known format for an acronym key.  This method manages
        converting an element to a string, while appropriately stripping
        unnecessary punctuation, and passing the result to the
        :func:`re.match`.

        Parameters
        ----------

        elem: :class:`panflute.Element`
            The document element to inspect for an acronym key.

        Returns
        -------

        Match:
            The result of the :func:`re.match` call with the string
            version of the element.

        """
        if isinstance(elem, panflute.Str):
            content = panflute.stringify(elem)
            if isinstance(elem.parent, panflute.Quoted):
                content = re.sub("['\"]", "", content)

        elif isinstance(elem, panflute.Span):
            content = panflute.stringify(elem.content[0]) \
                if len(elem.content) == 1 else ""
        else:
            content = ""

        return Key.PATTERN.match(content)

    def parse(self, elem: panflute.Element) -> None:
        """Parse the key from a document element

        This method does the low-level details of extracting the
        relevant information from a document :class:`panflute.Element`.
        It inspects the key for the ``+`` followed by the optional
        “don't count” flag ``*`` followed by the actual key.  It then
        extracts the class details to set the type, capitalization, and
        plural details if the element has the appropriate classes
        attribute.

        Raises
        ------

        RuntimeError:
            If the ``classes`` of the element contain more than one of
            the valid ``TYPES``.

        """
        match = self.match(elem)
        if not match:
            return None

        self.value = match.group("value")
        self.count = match.groupdict().get("count", "") != "*"
        types = [] if not hasattr(elem, "classes") \
            else [c for c in elem.classes if c in self.TYPES]
        if len(types) > 1:
            name = type(self).__name__
            raise RuntimeError(
                f"'{name}.parse' Too many classes {types}"
            )

        self.type = "" if len(types) == 0 else types[0]
        self.capitalize = hasattr(elem, "classes") and "caps" in elem.classes
        self.plural = hasattr(elem, "classes") and "plural" in elem.classes
        self.post = match.groupdict().get("post", "")

    def __str__(self) -> str:
        return "[+" + ("" if self.count else "*") \
            + self.value \
            + "]{" \
            + " ".join([
                    (".plural" if self.plural else ""),
                    (".caps" if self.capitalize else ""),
                    ("." + self.type if self.type != "" else ""),
            ]) \
            + "}" + self.post


def count(elem: panflute.Element, doc: panflute.Doc) -> None:
    """Count the use of acronyms in the document

    This method investigates the element and increments the 'count'
    value of the acronym in the :class:`panflute.MetaMap` of the
    document.  If the acronym does not have a 'count' field, it is
    added.  It is intended to be used to prepare the document before
    actually doing the actual substitution.  It also sets the 'used'
    field to False.

    Parameters
    ----------

    elem: :class:`panflute.Element`
        The element under inspection
    doc: :class:`panflte.Doc`
        The main document

    """
    key = get(elem, doc)
    if key:
        doc.acronyms[key.value]["total"] += 1 if key.count else 0


def get(elem: panflute.Element, doc: panflute.Doc) -> Optional[Key]:
    """Extract the key from an element

    Check if the given element contains a key in the metadata ``acronyms``
    field preceded by ``+``.  If it is, return the key and all its
    details.  Otherwise, return None.

    Parameters
    ----------

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

    match = Key.match(elem)
    if not match:
        return None

    key = Key(elem)
    return key if key.value in doc.acronyms else None
