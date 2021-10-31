from matplotlib import markers
import matplotlib.pyplot as plt
import numpy
import time
import json
DataPath = './PyPluginData'
# DataPath = '../../PyPluginData/AsoulFansCounting'
DataFileName = '/data.json'
PicName = '/All.png'

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
    plt.savefig(DataPath+PicName,dpi=200)
    plt.show()

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
    plt.figure(figsize=(6,6))
    plt.xticks(range(0,t,24))
    plt.plot(X,Y,color='b',label=Lable[ID])
    plt.legend(loc='upper left',bbox_to_anchor=(0.0,0.99))
    # plt.axhline(y=0,linestyle=':')
    # plt.savefig(DataPath+PicName,dpi=200)
    plt.show()

if __name__ == "__main__":
    DrawAll()
    Draw(0)
    Draw(1)
    Draw(2)
    Draw(3)
    Draw(4)
    Draw(5)