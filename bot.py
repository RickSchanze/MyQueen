#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter


if __name__ == "__main__":
    nonebot.init()
    app = nonebot.get_asgi()

    driver = nonebot.get_driver()
    driver.register_adapter(ONEBOT_V11Adapter)

    nonebot.load_builtin_plugins("echo")
    nonebot.load_plugins("./3rdparty/fortune")
    nonebot.load_plugins("./3rdparty/wordcloud")
    nonebot.load_plugins("./3rdparty/shindan")
    nonebot.load_plugins("./3rdparty/petpet")
    nonebot.load_plugins("./src/plugins/askandquestion")

    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app = "__mp_main__:app")
