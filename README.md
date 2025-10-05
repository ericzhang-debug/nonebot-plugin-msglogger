<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-msglogger

_✨ 一个基于 NoneBot2 的群聊消息记录插件，能够自动保存群聊消息到 PostgreSQL 数据库，并支持多媒体文件本地存储。 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-msglogger.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-msglogger">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-msglogger.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>


## 📖 介绍

📝 自动消息记录：自动捕获并保存所有群聊消息

🗂️ 分群存储：每个群聊独立数据表，数据隔离清晰

💾 多媒体支持：支持保存图片、表情包等多媒体文件

⚙️ 灵活配置：可通过配置文件控制是否保存各类文件

🗄️ PostgreSQL：使用高性能关系型数据库存储数据

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-msglogger

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-msglogger
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-msglogger
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-msglogger
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-msglogger
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_msglogger"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置（或是你指向的配置文件）

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| DATABASE_URL | 是 | postgresql://user:password@localhost:5432/msglogger | PgSQL连接字符串 |
| DATA_STORAGE_PATH | 是 | ./data | 图片等媒体文件存储路径 |
| ENABLE_IMAGE_DOWNLOAD | 是 | True | 是否启用下载普通图片 |
| ENABLE_FACE_IMAGE_DOWNLOAD | True | 无 | 是否启用下载表情图片 |
