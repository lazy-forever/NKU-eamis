# NKU-eamis

nku 南开大学(Nankai University) eamis教务系统抢课脚本，包括定时抢课、补退选监控抢课、放课循环抢课，自带一键登录功能

## 使用

安装python依赖

```bash
pip install -r requirements.txt
```

修改自己的config.json

运行程序

```bash
python main.py
```

## config填写说明

共分为三大模块: system, user, course

**system**模块:

mode: 选课模式, 0为定时抢课(用于预选或正选), 1为监控抢课(用于补退选), 2为循环抢课(用于正选放名额通常不会准时放名额的情况)

sleep: 补退选的监控间隔时间, 单位为秒

semesterId: 学期id, 通过选课网站->我的课表->切换到当前学期->查看cookie中的semester.id值

**user**模块:

username: 用户名

password: 密码

isEncrypted: 是否加密, 0为否, 1为是, 密码加密的程序位于login.py->eamis_account->encrypt函数中, 此字段目的在于不希望明文密码出现在配置文件中

**course**模块:

是一个lesson的数组, 用于配置选课信息

lesson_no: 课程编号

profileId: 课程所在profileId, 通过选课网站->选课->进入相应选课通道->查看选课url中的profileId值

name: 课程名称, 仅仅是为了方便查看, 无实际作用