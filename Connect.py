import json
import Spider
import time
import requests

HOST = ''
FILE_DIR = ''
AuthKey = ''
Session = None
TimeStamp = ''
CLEARTIME = 10
Account = 0
ReceiveCount = 10
DELAYTIME = 2

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


def Send(Group):
    global Session
    L = GetData()
    data = {
        "sessionKey": Session,
        "target": Group,
        "messageChain": [
            {
                "type": "Plain",
                "text": "向晚粉丝数为："+str(L[0])+"\n"
            },
            {
                "type": "Plain",
                "text": "贝拉粉丝数为："+str(L[1])+"\n"
            },
            {
                "type": "Plain",
                "text": "珈乐粉丝数为："+str(L[2])+"\n"
            },
            {
                "type": "Plain",
                "text": "嘉然粉丝数为："+str(L[3])+"\n"
            },
            {
                "type": "Plain",
                "text": "乃琳粉丝数为："+str(L[4])+"\n"
            },
            {
                "type": "Plain",
                "text": "电子宠物粉丝数为："+str(L[5])+"\n"
            },
        ]
    }
    re = requests.post(url=HOST+'/sendGroupMessage',json=data)


def Read():
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
                    if(item['type']=='Plain' and item['text']=='今日a手'):
                        FlagCommand = True
                        print("A手")
                if(FlagCommand):
                    Send(GroupName)


def run():
    ReCnt = 0
    while(True):
        if(Session == None):
            print("登录成功")
            Auth()
        ReCnt = ReCnt + 1
        print("第",ReCnt,"次读取")
        Read()
        if(ReCnt == CLEARTIME):
            ReCnt = 0
            print("释放成功")
            Release()
        time.sleep(DELAYTIME)


if __name__ == '__main__':
    # Auth()
    run()
