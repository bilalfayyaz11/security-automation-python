#!/usr/bin/env python3

import re

def validate_hostname(hostname):

    if len(hostname) > 253:
        return False

    if hostname.endswith('.'):
        hostname = hostname[:-1]

    labels = hostname.split('.')

    label_pattern = re.compile(
        r'^[a-zA-Z0-9]'
        r'([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )

    for label in labels:
        if len(label) < 1 or len(label) > 63:
            return False

        if not label_pattern.match(label):
            return False

    return True


def test_hostnames():

    test_cases = [
        ("example.com", True),
        ("sub.example.com", True),
        ("my-server.example.com", True),
        ("server1.example.com", True),
        ("-invalid.com", False),
        ("invalid-.com", False),
        ("inv@lid.com", False),
        ("a" * 64 + ".com", False),
        ("valid.example.", True)
    ]

    print("Hostname Validation Tests:")
    print("-" * 60)

    for hostname, expected in test_cases:
        result = validate_hostname(hostname)
        status = "PASS" if result == expected else "FAIL"
        print(f"{hostname:30} | Expected: {expected:5} | Got: {result:5} | {status}")


if __name__ == "__main__":
    test_hostnames()
