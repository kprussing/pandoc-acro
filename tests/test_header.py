__doc__ = """Check the bare expanded text"""

import os

import panflute

_expected = r"""\usepackage{acro}
\DeclareAcronym{BR}{
short = BR,
long = Betriebsrat,
long-plural-form = Betriebsräte,
short-plural-form = BRs
}
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

_expected_with_endings = r"""\usepackage{acro}
\acsetup{long-plural=es,short-plural=es}
\DeclareAcronym{afaik}{
short = AFAIK,
long = as far as I know,
long-plural = s,
short-plural = S
}
\DeclareAcronym{lol}{
short = lol,
long = laugh out loud
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


def test_header_with_endings() -> None:
    """Check the LaTeX header correctly declare new acro commands"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    text = "\n".join(open(os.path.join(dirname, p), "r").read()
                     for p in ("endings_metadata.yaml", "endings_example.md"))
    result = panflute.convert_text(text, output_format="latex",
                                   extra_args=["-F", "pandoc-acro",
                                               "--template", _template])
    assert _expected_with_endings == result
