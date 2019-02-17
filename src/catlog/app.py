import logging

from catlog import DEFAULT_REGEX, Errors, KNOWN_COMPRESSIONS, ReportException, VERSION



class App:

    def __init__(self, argv) -> None:
        self.options = None
        self.argv = argv


    def getOptions(self):
        import argparse

        parser = argparse.ArgumentParser(
            description="""
            Prints out a series of rotated log file in decending numerical order. Duplicates are printed out only once.

            Supported compression formats are the following: {}""".format(", ".join(KNOWN_COMPRESSIONS)),
            epilog="Version: {}".format(VERSION),
            )
        parser.add_argument(
            "LOG_PART",
            help="Files containing the rotated parts of the log",
            nargs="+",
            type=str
            )
        parser.add_argument(
            "-d", "--debug",
            help="Output debug information on stderr",
            action="store_true"
            )
        parser.add_argument(
            "-r", "--regex",
            help="""REGEX used to parse the log file number.
            Note that a single file is allowed to have a missing number, in which case it is assigned number -1.
            (Default: "{}")
            """.format(DEFAULT_REGEX),
            type=str,
            default=DEFAULT_REGEX
            )
        self.options = parser.parse_args(self.argv)

        if self.options.debug: self.logger.setLevel(logging.DEBUG)


    def debug(self, fmt, *args):
        self.logger.debug(fmt.format(*args))


    def run(self):
        # Read the options
        self.logger = logging.getLogger()
        self.getOptions()

        # Compile regex
        self.debug("Number regex: {}", self.options.regex)
        try:
            self.regex = re.compile(self.options.regex)
        except Exception as e:
            raise ReportException(Errors.Config, """Invalid Regex: "{}": {}""".format(self.options.regex, e))

        # Sort files and check for duplicate numbers
        files = self.options.LOG_PART
        self.debug("Files provided: {}", ", ".join(files))
        files = ((self.regex.search(f), f) for f in files)
        files = ((m and m.group(1) or "-1", f) for m, f in files)
        files = ((int(n), f) for n, f in files)
        files = sorted(files, reverse=True)

        for i in range(2, len(files), 1):
            if files[i][0] == files[i - 1][0]:
                raise ReportException(Errors.Numbering, "Duplicate number: {} on files {} and {}".format(files[i][0], files[i - 1][1], files[i][1]))

        files = [f for n, f in files]

        self.debug("Files, sorted: {}", ", ".join(files))

        # Output files
        for f in files:
            try:
                self.debug("Processing file: {}", f)
                ext = getExtension(f)
                self.debug("Extension: {}", ext)
                if ext in COMPRESSION_READERS:
                    self.debug("Using {} Compression".format(ext))
                    reader = COMPRESSION_READERS[ext]
                else:
                    reader = partial(open, mode="rt")
                reader = reader(f)
                for l in reader:
                    print(l, end="")
            except Exception as e:
                raise ReportException(Errors.IO, "Error reading {}: {}".format(f, e))
