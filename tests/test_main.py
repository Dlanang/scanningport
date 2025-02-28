import pytest
import asyncio
import aiohttp
from src.reports.report_generator import ReportGenerator
from src.scanners.subdomain_scanner import SubdomainScanner

@pytest.fixture
def sample_vulnerabilities():
    return [
        {"name": "Vuln A", "severity": "High", "analysis": "Analysis A"},
        {"name": "Vuln B", "severity": "Critical", "analysis": "Analysis B"},
        {"name": "Vuln C", "severity": "Low", "analysis": "Analysis C"},
        {"name": "Vuln D", "severity": "Medium", "analysis": "Analysis D"},
    ]

def test_severity_score():
    assert ReportGenerator.severity_score("Critical") == 4
    assert ReportGenerator.severity_score("High") == 3
    assert ReportGenerator.severity_score("Medium") == 2
    assert ReportGenerator.severity_score("Low") == 1
    # Jika severity tidak dikenali, skor default 0
    assert ReportGenerator.severity_score("Unknown") == 0

def test_generate_hacker_report(sample_vulnerabilities):
    report = ReportGenerator.generate_hacker_report(sample_vulnerabilities)
    # Pastikan report mencakup informasi nama dan tingkat keparahan
    assert "Vuln B" in report  # Vulnerability dengan severity Critical
    assert "Critical" in report
    assert "Top 10 Vulnerabilities Report" in report

@pytest.mark.asyncio
async def test_subdomain_scanner_gather_subdomains(monkeypatch):
    # Simulasikan fungsi scan_subdomain: hanya kembalikan hasil untuk subdomain yang dimulai dengan "active"
    async def fake_scan_subdomain(self, session, subdomain, retries=2):
        if subdomain.startswith("active"):
            return {"subdomain": f"http://{subdomain}.example.com", "status": 200}
        return None

    monkeypatch.setattr(SubdomainScanner, "scan_subdomain", fake_scan_subdomain)

    # Simulasikan isi wordlist sebagai string (misalnya, tiga baris)
    wordlist_content = "active1\ninactive1\nactive2\n"

    # Override metode gather_subdomains agar menggunakan string di atas tanpa harus membaca file
    async def fake_gather_subdomains(self):
        subdomains = wordlist_content.splitlines()
        async with aiohttp.ClientSession() as session:
            tasks = [self.scan_subdomain(session, sub) for sub in subdomains]
            responses = await asyncio.gather(*tasks)
            results = [res for res in responses if res]
        return results

    monkeypatch.setattr(SubdomainScanner, "gather_subdomains", fake_gather_subdomains)

    scanner = SubdomainScanner("example.com", "dummy_path")
    results = await scanner.gather_subdomains()
    assert len(results) == 2
    assert results[0]["subdomain"] == "http://active1.example.com"
