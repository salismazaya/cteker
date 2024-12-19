import logging

try:
    from colorama import Fore
except ImportError:
    Fore = type(
        'DummyFore',
        (object,),
        {
            'LIGHTYELLOW_EX': '',
            'CYAN': '',
            'RESET': '',
            'YELLOW': '',
            'LIGHTRED_EX': '',
            'RED': ''
        }
    )

from core import constants

class DebugFormatter(logging.Formatter):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: Fore.LIGHTYELLOW_EX + log_format + Fore.RESET,
        logging.INFO: Fore.CYAN + log_format + Fore.RESET,
        logging.WARNING: Fore.YELLOW + log_format + Fore.RESET,
        logging.ERROR: Fore.LIGHTRED_EX + log_format + Fore.RESET,
        logging.CRITICAL: Fore.RED + log_format + Fore.RESET
    }

    def get_log_fmt(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        return log_fmt

    def format(self, record):
        log_fmt = self.get_log_fmt(record)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Formatter(DebugFormatter):
    def get_log_fmt(self, _):
        return self.log_format


logger = logging.getLogger("cteker")

ch = logging.StreamHandler()

if constants.DEBUG:
    ch.setFormatter(DebugFormatter())
    logger.setLevel(level = logging.DEBUG)
else:
    ch.setFormatter(Formatter())
    logger.setLevel(level = logging.ERROR)

logger.addHandler(ch)