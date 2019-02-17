import logging
import sys

from catlog import ReportException
from catlog.app import App



def main():
    app = App()
    try:
        exit(app.run())
    except ReportException as e:
        msg = str(e)
        logging.critical(msg)
        exit(e.code)



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, style="{", format="{levelname}: {msg}")
    main()