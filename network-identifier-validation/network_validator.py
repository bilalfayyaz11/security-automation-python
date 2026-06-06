#!/usr/bin/env python3

import ipaddress
import re

def detect_and_validate(identifier):

    if '.' in identifier and ':' not in identifier:
        parts = identifier.split('.')

        if len(parts) == 4 and all(part.isdigit() for part in parts):
            try:
                ipaddress.IPv4Address(identifier)
                return ('IPv4', True)
            except ValueError:
                return ('IPv4', False)

        try:
            ipaddress.IPv4Address(identifier)
            return ('IPv4', True)
        except ValueError:
            pass

    if ':' in identifier:
        try:
            ipaddress.IPv6Address(identifier)
            return ('IPv6', True)
        except ValueError:
            return ('IPv6', False)

    if len(identifier) <= 253:
        hostname = identifier[:-1] if identifier.endswith('.') else identifier
        labels = hostname.split('.')

        label_pattern = re.compile(
            r'^[a-zA-Z0-9]'
            r'([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )

        if all(label_pattern.match(label) for label in labels):
            return ('Hostname', True)

    return ('Unknown', False)


def main():

    print("Network Identifier Validator")
    print("=" * 60)
    print("Enter network identifiers to validate")
    print("Type quit to exit\n")

    while True:
        identifier = input("Enter identifier: ").strip()

        if identifier.lower() == 'quit':
            break

        if not identifier:
            continue

        id_type, is_valid = detect_and_validate(identifier)
        status = "VALID" if is_valid else "INVALID"

        print(f"Type: {id_type:10} | Status: {status}")
        print()


if __name__ == "__main__":
    main()
