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
_macros.extend([f"\\item\n  \\{s}{{BR}}" for s in (
        "acfp",
        "acsp",
        "aclp",
    )
])

_expected = "\n".join([
    r"\begin{itemize}",
    r"\tightlist",
    *_macros,
    r"\end{itemize}",
    ]
)

_macros_with_endings = [f"\\item\n  \\{s}{{afaik}}" for s in (
        "ac",
        "aclp",
        "acsp",
        "acgpl",
        "acgps",
        "acgal",
        "acgas",
    )
]

_macros_with_endings.extend([f"\\item\n  \\{s}{{lol}}" for s in (
        "acgs",
        "aclp",
        "acp",
        "acgss",
        "acgsl",
        "acgsf",
        "Acgs",
        "Acgss",
        "Acgsl",
        "Acgsf",
        "acgbf",
        "acgbl",
        "acgbs",
    )
])

_expected_with_endings = "\n".join([
    r"\begin{itemize}",
    r"\tightlist",
    *_macros_with_endings,
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


def test_latex_with_endings() -> None:
    """Check the LaTeX output if custom endings are used"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    text = "\n".join(open(os.path.join(dirname, p), "r").read()
                     for p in ("endings_metadata.yaml", "endings_example.md"))
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro"])
    assert _expected_with_endings == result
