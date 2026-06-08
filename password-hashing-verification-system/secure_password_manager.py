#!/usr/bin/env python3
"""
Secure password manager using bcrypt.

Stores only bcrypt password hashes, verifies passwords using bcrypt.checkpw,
and avoids plain-text credential storage.
"""

import json
import os
from pathlib import Path
from typing import Dict, List

import bcrypt


class SecurePasswordManager:
    def __init__(self, storage_file: str = "secure_passwords.json", bcrypt_rounds: int = 12):
        self.storage_file = Path(storage_file)
        self.bcrypt_rounds = bcrypt_rounds
        self.users = self._load_users()

    def _load_users(self) -> Dict[str, str]:
        if self.storage_file.exists():
            with self.storage_file.open("r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def _save_users(self) -> None:
        with self.storage_file.open("w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=2)

        os.chmod(self.storage_file, 0o600)

    def hash_password(self, password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty")

        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)

        return hashed.decode("utf-8")

    def register_user(self, username: str, password: str) -> bool:
        username = username.strip().lower()

        if not username:
            print("[ERROR] Username cannot be empty")
            return False

        if username in self.users:
            print(f"[ERROR] User '{username}' already exists")
            return False

        hashed_password = self.hash_password(password)

        self.users[username] = {
            "password_hash": hashed_password,
            "algorithm": "bcrypt",
            "bcrypt_rounds": self.bcrypt_rounds,
        }

        self._save_users()

        print(f"[SUCCESS] User '{username}' registered successfully")
        return True

    def verify_password(self, username: str, password: str) -> bool:
        username = username.strip().lower()

        if username not in self.users:
            print(f"[ERROR] User '{username}' not found")
            return False

        stored_hash = self.users[username]["password_hash"].encode("utf-8")
        password_bytes = password.encode("utf-8")

        result = bcrypt.checkpw(password_bytes, stored_hash)

        if result:
            print(f"[SUCCESS] Password verified for '{username}'")
        else:
            print(f"[FAILED] Invalid password for '{username}'")

        return result

    def list_users(self) -> List[str]:
        return sorted(self.users.keys())


if __name__ == "__main__":
    print("=== SECURE PASSWORD MANAGER ===\n")

    manager = SecurePasswordManager()

    print("--- Registering Users ---")
    manager.register_user("alice", "SecurePass123!")
    manager.register_user("bob", "MyP@ssw0rd")
    manager.register_user("alice", "duplicate")

    print("\n--- Verifying Passwords ---")
    manager.verify_password("alice", "SecurePass123!")
    manager.verify_password("alice", "WrongPassword")
    manager.verify_password("bob", "MyP@ssw0rd")
    manager.verify_password("charlie", "anything")

    print("\n--- Registered Users ---")
    print(f"Users: {manager.list_users()}")
