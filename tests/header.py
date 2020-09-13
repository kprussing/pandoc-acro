__doc__="""Check the bare expanded text"""

import os
import unittest

from . import command, run_filter

_expected = r"""\usepackage{acro}
\DeclareAcronym{afaik}{
long = as far as I know,
short = AFAIK
}
\DeclareAcronym{lol}{
long = laugh out loud,
long-plural = es,
short = lol,
short-plural = es
}
"""

_template = os.path.join(os.path.dirname(__file__), "test.latex")

class TestMarkdown(unittest.TestCase):
    def test(self):
        result = run_filter(command + ["--template=" + _template, "-t", "latex"])
        self.assertEqual(result, _expected)

if __name__ == "__main__":
    unittest.main()
