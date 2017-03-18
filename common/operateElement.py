__author__ = 'shikun'
# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from common.variable import Constants as common
import time
from common import log


# 此脚本主要用于查找元素是否存在，操作页面元素
class OperateElement:

    def __init__(self, driver=None):
        self.driver = driver

    def findElement(self, operate):
        """
        查找元素.operate是字典
        operate_type：对应的操作
        element_info：元素详情
        find_type: find类型
        """
        if operate["operate_type"] == common.OPERATION_TYPE_SWIPE_LEFT:
            return True
        if operate["operate_type"] == common.OPERATION_TYPE_WAITE and operate["element_info"] == 'false':
            return True
        if operate["operate_type"] == common.OPERATION_TYPE_TAP:
            return True
        try:
            WebDriverWait(self.driver, common.WAIT_TIME).until(lambda x: elements_by(operate, self.driver))
            return True
        except WebDriverException:
            log.error("未匹配到输入元素：%s" % operate)
            return False

    def operate_element(self, operate):
        if self.findElement(operate):
            elements = {
                common.OPERATION_TYPE_CLICK: lambda: operate_click(operate, self.driver),
                common.OPERATION_TYPE_SEND_KEYS: lambda: send_keys(operate, self.driver),
                common.OPERATION_TYPE_SWIPE_LEFT: lambda: operate_swipe_left(operate, self.driver),
                common.OPERATION_TYPE_WAITE: lambda: operate_wait(operate),
                common.OPERATION_TYPE_TAP: lambda: operate_tap(operate, self.driver)
            }
            elements[operate["operate_type"]]()
            return True
        return False


def operate_wait(operate):
    sleepTime = common.WAIT_TIME
    if "timeout" in operate:
        sleepTime = operate["timeout"]
    time.sleep(sleepTime)


# 点击事件
def operate_click(operate, cts):
    if operate["find_type"] == common.find_element_by_id or operate["find_type"] == common.find_element_by_name or operate["find_type"] == common.find_element_by_xpath:
        elements_by(operate, cts).click()
    if operate["find_type"] == common.find_elements_by_id or operate["find_type"] == common.find_elements_by_name:
        elements_by(operate, cts)[operate["index"]].click()
    # 记录运行过程中的一些系统日志，比如闪退会造成自动化测试停止
    if common.SELENIUM_APPIUM == common.APPIUM:
        pass


# 左滑动
def operate_swipe_left(operate, cts):
    time.sleep(1)
    width = cts.get_window_size()["width"]
    height = cts.get_window_size()["height"]
    for i in range(operate["time"]):
        cts.swipe(width/4*3, height / 2, width / 4 * 1, height / 2, 500)
        time.sleep(1)
# start_x,start_y,end_x,end_y


# 轻点
def operate_tap(operate, driver):
    point_x = operate['point'][0]
    point_y = operate['point'][1]
    if (point_x == -1 and point_y == -1) or not point_x or not point_y:
        point_x = driver.get_window_size()["width"] / 2
        point_y = driver.get_window_size()["height"] / 2
    points = [(point_x, point_y)]
    driver.tap(points, duration=500)


def send_keys(operate, cts):
    elements_by(operate, cts).send_keys(operate["text"])


# 封装常用的标签
def elements_by(operate, cts):
    elements = {
        common.find_element_by_id: lambda: cts.find_element_by_id(operate["element_info"]),
        common.find_elements_by_id: lambda: cts.find_elements_by_id(operate["element_info"]),
        common.find_element_by_xpath: lambda: cts.find_element_by_xpath(operate["element_info"]),
        common.find_element_by_name: lambda: cts.find_element_by_name(operate['name']),
        common.find_elements_by_name: lambda: cts.find_elements_by_name(operate['name'])[operate['index']],
        common.find_element_by_class_name: lambda: cts.find_element_by_class_name(operate['element_info']),
        common.find_elements_by_class_name: lambda: cts.find_elements_by_class_name(operate['element_info'])[operate['index']]
    }
    return elements[operate["find_type"]]()
