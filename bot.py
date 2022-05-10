'''
Author: zh (RickSchanze) (帝皇の惊)
Date: 2022-04-30 18:16:57
Description: 
LastEditTime: 2022-05-10 13:22:59
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins("echo")
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin("nonebot_plugin_chatrecorder")
nonebot.load_plugin("nonebot_plugin_shindan")
nonebot.load_plugin("nonebot_plugin_wordcloud")
nonebot.load_plugin("nonebot_plugin_fortune")
nonebot.load_plugin("nonebot_plugin_petpet")
nonebot.load_plugin("nonebot_plugin_memes")
nonebot.load_plugin("nonebot_plugin_code")
nonebot.load_plugin("nonebot_plugin_simplemusic")
nonebot.load_plugins("src\\plugins\\askandquestion")
nonebot.load_plugins("src\\plugins\\words")
nonebot.load_plugins("src\\plugins\\timedTask")


if __name__ == "__main__":
    nonebot.logger.warning(
        "Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
