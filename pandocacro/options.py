__doc__ = """The module for processing options"""

import re
import warnings

from typing import List

from .pandocacro import Options

VALID_STYLES: List[str] = [
    "long-short",
    "short-long",
    "short",
    "long",
    "footnote",
]
"""The valid styles for first-style and single-style."""


def options(options: Options,
            silent: bool = False
            ) -> List[str]:
    r"""Generate the list of options for the ``acro`` package.

    This method traverses the map of options given to the filter and
    generates the properly formatted versions to pass to ``\usepackage``
    when loading ``acro``.  This method checks if a key is known
    (meaning used by the plain text output).  If it is, it checks that
    it is a valid value.  If the value is not on the known list of valid
    values, a warning is issued if not in silent mode.  In all cases,
    the key/value pairs are formatted for use in LaTeX output unless the
    value could not be converted to a string.

    Parameters
    ----------

    options: :class:`Options`
        The map of options from the metadata.
    silent: bool
        Disable all warnings.

    Returns
    -------

    list of str:
        The options formatted as 'key=value' to pass to ``\usepackage``.

    """
    output = []
    name = __name__ + ".acro_options"
    for key, val in options.items():
        value = str(
            ("true" if val else "false") if isinstance(val, bool) else val
        )

        output.append(f"{key}={value}")
        if not silent:
            valid = True
            if key in ("first-style", "single-style"):
                valid = value in VALID_STYLES
            elif key in ("single",):
                valid = re.match(r"(true|false|\d+)", value) is not None

            if not valid:
                warnings.warn(
                    f"'{name}' unknown value '{value}' for '{key}'"
                )

    return output


def acsetup(metamap: Options,
            silent: bool = False
            ) -> str:
    r"""Generate the ``\acsetup`` line for enabling ``acro``.

    This method extracts the options and values from the metadata and
    forms the appropriate ``\acsetup`` command to include in the LaTeX
    header.  The options are formatted as 'key=value' within the curly
    brackets.  If no options are found, the empty string is returned.

    Parameters
    ----------

    metamap: :class:`Options`
        The map of options from the metadata.
    silent: bool
        Disable all warnings.

    Returns
    -------

    str:
        The ``\acsetup`` line to add to the header

    """
    output = options(metamap, silent=silent)
    return "" if len(output) == 0 else (
        r"\acsetup{" + ",".join(output) + "}"
    )
