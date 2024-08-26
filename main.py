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
    hour = 7
    minute = 59
    second = 59
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
    utils.loop_choose(t=0) # 默认0.5s间隔, 可以在函数调用时传入参数 t 修改间隔时间





'''
config.json填写说明

共分为四大模块: system, user, helper, course

system模块:
mode: 选课模式, 0为定时抢课(用于预选或正选), 1为监控抢课(用于补退选), 2为循环抢课(用于正选放名额通常不会准时放名额的情况)
help: 是否开启帮助模式
sleep: 补退选的监控间隔时间, 单位为秒
semesterId: 学期id, 通过选课网站->我的课表->切换到当前学期->查看cookie中的semester.id值

user模块:
username: 用户名
password: 密码
isEncrypted: 是否加密, 0为否, 1为是, 密码加密的程序位于login.py->eamis_account->encrypt函数中, 此字段目的在于不希望明文密码出现在配置文件中

helper模块:
是一个user的数组, 用于帮助主账号进行选课, 但是不会进行选课操作, 仅用于监控选课情况
目前helper模块的功能尚未实现

course模块:
是一个lesson的数组, 用于配置选课信息
lesson_no: 课程编号
profileId: 课程所在profileId, 通过选课网站->选课->进入相应选课通道->查看选课url中的profileId值
name: 课程名称, 仅仅是为了方便查看, 无实际作用

'''
'''
未来计划:
1. 完善帮助模式
2. 监控抢课模式下, 提供监听到选课信号时, 退出冲突课程再选目标课程, 如目标课程未成功选上, 重新选回冲突课程
'''