from nonebot import require
from nonebot import on_command
import nonebot
from nonebot.adapters import Event, Bot
import httpx
import re
import datetime


scheduler = require("nonebot_plugin_apscheduler").scheduler
@scheduler.scheduled_job("cron", hour="7", minute="30")
async def morning():
    bot = nonebot.get_bot()
    text = ""
    url = ""
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    async with httpx.AsyncClient() as Client:
        response = await Client.get("https://api.oddfar.com/yl/q.php")
        text = response.text
    async with httpx.AsyncClient() as Client:
        response = await Client.get("https://api.ghser.com/random/fengjing.php?type=json")
        response = response.text
        url = re.search('"imgurl":"(.*?)"', response, re.S)
        url = url.group(1)
        url = url.replace("\/", "/")
    await bot.call_api("send_group_msg", message=f'''群友们早上好！
现在是{year}年{month}月{day}日早7:30分
祝各位群友有一天的好心情！

{text}
[CQ:image,file={url}]''', group_id=894535279, auto_escape=False)


@scheduler.scheduled_job("cron", hour="23", minute="30")
async def evening():
    bot = nonebot.get_bot()
    text = ""
    url = ""
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    async with httpx.AsyncClient() as Client:
        response = await Client.get("https://api.oddfar.com/yl/q.php")
        text = response.text
    async with httpx.AsyncClient() as Client:
        response = await Client.get("https://api.ghser.com/random/fengjing.php?type=json")
        response = response.text
        url = re.search('"imgurl":"(.*?)"', response, re.S)
        url = url.group(1)
        url = url.replace("\/", "/")
    await bot.call_api("send_group_msg", message=f'''群友们晚上好！
现在是{year}年{month}月{day}日晚23:30分
祝各位晚上有一个好梦！

{text}
[CQ:image,file={url}]''', group_id=894535279, auto_escape=False)
