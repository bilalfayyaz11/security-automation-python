import json
import statistics

class AnomalyDetector:

    def __init__(self, data_file):

        with open(data_file, "r") as f:
            self.users = json.load(f)

    def detect_anomalies(self):

        login_counts = [
            u["activity"]["login_count"]
            for u in self.users
        ]

        failed_logins = [
            u["activity"]["failed_logins"]
            for u in self.users
        ]

        off_hours = [
            u["activity"]["off_hours_access"]
            for u in self.users
        ]

        login_mean = statistics.mean(login_counts)
        login_std = statistics.stdev(login_counts)

        failed_mean = statistics.mean(failed_logins)
        failed_std = statistics.stdev(failed_logins)

        off_mean = statistics.mean(off_hours)
        off_std = statistics.stdev(off_hours)

        print("\n" + "=" * 80)
        print("ANOMALY DETECTION REPORT")
        print("=" * 80)

        found = False

        for user in self.users:

            anomalies = []

            activity = user["activity"]

            if activity["login_count"] > (
                login_mean + (2 * login_std)
            ):
                anomalies.append(
                    f"Excessive logins: {activity['login_count']}"
                )

            if activity["failed_logins"] > (
                failed_mean + (2 * failed_std)
            ):
                anomalies.append(
                    f"High failed logins: {activity['failed_logins']}"
                )

            if activity["off_hours_access"] > (
                off_mean + (2 * off_std)
            ):
                anomalies.append(
                    f"Unusual off-hours access: {activity['off_hours_access']}"
                )

            if (
                activity["privilege_escalation_attempts"] > 0
            ):
                anomalies.append(
                    f"Privilege escalation attempts: {activity['privilege_escalation_attempts']}"
                )

            if anomalies:

                found = True

                print(
                    f"\nUSER: {user['username']} "
                    f"({user['role']})"
                )

                print(
                    f"Department: {user['department']}"
                )

                print(
                    "Anomalies detected:"
                )

                for anomaly in anomalies:
                    print(
                        f"  - {anomaly}"
                    )

        if not found:
            print(
                "\nNo significant anomalies detected."
            )

        print("\n" + "=" * 80)

if __name__ == "__main__":

    detector = AnomalyDetector(
        "iam_data.json"
    )

    detector.detect_anomalies()
