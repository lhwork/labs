# -*- coding: UTF-8 -*-

import subprocess
import logging
import traceback

def check_pid_handle_num(maxnum = 500):
    try:
        #获取当前所有进程打开句柄数
        cmd = "/usr/sbin/lsof -n|awk '{print $2}'|sort|uniq -c|sort -nr"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        #轮询检查当前所有进程
        ret = {}
        for i in p.stdout.readlines():
            d = i.strip(' ').strip('\n').split(' ')
            print d
            if d[0] > maxnum:
                cmdd = "ps -C -p "+d[1]+"|awk '{print $6}'"
                pp = subprocess.Popen(cmdd, shell=True, stdout=subprocess.PIPE)

                #放入当前进程和句柄数量
                ret[d[1]] = {'serv':pp.stdout.readlines()[1], 'num':d[0]}
                pp.terminate()

        return ret
    except:
        logging.error('error in check_pid_handle_num:%s', traceback.format_exc())
        return []

if __name__ == '__main__':
    check_pid_handle_num()

