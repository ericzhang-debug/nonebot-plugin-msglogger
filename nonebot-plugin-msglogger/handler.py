import asyncio
import os
from pprint import pprint
import time
from pathlib import Path
from typing import Optional, List
from urllib.parse import urlparse

import aiofiles
import aiohttp
from nonebot import get_driver, logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    MessageSegment,
)
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    MetaData,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from .config import Config
from nonebot import get_plugin_config

async def extract_extent_name(event: MessageEvent) -> str:
    s1=str(event.message).strip()
    temp="jpg"
    for part in s1.split(","):
        if "file=" in part:
            temp=part.split(".")[1]
            return temp
    return temp    


class MessageLogger:
    def __init__(self):
        self.config = None
        self.engine = None
        self.session_factory = None
        self.data_storage_path = None
        self._initialized = False
        
    async def initialize(self):
        """延迟初始化，确保配置已加载"""
        if self._initialized:
            return
            
        # 获取插件配置
        self.config = get_plugin_config(Config)
        
        # 数据库连接
        self.engine = create_engine(self.config.database_url)
        self.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # 确保存储目录存在
        #数据总目录
        self.data_storage_path = Path(self.config.data_storage_path)
        self.data_storage_path.mkdir(parents=True, exist_ok=True)

        # self.image_storage_path = Path(self.config.data_storage_path+"/pic")
        # self.image_storage_path.mkdir(parents=True, exist_ok=True)

        # self.face_image_storage_path = Path(self.config.data_storage_path+"/face")
        # self.face_image_storage_path.mkdir(parents=True, exist_ok=True)
        

        
        self._initialized = True
        # print("*"*30)
        # pprint(self.config)
        # print("*"*30)
        logger.info("消息记录器初始化完成")
        
    async def ensure_table_exists(self, group_id: int):
        """确保群聊对应的数据表存在"""
        if not self._initialized:
            await self.initialize()
            
        table_name = f"group_msg_{group_id}"
        
        # 检查表是否存在
        with self.engine.connect() as conn:
            table_exists = self.engine.dialect.has_table(conn, table_name)
            
        if not table_exists:
            # 创建表
            metadata = MetaData()
            table = Table(
                table_name,
                metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("sender_id", String(50), nullable=False, comment="发送者QQ号"),
                Column("sender_nickname", String(255), nullable=False, comment="发送者昵称"),
                Column("send_time", DateTime, nullable=False, comment="发送时间"),
                Column("message_content", Text, comment="消息内容（文本）"),
                Column("reply_to", Text, comment="引用内容"),
                Column("raw_message", Text, nullable=False, comment="原始消息"),
                Column("message_type", String(50), nullable=False, comment="消息类型"),
                Column("image_filename", Text, nullable=True, comment="图片文件名"),
                Column("has_image", Boolean, default=False, comment="是否包含图片"),
            )
            metadata.create_all(self.engine)
            logger.info(f"创建数据表: {table_name}")
    
    async def download_image(self, url: str, group_id: int,event) -> Optional[str]:
        """下载图片并保存到指定目录"""
        if not self._initialized:
            await self.initialize()
            
        if not self.config.enable_image_download:
            return None
            
        try:
            # 创建群聊对应的图片目录
            group_base_dir = self.data_storage_path / f"{group_id}"
            group_image_dir = group_base_dir / "pic"
            group_image_dir.mkdir(parents=True, exist_ok=True)
            # 生成文件名（时间戳）
            
            extent_name=await extract_extent_name(event)

            timestamp = int(time.time() * 1000)
            filename = f"{timestamp}.{extent_name}"
            filepath = group_image_dir / filename
            # TODO:支持多类型
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        async with aiofiles.open(filepath, 'wb') as f:
                            await f.write(await response.read())
                        logger.info(f"普通图片下载成功: {filename}")
                        return filename
                    else:
                        logger.error(f"普通图片下载失败，状态码: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"图片下载异常: {e}")
            return None
        

    async def download_face_image(self, url: str, group_id: int,event) -> Optional[str]:
        """下载表情图片并保存到指定目录"""
        if not self._initialized:
            await self.initialize()
            
        if not self.config.enable_face_image_download:
            return None
            
        try:
            # 创建群聊对应的图片目录
            group_base_dir = self.data_storage_path / f"{group_id}"
            group_image_dir = group_base_dir / "face"
            group_image_dir.mkdir(parents=True, exist_ok=True)
            # 生成文件名（时间戳）

            extent_name=await extract_extent_name(event)
            
            timestamp = int(time.time() * 1000)
            filename = f"{timestamp}.{extent_name}"
            filepath = group_image_dir / filename
            # TODO:支持多类型
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        async with aiofiles.open(filepath, 'wb') as f:
                            await f.write(await response.read())
                        logger.info(f"表情图片下载成功: {filename}")
                        return filename
                    else:
                        logger.error(f"表情图片下载失败，状态码: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"图片下载异常: {e}")
            return None
    
    async def extract_message_info(self, event: GroupMessageEvent) -> dict:
        """提取消息信息"""
        if not self._initialized:
            await self.initialize()
        message_info = {
            "sender_id": event.user_id,
            "sender_nickname": event.sender.nickname if event.sender else "未知",
            "send_time": event.time,
            "message_content": "",
            "reply_to": None,
            "raw_message": str(event.message),
            "message_type": "text",
            "image_filename": None,
            "has_image": False,
        }
        
        # 处理消息内容
        text_parts = []
        image_urls = []
        face_image_urls = []
        
        for segment in event.message:
            if segment.type == "text":
                text_parts.append(str(segment.data.get("text", "")))
            elif segment.type == "image":
                if str(event.message).count("动画表情")>0:
                    face_image_urls.append(segment.data.get("url", ""))
                else:
                    image_urls.append(segment.data.get("url", ""))
                message_info["has_image"] = True
                message_info["message_type"] = "image"
            elif segment.type == "reply":
                message_info["reply_to"] = str(segment.data)
        
        # 合并文本内容
        message_info["message_content"] = "".join(text_parts).strip()
        
        # 下载图片
        if image_urls and self.config.enable_image_download:
            _filenames=[]
            for image_url in image_urls:
                image_filename = await self.download_image(image_url, event.group_id,event)
                _filenames.append(image_filename)
            message_info["image_filename"] = ",".join(_filenames)
        if face_image_urls and self.config.enable_face_image_download:
            # image_filename = await self.download_face_image(image_urls[0], event.group_id)
            # message_info["image_filename"] = image_filename
            _filenames=[]
            for image_url in face_image_urls:
                image_filename = await self.download_face_image(image_url, event.group_id,event)
                _filenames.append(image_filename)
            message_info["image_filename"] = ",".join(_filenames)

        return message_info
    
    async def log_message(self, event: GroupMessageEvent):
        """记录消息到数据库"""
        try:
            # 确保表存在
            await self.ensure_table_exists(event.group_id)
            
            # 提取消息信息
            message_info = await self.extract_message_info(event)
            
            # 插入数据库
            table_name = f"group_msg_{event.group_id}"
            with self.session_factory() as session:
                # 使用原生SQL插入，避免ORM映射问题
                stmt = text(f"""
                    INSERT INTO {table_name} 
                    (sender_id, sender_nickname, send_time, message_content, reply_to, raw_message, message_type, image_filename, has_image)
                    VALUES 
                    (:sender_id, :sender_nickname, to_timestamp(:send_time), :message_content, :reply_to, :raw_message, :message_type, :image_filename, :has_image)
                """)
                
                session.execute(stmt, {
                    "sender_id": message_info["sender_id"],
                    "sender_nickname": message_info["sender_nickname"],
                    "send_time": message_info["send_time"],
                    "message_content": message_info["message_content"],
                    "reply_to": message_info["reply_to"],
                    "raw_message": message_info["raw_message"],
                    "message_type": message_info["message_type"],
                    "image_filename": message_info["image_filename"],
                    "has_image": message_info["has_image"],
                })
                session.commit()
                
            logger.info(f"消息记录成功 - 群组: {event.group_id}, 发送者: {message_info['sender_nickname']}, 发送内容: {message_info['message_content']}")
            
        except Exception as e:
            logger.error(f"消息记录失败: {e}")

# 创建消息记录器实例
message_logger = MessageLogger()
