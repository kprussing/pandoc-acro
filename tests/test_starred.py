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


def generate() -> Tuple[str, List[Key]]:
    """Generate the text and the expected list of keys"""
    keys = []
    for _ in range(random.randrange(100)):
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
    text, keys = generate()
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


def test_forced_first_use() -> None:
    """Check the two usages work as expected

    Based on the rules, after the first use that counts, the default for
    subsequent uses should be the short version.
    """
    keys = []
    for type in ("long", ""):
        key = Key()
        key.value = value
        key.type = type
        key.plural = False
        key.capitalize = False
        key.count = True
        keys.append(key)

    text = meta + "-   " + "\n-   ".join(str(k) for k in keys)
    doc = panflute.convert_text(text, standalone=True)
    acronyms = {k: panflute.stringify(doc.metadata["acronyms"]["mwe"][k])
                for k in doc.metadata["acronyms"]["mwe"].content}
    result = panflute.convert_text(text, output_format="markdown",
                                   extra_args=["-F", "pandoc-acro"])
    lines = (line for line in result.splitlines())
    assert "-   " + acronyms["long"] == next(lines).rstrip()
    assert "-   " + acronyms["short"] == next(lines).rstrip()


def test_plain() -> None:
    """Check the results of the starred plain text output"""
    text, keys = generate()
    doc = panflute.convert_text(text, standalone=True)
    acronyms = {k: panflute.stringify(doc.metadata["acronyms"]["mwe"][k])
                for k in doc.metadata["acronyms"]["mwe"].content}

    result = panflute.convert_text(text, output_format="markdown",
                                   extra_args=["-F", "pandoc-acro"])
    lines = (line for line in result.splitlines())
    first = True
    for key in keys:
        if key.type == "long":
            expected = acronyms["long"] + ("s" if key.plural else "")
        elif key.type == "short":
            expected = acronyms["short"] + ("s" if key.plural else "")
        elif key.type == "full":
            expected = acronyms["long"] + ("s" if key.plural else "") \
                + " (" + acronyms["short"] + ")"
        else:
            if first:
                expected = acronyms["long"] + ("s" if key.plural else "") \
                    + " (" + acronyms["short"] + ")"
            else:
                expected = acronyms["short"] + ("s" if key.plural else "")

        if key.count:
            first = False

        head, *tail = (s for s in expected)
        expected = (head.upper() if key.capitalize else head) + "".join(tail)
        assert "-   " + expected == next(lines).rstrip()
