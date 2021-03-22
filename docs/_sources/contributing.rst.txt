Contributing
============

Thank you for your interest in improving this acronym filter for
Pandoc_.  Pandoc-acro is open sourced under the `BSD 2-Clause License`_
and welcomes feedback via bug reports, feature requests, and pull
requests.  Please report all bugs or request a feature by submitting an
issue on the Github_ project page.

Reporting Issues
----------------

When submitting a bug report on Github_, please include as much
information as possible to allow us to figure out what is happening.
Please try to include the Python version, the Panflute_ version, an
explanation of your input(s) and the expected output, and a minimal
example demonstrating issue.

Pull Requests
-------------

-   Follow :pep:`8` with `numpy docstrings`_
-   Update the documentation as appropriate
-   Update the Changelog
-   Provide a test demonstrating the error is fixed or the new feature
    works as expected if appropriate
-   Pull requests should be against the ``trunk`` branch

The development uses nox_ to aide with testing multiple Python versions
and linting the code and documentation.  It uses the conda_ back end to
manage the virtual environment to make sure Pandoc_ is available.
Therefore, you must have ``conda`` on your search path for
``nox`` to succeed.  To run the full suite (that must all pass), use

.. code:: bash

    nox -x

To run an individual session, use the ``--session`` option to ``nox``.
The available sessions are:

-   ``flake8`` to run flake8_
-   ``mypy`` to run mypy_
-   ``docs`` to run Sphinx_ on the documentation tree
-   ``test-3.X`` where ``X`` is a supported minor version of Python

The test sessions also accept additional arguments that can be passed to
pytest_.  For example, to run :file:`test_get_key.py` and launch the
debugger on error use

.. code:: bash

    nox -s test-3.8 -- --pdb tests/test_get_key.py

Deploying the HTML Documentation
--------------------------------

The HTML version of the documentation can be updated by running ``nox``
with the ``docs`` session.  Then add and commit the changes.  To
prevent pushing the stable branch without rebuilding the documentation,
copy the script :file:`pre-push-build-sphinx.py` to
:file:`.git/hooks/pre-push` and make it executable.

.. _BSD 2-Clause License: https://opensource.org/licenses/BSD-2-Clause
.. _conda: https://nox.thea.codes/en/stable/config.html#configuring-a-session-s-virtualenv
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _Github: https://github.com/kprussing/pandoc-acro
.. _mypy: https://mypy.readthedocs.io/en/stable/
.. _nox: https://nox.thea.codes/en/stable/index.html
.. _numpy docstrings: https://numpydoc.readthedocs.io/en/latest/format.html
.. _Pandoc: https://pandoc.org
.. _Panflute: http://scorreia.com/software/panflute/
.. _pytest: https://docs.pytest.org/en/stable/
.. _sphinx: https://www.sphinx-doc.org/en/master/index.html
