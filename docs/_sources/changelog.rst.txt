Changelog
=========

All notable changes to this project will be documented in this file.
The format is based on `Keep a Changelog`_.

Unreleased_
-----------

Added
^^^^^

-   Full support for the starred usage in the output
-   Random selection of keys for testing purposes
-   Support for creating a list of acronyms
-   Option to pass through arguments to pytest_ from nox_
-   HTML documentation generation via Sphinx_ and deploy to github pages
-   Hook to prevent pushing to stable without up to date HTML docs

Changed
^^^^^^^

-   Moved the main translation function to the submodule
-   Moved the version string to the main source following `single source
    pattern`_

Fixed
^^^^^

-   Typos in the README
-   Added missing files to the distribution

0.9.5_ 2020-12-25
-----------------

Added
^^^^^

-   A unique type for processing acronym keys
-   Have the key class manage the parsing during the initialization
-   Added mypy_ as a linting step

Changed
^^^^^^^

-   Refactored the tests to directly use the filter
-   Moved key extraction to a submodule for better testing
-   Moved the output generation to a submodule

Fixed
^^^^^

-   Correct the counting of starred keys

0.9.4_ 2020-12-18
-----------------

Fixed
^^^^^

-   Properly strip quotes when processing :class:`panflute.Quoted`
    blocks

0.9.3_ 2020-12-18
-----------------

Changed
^^^^^^^

-   Migrated from tox_ to nox_
-   Migrated to pytest_ for testing


Fixed
^^^^^

-   Corrected logic to make sure a key was registered before use
-   Parsing of acronyms at bounded by punctuation

0.9.1_ 2020-09-14
-----------------

Added
^^^^^

-   tox_ support linting with flake8_ and testing with unittest_

Fixed
^^^^^

-   LaTeX header inclusion logic to not overwrite user additions

Removed
^^^^^^^

-   Support for Python 3.5

.. _Unreleased: https://github.com/kprussing/pandoc-acro/compare/v0.9.5...HEAD
.. _0.9.5: https://github.com/kprussing/pandoc-acro/compare/v0.9.4...v0.9.5
.. _0.9.4: https://github.com/kprussing/pandoc-acro/compare/v0.9.3...v0.9.4
.. _0.9.3: https://github.com/kprussing/pandoc-acro/compare/v0.9.1...v0.9.3
.. _0.9.1: https://github.com/kprussing/pandoc-acro/releases/tag/v0.9.1
.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _mypy: https://mypy.readthedocs.io/en/stable/
.. _pytest: https://docs.pytest.org/en/stable/
.. _nox: xhttps://nox.thea.codes/en/stable/
.. _single source pattern: https://packaging.python.org/guides/single-sourcing-package-version/
.. _sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _tox: https://tox.readthedocs.io/en/latest/
.. _unittest: https://docs.python.org/3/library/unittest.html
