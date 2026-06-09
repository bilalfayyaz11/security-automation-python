from validators import AIOutputValidator


class CustomValidator(AIOutputValidator):
    def __init__(self):
        super().__init__()
        self.max_response_length = 500
        self.required_keywords = []

    def check_response_length(self, output):
        response = output.get("response", "")
        length = len(response)

        if length == 0:
            return False, "Response is empty"

        if length > self.max_response_length:
            return False, f"Response too long: {length} chars (max: {self.max_response_length})"

        return True, f"Response length acceptable: {length} chars"

    def check_required_keywords(self, output, keywords):
        if not keywords:
            return True, "No required keywords specified"

        response = output.get("response", "").lower()
        missing = [kw for kw in keywords if kw.lower() not in response]

        if missing:
            return False, f"Missing required keywords: {', '.join(missing)}"

        return True, "All required keywords present"


if __name__ == "__main__":
    validator = CustomValidator()

    test_output = {
        "query": "What is cybersecurity?",
        "response": "Cybersecurity protects systems and data from threats.",
        "confidence": 0.92,
        "sources": ["security_guide"],
        "timestamp": "2024-01-15T10:35:00Z"
    }

    print("Custom Validation Example:")
    print("-" * 40)

    is_valid, msg = validator.check_response_length(test_output)
    print(f"Length Check: {msg}")

    is_valid, msg = validator.check_required_keywords(
        test_output,
        ["cybersecurity", "protect"]
    )
    print(f"Keyword Check: {msg}")
