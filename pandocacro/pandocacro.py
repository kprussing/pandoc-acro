__doc__ = """Class definitions for the package"""

from typing import Dict, Union

Acronym = Dict[str, Union[str, int, bool]]
r"""A map of options passed to ``\DeclareAcronym`` and metadata variables.
"""

Options = Dict[str, Union[str, int, bool]]
r"""Options to pass to ``\usepackage`` when loading ``acro``."""


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

    """

    def __init__(self, acronyms: Dict[str, Union[Acronym, Options]]):
        self.acronyms: Dict[str, Acronym] = {
            k: v for k, v in acronyms.items() if k != "options"
        }
        self.options: Options = acronyms.get("options", {})

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
