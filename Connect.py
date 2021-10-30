import json
import Spider
import time
import requests
import os
import random

HOST = '' # BOT服务器地址
FILE_DIR = '' # 缓存文件目录
AuthKey = '' # AuthKey
Session = None # Session（自动获取）
CLEARTIME = 10 # Session释放计数
Account = 0 # 账户
ReceiveCount = 10 # 单次从队列读取的消息数
DELAYTIME = 2 # 每次请求间隔
RECALLTIME = 4 # 查询增量的取样时间点（30min为单位）
SendCommand = []

# 默认config.json目录：../../PyPluginConfig/AsoulFansCounting
# 或者 ./PyPluginConfig

ConfigPath = './PyPluginConfig'
# ConfigPath = '../../PyPluginConfig/AsoulFansCounting'
ConfigFileName = '/Config.json'

DataPath = './PyPluginData'
# DataPath = '../../PyPluginData/AsoulFansCounting'
DataFileName = '/data.json'

def GetConfig():
    if os.path.isfile(ConfigPath+ConfigFileName):
        global HOST,AuthKey,CLEARTIME,Account,ReceiveCount,DELAYTIME,RECALLTIME,SendCommand
        with open(ConfigPath+ConfigFileName,'r') as f:
            f.seek(0)
            s = f.read()
            data = json.loads(s)
            HOST = data['HOST']
            AuthKey = data['AuthKey']
            CLEARTIME = data['CLEARTIME']
            Account = data['Account']
            ReceiveCount = data['ReceiveCount']
            DELAYTIME = data['DELAYTIME']
            RECALLTIME = data['RECALLTIME']
            SendCommand = data['SendCommand']
    else:
        os.makedirs(ConfigPath,exist_ok=True)
        with open(ConfigPath+ConfigFileName,'w') as f:
            data = { # 默认配置
                'HOST' : '',
                'AuthKey' : '',
                'CLEARTIME' : 10,
                'Account' : 0,
                'ReceiveCount' : 10,
                'DELAYTIME' : 2,
                'RECALLTIME': 4,
                'SendCommand' : ['今日a手']
            }
            f.write(json.dumps(data))
        print('请修改Config.json')
        raise(Exception)


def GetData():
    return Spider.run()


def Auth():
    data = {
        "verifyKey": AuthKey
    }
    re = requests.post(url=HOST+'/verify', json=data)
    reda = json.loads(re.text)
    global Session 
    Session = reda['session']
    data = {
        "sessionKey": Session,
        "qq": Account
    }
    re = requests.post(url=HOST+'/bind', json=data)
    reda2 = json.loads(re.text)

def Release():
    global Session
    data = {
        "sessionKey": Session,
        "qq": Account
    }
    re = requests.post(url=HOST+'/release', json=data)
    Session = None

def CheckCommand(str):
    global SendCommand
    for x in SendCommand:
        if(str == x):
            return True
    return False

def Send(Group,Session):
    global Llast
    L = GetData()
    mapping = [('向晚',0),('贝拉',1),('珈乐',2),('嘉然',3),('乃琳',4),('电子宠物',5)]
    texts = []
    for i in mapping:
        delta = L[i[1]]-Llast[i[1]]
        if(delta > 0):
            texts.append(i[0]+"粉丝数为："+str(L[i[1]])+"( 🥵"+ str(delta) +" )\n")
        else:
            texts.append(i[0]+"粉丝数为："+str(L[i[1]])+"( 🥶"+ str(delta) +" )\n")
    data = {
        "sessionKey": Session,
        "target": Group,
        "messageChain": [
            {
                "type": "Plain",
                "text": texts[0]
            },
            {
                "type": "Plain",
                "text": texts[1]
            },
            {
                "type": "Plain",
                "text": texts[2]
            },
            {
                "type": "Plain",
                "text": texts[3]
            },
            {
                "type": "Plain",
                "text": texts[4]
            },
            {
                "type": "Plain",
                "text": texts[5]
            },
        ]
    }
    re = requests.post(url=HOST+'/sendGroupMessage',json=data)
    Llast = L

def Read():
    global Session
    param = {
        'sessionKey' : Session
    }
    re = requests.get(url=HOST+'/countMessage',params=param)
    reda = json.loads(re.text)
    Qsz = reda["data"]
    if(Qsz > 0):
        # print("获取消息")
        param = {
            'sessionKey' : Session,
            'count' : ReceiveCount
        }
        reMessage = requests.get(url=HOST+'/fetchMessage',params=param)
        redata = json.loads(reMessage.text)
        Message = redata['data']
        for message in Message:
            # print("遍历")
            if message['type'] == "GroupMessage":
                FlagCommand = False
                GroupName = message['sender']['group']['id']
                for item in message['messageChain']:
                    if(item['type']=='Plain' and CheckCommand(item['text'])):
                        FlagCommand = True
                        # print("A手")
                if(FlagCommand):
                    Send(GroupName,Session)


def run():
    GetConfig()
    ReCnt = 0
    while(True):
        if(Session == None):
            # print("登录成功")
            Auth()
        ReCnt = ReCnt + 1
        # print("第",ReCnt,"次读取")
        Read()
        if(ReCnt == CLEARTIME):
            ReCnt = 0
            # print("释放成功")
            Release()
        time.sleep(DELAYTIME)


def Main(): # 提供给MainProcess的接口
    GetConfig()
    Auth()
    Send()
    Release()

if __name__ == '__main__':
    # Auth()
    Llast = GetData()
    run()