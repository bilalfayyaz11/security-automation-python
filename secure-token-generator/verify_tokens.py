#!/usr/bin/env python3
import secrets

tokens = set()
count = 1000

for _ in range(count):
    token = secrets.token_hex(32)
    tokens.add(token)

print(f"Generated: {count} tokens")
print(f"Unique: {len(tokens)} tokens")
print(f"Duplicates: {count - len(tokens)}")

if len(tokens) == count:
    print("\nSUCCESS: All tokens are unique!")
else:
    print("\nWARNING: Duplicates found")
