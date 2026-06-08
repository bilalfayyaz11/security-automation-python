#!/usr/bin/env python3
"""
Secure Token Generator
Generates cryptographically secure tokens for multiple authentication and application security use cases.
"""

import secrets
import string


def generate_hex_token(length=32):
    """Generate a hexadecimal token using cryptographically secure randomness."""
    return secrets.token_hex(length)


def generate_url_safe_token(length=32):
    """Generate a URL-safe token suitable for links, sessions, and reset flows."""
    return secrets.token_urlsafe(length)


def generate_alphanumeric_token(length=16):
    """Generate an alphanumeric token using secure random character selection."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def main():
    print("=== Secure Token Generator ===\n")

    print("1. Hexadecimal Token (64 chars):")
    print(f"   {generate_hex_token(32)}\n")

    print("2. URL-Safe Token:")
    print(f"   {generate_url_safe_token(32)}\n")

    print("3. Alphanumeric Token (16 chars):")
    print(f"   {generate_alphanumeric_token(16)}\n")


if __name__ == "__main__":
    main()
