#!/usr/bin/env python3
"""
Secure Configuration Loader and Validator

Loads YAML configuration files, validates required fields, checks file permissions,
and detects common security risks such as weak passwords, insecure protocols,
disabled TLS, privileged usernames, and dangerous runtime settings.
"""

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


class ConfigValidator:
    """
    Load and validate configuration files for security issues.
    """

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_config(self) -> bool:
        """
        Load the configuration file safely with basic permission checks.
        """
        try:
            if not self.config_path.exists():
                self.errors.append(f"Configuration file not found: {self.config_path}")
                return False

            if not self.config_path.is_file():
                self.errors.append(f"Configuration path is not a regular file: {self.config_path}")
                return False

            file_mode = stat.S_IMODE(self.config_path.stat().st_mode)

            if file_mode & stat.S_IWOTH:
                self.errors.append("Configuration file is world-writable")

            if file_mode & stat.S_IROTH:
                self.warnings.append("Configuration file is world-readable")

            with self.config_path.open("r", encoding="utf-8") as file:
                loaded_data = yaml.safe_load(file)

            if loaded_data is None:
                self.errors.append("Configuration file is empty")
                return False

            if not isinstance(loaded_data, dict):
                self.errors.append("Configuration root must be a YAML mapping/object")
                return False

            self.config_data = loaded_data
            return True

        except yaml.YAMLError as exc:
            self.errors.append(f"YAML parsing error: {exc}")
            return False
        except PermissionError:
            self.errors.append(f"Permission denied while reading configuration: {self.config_path}")
            return False
        except OSError as exc:
            self.errors.append(f"OS error while loading configuration: {exc}")
            return False

    def validate_required_fields(self, required_schema: Dict[str, List[str]]) -> bool:
        """
        Validate that all required sections and fields are present.
        """
        is_valid = True

        for section, fields in required_schema.items():
            section_value = self.config_data.get(section)

            if section_value is None:
                self.errors.append(f"Missing required section: {section}")
                is_valid = False
                continue

            if not isinstance(section_value, dict):
                self.errors.append(f"Required section must be a mapping/object: {section}")
                is_valid = False
                continue

            for field in fields:
                if field not in section_value:
                    self.errors.append(f"Missing required field: {section}.{field}")
                    is_valid = False

        return is_valid

    def check_weak_passwords(self) -> List[str]:
        """
        Recursively check for weak or common passwords.
        """
        weak_passwords = []
        weak_values = {"123456", "password", "admin", "root", "12345", "qwerty", "letmein"}

        def search_passwords(data: Any, path: str = "") -> None:
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else str(key)

                    if "password" in str(key).lower() or "passwd" in str(key).lower():
                        if not isinstance(value, str):
                            weak_passwords.append(f"{current_path}: Password value must be a string")
                            continue

                        if len(value) < 12:
                            weak_passwords.append(f"{current_path}: Too short (< 12 chars)")

                        if value.lower() in weak_values:
                            weak_passwords.append(f"{current_path}: Common weak password")

                        if not any(char.isupper() for char in value):
                            weak_passwords.append(f"{current_path}: Missing uppercase character")

                        if not any(char.islower() for char in value):
                            weak_passwords.append(f"{current_path}: Missing lowercase character")

                        if not any(char.isdigit() for char in value):
                            weak_passwords.append(f"{current_path}: Missing digit")

                        if not any(not char.isalnum() for char in value):
                            weak_passwords.append(f"{current_path}: Missing special character")
                    else:
                        search_passwords(value, current_path)

            elif isinstance(data, list):
                for index, item in enumerate(data):
                    search_passwords(item, f"{path}[{index}]")

        search_passwords(self.config_data)
        return weak_passwords

    def check_insecure_protocols(self) -> List[str]:
        """
        Check for HTTP URLs and disabled SSL/TLS.
        """
        issues = []

        def search_values(data: Any, path: str = "") -> None:
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else str(key)
                    key_lower = str(key).lower()

                    if isinstance(value, str) and value.startswith("http://"):
                        issues.append(f"{current_path}: Uses insecure HTTP protocol")

                    if key_lower in {"ssl_enabled", "tls_enabled", "verify_ssl", "verify_tls"} and value is False:
                        issues.append(f"{current_path}: SSL/TLS verification is disabled")

                    search_values(value, current_path)

            elif isinstance(data, list):
                for index, item in enumerate(data):
                    search_values(item, f"{path}[{index}]")

        search_values(self.config_data)
        return issues

    def check_dangerous_settings(self) -> List[str]:
        """
        Check for risky production configuration values.
        """
        dangerous = []

        logging_level = str(self.config_data.get("logging", {}).get("level", "")).upper()
        if logging_level == "DEBUG":
            self.warnings.append("Debug logging enabled - may expose sensitive information")

        db_user = str(self.config_data.get("database", {}).get("username", ""))
        if db_user.lower() in {"root", "admin", "administrator"}:
            dangerous.append(f"Using privileged username: {db_user}")

        feature_flags = self.config_data.get("features", {})
        if isinstance(feature_flags, dict):
            if feature_flags.get("unsafe_mode") is True:
                dangerous.append("features.unsafe_mode: Unsafe mode is enabled")
            if feature_flags.get("admin_panel_enabled") is True:
                dangerous.append("features.admin_panel_enabled: Admin panel is enabled")

        return dangerous

    def generate_report(self) -> str:
        """
        Generate a formatted validation report.
        """
        report = []
        report.append("=" * 70)
        report.append("CONFIGURATION SECURITY VALIDATION REPORT")
        report.append("=" * 70)
        report.append(f"Configuration File: {self.config_path}")
        report.append("")

        if self.errors:
            report.append("[ERRORS] - Critical Issues:")
            for error in self.errors:
                report.append(f"  - {error}")
            report.append("")

        if self.warnings:
            report.append("[WARNINGS] - Security Concerns:")
            for warning in self.warnings:
                report.append(f"  - {warning}")
            report.append("")

        if not self.errors and not self.warnings:
            report.append("[SUCCESS] Configuration passed all security checks!")
        else:
            report.append(f"Total Errors: {len(self.errors)}")
            report.append(f"Total Warnings: {len(self.warnings)}")

        report.append("=" * 70)
        return "\n".join(report)


def validate_file(config_file: str) -> int:
    required_schema = {
        "database": ["host", "port", "username", "password", "ssl_enabled"],
        "api": ["endpoint", "timeout"],
        "logging": ["level"],
    }

    validator = ConfigValidator(config_file)

    if validator.load_config():
        validator.validate_required_fields(required_schema)

        for issue in validator.check_weak_passwords():
            validator.warnings.append(f"Weak password: {issue}")

        for issue in validator.check_insecure_protocols():
            validator.warnings.append(f"Insecure protocol: {issue}")

        for issue in validator.check_dangerous_settings():
            validator.warnings.append(f"Dangerous setting: {issue}")

    print(validator.generate_report())

    return 1 if validator.errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Secure YAML configuration validator")
    parser.add_argument(
        "config_files",
        nargs="*",
        default=[
            "config_secure.yaml",
            "config_insecure.yaml",
            "config_incomplete.yaml",
            "config_test.yaml",
        ],
        help="YAML configuration files to validate",
    )

    args = parser.parse_args()

    exit_code = 0
    for config_file in args.config_files:
        print(f"\nValidating: {config_file}")
        print("-" * 70)
        exit_code = max(exit_code, validate_file(config_file))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
