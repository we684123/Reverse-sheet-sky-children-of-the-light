import sys
import logging.handlers
import coloredlogs
from pathlib import Path


def generator(logger_config):
    if not Path(logger_config['log_file_path']).exists():
        Path(logger_config['log_file_path']).parents[0].mkdir()
    logger = logging.getLogger(__name__)
    handler1 = logging.StreamHandler(sys.stdout)
    handler2 = logging.handlers.TimedRotatingFileHandler(
        filename=logger_config['log_file_path'],
        when=logger_config['when'],
        encoding=logger_config['encoding'],
        backupCount=logger_config['backupCount'],
    )
    formatter = logging.Formatter(logger_config['log_format'])
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)

    logging_level = logger_config['logging_level']
    logger.setLevel(logging_level)
    handler1.setLevel(logging_level)
    handler2.setLevel(logging_level)

    logger.addHandler(handler1)
    logger.addHandler(handler2)

    coloredlogs.install(level=logging_level, logger=logger)
    return logger
    #  ===== logger設定完畢 =====
