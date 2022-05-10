'''
Author: zh (RickSchanze) (帝皇の惊)
Date: 2022-04-30 18:16:54
Description: 引入重要的全局变量"permission"
LastEditTime: 2022-05-10 13:17:38
'''
import json
import os
from nonebot import get_driver
permission_path = os.path.join(os.path.dirname(__file__), "permission.json")
config = get_driver().config
with open(permission_path, "r", encoding='utf-8') as per:
    permission = json.load(per)
    if "words_managers" not in permission.keys():
        permission["words_managers"] = []
    if "setu_managers" not in permission.keys():
        permission["setu_managers"] = []
    if "supermanagers" not in permission.keys():
        permission["supermanager"] = list(config.superusers)
    if "groupSetuAvailable" not in permission.keys():
        permission["groupSetuAvailable"] = {}
    if "canResponse" not in permission.keys():
        permission["canResponse"] = {}
    if "setuCount" not in permission.keys():
        permission["setuCount"] = {}
    if "sendTimedTask" not in permission.keys():
        permission["sendTimedTask"] = []
