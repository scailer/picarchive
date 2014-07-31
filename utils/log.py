from django.utils.termcolors import colorize
import logging

LOG_COLOR = {
    'DEBUG': 'blue',
    'INFO': 'yellow',
    'ERROR': 'red',
    'WARNING': 'magenta',
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        result = logging.Formatter.format(self, record)
        if record.levelname in LOG_COLOR:
            result = colorize(result, fg=LOG_COLOR[record.levelname])
        return result
