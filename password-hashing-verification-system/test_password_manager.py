#!/usr/bin/env python3
"""
Automated verification for secure password manager behavior.
"""

from pathlib import Path

from secure_password_manager import SecurePasswordManager


test_file = "test_secure_passwords.json"
Path(test_file).unlink(missing_ok=True)

manager = SecurePasswordManager(storage_file=test_file)

assert manager.register_user("bilal", "StrongPass123!") is True
assert manager.register_user("bilal", "AnotherPass123!") is False
assert manager.verify_password("bilal", "StrongPass123!") is True
assert manager.verify_password("bilal", "WrongPass") is False
assert manager.verify_password("missing", "anything") is False
assert "bilal" in manager.list_users()

content = Path(test_file).read_text(encoding="utf-8")
assert "StrongPass123!" not in content
assert "password_hash" in content
assert "bcrypt" in content

print("All password manager tests passed.")
