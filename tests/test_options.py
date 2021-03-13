__doc__ = """Check the options behave as expected"""

import os
import random
import re

from typing import Dict, List, Union

import panflute

from pandocacro import options


def generate_options() -> Dict[str, Union[str, int, bool]]:
    """Generate an option map of valid options"""
    meta: Dict[str, Union[str, int, bool]] = {}
    first_style = random.choice(options.VALID_STYLES + [""])
    if first_style:
        meta["first-style"] = first_style

    single_style = random.choice(options.VALID_STYLES + [""])
    if single_style:
        meta["single-style"] = single_style

    # See [this answer](https://stackoverflow.com/a/62358498/4249913)
    # for why we need the type information.
    choices: List[Union[str, int]] = [
        "true", "false", "", *[x for x in range(1, 6)]
    ]
    single = random.choice(choices)
    if single:
        meta["single"] = single

    case_sensitive = random.choice(("true", "false", ""))
    if case_sensitive:
        meta["case-sensitive"] = case_sensitive

    return meta


def test_options() -> None:
    """Check that the options for ``acro`` get generated properly"""
    for count in range(10):
        meta = generate_options()
        results = options.options(meta, silent=False)
        assert len(results) == len(meta)
        for opt in results:
            key, value = opt.split("=")
            assert key in meta
            assert str(meta[key]) == value


def test_acsetup() -> None:
    r"""Check that the \acsetup line for ``acro`` generates properly"""
    for count in range(10):
        meta = generate_options()

        match = re.match(r"\\acsetup{(.*)}",
                         options.acsetup(meta, silent=False))
        if len(meta) == 0:
            assert match is None
            assert options.acsetup(meta, silent=True) == ""
        else:
            assert match is not None
            assert match.group(1) is not None
            opts = match.group(1).split(",")
            assert len(opts) == len(meta)
            for opt in opts:
                key, value = opt.split("=")
                assert key in meta
                assert str(meta[key]) == value


def test_option_header() -> None:
    r"""Check the \usepackage{acro} gets added to the header"""
    _template = os.path.join(os.path.dirname(__file__), "test.latex")
    for count in range(10):
        meta = generate_options()
        text = ["---",
                "acronyms:",
                "  mwe:",
                "    short: mwe",
                "    long: minimum working example",
                ]
        if len(meta) > 0:
            text.extend(["  options:"] +
                        [f"    {k}: {v}" for k, v in meta.items()]
                        )

        text.extend(["...", ""])

        results = panflute.convert_text(
            "\n".join(text), output_format="latex",
            extra_args=["-F", "pandoc-acro", "--template", _template]
        ).splitlines()

        if len(meta) == 0:
            assert len(results) == 5
        else:
            assert len(results) == 6
            match = re.match(r"\\acsetup{(.*)}", results[1])
            assert match is not None
            assert match.group(1) is not None
            opts = match.group(1).split(",")
            assert len(opts) == len(meta)
            for opt in opts:
                key, value = opt.split("=")
                assert key in meta
                assert str(meta[key]) == value
