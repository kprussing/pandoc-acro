#!/usr/bin/env python
__doc__ = """Prevent the user from pushing to stable without updating
the HTML documentation.  This makes sure the stable branch always pushes
the most up to date documentation to the website.  This script checks if
the stable branch is being pushed.  If it is, it checks it out, runs
Sphinx to build the HTML documentation, checks if any changes need to be
committed, and reverts to the original branch.  It refuses to do any of
this if there are uncommitted or staged changes as this would
potentially interfere with the user's state.  To enable this hook, copy
this file to ``.git/hooks/pre-push`` and make it executable with ``chmod
+x .git/hooks/pre-push``.
"""

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("remote", type=str,
                    help="Name of the remote to which the push is being done")
parser.add_argument("url", type=str,
                    help="URL to which the push is being done")
args = parser.parse_args()

# Walk up from the current file until we hit a basename starting with
# ".git".  At that point, the content of root should be the root of the
# git repository
root = pathlib.Path(__file__).resolve()
while True:
    if re.match("[.]git", root.name):
        root = root.parent
        break

    root = root.parent

pushing_stable = False
for line in sys.stdin.readlines():
    if all(re.search("stable$", x) for x in line.split()[::2]):
        pushing_stable = True

if not pushing_stable:
    sys.exit(0)

changes = subprocess.run(["git", "status", "--porcelain"],
                         check=True,
                         capture_output=True,
                         universal_newlines=True).stdout
if any(re.match(r"^\s*M", x) for x in changes.splitlines()):
    print("Push error: You cannot push stable with modified files",
          file=sys.stderr)
    sys.exit(1)

staged = subprocess.run(["git", "diff", "--cached", "--name-only"],
                        check=True,
                        capture_output=True,
                        universal_newlines=True).stdout
if staged != "":
    print("Push error: You cannot push stable with staged files",
          file=sys.stderr)
    sys.exit(1)

branch = subprocess.run(["git", "symbolic-ref", "HEAD"],
                        check=True,
                        capture_output=True,
                        universal_newlines=True).stdout

if not re.search("stable$", branch):
    subprocess.run(["git", "checkout", "stable"], check=True)

build = subprocess.run(["nox", "-s", "github"], cwd=root)
success = build.returncode == 0

if success:
    changes = subprocess.run(["git", "status", "--porcelain", "docs"],
                             capture_output=True,
                             universal_newlines=True).stdout
    if any(re.match(r"^\s*M", x) for x in changes.splitlines()):
        print("Push error: Building the HTML documentation yields "
              "changes to commit", file=sys.stderr)
        success = False

subprocess.run(["git", "checkout", root / "docs"])
if not re.search("stable$", branch):
    subprocess.run(["git", "checkout", branch], check=True)

sys.exit(0 if success else 1)
