from nonebot import get_plugin_config, on_message
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from pprint import pprint
from .config import Config
from .handler import message_logger

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-msglogger",
    description="QQ群聊消息记录器",
    usage="自动记录群聊消息到PostgreSQL数据库",
    config=Config,
)

config = get_plugin_config(Config)

# 创建消息处理器
message_handler = on_message(priority=10, block=False)

@message_handler.handle()
async def handle_message(event: GroupMessageEvent):
    """处理群聊消息"""
    await message_logger.log_message(event)
