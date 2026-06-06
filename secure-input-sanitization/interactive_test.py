#!/usr/bin/env python3

from input_sanitizer import InputSanitizer

def main():
    while True:
        print("\n" + "="*50)
        print("Secure Input Sanitizer - Interactive Testing")
        print("="*50)
        print("1. Test Username Validation")
        print("2. Test Email Validation")
        print("3. Test HTML Escaping")
        print("4. Test Filename Sanitization")
        print("5. Test SQL Injection Detection")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            username = input("Enter username to test: ")
            is_valid = InputSanitizer.validate_alphanumeric(username, allow_spaces=False)
            print(f"Valid: {is_valid}")
            if is_valid:
                print(f"Sanitized: {InputSanitizer.remove_dangerous_chars(username)}")

        elif choice == '2':
            email = input("Enter email to test: ")
            print(f"Valid email format: {InputSanitizer.validate_email(email)}")

        elif choice == '3':
            text = input("Enter text with HTML: ")
            print(f"Original: {text}")
            print(f"Escaped: {InputSanitizer.escape_html(text)}")

        elif choice == '4':
            filename = input("Enter filename to sanitize: ")
            print(f"Original: {filename}")
            print(f"Sanitized: {InputSanitizer.sanitize_filename(filename)}")

        elif choice == '5':
            query = input("Enter text to check for SQL injection: ")
            print(f"SQL injection detected: {InputSanitizer.check_sql_injection(query)}")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
