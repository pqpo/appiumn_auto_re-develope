__author__ = 'shikun'
from testDAL import phoneBase


def get_men_total(devices=""):
    return phoneBase.get_men_total(devices)


def get_app_pix(devices):
    return phoneBase.get_app_pix(devices)


def get_phone_info(devices=""):
    return phoneBase.get_phone_info(devices)


def get_cpu_kel(devices=""):
    return phoneBase.get_cpu_kel(devices)


def remove_file(device, file):
    return phoneBase.remove_file(device, file)


def read_file(device, file):
    return phoneBase.read_file(device, file)

