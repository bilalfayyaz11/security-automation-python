import re
import subprocess

def validate_hostname(hostname):

    pattern = r'^[a-zA-Z0-9.-]+$'

    if not re.match(pattern, hostname):
        return False

    if len(hostname) > 253:
        return False

    return True

def ping_host(hostname):

    if not validate_hostname(hostname):
        print("Invalid hostname")
        return 1

    try:

        result = subprocess.run(
            ["ping", "-c", "4", hostname],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )

        print(result.stdout)

        return result.returncode

    except subprocess.TimeoutExpired:

        print("Ping timeout")

        return 1

    except Exception as e:

        print(f"Error: {e}")

        return 1

if __name__ == "__main__":

    host = input("Enter hostname to ping: ")

    ping_host(host)
