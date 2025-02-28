# src/scanners/subdomain_scanner.py
import asyncio
import aiohttp
import aiofiles
from typing import List, Optional, Dict
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class SubdomainScanner:
    """Melakukan scanning subdomain secara asinkron."""

    def __init__(self, target_domain: str, wordlist_path: str):
        self.target_domain = target_domain
        self.wordlist_path = wordlist_path

    async def scan_subdomain(self, session: aiohttp.ClientSession, subdomain: str, retries: int = 2) -> Optional[Dict]:
        url = f"http://{subdomain}.{self.target_domain}"
        for attempt in range(1, retries + 2):
            try:
                async with session.get(url, timeout=5) as response:
                    if response.status < 400:
                        logger.info(f"Subdomain aktif: {url} (Status: {response.status})")
                        return {"subdomain": url, "status": response.status}
            except Exception as e:
                logger.debug(f"Gagal memindai {url} pada percobaan {attempt}: {e}")
                await asyncio.sleep(1 * attempt)  # exponential backoff sederhana
        return None

    async def gather_subdomains(self) -> List[Dict]:
        results = []
        async with aiohttp.ClientSession() as session:
            # Membaca file wordlist secara asinkron
            async with aiofiles.open(self.wordlist_path, mode="r") as f:
                content = await f.read()
            subdomains = [line.strip() for line in content.splitlines() if line.strip()]
            tasks = [self.scan_subdomain(session, sub) for sub in subdomains]
            responses = await asyncio.gather(*tasks)
            results = [res for res in responses if res]
        return results
