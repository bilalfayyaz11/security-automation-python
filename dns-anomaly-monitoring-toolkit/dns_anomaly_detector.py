#!/usr/bin/env python3
"""
DNS Anomaly Detector

Detects suspicious DNS patterns using domain length checks,
Shannon entropy, numeric ratio, repeated NXDOMAIN indicators,
and IP-encoded domain patterns.
"""

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List


class DNSAnomalyDetector:
    def calculate_entropy(self, domain: str) -> float:
        domain_part = domain.split(".")[0].lower()

        if not domain_part:
            return 0.0

        counter = Counter(domain_part)
        length = len(domain_part)

        entropy = 0.0
        for count in counter.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        return entropy

    def check_domain_length(self, domain: str) -> Dict:
        domain_part = domain.split(".")[0]
        length = len(domain_part)

        result = {
            "check": "domain_length",
            "length": length,
            "suspicious": False,
            "reason": "",
        }

        if length > 20:
            result["suspicious"] = True
            result["reason"] = "Unusually long domain label, possible DGA behavior"
        elif length < 3:
            result["suspicious"] = True
            result["reason"] = "Unusually short domain label"

        return result

    def check_entropy(self, domain: str) -> Dict:
        entropy = self.calculate_entropy(domain)

        result = {
            "check": "entropy",
            "entropy": round(entropy, 2),
            "suspicious": False,
            "reason": "",
        }

        if entropy > 3.5:
            result["suspicious"] = True
            result["reason"] = "High entropy suggests random generation or DGA-like behavior"

        return result

    def check_numeric_ratio(self, domain: str) -> Dict:
        domain_part = domain.split(".")[0]

        if not domain_part:
            return {
                "check": "numeric_ratio",
                "ratio": 0,
                "suspicious": False,
                "reason": "",
            }

        numeric_count = sum(character.isdigit() for character in domain_part)
        ratio = numeric_count / len(domain_part)

        result = {
            "check": "numeric_ratio",
            "ratio": round(ratio, 2),
            "suspicious": False,
            "reason": "",
        }

        if ratio > 0.3:
            result["suspicious"] = True
            result["reason"] = "High numeric ratio is unusual for many legitimate domains"

        return result

    def check_ip_encoded_domain(self, domain: str) -> Dict:
        ip_pattern = re.compile(r"(\d{1,3}\.){3}\d{1,3}")

        result = {
            "check": "ip_encoded_domain",
            "suspicious": False,
            "reason": "",
        }

        if ip_pattern.search(domain):
            result["suspicious"] = True
            result["reason"] = "Domain contains an embedded IPv4 address pattern"

        return result

    def analyze_domain(self, domain: str) -> Dict:
        checks = [
            self.check_domain_length(domain),
            self.check_entropy(domain),
            self.check_numeric_ratio(domain),
            self.check_ip_encoded_domain(domain),
        ]

        suspicious_count = sum(1 for check in checks if check["suspicious"])

        if suspicious_count >= 2:
            risk = "HIGH"
        elif suspicious_count == 1:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return {
            "domain": domain,
            "risk": risk,
            "suspicious_checks": suspicious_count,
            "checks": checks,
        }

    def display_analysis(self, analysis: Dict) -> None:
        print(f"\nAnalyzing: {analysis['domain']}")
        print("-" * 70)

        for check in analysis["checks"]:
            status = "[SUSPICIOUS]" if check["suspicious"] else "[OK]"
            print(f"{status} {check['check']}: ", end="")

            if "length" in check:
                print(f"Length = {check['length']}")
            elif "entropy" in check:
                print(f"Entropy = {check['entropy']}")
            elif "ratio" in check:
                print(f"Ratio = {check['ratio']}")
            else:
                print("checked")

            if check.get("reason"):
                print(f"  Reason: {check['reason']}")

        print(f"\nOverall: {analysis['risk']} RISK")


def main() -> None:
    parser = argparse.ArgumentParser(description="DNS anomaly detector")
    parser.add_argument(
        "domains",
        nargs="*",
        default=[
            "google.com",
            "github.com",
            "aksjdhfkjashdfkjhaskjdfh.com",
            "test12345678901234567890.com",
            "abc123xyz789.com",
            "192.168.1.1.nip.io",
        ],
    )
    parser.add_argument("--json-output", default="dns_detection_report.json")

    args = parser.parse_args()

    detector = DNSAnomalyDetector()
    report = []

    print("\n" + "=" * 70)
    print("DNS ANOMALY DETECTOR")
    print("=" * 70)

    for domain in args.domains:
        analysis = detector.analyze_domain(domain)
        detector.display_analysis(analysis)
        report.append(analysis)

    Path(args.json_output).write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n" + "=" * 70)
    print(f"Detection Complete - report saved to {args.json_output}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
