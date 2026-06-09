import os

def ping_host(hostname):

    command = f"ping -c 4 {hostname}"

    result = os.system(command)

    return result

if __name__ == "__main__":

    host = input("Enter hostname to ping: ")

    ping_host(host)
