__doc__ = """Check the bare expanded text"""

import os

import panflute

_expected = r"""\usepackage{acro}
\DeclareAcronym{afaik}{
short = AFAIK,
long = as far as I know
}
\DeclareAcronym{lol}{
short = lol,
long = laugh out loud,
long-plural = es,
short-plural = es
}"""

_template = os.path.join(os.path.dirname(__file__), "test.latex")


def test_header() -> None:
    """Check the base LaTeX header includes"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    text = "\n".join(open(os.path.join(dirname, p), "r").read()
                     for p in ("metadata.yaml", "example.md"))
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro",
                                               "--template", _template])
    assert _expected == result


def test_header_after() -> None:
    """Check the header includes additional includes"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    text = "\n".join(open(os.path.join(dirname, p), "r").read()
                     for p in ("metadata.yaml",
                               "header-includes.yaml",
                               "example.md"))
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro",
                                               "--template", _template])
    assert "\\usepackage{test}\n" + _expected == result
