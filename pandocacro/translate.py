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
        + f"{{{key.value}}}" \
        + key.post
    return panflute.RawInline(macro, format="latex")
