import json
import toml
from mylog import *

config={}


# # json config
# try:
#     with open("config.json", "r") as f:
#         try:
#             config = json.load(f)
#         except:
#             error_log("config error")
#             exit(0)
# except:
#     error_log("can't find config file, here is a example")
#     print('''{
#     "system": {
#         "mode": 2,
#         "sleep": 1,
#         "semesterId": "4262"
#     },
#     "user": {
#         "username": "aaa",
#         "password": "123456",
#         "isEncrypted": false
#     },
#     "course": [
#         {
#             "lesson_no": "0915",
#             "profileId": "1631",
#             "name": ""
#         }
#     ]
# }''')
#     exit(0)

# toml config
try:
    with open("config.toml", "r") as f:
        try:
            config = toml.load(f)
        except:
            error_log("config error")
            exit(0)
except:
    error_log("can't find config file, here is a example")
    print('''[system]
mode = 2
sleep = 1
semesterId = "4262"
          
[user]
username =
password =
isEncrypted = false

[[course]]
lesson_no = "0915"
profileId = "1631"
name = ""
''')
    exit(0)
    

if "user" in config and "username" in config["user"] and "password" in config["user"]:
    info_log("config loaded, username:"+config["user"]["username"])
else:
    error_log("config error")
    exit(0)

if 'isEncrypted' not in config['user']:
    config['user']['isEncrypted'] = False

if __name__ == "__main__":
    print(config)