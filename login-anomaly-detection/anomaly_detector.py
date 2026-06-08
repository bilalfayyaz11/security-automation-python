#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
from collections import defaultdict

class LoginAnomalyDetector:

    def __init__(self, log_file):
        self.log_file = log_file
        self.df = None
        self.user_profiles = {}

    def load_logs(self):
        self.df = pd.read_csv(self.log_file)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['hour'] = self.df['timestamp'].dt.hour

        print(f"Loaded {len(self.df)} login records")
        print("\nSample data:")
        print(self.df.head())

    def build_user_profiles(self):
        successful = self.df[self.df['status'] == 'success']

        for username in successful['username'].unique():
            user_data = successful[successful['username'] == username]

            typical_hours = user_data['hour'].tolist()

            typical_locations = (
                user_data['location']
                .value_counts()
                .head(2)
                .index
                .tolist()
            )

            self.user_profiles[username] = {
                'typical_hours': typical_hours,
                'typical_locations': typical_locations,
                'login_count': len(user_data)
            }

        print(f"\nBuilt profiles for {len(self.user_profiles)} users")

    def detect_time_anomalies(self):
        business_start = 8
        business_end = 18

        anomalies = self.df[
            (self.df['hour'] < business_start) |
            (self.df['hour'] > business_end)
        ]

        return anomalies

    def detect_location_anomalies(self):
        anomalies = []

        for _, row in self.df.iterrows():
            username = row['username']
            location = row['location']

            if username in self.user_profiles:
                typical_locs = self.user_profiles[username]['typical_locations']

                if location not in typical_locs:
                    anomalies.append(row)

        return pd.DataFrame(anomalies) if anomalies else pd.DataFrame()

    def detect_frequency_anomalies(self, time_window=30, threshold=10):
        df_sorted = self.df.sort_values('timestamp')
        suspicious_users = defaultdict(int)

        for username in df_sorted['username'].unique():
            user_logs = df_sorted[df_sorted['username'] == username]

            user_logs = user_logs[user_logs['status'] == 'failed']

            recent = user_logs[
                user_logs['timestamp'] >= (
                    datetime.now() - pd.Timedelta(minutes=time_window)
                )
            ]

            if len(recent) >= threshold:
                suspicious_users[username] = len(recent)

        return suspicious_users

    def generate_report(self):
        print("\n" + "=" * 60)
        print("LOGIN ANOMALY DETECTION REPORT")
        print("=" * 60)

        self.build_user_profiles()

        print("\n[1] TIME-BASED ANOMALIES (Outside Business Hours)")
        print("-" * 60)
        time_anomalies = self.detect_time_anomalies()

        if len(time_anomalies) > 0:
            print(f"Found {len(time_anomalies)} suspicious login(s):")
            for _, row in time_anomalies.iterrows():
                print(f"  - {row['username']} at {row['timestamp']} from {row['location']}")
        else:
            print("No time-based anomalies detected.")

        print("\n[2] LOCATION-BASED ANOMALIES (Unusual Locations)")
        print("-" * 60)
        location_anomalies = self.detect_location_anomalies()

        if len(location_anomalies) > 0:
            print(f"Found {len(location_anomalies)} suspicious login(s):")
            for _, row in location_anomalies.iterrows():
                print(f"  - {row['username']} from {row['location']} (IP: {row['ip_address']})")
        else:
            print("No location-based anomalies detected.")

        print("\n[3] FREQUENCY-BASED ANOMALIES (Potential Brute Force)")
        print("-" * 60)
        freq_anomalies = self.detect_frequency_anomalies()

        if freq_anomalies:
            print(f"Found {len(freq_anomalies)} suspicious user(s):")
            for user, count in freq_anomalies.items():
                print(f"  - {user}: {count} failed attempts in last 30 minutes")
        else:
            print("No frequency-based anomalies detected.")

        print("\n" + "=" * 60)

if __name__ == "__main__":
    detector = LoginAnomalyDetector('auth_logs.csv')
    detector.load_logs()
    detector.generate_report()
