__doc__ = """Check the get_key method works as expected"""

import itertools

import pytest

import panflute
import pandocacro


def test_get_key() -> None:
    """Check the get key parses in a variety of contexts

    We want to make sure get_key can understand the parsing as a raw
    string or inside square brackets as well as in the presence of
    punctuation.

    """
    key = "mwe"
    markups = (
            f"+{key}",
            f"[+{key}]{{}}",
            f"[+{key}]{{.short}}"
        )
    contexts = (
            "{markup}",
            "{markup}.",
            "{markup}'s",
        )
    for markup, context in itertools.product(markups, contexts):
        mark = context.format(markup=markup)
        doc = panflute.convert_text(f"""---
acronyms:
  {key}:
    short: short
    long: long
...
{mark}
    """, standalone=True)
        elem = doc.content[0].content[0]
        result, post = pandocacro.get_key(elem, doc)
        if result != key:
            delim = '"' if "'" in mark else "'"
            pytest.fail(f"Error extracting {key} from {delim}{mark}{delim}. "
                        f"Found {elem} -> {result}")


if __name__ == "__main__":
    test_get_key()
