import json
import os
from typing import Dict, List, Optional


class ConfigManager:
    """配置文件管理器"""

    def __init__(self, config_path: str = None):
        # 使用用户主目录，跨平台兼容
        if config_path is None:
            config_path = os.path.join(
                os.path.expanduser("~"), ".openclaw", "openclaw.json"
            )
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载配置文件，如果不存在则创建默认配置"""
        if not os.path.exists(self.config_path):
            print(f"配置文件不存在，创建默认配置: {self.config_path}")
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            default_config = {
                "agents": {"defaults": {"model": {"primary": ""}, "models": {}}},
                "models": {"providers": {}},
            }
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def get_current_model(self) -> Optional[str]:
        """获取当前使用的模型"""
        try:
            return (
                self.config.get("agents", {})
                .get("defaults", {})
                .get("model", {})
                .get("primary")
            )
        except Exception as e:
            print(f"获取当前模型失败: {e}")
            return None

    def get_all_providers(self) -> Dict:
        """获取所有提供商"""
        return self.config.get("models", {}).get("providers", {})

    def save_provider(
        self,
        provider_id: str,
        base_url: str,
        api_key: str,
        model_id: str,
        context_window: int = 64000,
        max_tokens: int = 8000,
    ) -> bool:
        """保存提供商配置（同时更新 openclaw.json 和 auth-profiles.json）"""
        try:
            if "models" not in self.config:
                self.config["models"] = {}
            if "providers" not in self.config["models"]:
                self.config["models"]["providers"] = {}

            providers = self.config["models"]["providers"]

            if provider_id not in providers:
                providers[provider_id] = {
                    "baseUrl": base_url or "",
                    "apiKey": "",
                    "models": [{"id": model_id, "name": model_id}],
                }
            else:
                provider = providers[provider_id]
                if base_url:
                    provider["baseUrl"] = base_url
                if api_key:
                    provider["apiKey"] = api_key

                models = provider.get("models", [])
                model_ids = [m["id"] for m in models]

                if model_id not in model_ids:
                    models.append(
                        {
                            "id": model_id,
                            "name": model_id,
                            "reasoning": False,
                            "input": ["text"],
                            "cost": {
                                "input": 0,
                                "output": 0,
                                "cacheRead": 0,
                                "cacheWrite": 0,
                            },
                            "contextWindow": context_window,
                            "maxTokens": max_tokens,
                        }
                    )
                    provider["models"] = models

            # 保存配置
            saved = self._save_config()

            # 如果提供了 API Key，同时更新认证文件
            if api_key:
                self.update_provider_apikey(provider_id, api_key)

            return saved
        except Exception as e:
            print(f"保存提供商配置失败: {e}")
            return False

    def update_provider_config(self, provider_id: str, base_url: str, api_key: str, context_window: int = 64000, max_tokens: int = 8000) -> bool:
        """只更新提供商的配置信息，不添加模型（更新 openclaw.json）"""
        try:
            if "models" not in self.config:
                self.config["models"] = {}
            if "providers" not in self.config["models"]:
                self.config["models"]["providers"] = {}

            providers = self.config["models"]["providers"]

            if provider_id not in providers:
                providers[provider_id] = {
                    "baseUrl": base_url or "",
                    "apiKey": api_key or "",
                    "api": "openai-completions",
                    "models": [],
                }
            else:
                provider = providers[provider_id]
                if base_url:
                    provider["baseUrl"] = base_url
                if api_key:
                    provider["apiKey"] = api_key

            return self._save_config()
        except Exception as e:
            print(f"更新提供商配置失败: {e}")
            return False

    def switch_model_only(self, provider_id: str, model_id: str) -> bool:
        """只切换模型（不保存到通讯录）"""
        try:
            if "agents" not in self.config:
                self.config["agents"] = {}
            if "defaults" not in self.config["agents"]:
                self.config["agents"]["defaults"] = {}
            if "model" not in self.config["agents"]["defaults"]:
                self.config["agents"]["defaults"]["model"] = {}
            if "models" not in self.config["agents"]["defaults"]:
                self.config["agents"]["defaults"]["models"] = {}

            primary_model = f"{provider_id}/{model_id}"
            self.config["agents"]["defaults"]["model"]["primary"] = primary_model

            models_dict = self.config["agents"]["defaults"]["models"]
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
            models = provider_config.get("models", [])
            for model in models:
                model_id = model["id"]
                full_id = f"{provider_id}/{model_id}"

                cards.append(
                    {
                        "id": full_id,
                        "modelId": model_id,
                        "providerId": provider_id,
                        "baseUrl": provider_config.get("baseUrl", ""),
                        "isCurrent": full_id == current_model,
                    }
                )

        return cards

    def delete_model(self, provider_id: str, model_id: str) -> bool:
        """删除单个模型"""
        try:
            providers = self.config.get("models", {}).get("providers", {})
            if provider_id not in providers:
                return False

            provider = providers[provider_id]
            models = provider.get("models", [])
            provider["models"] = [m for m in models if m.get("id") != model_id]

            return self._save_config()
        except Exception as e:
            print(f"删除模型失败: {e}")
            return False

    def delete_provider(self, provider_id: str) -> bool:
        """删除整个提供商"""
        try:
            providers = self.config.get("models", {}).get("providers", {})
            if provider_id not in providers:
                return False

            del providers[provider_id]
            return self._save_config()
        except Exception as e:
            print(f"删除提供商失败: {e}")
            return False

    def update_provider_apikey(self, provider_id: str, api_key: str) -> bool:
        """更新提供商的 API Key（同时更新 openclaw.json 和 auth-profiles.json）"""
        try:
            providers = self.config.get("models", {}).get("providers", {})
            if provider_id not in providers:
                return False

            providers[provider_id]["apiKey"] = api_key
            openclaw_saved = self._save_config()

            self.update_auth_profile(provider_id, api_key)

            return openclaw_saved
        except Exception as e:
            print(f"更新 API Key 失败: {e}")
            return False

    def update_auth_profile(self, provider_id: str, api_key: str) -> bool:
        """更新 auth-profiles.json（OpenClaw 认证文件）"""
        try:
            auth_profiles_path = os.path.join(
                os.path.expanduser("~"),
                ".openclaw",
                "agents",
                "main",
                "agent",
                "auth-profiles.json",
            )

            if os.path.exists(auth_profiles_path):
                with open(auth_profiles_path, "r", encoding="utf-8") as f:
                    auth_config = json.load(f)
            else:
                auth_config = {"profiles": {}}

            profile_id = f"{provider_id}:manual"
            if "profiles" not in auth_config:
                auth_config["profiles"] = {}

            auth_config["profiles"][profile_id] = {
                "type": "token",
                "provider": provider_id,
                "token": api_key,
            }

            os.makedirs(os.path.dirname(auth_profiles_path), exist_ok=True)
            with open(auth_profiles_path, "w", encoding="utf-8") as f:
                json.dump(auth_config, f, indent=2, ensure_ascii=False)

            print(f"[ConfigManager] 已更新 auth-profiles.json: {profile_id}")
            return True
        except Exception as e:
            print(f"[ConfigManager] 更新 auth-profiles.json 失败: {e}")
            return False
