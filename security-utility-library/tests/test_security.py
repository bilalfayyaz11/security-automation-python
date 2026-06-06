import sys

sys.path.insert(0, '/home/ubuntu/security-utility-library')

from securitylib.password import validator
from securitylib.hash import hasher


def test_password_validation():
    print("=== Testing Password Validation ===\n")

    passwords = [
        "weak",
        "StrongPass123!",
        "noupppercase123!",
        "NOLOWERCASE123!",
        "NoDigitsHere!",
        "NoSpecialChar123"
    ]

    for pwd in passwords:
        result = validator.validate_password(pwd)

        print(f"Password: {pwd}")
        print(f"Valid: {result['valid']}")

        if not result["valid"]:
            print(f"Errors: {', '.join(result['errors'])}")

        print()


def test_hashing():
    print("=== Testing Hash Functions ===\n")

    data = "SecureData123"

    hash_result = hasher.hash_sha256(data)

    print(f"Data: {data}")
    print(f"SHA-256: {hash_result}")

    print()

    print(f"Hash verification: {hasher.verify_hash(data, hash_result)}")

    print()

    with open("/tmp/test_file.txt", "w") as file:
        file.write("Test file content for hashing")

    print(f"File hash: {hasher.hash_file('/tmp/test_file.txt')}")


if __name__ == "__main__":
    test_password_validation()
    test_hashing()
    print("\n=== All Tests Complete ===")
