#!/usr/bin/env python3

from requirement_parser import RequirementParser

parser = RequirementParser()

custom_req = "verify email format"

parsed = parser.parse_requirement(custom_req)

template = parser.generate_function_template(parsed)

print(f"Custom Requirement: {custom_req}")
print()
print("Parsed Structure:")
print(parsed)

print("\nGenerated Function:\n")
print(template)
