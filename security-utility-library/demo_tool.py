#!/usr/bin/env python3

from securitylib.password import validator
from securitylib.hash import hasher


def main():
    print("Security Utility Library Demo\n")

    print("1. Validate Password")
    print("2. Hash Data")
    print("3. Exit")

    choice = input("\nEnter choice (1-3): ")

    if choice == "1":
        password = input("Enter password: ")

        result = validator.validate_password(password)

        if result["valid"]:
            print("\nPassword is strong")
        else:
            print("\nPassword is weak")

            for error in result["errors"]:
                print("-", error)

    elif choice == "2":
        data = input("Enter data: ")
        print(hasher.hash_sha256(data))

    else:
        print("Goodbye")


if __name__ == "__main__":
    main()
