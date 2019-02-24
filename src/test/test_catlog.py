import sys

from pytest import fixture

from catlogs.app import App



class ExitException(Exception):
    def __init__(self, status):
        self.status = status



@fixture
def app(monkeypatch):
    class AppRunner:
        def run(self, argv):
            app = App(["catlogs"] + argv)

            monkeypatch.setattr("sys.exit", self.exit)
            self.exitcode = 0
            try:
                app.run()
            except ExitException as ex:
                self.exitcode = ex.status


        def exit(self, code):
            raise ExitException(code)



    app = AppRunner()
    return app



def test_noargs(app, capsys):
    EXPECTED_STDERR = ("usage: catlogs [-h] [-d] [-r REGEX] LOG_PART [LOG_PART ...]\n"
                       "catlogs: error: the following arguments are required: LOG_PART\n")

    app.run([])

    assert app.exitcode == 2

    outputs = capsys.readouterr()
    print(outputs.out)
    print(outputs.err, file=sys.stderr)
    assert "" == outputs.out
    assert EXPECTED_STDERR == outputs.err



def test_help(app, capsys):
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
                "Version: "
                )

    app.run(["-h"])
    assert app.exitcode == 0

    outputs = capsys.readouterr()
    print(outputs.out)
    assert outputs.out.startswith(EXPECTED)
    assert "" == outputs.err



def test_unordered_files(app, capsys):
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
                "This is file 0, line 3\n"
                )

    ARGS = ["test/sample_files/dotlogfile.4.log.gz",
            "test/sample_files/dotlogfile.0.log",
            "test/sample_files/dotlogfile.2.log.gz",
            "test/sample_files/dotlogfile.5.log.gz",
            "test/sample_files/dotlogfile.1.log",
            "test/sample_files/dotlogfile.3.log.gz", ]

    app.run(ARGS)
    assert app.exitcode == 0

    outputs = capsys.readouterr()

    print(outputs.out)

    assert EXPECTED == outputs.out
    assert "" == outputs.err
