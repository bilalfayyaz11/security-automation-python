#!/usr/bin/env python3
"""
Structured Log Parser Utility
"""

import re
from datetime import datetime
from typing import Dict, List, Optional


def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    pattern = r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\S+)\s+(INFO|WARNING|ERROR|DEBUG|CRITICAL)\s+(.+)$'
    match = re.match(pattern, line.strip())

    if not match:
        return None

    timestamp = f"{match.group(1)} {match.group(2)}"
    ip_address = match.group(3)

    if not validate_ip_address(ip_address):
        return None

    return {
        "timestamp": timestamp,
        "ip_address": ip_address,
        "level": match.group(4),
        "message": match.group(5)
    }


def tokenize_message(message: str) -> List[str]:
    return [token for token in message.split() if token]


def extract_timestamp_components(timestamp_str: str) -> Dict[str, int]:
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return {
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hour": dt.hour,
        "minute": dt.minute,
        "second": dt.second
    }


def validate_ip_address(ip: str) -> bool:
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    if not re.match(pattern, ip):
        return False

    return all(0 <= int(part) <= 255 for part in ip.split("."))


def parse_log_file(filename: str) -> List[Dict[str, str]]:
    parsed_logs = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parsed_entry = parse_log_line(line)
            if parsed_entry:
                parsed_logs.append(parsed_entry)

    return parsed_logs


def filter_by_level(parsed_logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    return [log for log in parsed_logs if log["level"] == level.upper()]


def main():
    print("=== Log Parser Utility ===\n")

    parsed_logs = parse_log_file("sample.log")

    print(f"Total entries parsed: {len(parsed_logs)}\n")

    print("First 3 parsed entries:")
    for entry in parsed_logs[:3]:
        print(entry)

    print("\nERROR level entries:")
    for entry in filter_by_level(parsed_logs, "ERROR"):
        print(entry)

    print("\nTokenized messages:")
    for entry in parsed_logs:
        tokens = tokenize_message(entry["message"])
        print(f"{entry['level']} | {entry['ip_address']} | {tokens}")

    print("\nTimestamp components from first entry:")
    if parsed_logs:
        print(extract_timestamp_components(parsed_logs[0]["timestamp"]))


if __name__ == "__main__":
    main()
