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
\acsetup{long-plural-ending=es,short-plural-ending=es}

\DeclareAcroEnding{gs}{s}{s}
\NewAcroCommand\acgs{m}{\acrogs\UseAcroTemplate{first}{#1}}
\NewAcroCommand\acgss{m}{\acrogs\UseAcroTemplate{short}{#1}}
\NewAcroCommand\acgsl{m}{\acrogs\UseAcroTemplate{long}{#1}}
\NewAcroCommand\acgsf{m}{\acrofull\acrogs\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acgs{m}{\acroupper\acrogs\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acgss{m}{\acroupper\acrogs\UseAcroTemplate{short}{#1}}
\NewAcroCommand\Acgsl{m}{\acroupper\acrogs\UseAcroTemplate{long}{#1}}
\NewAcroCommand\Acgsf{m}{\acroupper\acrofull\acrogs\UseAcroTemplate{first}{#1}}

\DeclareAcroEnding{gp}{}{}
\NewAcroCommand\acgp{m}{\acrogp\UseAcroTemplate{first}{#1}}
\NewAcroCommand\acgps{m}{\acrogp\UseAcroTemplate{short}{#1}}
\NewAcroCommand\acgpl{m}{\acrogp\UseAcroTemplate{long}{#1}}
\NewAcroCommand\acgpf{m}{\acrofull\acrogp\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acgp{m}{\acroupper\acrogp\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acgps{m}{\acroupper\acrogp\UseAcroTemplate{short}{#1}}
\NewAcroCommand\Acgpl{m}{\acroupper\acrogp\UseAcroTemplate{long}{#1}}
\NewAcroCommand\Acgpf{m}{\acroupper\acrofull\acrogp\UseAcroTemplate{first}{#1}}

\DeclareAcroEnding{ga}{}{}
\NewAcroCommand\acga{m}{\acroga\UseAcroTemplate{first}{#1}}
\NewAcroCommand\acgas{m}{\acroga\UseAcroTemplate{short}{#1}}
\NewAcroCommand\acgal{m}{\acroga\UseAcroTemplate{long}{#1}}
\NewAcroCommand\acgaf{m}{\acrofull\acroga\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acga{m}{\acroupper\acroga\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acgas{m}{\acroupper\acroga\UseAcroTemplate{short}{#1}}
\NewAcroCommand\Acgal{m}{\acroupper\acroga\UseAcroTemplate{long}{#1}}
\NewAcroCommand\Acgaf{m}{\acroupper\acrofull\acroga\UseAcroTemplate{first}{#1}}

\DeclareAcroEnding{gb}{}{}
\NewAcroCommand\acgb{m}{\acrogb\UseAcroTemplate{first}{#1}}
\NewAcroCommand\acgbs{m}{\acrogb\UseAcroTemplate{short}{#1}}
\NewAcroCommand\acgbl{m}{\acrogb\UseAcroTemplate{long}{#1}}
\NewAcroCommand\acgbf{m}{\acrofull\acrogb\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acgb{m}{\acroupper\acrogb\UseAcroTemplate{first}{#1}}
\NewAcroCommand\Acgbs{m}{\acroupper\acrogb\UseAcroTemplate{short}{#1}}
\NewAcroCommand\Acgbl{m}{\acroupper\acrogb\UseAcroTemplate{long}{#1}}
\NewAcroCommand\Acgbf{m}{\acroupper\acrofull\acrogb\UseAcroTemplate{first}{#1}}
\DeclareAcronym{afaik}{
short = AFAIK,
long = as far as I know,
long-gp = q,
long-plural = s,
short-ga = A,
short-plural = S
}
\DeclareAcronym{lol}{
short = lol,
long = laugh out loud,
long-gb-form = rolling on the floor laughing,
short-gb-form = rofl
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
