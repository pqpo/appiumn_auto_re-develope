__author__ = 'shikun'
import math
from common import log


def phone_avg_use_cpu(cpu):
    result = "0%"
    if len(cpu) > 0:
        result = "%.1f" % (sum(cpu) / len(cpu)) + "%"
    return result


def phone_avg_use_raw(men):
    result = "0M"
    if len(men) > 0:
        result = str(math.ceil(sum(men) / len(men) / 1024)) + "M"
    return result


def phone_max_use_raw(l_men):
    result = "0M"
    if len(l_men) > 0:
        result = str(math.ceil((max(l_men)) / 1024)) + "M"
    return result


def phone_max_use_cpu(cpu):
    result = "0%"
    if len(cpu):
        result = str(max(cpu)) + "%"
    return result


def phone_raw(raw):
    result = "0M"
    if raw > 0:
        result = str(math.ceil(raw)) + "M"
    return result


# def fps_max(d_fps):
#     log.info("fps_max1 %s" % d_fps)
#     try:
#         if len(d_fps) > 0:
#             return str(max(d_fps))
#     except:
#         pass
#     return "0"


# def fps_avg(d_fps):
#     log.info("fps_avg1 %s" % d_fps)
#     result = 0
#     try:
#         if len(d_fps) > 0:
#             result = float(str(math.ceil(sum(d_fps) / len(d_fps))))
#             return '%.2f' % result
#     except:
#         pass
#     return result



