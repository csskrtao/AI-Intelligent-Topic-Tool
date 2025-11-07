"""
配置管理模块
负责加载和管理应用程序配置，包括 API Key、环境变量等
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """应用程序配置类"""
    
    def __init__(self):
        """初始化配置，加载环境变量"""
        # 加载 .env 文件
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        
        # API 配置
        self.api_key: str = os.getenv('MODELVERSE_API_KEY', '')
        self.api_base_url: str = os.getenv(
            'MODELVERSE_API_BASE_URL', 
            'https://api.modelverse.cn/v1'
        )
        self.ocr_model_name: str = os.getenv(
            'OCR_MODEL_NAME', 
            'deepseek-ai/DeepSeek-OCR'
        )
        
        # 请求配置
        self.ocr_timeout: int = int(os.getenv('OCR_TIMEOUT', '30'))
        self.max_tokens: int = int(os.getenv('MAX_TOKENS', '8192'))
        
        # 导出配置
        self.export_dir: Path = Path(__file__).parent.parent / os.getenv('EXPORT_DIR', 'exports')
        
        # 确保导出目录存在
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        验证配置是否完整
        
        Returns:
            tuple[bool, Optional[str]]: (是否有效, 错误信息)
        """
        if not self.api_key:
            return False, "未配置 MODELVERSE_API_KEY，请在 .env 文件中设置"
        
        if not self.api_base_url:
            return False, "API 基础 URL 未配置"
        
        return True, None
    
    def get_api_endpoint(self, endpoint: str = 'chat/completions') -> str:
        """
        获取完整的 API 端点 URL
        
        Args:
            endpoint: API 端点路径
            
        Returns:
            str: 完整的 URL
        """
        return f"{self.api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    def __repr__(self) -> str:
        """返回配置的字符串表示（隐藏敏感信息）"""
        masked_key = f"{self.api_key[:8]}..." if len(self.api_key) > 8 else "***"
        return (
            f"Config(api_key={masked_key}, "
            f"api_base_url={self.api_base_url}, "
            f"ocr_model={self.ocr_model_name})"
        )


# 全局配置实例
config = Config()


if __name__ == '__main__':
    # 测试配置加载
    print("配置信息:", config)
    is_valid, error_msg = config.validate()
    if is_valid:
        print("✓ 配置验证通过")
    else:
        print(f"✗ 配置验证失败: {error_msg}")

