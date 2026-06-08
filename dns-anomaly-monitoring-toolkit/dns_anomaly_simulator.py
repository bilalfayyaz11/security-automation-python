#!/usr/bin/env python3
"""
DNS Anomaly Simulator

Simulates common DNS anomalies including NXDOMAIN spikes,
fast-flux behavior, suspicious random domains, and IP-based domains.
"""

import json
import random
import string
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import dns.exception
import dns.resolver


class DNSAnomalySimulator:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 3
        self.resolver.lifetime = 3
        self.legitimate_domains = ["google.com", "github.com", "stackoverflow.com"]
        self.suspicious_domains = [
            "aksjdhfkjashdf.com",
            "google-login-verify.tk",
            "192.168.1.1.nip.io",
        ]

    def simulate_normal_query(self, domain: str) -> Dict:
        result = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "anomaly_type": "none",
            "status": "success",
            "ips": [],
            "response_time_ms": None,
        }

        try:
            start = time.perf_counter()
            answers = self.resolver.resolve(domain, "A")
            end = time.perf_counter()
            result["ips"] = [str(rdata) for rdata in answers]
            result["response_time_ms"] = round((end - start) * 1000, 2)
        except dns.exception.DNSException as error:
            result["status"] = "failed"
            result["error"] = str(error)

        return result

    def simulate_nxdomain(self) -> Dict:
        fake_domain = f"nonexistent{random.randint(1000, 9999)}.invalid"
        return {
            "domain": fake_domain,
            "timestamp": datetime.now().isoformat(),
            "anomaly_type": "NXDOMAIN",
            "status": "anomaly_detected",
            "description": "Domain does not exist",
        }

    def simulate_fast_flux(self, domain: str) -> List[Dict]:
        results = []

        for query_number in range(1, 4):
            result = {
                "domain": domain,
                "timestamp": datetime.now().isoformat(),
                "anomaly_type": "fast_flux",
                "query_number": query_number,
                "ips": [
                    f"192.0.2.{random.randint(1, 254)}"
                    for _ in range(random.randint(2, 5))
                ],
                "description": "Same domain returns rapidly changing IP sets",
            }
            results.append(result)
            time.sleep(0.2)

        return results

    def simulate_dga_domain(self) -> Dict:
        length = random.randint(15, 30)
        random_string = "".join(random.choices(string.ascii_lowercase, k=length))
        dga_domain = f"{random_string}.com"

        return {
            "domain": dga_domain,
            "timestamp": datetime.now().isoformat(),
            "anomaly_type": "DGA_pattern",
            "status": "suspicious",
            "entropy": "high",
            "description": "Domain resembles DGA output due to random-looking characters",
        }

    def simulate_ip_based_domain(self) -> Dict:
        return {
            "domain": "192.168.1.1.nip.io",
            "timestamp": datetime.now().isoformat(),
            "anomaly_type": "ip_encoded_domain",
            "status": "suspicious",
            "description": "Domain embeds an IP address pattern",
        }


def run_simulation() -> List[Dict]:
    simulator = DNSAnomalySimulator()
    events = []

    print("\n" + "=" * 70)
    print("DNS ANOMALY SIMULATOR")
    print("=" * 70 + "\n")

    print("[1] Normal DNS Queries")
    print("-" * 70)
    for domain in simulator.legitimate_domains[:2]:
        result = simulator.simulate_normal_query(domain)
        events.append(result)
        print(f"Domain: {result['domain']}")
        print(f"Status: {result['status']}")
        print(f"IPs: {', '.join(result.get('ips', []))}")
        print(f"Response Time: {result.get('response_time_ms')}ms\n")

    print("[2] NXDOMAIN Anomaly")
    print("-" * 70)
    nxdomain_result = simulator.simulate_nxdomain()
    events.append(nxdomain_result)
    print(f"Domain: {nxdomain_result['domain']}")
    print(f"Anomaly: {nxdomain_result['anomaly_type']}")
    print(f"Description: {nxdomain_result['description']}\n")

    print("[3] Fast Flux DNS Anomaly")
    print("-" * 70)
    flux_results = simulator.simulate_fast_flux("suspicious-site.com")
    events.extend(flux_results)
    for result in flux_results:
        print(f"Query {result['query_number']}: {len(result['ips'])} IPs -> {result['ips']}")

    print("\n[4] DGA Pattern")
    print("-" * 70)
    dga_result = simulator.simulate_dga_domain()
    events.append(dga_result)
    print(f"Domain: {dga_result['domain']}")
    print(f"Anomaly: {dga_result['anomaly_type']}")
    print(f"Description: {dga_result['description']}\n")

    print("[5] IP-Based Domain Pattern")
    print("-" * 70)
    ip_based = simulator.simulate_ip_based_domain()
    events.append(ip_based)
    print(f"Domain: {ip_based['domain']}")
    print(f"Anomaly: {ip_based['anomaly_type']}")
    print(f"Description: {ip_based['description']}")

    Path("dns_anomaly_events.json").write_text(json.dumps(events, indent=2), encoding="utf-8")

    print("\n" + "=" * 70)
    print("Simulation Complete")
    print("Events saved to dns_anomaly_events.json")
    print("=" * 70 + "\n")

    return events


if __name__ == "__main__":
    run_simulation()
