from __future__ import annotations
import logging
import logging.handlers
import os
from traceback import format_exc
from swa_lib import WORK_DIR


class MakeLogging:
    """Class for logging to console and file"""
    fmt = f"\n%(levelname)s %(asctime)s %(message)s"
    log_levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'notset': logging.NOTSET
    }

    def __init__(self, log_file_name: str = 'log.txt'):
        """
        Initialize logging to log_file_name file and console.
        """
        try:
            self.log_file_name = os.path.join(WORK_DIR, 'log', log_file_name)
            self.logger = logging.getLogger(os.path.basename(__file__))
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
            self.logger.setLevel(logging.DEBUG)
            # init console logger with file level
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(logging.Formatter(fmt=self.fmt))
            self.logger.addHandler(ch)
            if self.log_file_name:
                # create log folder if necessary
                log_dir_path = os.path.dirname(self.log_file_name)
                if not os.path.isdir(log_dir_path):
                    os.makedirs(log_dir_path, exist_ok=True)
                # init rotating file logger with 10MB max , 10 max files
                fh = logging.handlers.RotatingFileHandler(self.log_file_name,
                                                          encoding='utf8',
                                                          maxBytes=10_000_000,
                                                          backupCount=10)
                fh.setFormatter(logging.Formatter(fmt=self.fmt))
                fh.setLevel(logging.DEBUG)
                self.logger.addHandler(fh)
        except Exception:
            print(f"Logging initializing error:\n{format_exc()}")
            exit(-1)

    def __call__(self, lvl: str | int, msg: str, *args, **kwargs):
        """Log message

        :param lvl: str. Level of message
        :param msg: str. Text of message
        """
        lvl = self.log_levels[lvl.lower()] if (type(lvl) == str) else lvl
        # log to file
        try:
            self.logger.log(lvl, msg, *args, **kwargs)
        except Exception:
            print(msg)

    def critical(self, msg: str):
        self.__call__(logging.CRITICAL, msg)

    def error(self, msg: str):
        self.__call__(logging.ERROR, msg)

    def warning(self, msg: str):
        self.__call__(logging.WARNING, msg)

    def info(self, msg: str):
        self.__call__(logging.INFO, msg)

    def debug(self, msg: str):
        self.__call__(logging.DEBUG, msg)

    def notset(self, msg: str):
        self.__call__(logging.NOTSET, msg)


log = MakeLogging()
