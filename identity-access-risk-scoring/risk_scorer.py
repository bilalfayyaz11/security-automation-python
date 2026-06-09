import json
import pandas as pd

class IAMRiskScorer:

    def __init__(self, data_file):

        with open(data_file, "r") as f:
            self.users = json.load(f)

        self.risk_scores = []

    def calculate_permission_risk(self, permissions):

        risk_score = 0

        high_risk = [
            "admin",
            "sudo",
            "config_change",
            "delete"
        ]

        medium_risk = [
            "deploy",
            "database_access"
        ]

        for perm in permissions:

            if perm in high_risk:
                risk_score += 10

            elif perm in medium_risk:
                risk_score += 5

            else:
                risk_score += 1

        return min(risk_score, 30)

    def calculate_behavior_risk(self, activity):

        risk_score = 0

        if activity["failed_logins"] > 10:
            risk_score += 15

        elif activity["failed_logins"] > 5:
            risk_score += 8

        if activity["off_hours_access"] > 20:
            risk_score += 12

        elif activity["off_hours_access"] > 10:
            risk_score += 6

        risk_score += (
            activity["privilege_escalation_attempts"] * 5
        )

        if activity["data_downloads"] > 40:
            risk_score += 8

        return min(risk_score, 40)

    def calculate_account_hygiene_risk(self, pwd_age):

        if pwd_age > 180:
            return 30

        elif pwd_age > 90:
            return 20

        elif pwd_age > 60:
            return 10

        return 5

    def score_all_users(self):

        for user in self.users:

            perm_risk = self.calculate_permission_risk(
                user["permissions"]
            )

            behavior_risk = self.calculate_behavior_risk(
                user["activity"]
            )

            hygiene_risk = self.calculate_account_hygiene_risk(
                user["last_password_change"]
            )

            total = (
                perm_risk +
                behavior_risk +
                hygiene_risk
            )

            if total >= 70:
                level = "CRITICAL"

            elif total >= 50:
                level = "HIGH"

            elif total >= 30:
                level = "MEDIUM"

            else:
                level = "LOW"

            self.risk_scores.append({
                "username": user["username"],
                "role": user["role"],
                "department": user["department"],
                "permission_risk": perm_risk,
                "behavior_risk": behavior_risk,
                "hygiene_risk": hygiene_risk,
                "total_risk_score": total,
                "risk_level": level
            })

    def generate_report(self):

        df = pd.DataFrame(self.risk_scores)

        df = df.sort_values(
            "total_risk_score",
            ascending=False
        )

        print("\n" + "=" * 80)
        print("IAM RISK ASSESSMENT REPORT")
        print("=" * 80)

        print(df.to_string(index=False))

        print("\n" + "=" * 80)

        print("\nRISK SUMMARY:")

        print(
            f"Total Users Analyzed: "
            f"{len(self.risk_scores)}"
        )

        print(
            f"Critical Risk: "
            f"{len(df[df['risk_level']=='CRITICAL'])}"
        )

        print(
            f"High Risk: "
            f"{len(df[df['risk_level']=='HIGH'])}"
        )

        print(
            f"Medium Risk: "
            f"{len(df[df['risk_level']=='MEDIUM'])}"
        )

        print(
            f"Low Risk: "
            f"{len(df[df['risk_level']=='LOW'])}"
        )

        print(
            f"Average Risk Score: "
            f"{df['total_risk_score'].mean():.2f}"
        )

        df.to_csv(
            "risk_report.csv",
            index=False
        )

        print(
            "\nDetailed report saved to: risk_report.csv"
        )

if __name__ == "__main__":

    scorer = IAMRiskScorer(
        "iam_data.json"
    )

    scorer.score_all_users()

    scorer.generate_report()
