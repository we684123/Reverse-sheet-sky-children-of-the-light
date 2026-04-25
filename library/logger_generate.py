import logging.handlers
import random
import string
import sys
from pathlib import Path
from typing import Any

import coloredlogs


def generate(logger_config: dict[str, Any], name: str = "", need_serial: bool = False, **kwargs: Any) -> logging.Logger:
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

    if "need_serial" in kwargs:
        need_serial = kwargs["need_serial"]

    log_file_path = Path(logger_config["log_file_path"])
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    if name == "":
        name = __name__
    if need_serial:
        rdt_len = 5
        rdt = "".join(random.choice(string.ascii_letters + string.digits) for x in range(rdt_len))
        logger = logging.getLogger(name + "_" + rdt)
    else:
        logger = logging.getLogger(name)
    handler1 = logging.StreamHandler(sys.stdout)
    handler2 = logging.handlers.TimedRotatingFileHandler(
        filename=log_file_path,
        when=logger_config["when"],
        encoding=logger_config["encoding"],
        backupCount=logger_config["backupCount"],
    )
    formatter = logging.Formatter(logger_config["log_format"])
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)

    logging_level = logger_config["logging_level"]
    logger.setLevel(logging_level)
    handler1.setLevel(logging_level)
    handler2.setLevel(logging_level)

    logger.addHandler(handler1)
    logger.addHandler(handler2)

    coloredlogs.install(level=logging_level, logger=logger)
    return logger
    #  ===== logger設定完畢 =====
