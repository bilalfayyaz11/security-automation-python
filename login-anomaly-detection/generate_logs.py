#!/usr/bin/env python3
import random
from datetime import datetime, timedelta

users = ['alice', 'bob', 'charlie', 'admin']
ips = ['192.168.1.10', '192.168.1.20', '10.0.0.5', '203.0.113.45', '198.51.100.78']
locations = ['NewYork', 'LosAngeles', 'Chicago', 'Houston', 'Phoenix']

logs = []
start_date = datetime.now() - timedelta(days=7)

for day in range(7):
    for user in users[:3]:
        for _ in range(random.randint(2, 5)):
            hour = random.randint(8, 18)
            timestamp = start_date + timedelta(days=day, hours=hour, minutes=random.randint(0, 59))
            ip = random.choice(ips[:3])
            location = random.choice(locations[:2])
            logs.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},{user},{ip},{location},success")

timestamp = datetime.now() - timedelta(days=1, hours=2)
logs.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},alice,192.168.1.10,NewYork,success")

timestamp = datetime.now() - timedelta(hours=5)
logs.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},bob,203.0.113.45,Tokyo,success")

for i in range(15):
    timestamp = datetime.now() - timedelta(minutes=30-i)
    logs.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},admin,198.51.100.78,Unknown,failed")

with open('auth_logs.csv', 'w') as f:
    f.write("timestamp,username,ip_address,location,status\n")
    for log in sorted(logs):
        f.write(log + "\n")

print("Generated auth_logs.csv with sample data")
