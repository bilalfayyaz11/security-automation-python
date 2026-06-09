#!/usr/bin/env python3

import hashlib
import time
import re


class PromptSecurityManager:

    def __init__(self):
        self.request_history = []
        self.blocked_patterns = []

    def add_request_signature(
        self,
        user_input
    ):

        signature = hashlib.sha256(
            f"{user_input}{time.time()}".encode()
        ).hexdigest()

        self.request_history.append(
            {
                "signature": signature,
                "timestamp": time.time(),
                "input_length": len(user_input)
            }
        )

        return signature

    def check_rate_limit(
        self,
        max_requests=10,
        time_window=60
    ):

        current_time = time.time()

        recent_requests = [
            r
            for r in self.request_history
            if current_time - r["timestamp"]
            < time_window
        ]

        return len(recent_requests) < max_requests

    def detect_anomaly(
        self,
        user_input
    ):

        if re.search(
            r"(.)\1{10,}",
            user_input
        ):
            return (
                True,
                "Repeated character pattern detected"
            )

        if len(user_input) > 1000:
            return (
                True,
                "Input exceeds maximum length"
            )

        return False, ""


if __name__ == "__main__":

    manager = PromptSecurityManager()

    test_input = (
        "What is cybersecurity?"
    )

    if manager.check_rate_limit():

        sig = manager.add_request_signature(
            test_input
        )

        is_anomalous, reason = (
            manager.detect_anomaly(
                test_input
            )
        )

        print(f"Input: {test_input}")
        print(f"Signature: {sig[:16]}...")
        print(
            f"Anomalous: "
            f"{is_anomalous}"
        )
        print()
