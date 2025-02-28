# src/integrations/deepseek_reasoner.py
import asyncio
from typing import Dict, Any
from src.utils.logger import setup_logger
from openai import OpenAI  # Pastikan package openai sudah di-install
from config.config import DEEPSEEK_API_KEY, DEEPSEEK_REASONER_BASE

logger = setup_logger(__name__)

class DeepSeekReasoner:
    """Menganalisis celah keamanan menggunakan DeepSeek Reasoner (DeepSex)."""

    def __init__(self, api_key: str = DEEPSEEK_API_KEY, base_url: str = DEEPSEEK_REASONER_BASE):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def analyze(self, vulnerability: Dict[str, Any]) -> str:
        messages = [
            {"role": "system", "content": "You are a security reasoning assistant."},
            {"role": "user", "content": (
                f"Jelaskan potensi dampak dan strategi mitigasi untuk vulnerability "
                f"'{vulnerability.get('name', 'unknown')}' dengan tingkat keparahan "
                f"'{vulnerability.get('severity', 'unknown')}'."
            )}
        ]
        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            stream=False
        )
        analysis = response.choices[0].message.content
        logger.info(f"Analisis selesai untuk {vulnerability.get('name', 'unknown')}")
        return analysis

    async def analyze_async(self, vulnerability: Dict[str, Any]) -> str:
        return await asyncio.to_thread(self.analyze, vulnerability)
