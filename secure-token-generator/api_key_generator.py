#!/usr/bin/env python3
"""
API Key and Secret Generator
Creates API keys, signing secrets, webhook secrets, and strong passwords using Python's secrets module.
"""

import secrets
import string
import json
import os
from datetime import datetime


def generate_api_key(prefix="sk", length=32):
    """Generate an API key with a readable prefix and secure random suffix."""
    alphabet = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}_{random_part}"


def generate_secret_key(length=64):
    """Generate a high-entropy hexadecimal secret key."""
    return secrets.token_hex(length)


def generate_password(length=16, use_special=True):
    """Generate a secure password with optional special characters."""
    alphabet = string.ascii_letters + string.digits
    if use_special:
        alphabet += string.punctuation

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and (not use_special or any(c in string.punctuation for c in password))
        ):
            return password


def save_credentials(filename, credentials):
    """Save generated credentials to a JSON file with owner-only permissions."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(credentials, f, indent=2)
    os.chmod(filename, 0o600)


def main():
    print("=== API Key and Secret Generator ===\n")

    credentials = {
        "generated_at": datetime.now().isoformat(),
        "api_key": generate_api_key("sk", 32),
        "api_secret": generate_secret_key(64),
        "webhook_secret": generate_secret_key(32),
        "admin_password": generate_password(20, use_special=True),
        "database_password": generate_password(24, use_special=True),
    }

    print("Generated Credentials:")
    print("-" * 60)
    for key, value in credentials.items():
        if key != "generated_at":
            print(f"{key:20s}: {value}")
    print("-" * 60)

    output_file = "credentials.json"
    save_credentials(output_file, credentials)
    print(f"\nCredentials saved to: {output_file}")
    print("File permissions set to 600 (owner read/write only)")


if __name__ == "__main__":
    main()
