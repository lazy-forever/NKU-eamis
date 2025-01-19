# NKU-eamis
![Version](https://img.shields.io/badge/Version-5.0.1-blue.svg) ![Language](https://img.shields.io/badge/Language-Python3-red.svg) ![License](https://img.shields.io/badge/License-AGPL--3.0-yellow.svg)

## 介绍

nku 南开大学(Nankai University) eamis教务系统抢课脚本，包括定时抢课、补退选监控抢课、放课循环抢课，自带一键登录功能

## 特性

:heavy_check_mark: 自动化登录\
:heavy_check_mark: cookie自动化更新\
:heavy_check_mark: 预选正选定时抢课\
:heavy_check_mark: 正选放课循环抢课\
:heavy_check_mark: 补退选监控抢课\
:heavy_check_mark: 多课程支持

**更新中的功能**

:construction: 完善冲突课程交互模式\
:construction: 提供UI界面\
:construction: 增加WebVPN登录方式\
:construction: Webhook通知

**限制**

:heavy_multiplication_x: 保证一定可以抢到课程\
:heavy_multiplication_x: 违背选课规则

:warning: 本脚本仅供学习交流使用，不得用于任何商业用途，由此产生的一切后果与作者无关，严禁用于任何违法行为。

:warning: 本脚本仅用于测试，**禁止将此脚本用于真实抢课行为，所产生的一切后果由使用者自行承担，与作者本人无任何关系。**

## 使用

使用前请确保已经安装python3和pip

安装python依赖

```bash
pip install -r requirements.txt
```

复制`config.toml.example`到`config.toml`并修改为自己的`config.toml`文件

```bash
cp config.toml.example config.toml
```

运行程序

```bash
python main.py
```

## 贡献与支持

如果你有任何问题或者建议，欢迎提交issue或者pull request

如果你觉得这个项目对你有帮助，欢迎给我一个star，并推荐给你的朋友，也可以通过我的主页请我喝杯咖啡

感谢所有为这个项目提交代码的人