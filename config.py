import json
from mylog import *

config={}
with open("config.json", "r") as f:
    try:
        config = json.load(f)
    except:
        error_log("config error")
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