import nox


@nox.session
def flake8(session):
    """Run the flake8"""
    session.install("flake8")
    session.run("flake8", "pandocacro", "tests", "noxfile.py")


@nox.session
def mypy(session):
    """Run mypy"""
    session.install("mypy")
    session.run("mypy", "pandocacro", "tests", "noxfile.py")


@nox.session(python=[f"3.{x}" for x in range(6, 10)],
             venv_backend="conda")
def test(session):
    """Run the regression tests

    Alternate flags can be passed to ``pytest`` using the positional
    arguments.
    """
    session.install("pytest")
    session.install("panflute>=2.0")
    session.install("pyyaml")
    session.install('.')
    session.conda_install("pandoc>=2.11")
    if session.posargs:
        tests = session.posargs
    else:
        tests = ["tests"]

    session.run("pytest", *tests)
