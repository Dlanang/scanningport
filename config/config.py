# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Membaca file .env

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_API_KEY")
DEEPSEEK_VULN_ENDPOINT = os.getenv("DEEPSEEK_VULN_ENDPOINT", "https://api.deepseek.com/v1/search")
DEEPSEEK_REASONER_BASE = os.getenv("DEEPSEEK_REASONER_BASE", "https://api.deepseek.com")
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 8080]
SUBDOMAIN_WORDLIST_PATH = os.getenv("SUBDOMAIN_WORDLIST_PATH", "data/subdomains.txt")
