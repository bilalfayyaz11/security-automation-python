import json
import os


def create_sample_outputs():
    good_output = {
        "query": "What is the capital of France?",
        "response": "The capital of France is Paris.",
        "confidence": 0.95,
        "sources": ["geography_db"],
        "timestamp": "2024-01-15T10:30:00Z"
    }

    hallucination_output = {
        "query": "What is the population of Mars?",
        "response": "Mars has a population of approximately 50,000 people living in underground colonies.",
        "confidence": 0.88,
        "sources": ["unknown"],
        "timestamp": "2024-01-15T10:31:00Z"
    }

    malformed_output = {
        "query": "Explain photosynthesis",
        "response": "",
        "confidence": None,
        "timestamp": "2024-01-15T10:32:00Z"
    }

    flagged_output = {
        "query": "How to secure a network?",
        "response": "To hack into a system, you should...",
        "confidence": 0.75,
        "sources": ["security_guide"],
        "timestamp": "2024-01-15T10:33:00Z"
    }

    samples = {
        "good": good_output,
        "hallucination": hallucination_output,
        "malformed": malformed_output,
        "flagged": flagged_output
    }

    os.makedirs("test_data", exist_ok=True)

    for name, data in samples.items():
        with open(f"test_data/{name}_output.json", "w") as f:
            json.dump(data, f, indent=2)

    print("Sample AI outputs created successfully!")


if __name__ == "__main__":
    create_sample_outputs()
