__author__ = 'shikun'
# -*- coding: utf-8 -*-
import re, os
from common import log

num_re = re.compile("\d+\.?\d*")


# 常用的性能监控
def top_cpu(devices, pkg_name):
    cmd = "adb -s "+devices+" shell dumpsys cpuinfo | findstr " + pkg_name+":"
    get_cmd = os.popen(cmd).read()
    match = re.compile(pkg_name + ":\s+(\d+\.?\d*)%").search(get_cmd)
    result = 0.0
    if match:
        try:
            result = float(match.group(1))
        except:
            log.war("获取失败：" + str(result))
    return result


# 得到men的使用情况
def get_men(devices, pkg_name):
    cmd = "adb -s "+devices+" shell  dumpsys  meminfo %s"  %(pkg_name)
    get_cmd = os.popen(cmd).read()
    match = re.compile("TOTAL:\s*(\d+)").search(get_cmd)
    result = 0
    if match:
        try:
            result = int(match.group(1))
        except:
            log.war("获取失败：" + str(result))
    return result


# 得到fps
# def get_fps(devices, pkg_name):
#     _adb = "adb -s "+devices+" shell dumpsys gfxinfo %s | findstr -A 128 'Execute'  | findstr -v '[a-Z]' "%pkg_name
#     result = os.popen(_adb).read().strip()
#     result = result.split('\r\n')
#     # r_result = [] # 总值
#     # t_result = [] # draw,Process,Execute分别的值
#     # f_sum = 0
#     for i in result:
#         l_result = i.split('\t')[-3:]
#         f_sum = 0
#         for j in l_result:
#             r = re.search(r"\d+\.\d+", str(j))
#             if r:
#                 f_sum += float(r.group())
#             # t_result.append('%.2f'%f_sum)
#         return float('%.2f' % f_sum)
    # print(r_result)
    # print(t_result)
# get_phone_info("MSM8926")

# 取到流量后可以用步骤后的流量减去步骤前的流量得到步骤消耗流量！也可以用时间差来计算！
# def getFlow(pid="31586"):
#     flow_info = os.popen("adb shell cat /proc/"+pid+"/net/dev").readlines()
#     t = []
#     for info in flow_info:
#         temp_list = info.split()
#         t.append(temp_list)
#     flow[0].append(ceil(int(t[6][1])/1024)) # 下载
#     flow[1].append(ceil(int(t[6][9])/1024)) # 发送
#     return flow

if __name__ == '__main__':
    print(top_cpu(devices="TA09003E57",pkg_name="com.hexin.plat.kaihu"))
    print(get_men(devices="TA09003E57",pkg_name="com.hexin.plat.kaihu"))
    # print(get_fps(devices="TA09003E57",pkg_name="com.hexin.plat.kaihu"))
    pass