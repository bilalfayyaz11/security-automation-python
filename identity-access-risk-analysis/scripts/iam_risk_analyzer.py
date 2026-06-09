#!/usr/bin/env python3
"""
IAM Risk Analysis Framework
Correlates user identities, permissions, behavior, and calculates risk scores.
"""

import json
from datetime import datetime


class IAMRiskAnalyzer:
    """Analyze identity, access, and behavior risk across users."""

    def __init__(self, users_file, permissions_file, behavior_file):
        self.users = self.load_json(users_file)["users"]
        self.permissions = self.load_json(permissions_file)["permissions"]
        self.activities = self.load_json(behavior_file)["activities"]

    def load_json(self, filepath):
        """Load JSON data from a file."""
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    def correlate_user_data(self, user_id):
        """Correlate identity, permission, and activity records for one user."""
        user_info = next((user for user in self.users if user["id"] == user_id), None)
        user_permissions = [perm for perm in self.permissions if perm["user_id"] == user_id]
        user_activities = [activity for activity in self.activities if activity["user_id"] == user_id]

        return {
            "identity": user_info,
            "permissions": user_permissions,
            "activities": user_activities,
        }

    def analyze_permission_risk(self, permissions):
        """Calculate risk score based on access level and privilege exposure."""
        risk_score = 0

        for permission in permissions:
            access_level = permission.get("access_level", "").lower()

            if access_level == "admin":
                risk_score += 30
            elif access_level == "write":
                risk_score += 15
            elif access_level == "read":
                risk_score += 5

        return min(risk_score, 100)

    def analyze_behavior_risk(self, activities):
        """Calculate risk score based on failed logins, after-hours activity, and sensitive actions."""
        risk_score = 0
        high_risk_actions = {"delete_records", "modify_config", "privilege_escalation"}

        for activity in activities:
            action = activity.get("action", "")
            success = activity.get("success", True)

            if action == "login" and success is False:
                risk_score += 20

            timestamp = activity.get("timestamp")
            if timestamp:
                try:
                    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour
                    if hour >= 22 or hour <= 6:
                        risk_score += 15
                except ValueError:
                    risk_score += 10

            if action in high_risk_actions:
                risk_score += 25

        return min(risk_score, 100)

    def calculate_composite_risk(self, user_id):
        """Calculate weighted composite risk for a user."""
        user_data = self.correlate_user_data(user_id)
        identity = user_data["identity"]

        permission_risk = self.analyze_permission_risk(user_data["permissions"])
        behavior_risk = self.analyze_behavior_risk(user_data["activities"])
        composite_risk = (permission_risk * 0.4) + (behavior_risk * 0.6)

        if composite_risk >= 70:
            risk_level = "HIGH"
        elif composite_risk >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "user_id": user_id,
            "user_name": identity["name"] if identity else "Unknown",
            "department": identity["department"] if identity else "Unknown",
            "permission_risk": round(permission_risk, 2),
            "behavior_risk": round(behavior_risk, 2),
            "composite_risk": round(composite_risk, 2),
            "risk_level": risk_level,
            "permission_count": len(user_data["permissions"]),
            "activity_count": len(user_data["activities"]),
        }

    def analyze_all_users(self):
        """Analyze every user and rank by highest composite risk."""
        results = []

        for user in self.users:
            results.append(self.calculate_composite_risk(user["id"]))

        results.sort(key=lambda result: result["composite_risk"], reverse=True)
        return results

    def generate_report(self, output_file):
        """Generate a text report with summary and user-level risk details."""
        results = self.analyze_all_users()

        high_risk = sum(1 for result in results if result["risk_level"] == "HIGH")
        medium_risk = sum(1 for result in results if result["risk_level"] == "MEDIUM")
        low_risk = sum(1 for result in results if result["risk_level"] == "LOW")

        report = [
            "=" * 80,
            "IAM RISK ANALYSIS REPORT",
            "=" * 80,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Users Analyzed: {len(results)}",
            "=" * 80,
            "",
            "RISK SUMMARY:",
            f"  High Risk Users: {high_risk}",
            f"  Medium Risk Users: {medium_risk}",
            f"  Low Risk Users: {low_risk}",
            "",
            "=" * 80,
            "DETAILED USER RISK ANALYSIS:",
            "=" * 80,
        ]

        for result in results:
            report.extend(
                [
                    "",
                    f"User: {result['user_name']} ({result['user_id']})",
                    f"Department: {result['department']}",
                    f"Risk Level: {result['risk_level']}",
                    f"Composite Risk Score: {result['composite_risk']}/100",
                    f"  - Permission Risk: {result['permission_risk']}/100",
                    f"  - Behavior Risk: {result['behavior_risk']}/100",
                    f"Permissions: {result['permission_count']}",
                    f"Activities Logged: {result['activity_count']}",
                    "-" * 80,
                ]
            )

        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(report))

        print(f"Report generated: {output_file}")
        return results


def main():
    """Run IAM risk analysis."""
    print("Starting IAM Risk Analysis...")

    analyzer = IAMRiskAnalyzer(
        "data/users.json",
        "data/permissions.json",
        "data/behavior_logs.json",
    )

    results = analyzer.generate_report("reports/iam_risk_report.txt")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    for result in results:
        print(
            f"{result['user_name']:20} | "
            f"Risk: {result['risk_level']:6} | "
            f"Score: {result['composite_risk']:5.1f}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
