'''
Author: zh (RickSchanze) (帝皇の惊)
Date: 2022-04-29 18:13:37
Description: 定时任务相关功能,注意在导入模块时顺序比较重要，若没有理解请勿随意改动
LastEditTime: 2022-05-10 13:33:12
'''

#####################################################################################


from .timedTask import TimedTask
from Allpermission import permission
from nonebot.adapters.onebot.v11 import Message
import os
import sys


from nonebot import on_command, on_request, require
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupRequestEvent, FriendRequestEvent
import nonebot
import datetime
import httpx
import re
import logging
import json

work_path = os.getcwd()

permission_path = os.path.join(work_path, "src\plugins")

permission_file = os.path.join(permission_path, "permission.json")

sys.path.append(permission_path)
scheduler = require("nonebot_plugin_apscheduler").scheduler

task = TimedTask()

nickname = nonebot.get_driver().config.nickname

tmpfile1 = "tmp1.jpg"

tmpfile1 = os.path.join(permission_path, tmpfile1)

tmpfile2 = "tmp2.jpg"

tmpfile2 = os.path.join(permission_path, tmpfile2)


#######################################################################################


@scheduler.scheduled_job("cron", hour="7", minute="30")
async def morning():
    '''
    description: 早七点半向群里定时发送的消息 
    '''
    global tmpfile1
    bot = nonebot.get_bot()
    #############################################################################
    # 获取今天日期信息
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    #############################################################################
    url = ""
    async with httpx.AsyncClient() as Client:
        # 获得图片链接，用了正则表达式
        try:
            response = await Client.get("https://api.ghser.com/random/fengjing.php?type=json", timeout=30)
            response = response.text
            url = re.search('"imgurl":"(.*?)"', response, re.S)
            url = url.group(1)
            url = url.replace("\/", "/")
        except httpx.ReadTimeout as e:
            logging.error("获取风景图片超时")
    #############################################################################
    await task.get_update()
    yesterday_up = "昨天，这些番更新了:\n"
    yes_img = await task.composition_yesterday()
    yes_img.save(tmpfile1)
    tmp1 = tmpfile1.replace("\\", "//")
    yesterday_up += f"[CQ:image,file=file://{tmp1}]"
    #############################################################################
    for id in permission["sendTimedTask"]:
        await bot.call_api("send_group_msg", message=f'''群友们早上好！
现在是{year}年{month}月{day}日早7:30分
祝各位群友有一天的好心情！
{yesterday_up}
{(await task.words_get())}[CQ:image,file={url}]''', group_id=int(id), auto_escape=False)


@scheduler.scheduled_job("cron", hour="23", minute="30")
async def evening():
    '''
    description: 晚十一点半定时发送群消息
    param {*}
    return {*}
    '''
    global tmpfile1
    bot = nonebot.get_bot()
    ####################################################################################################
    # 获取今天番剧信息
    await task.get_update()
    today_up = "今天，这些番更新了:\n"
    today_img = (await task.composition_today())
    today_img.save(tmpfile1)
    tmp1 = tmpfile1.replace("\\", "//")
    today_up += f"[CQ:image,file=file://{tmp1}]"
    ####################################################################################################
    url = ""
    async with httpx.AsyncClient() as Client:
        # 下面用于获取到每日随机图片的链接(即url)
        try:
            response = await Client.get("https://api.ghser.com/random/fengjing.php?type=json", timeout=30)
            response = response.text
            url = re.search('"imgurl":"(.*?)"', response, re.S)
            url = url.group(1)
            url = url.replace("\/", "/")
        except httpx.ReadTimeout as e:
            logging.error("获取风景图片超时")
    ####################################################################################################
    # 获取今天的日期，用于下面发送信息
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    ####################################################################################################
    for id in permission["sendTimedTask"]:
        await bot.call_api("send_group_msg", message=f'''群友们晚上好！
现在是{year}年{month}月{day}日晚23:30分
祝各位晚上有一个好梦！
{today_up}
{(await task.words_get())}[CQ:image,file={url}]''', group_id=int(id), auto_escape=False)


@scheduler.scheduled_job("cron", hour="0", minute="0")
async def _():
    '''
    description: 清除涩图统计信息的方法 
    param {*}
    return {*}
    '''
    permission["setuCount"] = {}
    with open(permission_file, 'w', encoding='utf-8') as f:
        json.dump(permission, fp=f, indent=4, ensure_ascii=False)

morning_anime = on_command("最新番剧", block=True)


@morning_anime.handle()
async def morning_anime_handle(bot: Bot, event: Event):
    '''
    description: 收到“最新番剧”消息时做出的响应
    param {*}
    return {*}
    '''
    global tmpfile1, tmpfile2
    group_id = event.group_id
    await task.get_update()
    reply_str = ""
    reply_str += "今天，这些番剧更新了：\n"
    img = await task.composition_today()
    img.save(tmpfile1)
    tmp1 = tmpfile1.replace("\\", "//")
    reply_str += f'[CQ:image,file=file://{tmp1}]'

    reply_str += "昨天，这些番更新了: \n"
    img = await task.composition_yesterday()
    img.save(tmpfile2)
    tmp2 = tmpfile2.replace("\\", "//")
    reply_str += f'[CQ:image,file=file://{tmp2}]'
    await bot.call_api("send_group_msg", message=reply_str, group_id=int(group_id), auto_escape=False)

addTimedTasks = on_command(f"增加定时播报", block=True)


@addTimedTasks.handle()
async def timedTasks_handle(event: Event, bot: Bot):
    if isinstance(event, PrivateMessageEvent):
        return
    group_id = str(event.group_id)
    if group_id in permission["sendTimedTask"]:
        await bot.send(event=event, message="已经加入队列！")
    else:
        permission["sendTimedTask"].append(group_id)
        await bot.send(event=event, message="好，了解！")
        with open(permission_file, 'w', encoding='utf-8') as f:
            json.dump(permission, fp=f, indent=4, ensure_ascii=False)

removeTimedTasks = on_command(f"不要定时播报了", block=True)


@removeTimedTasks.handle()
async def removeTimedTasks_handle(event: Event, bot: Bot):
    if isinstance(event, PrivateMessageEvent):
        return
    group_id = str(event.group_id)
    if group_id in permission["sendTimedTask"]:
        del permission[permission["sendTimedTask"].index(group_id)]
        await bot.send(event=event, message="明白！")
        with open(permission_file, 'w', encoding='utf-8') as f:
            json.dump(permission, fp=f, indent=4, ensure_ascii=False)
    else:
        await bot.send(event=event, message="明白！可是我本来就没有这个打算呢...")

group_invite = on_request()


@group_invite.handle()
async def group_invite_handle(event: Event, bot: Bot):
    if isinstance(event, GroupRequestEvent):
        await event.approve(bot)

friend_invite = on_request()


@friend_invite.handle()
async def group_invite_handle(event: Event, bot: Bot):
    if isinstance(bot, FriendRequestEvent):
        await event.approve(bot)

bug_forward = on_command("提交bug")


@bug_forward.handle()
async def bug_forward_handle(event: Event, bot: Bot):
    await bot.call_api("send_private_msg", message=event.raw_message, user_id=2815091564, auto_escape=False)

test = on_command("testForMe", priority=1)


@test.handle()
async def k(event: Event, bot: Bot):
    await bot.send(event=event, message=Message("[CQ:image,file=f5ece26f7b0ffefd99e725bb1ebf7fe5.image]"))
