from matplotlib import markers
import matplotlib.pyplot as plt
import numpy
import time
import json
import os
import requests

DataPath = './PyPluginData'
# DataPath = '../../PyPluginData/AsoulFansCounting'
DataFileName = '/data.json'
PicName = '/All.jpg'
BOTPath = 'PyPluginData/AsoulFansCounting/FansPic'

def Min(x,y):
    if x<y:
        return x
    else:
        return y

def DrawAll():
    with open(DataPath+DataFileName,"r") as f:
        data = f.readlines()
    t = Min(len(data),336)
    Data = data[-t:]
    X = []
    Y = {}
    for s in Data:
        x = json.loads(s)
        day = time.localtime(x["time"]).tm_mday
        hour = time.localtime(x["time"]).tm_hour
        min = time.localtime(x["time"]).tm_min
        X.append(str(day)+'.'+str(hour)+':'+str(min))
        # print(time.localtime(x["time"]))
        for y in range(0,6):
            if y in Y:
                Y[y].append(x["data"][y])
            else:
                Y[y] = [x["data"][y]]
    X.pop()
    for y in range(0,6):
        lengt = len(Y[y])
        for i in range(0,lengt-1):
            Y[y][i]=Y[y][i+1]-Y[y][i]
        Y[y].pop()
    # plt.rcParams['savefig.dpi']=200
    # plt.rcParams['figure.dpi']=200
    plt.figure(figsize=(25,5))
    plt.xticks(range(0,t,24))
    
    plt.plot(X,Y[0],color='b',label='Ava')
    plt.plot(X,Y[1],color='c',label='Bella')
    plt.plot(X,Y[2],color='g',label='Carol')
    plt.plot(X,Y[3],color='r',label='Diana')
    plt.plot(X,Y[4],color='k',label='Elieen')
    plt.plot(X,Y[5],color='m',label='Nana7mi')
    plt.legend(loc='upper left',bbox_to_anchor=(0.0,0.99))
    plt.axhline(y=0,linestyle=':')
    plt.savefig(DataPath+'/FansPic'+PicName,dpi=200)
    # plt.show()
    plt.close()

def Draw(ID):
    Lable = ['Ava','Bella','Carol','Diana','Elieen','Nana7mi']
    with open(DataPath+DataFileName,"r") as f:
        data = f.readlines()
    t = Min(len(data),336)
    Data = data[-t:]
    X = []
    Y = []
    for s in Data:
        x = json.loads(s)
        day = time.localtime(x["time"]).tm_mday
        hour = time.localtime(x["time"]).tm_hour
        min = time.localtime(x["time"]).tm_min
        X.append(str(day)+'.'+str(hour)+':'+str(min))
        # print(time.localtime(x["time"]))
        Y.append(x["data"][ID])
    # plt.rcParams['savefig.dpi']=200
    # plt.rcParams['figure.dpi']=200
    plt.figure(figsize=(8,6))
    plt.xticks(range(0,t,24))
    plt.plot(X,Y,color='b',label=Lable[ID])
    plt.legend(loc='upper left',bbox_to_anchor=(0.0,0.99))
    # plt.axhline(y=0,linestyle=':')
    a = plt.yticks()
    plt.yticks(a[0],list(map(str,map(int,a[0])))) # 去科学计数法
    plt.savefig(DataPath+'/FansPic'+'/'+str(ID)+'.jpg',dpi=200)
    # plt.show()
    plt.close()

def RunAnalysis(ID):
    if type(ID) == int:
        Draw(ID)
        return str(ID)+'.jpg'
    else:
        DrawAll()
        return 'All.jpg'

def Send(ID,Group,Session,HOST):
    Name = RunAnalysis(ID)
    if not type(ID) == int:
        Str = '粉丝增量图\n'
    else:
        Str = '粉丝数量图\n'
        
    data = {
        "sessionKey": Session,
        "target": Group,
        "messageChain": [
            {
                "type": "Plain",
                "text": Str,
            },
            {
                "type": "Image",
                "path": BOTPath+'/'+Name,
            }
        ]
    }
    re = requests.post(url=HOST+'/sendGroupMessage',json=data)
    print(re.text)

if __name__ == "__main__":
    DrawAll()
    Draw(0)
    Draw(1)
    Draw(2)
    Draw(3)
    Draw(4)
    Draw(5)