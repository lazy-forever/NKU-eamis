import js2py

# 从js代码中提取JSON
def json_dump(js_code: str):
    lesson_jsons = js2py.eval_js(js_code)
    return lesson_jsons

# 通过课程no获取课程id
def get_id_by_no(lesson_jsons, no):
    for lesson_json in lesson_jsons:
        if lesson_json['no'] == str(no):
            return lesson_json['id']
    return None

# 通过课程no获取课程group
def get_group_by_no(lesson_jsons, no):
    for lesson_json in lesson_jsons:
        if lesson_json['no'] == str(no):
            return lesson_json['expLessonGroups']==[] and "undefined" or lesson_json['expLessonGroups'][0]['id']
    return None

# 通过课程no获取课程name
def get_name_by_no(lesson_jsons, no):
    for lesson_json in lesson_jsons:
        if lesson_json['no'] == str(no):
            return lesson_json['name']
    return None

# 通过课程id获取课程已选人数sc和限选人数lc
def get_sc_lc_by_id(lessonId2Counts:dict, id):
    if str(id) in lessonId2Counts:
        t=lessonId2Counts[str(id)]
        return t['sc'],t['lc']
    else:
        return None, None

if __name__ == '__main__':
    lesson=""
    json=json_dump(lesson)
    print(get_sc_lc_by_id(json, '576906'))