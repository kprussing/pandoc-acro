__doc__ = """Check the get_key method works as expected"""

import itertools
import re

import pytest

import panflute
import pandocacro
import pandocacro.keys

key = "mwe"
acronyms = {
        "short": "short",
        "long": "long"
    }
markups = (
        f"+{key}",
        f"[+{key}]{{}}",
        f"[+{key}]{{.short}}"
    )
punctuations = (
        "",
        ".",
        "'s",
        "’s",
    )
text = f"""---
acronyms:
    {key}:
        short: {acronyms['short']}
        long: {acronyms['long']}
...

{{mark}}
"""


def test_get_key() -> None:
    """Check the get key parses in a variety of contexts

    We want to make sure get_key can understand the parsing as a raw
    string or inside square brackets as well as in the presence of
    punctuation.

    """
    for markup, punc in itertools.product(markups, punctuations):
        mark = markup + punc
        doc = panflute.convert_text(text.format(mark=mark), standalone=True)
        pandocacro.prepare(doc)
        elem = doc.content[0].content[0]
        result = pandocacro.keys.get(elem, doc)
        assert result is not None
        if result.value != key:
            delim = '"' if "'" in mark else "'"
            pytest.fail(f"Error extracting {key} from {delim}{mark}{delim}. "
                        f"Found {elem} -> {result.value}")

        if "[" not in markup:
            # We have a bare string
            post = result.post
        elif punc != "":
            # We have a span so the punctuation should be the next
            # element.
            post = panflute.stringify(doc.content[0].content[1])

        if punc != (re.sub("’", "'", post) if "'" in punc else punc):
            delim = '"' if "'" in mark else "'"
            pytest.fail(f"Error extracting {delim}{punc}{delim} "
                        f"from {delim}{elem}{delim}")


if __name__ == "__main__":
    test_get_key()
