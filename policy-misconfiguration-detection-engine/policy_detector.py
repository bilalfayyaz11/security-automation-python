#!/usr/bin/env python3

import json
from collections import Counter

class PolicyDetector:

    def __init__(self):
        self.findings = []

    def load_policy(self, filename):

        try:
            with open(filename, 'r') as f:
                return json.load(f)

        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return None

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {filename}")
            return None

    def check_overly_permissive_source(self, rule):

        if (
            rule.get('source') == '0.0.0.0/0'
            and rule.get('action') == 'ALLOW'
        ):
            port = rule.get('port')

            return (
                f"CRITICAL: Rule {rule['rule_id']} "
                f"allows traffic from anywhere "
                f"to port {port}"
            )

        return None

    def check_conflicting_rules(self, rules):

        conflicts = []

        for i, rule1 in enumerate(rules):

            for rule2 in rules[i + 1:]:

                if (
                    rule1['source'] == rule2['source']
                    and rule1['destination'] == rule2['destination']
                    and rule1['port'] == rule2['port']
                    and rule1['protocol'] == rule2['protocol']
                ):

                    if rule1['action'] != rule2['action']:

                        conflicts.append(
                            f"CONFLICT: Rules "
                            f"{rule1['rule_id']} and "
                            f"{rule2['rule_id']} have "
                            f"conflicting actions for "
                            f"same traffic"
                        )

        return conflicts

    def check_wildcard_permissions(self, rule):

        if rule.get('user') == '*':

            return (
                f"HIGH: Rule {rule['rule_id']} "
                f"grants {rule['permission']} "
                f"to everyone"
            )

        return None

    def check_sensitive_resource_access(self, rule):

        sensitive_resources = [
            '/etc/passwd',
            '/etc/shadow',
            '/root',
            '/var/log/secure'
        ]

        resource = rule.get('resource')
        user = rule.get('user')

        if (
            resource in sensitive_resources
            and user not in ['admin', 'root']
        ):

            return (
                f"HIGH: Rule {rule['rule_id']} "
                f"allows {user} access to "
                f"sensitive resource {resource}"
            )

        return None

    def analyze_firewall_policy(self, policy_data):

        if not policy_data:
            return

        rules = policy_data.get(
            'firewall_rules',
            []
        )

        print(
            f"\nAnalyzing {len(rules)} "
            f"firewall rules..."
        )

        for rule in rules:

            finding = self.check_overly_permissive_source(
                rule
            )

            if finding:
                self.findings.append(finding)

        conflicts = self.check_conflicting_rules(
            rules
        )

        self.findings.extend(conflicts)

    def analyze_access_policy(self, policy_data):

        if not policy_data:
            return

        rules = policy_data.get(
            'access_rules',
            []
        )

        print(
            f"Analyzing {len(rules)} "
            f"access control rules..."
        )

        for rule in rules:

            finding = self.check_wildcard_permissions(
                rule
            )

            if finding:
                self.findings.append(finding)

            finding = self.check_sensitive_resource_access(
                rule
            )

            if finding:
                self.findings.append(finding)

    def generate_report(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "SECURITY FINDINGS REPORT"
        )

        print(
            "=" * 60
        )

        if not self.findings:

            print(
                "\nNo misconfigurations detected."
            )

            return

        print(
            f"\nTotal Issues Found: "
            f"{len(self.findings)}\n"
        )

        for i, finding in enumerate(
            self.findings,
            1
        ):
            print(f"{i}. {finding}")

        critical = sum(
            1 for f in self.findings
            if 'CRITICAL' in f
        )

        high = sum(
            1 for f in self.findings
            if 'HIGH' in f
        )

        conflicts = sum(
            1 for f in self.findings
            if 'CONFLICT' in f
        )

        print(
            "\n" + "-" * 60
        )

        print(
            f"Summary: "
            f"{critical} Critical, "
            f"{high} High, "
            f"{conflicts} Conflicts"
        )

        print(
            "=" * 60
        )

def main():

    print("=" * 60)

    print(
        "Policy Misconfiguration Detection Engine"
    )

    print("=" * 60)

    detector = PolicyDetector()

    fw_policy = detector.load_policy(
        'firewall_policy.json'
    )

    detector.analyze_firewall_policy(
        fw_policy
    )

    ac_policy = detector.load_policy(
        'access_policy.json'
    )

    detector.analyze_access_policy(
        ac_policy
    )

    detector.generate_report()

    print(
        "\nAnalysis complete!"
    )

if __name__ == "__main__":
    main()
