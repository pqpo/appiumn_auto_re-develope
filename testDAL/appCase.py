__author__ = 'shikun'
# -*- coding: utf-8 -*-
import json
from common import operateYaml, appPerformance as ap, operateElement as bo
from common.variable import Constants as common
from common import screenShots
from common import reportPhone as rp
from testBLL import phoneBase as ba
import os
from common import operateFile
import time
from common import log


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
IS_CRASH = 1  # 闪退了
NO_ELEMENT = 2  # 找不到元素
NORMAL = 0  # 正常


class AppCase:

    def __init__(self, **kwargs):
        '''

        :param kwargs:
        test_module:'模块名'
        GetAppCaseInfo: '用例介绍'
        GetAppCase: 'app case'
        fps: []
        cpu: []
        men: []
        driver:
        package： 包名
        devices: 设备名
        '''
        self.crashLog = kwargs["crashLog"]
        self.test_module = kwargs["test_module"]
        self.GetAppCaseInfo = kwargs["GetAppCaseInfo"]
        self.GetAppCase = kwargs["GetAppCase"]
        self.driver = kwargs["driver"]
        self.package = kwargs["package"]
        self.device = kwargs["device"]
        # self.fps = kwargs["fps"]
        self.cpu = kwargs["cpu"]
        self.men = kwargs["men"]

    def get_phone_name(self):
        get_phone = ba.get_phone_info(devices=self.device)
        phone_name = get_phone["brand"] + "_"+"android" + "_" + get_phone["release"]
        return phone_name, get_phone["device"]  # 这里的device就是设备名

    def getModeList(self, f):
        bs = []
        gh = operateYaml.get_yaml(f)
        for i in range(len(gh)):
            if i == 0:
                # 用例id
                self.GetAppCaseInfo.test_id = gh[i].get(common.TEST_ID, "false")
                # 用例介绍
                self.GetAppCaseInfo.test_desc = gh[i].get(common.TEST_DESC, "false")

            self.GetAppCase.element_info = gh[i].get(common.ELEMENT_INFO, "false")

            # 操作类型
            self.GetAppCase.operate_type = gh[i].get(common.OPERATION_TYPE, "false")

            self.GetAppCase.index = gh[i].get(common.FIND_ELEMENTS_INDEX, "false")

            self.GetAppCase.text = gh[i].get(common.SEND_KEY_TEXT, "false")

            # 验证类型
            self.GetAppCase.find_type = gh[i].get(common.FIND_TYPE, "false")

            self.GetAppCase.times = gh[i].get(common.SWIPE_TIMES, 1)

            self.GetAppCase.timeout = gh[i].get(common.WAITE_TIMEOUT, common.DEFAULT_TIMEOUT)

            self.GetAppCase.point = gh[i].get(common.TAP_POINT, [-1, -1])

            self.GetAppCase.direction = gh[i].get(common.SWIPE_DIRECTION, common.SWIPE_DIRECTION_TO_LEFT)

            bs.append(json.loads(json.dumps(self.GetAppCase().to_primitive())))
        return bs

    def execCase(self, f, **kwargs):
        '''

        :param f: 用例文件
        :param kwargs:
        test_name: 用例名
        is_last: 最后一个用例 1, 0
        :return:
        '''
        bc = self.getModeList(f)
        go = bo.OperateElement(driver=self.driver)
        ch_check = bc[-1]
        if self.crashLog:
            ba.remove_file(self.device, self.crashLog)
        _d_report_common = {"test_success": 0, "test_failed": 0, "test_sum": 0} #case的运行次数和性能
        operate_result = NORMAL  # 0表示没有闪退，1标识有闪退，2标识没有闪退，找不到页面元素
        ng_img = None
        for k in bc:
            if k[common.OPERATION_TYPE] != "false":
                # 单个case的情况收集
                self.cpu.append(ap.top_cpu(devices=self.device, pkg_name=self.package))
                self.men.append(ap.get_men(devices=self.device, pkg_name=self.package))
                # self.fps.append(ap.get_fps(devices=self.device, pkg_name=self.package))
                _operate = go.operate_element(k)
                if len(self.pull_crash_log()) > 0:
                    operate_result = IS_CRASH
                    ng_img = screenShots.screen_shot(case_name=kwargs["test_name"], driver=self.driver, result_path=common.SCREEN_IMG_PATH)
                    break
                elif not _operate:
                    operate_result = NO_ELEMENT
                    ng_img = screenShots.screen_shot(case_name=kwargs["test_name"], driver=self.driver, result_path=common.SCREEN_IMG_PATH)
                    break
                time.sleep(2)
        _d_report_common["test_sum"] += 1
        if ng_img is None:
            ng_img = screenShots.screen_shot(case_name=kwargs["test_name"], driver=self.driver, result_path=common.SCREEN_IMG_PATH)
        self.report(go, ch_check, _d_report_common, kwargs, operate_result, ng_img)

    def report(self, go, ch_check, _d_report_common, kwargs, operate_result, ng_img):

        self.GetAppCaseInfo.test_men_max = rp.phone_max_use_raw(self.men)  # 内存最大使用情况
        self.GetAppCaseInfo.test_men_avg = rp.phone_avg_use_raw(self.men)  # 内存平均使用
        self.GetAppCaseInfo.test_cpu_max = rp.phone_max_use_cpu(self.cpu)  # cpu最大使用
        self.GetAppCaseInfo.test_cpu_avg = rp.phone_avg_use_cpu(self.cpu)  # cpu平均使用
        # self.GetAppCaseInfo.test_fps_max = rp.fps_max(self.fps)
        # self.GetAppCaseInfo.test_fps_avg = rp.fps_avg(self.fps)
        self.GetAppCaseInfo.test_image = ng_img
        log.info("mem: %s" % str(self.men))
        log.info("cpu: %s" % str(self.cpu))

        d_report = {}
        raw = ba.get_men_total(devices=self.device)
        d_report["phone_name"] = self.get_phone_name()[0]
        d_report["phone_pix"] = ba.get_app_pix(self.device)
        d_report["phone_cpu"] = ba.get_cpu_kel(self.device)
        d_report["phone_raw"] = rp.phone_raw(raw / 1024)

        if operate_result == NORMAL:  # 正常情况
            if go.findElement(ch_check):
                _d_report_common["test_success"] += 1
                self.GetAppCaseInfo.test_result = "成功"
                self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
            else:
                _d_report_common["test_failed"] += 1
                test_reason = "检查不到元素"
                self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
                self.GetAppCaseInfo.test_result = "失败"
                self.GetAppCaseInfo.test_reason = test_reason
        elif operate_result == IS_CRASH:  # 如果闪退了
            _d_report_common["test_failed"] += 1
            self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
            self.GetAppCaseInfo.test_result = "失败"
            self.GetAppCaseInfo.test_reason = "崩溃了"
            self.GetAppCaseInfo.test_log = self.pull_crash_log()  # 记录本地日志
        elif operate_result == NO_ELEMENT:  # 找不到元素
            _d_report_common["test_failed"] += 1
            self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
            self.GetAppCaseInfo.test_result = "失败"
            self.GetAppCaseInfo.test_reason = "找不到元素"
        self.GetAppCaseInfo.test_name = kwargs["test_name"]
        self.GetAppCaseInfo.test_module = self.test_module
        self.GetAppCaseInfo.test_phone_name = self.get_phone_name()[0]
        info_case = json.loads(json.dumps(self.GetAppCaseInfo().to_primitive()))
        self.write_detail(info_case, f=common.REPORT_INFO_PATH, key="info")  # 写入所有的case包括，init,info中的excel中的case情况
        if kwargs["isLast"] == "1":
            # 记录每个设备的case运行情况
            if operate_result == NORMAL: # 如果没有闪退了
                d_report["phone_avg_use_cpu"] = self.GetAppCaseInfo.test_cpu_avg
                d_report["phone_max_use_cpu"] = self.GetAppCaseInfo.test_cpu_max
                d_report["phone_avg_use_raw"] = self.GetAppCaseInfo.test_men_avg
                d_report["phone_max_use_raw"] = self.GetAppCaseInfo.test_men_max
                # d_report["fps_avg"] = self.GetAppCaseInfo.test_fps_avg
                # d_report["fps_max"] = self.GetAppCaseInfo.test_fps_max
            else:
                d_report["phone_avg_use_cpu"] = "0"
                d_report["phone_max_use_cpu"] = "0"
                d_report["phone_avg_use_raw"] = "0"
                d_report["phone_max_use_raw"] = "0"
                # d_report["fps_avg"] = "0"
                # d_report["fps_max"] = "0"
            # 最后case要写最下面的统计步骤
            self.write_detail(d_report, f=common.REPORT_INIT, key="init")

    def read_detail_report(self, f=""):
       op = operateFile.OperateFile(f, "r")
       return op.read_txt_row()

    # 写入统计case的info,init情况
    def write_detail(self, json, f="", key="info"):
        '''

        :param json: 存储的json
        :param f: 存储的文件文字，一般是info,和init的位置
        :param key:  info和init两个值,要和f的路径匹配;REPORT_INFO_PATH对应info,REPORT_INIT对应init
        这里的key就是init,当f的值为REPORT_INFO_PATH,这里
        :return:
        '''
        _read_json_temp = self.read_detail_report(f)
        _result = {}
        if len(_read_json_temp) > 0:
            _read_json = eval(_read_json_temp)
            _read_json[key].append(json)
            _result = _read_json
        else:
            _result[key] = []
            _result[key].append(json)
        op = operateFile.OperateFile(f, "w")
        op.write_txt(str(_result))
        log.info(_result)

    # 写入统计总的case的运行次数
    def write_report_collect(self, json, f=""):
        _read_json_temp = self.read_detail_report(f)
        op = operateFile.OperateFile(f, "w")
        _result = {}
        if len(_read_json_temp) > 0:
            _read_json = eval(_read_json_temp)
            for i in _read_json:
                if i == "test_success" or i == "test_failed" or i == "test_sum":  # 统计总的case的运行次数
                    _result[i] = int(_read_json[i]) + int(json[i])
                else:
                    _result[i] = _read_json[i]
        if len(_result) > 0:
            op.write_txt(str(_result))
        else:
            op.write_txt(str(json))

    def pull_crash_log(self):
        crash_log = ""
        if self.crashLog:
            crash_log = ba.read_file(self.device, self.crashLog)
            if len(crash_log) > 0:
                log.info("crash log: %s" % crash_log)
        return crash_log
