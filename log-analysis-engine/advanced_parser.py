#!/usr/bin/env python3
"""
Advanced Log Parser with Statistics and CSV Export
"""

import csv
from collections import Counter
from typing import Dict, List

from log_parser import parse_log_file


def generate_statistics(parsed_logs: List[Dict[str, str]]) -> Dict:
    level_counter = Counter(log["level"] for log in parsed_logs)
    ip_counter = Counter(log["ip_address"] for log in parsed_logs)

    return {
        "total_entries": len(parsed_logs),
        "level_counts": level_counter,
        "unique_ips": len(ip_counter),
        "top_ips": ip_counter.most_common(3)
    }


def extract_ip_addresses(parsed_logs: List[Dict[str, str]]) -> List[str]:
    return [log["ip_address"] for log in parsed_logs]


def search_logs(parsed_logs: List[Dict[str, str]], keyword: str) -> List[Dict[str, str]]:
    keyword = keyword.lower()
    return [log for log in parsed_logs if keyword in log["message"].lower()]


def export_to_csv(parsed_logs: List[Dict[str, str]], output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["timestamp", "ip_address", "level", "message"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(parsed_logs)


def main():
    print("=== Advanced Log Parser ===\n")

    parsed_logs = parse_log_file("sample.log")
    stats = generate_statistics(parsed_logs)

    print("Statistics:")
    print(f"Total entries: {stats['total_entries']}")
    print(f"Level counts: {dict(stats['level_counts'])}")
    print(f"Unique IPs: {stats['unique_ips']}")
    print(f"Top IPs: {stats['top_ips']}")

    print("\nSearch results for keyword: login")
    for entry in search_logs(parsed_logs, "login"):
        print(entry)

    print("\nAll extracted IP addresses:")
    for ip in extract_ip_addresses(parsed_logs):
        print(ip)

    export_to_csv(parsed_logs, "output.csv")
    print("\nExported parsed logs to output.csv")
    print("\nProcessing complete!")


if __name__ == "__main__":
    main()
