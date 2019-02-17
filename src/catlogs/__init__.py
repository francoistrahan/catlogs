from enum import Enum
from functools import partial
import gzip
import re



VERSION = "1.2.0"



class Errors(Enum):
    Config = -1
    Numbering = -2
    IO = 1



class ReportException(Exception):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code



COMPRESSION_READERS = {
    "gz": partial(gzip.open, mode="rt")
    }

KNOWN_COMPRESSIONS = sorted(COMPRESSION_READERS.keys())

DEFAULT_REGEX = r"""([0-9]+)"""

EXTENSION_REGEX = re.compile(r"""^.*\.([^.]+)$""")



def getExtension(filepath):
    m = EXTENSION_REGEX.match(filepath)
    if m:
        return m.group(1)
    else:
        return None
