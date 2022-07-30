import logging

from settings.settings import settings


def get_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter(fmt=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')

    cls_handler = logging.StreamHandler()
    cls_handler.setFormatter(formatter)
    cls_handler.setLevel(logging.DEBUG if not settings.production else logging.WARNING)

    file_handler = logging.FileHandler(settings.logging_file_name)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG if not settings.production else logging.INFO)

    logger = logging.getLogger(name)

    logger.addHandler(cls_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger
