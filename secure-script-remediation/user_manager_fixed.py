#!/usr/bin/env python3

import sys
import hashlib
import subprocess

ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

def authenticate_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return username == "admin" and password_hash == ADMIN_PASSWORD_HASH

def list_users():
    try:
        result = subprocess.run(
            ["grep", "/bin/bash", "/etc/passwd"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(result.stdout)
    except subprocess.TimeoutExpired:
        print("Command timed out")
    except Exception as error:
        print(f"Error listing users: {error}")

def add_user(username):
    if not username.isalnum() or len(username) < 3 or len(username) > 20:
        print("Invalid username. Use 3-20 alphanumeric characters.")
        return

    try:
        with open("/tmp/users.txt", "a") as file:
            file.write(username + "\n")

        print(f"User '{username}' added successfully")

    except IOError as error:
        print(f"Error writing file: {error}")

def read_users():
    try:
        with open("/tmp/users.txt", "r") as file:
            content = file.read()

        return content if content else "No users found"

    except FileNotFoundError:
        return "User file not found. Add users first."

    except IOError as error:
        return f"Error reading file: {error}"

def main():
    print("User Management System (Secure Version)")
    print("1. Authenticate")
    print("2. List system users")
    print("3. Add user")
    print("4. Read users")
    print("5. Exit")

    choice = input("Enter choice (1-5): ").strip()

    if not choice.isdigit() or int(choice) not in range(1,6):
        print("Invalid choice")
        return

    choice = int(choice)

    if choice == 1:
        user = input("Username: ")
        pwd = input("Password: ")

        if authenticate_user(user, pwd):
            print("Access granted")
        else:
            print("Access denied")

    elif choice == 2:
        list_users()

    elif choice == 3:
        name = input("Enter username: ")
        add_user(name)

    elif choice == 4:
        print(read_users())

    elif choice == 5:
        sys.exit(0)

if __name__ == "__main__":
    main()
