# -*- coding: utf-8 -*-
import sys
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
sys.path.append(PATH('../'))
import datetime
import xlsxwriter
import time
import unittest
from testRunner.runnerBase import TestInterfaceCase
from testBLL import email as b_email
from testBLL import server
from testBLL import adbCommon
from testMode import email as m_email
from testBLL import report as b_report
from testBLL import phoneBase
from common.variable import Constants
from common import dataToString
from testBLL import apkBase
from multiprocessing import Pool
from common import operateFile
from common import operateYaml
from http.server import HTTPServer
from common import myserver
from common import log
from multiprocessing import Process
import subprocess
from testRunner.autoTest import AutoTest


data = {"init": [], "info": []}

def get_devices():
    return operateYaml.get_yaml(PATH("../devices.yaml"))


def get_email():
    m_m_email = m_email.GetEmail()
    m_m_email.file = PATH('../email.ini')
    email = b_email.read_email(m_m_email)
    return email


def read_report(f=""):
    op = operateFile.OperateFile(f, "r")
    return op.read_txt_row()


# 得到总统计的case
def get_report_collect(start_test_time, endtime, starttime, device):
    _read_collect_json = eval(read_report(Constants.REPORT_COLLECT_PATH))
    for key in _read_collect_json:
        data[key] = _read_collect_json[key]
    apk_msg = apkBase.ApkInfo(device["appPath"])
    data["app_name"] = apk_msg.get_apk_name()
    data["app_size"] = apk_msg.get_apk_size()
    data["app_version"] = apk_msg.get_apk_version()
    data["test_sum_date"] = str((endtime - starttime).seconds) + "秒"
    data["test_date"] = start_test_time


# 得到每个设备的的case 运行情况
def get_report_init():
    data["init"] = eval(read_report(Constants.REPORT_INIT))["init"]


# 得到每个case的运行情况
def get_report_info():
    data["info"] = eval(read_report(Constants.REPORT_INFO_PATH))["info"]


def get_common_report(start_test_time, end_time, start_time, device):
    get_report_collect(start_test_time, end_time, start_time, device)
    get_report_init()
    get_report_info()


def runner_pool(module_case_yaml):
    module_case = operateYaml.get_yaml(module_case_yaml)
    devices_pool = []
    for i in range(0, len(ga["appium"])):
        device = {}
        item = ga["appium"][i]
        device["appPath"] = item["app"]
        device["resetApp"] = False
        if 'resetApp' in item:
            device["resetApp"] = item["resetApp"] == 1
        device["deviceName"] = item["devices"]
        device["platformVersion"] = phoneBase.get_phone_info(devices=item["devices"])["release"]
        device["platformName"] = item["platformName"]
        device["port"] = item["port"]
        device["module_case"] = module_case
        devices_pool.append(device)
    pool = Pool(len(devices_pool))
    pool.map(case_runner, devices_pool)
    pool.close()
    pool.join()


def case_runner(device):
    start_test_time = dataToString.getStrTime(time.localtime(), "%Y-%m-%d %H:%M %p")
    start_time = datetime.datetime.now()
    suite = unittest.TestSuite()
    suite.addTest(TestInterfaceCase.parametrize(AutoTest, device=device))
    unittest.TextTestRunner(verbosity=2).run(suite)
    end_time = datetime.datetime.now()
    get_common_report(start_test_time, end_time, start_time, device)
    report()


def report():
    workbook = xlsxwriter.Workbook('GetReport.xlsx')
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    log.error(data)
    b_operate_report = b_report.OperateReport(wd=workbook, data=data)
    b_operate_report.init(worksheet)
    b_operate_report.detail(worksheet2)
    b_operate_report.close()
    # b_email.send_mail(get_email())


def open_web_server():
    web_server = HTTPServer((Constants.HOST, Constants.PORT), myserver.myHandler)
    web_server.serve_forever()


def check_module_file(module_file):
    result = True
    module_yaml = operateYaml.get_yaml(PATH(module_file))
    if not module_yaml:
        result = False
    elif "moduleName" not in module_yaml:
        log.error(u"module name 不存在")
        result = False
    elif "cases" not in module_yaml or len(module_yaml["cases"]) == 0:
        log.error(u"cases 不存在")
        result = False
    else:
        cases = module_yaml["cases"]
        for case in cases:
            if "caseName" not in case:
                log.error(u"caseName 不存在")
                result = False
            elif "casePath" not in case:
                log.error(u"casePath 不存在")
                result = False
            elif not operateYaml.get_yaml(case["casePath"]):
                result = False
    return result


if __name__ == '__main__':
    log.info("--------------------------------Start--------------------------------------")
    ga = get_devices()
    case_file = PATH('../module.yaml')
    if len(sys.argv) > 1:
        case_file = sys.argv[1]
    log.info('test module file: %s' % case_file)
    if not check_module_file(case_file):
        pass
    elif adbCommon.attached_devices():
        p = Process(target=open_web_server, args=())
        p.start()

        appium_server = server.AppiumServer(ga)
        appium_server.start_server()
        while not appium_server.is_runnnig():
            time.sleep(2)
        runner_pool(PATH(case_file))
        appium_server.stop_server()
        subprocess.Popen("taskkill /F /T /PID " + str(p.pid), shell=True)
        # web_server.server_close() #关闭webserver
        operateFile.OperateFile(Constants.REPORT_COLLECT_PATH).remove_file()
        operateFile.OperateFile(Constants.REPORT_INIT).remove_file()
        operateFile.OperateFile(Constants.REPORT_INFO_PATH).remove_file()
        operateFile.OperateFile(Constants.CRASH_LOG_PATH).remove_file()
    else:
        log.error(u"设备不存在")
    log.info("--------------------------------End---------------------------------------")
