'''
Author: zh (RickSchanze) (帝皇の惊)
Date: 2022-04-12 21:17:13
Description: 
LastEditTime: 2022-05-01 22:18:44
'''
#####################################################################
import asyncio
import json
import time
import cv2 as cv
import numpy as np
from bs4 import BeautifulSoup
from PIL import ImageFont, Image, ImageDraw

import logging

import httpx

import datetime
#####################################################################


class TimedTask:
    def __init__(self) -> None:
        '''
        description: 初始化,url一般为设定好的值，不需要更改 
        param {*}
        return {*}
        '''
        self.__url_text: str = ""
        self.__detail_information: dict = {}
        self.__today_and_yesterday: dict = {}
        self.__today_picture_list: list[cv.Mat] = []
        self.__yesterday_picture_list: list[cv.Mat] = []

    async def __get_url_text(self) -> str:
        '''
        description: 该函数用于获取网址的响应，由于响应时间可能较长，故设为异步 
        param {*}
        return {*}
        '''
        async with httpx.AsyncClient() as client:
            responnse = await client.get("https://www.agemys.com/update?page=1", timeout=30)
            self.__url_text = responnse.text

    async def __parse_url_text(self) -> None:
        '''
        description: 该函数用于对首个url返回的html代码进行解析，分离出我们需要的东西（具体番剧的名字以及详情页）
        param {*}
        return {*}
        '''
        soup = BeautifulSoup(self.__url_text, 'lxml')
        all_update = soup.find_all(class_='anime_icon2')
        detail_information = []
        for update in all_update:
            detail_http = "https://www.agemys.com" + \
                update.a['href'] + "?playid=2_1"
            detail_http = detail_http.replace('detail', 'play')
            name = update.a.img['alt']
            chapter = update.a.span.string
            picture = update.a.img['src']
            detail_information.append(
                {
                    "detail_http": detail_http,
                    "name": name,
                    "chapter": chapter,
                    "picture":picture
                }
            )
        self.__detail_information = detail_information

    def __time_is_today(self, aTime: str) -> bool:
        '''
        description: 该函数用于查看番剧是不是今天更新的 
        param {*}
        return {*}
        '''
        today = time.strftime("%Y-%m-%d", time.localtime())
        if today in aTime:
            return True
        else:
            return False

    def __time_is_yesterday(self, aTime: str) -> bool:
        '''
        description: 该函数用于查看番剧是不是昨天更新的 
        param {*}
        return {*}
        '''
        yesterday = self.__getYesterday()
        yesterday = str(yesterday)
        if yesterday in aTime:
            return True
        else:
            return False

    def __getYesterday(self):
        '''
        description: 获取昨天日期的函数 
        param {*}
        return {*}
        '''
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today-oneday
        return yesterday

    async def __get_update_time(self) -> None:
        '''
        description: 获取更新日期的函数
        param {*}
        return {*}
        '''
        self.__today_and_yesterday = {
            "today": [],
            "yesterday": []
        }
        for index in range(len(self.__detail_information)):
            async with httpx.AsyncClient() as client:
                try:
                    info = await client.get(self.__detail_information[index]["detail_http"], timeout=20)
                    info = info.text
                    soup = BeautifulSoup(info, 'lxml')

                    ######################################
                    try:
                        update_time = soup.find_all(
                            class_="play_imform_val")[-3].text
                    except Exception as e:
                        logging.error(
                            f"在解析{self.__detail_information[index]}时越界访问")
                    ######################################

                    if self.__time_is_today(update_time):
                        self.__today_and_yesterday["today"].append(self.__detail_information[index])
                    elif self.__time_is_yesterday(update_time):
                        self.__today_and_yesterday["yesterday"].append(
                            self.__detail_information[index])
                    else:
                        break
                except httpx.ConnectTimeout:
                    logging.error(f"在获取{self.__detail_information[index]}时超时")
    
    async def get_update(self) -> None:
        '''
        description: 公有接口，由于网站可能更新，因此获取最新番剧时必须调用一次用以获得最新信息 
        param {*}
        return {*}
        '''
        try:
            await self.__get_url_text()
            await self.__parse_url_text()
            await self.__get_update_time()
        except Exception as e:
            logging.error(e)

    async def __get_today_picture(self) -> None:
        '''
        description: 爬取今日更新所有番剧的封面
        param {*}
        return {*}
        '''        
        self.__today_picture_list.clear()
        for every in self.__today_and_yesterday["today"]:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get("https:" + every["picture"], timeout=30)
                except Exception as e:
                    logging.error(e)
                self.__today_picture_list.append(cv.imdecode(np.asarray(bytearray(response.content), dtype=np.uint8), cv.IMREAD_COLOR))

    async def composition_today(self) -> Image:
        '''
        description: 将番剧封面于番剧名称更新集数合成为一张图片 
        param {*}
        return {*}
        '''        
        await self.__get_today_picture()
        today = self.__today_and_yesterday["today"]
        length = len(self.__today_picture_list)
        rows = int(length / 4) + 1 if length % 4 != 0 else int(length / 4)
        pic = np.zeros([10 + 308 * rows, 920, 3], np.uint8)
        
        font = ImageFont.truetype("msyh.ttc", 20)
        for index in range(0, length):
            col = index % 4
            row = int((index / 4))
            pic[10 + 308 * row: 10 + 308 * row + 208,10 + 250 * col : 10 + 250 * col + 150,:] \
                = self.__today_picture_list[index][:,:,:]
        img = Image.fromarray(cv.cvtColor(pic, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        for index in range(0, length):
            col = index % 4
            row = int((index / 4))
            name = today[index]["name"] if len(today[index]["name"]) <= 10 else today[index]["name"][0:10] + "..."
            draw.text((10 + 250 * col, 10 +  228 + 308 * row),  name, font=font, fill="#FFFFFF")
            draw.text((10 + 250 * col, 10 +  258 + 308 * row), today[index]["chapter"], font=font, fill="#FFFFFF")
        return img

    async def __get_yesterday_picture(self) -> None:
        self.__yesterday_picture_list.clear()
        for every in self.__today_and_yesterday["yesterday"]:
            async with httpx.AsyncClient() as client:
                response = await client.get("https:" + every["picture"], timeout=30)
                self.__yesterday_picture_list.append(cv.imdecode(np.asarray(bytearray(response.content), dtype=np.uint8), cv.IMREAD_COLOR))

    async def composition_yesterday(self) -> Image:
        await self.__get_yesterday_picture()
        today = self.__today_and_yesterday["yesterday"]
        length = len(self.__yesterday_picture_list)
        rows = int(length / 4) + 1 if length % 4 != 0 else int(length / 4)
        pic = np.zeros([10 + 308 * rows, 920, 3], np.uint8)
        font = ImageFont.truetype("msyh.ttc", 20)
        for index in range(0, length):
            col = index % 4
            row = int((index / 4))
            pic[10 + 308 * row: 10 + 308 * row + 208,10 + 250 * col : 10 + 250 * col + 150,:] \
                = self.__yesterday_picture_list[index][:,:,:]
        img = Image.fromarray(cv.cvtColor(pic, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        for index in range(0, length):
            col = index % 4
            row = int((index / 4))
            name = today[index]["name"] if len(today[index]["name"]) <= 10 else today[index]["name"][0:10] + "..."
            draw.text((10 + 250 * col, 10 +  228 + 308 * row),  name, font=font, fill="#FFFFFF")
            draw.text((10 + 250 * col, 10 +  258 + 308 * row), today[index]["chapter"], font=font, fill="#FFFFFF")
        return img

    async def words_get(self):
        async with httpx.AsyncClient() as client:
            try:
                rtnJson = await client.get("https://v1.jinrishici.com/all", timeout=30)
            except Exception as e:
                logging.error(e)
            rtnJson = json.loads(str(rtnJson.text))
            return " " + rtnJson["content"] + "\n" + "----" + rtnJson["author"] + " 《" + rtnJson["origin"] + "》" 

test = TimedTask()
asyncio.run(test.words_get())