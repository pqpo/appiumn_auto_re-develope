__author__ = 'shikun'
# -*- coding: utf-8 -*-
import unittest
from appium import webdriver
from common.variable import Constants
from testBLL import apkBase


def appium_test_case(device):
    app_path = device["appPath"]
    apk_base = apkBase.ApkInfo(app_path)
    desired_caps = {}
    desired_caps['platformName'] = device["platformName"]
    desired_caps['platformVersion'] = device["platformVersion"]
    desired_caps['platformVersion'] = device["platformVersion"]
    desired_caps['deviceName'] = device["deviceName"]
    desired_caps['appPackage'] = apk_base.get_apk_pkg()
    desired_caps['appActivity'] = apk_base.get_apk_activity()
    desired_caps['udid'] = device["deviceName"]
    if device["resetApp"]:
        desired_caps['app'] = app_path
    # desired_caps["unicodeKeyboard"] = "True"
    # desired_caps["resetKeyboard"] = "True"
    # Constants.PACKAGE = apk_base.get_apk_pkg()
    remote = "http://127.0.0.1:" + str(device["port"]) + "/wd/hub"
    driver = webdriver.Remote(remote, desired_caps)
    # common.DRIVER = driver
    # common.FLAG = False
    return driver


class TestInterfaceCase(unittest.TestCase):

    def __init__(self, methodName='runTest', device=None):
        super(TestInterfaceCase, self).__init__(methodName)
        self.device = device

    def setUp(self):
        if self.device["platformName"] == Constants.ANDROID:
            self.driver = appium_test_case(self.device)

    def package_name(self):
        return apkBase.ApkInfo(self.device['appPath']).get_apk_pkg()

    @staticmethod
    def parametrize(test_case_class, device=None):
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(test_case_class)
        suite = unittest.TestSuite()
        for name in test_names:
            suite.addTest(test_case_class(name, device=device))
        return suite


