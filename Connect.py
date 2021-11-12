import Spider

LMap = {}

# DataPath = './PyPluginData'
DataPath = '../../PyPluginData/AsoulFansCounting'
DataFileName = '/data.json'

def GetData():
    return Spider.run()

def Send(Group,bot,*Args):
    global Llast
    global LMap
    L = GetData()
    mapping = [('向晚',0),('贝拉',1),('珈乐',2),('嘉然',3),('乃琳',4),('电子宠物',5)]
    texts = []
    if(Group in LMap):
        for i in mapping:
            delta = L[i[1]]-LMap[Group][i[1]]
            if(delta > 0):
                texts.append(i[0]+"粉丝数为："+str(L[i[1]])+"( 🥵"+ str(delta) +" )\n")
            else:
                texts.append(i[0]+"粉丝数为："+str(L[i[1]])+"( 🥶"+ str(delta) +" )\n")
    else:
        for i in mapping:
            delta = L[i[1]]-Llast[i[1]]
            if(delta > 0):
                texts.append(i[0]+"粉丝数为："+str(L[i[1]])+"( 🥵"+ str(delta) +" )\n")
            else:
                texts.append(i[0]+"粉丝数为："+str(L[i[1]])+"( 🥶"+ str(delta) +" )\n")
    messageChain = [
        {
            "type": "Plain",
            "text": '粉丝增长量统计时间段：\n从上次询问到本次询问之间粉丝量之间的增长量\n'
        },
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
    bot.GroupMessage(Group,messageChain)
    LMap[Group] = L

Llast = None

def Main(*args,**kwargs): # 提供给MainProcess的接口
    global Llast
    # GetConfig()
    if(Llast == None):
        Llast = GetData()
    groupID = kwargs['sender']['group']['id']
    bot = kwargs['BOT']
    Send(groupID,bot)

if __name__ == '__main__':
    # Auth()
    Llast = GetData()