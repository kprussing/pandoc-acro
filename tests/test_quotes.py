__doc__ = """Check acronyms in quote blocks work as expected"""

import os

import pytest

import panflute

FILTER = os.path.join(os.path.dirname(__file__),
                      os.pardir,
                      "pandocacro",
                      "__init__.py"
                     )

key = "mwe"
acronyms = {
    key: {
        "short": key,
        "long": "minimum working example"
    }
}
checks = {
    f"'+{key}'": [
        (
            "markdown",
            f"'{acronyms[key]['long']} ({acronyms[key]['short']})'",
        ),
        (
            "latex",
            f"`\\ac{{{key}}}'",
        ),
    ],
    f'"+{key}"': [
        (
            "markdown",
            f'"{acronyms[key]["long"]} ({acronyms[key]["short"]})"',
        ),
        (
            "latex",
            f"``\\ac{{{key}}}''",
        ),
    ],
    f"'[+{key}]{{}}'": [
        (
            "markdown",
            f"'{acronyms[key]['long']} ({acronyms[key]['short']})'",
        ),
        (
            "latex",
            f"`\\ac{{{key}}}'",
        ),
    ],
    f'"[+{key}]{{.long}}"': [
        (
            "markdown",
            f'"{acronyms[key]["long"]}"',
        ),
        (
            "latex",
            f"``\\acl{{{key}}}''",
        ),
    ],
}


def test_quotes(debug: bool = False) -> None:
    """Check that acronyms nested in quotes expand

    We know :func:`get_key` works inside a span, but it appears the
    parsing is not great when it comes to quotes.  In particular, simple
    markers such as ``+mwe`` fail to get parsed but the spanned versions
    ``[+mwe]{}`` do.  To make sure :class:`panflute.Quoted` gets handled
    properly for both LaTeX and bare outputs and with basic and spanned,
    we need a test.

    Parameters
    ----------

    debug: bool, optional
        Disable :func:`pytest.fail` while debugging.

    """
    for check in checks:
        for format, expected in checks[check]:
            result = panflute.convert_text(f"""---
acronyms:
  {key}:
    short: {acronyms[key]['short']}
    long: {acronyms[key]['long']}
...

{check}
""", output_format=format, extra_args=["-F", FILTER])
            if result != expected:
                if debug:
                    print(f"Error converting {check} for {format}")
                else:
                    pytest.fail(f"Error converting {check} for {format}\n"
                                f"  Expected: {expected}\n"
                                f"  Found: {result}")


if __name__ == "__main__":
    test_quotes(debug=True)
