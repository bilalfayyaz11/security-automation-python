#!/usr/bin/env python3

import re
import html
import os


class InputSanitizer:

    DANGEROUS_CHARS = [
        '<', '>', '&', '"', "'", ';',
        '|', '`', '$', '(', ')', '{', '}'
    ]

    SQL_KEYWORDS = [
        'SELECT',
        'INSERT',
        'UPDATE',
        'DELETE',
        'DROP',
        'UNION',
        '--',
        '/*'
    ]

    @staticmethod
    def remove_dangerous_chars(user_input):
        sanitized = user_input

        for char in InputSanitizer.DANGEROUS_CHARS:
            sanitized = sanitized.replace(char, '')

        return sanitized

    @staticmethod
    def validate_alphanumeric(user_input, allow_spaces=True):

        if allow_spaces:
            pattern = r'^[a-zA-Z0-9 ]+$'
        else:
            pattern = r'^[a-zA-Z0-9]+$'

        return bool(re.match(pattern, user_input))

    @staticmethod
    def validate_email(email):

        pattern = (
            r'^[a-zA-Z0-9._%+-]+'
            r'@[a-zA-Z0-9.-]+'
            r'\.[a-zA-Z]{2,}$'
        )

        return bool(re.match(pattern, email))

    @staticmethod
    def sanitize_filename(filename):

        sanitized = os.path.basename(filename)

        sanitized = re.sub(
            r'[^a-zA-Z0-9._-]',
            '',
            sanitized
        )

        return sanitized

    @staticmethod
    def escape_html(user_input):

        return html.escape(user_input)

    @staticmethod
    def check_sql_injection(user_input):

        upper_input = user_input.upper()

        for keyword in InputSanitizer.SQL_KEYWORDS:
            if keyword in upper_input:
                return True

        return False
