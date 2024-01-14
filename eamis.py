import requests
import time
import warnings
warnings.filterwarnings("ignore")
import json_dump
import lesson_json
import json
import mylog
import threading
flag=True
# 课程类
class lesson:
    def __init__(self, no, lc=-1):
        self.no=no
        self.id=json_dump.get_id_by_no(lessonJSONs, no)
        if lc==-1:
            _, self.lc=json_dump.get_sc_lc_by_id(lessonId2Counts, self.id)
        else:
            self.lc=lc
        self.group=json_dump.get_group_by_no(lessonJSONs, no)
        self.name=json_dump.get_name_by_no(lessonJSONs, no)
        self.choose=False
    def __str__(self):
        return str(self.no)+" "+self.name+" "+str(self.id)+" "+str(self.lc)+" "+str(self.group)

# 这里输入你待选的课程号，选课顺序按照列表顺序
lesson_no=[2888,2865]
lesson_list=[]
profileId="1476"

# 这里输入你的浏览器cookie
JSESSIONID=""
srv_id=""
semesterid="4284"
cookies={
    "JSESSIONID":JSESSIONID,
    "srv_id":srv_id,
    "semester.id":semesterid
}
# 别人的cookie，用于加快监控速度
cookies_list=[{
    "JSESSIONID":"",
    "srv_id":"",
    "semester.id":"4284"
},{
    "JSESSIONID":"",
    "srv_id":"",
    "semester.id":"4284"
}]
cookies_outdated_list=[] # cookie是否失效列表,True为有效，False为失效
useful_num=1 # 有效cookie数量

# 这里为选课人数刷新地址
url="https://eamis.nankai.edu.cn/eams/stdElectCourse!queryStdCount.action?projectId=1&semesterId="+semesterid
# 选课地址
choose_url="https://eamis.nankai.edu.cn/eams/stdElectCourse!batchOperator.action?profileId="+profileId
# 课程人数信息，可能需要更新
lessonId2Counts_url="https://eamis.nankai.edu.cn/eams/stdElectCourse!queryStdCount.action?projectId=1&semesterId="+semesterid
lessonId2Counts_data=requests.get(lessonId2Counts_url, cookies=cookies, verify=False).text
# 课程信息
lessonJSONs_url="https://eamis.nankai.edu.cn/eams/stdElectCourse!data.action?profileId="+profileId
lessonJSONs_data=requests.get(lessonJSONs_url, cookies=cookies, verify=False).text
# 课程老师信息
teacherId2I18n_url="https://eamis.nankai.edu.cn/eams/stdElectCourse!teacherI18n.action?profileId="+profileId+"&lang=zh"
teacherId2I18n_data=requests.get(teacherId2I18n_url, cookies=cookies, verify=False).text
# 课程教室信息
classroomId2I18n_url="https://eamis.nankai.edu.cn/eams/stdElectCourse!classroomI18N.action?profileId="+profileId+"&lang=zh"
classroomId2I18n_data=requests.get(classroomId2I18n_url, cookies=cookies, verify=False).text



# 初始化
try:
    mylog.info_log("初始化中...")
    # lessonId2Counts=json_dump.json_dump(lessonId2Counts_data)
    if "即将跳转至密码修改页面，请按要求修改密码。" in lessonId2Counts_data:
        raise Exception()
    lessonId2Counts = lesson_json.parse_json(lessonId2Counts_data)
    mylog.info_log("人数信息初始化成功")
    lessonJSONs=json_dump.json_dump(lessonJSONs_data)
    mylog.info_log("课程信息初始化成功")
    # teacherId2I18n=json_dump.json_dump(teacherId2I18n_data)
    # mylog.info_log("教师信息初始化成功")
    # classroomId2I18n=json_dump.json_dump(classroomId2I18n_data)
    # mylog.info_log("教室信息初始化成功")
    mylog.info_log("初始化成功")
except:
    mylog.error_log("初始化失败，请检查Cookie是否失效")
    exit()
for i in range(len(cookies_list)):
    lessonId2Counts_data=requests.get(lessonId2Counts_url, cookies=cookies_list[i], verify=False).text
    if "即将跳转至密码修改页面，请按要求修改密码。" in lessonId2Counts_data:
        cookies_outdated_list.append(False)
        mylog.error_log("列表中第"+str(i+1)+"个Cookie失效")
    else:
        cookies_outdated_list.append(True)
        useful_num+=1
        mylog.info_log("列表中第"+str(i+1)+"个Cookie有效")
for i in lesson_no:
    lesson_list.append(lesson(i))
for i in lesson_list:
    mylog.info_log(str(i))






# 通过lesson找sc
def sc(l:lesson):
    s, _ = json_dump.get_sc_lc_by_id(lessonId2Counts, l.id)
    return s

# 选课函数
def choose(lesson0:lesson):
    global flag
    choose_data={
        "optype":"true",
        "operator0":lesson0.id+":true:0",
        "lesson0":lesson0.id,
        "expLessonGroup_"+lesson0.id:lesson0.group==None and "undefined" or lesson0.group,
    }
    response = requests.post(choose_url, cookies=cookies, data=choose_data, verify=False)
    if "成功" in response.text:
        if "即将跳转至密码修改页面，请按要求修改密码。" in response.text:
            mylog.error_log("Cookie失效")
            flag=False
            exit()
        mylog.info_log(str(lesson0.no)+" "+lesson0.name+" "+"选课成功")
        return True
    else:
        index=response.text.find("失败")
        end=response.text.find("</br>",index)
        if index!=-1 :
            reason=response.text[index:end]
            mylog.error_log("选课失败"+":"+reason)
        else:
            mylog.error_log("Cookie失效")
            flag=False
            exit()
        return False



# 更新lessonId2Counts
def update(cookies):
    if flag==False:# 退出线程
        exit()
    global lessonId2Counts
    response = requests.get(lessonId2Counts_url, cookies=cookies,verify=False)
    if response.status_code == 200:
        try:
            lessonId2Counts = lesson_json.parse_json(response.text)
        except:
            mylog.error_log("更新失败，请检查Cookie是否失效")
            return False
        text="人物信息更新成功 "
        for i in lesson_list:
            text+=i.name+":"+str(sc(i))+"/"+str(i.lc)+" "
        mylog.warn_log(text)
    else:
        mylog.error_log("更新失败，状态码:", response.status_code)
    return True

# 更新线程
def update_thread():
    global flag
    global useful_num
    while True:
        for i in range(-1,len(cookies_list)):
            if flag==False: # 结束，退出线程
                exit()
            if i==-1:
                if update(cookies)==False:
                    exit() # 此时cookie失效，退出线程
            elif cookies_outdated_list[i]==True:
                if update(cookies_list[i])==False:
                    # 此时cookie失效，更新cookie失效列表
                    cookies_outdated_list[i]=False
                    useful_num-=1
            else:
                continue
            time.sleep(1/useful_num)




# 选课
#
# 定时抢课
def time_choose_lesson(hour:int, minute:int, second:int):
    while 1:
        now=time.localtime()
        if now.tm_hour==hour and now.tm_min==minute and now.tm_sec==second:
            for i in lesson_list:
                choose(i)
                time.sleep(0.5)
            break
        
# 补退选监控抢课
def monitor_choose_lesson():
    threading.Thread(target=update_thread).start()
    while 1:
        for i in lesson_list:
            if sc(i)<i.lc and i.choose==False:
                mylog.info_log("监控到"+i.name+"有余量，开始抢课")
                if choose(i)==True:
                    i.choose=True
                else:
                    mylog.error_log(i.name+"抢课失败")
                time.sleep(0.5)







if __name__=="__main__":
    monitor_choose_lesson()