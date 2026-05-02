__doc__ = """Functions to generate the list of acronyms"""

import logging

from typing import Optional, Union

import panflute


def _metadata_list_options(doc: panflute.Doc) -> dict:
    """Return acronym list options from document metadata.

    The metadata should be provided under the top-level ``acronym-list``
    key, for example::

        acronym-list:
          format: table
          caption: List of acronyms

    """
    if "acronym-list" not in doc.metadata:
        return {}

    options = doc.get_metadata("acronym-list")
    return options if isinstance(options, dict) else {}


def _list_option(elem: Union[panflute.Div, panflute.Header],
                 doc: panflute.Doc,
                 key: str,
                 default: Optional[str] = None) -> Optional[str]:
    """Return an acronym list option.

    Options are resolved in the following order:

    1. Attributes on the ``#acronyms`` placeholder.
    2. Top-level ``acronym-list`` YAML metadata.
    3. The supplied default value.

    """
    if key in elem.attributes:
        return elem.attributes[key]

    options = _metadata_list_options(doc)
    return options.get(key, default)


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


def _bullet_list(acronyms) -> panflute.BulletList:
    """Build the acronym bullet list."""
    acrolist = [panflute.ListItem(
        panflute.Plain(
            panflute.Strong(panflute.Str(acro["short"])),
            panflute.Str(":"),
            panflute.Space,
            *panflute.convert_text(acro["long"])[0].content
            )
        ) for acro in acronyms if acro["list"]]

    return panflute.BulletList(*acrolist)


def _table(elem: Union[panflute.Div, panflute.Header],
           doc: panflute.Doc,
           acronyms) -> panflute.Table:
    """Build the acronym table."""
    rows = [
        panflute.TableRow(
            panflute.TableCell(
                panflute.Plain(
                    panflute.Strong(panflute.Str(acro["short"]))
                )
            ),
            panflute.TableCell(
                panflute.Plain(
                    *panflute.convert_text(acro["long"])[0].content
                )
            )
        )
        for acro in acronyms if acro["list"]
    ]

    caption_text = _list_option(elem, doc, "caption")
    caption = None
    if caption_text:
        caption = panflute.Caption(
            panflute.Plain(
                *panflute.convert_text(caption_text)[0].content
            )
        )

    short_heading = _list_option(
        elem, doc, "table-short-heading", "Acronym"
    )
    long_heading = _list_option(
        elem, doc, "table-long-heading", "Definition"
    )

    return panflute.Table(
        panflute.TableBody(*rows),
        head=panflute.TableHead(
            panflute.TableRow(
                panflute.TableCell(
                    panflute.Plain(panflute.Str(short_heading))
                ),
                panflute.TableCell(
                    panflute.Plain(panflute.Str(long_heading))
                )
            )
        ),
        caption=caption
    )


def plain(elem: Union[panflute.Div, panflute.Header],
          doc: panflute.Doc) -> Optional[panflute.Div]:
    """Assemble the plain text version of the acronym list

    The plain text output can be either a bulleted list of acronyms::

        -   {short}: {long}

    or a two-column table of acronyms::

        | Acronym | Definition |
        |---------|------------|
        | {short} | {long}     |

    The output format is controlled by the ``format`` option, which can be
    provided either as an attribute on the ``#acronyms`` placeholder or in
    the top-level ``acronym-list`` YAML metadata. Supported values are
    ``bullet`` and ``table``. The default is ``bullet``.

    For table output, a caption can be provided with the ``caption`` option.

    Examples
    --------

    YAML metadata::

        acronym-list:
          format: table
          caption: List of acronyms

    Placeholder attributes::

        ::: {#acronyms format="table" caption="List of acronyms"}
        :::

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

    list_format = _list_option(elem, doc, "format", "bullet").lower()
    if list_format not in ("bullet", "table"):
        logger.warning(f"Unknown acronym list format '{list_format}'")
        list_format = "bullet"

    if list_format == "table":
        contents = _table(elem, doc, acronyms)
    else:
        contents = _bullet_list(acronyms)

    return panflute.Div(header, contents, identifier="acronym-list")