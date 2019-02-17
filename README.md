# Description

When trying to search logs, it is very common on unix system to have logs
rotated, and those older than 2 or 3 rotations. Searching those logs from the
command line can be unpleasant.

This software behaves a bit like "cat", except it does the following:

- It will sort logs according to their numeral extension (descending)
- It will detect compressed files and decompress accordingly

For more info, try `catlogs --help`

# Actually, here is the help :

Well, rather a frozen, unmaintained part of documentation from v1.2.0. Do look at the actual help !

~~~~
usage: catlogs [-h] [-d] [-r REGEX] LOG_PART [LOG_PART ...]

Prints out a series of rotated log file in decending numerical order.
Duplicates are printed out only once. Supported compression formats are the
following: gz

positional arguments:
  LOG_PART              Files containing the rotated parts of the log

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Output debug information on stderr
  -r REGEX, --regex REGEX
                        REGEX used to parse the log file number. Note that a
                        single file is allowed to have a missing number, in
                        which case it is assigned number -1. (Default:
                        "([0-9]+)")
~~~~

# Todo

- Add more compression algorithms
  - xz
  - what else
- Test (and probably handle) errors
