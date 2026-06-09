import json
import os
from validators import AIOutputValidator


def load_ai_output(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def validate_output_file(filepath, validator):
    print(f"\n{'=' * 60}")
    print(f"Validating: {os.path.basename(filepath)}")
    print(f"{'=' * 60}")

    output = load_ai_output(filepath)
    results = validator.validate_all(output)

    print(f"\nOverall Status: {'PASS' if results['overall_valid'] else 'FAIL'}")
    print("\nDetailed Checks:")

    for check_name, check_result in results["checks"].items():
        status = "PASS" if check_result["passed"] else "FAIL"
        print(f"  [{status}] {check_name}: {check_result['message']}")

    return results


def main():
    validator = AIOutputValidator()

    test_dir = "test_data"

    test_files = [
        os.path.join(test_dir, f)
        for f in os.listdir(test_dir)
        if f.endswith(".json")
    ]

    results_summary = []

    for filepath in sorted(test_files):
        result = validate_output_file(filepath, validator)
        results_summary.append({
            "file": os.path.basename(filepath),
            "valid": result["overall_valid"]
        })

    print(f"\n{'=' * 60}")
    print("VALIDATION SUMMARY")
    print(f"{'=' * 60}")

    for item in results_summary:
        status = "PASS" if item["valid"] else "FAIL"
        print(f"[{status}] {item['file']}")

    total = len(results_summary)
    passed = sum(1 for item in results_summary if item["valid"])

    print(f"\nTotal: {passed}/{total} outputs passed validation")


if __name__ == "__main__":
    main()
