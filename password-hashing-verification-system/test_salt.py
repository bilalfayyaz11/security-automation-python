#!/usr/bin/env python3
"""
Demonstrates that bcrypt generates a different hash for the same password
because each hash includes a unique salt.
"""

import bcrypt

password = "SamePassword123"

print("Hashing the same password 3 times:\n")

for index in range(3):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    print(f"Hash {index + 1}: {hashed.decode('utf-8')}")

print("\nNotice: Each hash is different due to unique salt.")
print("This helps prevent rainbow table attacks.")
