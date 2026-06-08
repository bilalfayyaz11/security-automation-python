#!/usr/bin/env python3
"""
Plain text password storage demonstration.

This intentionally shows insecure password storage so the risk can be compared
against bcrypt-based secure hashing.
"""


def store_password_insecure(username: str, password: str) -> None:
    with open("insecure_passwords.txt", "a", encoding="utf-8") as file:
        file.write(f"{username}:{password}\n")
    print(f"[INSECURE] Stored password for {username}")


def verify_password_insecure(username: str, password: str) -> bool:
    try:
        with open("insecure_passwords.txt", "r", encoding="utf-8") as file:
            for line in file:
                stored_user, stored_pass = line.strip().split(":", 1)
                if stored_user == username and stored_pass == password:
                    return True
        return False
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    print("=== INSECURE PASSWORD STORAGE DEMO ===")

    store_password_insecure("alice", "password123")
    store_password_insecure("bob", "qwerty456")

    print("\nVerifying passwords:")
    print(f"Alice login: {verify_password_insecure('alice', 'password123')}")
    print(f"Bob wrong password: {verify_password_insecure('bob', 'wrong')}")

    print("\n[WARNING] Check insecure_passwords.txt to see the danger.")
