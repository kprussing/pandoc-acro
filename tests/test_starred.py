__doc__ = """Test the starred version of the acronym"""

import random

from typing import List, Tuple

import panflute

from pandocacro.keys import Key


value = "mwe"
meta = f"""---
acronyms:
    {value}:
        short: short
        long: long
...
"""


def generate(N: int) -> Tuple[str, List[Key]]:
    """Generate the text and the expected list of keys"""
    keys = []
    for _ in range(10):
        key = Key()
        key.value = value
        key.count = random.choice((True, False))
        key.type = random.choice(("", "full", "short", "long"))
        key.capitalize = random.choice((True, False))
        key.plural = random.choice((True, False))
        keys.append(key)

    return meta + "-   " + "\n-   ".join(str(k) for k in keys), keys


def test_latex() -> None:
    """Check the starred LaTeX version works as expected"""
    text, keys = generate(10)
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro"])
    lines = (line for line in result.splitlines())
    assert r"\begin{itemize}" == next(lines)
    assert r"\tightlist" == next(lines)
    for key in keys:
        assert r"\item" == next(lines)
        expected = "\\" + ("A" if key.capitalize else "a") + "c" \
            + ("" if key.type == "" else key.type[0]) \
            + ("p" if key.plural else "") \
            + ("" if key.count else "*") \
            + "{" + key.value + "}"
        assert expected == next(lines).strip()

    assert r"\end{itemize}" == next(lines)
