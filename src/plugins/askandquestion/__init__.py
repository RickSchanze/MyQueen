import os
import json
import nonebot
from nonebot import get_driver, on_command, on_message, on_notice
from nonebot.adapters import Bot, Event
from nonebot.adapters import Message
from nonebot.typing import T_State
from nonebot.params import ArgStr
from numpy import printoptions
from .config import Config


class GlobalDialog:
    global_msg = ""

    def __init__(self):
        try:
            path = os.path.join(os.path.dirname(__file__), "global_Dialog.json")
            with open(path, encoding = "utf-8") as f:
                self.global_msg = json.load(f)
        except FileNotFoundError as e:
            with open("global_Dialog.json", "a+", encoding = "utf-8") as f:
                pass


global_config = get_driver().config
config = Config.parse_obj(global_config)
_sub_plugins = set()
readAllDialog = config.global_reply
msg_list = { }
globalDig = GlobalDialog().global_msg
# I think there should be a better way to manage global variables
# Especially for asynchronous programs


def session_to_group_id(session):  # 将 session 信息转变为群号
    return session.split("_")[1]

def message_to_qq(qq):  # 命令后面 at 人的时候，获取那个人的 QQ
    if len(qq.split("=")) == 2:
        return qq.split("=")[1][:-2]
    else:
        return 0


add_manager = on_command("addManager", priority = 1)
@add_manager.handle()
async def add_manager_handle(event: Event, bot: Bot):
    group_id = session_to_group_id(event.get_session_id())
    user_id = event.get_user_id()
    if user_id in globalDig["supermanager"]:
        text = message_to_qq(event.raw_message)
        if text:
            globalDig["managers"].append(text)
    else:
        await bot.call_api("send_group_msg", message = f"[CQ:at,qq={user_id}]抱歉，您没有足够权限", group_id = int(group_id), auto_escape = False)


delMsg = on_command("del", priority = 1)
@delMsg.handle()
async def delMsg_handle(event: Event, bot: Bot):
    group_id = session_to_group_id(event.get_session_id())
    user_id = event.get_user_id()
    if user_id in globalDig["managers"] or user_id in globalDig["supermanager"]:
        key = event.raw_message[4:]
        for item in list(globalDig.values())[2:]:
            if key in item.keys():
                item.pop(key)
                path = os.path.join(os.path.dirname(__file__), "global_Dialog.json")
                with open(path, "w", encoding = "utf-8") as f:
                    json.dump(globalDig, fp = f, indent = 2, ensure_ascii = False)
    else:
        await bot.call_api("send_group_msg", message = f"[CQ:at,qq={user_id}]抱歉，您没有足够权限", group_id = int(group_id), auto_escape = False)


help = on_command("help", aliases={"帮助", "使用方法"}, priority = 1)
@help.handle()
async def help_handle(event: Event, bot: Bot):
    group_id = session_to_group_id(event.get_session_id())
    await bot.call_api("send_group_msg", message="[CQ:image,file=file://D://software//QQBotMyQueen//MyQueen//src//help//help.jpg]", group_id = int(group_id), auto_escape = False)
    # Wait a minute
    # Using absolute paths leads to low portability
    # Consider using relative paths or URLs


learning = on_message(priority = 20)
@learning.handle()
async def learning_handle(event: Event, bot: Bot, state: T_State):
    group_id = session_to_group_id(event.get_session_id())
    msg = event.raw_message
    if group_id not in msg_list.keys():
        msg_list[group_id] = []
    if len(msg_list[group_id]) != 6:
        msg_list[group_id].append(msg)
    else:
        if not (msg_list[group_id][0] == msg_list[group_id][2] and msg_list[group_id][0] == msg_list[group_id][4] and msg_list[group_id][1] == msg_list[group_id][3] and msg_list[group_id][1] == msg_list[group_id][5] and msg == msg_list[group_id][0]):
            del msg_list[group_id][0]  # I think there will be a better way to remove the first element in a list
            msg_list[group_id].append(msg)

    if len(msg_list[group_id]) == 6:
        if msg_list[group_id][0] == msg_list[group_id][2] and msg_list[group_id][0] == msg_list[group_id][4] and msg_list[group_id][1] == msg_list[group_id][3] and msg_list[group_id][1] == msg_list[group_id][5] and msg_list[group_id][1] != msg_list[group_id][0]:  # 三条对话分别相等
            if group_id not in globalDig.keys():
                globalDig[group_id] = {}
            globalDig[group_id][msg_list[group_id][4]] = msg_list[group_id][5]
            path = os.path.join(os.path.dirname(__file__), "global_Dialog.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(globalDig, fp = f, indent = 2, ensure_ascii = False)


response = on_message(priority = 20)
@response.handle()
async def response_handle(event: Event, bot: Bot):
    group_id = session_to_group_id(event.get_session_id())
    msg = event.raw_message
    if group_id in globalDig.keys() and msg in globalDig[group_id].keys():
        await bot.call_api("send_group_msg", message = globalDig[group_id][msg], group_id = int(group_id), auto_escape = False)
    else:
        for item in list(globalDig.values())[2:]:
            if msg in item.keys():
                await bot.call_api("send_group_msg", message=item[msg], group_id = int(group_id), auto_escape = False)
                return


sick = on_command("逆天发病")
@sick.handle()
async def sick_handle(event: Event, bot: Bot):
    qq = message_to_qq(event.raw_message)
    group_id = session_to_group_id(event.get_session_id())
    await bot.call_api("send_group_msg", message=f"[CQ:at,qq={qq}]的脚小小的香香的，不像手经常使用来得灵活，但有一种独特的可爱的笨拙，嫩嫩的脚丫光滑细腻，凌莹剔透，看得见皮肤下面细细的血管与指甲之下粉白的月牙。再高冷的女生小脚也是敏感的害羞的，轻轻挠一挠，她就摇身一变成为娇滴滴的女孩，脚丫像是一把钥匙，轻轻掌握它就能打开女孩子的心灵。", group_id = int(group_id), auto_escape = False)
