import utils
from mylog import *
import config
import time

info_log("程序初始化完毕，即将进行选课")


mode = config.config["system"]["mode"]

if mode == 0:
    # 定时抢课
    info_log("定时抢课模式")
    time.sleep(1.5)
    hour = config.config["system"]["hour"]
    minute = config.config["system"]["minute"]
    second = config.config["system"]["second"]
    utils.time_choose_lesson(hour, minute, second)
elif mode == 1:
    # 监控抢课
    info_log("监控抢课模式")
    time.sleep(1.5)
    utils.monitor_choose_lesson()
elif mode == 2:
    # 循环抢课
    info_log("循环抢课模式")
    time.sleep(1.5)
    utils.loop_choose(t=0.5 if 'sleep' not in config.config['system'] else config.config['system']['sleep'])

info_log("选课结束")