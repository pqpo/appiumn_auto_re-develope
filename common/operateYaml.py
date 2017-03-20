__author__ = 'shikun'
import yaml
from yaml.scanner import ScannerError
from yaml.parser import ParserError
from common import log


# -*- coding:utf-8 -*-
def get_yaml(home_yaml):
    try:
        with open(home_yaml, encoding='utf-8') as f:
            x = yaml.load(f)
            return x
    except FileNotFoundError:
        log.error(u"找不到文件: %s" % home_yaml)
    except ScannerError:
        log.error(u"yaml 格式有误: %s" % home_yaml)
    except ParserError:
        log.error(u"yaml 格式有误: %s" % home_yaml)

