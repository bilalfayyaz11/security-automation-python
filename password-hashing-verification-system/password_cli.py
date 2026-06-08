#!/usr/bin/env python3
"""
Interactive CLI for the secure password manager.
"""

import getpass

from secure_password_manager import SecurePasswordManager


def main() -> None:
    manager = SecurePasswordManager()

    print("=" * 60)
    print("SECURE PASSWORD MANAGEMENT SYSTEM")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("1. Register new user")
        print("2. Login")
        print("3. List users")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
            manager.register_user(username, password)

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")

            if manager.verify_password(username, password):
                print(f"\nWelcome, {username}!")
            else:
                print("\nAccess denied.")

        elif choice == "3":
            users = manager.list_users()
            print(f"\nRegistered users: {', '.join(users) if users else 'None'}")

        elif choice == "4":
            print("\nGoodbye.")
            break

        else:
            print("\n[ERROR] Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
