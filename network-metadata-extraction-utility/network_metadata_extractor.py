#!/usr/bin/env python3
"""
Network Metadata Extraction Utility

Parses network traffic logs, extracts connection metadata, enriches records
with service identification, classifies internal/external IPs, and exports
structured JSON for investigation workflows.
"""

import argparse
import ipaddress
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class NetworkMetadataExtractor:
    def __init__(self):
        self.connections: List[Dict] = []
        self.stats = defaultdict(int)
        self.parse_errors: List[Dict] = []

        self.port_services = {
            20: "FTP-DATA",
            21: "FTP",
            22: "SSH",
            23: "TELNET",
            25: "SMTP",
            53: "DNS",
            67: "DHCP",
            68: "DHCP",
            80: "HTTP",
            110: "POP3",
            123: "NTP",
            143: "IMAP",
            161: "SNMP",
            389: "LDAP",
            443: "HTTPS",
            445: "SMB",
            993: "IMAPS",
            995: "POP3S",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5353: "mDNS",
            8080: "HTTP-Proxy",
            8443: "HTTPS-Alt",
        }

    def parse_log_line(self, line: str) -> Optional[Dict]:
        pattern = (
            r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
            r"(?P<protocol>TCP|UDP|ICMP)\s+"
            r"(?P<src_ip>(?:\d{1,3}\.){3}\d{1,3}):(?P<src_port>\d+)\s+"
            r"->\s+"
            r"(?P<dst_ip>(?:\d{1,3}\.){3}\d{1,3}):(?P<dst_port>\d+)"
        )

        match = re.search(pattern, line.strip(), re.IGNORECASE)
        if not match:
            return None

        metadata = match.groupdict()
        metadata["protocol"] = metadata["protocol"].upper()
        metadata["src_port"] = int(metadata["src_port"])
        metadata["dst_port"] = int(metadata["dst_port"])

        try:
            ipaddress.ip_address(metadata["src_ip"])
            ipaddress.ip_address(metadata["dst_ip"])
        except ValueError:
            return None

        return metadata

    def classify_ip(self, ip: str) -> str:
        address = ipaddress.ip_address(ip)

        if address.is_private:
            return "Internal"

        if address.is_loopback:
            return "Loopback"

        if address.is_multicast:
            return "Multicast"

        if address.is_reserved:
            return "Reserved"

        return "External"

    def enrich_metadata(self, metadata: Dict) -> Dict:
        src_ip = metadata["src_ip"]
        dst_ip = metadata["dst_ip"]
        dst_port = metadata["dst_port"]

        enriched = dict(metadata)
        enriched["service"] = self.port_services.get(dst_port, f"Unknown-{dst_port}")
        enriched["src_type"] = self.classify_ip(src_ip)
        enriched["dst_type"] = self.classify_ip(dst_ip)
        enriched["direction"] = self.classify_direction(enriched["src_type"], enriched["dst_type"])
        enriched["is_privileged_dst_port"] = dst_port < 1024
        enriched["generated_at"] = datetime.now().isoformat()

        return enriched

    def classify_direction(self, src_type: str, dst_type: str) -> str:
        if src_type == "Internal" and dst_type == "External":
            return "Outbound"
        if src_type == "External" and dst_type == "Internal":
            return "Inbound"
        if src_type == "Internal" and dst_type == "Internal":
            return "Internal"
        return "Other"

    def process_log_file(self, filename: str) -> None:
        path = Path(filename)

        print(f"[*] Processing log file: {path}")

        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                if not line.strip():
                    continue

                metadata = self.parse_log_line(line)

                if metadata is None:
                    self.parse_errors.append({
                        "line_number": line_num,
                        "line": line.strip(),
                    })
                    continue

                enriched = self.enrich_metadata(metadata)
                self.connections.append(enriched)

                self.stats["total_connections"] += 1
                self.stats[f"protocol_{enriched['protocol']}"] += 1
                self.stats[f"service_{enriched['service']}"] += 1
                self.stats[f"direction_{enriched['direction']}"] += 1
                self.stats[f"dst_type_{enriched['dst_type']}"] += 1

        print(f"[+] Processed {self.stats['total_connections']} connections")
        print(f"[+] Parse errors: {len(self.parse_errors)}")

    def generate_report(self) -> None:
        print("\n" + "=" * 70)
        print("NETWORK METADATA EXTRACTION REPORT")
        print("=" * 70)

        print(f"\n[*] Total Connections: {self.stats['total_connections']}")
        print(f"[*] Parse Errors: {len(self.parse_errors)}")

        print("\n[*] Protocol Distribution:")
        for key, value in sorted(self.stats.items()):
            if key.startswith("protocol_"):
                print(f"    {key.replace('protocol_', '')}: {value}")

        print("\n[*] Top Services:")
        services = [
            (key.replace("service_", ""), value)
            for key, value in self.stats.items()
            if key.startswith("service_")
        ]
        services.sort(key=lambda item: item[1], reverse=True)

        for service, count in services[:10]:
            print(f"    {service}: {count}")

        unique_src_ips = sorted({conn["src_ip"] for conn in self.connections})
        unique_dst_ips = sorted({conn["dst_ip"] for conn in self.connections})

        print(f"\n[*] Unique Source IPs: {len(unique_src_ips)}")
        print(f"[*] Unique Destination IPs: {len(unique_dst_ips)}")

        print("\n[*] Traffic Direction:")
        for key, value in sorted(self.stats.items()):
            if key.startswith("direction_"):
                print(f"    {key.replace('direction_', '')}: {value}")

        print("\n[*] Destination Classification:")
        for key, value in sorted(self.stats.items()):
            if key.startswith("dst_type_"):
                print(f"    {key.replace('dst_type_', '')}: {value}")

        print("\n[*] Top Destination IPs:")
        for ip, count in Counter(conn["dst_ip"] for conn in self.connections).most_common(10):
            print(f"    {ip}: {count}")

    def export_json(self, output_file: str) -> None:
        output = {
            "generated_at": datetime.now().isoformat(),
            "metadata": self.connections,
            "statistics": dict(self.stats),
            "parse_errors": self.parse_errors,
        }

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=2)

        print(f"\n[+] Exported metadata to: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Network metadata extraction utility")
    parser.add_argument("--input", default="network_traffic.log", help="Input network log file")
    parser.add_argument("--output", default="network_metadata.json", help="Output JSON file")

    args = parser.parse_args()

    print("Network Metadata Extraction Utility")
    print("-" * 70)

    extractor = NetworkMetadataExtractor()
    extractor.process_log_file(args.input)
    extractor.generate_report()
    extractor.export_json(args.output)

    print("\n[+] Analysis complete!")


if __name__ == "__main__":
    main()
