import Connect
import json
import Analysis
from functools import partial
import re
import FrameAPI

FriendCommandMap = {

}

GroupCommandMap = {
    '["Plain","^今日a手$"]': 0,
    '["Plain","^今日asoul$"]': 0,
    '["Plain","^#查询引流效果$"]': 0,
    '["Plain","^一个魂在哪里$"]': 0,
    '["Plain","^#近日涨粉情况$"]': 1,
    '["Plain","^#查询向晚状态$"]': 2,
    '["Plain","^#查询贝拉状态$"]': 3,
    '["Plain","^#查询珈乐状态$"]': 4,
    '["Plain","^#查询嘉然状态$"]': 5,
    '["Plain","^#查询乃琳状态$"]': 6,
    '["Plain","^#海子姐来全杀了$"]': 7,
}
FuncMap = [
    Connect.Main,
    partial(Analysis.Send, 'All'),
    partial(Analysis.Send, 0),
    partial(Analysis.Send, 1),
    partial(Analysis.Send, 2),
    partial(Analysis.Send, 3),
    partial(Analysis.Send, 4),
    partial(Analysis.Send, 5)
]

# 默认config.json目录：../../PyPluginConfig/AsoulFansCounting
# 或者 ./PyPluginConfig

def CheckCommand(MessageType, MessageContain,CommandMap):
    for x in CommandMap.keys():
        t = json.loads(x)
        MatchResult = re.match(t[1], MessageContain)
        if(t[0] == MessageType and MatchResult != None):
            return (CommandMap[x],MatchResult.groups())
    return None

def MainHandler(Message,BOT):
    for message in Message:
        if(message['type'] == 'GroupMessage'):
            CommandMap = GroupCommandMap
        elif(message['type'] == 'FriendMessage'):
            CommandMap = FriendCommandMap
        else:
            CommandMap = None
        if CommandMap != None:
            for item in message['messageChain']:
                try:
                    t = CheckCommand(
                            item['type'], item['text'], CommandMap)
                    if t != None:
                        print("Message Recognized ,running Plugin ID",t[0])
                        FuncMap[t[0]](t[1],sender = message['sender'],bot = BOT)
                except KeyError:
                    pass

if __name__ == '__main__':
    BOT = FrameAPI.HttpBot()
    BOT.Login()
    BOT.MessageChecker(MainHandler)