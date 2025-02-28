# src/integrations/deepseek_client.py
import aiohttp
from typing import Optional, Dict, Any
from src.utils.logger import setup_logger
from config.config import DEEPSEEK_API_KEY, DEEPSEEK_VULN_ENDPOINT

logger = setup_logger(__name__)

class DeepSeekClient:
    """
    Interaksi dengan DeepSeek Vulnerability API.
    """

    def __init__(self, api_key: str = DEEPSEEK_API_KEY, endpoint: str = DEEPSEEK_VULN_ENDPOINT):
        self.api_key = api_key
        self.endpoint = endpoint

    async def search_vulnerabilities(self, query: str) -> Optional[Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        params = {"q": query}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.endpoint, headers=headers, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"DeepSeek menemukan celah untuk query: {query}")
                        return data
                    else:
                        logger.error(f"DeepSeek API error: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Error memanggil DeepSeek API: {e}")
                return None

    async def gather_vulnerabilities(self, target_domain: str) -> list:
        query = f"domain:{target_domain}"
        data = await self.search_vulnerabilities(query)
        if data:
            vulnerabilities = data.get("vulnerabilities", [])
            logger.info(f"Ditemukan {len(vulnerabilities)} celah untuk {target_domain}")
            return vulnerabilities
        return []
