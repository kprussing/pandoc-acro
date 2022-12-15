__doc__ = """Class definitions for the package"""

from typing import Dict, Union
import re

Acronym = Dict[str, Union[str, int, bool]]
r"""A map of options passed to ``\DeclareAcronym`` and metadata variables.
"""

Options = Dict[str, Union[str, int, bool]]
r"""Options to pass to ``\usepackage`` when loading ``acro``."""

Endings = Dict[str, Dict[Union['short', 'long'], str]]
r""""""

class PandocAcro:
    """A class for managing the acronyms in a document

    This class stores a copy of the acronyms field from the metadata in
    a easily modifiable location.  It loads the options into a
    dictionary where the keys map to the values, and it places the
    acronyms into a dictionary that maps the keys to the formatting
    options for the acronym.  The acronyms can also be accessed using
    a mapping notation ``obj['key']``.  The intended usage is to
    initialize the class from the call to the document's
    :func:`get_metadata`::

        obj = PandocAcro(doc.get_metadata("acronyms"))

    Attributes
    ----------

    acronyms: map of strings :class:`Acronyms`
        The mapping of the acronym keys to the formatting options for
        the acronym.  The keys can also be accessed using index
        notation.
    options: :class:`Options`
        The mapping of the option names to the values.
    endings: map of strings :class:`Endings`
        The mapping of the new ending names (excluding plural) to the long and short default forms.

    """

    def __init__(self, acronyms: Dict[str, Union[Acronym, Options, Endings]]):
        self.acronyms: Dict[str, Acronym] = {
            k: v for k, v in acronyms.items() if k != "options" and k != "endings"
        }

        self.endings: Dict[str, Endings] = {
            k: {'short': v.get("short", ""), 'long': v.get("long", "")}
            for k, v in acronyms.get("endings", {}).items() if k != "plural"
        }
        self.options: Options = acronyms.get("options", {})
        if "endings" in acronyms.keys() and "plural" in acronyms.get("endings"):
            if "long" in acronyms.get("endings").get("plural"):
                self.options["long-plural"] = acronyms.get("endings").get("plural").get("long")
            if "short" in acronyms.get("endings").get("plural"):
                self.options["short-plural"] = acronyms.get("endings").get("plural").get("short")

    def __getitem__(self, key):
        return self.acronyms[key]

    def __contains__(self, key):
        return key in self.acronyms

    def __iter__(self):
        return iter(self.acronyms)

    def __len__(self):
        return len(self.acronyms)

    def keys(self):
        return self.acronyms.keys()

    def values(self):
        return self.acronyms.values()

    def items(self):
        return self.acronyms.items()

    def default_long_plural(self):
        return self.options.get("long-plural", "s")

    def default_short_plural(self):
        return self.options.get("short-plural", "s")

    def new_default_endings(self):
        return self.endings

