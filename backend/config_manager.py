import json
import os
from typing import Dict, List, Optional, Tuple
from models import ProviderConfig, ProviderModel


class ConfigManager:
    """配置文件管理器"""

    def __init__(self, config_path: str = "C:\\Users\\Administrator\\.openclaw\\openclaw.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载配置文件，如果不存在则创建默认配置"""
        if not os.path.exists(self.config_path):
            print(f"配置文件不存在，创建默认配置: {self.config_path}")
            # 创建目录
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            # 默认配置结构
            default_config = {
                "agents": {
                    "defaults": {
                        "model": {
                            "primary": ""
                        },
                        "models": {}
                    }
                },
                "models": {
                    "providers": {}
                }
            }
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

    def get_current_model(self) -> Optional[str]:
        """获取当前使用的模型"""
        try:
            return self.config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary')
        except Exception as e:
            print(f"获取当前模型失败: {e}")
            return None

    def get_all_providers(self) -> Dict:
        """获取所有提供商"""
        return self.config.get('models', {}).get('providers', {})

    def save_provider(self, provider_id: str, base_url: str, api_key: str, model_id: str) -> bool:
        """保存提供商配置（apiKey不保存到JSON文件）"""
        try:
            # 确保 models.providers 节点存在
            if 'models' not in self.config:
                self.config['models'] = {}
            if 'providers' not in self.config['models']:
                self.config['models']['providers'] = {}

            # 检查提供商是否已存在
            providers = self.config['models']['providers']

            if provider_id not in providers:
                # 创建新提供商（不保存apiKey）
                provider_config = ProviderConfig(
                    baseUrl=base_url or "",
                    apiKey="",  # 不保存apiKey到JSON
                    models=[ProviderModel(
                        id=model_id,
                        name=f"{model_id}"
                    )]
                )
                providers[provider_id] = provider_config.dict()
            else:
                # 提供商已存在，更新基础信息（不更新apiKey）
                provider = providers[provider_id]
                if base_url:
                    provider['baseUrl'] = base_url
                # 注意：不保存 api_key 到 JSON 文件

                # 添加模型
                models = provider.get('models', [])
                model_ids = [m['id'] for m in models]

                if model_id not in model_ids:
                    models.append({
                        'id': model_id,
                        'name': f"{model_id}",
                        'reasoning': False,
                        'input': ['text'],
                        'cost': {'input': 0, 'output': 0, 'cacheRead': 0, 'cacheWrite': 0},
                        'contextWindow': 64000,
                        'maxTokens': 8000
                    })
                    provider['models'] = models

            return self._save_config()
        except Exception as e:
            print(f"保存提供商配置失败: {e}")
            return False

    def switch_model(self, provider_id: str, model_id: str) -> bool:
        """切换模型（同时保存到通讯录）"""
        # 先保存到通讯录
        self.save_provider(provider_id, "", "", model_id)
        # 再设置为当前模型
        return self.switch_model_only(provider_id, model_id)

    def switch_model_only(self, provider_id: str, model_id: str) -> bool:
        """只切换模型（不保存到通讯录）"""
        try:
            # 确保 agents.defaults 节点存在
            if 'agents' not in self.config:
                self.config['agents'] = {}
            if 'defaults' not in self.config['agents']:
                self.config['agents']['defaults'] = {}
            if 'model' not in self.config['agents']['defaults']:
                self.config['agents']['defaults']['model'] = {}
            if 'models' not in self.config['agents']['defaults']:
                self.config['agents']['defaults']['models'] = {}

            # 设置主模型
            primary_model = f"{provider_id}/{model_id}"
            self.config['agents']['defaults']['model']['primary'] = primary_model

            # 确保模型在 models 列表中
            models_dict = self.config['agents']['defaults']['models']
            if primary_model not in models_dict:
                models_dict[primary_model] = {}

            return self._save_config()
        except Exception as e:
            print(f"切换模型失败: {e}")
            return False

    def get_model_cards(self) -> List[Dict]:
        """获取所有模型卡片（不返回apiKey）"""
        cards = []
        current_model = self.get_current_model()

        providers = self.get_all_providers()

        for provider_id, provider_config in providers.items():
            models = provider_config.get('models', [])
            for model in models:
                model_id = model['id']
                full_id = f"{provider_id}/{model_id}"

                cards.append({
                    'id': full_id,
                    'modelId': model_id,
                    'providerId': provider_id,
                    'baseUrl': provider_config.get('baseUrl', ''),
                    # 不返回 apiKey，保护敏感信息
                    'isCurrent': full_id == current_model
                })

        return cards

    def delete_model(self, provider_id: str, model_id: str) -> bool:
        """删除单个模型"""
        try:
            providers = self.config.get('models', {}).get('providers', {})
            if provider_id not in providers:
                return False

            provider = providers[provider_id]
            models = provider.get('models', [])
            original_len = len(models)
            provider['models'] = [m for m in models if m.get('id') != model_id]

            if len(provider['models']) == original_len:
                return False

            return self._save_config()
        except Exception as e:
            print(f"删除模型失败: {e}")
            return False

    def delete_provider(self, provider_id: str) -> bool:
        """删除整个提供商"""
        try:
            providers = self.config.get('models', {}).get('providers', {})
            if provider_id not in providers:
                return False

            del providers[provider_id]
            return self._save_config()
        except Exception as e:
            print(f"删除提供商失败: {e}")
            return False

    def update_provider_apikey(self, provider_id: str, api_key: str) -> bool:
        """更新提供商的 API Key"""
        try:
            providers = self.config.get('models', {}).get('providers', {})
            if provider_id not in providers:
                return False

            providers[provider_id]['apiKey'] = api_key
            return self._save_config()
        except Exception as e:
            print(f"更新 API Key 失败: {e}")
            return False
