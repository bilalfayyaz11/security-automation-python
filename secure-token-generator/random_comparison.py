import random
import secrets

print("=== Insecure Random (for demonstration only) ===")
random.seed(42)
for i in range(3):
    print(f"Random number {i+1}: {random.randint(1000, 9999)}")

print("\n=== Cryptographically Secure Random ===")
for i in range(3):
    print(f"Secure number {i+1}: {secrets.randbelow(9000) + 1000}")
