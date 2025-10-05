from pydantic import BaseModel, Field


class Config(BaseModel):
    """Plugin Config Here"""
    
    # PostgreSQL数据库配置
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/msglogger",
        description="PostgreSQL数据库连接URL"
    )
    
    # 数据存储路径
    data_storage_path: str = Field(
        default="./data",
        description="数据存储根目录路径"
    )
    
    # 是否启用图片下载
    enable_image_download: bool = Field(
        default=True,
        description="是否启用图片下载功能"
    )
    # 是否启用表情图片下载
    enable_face_image_download: bool = Field(
        default=True,
        description="是否启用表情图片下载"
    )
