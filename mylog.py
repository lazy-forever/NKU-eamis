import time as _time
from colorama import init, Fore
init(autoreset=True)

def warn_log(message):
    print(f"{Fore.BLUE}{_time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())} "
          f"{Fore.YELLOW}WARN: {message}")

def error_log(message):
    print(f"{Fore.BLUE}{_time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())} "
          f"{Fore.RED}ERROR: {message}")

def info_log(message):
    print(f"{Fore.BLUE}{_time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())} "
          f"{Fore.GREEN}INFO: {message}")

if __name__ == '__main__':
    warn_log('警告信息')
    error_log('错误信息')
    info_log('提示信息')
