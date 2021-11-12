from . import Connect
from . import Analysis
from functools import partial

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

print("Importing Plugin",__name__)