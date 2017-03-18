__author__ = 'shikun'
import os
from common import log


class OperateFile:
    def __init__(self, file, method='w+'):
        self.file = file
        self.method = method
        self.fileHandle = None

    def write_txt(self, line):
        OperateFile(self.file).check_file()
        self.fileHandle = open(self.file, self.method)
        self.fileHandle.write(line + "\n")
        self.fileHandle.close()

    def read_txt_row(self):
        resutl = ""
        if OperateFile(self.file).check_file():
            self.fileHandle = open(self.file, self.method)
            resutl = self.fileHandle.readline()
            self.fileHandle.close()
        return resutl

    def read_txt_rows(self):
        if OperateFile(self.file).check_file():
            self.fileHandle = open(self.file, self.method)
            file_list = self.fileHandle.readlines()
            for i in file_list:
                print(i.strip("\n"))
            self.fileHandle.close()

    def check_file(self):
        if not os.path.isfile(self.file):
            return False
        else:
            return True

    def mkdir_file(self):
        if not os.path.isfile(self.file):
            f = open(self.file, self.method)
            f.close()
            log.info("创建文件成功 %s" % self.file)
        else:
            log.info("文件已经存在 %s" % self.file)

    def remove_file(self):
        if os.path.isfile(self.file):
            os.remove(self.file)
            log.info("删除文件成功 %s" % self.file)
        else:
            log.info("文件不存在 %s" % self.file)

