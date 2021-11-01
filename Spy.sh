#!/usr/bin/env bash
PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
cd {BOT_PATH}/PyPlugin/AsoulFansCounting
touch {BOT_PATH}/PyPlugin/AsoulFansCounting/run
source {BOT_PATH}/PyPlugin/AsoulFansCounting/venv/bin/activate # 启用虚拟环境
{BOT_PATH}/PyPlugin/AsoulFansCounting/venv/bin/python3 {BOT_PATH}/PyPlugin/AsoulFansCounting/Spider.py #启动爬虫
deactivate
#使用时将{BOT_PATH}替换为机器人mcl.jar所在路径
#按照自己的虚拟环境配置修改虚拟环境路径信息