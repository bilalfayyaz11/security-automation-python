#!/usr/bin/env python3
"""
HTTP Header Security Analyzer

Extracts HTTP response headers, detects missing security headers,
identifies insecure configurations, and generates a clear security report.
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Tuple

import requests
from colorama import Fore, Style, init


init(autoreset=True)


SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "description": "Enforces HTTPS connections",
        "severity": "HIGH",
    },
    "Content-Security-Policy": {
        "description": "Controls resource loading and reduces XSS impact",
        "severity": "HIGH",
    },
    "X-Frame-Options": {
        "description": "Prevents clickjacking attacks",
        "severity": "MEDIUM",
    },
    "X-Content-Type-Options": {
        "description": "Prevents MIME-type sniffing",
        "severity": "MEDIUM",
    },
    "Referrer-Policy": {
        "description": "Controls referrer information leakage",
        "severity": "MEDIUM",
    },
    "Permissions-Policy": {
        "description": "Controls browser feature permissions",
        "severity": "MEDIUM",
    },
    "Cross-Origin-Opener-Policy": {
        "description": "Isolates browsing context groups",
        "severity": "LOW",
    },
    "Cross-Origin-Resource-Policy": {
        "description": "Restricts cross-origin resource loading",
        "severity": "LOW",
    },
}


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url


def fetch_headers(url: str, timeout: int = 10, verify_tls: bool = True) -> Tuple[Dict[str, str], int, str]:
    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            verify=verify_tls,
            headers={
                "User-Agent": "header-security-analyzer/1.0"
            },
        )
        return dict(response.headers), response.status_code, response.url

    except requests.exceptions.SSLError as error:
        print(f"{Fore.RED}TLS certificate validation failed: {error}")
        return {}, 0, url

    except requests.exceptions.Timeout:
        print(f"{Fore.RED}Error fetching URL: request timed out after {timeout} seconds")
        return {}, 0, url

    except requests.exceptions.RequestException as error:
        print(f"{Fore.RED}Error fetching URL: {error}")
        return {}, 0, url


def display_headers(headers: Dict[str, str]) -> None:
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.CYAN}HTTP HEADERS FOUND")
    print(f"{Fore.CYAN}{'=' * 70}\n")

    if not headers:
        print(f"{Fore.RED}No headers returned.")
        return

    for header_name, header_value in sorted(headers.items()):
        print(f"{Fore.WHITE}{header_name}: {Style.RESET_ALL}{header_value}")


def header_lookup(headers: Dict[str, str], expected_name: str):
    lower_map = {name.lower(): value for name, value in headers.items()}
    return lower_map.get(expected_name.lower())


def analyze_hsts(value: str) -> List[str]:
    issues = []
    match = re.search(r"max-age\s*=\s*(\d+)", value, re.IGNORECASE)

    if not match:
        issues.append("Strict-Transport-Security: missing max-age directive")
        return issues

    max_age = int(match.group(1))

    if max_age < 15552000:
        issues.append(
            f"Strict-Transport-Security: max-age is too low ({max_age}); recommended minimum is 15552000 seconds"
        )

    if "includesubdomains" not in value.replace("-", "").lower():
        issues.append("Strict-Transport-Security: includeSubDomains is missing")

    return issues


def analyze_security_headers(headers: Dict[str, str]) -> Tuple[List[Dict[str, str]], List[str], List[Dict[str, str]]]:
    missing = []
    insecure = []
    present = []

    for header_name, metadata in SECURITY_HEADERS.items():
        value = header_lookup(headers, header_name)

        if value is None:
            missing.append({
                "header": header_name,
                "description": metadata["description"],
                "severity": metadata["severity"],
            })
        else:
            present.append({
                "header": header_name,
                "value": value,
                "severity": metadata["severity"],
            })

    x_frame = header_lookup(headers, "X-Frame-Options")
    if x_frame and x_frame.upper().startswith("ALLOW"):
        insecure.append(f"X-Frame-Options: insecure value '{x_frame}'")

    x_content = header_lookup(headers, "X-Content-Type-Options")
    if x_content and x_content.lower() != "nosniff":
        insecure.append(f"X-Content-Type-Options: expected 'nosniff', found '{x_content}'")

    x_xss = header_lookup(headers, "X-XSS-Protection")
    if x_xss and x_xss.strip().startswith("0"):
        insecure.append("X-XSS-Protection: disabled with value 0")

    hsts = header_lookup(headers, "Strict-Transport-Security")
    if hsts:
        insecure.extend(analyze_hsts(hsts))

    csp = header_lookup(headers, "Content-Security-Policy")
    if csp:
        lowered_csp = csp.lower()
        if "unsafe-inline" in lowered_csp:
            insecure.append("Content-Security-Policy: contains unsafe-inline")
        if "unsafe-eval" in lowered_csp:
            insecure.append("Content-Security-Policy: contains unsafe-eval")
        if "default-src" not in lowered_csp:
            insecure.append("Content-Security-Policy: missing default-src directive")

    return missing, insecure, present


def calculate_score(missing: List[Dict[str, str]], insecure: List[str]) -> int:
    score = 100

    severity_penalties = {
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5,
    }

    for item in missing:
        score -= severity_penalties.get(item["severity"], 5)

    score -= len(insecure) * 8

    return max(score, 0)


def display_security_report(missing: List[Dict[str, str]], insecure: List[str], present: List[Dict[str, str]]) -> None:
    score = calculate_score(missing, insecure)

    print(f"\n{Fore.YELLOW}{'=' * 70}")
    print(f"{Fore.YELLOW}SECURITY ANALYSIS REPORT")
    print(f"{Fore.YELLOW}{'=' * 70}\n")

    print(f"{Fore.CYAN}Security Score: {score}/100\n")

    if present:
        print(f"{Fore.GREEN}Present Security Headers ({len(present)}):")
        for item in present:
            print(f"  - {item['header']} [{item['severity']}]")
    else:
        print(f"{Fore.RED}No recognized security headers found.")

    if missing:
        print(f"\n{Fore.RED}Missing Security Headers ({len(missing)}):")
        for item in missing:
            print(f"  - {item['header']} [{item['severity']}]: {item['description']}")
    else:
        print(f"\n{Fore.GREEN}All tracked security headers are present!")

    if insecure:
        print(f"\n{Fore.RED}Insecure Configurations Found ({len(insecure)}):")
        for issue in insecure:
            print(f"  - {issue}")
    else:
        print(f"\n{Fore.GREEN}No insecure configurations detected!")


def write_json_report(path: str, url: str, final_url: str, status_code: int, headers: Dict[str, str], missing, insecure, present) -> None:
    report = {
        "requested_url": url,
        "final_url": final_url,
        "status_code": status_code,
        "security_score": calculate_score(missing, insecure),
        "present_security_headers": present,
        "missing_security_headers": missing,
        "insecure_configurations": insecure,
        "headers": headers,
    }

    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"\n{Fore.GREEN}JSON report written to: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="HTTP header security analyzer")
    parser.add_argument("url", help="Target URL or domain to analyze")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--json-output", help="Write machine-readable JSON report to file")
    parser.add_argument("--insecure-skip-tls-verify", action="store_true", help="Disable TLS verification for testing only")

    args = parser.parse_args()

    url = normalize_url(args.url)

    print(f"{Fore.CYAN}Analyzing: {url}\n")

    headers, status_code, final_url = fetch_headers(
        url,
        timeout=args.timeout,
        verify_tls=not args.insecure_skip_tls_verify,
    )

    if not headers:
        print(f"{Fore.RED}No headers could be analyzed.")
        return 1

    print(f"{Fore.CYAN}HTTP Status Code: {status_code}")
    print(f"{Fore.CYAN}Final URL: {final_url}")

    display_headers(headers)

    missing, insecure, present = analyze_security_headers(headers)
    display_security_report(missing, insecure, present)

    if args.json_output:
        write_json_report(args.json_output, url, final_url, status_code, headers, missing, insecure, present)

    return 0


if __name__ == "__main__":
    sys.exit(main())
