import json
import base64
from typing import Dict, Optional
from cryptography.fernet import Fernet
import os

# 生成加密密钥（生产环境应该从环境变量读取）
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)


class SecureConfig:
    """加密配置存储"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "secure_config.json")
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            default_config = {"providers": {}}
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def encrypt(self, data: str) -> str:
        """加密数据"""
        encrypted = cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = cipher.decrypt(encrypted)
        return decrypted.decode()

    def save_provider(self, provider_id: str, config: Dict) -> bool:
        """保存提供商配置（加密 API Key）"""
        try:
            if 'providers' not in self.config:
                self.config['providers'] = {}

            # 加密 API Key
            encrypted_apikey = self.encrypt(config.get('apiKey', ''))

            self.config['providers'][provider_id] = {
                'baseUrl': config.get('baseUrl', ''),
                'apiKey': encrypted_apikey,
                'contextWindow': config.get('contextWindow', 64000),
                'maxTokens': config.get('maxTokens', 8000)
            }

            return self._save_config()
        except Exception as e:
            print(f"保存提供商配置失败: {e}")
            return False

    def get_provider(self, provider_id: str) -> Optional[Dict]:
        """获取提供商配置（解密 API Key）"""
        try:
            if provider_id not in self.config['providers']:
                return None

            provider = self.config['providers'][provider_id]
            
            # 解密 API Key
            decrypted_apikey = self.decrypt(provider['apiKey'])

            return {
                'baseUrl': provider['baseUrl'],
                'apiKey': decrypted_apikey,
                'contextWindow': provider['contextWindow'],
                'maxTokens': provider['maxTokens']
            }
        except Exception as e:
            print(f"获取提供商配置失败: {e}")
            return None

    def get_all_providers(self) -> Dict:
        """获取所有提供商配置（不返回 API Key）"""
        providers = {}
        for provider_id, provider in self.config.get('providers', {}).items():
            providers[provider_id] = {
                'baseUrl': provider['baseUrl'],
                'contextWindow': provider['contextWindow'],
                'maxTokens': provider['maxTokens']
            }
        return providers
