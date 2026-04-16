"""
LLM客户端封装
统一使用OpenAI格式调用
"""

import json
import re
from typing import Optional, Dict, Any, List
import httpx
from openai import OpenAI

from ..config import Config


class LLMClient:
    """LLM客户端"""

    # Mapping from role name → (api_key_attr, base_url_attr, model_name_attr)
    _ROLE_CONFIG: Dict[str, tuple] = {
        "strong": ("MODEL_STRONG_API_KEY", "MODEL_STRONG_BASE_URL", "MODEL_STRONG_NAME"),
        "fast":   ("MODEL_FAST_API_KEY",   "MODEL_FAST_BASE_URL",   "MODEL_FAST_NAME"),
        "local":  ("MODEL_LOCAL_API_KEY",  "MODEL_LOCAL_BASE_URL",  "MODEL_LOCAL_NAME"),
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME

        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=httpx.Timeout(connect=10.0, read=120.0, write=30.0, pool=5.0),
            max_retries=0,  # let retry_with_backoff handle retries
        )

    @classmethod
    def for_role(cls, role: str) -> "LLMClient":
        """
        Factory: return an LLMClient pre-configured for a named model role.

        Roles
        -----
        "strong"  Quality-critical tasks — report generation, ontology building.
                  Set MODEL_STRONG_NAME / MODEL_STRONG_BASE_URL / MODEL_STRONG_API_KEY.
        "fast"    Bulk / cheap tasks — agent-profile generation, simulation config.
                  Set MODEL_FAST_NAME / MODEL_FAST_BASE_URL / MODEL_FAST_API_KEY.
        "local"   Dev / testing via Ollama or any OpenAI-compatible local server.
                  Set MODEL_LOCAL_NAME / MODEL_LOCAL_BASE_URL / MODEL_LOCAL_API_KEY.
        other     Falls back to the default LLM_* config (backward compatible).
        """
        if role not in cls._ROLE_CONFIG:
            return cls()

        key_attr, url_attr, name_attr = cls._ROLE_CONFIG[role]
        return cls(
            api_key=getattr(Config, key_attr),
            base_url=getattr(Config, url_attr),
            model=getattr(Config, name_attr),
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式（如JSON模式）
            
        Returns:
            模型响应文本
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        # 部分模型（如MiniMax M2.5）会在content中包含<think>思考内容，需要移除
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content
    
    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回JSON
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            解析后的JSON对象
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        # 清理markdown代码块标记
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE)
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"LLM返回的JSON格式无效: {cleaned_response}")

