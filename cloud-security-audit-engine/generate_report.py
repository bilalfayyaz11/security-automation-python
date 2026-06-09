#!/usr/bin/env python3

import json
from datetime import datetime

def load_audit_results():
    results = {}

    try:
        with open("reports/config_audit.json", "r") as f:
            results["config"] = json.load(f)
    except FileNotFoundError:
        results["config"] = []

    try:
        with open("reports/log_audit.json", "r") as f:
            results["log"] = json.load(f)
    except FileNotFoundError:
        results["log"] = []

    return results

def calculate_compliance_score(findings):
    weights = {"CRITICAL": 10, "HIGH": 5, "MEDIUM": 2, "LOW": 1}
    penalty = 0
    total_issues = 0

    for category in findings.values():
        for finding in category:
            penalty += weights.get(finding.get("severity", "LOW"), 1)
            total_issues += 1

    return max(0, 100 - penalty), total_issues

def generate_html_report(results, score, total_issues):
    rows = ""

    for finding in results["config"]:
        rows += f"<tr><td>{finding['severity']}</td><td>{finding['issue']}</td><td>{finding['recommendation']}</td></tr>"

    for finding in results["log"]:
        rows += f"<tr><td>{finding['severity']}</td><td>{finding['type']}</td><td>{finding['details']}</td></tr>"

    return f"""
<!DOCTYPE html>
<html>
<head><title>Security Compliance Report</title></head>
<body>
<h1>Security Compliance Audit Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<h2>Compliance Score: {score}/100</h2>
<p>Total Issues Found: {total_issues}</p>
<table border="1">
<tr><th>Severity</th><th>Finding</th><th>Details</th></tr>
{rows}
</table>
</body>
</html>
"""

def main():
    results = load_audit_results()
    score, total_issues = calculate_compliance_score(results)
    html = generate_html_report(results, score, total_issues)

    with open("reports/compliance_report.html", "w") as f:
        f.write(html)

    print(f"Compliance Score: {score}/100")
    print(f"Total Issues: {total_issues}")

if __name__ == "__main__":
    main()
