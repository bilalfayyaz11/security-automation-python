#!/usr/bin/env python3
"""
Command-line security scanner for detecting sensitive patterns in files.
"""

import argparse
import os
import re
import sys
from collections import defaultdict


class SecurityScanner:
    """CLI security scanner for files and directories."""

    def __init__(self):
        self.patterns = {
            "hardcoded_password": {
                "regex": r'\b(password|passwd|pwd|database_password|db_password|secret_key)\b\s*=\s*["\'][^"\']+["\']',
                "severity": "HIGH",
                "description": "Potential hardcoded password or secret assignment"
            },
            "api_key": {
                "regex": r'\b(api_key|apikey|api-key|access_key|token)\b\s*=\s*["\'][^"\']+["\']',
                "severity": "HIGH",
                "description": "Potential hardcoded API key or access token"
            },
            "private_key": {
                "regex": r'-----BEGIN\s+(RSA\s+|DSA\s+|EC\s+|OPENSSH\s+)?PRIVATE\s+KEY-----',
                "severity": "CRITICAL",
                "description": "Private key material detected"
            },
            "ip_address": {
                "regex": r'\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b',
                "severity": "LOW",
                "description": "IPv4 address detected"
            },
            "email": {
                "regex": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
                "severity": "LOW",
                "description": "Email address detected"
            }
        }
        self.findings = []

    def scan_file(self, filepath):
        if not os.path.isfile(filepath):
            print(f"Error: File '{filepath}' not found")
            return

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                lines = file.readlines()
        except Exception as error:
            print(f"Error reading file '{filepath}': {error}")
            return

        for line_num, line in enumerate(lines, start=1):
            for issue_type, rule in self.patterns.items():
                matches = re.finditer(rule["regex"], line, re.IGNORECASE)

                for match in matches:
                    self.findings.append({
                        "file": filepath,
                        "line": line_num,
                        "type": issue_type,
                        "severity": rule["severity"],
                        "description": rule["description"],
                        "content": line.strip(),
                        "match": match.group()
                    })

    def scan_directory(self, dirpath):
        if not os.path.isdir(dirpath):
            print(f"Error: Directory '{dirpath}' not found")
            return

        ignored_dirs = {"__pycache__", ".git", ".venv", "venv", "node_modules"}

        for root, dirs, files in os.walk(dirpath):
            dirs[:] = [directory for directory in dirs if directory not in ignored_dirs]

            for filename in files:
                if filename.startswith("."):
                    continue

                filepath = os.path.join(root, filename)
                self.scan_file(filepath)

    def generate_report(self):
        print("\n" + "=" * 76)
        print("SECURITY SCAN REPORT")
        print("=" * 76)

        if not self.findings:
            print("\nNo security issues found.")
            return

        print(f"\nTotal Issues Found: {len(self.findings)}")

        severity_counts = defaultdict(int)
        type_groups = defaultdict(list)

        for finding in self.findings:
            severity_counts[finding["severity"]] += 1
            type_groups[finding["type"]].append(finding)

        print("\nSeverity Summary:")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if severity_counts[severity]:
                print(f"  {severity}: {severity_counts[severity]}")

        for issue_type, items in type_groups.items():
            print(f"\n[{issue_type.upper().replace('_', ' ')}] - {len(items)} occurrence(s)")
            print("-" * 76)

            for item in items:
                print(f"  Severity: {item['severity']}")
                print(f"  Description: {item['description']}")
                print(f"  File: {item['file']}")
                print(f"  Line: {item['line']}")
                print(f"  Match: {item['match']}")
                print(f"  Context: {item['content']}")
                print()


def main():
    parser = argparse.ArgumentParser(
        description="Security Scanner - Scan files and directories for common security issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 security_scanner.py -f config.txt
  python3 security_scanner.py -d ./source-code
  python3 security_scanner.py --file secrets.env
        """
    )

    parser.add_argument("-f", "--file", help="Scan a single file", type=str)
    parser.add_argument("-d", "--directory", help="Scan all files in a directory", type=str)

    args = parser.parse_args()

    if not args.file and not args.directory:
        parser.print_help()
        sys.exit(1)

    scanner = SecurityScanner()

    if args.file:
        print(f"Scanning file: {args.file}")
        scanner.scan_file(args.file)

    if args.directory:
        print(f"Scanning directory: {args.directory}")
        scanner.scan_directory(args.directory)

    scanner.generate_report()


if __name__ == "__main__":
    main()
