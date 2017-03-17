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
        self.bc = b_app_case.GetAppCase(test_module="登录", GetAppCaseInfo=m_app_case.GetAppCaseInfo,
                                        GetAppCase=m_app_case.GetAppCase, fps=[], cpu=[], men=[],
                                        driver=self.driver, package=self.package_name(),
                                        devices=self.device["deviceName"])

    def normal_login(self):
        self.bc.execCase(PATH("yaml/normalLoginCase.yaml"), test_name="normal_login", isLast="0")

    def reset_login(self):
        self.bc.execCase(PATH("yaml/resetLoginCase.yaml"), test_name="reset_login", isLast="0")

    def logout(self):
        self.bc.execCase(PATH("yaml/logoutCase.yaml"), test_name="logout", isLast="1")

    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()
        pass

    @staticmethod
    def tearDownClass():
        pass

    def test_home(self):
        self.normal_login()
        self.logout()

