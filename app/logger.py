import logging

from settings.settings import settings


log_format = u'%(filename)s:%(lineno)d #%(levelname)-8s ' \
             u'[%(asctime)s] - %(name)s - %(message)s'


def get_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter(fmt=log_format)

    cls_handler = logging.StreamHandler()
    cls_handler.setFormatter(formatter)
    cls_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(settings.logging_file_name)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.addHandler(cls_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger
