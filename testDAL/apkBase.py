__author__ = 'shikun'
from math import  floor
import subprocess
import os

class ApkInfo():

    appSize = ''
    appVersion = ''
    packageName = ''
    launcherActivity = ''

    def __init__(self, apkpath):
        self.apkpath = apkpath

    # 得到app的文件大小
    def get_apk_size(self):
        if not ApkInfo.appSize:
            ApkInfo.appSize = floor(os.path.getsize(self.apkpath)/(1024*1000))
        return str(ApkInfo.appSize) + "M"

    # 得到版本
    def get_apk_version(self):
        if not ApkInfo.appVersion:
            cmd = "aapt dump badging " + self.apkpath + " | findstr versionName"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            if output != "":
                ApkInfo.appVersion = output.decode().split()[3].replace("versionName=", "").replace("'", "")
        return ApkInfo.appVersion

    #得到应用名字
    def get_apk_name(self):
        # cmd = "aapt dump badging " + self.apkpath + " | findstr application-label-zh-CN: "
        # result = ""
        # p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
        #                      stderr=subprocess.PIPE,
        #                      stdin=subprocess.PIPE, shell=True)
        # (output, err) = p.communicate()
        # if output != "":
        #     result = output.split()[0].decode()[24:]
        return self.get_apk_pkg()

    #得到包名
    def get_apk_pkg(self):
        if not ApkInfo.packageName:
            cmd = "aapt dump badging " + self.apkpath + " | findstr package:"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            if output != "":
                ApkInfo.packageName = output.decode().split()[1].replace("name=", "").replace("'", "")
        return ApkInfo.packageName

    #得到启动类
    def get_apk_activity(self):
        if not ApkInfo.launcherActivity:
            cmd = "aapt dump badging " + self.apkpath + " | findstr launchable-activity:"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            if output != "":
                ApkInfo.launcherActivity = output.decode().split()[1].replace("name=", "").replace("'", "")

        return ApkInfo.launcherActivity

if __name__ == '__main__':
    print(ApkInfo(r"C:\Users\Administrator\Desktop\4.1.1外部渠道包\kaihu_V4.10.01_20160427_f1852c4_3gcn.apk").get_apk_pkg())
    print(ApkInfo(r"C:\Users\Administrator\Desktop\4.1.1外部渠道包\kaihu_V4.10.01_20160427_f1852c4_3gcn.apk").get_apk_version())
    print(ApkInfo(r"C:\Users\Administrator\Desktop\4.1.1外部渠道包\kaihu_V4.10.01_20160427_f1852c4_3gcn.apk").get_apk_name())
    print(ApkInfo(r"C:\Users\Administrator\Desktop\4.1.1外部渠道包\kaihu_V4.10.01_20160427_f1852c4_3gcn.apk").get_apk_activity())



