# AsoulFansCounting

基于MIRAI框架实现的查询Asoul成员粉丝数的工具

## 基于

[MIRAI框架](https://github.com/mamoe/mirai)
[MIRAI-API-HTTP](https://github.com/project-mirai/mirai-api-http)
[DgmBot](https://github.com/dreagonm/DgmBot)

## 插件功能

- 查询Asoul成员当前粉丝量和粉丝增量
- 查询近期Asoul成员粉丝数量图和粉丝增量图

## 插件使用

**路径可在Python文件中自行修改**
**后续{BOTPATH}代表机器人目录，即mcl.jar所在目录**


0. 配置``MIRAI-API-HTTP``，修改``setting.yml``
示例：
```yml
adapters: 
  - http
debug: false
enableVerify: true
verifyKey: 123456 # 改为自己的验证密钥
singleMode: false
cacheSize: 4096
adapterSettings:
  http:
    host: 0.0.0.0
    port: 8081 # 监听端口，和后续配置保持一致即可
    cors: [*]

```
1. 在机器人目录下创建``PyPlugin``目录，将仓库中文件放入``AsoulFansCounting``目录下
2. 安装虚拟环境并根据``requirements.txt``安装相关依赖
3. 运行``MainProcess.py``，启动插件
4. 第一次启动会报错，并在机器人目录下的``PyPluginConfig``目录下的``AsoulFansCounting``目录中生成默认的``MainConfig.json``配置文件
5. 修改配置文件，示例如下
```json
{
    "HOST": "http://127.0.0.1:8081", // 运行BOT的服务器地址和端口，
    // 在同一台机器运行时地址填写http://127.0.0.1:port 
    "AuthKey": "", // 验证使用的密钥，配置方法请在第0步或者``MIRAI-API-HTTP``文档中查看
    "CLEARTIME": 10,
    "Account": 0, // BOT使用的帐号
    "ReceiveCount": 10, 
    "DELAYTIME": 2
    }
```
6. 再次运行，即可正常使用粉丝量查询

### 启用粉丝增量图绘制功能

0. 修改``Spy.sh``

- 将``{BOT_PATH}``替换为机器人目录的绝对路径
- 修改虚拟环境的路径
- 修改``{BOT_PATH}/PyPlugin/AsoulFansCounting/venv/bin/python3``为虚拟环境中解释器的绝对路径

1. 开启数据收集
``Spy.sh``是一个自动收集数据的脚本，会将粉丝数据自动存放在``{BOTPATH}/PyPluginData/AsoulFansCounting/data.json``中，使用Crontab将其配置为定时任务，推荐每30分钟启动一次

示例：
```bash
> crontab -e
> 0,30 * * * * {Spy.sh的绝对路径}
```

2. 配置完成

## BOT指令

| 指令                                                 | 效果                     |
| ---------------------------------------------------- | ------------------------ |
| "今日a手","今日asoul","#查询引流效果","一个魂在哪里" | 查询当前粉丝数量         |
| \"#近日涨粉情况"                                     | 生成近日粉丝增量图       |
| ”\#查询{asoul成员名}状态“（示例：\#查询珈乐状态）    | 生成对应成员的粉丝数量图 |
| "\#海子姐来全杀了"                                   | 生成海子姐粉丝图         |

### 自定义指令

修改``MainProcess.py``中的``CommandMap``即可
