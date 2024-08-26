import json_dump

class lesson:
    def __init__(self, no, profileId, lessonJSONs, lesson_count):
        self.no=no
        self.id=json_dump.get_id_by_no(lessonJSONs, no)
        self.lc=lesson_count[str(self.id)]['lc']
        self.profileId=profileId
        self.group=json_dump.get_group_by_no(lessonJSONs, no)
        self.name=json_dump.get_name_by_no(lessonJSONs, no)
        self.choose=False
        self.choose_url="https://eamis.nankai.edu.cn/eams/stdElectCourse!batchOperator.action?profileId="+profileId
    def __str__(self):
        return str(self.no)+" "+self.name+" "+str(self.id)+" "+str(self.lc)+" "+str(self.group)
    def toString(self):
        return str(self.no)+" 课程名称："+self.name+" id："+str(self.id)+" 选课上限："+str(self.lc)+" 组号："+str(self.group)
    

if __name__ == '__main__':
    lesson=lesson("0849", "1620")
    print(lesson)