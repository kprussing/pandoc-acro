__doc__ = """Functions to translate keys to proper output"""

from typing import Optional, Tuple

import panflute

from . import keys
from .pandocacro import PandocAcro


def translate(elem: panflute.Element,
              doc: panflute.Doc) -> Optional[panflute.Element]:
    """Translate a marked acronym to the expanded version

    This method is the filter interface to actually inspect an element
    and translate it to the appropriate replacement.  This includes
    generating the appropriate LaTeX macro or fully expanding the text
    based on the :class:`panflute.Doc` :attr:`format`.

    Parameters
    ----------

    elem: :class:`panflute.Element`
        The element to inspect and replace.
    doc: :class:`panflute.Doc`
        The document under consideration.

    Returns
    -------

    :class:`panflute.Element`, optional:
        The replacement element with the acronym replacement.


    """
    if isinstance(elem, panflute.Str):
        if isinstance(elem.parent, panflute.Span):
            # Apparently, panflute does the contents of the Span before
            # the Span.  Therefore we should punt to let the Span be
            # evaluated and not the string.
            return None

        return translate(panflute.Span(elem), doc)

    key = keys.get(elem, doc)
    if not key:
        return None

    if doc.format in ("latex", "beamer"):
        return latex(key)
    else:
        return plain(key, doc.acronyms)


def latex(key: keys.Key) -> panflute.RawInline:
    """Generate the LaTeX output from a key

    This method inspects the given :class:`keys.Key` and determine the
    properly formatted version of the LaTeX acronym.

    Parameters
    ----------

    key: :class:`keys.Key`
        The :class:`keys.Key` to interpret.

    Returns
    -------

    :class:`panflute.RawInline`
        The LaTeX formatted acronym.

    """
    macro = "\\" + ("A" if key.capitalize else "a") + "c" \
        + {"full": "f",
           "short": "s",
           "long": "l"
           }.get(key.type, "") \
        + ("p" if key.plural else "") \
        + ("*" if not key.count else "") \
        + f"{{{key.value}}}" \
        + key.post
    return panflute.RawInline(macro, format="latex")


def plain(key: keys.Key, acronyms: PandocAcro) -> panflute.Str:
    """Generate the plain text acronym expansion from a key

    This method inspects the given :class:`keys.Key` and deduces the
    appropriate expansion based on the details in the given
    :class:`Acronyms` mapping.  It explicitly checks the user requested
    formatting ('long', 'short', 'full', etc.) to do the formatting, but
    it falls back on inspecting the number of usages based on the
    'count' and 'used' fields for the acronym.  Further, it increments
    the 'used' field in the :class:`Acronyms` unless the key was marked
    “do not count.”

    Parameters
    ----------

    key: :class:`keys.Key`
        The :class:`keys.Key` to interpret.

    Returns
    -------

    :class:`panflute.Str`
        The plain text formatted acronym expansion.

    Raises
    ------

    NotImplementedError:
        When an unknown first or single style is requested.

    """
    long_ = acronyms[key.value]["long"] + (
        acronyms[key.value].get("long-plural", "s") if key.plural else ""
    )
    short_ = acronyms[key.value]["short"] + (
        acronyms[key.value].get("short-plural", "s") if key.plural else ""
    )

    def get_style(option: str, default: str) -> Tuple[str, bool]:
        style = acronyms.options.get(option, default)
        if style == "long-short":
            return long_ + " (" + acronyms[key.value]["short"] + ")", True
        elif style == "short-long":
            return short_ + " (" + acronyms[key.value]["long"] + ")", True
        elif style == "long":
            return long_, False
        elif style == "short":
            return short_, True
        else:
            raise NotImplementedError(
                f"{__name__}.plain unknown style '{style}'"
            )

    single_ = acronyms.options.get("single", False)
    try:
        single = int(single_)
    except TypeError:
        single = single_ == "true"

    if key.type == "full":
        text, to_list = get_style("first-style", "long-short")
    elif key.type == "short":
        text = short_
        to_list = True
    elif key.type == "long":
        text = long_
        to_list = False
    elif (single is True and acronyms[key.value]["total"] < 2) or (
                isinstance(single, int) and
                acronyms[key.value]["total"] <= single
            ):
        # We are below the threshold for the usage to "count".
        text, to_list = get_style("single-style", "long")
    elif acronyms[key.value]["count"] == 0:
        text, to_list = get_style("first-style", "long-short")
    else:
        text = short_
        to_list = True

    if key.count:
        acronyms[key.value]["count"] += 1

    if to_list:
        acronyms[key.value]["list"] = True

    head, *tail = (s for s in text)
    return panflute.Str((head.upper() if key.capitalize else head)
                        + "".join(tail) + key.post)
