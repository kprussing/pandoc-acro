__doc__="""Check the bare expanded text"""

import unittest

from . import command, run_filter

_macros = [f"\\item\n  \\{s}{{afaik}}" for s in (
        "acs",
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

_expected = "\n".join([
    r"\begin{itemize}",
    r"\tightlist",
    *_macros,
    r"\end{itemize}",
    ]
) + "\n"

class TestMarkdown(unittest.TestCase):
    def test(self):
        result = run_filter(command + ["-t", "latex"])
        self.assertEqual(result, _expected)

if __name__ == "__main__":
    unittest.main()
