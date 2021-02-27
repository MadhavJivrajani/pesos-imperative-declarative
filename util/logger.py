import logging
from logging import Formatter, getLogger, StreamHandler

__all__ = ['setup_logging']

class Color:
	def __init__(self) -> None:
		self.colors = {
			'black'     : 30,
			'red'       : 31,
			'green'     : 32,
			'yellow'    : 33,
			'blue'      : 34,
			'magenta'   : 35,
			'cyan'      : 36,
			'white'     : 37,
			'bgred'     : 41,
			'bggreen'   : 42
		}

		self.prefix = '\033[1;'
		self.suffix = '\033[0m'

	def colorize(self, text, color=None):
		if color not in self.colors:
			color = 'white'

		clr = self.colors[color]
		return (self.prefix+'%dm%s'+self.suffix) % (clr, text)

class CustomFormatter(Formatter):
	def __init__(self) -> None:
		self.colorize = Color().colorize
		self.level_format = "%(levelname)s"
		self.rem_format = " %(asctime)s.%(msecs)03d: %(message)s"

	def format(self, record):
		mapping = {
			'INFO'              : 'cyan',
			'RECONCILE'         : 'yellow',
			'ERROR'             : 'red',
			'CRITICAL'          : 'bgred',
			'STABLE'            : 'green',
            'AWAIT_RECONCILE'   : 'yellow'
		}

		clr = self.colorize(self.level_format, mapping.get(record.levelname, 'white')) \
			+ self.rem_format
		formatter = logging.Formatter(clr, datefmt='%m/%d/%Y %H:%M:%S')

		return formatter.format(record)

def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = CustomFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    logger.setLevel(logging.DEBUG)
    logging.STABLE = 25
    logging.RECONCILE = 26
    logging.AWAIT_RECONCILE = 27

    logging.addLevelName(logging.STABLE, 'STABLE')
    logging.addLevelName(logging.RECONCILE, 'RECONCILE')
    logging.addLevelName(logging.AWAIT_RECONCILE, 'AWAIT_RECONCILE')

    setattr(
        logger,
        'stable',
        lambda message, *args: logger._log(logging.STABLE, message, args)
    )

    setattr(
        logger,
        'reconcile',
        lambda message, *args: logger._log(logging.RECONCILE, message, args)
    )

    setattr(
        logger,
        'awaiting',
        lambda message, *args: logger._log(logging.AWAIT_RECONCILE, message, args)
    )
    return logger
