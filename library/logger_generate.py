import sys
import random
import string
import logging.handlers
from pathlib import Path

import coloredlogs


def generate(logger_config, name='', need_serial=False, **kwargs):
    """
    logger_config is like to
    {
        "logging_level": "INFO",  # DEBUG # INFO # ERROR # WARNING
        "log_file_path": './logs/example',
        "log_format": '%(asctime)s - %(levelname)s : %(message)s',
        "backupCount": 7,
        "when": 'D',
        "encoding": 'utf-8',
    }
    need_serial just a boolean
    if True, will generate have serial logger
    """

    if 'need_serial' in kwargs:
        need_serial = kwargs['need_serial']

    if not Path(logger_config['log_file_path']).exists():
        try:
            Path(logger_config['log_file_path']).parents[0].mkdir()
        except Exception as e:
            e  # 應付 pep8

    if name == '':
        name = __name__
    if need_serial:
        rdt_len = 5
        rdt = ''.join(random.choice(string.ascii_letters + string.digits)
                      for x in range(rdt_len))
        logger = logging.getLogger(name + '_' + rdt)
    else:
        logger = logging.getLogger(name)
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
