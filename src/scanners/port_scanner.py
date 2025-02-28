# src/scanners/port_scanner.py
import asyncio
from typing import List, Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class PortScanner:
    """Melakukan port scanning secara asinkron untuk sebuah host."""

    def __init__(self, common_ports: List[int]):
        self.common_ports = common_ports

    async def scan_port(self, host: str, port: int) -> Optional[int]:
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=2)
            writer.close()
            await writer.wait_closed()
            logger.info(f"Port {port} terbuka di {host}")
            return port
        except Exception as e:
            logger.debug(f"Port {port} tertutup di {host}: {e}")
            return None

    async def scan_ports(self, host: str) -> List[int]:
        tasks = [self.scan_port(host, port) for port in self.common_ports]
        results = await asyncio.gather(*tasks)
        return [port for port in results if port is not None]
