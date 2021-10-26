import requests
import json

UID = [
    672346917, # Ava
    672353429, # Bella
    351609538, # Carol
    672328094, # Diana
    672342685, # Elieen
    434334701, # Nana7mi
    ]

Url = 'https://api.bilibili.com/x/relation/stat' # 获取粉丝数的接口

Param = { # 接口参数
    'vmid' : '', # uid
    'jsonp':'jsonp'
}

Headers = { # 请求头
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
    'referer' : 'https://space.bilibili.com/', # +str(uid)
    'origin' : 'https://space.bilibili.com'
} 

def GetMemberFans(uid):
    head = Headers.copy()
    head['referer'] = head['referer']+str(uid)
    Param['vmid'] = str(uid)
    Req = requests.get(url=Url,headers=head,params=Param)
    Req.encoding='utf-8'
    data=json.loads(Req.text)
    return data['data']['follower']

def run():
    L = []
    for i in UID:
        L.append(GetMemberFans(i))
    return L

if __name__ == '__main__': # using for test
    print(run())