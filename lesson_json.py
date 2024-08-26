'''
为什么要写这个文件？
因为课程信息的json格式不标准，而课程信息文件太大，使用demjson解析太慢，所以自己写了一个解析器
实测解析时间大概是1s左右
'''

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from an empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from an empty stack")

    def size(self):
        return len(self.items)

def parse_json(json_str):
    # 找到lessonJSONs的起始位置
    start_index = json_str.find('=')
    end_index = json_str.find(';')
    # 截取lessonJSONs的部分
    json_str = json_str[start_index+1:end_index]
    json_str = json_str.replace(" ", "").replace("\n", "").replace("\t", "")
    result = {}
    result_stack = Stack()
    current_key = ""
    current_value = ""
    stack=Stack()
    is_key = True

    for char in json_str:
        if char == '{':
            is_key = True
            if current_key:
                stack.push(current_key)
                current_key = ""
            result_stack.push(result)
            result = {}
        elif char == '}':
            if current_key and current_value:
                if isinstance(current_value, str):
                    if current_value.isdigit():
                        current_value = int(current_value)
                result[current_key] = current_value
                current_key = ""
                current_value = ""
            if stack.size()>0:
                current_key=stack.pop()
                result_stack.peek()[current_key]=result
                result=result_stack.pop()
                current_key=""
        elif char == ':':
            is_key = False
        elif char == ',':
            is_key = True
            if current_key and current_value:
                if isinstance(current_value, str):
                    if current_value.isdigit():
                        current_value = int(current_value)
                result[current_key] = current_value
                current_key = ""
                current_value = ""
        elif char.isalnum() or char in [' ', '_']:
            if is_key:
                current_key += char
            else:
                current_value += char

    return result


if __name__ == '__main__':
    # 测试
    json_string = '''
    aaa={ '577482': {
            sc: 9,
            lc: 60,
            upsc: 3,
            uplc: 10,
            plc: 0,
            puplc: 0,
            expLessonGroups: {
                '5644': {
                    indexNo: 1,
                    stdCount: 9,
                    stdCountLimit: 60,
                    proStdCountLimit: 60
                },
                '5645': {
                    indexNo: 1,
                    stdCount: 9,
                    stdCountLimit: 60,
                    proStdCountLimit: 60
                }
            }
        },
        '577484': {
            sc: 46,
            lc: 80,
            upsc: 0,
            uplc: 0,
            plc: 0,
            puplc: 0
        }
    };'''
    parsed_json = parse_json(json_string)
    print(parsed_json['577482'])