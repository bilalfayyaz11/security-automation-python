#!/usr/bin/env python3
"""
DNS Resolution Utility

Performs DNS lookups for multiple record types and reports resolution status,
response time, and resolver metadata.
"""

import argparse
import time
from datetime import datetime
from typing import Dict, List, Optional

import dns.exception
import dns.resolver


def resolve_domain(domain: str, record_type: str = "A", timeout: float = 3.0) -> Dict:
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout

    result = {
        "domain": domain,
        "record_type": record_type,
        "timestamp": datetime.now().isoformat(),
        "status": "unknown",
        "records": [],
        "response_time_ms": None,
        "error": None,
    }

    try:
        start = time.perf_counter()
        answers = resolver.resolve(domain, record_type)
        end = time.perf_counter()

        result["records"] = [str(rdata) for rdata in answers]
        result["response_time_ms"] = round((end - start) * 1000, 2)
        result["status"] = "success"

    except dns.resolver.NXDOMAIN:
        result["status"] = "nxdomain"
        result["error"] = "Domain does not exist"

    except dns.resolver.NoAnswer:
        result["status"] = "no_answer"
        result["error"] = f"No {record_type} record returned"

    except dns.exception.Timeout:
        result["status"] = "timeout"
        result["error"] = "DNS query timed out"

    except dns.exception.DNSException as error:
        result["status"] = "dns_error"
        result["error"] = str(error)

    return result


def display_result(result: Dict) -> None:
    print(f"Domain: {result['domain']}")
    print(f"Record Type: {result['record_type']}")
    print(f"Status: {result['status']}")
    print(f"Response Time: {result['response_time_ms']}ms")

    if result["records"]:
        for record in result["records"]:
            print(f"  -> {record}")

    if result["error"]:
        print(f"Error: {result['error']}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="DNS resolution utility")
    parser.add_argument("domains", nargs="*", default=["google.com", "github.com", "localhost"])
    parser.add_argument("--record-type", default="A")
    parser.add_argument("--timeout", type=float, default=3.0)

    args = parser.parse_args()

    print(f"\n{'=' * 70}")
    print(f"DNS Resolution Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 70}\n")

    for domain in args.domains:
        display_result(resolve_domain(domain, args.record_type, args.timeout))


if __name__ == "__main__":
    main()
