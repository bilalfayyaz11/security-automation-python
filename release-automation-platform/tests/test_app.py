import sys

sys.path.insert(0, "src")

from app import calculate, greet


def test_greet():
    result = greet("Test")
    assert "Hello, Test!" in result
    print("✓ Greet test passed")


def test_calculate():
    assert calculate(2, 3) == 5
    print("✓ Calculate test passed")


if __name__ == "__main__":
    test_greet()
    test_calculate()
    print("\nAll tests passed!")
