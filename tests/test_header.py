__doc__ = """Check the bare expanded text"""

from . import command, run_filter

import os
import unittest

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


class TestHeader(unittest.TestCase):
    def test(self):
        result = run_filter(command + ["--template=" + _template,
                                       "-t", "latex"])
        self.assertEqual(result, _expected)

    def test_extra_after(self):
        extra = r"\usepackage{test}"
        extras = os.path.join(os.path.dirname(__file__),
                              "header-includes.yaml")
        result = run_filter(command + [extras,
                                       "--template=" + _template,
                                       "-t", "latex"])
        self.assertEqual(result, extra + "\n" + _expected)


if __name__ == "__main__":
    unittest.main()
