__doc__ = """Test the printing of the list of acronyms"""

import random

from typing import List, Tuple

import panflute
import yaml

from pandocacro.keys import Key


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
    for _ in range(random.randrange(10)):
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
