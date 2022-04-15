from permission import permission
import logging
import re
from tokenize import group
import httpx
from nonebot import on_command, on_keyword
from nonebot.adapters import Bot, Event, Message
from nonebot.permission import SUPERUSER
import json
import nonebot
import os
import sys
from nonebot.plugin import require
# 变量定义环节
work_path = os.getcwd()
index_path = os.path.join(work_path, "src\plugins\words\index.txt")
picture = ''

permission_path = os.path.join(work_path, "src\plugins")

permission_file = os.path.join(permission_path, "permission.json")

sys.path.append(permission_path)


# 读取权限文件


def message_to_qq(qq):              # 命令后面at人的时候，获取那个人的QQ
    if len(qq.split('=')) == 2:
        return qq.split('=')[1][:-2]
    else:
        return 0

# 获得话的方法


async def get_words(url):
    async with httpx.AsyncClient() as Client:
        response = await Client.get(url)
        return response.text

words = on_command("麦昆文青一下", aliases={"文青麦昆", "麦昆文青", "文青一个"}, priority=1)


@words.handle()
async def words_handle(event, bot):
    word = await get_words("https://api.oddfar.com/yl/q.php")
    await bot.call_api("send_group_msg", message=word, group_id=int(event.group_id), auto_escape=False)

'''
    涩图
'''

# 总API
urls = [
    "https://api.lolicon.app/setu/v2",
    "https://img.xjh.me/random_img.php",

]


async def get_picture_informatin(url):
    async with httpx.AsyncClient() as Client:
        try:
            response = await Client.get(url, timeout=20)
            response = response.text
            response = json.loads(response)
            data = response["data"]
            pid = data[0]["pid"]
            author = data[0]["author"]
            title = data[0]["title"]
            url = "https://pixiv.re/" + str(pid) + ".jpg"
            return {
                "pid": pid,
                "author": author,
                "title": title,
                "url": url
            }
        except httpx.ConnectTimeout as e:
            logging.error("使用API时超时错误")


async def get_picture_and_save(url, pid):
    with open(index_path, "r+", encoding='utf-8') as index_file:
        index = int(index_file.read())
        async with httpx.AsyncClient() as Client:
            try:
                response = await Client.get(url, timeout=20)
                with open(os.path.join(work_path, f"src\plugins\words\pictures\picture{index}_{pid}.jpg"), "wb") as f:
                    f.write(response.content)
                    rtn = index
                    index += 1
                    index_file.seek(0)
                    index_file.truncate()
                    index_file.write(str(index))
                    return rtn
            except httpx.ConnectTimeout as e:
                logging.error("下载图片时超时错误")

'''
    下面是处理涩图与非涩图的
    由于使用的API不同，所以需要分别判断
'''
setu = on_command("来张涩图", aliases={"涩图", "来份涩图"}, priority=1)



@setu.handle()
async def setu_hanlde(event, bot):
    # 检测涩图功能是否可用
    setuAvailable = False
    if str(event.group_id) in permission["groupSetuAvailable"].keys():
        setuAvailable = permission["groupSetuAvailable"][str(
            event.group_id)]
    if setuAvailable:
        # 检测是否有涩涩资格
        picture_information = await get_picture_informatin(urls[0])
        picture_index = await get_picture_and_save(picture_information["url"], picture_information["pid"])
        title = picture_information["title"]
        author = picture_information["author"]
        pid = picture_information["pid"]
        await bot.call_api("send_group_msg", message=f'''作品名:{title}
作者:{author}
pid:{pid}''', group_id=int(event.group_id), auto_escape=False)
        picture = f"pictures/picture{picture_index}_{pid}.jpg"
        picture = os.path.join(work_path, f"src\plugins\words\{picture}")
        picture = picture.replace("\\", "//")
        await bot.call_api("send_group_msg", message=f"[CQ:image,type=flash,file=file://{picture}]", group_id=int(event.group_id), auto_escape=False)

    else:
        await bot.call_api("send_group_msg", message="本群涩图功能已关闭！", group_id=int(event.group_id), auto_escape=False)

notsetu = on_command("来张好看的", aliases={"麦昆来张好看的"}, priority=1)
@notsetu.handle()
async def nowsetu_handle(event, bot):
    async with httpx.AsyncClient() as Client:
        response = await Client.get(urls[1])
        response = response.text
        aUrl = re.search('src="(.*?)"', response, re.S)
        await bot.call_api("send_group_msg", message=f"[CQ:image,file=http:{aUrl.group(1)}]", group_id=int(event.group_id), auto_escape=False)

setAvailableTrue = on_command("setSetuAvailable:True")


@setAvailableTrue.handle()
async def setAvailable_handle(event: Event, bot):
    if event.get_user_id() in permission["setu_managers"] or event.get_user_id() in permission["supermanager"]:
        group_id = (event.group_id)
        if group_id not in permission["groupSetuAvailable"]:
            permission["groupSetuAvailable"][str(group_id)] = {}
        permission["groupSetuAvailable"][str(group_id)] = True
        with open(permission_file, 'w', encoding='utf-8') as f:
            json.dump(permission, fp=f, indent=4, ensure_ascii=False)
    else:
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={event.get_user_id()}]抱歉，您没有足够权限", group_id=int(event.group_id), auto_escape=False)


setAvailableFalse = on_command("setSetuAvailable:False")


@setAvailableFalse.handle()
async def setAvailable_handle(event: Event, bot: Bot):
    if event.get_user_id() in permission["setu_managers"] or event.get_user_id() in permission["supermanager"]:
        group_id = (event.group_id)
        if group_id not in permission["groupSetuAvailable"]:
            permission["groupSetuAvailable"][str(group_id)] = {}
        permission["groupSetuAvailable"][str(group_id)] = False
        with open(permission_file, 'w', encoding='utf-8') as f:
            json.dump(permission, fp=f, indent=4, ensure_ascii=False)
    else:
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={event.get_user_id()}]抱歉，您没有足够权限", group_id=int(event.group_id), auto_escape=False)


add_manager = on_command("addSetuManager")


@add_manager.handle()
async def add_manager_handle(event: Event, bot: Bot):
    group_id = event.group_id
    user_id = event.get_user_id()
    if user_id in permission["supermanager"]:
        text = message_to_qq(event.raw_message)
        if text not in permission["setu_managers"]:
            permission["setu_managers"].append(text)
            with open(permission_file, 'w', encoding='utf-8') as f:
                json.dump(permission, fp=f, indent=4, ensure_ascii=False)

    else:
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={user_id}]抱歉，您没有足够权限", group_id=int(group_id), auto_escape=False)


remove_setumanager = on_command("removeSetuManager", priority=1)


@remove_setumanager.handle()
async def remove_manager_handle(event: Event, bot: Bot):
    group_id = event.group_id
    user_id = event.get_user_id()
    if user_id in permission["supermanager"]:
        text = message_to_qq(event.raw_message)
        if text in permission["setu_managers"]:
            del permission["setu_managers"][permission["setu_managers"].index(
                text)]
            with open(permission_file, 'w', encoding='utf-8') as f:
                json.dump(permission, fp=f, indent=4, ensure_ascii=False)

    else:
        await bot.call_api("send_group_msg", message=f"[CQ:at,qq={user_id}]抱歉，您没有足够权限", group_id=int(group_id), auto_escape=False)
