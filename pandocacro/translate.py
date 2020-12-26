__doc__ = """Functions to translate keys to proper output"""

import panflute

from .keys import Key


def latex(key: Key) -> panflute.RawInline:
    """Generate the LaTeX output from a key

    This method inspects the given :class:`Key` and determine the
    properly formatted version of the LaTeX acronym.

    Parameters
    ----------

    key: :class:`Key`
        The :class:`Key` to interpret.

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


def plain(key: Key, acronyms: panflute.MetaMap) -> panflute.Str:
    """Generate the plain text acronym expansion from a key

    This method inspects the given :class:`Key` and deduces the
    appropriate expansion based on the details in the given
    :class:`Acronyms` mapping.  It explicitly checks the user requested
    formatting ('long', 'short', 'full', etc.) to do the formatting, but
    it falls back on inspecting the number of usages based on the
    'count' and 'used' fields for the acronym.  Further, it increments
    the 'used' field in the :class:`Acronyms` unless the key was marked
    “do not count.”

    Parameters
    ----------

    key: :class:`Key`
        The :class:`Key` to interpret.

    Returns
    -------

    :class:`panflute.Str`
        The plain text formatted acronym expansion.

    """
    content = {
        k: panflute.stringify(acronyms[key.value][k])
        for k in acronyms[key.value].content
    }
    long_ = content["long"] + (
        content.get("long-plural", "s") if key.plural else ""
    )
    short_ = content["short"] + (
        content.get("short-plural", "s") if key.plural else ""
    )
    full_ = long_ + " (" + content["short"] + ")"
    if key.type == "full":
        text = full_
    elif key.type == "short":
        text = short_
    elif key.type == "long":
        text = long_
    else:
        if int(acronyms[key.value]["count"].text) > 1:
            if acronyms[key.value]["used"].boolean:
                text = short_
            else:
                text = full_

        else:
            text = long_

    if key.count:
        acronyms[key.value]["used"] = True

    head, *tail = (s for s in text)
    return panflute.Str((head.upper() if key.capitalize else head)
                        + "".join(tail) + key.post)
