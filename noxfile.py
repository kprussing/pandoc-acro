import configparser
import pathlib

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


def setup_environment(session):
    """Install the base dependencies"""
    # Get the dependencies from the setup.cfg
    parser = configparser.ConfigParser(empty_lines_in_values=True)
    parser.read(pathlib.Path(__file__).parent / "setup.cfg")
    deps = parser.get("options", "install_requires", fallback="")
    session.install(*[d for d in deps.splitlines() if d])
    session.install('.')


@nox.session(python=[f"3.{x}" for x in range(6, 10)],
             venv_backend="conda")
def test(session):
    """Run the regression tests

    Alternate flags can be passed to ``pytest`` using the positional
    arguments.
    """
    session.install("pytest", "pyyaml")
    setup_environment(session)
    session.conda_install("pandoc>=2.11")
    if session.posargs:
        tests = session.posargs
    else:
        tests = ["tests"]

    session.run("pytest", *tests)


@nox.session
def docs(session):
    """Build the documentation"""
    session.install("sphinx")
    setup_environment(session)
    docs = pathlib.Path(session.bin).parent
    html = docs / "html"
    doctrees = docs / "doctrees"
    srcdir = pathlib.Path(__file__).parent / "doc"
    static = srcdir / "_static"
    if not static.is_dir():
        static.mkdir()

    session.run("sphinx-build",
                "-b", "html",
                "-W",  # Warnings as errors
                "-d", str(doctrees.resolve()),
                str(srcdir.resolve()),
                str(html.resolve())
                )
