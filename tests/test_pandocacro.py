import pathlib

import panflute

import pandocacro


def test_pandocacro() -> None:
    """Check the prepare and finalize properly add and remove the acronyms
    """
    root = pathlib.Path(__file__).parent
    text = "\n".join(
        [(root / f).open().read() for f in ("metadata.yaml", "example.md")]
    )
    doc = panflute.convert_text(text, standalone=True)
    assert isinstance(doc, panflute.Doc)
    assert not hasattr(doc, "acronyms")

    pandocacro.prepare(doc)
    assert hasattr(doc, "acronyms")

    for acro in doc.acronyms:
        for key, type_ in (("count", int),
                           ("list", bool),
                           ("used", bool),
                           ):
            assert key in doc.acronyms[acro]
            assert isinstance(doc.acronyms[acro][key], type_)

    pandocacro.finalize(doc)
    assert not hasattr(doc, "acronyms")
