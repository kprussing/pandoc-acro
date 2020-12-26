__doc__ = """Check the bare expanded text"""

import os

import panflute

_macros = [f"\\item\n  \\{s}{{afaik}}" for s in (
        "ac",
        "ac",
        "acp",
        "acsp",
        "acl",
        "aclp",
        "acf",
        "acfp",
        "Ac",
        "Acp",
        "Acs",
        "Acsp",
        "Acl",
        "Aclp",
        "Acf",
        "Acfp",
    )
]

_expected = "\n".join([
    r"\begin{itemize}",
    r"\tightlist",
    *_macros,
    r"\end{itemize}",
    ]
)


def test_latex() -> None:
    """Check the LaTeX output"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    text = "\n".join(open(os.path.join(dirname, p), "r").read()
                     for p in ("metadata.yaml", "example.md"))
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro"])
    assert _expected == result
