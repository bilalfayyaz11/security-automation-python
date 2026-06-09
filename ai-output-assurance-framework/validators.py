from jsonschema import validate, ValidationError
import re


class AIOutputValidator:
    def __init__(self):
        self.schema = {
            "type": "object",
            "required": ["query", "response", "confidence", "timestamp"],
            "properties": {
                "query": {"type": "string", "minLength": 1},
                "response": {"type": "string", "minLength": 1},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "sources": {"type": "array"},
                "timestamp": {"type": "string"}
            }
        }

        self.forbidden_patterns = [
            r"\bhack\b",
            r"\bexploit\b",
            r"\bcrack\b",
            r"\bmalware\b"
        ]

        self.min_confidence = 0.7

    def validate_schema(self, output):
        try:
            validate(instance=output, schema=self.schema)
            return True, "Schema validation passed"
        except ValidationError as e:
            return False, f"Schema validation failed: {e.message}"

    def check_confidence(self, output):
        confidence = output.get("confidence")

        if confidence is None:
            return False, "Confidence score missing"

        if confidence < self.min_confidence:
            return False, f"Confidence {confidence} below threshold {self.min_confidence}"

        return True, f"Confidence {confidence} acceptable"

    def filter_content(self, output):
        response_text = output.get("response", "").lower()

        for pattern in self.forbidden_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return False, f"Forbidden pattern detected: {pattern}"

        return True, "Content filter passed"

    def check_hallucination_indicators(self, output):
        sources = output.get("sources", [])

        if not sources or "unknown" in sources:
            return False, "No valid sources provided - potential hallucination"

        response = output.get("response", "")
        suspicious_phrases = ["approximately", "around", "roughly"]

        if any(phrase in response.lower() for phrase in suspicious_phrases):
            if not sources or len(sources) == 0:
                return False, "Specific claims without sources - verify accuracy"

        return True, "No obvious hallucination indicators"

    def validate_all(self, output):
        results = {
            "overall_valid": True,
            "checks": {}
        }

        checks = [
            ("schema", self.validate_schema),
            ("confidence", self.check_confidence),
            ("content_filter", self.filter_content),
            ("hallucination", self.check_hallucination_indicators)
        ]

        for check_name, check_func in checks:
            is_valid, message = check_func(output)

            results["checks"][check_name] = {
                "passed": is_valid,
                "message": message
            }

            if not is_valid:
                results["overall_valid"] = False

        return results
