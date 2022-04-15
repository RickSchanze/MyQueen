## MyQueen

MyQueen（麦昆）是一个基于 nonebot 的机器人，支持 OneBot 接口。

### 功能

1. 复读姬
2. [抽签/今日运势](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune)
3. [词云](https://github.com/he0119/nonebot-plugin-wordcloud)
4. [ShindanMaker](https://github.com/MeetWq/nonebot-plugin-shindan)
5. [头像表情包](https://github.com/MeetWq/nonebot-plugin-petpet)
6. [表情包制作](https://github.com/MeetWq/nonebot-plugin-petpet)
7. [在线运行代码](https://github.com/yzyyz1387/nonebot_plugin_code)
8. 涩图/非涩图(开发完善中)
9. 定时早晚安(开发完善中)
10. 文青麦昆(发送 `文青麦昆` 获得随机语录)

具体内容可以使用 `help` 或 `帮助` 指令查看。

### 注意

插件 [头像表情包](https://github.com/MeetWq/nonebot-plugin-petpet)、[表情包制作](https://github.com/MeetWq/nonebot-plugin-petpet) 需要提供图片资源以保证正常运行，如果网络不佳，可以前往其 GitHub 仓库下载资源并按照其提示安装。

插件 [抽签/今日运势](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune) 无法通过 pip 顺利安装，请前往其 GitHub 仓库下载资源并按照其提示安装。

### 部署

可以参见[这里](https://www.cnblogs.com/RickSchanze/articles/16146041.html)。

### 功能说明

#### 涩图功能

当群成员发送 `涩图` 时，获得的涩图会首先保存在 `src/plugin/words/pictures` 中，之后再往群中发送涩图时，发送的是闪照。

#### 复读功能

如果两个群有同一个复读关键词，那么麦昆将优先使用对应群的。

复读语录位于 `src/plugins/askandquestion/global_Dialog.json`。

### 权限说明

权限文件位于 `src/plugins/permission.json`。

#### 复读管理员

用于管理麦昆复读所说的话，可用命令：

- `del [消息]`：删除一条消息所对应的回应，**该命令为全局删除**！

#### 涩图管理员

用于管理麦昆能不能往群里发涩图，可用命令：

- `setSetuAvailable:True`：开启本群的涩图功能
- `setSetuAvailable:False`：关闭本群的涩图功能

注意：涩图管理员可以对每一个群使用这两条命令！

#### 超级管理员

除了拥有涩图管理员和复读管理员的命令外，还拥有：

- `addRepeatManager[@群成员]`：将该成员设为复读管理员
- `removeRepeatManager[@群成员]`：移除该成员的复读管理员资格
- `addSetuManager[@群成员]`：将该成员设为涩图管理员
- `removeRepeatManager[@群成员]`：移除该成员的涩图管理员资格

### 后续计划

1. 完善涩图模块，实现私发涩图与涩图撤回；
2. 完善定时任务模块，实现可以给每个愿意的群定时发早晚安；
3. 完善文青麦昆模块，将其加入权限系统中。

### 后记

感谢 [nonebot](https://nb2.baka.icu/) 提供 bot 框架支持！

感谢 [cqhttp](https://docs.go-cqhttp.org/) 提供接口支持！

欢迎加 QQ 群 947080238 来找我玩！
