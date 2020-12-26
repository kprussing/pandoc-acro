__doc__ = """Check the bare expanded text"""

import os

import panflute

_expected = "\n".join("-   " + s for s in (
    "as far as I know (AFAIK)",
    "AFAIK",
    "AFAIKs",
    "AFAIKs",
    "as far as I know",
    "as far as I knows",
    "as far as I know (AFAIK)",
    "as far as I knows (AFAIK)",
    "AFAIK",
    "AFAIKs",
    "AFAIK",
    "AFAIKs",
    "As far as I know",
    "As far as I knows",
    "As far as I know (AFAIK)",
    "As far as I knows (AFAIK)",
    )
)


def test_markdown() -> None:
    """Check the Markdown output"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    text = "\n".join(open(os.path.join(dirname, p), "r").read()
                     for p in ("metadata.yaml", "example.md"))
    result = panflute.convert_text(text, output_format="markdown",
                                   extra_args=["-F", "pandoc-acro"])
    assert _expected == result
