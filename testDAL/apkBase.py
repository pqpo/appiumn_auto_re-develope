__author__ = 'shikun'
from math import  floor
import subprocess
import os
import re


class ApkInfo:

    def __init__(self, apkpath):
        self.apkpath = apkpath
        self.dump_badging = None

    def get_dump_badging(self):
        if not self.dump_badging:
            (output, err) = subprocess.Popen("aapt dump badging " + self.apkpath, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE, shell=True).communicate()
            if output:
                self.dump_badging = output.decode()
        return self.dump_badging


    # 得到app的文件大小
    def get_apk_size(self):
        return str("%.2f" % (os.path.getsize(self.apkpath)/(1024*1000))) + "M"

    # 得到版本
    def get_apk_version(self):
        result = "Unknown"
        dump = self.get_dump_badging()
        if dump:
            match = re.compile("versionName='(.+?)'").search(dump)
            if match:
                result = match.group(1)
        return result

    # 得到应用名字
    def get_apk_name(self):
        return self.get_apk_pkg().split(".")[-1]

    # 得到包名
    def get_apk_pkg(self):
        result = "Unknown"
        dump = self.get_dump_badging()
        if dump:
            match = re.compile("package: name='(.+?)'").search(dump)
            if match:
                result = match.group(1)
        return result

    # 得到启动类
    def get_apk_activity(self):
        result = "Unknown"
        dump = self.get_dump_badging()
        if dump:
            match = re.compile("launchable-activity: name='(.+?)'").search(dump)
            if match:
                result = match.group(1)
        return result

if __name__ == '__main__':
    apkInfo = ApkInfo(r"C:\Users\Administrator\Desktop\4.1.1外部渠道包\kaihu_V4.10.01_20160427_f1852c4_3gcn.apk")
    print(apkInfo.get_apk_version())
    print(apkInfo.get_apk_size())
    print(apkInfo.get_apk_pkg())
    print(apkInfo.get_apk_name())
    print(apkInfo.get_apk_activity())
    pass



