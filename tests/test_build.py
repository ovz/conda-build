"""
This file tests prefix finding for Windows and *nix.
"""

import os
import sys

from conda_build import build
from conda_build.config import config
from conda.compat import TemporaryDirectory

prefix_tests = {"normal": os.path.sep}
if sys.platform == "win32":
    prefix_tests.update({"double_backslash": "\\\\",
                         "forward_slash": "/"})


def _write_prefix(filename, prefix, replacement):
    with open(filename, "w") as f:
        f.write(prefix.replace(os.path.sep, replacement))
        f.write("\n")


def test_find_prefix_files():
    """
    Write test output that has the prefix to be found, then verify that the prefix finding
    identified the correct number of files.
    """
    if not os.path.isdir(config.build_prefix):
        os.makedirs(config.build_prefix)
    with TemporaryDirectory(prefix=config.build_prefix + os.path.sep) as tmpdir:
        # create text files to be replaced
        files = []
        for slash_style in prefix_tests:
            filename = os.path.join(tmpdir, "%s.txt" % slash_style)
            _write_prefix(filename, config.build_prefix, prefix_tests[slash_style])
            files.append(filename)

        assert len(list(build.have_prefix_files(files))) == len(files)
