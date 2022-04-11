## MyQueen

MyQueen（麦昆）是一个基于 nonebot 的机器人，支持 OneBot 接口。

### 功能

1. 复读姬
2. [抽签/今日运势](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune)
3. [词云](https://github.com/he0119/nonebot-plugin-wordcloud)
4. [ShindanMaker](https://github.com/MeetWq/nonebot-plugin-shindan)
5. [头像表情包](https://github.com/MeetWq/nonebot-plugin-petpet)
6. [表情包制作](https://github.com/MeetWq/nonebot-plugin-petpet)

具体内容可以使用 `help` 或 `帮助` 指令查看。

### 部署

```bash
git clone --recursive https://github.com/RickSchanze/MyQueen.git
cd MyQueen
pip install -r requirements.txt
playwright install-deps  # optional
python bot.py
```
