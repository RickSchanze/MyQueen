
import os
from nonebot import on_command, on_message
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
import json
import sys


class GlobalDialog:
    global_msg = ''

    def __init__(self):
        try:
            path = os.path.join(os.path.dirname(
                __file__), "global_Dialog.json")
            with open(path, encoding='utf-8') as f:
                self.global_msg = json.load(f)
        except FileNotFoundError as e:
            with open("global_Dialog.json", "a+", encoding='utf-8') as f:
                pass


msg_list = {}

work_path = os.getcwd()

permission_path = os.path.join(work_path, "src\plugins")

sys.path.append(permission_path)

permission_file = os.path.join(permission_path, "permission.json")

help_path = os.path.join(work_path, "src\help\help.jpg")



help_path = help_path.replace("\\", "//")

from permission import permission


globalDig = GlobalDialog().global_msg


def message_to_qq(qq):              # 命令后面at人的时候，获取那个人的QQ
    if len(qq.split('=')) == 2:
        return qq.split('=')[1][:-2]
    else:
        return 0


add_manager = on_command("addRepeatManager", priority=1)


@add_manager.handle()
async def add_manager_handle(event: Event, bot: Bot):
    group_id = event.group_id
    user_id = event.get_user_id()
    if str(user_id) in permission["supermanager"]:
        text = message_to_qq(event.raw_message)
        if text not in permission["words_managers"]:
            permission["words_managers"].append(text)
            with open(permission_file, 'w', encoding='utf-8') as f:
                json.dump(permission, fp=f, indent=4, ensure_ascii=False)

    else:
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={user_id}]抱歉，您没有足够权限", group_id=int(group_id), auto_escape=False)

removeManager = on_command("removeRepeatManager", priority=1)


@removeManager.handle()
async def remove_manager_handle(event: Event, bot: Bot):
    group_id = event.group_id
    user_id = event.get_user_id()
    if str(user_id) in permission["supermanager"]:
        text = message_to_qq(event.raw_message)
        if text in permission["words_managers"]:
            del permission["words_managers"][permission["words_managers"].index(
                text)]
            with open(permission_file, 'w', encoding='utf-8') as f:
                json.dump(permission, fp=f, indent=4, ensure_ascii=False)

    else:
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={user_id}]抱歉，您没有足够权限", group_id=int(group_id), auto_escape=False)

delMsg = on_command("del", priority=1)


@delMsg.handle()
async def delMsg_handle(event: Event, bot: Bot):
    group_id = event.group_id
    user_id = event.get_user_id()
    if user_id in permission["words_managers"] or user_id in permission["supermanager"]:
        key = event.raw_message[4:]
        for item in globalDig.values():
            if key in item.keys():
                item.pop(key)
                path = os.path.join(os.path.dirname(
                    __file__), "global_Dialog.json")
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(globalDig, fp=f, indent=4, ensure_ascii=False)
    else:
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={user_id}]抱歉，您没有足够权限", group_id=int(group_id), auto_escape=False)


help = on_command("help", aliases={"帮助", "使用方法"}, priority=1)


@help.handle()
async def help_handle(event: Event, bot: Bot):
    group_id = event.group_id
    await bot.call_api("send_group_msg", message=f"[CQ:image,file=file://{help_path}]", group_id=int(group_id), auto_escape=False)

learning = on_message(priority=20)


@learning.handle()
async def learning_handle(event: Event, bot: Bot, state: T_State):
    group_id = str(event.group_id)
    msg = event.raw_message
    if group_id not in msg_list.keys():
        msg_list[group_id] = []
    if len(msg_list[group_id]) != 4:
        msg_list[group_id].append(msg)
    else:
        if not (msg_list[group_id][0] == msg_list[group_id][2] and msg_list[group_id][1] == msg_list[group_id][3] and msg == msg_list[group_id][0]):
            del msg_list[group_id][0]
            msg_list[group_id].append(msg)

    if len(msg_list[group_id]) == 4:
        if msg_list[group_id][0] == msg_list[group_id][2] and msg_list[group_id][1] == msg_list[group_id][3] and msg_list[group_id][1] != msg_list[group_id][0]:    # 三条对话分别相等
            if group_id not in globalDig.keys():
                globalDig[group_id] = {}
            globalDig[group_id][msg_list[group_id][2]] = msg_list[group_id][3]
            path = os.path.join(os.path.dirname(
                __file__), "global_Dialog.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(globalDig, fp=f, indent=4, ensure_ascii=False)


response = on_message(priority=20)


@response.handle()
async def response_handle(event: Event, bot: Bot):
    group_id = str(event.group_id)
    msg = event.raw_message
    if group_id in globalDig.keys() and msg in globalDig[group_id].keys():
        await bot.call_api("send_group_msg", message=globalDig[group_id][msg], group_id=int(group_id), auto_escape=False)
        return
    else:
        for item in globalDig.values():
            if msg in item.keys():
                await bot.call_api("send_group_msg", message=item[msg], group_id=int(group_id), auto_escape=False)
                return

sick = on_command("逆天发病")


@sick.handle()
async def sick_handle(event: Event, bot: Bot):
    qq = message_to_qq(event.raw_message)
    group_id = event.group_id
    await bot.call_api("send_group_msg", message=f"[CQ:at,qq={qq}]的脚小小的香香的，不像手经常使用来得灵活，但有一种独特的可爱的笨拙，嫩嫩的脚丫光滑细腻，凌莹剔透，看得见皮肤下面细细的血管与指甲之下粉白的月牙。再高冷的女生小脚也是敏感的害羞的，轻轻挠一挠，她就摇身一变成为娇滴滴的女孩，脚丫像是一把钥匙，轻轻掌握它就能打开女孩子的心灵。", group_id=int(group_id), auto_escape=False)
