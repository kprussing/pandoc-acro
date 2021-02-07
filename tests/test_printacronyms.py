__doc__ = """Test the printing of the list of acronyms"""

import random
import re
import string

from typing import List, Tuple

import panflute
import yaml

from pandocacro.keys import Key
from pandocacro import printacronyms


TEXT = """---
acronyms:
  mwe:
    short: MWE
    long: minimum working example
  mfe:
    short: MFE
    long: minimum failing example
  afaik:
    short: AFAIK
    long: as far as I know
..."""


def generate() -> Tuple[str, List[Key]]:
    """Generate the base text and expected list of keys"""
    keys = []
    values = [v for v in yaml.safe_load(TEXT)["acronyms"].keys()]
    for _ in range(random.randrange(1, 11)):
        key = Key()
        key.value = random.choice(values)
        key.count = random.choice((True, False))
        key.type = random.choice(("", "full", "short", "long"))
        key.capitalize = random.choice((True, False))
        key.plural = random.choice((True, False))
        keys.append(key)

    return TEXT + "\n-   " + "\n-   ".join(str(k) for k in keys), keys


def test_latex() -> None:
    r"""Check the \printacronyms macro is placed correctly"""
    base, _ = generate()
    div = """
::: {{#{ident}}}
:::
"""
    text = "\n".join([base, div.format(ident="acronyms")])
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro"])
    assert result.splitlines()[-1] == r"\printacronyms"

    text = "\n".join([base,
                      div.format(ident="refs"),
                      div.format(ident="acronyms"),
                      ])
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro"])
    assert result.splitlines()[-1] == r"\printacronyms"

    text = "\n".join([base,
                      div.format(ident="acronyms"),
                      div.format(ident="refs"),
                      ])
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro"])
    lines = (line for line in reversed(result.splitlines()))
    while True:
        line = next(lines)
        if line == "":
            break

    assert next(lines) == r"\printacronyms"


def test_latex_options() -> None:
    r"""Check the expected options get printed correctly"""
    letters = string.ascii_uppercase + string.ascii_lowercase + " "
    for _ in range(random.randrange(10)):
        block = random.choice(("::: {{#acronyms {options}}}\n:::",
                               "# {name} {{#acronyms {options}}}"))
        name = re.sub(" +", " ", "".join(random.choices(letters, k=20)))
        options = []
        sort = random.choice((None, "true", "false", "bad"))
        if sort is not None:
            options.append(f"sort={sort}")

        doc = panflute.convert_text(
            block.format(name=name, options=" ".join(options)),
            standalone=True
        )
        doc.format = "latex"
        result = printacronyms(doc.content[-1], doc)

        assert result is not None

        match = re.match(r"\\printacronyms(?:\[(.*)])?",
                         panflute.stringify(result))
        assert match
        if match.group(1) is None:
            assert isinstance(doc.content[-1], panflute.Div) \
                and sort in (None, "bad")
            continue

        args = [[s for s in a.split("=")] for a in match.group(1).split(",")]
        try:
            val = next(v for k, v in args if k == "name")
        except StopIteration:
            assert isinstance(doc.content[-1], panflute.Div)
        else:
            assert val == name.strip()

        try:
            val = next(v for k, v in args if k == "sort")
        except StopIteration:
            assert sort in (None, "bad")
        else:
            assert sort == val
