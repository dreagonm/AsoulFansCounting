import requests
import json
import os
import time

ConfigPath = '../../PyPluginConfig'
ConfigFileName = '/FrameConfig.json'
LocalVersion = 'V1.1'

class HttpBot:
    # HOST ,Authkey ,CLEARTIME, Account, ReceiveCount ,Delaytime
    def __init__(self):
        print("Initing HttpBot, Frame Version ",LocalVersion)
        Data = self.ConfigGet()
        Ver = Data['Version']
        if Ver != LocalVersion:
            print("配置文件和机器人版本不匹配，请删除配置文件，重新运行机器人")
            raise(Exception)
        self.HOST = Data['HOST']
        self.AuthKey = Data['AuthKey']
        self.Account = Data['Account']
        self.ReceiveCount = Data['ReceiveCount']
        self.DELAYTIME = Data['DELAYTIME']
    
    def InitConfigFile(self):
        os.makedirs(ConfigPath, exist_ok=True)
        with open(ConfigPath+ConfigFileName, 'w') as f:
            data = {  # 默认配置
                'HOST': '',
                'AuthKey': '',
                'Account': 0,
                'ReceiveCount': 10,
                'DELAYTIME': 2,
                'Version': LocalVersion
            }
            f.write(json.dumps(data))
        pass

    def ConfigGet(self):
        if os.path.isfile(ConfigPath+ConfigFileName):
            global HOST, AuthKey, CLEARTIME, Account, ReceiveCount, DELAYTIME
            with open(ConfigPath+ConfigFileName, 'r') as f:
                f.seek(0)
                s = f.read()
                data = json.loads(s)
                return data
        else:
            self.InitConfigFile()
            print('请修改配置文件')
            raise(Exception)

    def Auth(self):
        print("Authing ",self.Account)
        data = {
            "verifyKey": self.AuthKey
        }
        re = requests.post(url=self.HOST+'/verify', json=data)
        reda = json.loads(re.text)
        self.Session = reda['session']
        
    def Bind(self):
        print("Binding ",self.Account)
        data = {
            "sessionKey": self.Session,
            "qq": self.Account
        }
        re = requests.post(url=self.HOST+'/bind', json=data)
        reda2 = json.loads(re.text)

    def Login(self):
        print("Logging ",self.Account)
        self.Auth()
        self.Bind()

    def Release(self):
        data = {
            "sessionKey": self.Session,
            "qq": self.Account
        }
        re = requests.post(url=self.HOST+'/release', json=data)
        Session = None

    def GroupMessage(self,Target,MessageChain):
        data = {
            "sessionKey": self.Session,
            "target": Target,
            "messageChain": MessageChain
        }
        re = requests.post(url=self.HOST+'/sendGroupMessage',json=data)
        redata = json.loads(re)
        MID = redata["messageId"]
        return MID

    def FriendMessage(self,Target,MessageChain):
        data = {
            "sessionKey": self.Session,
            "target": Target,
            "messageChain": MessageChain
        }
        re = requests.post(url=self.HOST+'/sendFriendMessage',json=data)
        redata = json.loads(re)
        MID = redata["messageId"]
        return MID

    def Recall(self, Target):
        data = {
            "sessionKey":"{{session}}",
            "target":Target
        }
        re = requests.post(url=self.HOST+'/recall',json=data)

    def GetMessageNum(self):
        param = {
        'sessionKey': self.Session
        }
        re = requests.get(url=self.HOST + '/countMessage',params = param)
        reda = json.loads(re.text)
        return reda["data"]

    def MessageAcquire(self):
        param = {
            'sessionKey': self.Session,
            'count': self.ReceiveCount
        }
        reMessage = requests.get(url=self.HOST+'/fetchMessage', params=param)
        redata = json.loads(reMessage.text)
        Message = redata['data']
        return Message
    
    def MessageChecker(self,Handler):
        while(True):
            if self.GetMessageNum() > 0:
                Message = self.MessageAcquire()
                Handler(Message,self)
            time.sleep(self.DELAYTIME)

class WebsocketBot:
    def Connect():
        pass

    def Release():
        pass

    def EventHandler():
        pass