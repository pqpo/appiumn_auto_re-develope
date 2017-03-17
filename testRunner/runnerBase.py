__author__ = 'shikun'
# -*- coding: utf-8 -*-
import unittest
from appium import webdriver
from common.variable import GetVariable as common
import os
from selenium import webdriver as web
from testBLL import  apkBase


def appium_test_case(device):
    app_path = device["appPath"]
    apk_base = apkBase.apkInfo(app_path)
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
    common.PACKAGE = apk_base.get_apk_pkg()
    remote = "http://127.0.0.1:" + str(device["port"]) + "/wd/hub"
    driver = webdriver.Remote(remote, desired_caps)
    # common.DRIVER = driver
    # common.FLAG = False
    return driver


def selenium_testcase(get_devices):
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = web.Chrome(chromedriver)
    # driver = web.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)
    common.DRIVER = driver
    common.FLAG = False
    driver.maximize_window()  #将浏览器最大化
    driver.get(get_devices.open_url)


class TestInterfaceCase(unittest.TestCase):

    def __init__(self, methodName='runTest', device=None):
        super(TestInterfaceCase, self).__init__(methodName)
        self.device = device

    @staticmethod
    def setUpClass():
        # global driver
        # ga = get_evices()
        # common.SELENIUM_APPIUM = ga.selenium_appium
        # if common.SELENIUM_APPIUM == common.APPIUM: # appium入口
        #     if ga.platformName == common.ANDROID and common.FLAG:
        #         appium_testcase(ga)
        # if common.SELENIUM_APPIUM == common.SELENIUM and common.FLAG: # selenium入口
        #     selenium_testcase(ga)
        #     # driver.get("http://www.baidu.com")
        #     # data = driver.title
            pass

    def setUp(self):
        if self.device["platformName"] == common.ANDROID:
            self.driver = appium_test_case(self.device)

    def tearDown(self):
        # self.driver.close_app()
        # self.driver.quit()
        pass

    def package_name(self):
        return apkBase.apkInfo(self.device['appPath']).get_apk_pkg()

    @staticmethod
    def tearDownClass():
        # driver.close_app()
        # driver.quit()
        print('tearDownClass')

    @staticmethod
    def parametrize(testcase_klass, device=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, device=device))
        return suite


