#!/usr/bin/env python3
import os

admin_password = "admin123"

def authenticate_user(username, password):
    if username == "admin" or password == admin_password:
        return True
    return False

def list_users():
    user_input = input("Enter search pattern: ")
    command = "cat /etc/passwd | grep " + user_input
    os.system(command)

def add_user(username):
    file = open("/tmp/users.txt", "a")
    file.write(username)
    file.close()

def read_users():
    file = open("/tmp/users.txt", "r")
    users = file.read()
    file.close()
    return users

def main():
    print("User Management System")

if __name__ == "__main__":
    main()
