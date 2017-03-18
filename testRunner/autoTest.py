from testBLL import appCase as b_app_case
from testMode import appCase as m_app_case
from testRunner.runnerBase import TestInterfaceCase as te


class AutoTest(te):

    def setUp(self):
        super(AutoTest, self).setUp()
        self.bc = b_app_case.GetAppCase(test_module=self.device['module_case']['moduleName'], GetAppCaseInfo=m_app_case.GetAppCaseInfo,
                                        GetAppCase=m_app_case.GetAppCase, fps=[], cpu=[], men=[],
                                        driver=self.driver, package=self.package_name(),
                                        devices=self.device["deviceName"])

    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()
        pass

    def testModule(self):
        cases = self.device['module_case']['cases']
        for i in range(len(cases)):
            case = cases[i]
            self.bc.execCase(case['casePath'], test_name=case['caseName'], isLast="1" if len(cases) == i + 1 else "0")

