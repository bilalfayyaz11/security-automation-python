#!/usr/bin/env python3
"""
Token Manager
Interactive secure token generation utility for session tokens, CSRF tokens, password reset tokens,
API credentials, OTP secrets, and complete application token sets.
"""

import base64
import json
import os
import secrets
import string
from datetime import datetime


class TokenManager:
    """Manages generation and secure local storage of application tokens."""

    def __init__(self):
        self.tokens = {}

    def generate_session_token(self):
        """Generate a URL-safe session token."""
        return secrets.token_urlsafe(32)

    def generate_csrf_token(self):
        """Generate a CSRF token."""
        return secrets.token_hex(32)

    def generate_reset_token(self):
        """Generate a password reset token."""
        return secrets.token_urlsafe(48)

    def generate_api_key_pair(self, prefix="app"):
        """Generate an API key and secret pair."""
        safe_prefix = "".join(c.lower() for c in prefix if c.isalnum()) or "app"
        key_id = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        api_key = f"{safe_prefix}_{key_id}"
        api_secret = secrets.token_hex(32)
        return {"api_key": api_key, "api_secret": api_secret}

    def generate_otp_secret(self):
        """Generate a Base32 OTP/2FA secret."""
        random_bytes = secrets.token_bytes(20)
        return base64.b32encode(random_bytes).decode("utf-8")

    def create_token_set(self, name):
        """Create a complete token set for an application."""
        token_set = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "session_token": self.generate_session_token(),
            "csrf_token": self.generate_csrf_token(),
            "reset_token": self.generate_reset_token(),
            "api_credentials": self.generate_api_key_pair(name),
            "otp_secret": self.generate_otp_secret(),
        }
        self.tokens[name] = token_set
        return token_set

    def save_tokens(self, filename="tokens.json"):
        """Save generated tokens with owner-only permissions."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.tokens, f, indent=2)
        os.chmod(filename, 0o600)
        return filename


def print_menu():
    print("\n=== Secure Token Manager ===")
    print("1. Generate Session Token")
    print("2. Generate CSRF Token")
    print("3. Generate Password Reset Token")
    print("4. Generate API Key Pair")
    print("5. Generate OTP Secret")
    print("6. Generate Complete Token Set")
    print("7. Exit")
    print("=" * 30)


def main():
    manager = TokenManager()

    while True:
        print_menu()
        choice = input("\nSelect option (1-7): ").strip()

        if choice == "1":
            print(f"\nSession Token:\n{manager.generate_session_token()}")

        elif choice == "2":
            print(f"\nCSRF Token:\n{manager.generate_csrf_token()}")

        elif choice == "3":
            print(f"\nPassword Reset Token:\n{manager.generate_reset_token()}")

        elif choice == "4":
            pair = manager.generate_api_key_pair()
            print(f"\nAPI Key: {pair['api_key']}")
            print(f"API Secret: {pair['api_secret']}")

        elif choice == "5":
            print(f"\nOTP Secret (Base32):\n{manager.generate_otp_secret()}")

        elif choice == "6":
            name = input("Enter application name: ").strip()
            if name:
                token_set = manager.create_token_set(name)
                print(f"\nComplete token set generated for: {name}")
                print(json.dumps(token_set, indent=2))
                filename = manager.save_tokens()
                print(f"\nTokens saved to: {filename}")
            else:
                print("\nApplication name cannot be empty.")

        elif choice == "7":
            print("\nExiting Token Manager. Stay secure!")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()
