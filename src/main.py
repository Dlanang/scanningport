# src/main.py
import asyncio
import json
import argparse
from config.config import SUBDOMAIN_WORDLIST_PATH, COMMON_PORTS
from src.scanners.subdomain_scanner import SubdomainScanner
from src.scanners.port_scanner import PortScanner
from src.integrations.deepseek_client import DeepSeekClient
from src.integrations.deepseek_reasoner import DeepSeekReasoner
from src.reports.report_generator import ReportGenerator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

async def main(target_domain: str, wordlist_path: str, output_file: str, report_file: str, analyze_flag: bool):
    logger.info(f"Memulai scan untuk {target_domain} dengan IntegrityHackerPro Ultimate QA-Enhanced")
    
    # 1. Subdomain scanning
    subdomain_scanner = SubdomainScanner(target_domain, wordlist_path)
    active_subdomains = await subdomain_scanner.gather_subdomains()
    logger.info(f"Ditemukan {len(active_subdomains)} subdomain aktif.")
    
    # 2. Port scanning untuk setiap subdomain aktif
    port_scanner = PortScanner(COMMON_PORTS)
    for entry in active_subdomains:
        host = entry["subdomain"].replace("http://", "").replace("https://", "")
        open_ports = await port_scanner.scan_ports(host)
        entry["open_ports"] = open_ports

    # 3. Mengambil data vulnerabilities dari DeepSeek
    deepseek_client = DeepSeekClient()
    vulnerabilities = await deepseek_client.gather_vulnerabilities(target_domain)
    
    # 4. Analisis vulnerabilities dengan DeepSeek Reasoner (jika --analyze diaktifkan)
    if analyze_flag and vulnerabilities:
        deepseek_reasoner = DeepSeekReasoner()
        for vuln in vulnerabilities:
            analysis = await deepseek_reasoner.analyze_async(vuln)
            vuln["analysis"] = analysis

    # 5. Buat laporan hacker (Top 10 vulnerabilities)
    hacker_report = ReportGenerator.generate_hacker_report(vulnerabilities) if vulnerabilities else "No vulnerabilities found."
    
    # 6. Gabungkan hasil scan ke dalam output akhir
    results = {
        "target_domain": target_domain,
        "active_subdomains": active_subdomains,
        "vulnerabilities": vulnerabilities,
        "hacker_report": hacker_report
    }
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Hasil scan disimpan di {output_file}")

    with open(report_file, "w") as f:
        f.write(hacker_report)
    logger.info(f"Hacker report disimpan di {report_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IntegrityHackerPro Ultimate QA-Enhanced: Alat Bug Bounty Canggih berbasis metodologi pentesting")
    parser.add_argument("-t", "--target", required=True, help="Domain target (misal: example.com)")
    parser.add_argument("-w", "--wordlist", default=SUBDOMAIN_WORDLIST_PATH, help="Path file wordlist subdomain")
    parser.add_argument("-o", "--output", default="integrity_hacker_pro_results.json", help="File output JSON")
    parser.add_argument("-r", "--report", default="hacker_report.txt", help="File output laporan hacker")
    parser.add_argument("--analyze", action="store_true", help="Aktifkan analisis vulnerability menggunakan DeepSeek Reasoner")
    args = parser.parse_args()

    asyncio.run(main(args.target, args.wordlist, args.output, args.report, args.analyze))
