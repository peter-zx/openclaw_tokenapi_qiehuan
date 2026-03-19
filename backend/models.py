from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class ProviderModel(BaseModel):
    id: str
    name: str
    reasoning: bool = False
    input: List[str] = ["text"]
    cost: Dict = {}
    contextWindow: int = 64000
    maxTokens: int = 8000


class ProviderConfig(BaseModel):
    baseUrl: str
    apiKey: str
    api: str = "openai-completions"
    models: List[ProviderModel] = []


class ModelSwitchRequest(BaseModel):
    providerId: str
    baseUrl: str
    apiKey: str
    modelId: str


class GatewayControlRequest(BaseModel):
    action: str = Field(..., description="Action: start, stop, restart")
