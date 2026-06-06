"""
Hashing utilities.
"""

import hashlib


def hash_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


def hash_file(filepath):
    with open(filepath, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()


def verify_hash(data, expected_hash):
    return hash_sha256(data) == expected_hash
