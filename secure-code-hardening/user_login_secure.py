import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_username(username):

    if not username:
        return False

    if len(username) > 50:
        return False

    return username.replace("_", "").isalnum()

def authenticate_user(username, password):

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"

    hashed_pwd = hash_password(password)

    cursor.execute(
        query,
        (username, hashed_pwd)
    )

    result = cursor.fetchone()

    conn.close()

    return bool(result)

if __name__ == "__main__":

    user = input("Enter username: ")

    if not validate_username(user):
        print("Invalid username format")
        raise SystemExit(1)

    pwd = input("Enter password: ")

    if authenticate_user(user, pwd):
        print("Login successful!")
    else:
        print("Login failed!")
