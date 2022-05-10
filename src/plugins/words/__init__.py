'''
Author: zh(RickSchanze)(帝皇の惊)
Description: 涩图模块定义的handle，请注意不要改变语句
    sys.path.append(permission_path)
    from permission import permission
    的顺序
Date: 2022-05-05 20:01:58
LastEditTime: 2022-05-10 13:24:53
'''


from .words import Words
from Allpermission import permission
from nonebot import on_command
from nonebot.adapters import Bot, Event
import json
import os
import sys
import logging
import re
import httpx
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Message
# 变量定义环节
work_path = os.getcwd()
index_path = os.path.join(work_path, "src\plugins\words\index.txt")
picture = ''

permission_path = os.path.join(work_path, "src\plugins")

permission_file = os.path.join(permission_path, "permission.json")

sys.path.append(permission_path)


allWords = Words()

'''
    下面是处理涩图与非涩图的
    由于使用的API不同，所以需要分别判断
'''
setu = on_command("涩图", priority=1)


@setu.handle()
async def setu_hanlde(event: Event, bot: Bot):
    # 检测涩图功能是否可用
    setuAvailable = False
    if str(event.group_id) in permission["groupSetuAvailable"].keys():
        setuAvailable = permission["groupSetuAvailable"][str(
            event.group_id)]
    if setuAvailable:
        # 检测是否有涩涩资格
        name = event.get_plaintext()
        if len(name) == 2:
            name = ""
            url = allWords.urls[0]
        else:
            name = name[2:].strip()
            url = allWords.urls[0] + f'?keyword={name}'
        try:
            await allWords.get_picture_informatin(url)
        except IndexError as e:
            await bot.call_api("send_group_msg", message=f"找不到你要的主题捏", group_id=int(event.group_id), auto_escape=False)
            logging.error(e)
            return
        ############################################################################################
        # 开始获取涩图，并将涩图的详细信息发送出去
        picture_index = await allWords.get_picture_and_save(allWords.picture_information["url"], allWords.picture_information["pid"])
        title = allWords.picture_information["title"]
        author = allWords.picture_information["author"]
        pid = allWords.picture_information["pid"]
        await bot.call_api("send_group_msg", message=f'''作品名:{title}
作者:{author}
pid:{pid},
地址:{allWords.picture_information["url"]}''', group_id=int(event.group_id), auto_escape=False)
        #############################################################################################
        # 保存涩图后发送：保存涩图是夹带私货
        picture = f"pictures/picture{picture_index}_{pid}.jpg"
        picture = os.path.join(work_path, f"src\plugins\words\{picture}")
        picture = picture.replace("\\", "//")
        try:
            await bot.call_api("send_group_msg", message=f"[CQ:image,type=flash,file=file://{picture}]", group_id=int(event.group_id), auto_escape=False)
        except ActionFailed as e:
            logging.error("消息发送失败，文件可能不存在，具体请看cqhttp端" + e.adapter_name)
        #############################################################################################
        # 涩图计数器
        qq = str(event.get_user_id())
        nickname = event.sender.nickname
        if qq not in permission["setuCount"].keys():
            permission["setuCount"][qq] = {
                "count": 0,
                "nickname": nickname
            }
        permission["setuCount"][qq]["count"] += 1
        ############################################################################################
        # 保存当天的涩图计数器到文件
        with open(permission_file, 'w', encoding='utf-8') as f:
            json.dump(permission, fp=f, indent=4, ensure_ascii=False)
        #############################################################################################

    else:
        await bot.call_api("send_group_msg", message="不可以涩涩！", group_id=int(event.group_id), auto_escape=False)

notsetu = on_command(
    "来张好看的", aliases={f"{allWords.nickname}来张好看的"}, priority=1)


@notsetu.handle()
async def nowsetu_handle(event, bot):
    async with httpx.AsyncClient() as Client:
        response = await Client.get(allWords.urls[1])
        response = response.text
        aUrl = re.search('src="(.*?)"', response, re.S)
        await bot.send(event=event, message=Message(f"[CQ:image,file=http:{aUrl.group(1)}]"))

setAvailableTrue = on_command("我要涩涩！")


@setAvailableTrue.handle()
async def setAvailable_handle(event: Event, bot):
    if isinstance(event, PrivateMessageEvent):
        return
    group_id = str(event.group_id)
    if event.get_user_id() in permission["setu_managers"] or event.get_user_id() in permission["supermanager"]:
        if group_id not in permission["groupSetuAvailable"].keys():
            permission["groupSetuAvailable"][str(group_id)] = False
        permission["groupSetuAvailable"][str(group_id)] = True
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={event.get_user_id()}]涩涩！", group_id=int(event.group_id), auto_escape=False)
        with open(permission_file, 'w', encoding='utf-8') as f:
            json.dump(permission, fp=f, indent=4, ensure_ascii=False)
    else:
        if group_id not in permission["groupSetuAvailable"].keys():
            permission["groupSetuAvailable"][str(group_id)] = False

        if permission["groupSetuAvailable"][str(group_id)]:
            await bot.call_api("send_group_msg", message=f"[CQ:at,qq={event.get_user_id()}]一起涩涩！", group_id=int(event.group_id), auto_escape=False)
        else:
            await bot.call_api("send_group_msg", message=f"[CQ:at,qq={event.get_user_id()}]不可以涩涩！", group_id=int(event.group_id), auto_escape=False)


setAvailableFalse = on_command("不可以涩涩！")


@setAvailableFalse.handle()
async def setAvailable_handle(event: Event, bot: Bot):
    if isinstance(event, PrivateMessageEvent):
        return
    group_id = str(event.group_id)
    if event.get_user_id() in permission["setu_managers"] or event.get_user_id() in permission["supermanager"]:
        if group_id not in permission["groupSetuAvailable"].keys():
            permission["groupSetuAvailable"][str(group_id)] = False
        permission["groupSetuAvailable"][str(group_id)] = False
        await bot.call_api("send_group_msg", message=f"不可以涩涩！！", group_id=int(event.group_id), auto_escape=False)

        with open(permission_file, 'w', encoding='utf-8') as f:
            json.dump(permission, fp=f, indent=4, ensure_ascii=False)
    else:
        if group_id not in permission["groupSetuAvailable"].keys():
            permission["groupSetuAvailable"][str(group_id)] = False
        if permission["groupSetuAvailable"][str(group_id)]:
            await bot.call_api("send_group_msg", message=f"[CQ:at,qq={event.get_user_id()}]为什么？就要涩涩！", group_id=int(event.group_id), auto_escape=False)
        else:
            await bot.call_api("send_group_msg", message=f"[CQ:at,qq={event.get_user_id()}]不可以涩涩！", group_id=int(event.group_id), auto_escape=False)


add_manager = on_command("addSetuManager")


@add_manager.handle()
async def add_manager_handle(event: Event, bot: Bot):
    if isinstance(event, PrivateMessageEvent):
        group_id = event.get_user_id()
    else:
        group_id = event.group_id
    user_id = event.get_user_id()
    if user_id in permission["supermanager"]:
        text = allWords.message_to_qq(event.raw_message)
        if text not in permission["setu_managers"]:
            permission["setu_managers"].append(text)
            with open(permission_file, 'w', encoding='utf-8') as f:
                json.dump(permission, fp=f, indent=4, ensure_ascii=False)

    else:
        if isinstance(event, PrivateMessageEvent):
            await bot.call_api("send_private_msg", message=f"你不是我的Master，不听你话捏", user_id=int(group_id), auto_escape=False)
        else:
            await bot.call_api("send_group_msg", message=f"[CQ:at,qq={user_id}]你不是我的Master，不听你话捏", group_id=int(group_id), auto_escape=False)


remove_setumanager = on_command("removeSetuManager", priority=1)


@remove_setumanager.handle()
async def remove_manager_handle(event: Event, bot: Bot):
    if isinstance(event, PrivateMessageEvent):
        group_id = event.get_user_id()
    else:
        group_id = event.group_id
    user_id = event.get_user_id()
    if user_id in permission["supermanager"]:
        text = allWords.message_to_qq(event.raw_message)
        if text in permission["setu_managers"]:
            del permission["setu_managers"][permission["setu_managers"].index(
                text)]
            with open(permission_file, 'w', encoding='utf-8') as f:
                json.dump(permission, fp=f, indent=4, ensure_ascii=False)

    else:
        if isinstance(event, PrivateMessageEvent):
            await bot.call_api("send_private_msg", message=f"你不是我的Master，不听你话捏", user_id=int(group_id), auto_escape=False)
        else:
            await bot.call_api("send_group_msg", message=f"[CQ:at,qq={user_id}]你不是我的Master，不听你话捏", group_id=int(group_id), auto_escape=False)

check = on_command("查看涩图统计", aliases={"统计涩图"})


@check.handle()
async def check_handle(event: Event, bot: Bot):
    strMessage = ''
    for item in permission["setuCount"].items():
        judge = ''
        if item[1]["count"] > 20:
            judge = '小心猝死'
        elif item[1]["count"] > 15 and item[1]["count"] <= 20:
            judge = '伟大导师'
        elif item[1]["count"] > 10 and item[1]["count"] < 15:
            judge = '求导达人'
        elif item[1]["count"] > 5 and item[1]["count"] <= 10:
            judge = '适度放松'
        else:
            judge = '修身养性'
        strMessage = strMessage + "昵称: " + \
            item[1]["nickname"] + ", 次数: " + \
            str(item[1]["count"]) + "  鉴定为: " + judge + "\n"
    await bot.call_api("send_group_msg", message=strMessage, group_id=int(event.group_id), auto_escape=False)


awords = on_command(f"{allWords.nickname}文青一下", aliases={
                    f"文青{allWords.nickname}", f"{allWords.nickname}文青", "文青一个"}, priority=1)


@awords.handle()
async def words_handle(event: Event, bot: Bot):
    word = await allWords.get_words("https://api.oddfar.com/yl/q.php")
    await bot.send(event=event, message=word)
