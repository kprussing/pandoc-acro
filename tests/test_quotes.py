__doc__ = """Check acronyms in quote blocks work as expected"""

import pytest

import panflute

key = "mwe"
acronyms = {
    key: {
        "short": key,
        "long": "minimum working example"
    }
}
checks = {
    # Simplest form in all quote styles
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
    f"‘+{key}’": [
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
    f'“+{key}”': [
        (
            "markdown",
            f'"{acronyms[key]["long"]} ({acronyms[key]["short"]})"',
        ),
        (
            "latex",
            f"``\\ac{{{key}}}''",
        ),
    ],
    # Explicit spans
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
    # Acronyms not the sole item in a quotation
    f'"+{key} with text"': [
        (
            "markdown",
            f'"{acronyms[key]["long"]} ({acronyms[key]["short"]}) with text"',
        ),
        (
            "latex",
            f"``\\ac{{{key}}} with text''",
        ),
    ],
    f'"with +{key} text"': [
        (
            "markdown",
            f'"with {acronyms[key]["long"]} ({acronyms[key]["short"]}) text"',
        ),
        (
            "latex",
            f"``with \\ac{{{key}}} text''",
        ),
    ],
    f'"with text +{key}"': [
        (
            "markdown",
            f'"with text {acronyms[key]["long"]} ({acronyms[key]["short"]})"',
        ),
        (
            "latex",
            f"``with text \\ac{{{key}}}''",
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
""", output_format=format, extra_args=["-F", "pandoc-acro"])
            if result != expected:
                if debug:
                    print(f"Error converting {check} for {format}")
                else:
                    pytest.fail(f"Error converting {check} for {format}\n"
                                f"  Expected: {expected}\n"
                                f"  Found: {result}")


if __name__ == "__main__":
    test_quotes(debug=True)
