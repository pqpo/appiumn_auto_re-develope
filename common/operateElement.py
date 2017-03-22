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
        operation_type = operate[common.OPERATION_TYPE]
        if operation_type == common.OPERATION_TYPE_SWIPE:
            return True
        if operation_type == common.OPERATION_TYPE_SWIPE_UNTIL:
            return True
        if operation_type == common.OPERATION_TYPE_WAITE and operate[common.ELEMENT_INFO] == 'false':
            return True
        if operation_type == common.OPERATION_TYPE_TAP:
            return True
        find = wait_until_elements(operate, self.driver)
        if not find:
            log.error("未匹配到输入元素：%s" % operate)
        return find

    def operate_element(self, operate):
        if self.findElement(operate):
            elements = {
                common.OPERATION_TYPE_CLICK: lambda: operate_click(operate, self.driver),
                common.OPERATION_TYPE_SEND_KEYS: lambda: send_keys(operate, self.driver),
                common.OPERATION_TYPE_SWIPE: lambda: operate_swipe(self.driver, operate[common.SWIPE_DIRECTION], operate[common.SWIPE_TIMES]),
                common.OPERATION_TYPE_WAITE: lambda: operate_wait(operate[common.WAITE_TIMEOUT]),
                common.OPERATION_TYPE_TAP: lambda: operate_tap(operate, self.driver),
                common.OPERATION_TYPE_SWIPE_UNTIL: lambda: operate_swipe_until(operate, self.driver)
            }
            return elements[operate[common.OPERATION_TYPE]]()
        return False


def wait_until_elements(operate, driver, timeout=common.DEFAULT_TIMEOUT):
    try:
        WebDriverWait(driver, timeout).until(
            lambda x: elements_by(driver, operate[common.FIND_TYPE], operate[common.ELEMENT_INFO],
                                  operate.get(common.FIND_ELEMENTS_INDEX, 0)))
        return True
    except WebDriverException:
        return False


def operate_swipe_until(operate, driver):
    times = 0
    max_times = operate.get(common.SWIPE_TIMES, 5)
    while times < max_times and (not wait_until_elements(operate, driver, 2)):
        operate_swipe(driver, operate[common.SWIPE_DIRECTION])
        times = + 1
    time.sleep(2)
    find = wait_until_elements(operate, driver)
    if not find:
        log.error("未匹配到输入元素：%s" % operate)
    return find


def operate_wait(timeout=common.DEFAULT_TIMEOUT):
    time.sleep(timeout)
    return True


# 滑动
def operate_swipe(cts, direction, swipe_time=1):
    time.sleep(1)
    width = cts.get_window_size()["width"]
    height = cts.get_window_size()["height"]
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    if direction == common.SWIPE_DIRECTION_TO_LEFT:
        start_x = width / 4 * 3
        start_y = height / 2
        end_x = width / 4
        end_y = height / 2
    elif direction == common.SWIPE_DIRECTION_TO_RIGHT:
        start_x = width / 4
        start_y = height / 2
        end_x = width / 4 * 3
        end_y = height / 2
    elif direction == common.SWIPE_DIRECTION_TO_TOP:
        start_x = width / 2
        start_y = height / 4 * 3
        end_x = width / 2
        end_y = height / 4
    elif direction == common.SWIPE_DIRECTION_TO_BOTTOM:
        start_x = width / 2
        start_y = height / 4
        end_x = width / 2
        end_y = height / 4 * 3
    for i in range(swipe_time):
        cts.swipe(start_x, start_y, end_x, end_y, 800)
        time.sleep(1)
    return True


# 轻点
def operate_tap(operate, driver):
    point_x = operate[common.TAP_POINT][0]
    point_y = operate[common.TAP_POINT][1]
    width = driver.get_window_size()["width"]
    height = driver.get_window_size()["height"]
    if (point_x == -1 and point_y == -1) or not point_x or not point_y:
        point_x = width / 2
        point_y = height / 2
    if 0 < point_x < 1:
        point_x = width * point_x
    if 0 < point_y < 1:
        point_y = height * point_y
    points = [(point_x, point_y)]
    driver.tap(points, duration=500)
    return True


def send_keys(operate, driver):
    elements_by(driver, operate[common.FIND_TYPE], operate[common.ELEMENT_INFO],
                operate.get(common.FIND_ELEMENTS_INDEX, 0)).send_keys(operate[common.SEND_KEY_TEXT])
    return True


# 点击事件
def operate_click(operate, driver):
    elements_by(driver, operate[common.FIND_TYPE], operate[common.ELEMENT_INFO],
                operate.get(common.FIND_ELEMENTS_INDEX, 0)).click()
    return True


# 封装常用的标签
def elements_by(cts, find_type, element_info, index=0):
    elements = {
        common.FIND_TYPE_BY_ID: lambda: cts.find_element_by_id(element_info),
        common.FIND_TYPE_BY_IDS: lambda: cts.find_elements_by_id(element_info),
        common.FIND_TYPE_BY_XPATH: lambda: cts.find_element_by_xpath(element_info),
        common.FIND_TYPE_BY_NAME: lambda: cts.find_element_by_name(element_info),
        common.FIND_TYPE_BY_NAMES: lambda: cts.find_elements_by_name(element_info)[index],
        common.FIND_TYPE_BY_CLASS_NAME: lambda: cts.find_element_by_class_name(element_info),
        common.FIND_TYPE_BY_CLASS_NAMES: lambda: cts.find_elements_by_class_name(element_info)[index],
    }
    return elements[find_type]()
