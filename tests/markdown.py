__doc__="""Check the bare expanded text"""

import unittest

from . import command, run_filter

_expected = "\n".join("-   " + s for s in (
    "AFAIK",
    "as far as I know (AFAIK)",
    "AFAIK",
    "AFAIKs",
    "AFAIKs",
    "as far as I know",
    "as far as I knows",
    "as far as I know (AFAIK)",
    "as far as I knows (AFAIKs)",
    "AFAIK",
    "AFAIKs",
    "AFAIK",
    "AFAIKs",
    "As far as I know",
    "As far as I knows",
    "As far as I know (AFAIK)",
    "As far as I knows (AFAIKs)",
    )
) + "\n"

class TestMarkdown(unittest.TestCase):
    def test(self):
        result = run_filter(command + ["-t", "markdown"])
        self.assertEqual(result, _expected)

if __name__ == "__main__":
    unittest.main()
