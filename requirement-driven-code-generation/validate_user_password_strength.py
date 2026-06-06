def validate_user_password_strength(input_data):
    """
    Validate user password strength.

    Args:
        input_data: Password string to validate

    Returns:
        bool: True if password meets all strength rules, False otherwise
    """
    password = str(input_data)

    has_length = len(password) >= 8
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)

    return all([has_length, has_upper, has_lower, has_digit, has_special])


if __name__ == "__main__":
    test_passwords = [
        "weak",
        "StrongPass1!",
        "NoSpecial123",
        "MySecureP@ssw0rd"
    ]

    for password in test_passwords:
        is_valid = validate_user_password_strength(password)
        print(f"Password: '{password}' - Valid: {is_valid}")
