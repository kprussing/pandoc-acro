import nox


@nox.session
def lint(session):
    """Run the linter"""
    session.install("flake8")
    session.run("flake8", "pandocacro", "tests", "noxfile.py")


@nox.session(python=[f"3.{x}" for x in range(6, 10)],
             venv_backend="conda")
def test(session):
    """Run the regression tests"""
    session.install("panflute")
    session.install('.')
    session.conda_install("pandoc")
    session.run('python', '-m', 'unittest', 'discover', '-v')
