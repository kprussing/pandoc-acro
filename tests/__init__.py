__doc__ = """Common utilities for running tests"""

import os
import subprocess

_filter = os.path.join(os.path.dirname(__file__),
                       os.pardir,
                       "pandocacro",
                       "__init__.py")

_inputs = [os.path.join(os.path.dirname(__file__), s)
           for s in ("metadata.yaml", "example.md")]

command = ["pandoc", "-F", _filter] + _inputs
"""The base command with all inputs"""


def run_filter(command: list) -> str:
    """Run Pandoc with the filter on the example inputs"""
    return subprocess.run(command, check=True, stdout=subprocess.PIPE,
                          universal_newlines=True).stdout
