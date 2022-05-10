
import logging
import httpx
from nonebot import get_driver
import json
import os
import sys
# 变量定义环节
work_path = os.getcwd()
index_path = os.path.join(work_path, "src\plugins\words\index.txt")
picture = ''

permission_path = os.path.join(work_path, "src\plugins")

permission_file = os.path.join(permission_path, "permission.json")

sys.path.append(permission_path)


class Words:
    def __init__(self) -> None:
        self.words = ''                 # 骚话
        self.picture_information = {}   # 图片信息，pid，名字，作者，地址
        driver = get_driver()
        self.urls = [
            "https://api.lolicon.app/setu/v2",
            "https://img.xjh.me/random_img.php",
        ]
        self.nickname = list(driver.config.nickname)[0]

    def message_to_qq(self, qq):              # 命令后面at人的时候，获取那个人的QQ
        '''
        description: 在@某个人时，获得被@的人的QQ，一般用于解析命令 
        param {*}
        return {*}
        '''
        if len(qq.split('=')) == 2:
            return qq.split('=')[1][:-2]
        elif len(qq.split(' ')) == 2:
            return str(qq.split(' ')[1])
        else:
            logging.error("QQ号解析失败！")

    async def get_words(self, url):
        '''
        description: 对应于“麦昆文青” 
        param {*}
        return {*}
        '''
        async with httpx.AsyncClient() as Client:
            response = await Client.get(url)
            return response.text

    async def get_picture_informatin(self, url) -> None:
        '''
        description: 从涩图API获取涩图信息的json 
        param {
            "url" : 涩图API地址，一般不需要修改
        }
        return {*}
        '''
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
                self.picture_information = {
                    "pid": pid,
                    "author": author,
                    "title": title,
                    "url": url
                }
            except httpx.ConnectTimeout as e:
                logging.error("使用API时超时错误")

    async def get_picture_and_save(self, url, pid):
        '''
        description: 利用代理网站和提供的API来获取涩图并保存至本地 
        param {
            "pid":涩图的pid
        }
        return {*}
        '''
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
