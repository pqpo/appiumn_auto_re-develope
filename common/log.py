import logging


logger = logging.getLogger("test.log")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] : %(message)s', '%Y-%m-%d %H:%M:%S')
# 设置CMD日志
sh = logging.StreamHandler()
sh.setFormatter(fmt)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)


def debug(message):
    logger.debug(message)


def info(message):
    logger.info(message)


def war(message):
    logger.warn(message)


def error(message):
    logger.error("【%s】" % message)


def cri(message):
    logger.critical(message)

