import logging
import ctypes

FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool


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


def war(message, color=FOREGROUND_YELLOW):
    set_color(color)
    logger.warn(message)
    set_color(FOREGROUND_WHITE)


def error(message, color=FOREGROUND_RED):
    set_color(color)
    logger.error("【%s】" % message)
    set_color(FOREGROUND_WHITE)


def cri(message):
    logger.critical(message)

