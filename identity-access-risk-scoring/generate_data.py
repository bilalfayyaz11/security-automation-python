import json
import random

def generate_user_data():

    users = []

    user_profiles = [
        {"username": "alice", "role": "admin", "department": "IT"},
        {"username": "bob", "role": "developer", "department": "Engineering"},
        {"username": "charlie", "role": "analyst", "department": "Finance"},
        {"username": "david", "role": "user", "department": "HR"},
        {"username": "eve", "role": "contractor", "department": "External"}
    ]

    for profile in user_profiles:

        user_data = {
            "username": profile["username"],
            "role": profile["role"],
            "department": profile["department"],
            "permissions": generate_permissions(profile["role"]),
            "activity": generate_activity(profile["username"]),
            "last_password_change": random.randint(1, 365)
        }

        users.append(user_data)

    return users

def generate_permissions(role):

    base_permissions = ["read", "write"]

    if role == "admin":
        return base_permissions + ["delete", "admin", "sudo", "config_change"]

    elif role == "developer":
        return base_permissions + ["deploy", "database_access"]

    elif role == "analyst":
        return base_permissions + ["report_access"]

    else:
        return ["read"]

def generate_activity(username):

    if username == "eve":

        login_count = random.randint(50, 100)
        failed_logins = random.randint(15, 30)
        off_hours_access = random.randint(20, 40)

    elif username == "alice":

        login_count = random.randint(30, 50)
        failed_logins = random.randint(0, 2)
        off_hours_access = random.randint(5, 15)

    else:

        login_count = random.randint(20, 40)
        failed_logins = random.randint(0, 5)
        off_hours_access = random.randint(0, 5)

    return {
        "login_count": login_count,
        "failed_logins": failed_logins,
        "off_hours_access": off_hours_access,
        "data_downloads": random.randint(0, 50),
        "privilege_escalation_attempts": random.randint(0, 3)
    }

users = generate_user_data()

with open("iam_data.json", "w") as f:
    json.dump(users, f, indent=2)

print("Sample IAM data generated successfully!")
print(f"Created data for {len(users)} users")
