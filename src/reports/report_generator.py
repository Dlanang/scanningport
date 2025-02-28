# src/reports/report_generator.py
from typing import List, Dict
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class ReportGenerator:
    """Menghasilkan laporan celah keamanan berdasarkan data vulnerability."""

    @staticmethod
    def severity_score(severity: str) -> int:
        mapping = {
            "Critical": 4,
            "High": 3,
            "Medium": 2,
            "Low": 1
        }
        return mapping.get(severity.capitalize(), 0)

    @classmethod
    def generate_hacker_report(cls, vulnerabilities: List[Dict]) -> str:
        sorted_vulns = sorted(vulnerabilities, key=lambda v: cls.severity_score(v.get("severity", "Low")), reverse=True)
        top_10 = sorted_vulns[:10]
        
        report_lines = ["===== Top 10 Vulnerabilities Report (Hacker's Insight) ====="]
        for idx, vuln in enumerate(top_10, start=1):
            name = vuln.get("name", "N/A")
            severity = vuln.get("severity", "N/A")
            analysis = vuln.get("analysis", "No analysis provided.")
            report_lines.append(f"{idx}. {name} | Severity: {severity}")
            report_lines.append(f"   Analysis: {analysis}")
            report_lines.append("-" * 60)
        report = "\n".join(report_lines)
        logger.info("Hacker report telah dibuat.")
        return report
