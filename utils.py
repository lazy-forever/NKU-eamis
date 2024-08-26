import config
from mylog import *
from login import eamis_account
import requests
import json_dump
from lesson_json import parse_json
from lesson import lesson
import time


info_log("初始化中...")
# 全部profileId
profileIds = []
for i in config.config['course']:
    if i['profileId'] not in profileIds:
        profileIds.append(i['profileId'])

# 初始化eamis账户
username = config.config["user"]["username"]
password = config.config["user"]["password"]
is_password_encrypted = config.config["user"]["isEncrypted"]
account = eamis_account(username, password, is_password_encrypted, profileIds)
account.verify()
info_log("cookies loaded success, JSESSIONID:"+account.cookies.get("JSESSIONID")+", srv_id:"+account.cookies.get("srv_id"))


# 选课人数刷新地址
lesson_count_url = "https://eamis.nankai.edu.cn/eams/stdElectCourse!queryStdCount.action?projectId=1&semesterId="+config.config["system"]["semesterId"]
lesson_count = requests.get(lesson_count_url, cookies=account.cookies, verify=False).text
lesson_count = parse_json(lesson_count)
info_log("lesson count data loaded success")


# 全部课程信息
lessonJSONs = {}
for i in profileIds:
    lessonJSONs_url = "https://eamis.nankai.edu.cn/eams/stdElectCourse!data.action?profileId="+i
    lessonJSONs[i] = requests.get(lessonJSONs_url, cookies=account.cookies, verify=False).text
    lessonJSONs[i] = json_dump.json_dump(lessonJSONs[i])

# 待选课程信息
lessons = []
for l in config.config['course']:
    lessons.append(lesson(l['lesson_no'], l['profileId'], lessonJSONs[l['profileId']], lesson_count))
    info_log("lesson "+lessons[-1].toString())
info_log("lesson data loaded success")

def sc(l:lesson):
    s, _ = json_dump.get_sc_lc_by_id(lesson_count, l.id)
    return s

flag = True

sleep_time = config.config["system"]["sleep"]
# 更新选课人数
def update():
    global lesson_count
    while flag:
        response = requests.get(lesson_count_url, cookies=account.cookies, verify=False, allow_redirects=False)
        if response.status_code == 200:
            try:
                lesson_count = parse_json(response.text)
            except:
                error_log("lesson count data updated failed, maybe Cookie is outdated")
                account.verify()
                continue
            info_log("lesson count data updated success")
            for i in lessons:
                sc_count = str(sc(i))
                lc_count = str(i.lc)
                if sc_count != lc_count:
                    warn_log(i.name+":"+sc_count+"/"+ lc_count)
                else:
                    info_log(i.name+":"+sc_count+"/"+ lc_count)
            time.sleep(sleep_time)
        else:
            error_log("lesson count data updated failed, status code:"+str(response.status_code))
            account.verify()
            time.sleep(1)


# 选课函数
def choose(lesson0:lesson):
    choose_data={
        "optype":"true",
        "operator0":str(lesson0.id)+":true:0",
        "lesson0":str(lesson0.id),
        "expLessonGroup_"+str(lesson0.id):lesson0.group==None and "undefined" or lesson0.group,
    }
    response = requests.post(lesson0.choose_url, cookies=account.cookies, data=choose_data, verify=False)
    if "成功" in response.text:
        if "即将跳转至密码修改页面，请按要求修改密码。" in response.text:
            error_log("Cookie outdate")
            account.verify()
            return False
        info_log(str(lesson0.no)+" "+lesson0.name+" "+"选课成功")
        lesson0.choose = True
        return True
    else:
        index=response.text.find("失败")
        end=response.text.find("</br>",index)
        if index!=-1 :
            reason=response.text[index:end]
            error_log(str(lesson0.no)+" "+lesson0.name+" 选课失败"+":"+reason)
        else:
            error_log("Cookie outdate")
            account.verify()
        return False

# 循环选课
def loop_choose(t=0.5):
    for i in lessons:
        if not i.choose:
            while not choose(i):
                time.sleep(t)
            time.sleep(0.5)

# 定时抢课
def time_choose_lesson(hour:int, minute:int, second:int):
    while 1:
        now=time.localtime()
        if now.tm_hour==hour and now.tm_min==minute and now.tm_sec==second:
            for i in lessons:
                choose(i)
                time.sleep(0.5)
            break

# 补退选监控抢课
def monitor_choose_lesson():
    import threading
    threading.Thread(target=update).start()
    while 1:
        for i in lessons:
            if int(sc(i))<int(i.lc) and i.choose==False:
                warn_log("监控到"+i.name+"有余量，开始抢课")
                if choose(i)==True:
                    i.choose=True
                else:
                    error_log(i.name+"抢课失败")
                time.sleep(0.5)

if __name__ == '__main__':
    # import threading
    # update_thread = threading.Thread(target=update)
    # update_thread.start()
    monitor_choose_lesson()