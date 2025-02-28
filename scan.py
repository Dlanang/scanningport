#!/usr/bin/env python
import argparse
import asyncio
from src.main import main
from config.config import SUBDOMAIN_WORDLIST_PATH

def parse_args():
    parser = argparse.ArgumentParser(
        description="IntegrityHackerPro Ultimate QA-Enhanced - Scanning Tool"
    )
    parser.add_argument(
        "-t", "--target", required=True,
        help="Domain target (misal: example.com)"
    )
    parser.add_argument(
        "-w", "--wordlist", default=SUBDOMAIN_WORDLIST_PATH,
        help="Path file wordlist subdomain (default: data/subdomains.txt)"
    )
    parser.add_argument(
        "-o", "--output", default="integrity_hacker_pro_results.json",
        help="File output untuk hasil scan dalam format JSON"
    )
    parser.add_argument(
        "-r", "--report", default="hacker_report.txt",
        help="File output untuk laporan hacker (teks)"
    )
    parser.add_argument(
        "--analyze", action="store_true",
        help="Aktifkan analisis vulnerability menggunakan DeepSeek Reasoner"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.target, args.wordlist, args.output, args.report, args.analyze))
