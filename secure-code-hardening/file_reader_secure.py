import os

from pathlib import Path

def read_user_file(filename):

    base_path = Path("/tmp/uploads").resolve()

    safe_filename = os.path.basename(filename)

    file_path = (base_path / safe_filename).resolve()

    try:
        file_path.relative_to(base_path)

    except ValueError:
        return "Error: Access denied - path traversal detected"

    if not file_path.exists():
        return "Error: File not found"

    if not file_path.is_file():
        return "Error: Not a file"

    try:
        with open(file_path, "r") as f:
            return f.read()

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":

    file = input("Enter filename to read: ")

    print(read_user_file(file))
