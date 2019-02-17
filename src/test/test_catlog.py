from io import StringIO
import re
import unittest
from unittest.mock import patch

from catlogs.app import App



class ArgparseExitException(Exception):
    def __init__(self, status, message):
        self.message = message
        self.status = status



class TestCatlog(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.stdout = StringIO()
        patcher = patch("sys.stdout", self.stdout)
        patcher.start()
        self.addCleanup(patcher.stop)

        self.stderr = StringIO()
        patcher = patch("sys.stderr", self.stderr)
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch("argparse.ArgumentParser.exit", self.argparse_exit)
        patcher.start()
        self.addCleanup(patcher.stop)

        self.argv = ["catlogs"]


    def tearDown(self) -> None:
        self.app = None


    def argparse_exit(self, status=0, message=None):
        raise ArgparseExitException(status, message)


    def addArgs(self, *argv):
        for a in argv: self.argv.append(a)


    def runapp(self):
        self.app = App(self.argv)
        self.app.run()


    def test_help(self):
        EXPECTED = ("usage: catlogs [-h] [-d] [-r REGEX] LOG_PART [LOG_PART ...]\n"
                    "\n"
                    "Prints out a series of rotated log file in decending numerical order.\n"
                    "Duplicates are printed out only once. Supported compression formats are the\n"
                    "following: gz\n"
                    "\n"
                    "positional arguments:\n"
                    "  LOG_PART              Files containing the rotated parts of the log\n"
                    "\n"
                    "optional arguments:\n"
                    "  -h, --help            show this help message and exit\n"
                    "  -d, --debug           Output debug information on stderr\n"
                    "  -r REGEX, --regex REGEX\n"
                    "                        REGEX used to parse the log file number. Note that a\n"
                    "                        single file is allowed to have a missing number, in\n"
                    "                        which case it is assigned number -1. (Default:\n"
                    "                        \"([0-9]+)\")\n"
                    "\n"
                    )

        self.addArgs("-h")
        with self.assertRaises(ArgparseExitException)as ex:
            self.runapp()
        self.assertEqual(0, ex.exception.status)
        self.assertEqual(None, ex.exception.message)

        self.assertRegex(self.stdout.getvalue(), re.escape(EXPECTED))
        self.assertEqual("", self.stderr.getvalue())


    def test_unordered_files(self):
        EXPECTED = ("This is file 5, line 1\n"
                    "This is file 5, line 2\n"
                    "This is file 5, line 3\n"
                    "This is file 4, line 1\n"
                    "This is file 4, line 2\n"
                    "This is file 4, line 3\n"
                    "This is file 3, line 1\n"
                    "This is file 3, line 2\n"
                    "This is file 3, line 3\n"
                    "This is file 2, line 1\n"
                    "This is file 2, line 2\n"
                    "This is file 2, line 3\n"
                    "This is file 1, line 1\n"
                    "This is file 1, line 2\n"
                    "This is file 1, line 3\n"
                    "This is file 0, line 1\n"
                    "This is file 0, line 2\n"
                    "This is file 0, line 3\n")

        self.addArgs(
            "test/sample_files/dotlogfile.4.log.gz",
            "test/sample_files/dotlogfile.0.log",
            "test/sample_files/dotlogfile.2.log.gz",
            "test/sample_files/dotlogfile.5.log.gz",
            "test/sample_files/dotlogfile.1.log",
            "test/sample_files/dotlogfile.3.log.gz",
            )

        self.runapp()

        self.assertEqual(EXPECTED, self.stdout.getvalue())
