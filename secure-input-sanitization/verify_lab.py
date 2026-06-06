#!/usr/bin/env python3

from input_sanitizer import InputSanitizer

print("Verification Tests:")
print("-" * 50)

test1 = InputSanitizer.remove_dangerous_chars("test<script>")
print(f"Test 1 - Remove dangerous chars: {'PASS' if '<' not in test1 and '>' not in test1 else 'FAIL'}")

test2 = InputSanitizer.validate_alphanumeric("user123")
print(f"Test 2 - Alphanumeric validation: {'PASS' if test2 else 'FAIL'}")

test3 = InputSanitizer.validate_email("user@example.com")
print(f"Test 3 - Email validation: {'PASS' if test3 else 'FAIL'}")

test4 = InputSanitizer.sanitize_filename("../../etc/passwd")
print(f"Test 4 - Filename sanitization: {'PASS' if '..' not in test4 and '/' not in test4 else 'FAIL'}")

test5 = InputSanitizer.check_sql_injection("SELECT * FROM users")
print(f"Test 5 - SQL injection detection: {'PASS' if test5 else 'FAIL'}")

print("-" * 50)
print("All tests completed!")
