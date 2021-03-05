__doc__ = """Functions to generate the list of acronyms"""

import logging

from typing import Optional, Union

import panflute


def printacronyms(elem: panflute.Element,
                  doc: panflute.Doc) -> Optional[panflute.Block]:
    """Print the list of acronyms.

    This is the high level filter to generate a list of acronyms.  It
    checks for a :class:`panflute.Div` or :class:`panflute.Header` that
    has the :attr:`identifier` 'acronyms' and replaces it with the
    appropriate list of acronyms.

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
    if not isinstance(elem, (panflute.Div, panflute.Header)) \
            or elem.identifier != "acronyms":
        return None

    if doc.format in ("latex", "beamer"):
        return latex(elem, doc)

    return plain(elem, doc)


def latex(elem: Union[panflute.Div, panflute.Header],
          doc: panflute.Doc) -> panflute.RawBlock:
    r"""Assemble the LaTeX version of the acronym list

    The base LaTeX output is the ``\printacronyms`` macro, but we need
    to extract the possible name, and sort variables based on the
    content and attributes.  The content is stringified and set to the
    ``name`` option and ``sort`` is translated as lower case.  If one of
    the attributes cannot be interpreted, it is omitted from the option
    list and a warning is logged.

    Parameters
    ----------

    elem: :class:`panflute.Div` or :class:`panflute.Header`
        The element to replace
    doc: :class:`panflute.Doc`
        The document under consideration.

    Returns
    -------

    :class:`panflute.RawBlock`:
        The replacement for the block.

    """
    logger = logging.getLogger(__name__ + ".latex")
    options = []
    if isinstance(elem, panflute.Header):
        options.append("name=" + panflute.stringify(elem))

    if "sort" in elem.attributes:
        sort = elem.attributes["sort"].lower()
        if sort not in ("true", "false"):
            logger.warning(f"Unknown 'sort' option '{sort}'")
        else:
            options.append(f"sort={sort}")

    args = ("[" + ",".join(options) + "]") if options else ""
    return panflute.RawBlock(r"\printacronyms" + args, format="latex")


def plain(elem: Union[panflute.Div, panflute.Header],
          doc: panflute.Doc) -> Optional[panflute.Div]:
    """Assemble the plain text version of the acronym list

    The base plain text output is a bulleted list of acronyms in the
    following format::

        -   {short}: {long}

    in a new :class:`panflute.Div` with the identifier “acronym-list”.
    If the given element is a :class:`panflute.Div`, the list is placed
    under a level 1 header with the text “Acronyms” unless the ``name``
    or ``level`` attributes are set in which case, the request is
    honored.  The list is sorted by the short version of the acronyms by
    default unless the ``sort`` attribute is set to “false” (case
    insensitive) in which case the order is unspecified.  If an
    attribute cannot be interpreted, it is omitted and a warning is
    logged.

    Parameters
    ----------

    elem: :class:`panflute.Div` or :class:`panflute.Header`
        The element to replace
    doc: :class:`panflute.Doc`
        The document under consideration.

    Returns
    -------

    :class:`panflute.Div`, optional:
        The replacement for the block.

    """
    logger = logging.getLogger(__name__ + ".plain_text")
    if "acronyms" not in doc.metadata:
        return None

    if isinstance(elem, panflute.Header):
        header = elem
    elif isinstance(elem, panflute.Div):
        header = panflute.Header(panflute.Str(
                                    elem.attributes.get("name", "Acronyms")
                                 ),
                                 level=elem.attributes.get("level", 1))
    else:
        cls = type(elem)
        logger.warning(f"Unknown element type {cls}")
        return None

    if "sort" in elem.attributes:
        sort = elem.attributes["sort"].lower()
        if sort not in ("true", "false"):
            sort = "true"
            logger.warning(f"Unknown 'sort' option '{sort}'")
    else:
        sort = "true"

    if sort == "true":
        acronyms = sorted(doc.acronyms.values(), key=lambda x: x["short"])
    else:
        acronyms = doc.acronyms.values()

    acrolist = [panflute.ListItem(
        panflute.Plain(
            panflute.Strong(panflute.Str(acro["short"])),
            panflute.Str(":"),
            panflute.Space,
            *panflute.convert_text(acro["long"])[0].content
            )
        ) for acro in acronyms if acro["list"]]
    return panflute.Div(header, panflute.BulletList(*acrolist),
                        identifier="acronym-list")
