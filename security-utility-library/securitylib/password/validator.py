"""
Password validation module.
"""

def check_length(password, min_length=8):
    return len(password) >= min_length


def has_uppercase(password):
    return any(char.isupper() for char in password)


def has_lowercase(password):
    return any(char.islower() for char in password)


def has_digit(password):
    return any(char.isdigit() for char in password)


def has_special_char(password):
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return any(char in special_chars for char in password)


def validate_password(password, min_length=8):
    errors = []

    if not check_length(password, min_length):
        errors.append(f"Password must be at least {min_length} characters")

    if not has_uppercase(password):
        errors.append("Password must contain an uppercase letter")

    if not has_lowercase(password):
        errors.append("Password must contain a lowercase letter")

    if not has_digit(password):
        errors.append("Password must contain a digit")

    if not has_special_char(password):
        errors.append("Password must contain a special character")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
