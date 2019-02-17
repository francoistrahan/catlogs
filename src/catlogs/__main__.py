import logging
import sys

from catlogs import ReportException
from catlogs.app import App



def main():
    logging.basicConfig(stream=sys.stderr, style="{", format="{levelname}: {msg}")

    app = App(sys.argv)
    try:
        exit(app.run())
    except ReportException as e:
        msg = str(e)
        logging.critical(msg)
        exit(e.code)



if __name__ == "__main__":
    main()
