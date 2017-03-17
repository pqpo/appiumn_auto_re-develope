import os
from testBLL import appCase as b_app_case
from testMode import appCase as m_app_case
from testRunner.runnerBase import TestInterfaceCase as te

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class TestLogin(te):

    def setUp(self):
        super(TestLogin, self).setUp()
        self.bc = b_app_case.GetAppCase(test_module="精选页面", GetAppCaseInfo=m_app_case.GetAppCaseInfo,
                                        GetAppCase=m_app_case.GetAppCase, fps=[], cpu=[], men=[],
                                        driver=self.driver, package=self.package_name(),
                                        devices=self.device["deviceName"])

    def home_login(self):
        self.bc.execCase(PATH("yaml/resetLoginCase.yaml"), test_name="test_login", isLast="0")

    def home_logout(self):
        self.bc.execCase(PATH("yaml/logoutCase.yaml"), test_name="test_logout", isLast="1")

    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()
        pass

    @staticmethod
    def tearDownClass():
        pass

    def test_home(self):
        self.home_login()
        self.home_logout()

