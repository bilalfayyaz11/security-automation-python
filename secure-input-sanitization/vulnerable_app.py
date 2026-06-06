#!/usr/bin/env python3

import os

def unsafe_command_execution(user_input):
    command = f"echo {user_input}"
    os.system(command)

def unsafe_file_access(filename):
    try:
        with open(filename, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Vulnerable Application Demo ===")

    print("\n[Test 1] Command Injection:")
    user_input = "Hello; ls -la"
    print(f"Input: {user_input}")
    unsafe_command_execution(user_input)

    print("\n[Test 2] Path Traversal:")
    filename = "../../etc/passwd"
    print(f"Filename: {filename}")
    unsafe_file_access(filename)
