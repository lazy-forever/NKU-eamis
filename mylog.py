import ctypes as _ctypes
import time as _time

'''
这个模块用于打印日志
'''

_FOREGROUND_RED = 0x0C  # 红色
_FOREGROUND_GREEN = 0x0A  # 绿色
_FOREGROUND_BLUE = 0x0b  # 蓝色
_FOREGROUND_YELLOW = 0x0E  # 黄色
# 获取标准输出的句柄
_std_handle = _ctypes.windll.kernel32.GetStdHandle(-11)
def _set_color(color):
    _ctypes.windll.kernel32.SetConsoleTextAttribute(_std_handle, color)

def _reset_color():
    _set_color(0x0F)  # 还原为默认颜色

def warn_log(message):
    _set_color(_FOREGROUND_BLUE)
    print(_time.strftime("%Y-%m-%d %H:%M:%S", _time.localtime()), end=' ')
    _reset_color()
    _set_color(_FOREGROUND_YELLOW)
    print(f'WARN: {message}')
    _reset_color()

def error_log(message):
    _set_color(_FOREGROUND_BLUE)
    print(_time.strftime("%Y-%m-%d %H:%M:%S", _time.localtime()), end=' ')
    _reset_color()
    _set_color(_FOREGROUND_RED)
    print(f'ERROR: {message}')
    _reset_color()

def info_log(message):
    _set_color(_FOREGROUND_BLUE)
    print(_time.strftime("%Y-%m-%d %H:%M:%S", _time.localtime()), end=' ')
    _reset_color()
    _set_color(_FOREGROUND_GREEN)
    print(f'INFO: {message}')
    _reset_color()

if __name__ == '__main__':
    warn_log('警告信息')
    error_log('错误信息')
    info_log('提示信息')