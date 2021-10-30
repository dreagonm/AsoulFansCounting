import os
import Connect
import json
import time
import requests

CommandMap = {'["Plain","今日a手"]':0}
FuncMap = [Connect.Main]

# 默认config.json目录：../../PyPluginConfig/AsoulFansCounting
# 或者 ./PyPluginConfig

ConfigPath = './PyPluginConfig'
# ConfigPath = '../../PyPluginConfig'
ConfigFileName = '/MainConfig.json'

DataPath = './PyPluginData'
# DataPath = '../../PyPluginData'
DataFileName = '/Maindata.json'

HOST = '' # BOT服务器地址
AuthKey = '' # AuthKey
Session = None # Session（自动获取）
CLEARTIME = 10 # Session释放计数
Account = 0 # 账户
ReceiveCount = 10 # 单次从队列读取的消息数
DELAYTIME = 2 # 每次请求间隔

def GetConfig():
    if os.path.isfile(ConfigPath+ConfigFileName):
        global HOST,AuthKey,CLEARTIME,Account,ReceiveCount,DELAYTIME
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
                # 'CommandMap' : 
            }
            f.write(json.dumps(data))
        print('请修改Config.json')
        raise(Exception)


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

def CheckCommand(MessageType,MessageContain):
    print("CHECK")
    for x in CommandMap.keys():
        t = json.loads(x)
        if(t[0]==MessageType and t[1]==MessageContain):
            FuncMap[CommandMap[x]]

def loop():
    global Session
    param = {
        'sessionKey' : Session
    }
    re = requests.get(url=HOST+'/countMessage',params=param)
    reda = json.loads(re.text)
    Qsz = reda["data"]
    if(Qsz > 0):
        print("获取消息")
        param = {
            'sessionKey' : Session,
            'count' : ReceiveCount
        }
        reMessage = requests.get(url=HOST+'/fetchMessage',params=param)
        redata = json.loads(reMessage.text)
        Message = redata['data']
        for message in Message:
            print("遍历")
            if message['type'] == "GroupMessage":
                FlagCommand = False
                GroupName = message['sender']['group']['id']
                for item in message['messageChain']:
                    try:
                        CheckCommand(item['type'],item['text'])
                    except KeyError:
                        pass

if __name__ == '__main__':
    GetConfig()
    ReCnt = 0
    while(True):
        if(Session == None):
            print("登录成功")
            Auth()
        ReCnt = ReCnt + 1
        print("第",ReCnt,"次读取")
        loop()
        if(ReCnt == CLEARTIME):
            ReCnt = 0
            print("释放成功")
            Release()
        time.sleep(DELAYTIME)