from setuptools import setup, find_packages

setup(
    name = "nonebot-plugin-msglogger",
    version = "0.0.4",
    keywords = ["nonebot","nonebot-plugin","msglogger","Message", "nonebot-plugin-msglogger"],
    description = "A NoneBot plugin for automatically recording group chat messages into PostgreSQL database with media file storage support.",
    long_description = "This is a NoneBot plugin designed to automatically capture and store all group chat messages into a PostgreSQL database. The plugin creates separate database tables for each group chat, ensuring organized data structure and efficient querying. It supports saving various media files including images and emoticons to local storage, with configurable options to enable or disable file saving based on user preferences. The plugin operates seamlessly in the background, providing reliable message archiving and media preservation capabilities for group chat management.",
    license = "GPLv3 Licence",
    url = "https://github.com/ericzhang-debug/nonebot-plugin-msglogger",
    author = "EricZhang",
    author_email = "15364519511@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "nonebot2",
        "nonebot-adapter-onebot",
        "sqlalchemy",
        "psycopg2-binary",
        "aiohttp",
        "aiofiles"
    ]
)
