__author__ = 'shikun'
import math
from common import log


def phone_avg_use_cpu(cpu):
    log.info("phone_avg_use_cpu1 %s" % cpu)
    result = ""
    try:
        if len(cpu) > 0:
           result = str(math.ceil(sum(cpu)/len(cpu))) + "%"
        return result
    except:
        return result


def phone_avg_use_raw(men):
    log.info("phone_avg_use_raw1 %s" % men)
    try:
        if len(men) > 0 :
            return str(math.ceil(sum(men)/len(men))) + "%"
        return 0
    except:
        return 0


def phone_max_use_raw(l_men):
    log.info("phone_max_use_raw1 %s" % l_men )
    print(l_men)
    if len(l_men) > 0:
        return str(math.ceil((max(l_men))/1024)) + "M"
    return "0"


def phone_avg_max_use_cpu(cpu):
    log.info("phone_avg_max_use_cpu1 %s" % cpu)
    print(cpu)
    try:
        if len(cpu):
            return str(max(cpu)) + "%"
        return "0"
    except :
        return "0"


def phone_raw(raw):
    log.info("phone_raw1 %s" % raw)
    if raw > 0:
        return str(math.ceil(raw)) + "M"
    return "0"


def fps_max(d_fps):
    log.info("fps_max1 %s" % d_fps)
    if len(d_fps) > 0:
        return str(max(d_fps))
    return "0"


def fps_avg(d_fps):
    log.info("fps_avg1 %s" % d_fps)
    result = 0
    if len(d_fps) > 0:
        result = float(str(math.ceil(sum(d_fps)/len(d_fps))))
        return '%.2f' % result
    return result


