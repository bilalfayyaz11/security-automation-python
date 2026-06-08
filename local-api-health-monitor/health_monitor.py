#!/usr/bin/env python3
"""
Local API Health Monitor

Checks API endpoints, measures response time, logs service health,
detects failures, and writes the latest endpoint status to JSON.
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests


class APIHealthMonitor:
    def __init__(self, base_url: str, check_interval: int = 10, log_dir: str = "logs"):
        self.base_url = base_url.rstrip("/")
        self.check_interval = check_interval
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "health_monitor.log"
        self.status_file = self.log_dir / "current_status.json"

    def log_message(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(log_entry + "\n")

    def check_endpoint(self, endpoint: str, timeout: int = 5) -> Dict:
        url = f"{self.base_url}{endpoint}"

        result = {
            "endpoint": endpoint,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "response_time_ms": None,
            "status_code": None,
            "error": None,
        }

        try:
            start_time = time.perf_counter()
            response = requests.get(url, timeout=timeout)
            end_time = time.perf_counter()

            result["response_time_ms"] = round((end_time - start_time) * 1000, 2)
            result["status_code"] = response.status_code

            if 200 <= response.status_code < 300:
                result["status"] = "healthy"
            else:
                result["status"] = "unhealthy"
                result["error"] = f"HTTP {response.status_code}"

        except requests.exceptions.Timeout:
            result["status"] = "timeout"
            result["error"] = "Request timed out"

        except requests.exceptions.ConnectionError:
            result["status"] = "unreachable"
            result["error"] = "Could not connect to service"

        except requests.exceptions.RequestException as error:
            result["status"] = "error"
            result["error"] = str(error)

        return result

    def check_all_endpoints(self, endpoints: List[str]) -> List[Dict]:
        results = []

        for endpoint in endpoints:
            result = self.check_endpoint(endpoint)
            results.append(result)

            if result["status"] == "healthy":
                self.log_message(
                    f"{endpoint} is healthy "
                    f"(status={result['status_code']}, response_time={result['response_time_ms']}ms)",
                    "INFO",
                )
            else:
                self.log_message(
                    f"{endpoint} is {result['status']} "
                    f"(status={result['status_code']}, error={result['error']})",
                    "ERROR",
                )

        return results

    def save_status(self, results: List[Dict]) -> None:
        status_data = {
            "last_check": datetime.now().isoformat(),
            "base_url": self.base_url,
            "endpoints": results,
            "summary": {
                "total": len(results),
                "healthy": sum(1 for result in results if result["status"] == "healthy"),
                "unhealthy": sum(1 for result in results if result["status"] != "healthy"),
            },
        }

        with self.status_file.open("w", encoding="utf-8") as file:
            json.dump(status_data, file, indent=2)

    def run(self, endpoints: List[str], duration: Optional[int] = None) -> None:
        self.log_message(f"Starting health monitor for {self.base_url}")
        self.log_message(f"Monitoring endpoints: {', '.join(endpoints)}")
        self.log_message(f"Check interval: {self.check_interval} seconds")

        start_time = time.time()
        check_count = 0

        try:
            while True:
                check_count += 1
                self.log_message(f"--- Health Check #{check_count} ---")

                results = self.check_all_endpoints(endpoints)
                self.save_status(results)

                if duration and (time.time() - start_time) >= duration:
                    self.log_message("Monitoring duration completed")
                    break

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.log_message("Monitoring stopped by user", "INFO")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local API health monitor")
    parser.add_argument("--base-url", default="http://localhost:5000")
    parser.add_argument("--interval", type=int, default=5)
    parser.add_argument("--duration", type=int, default=45)
    parser.add_argument(
        "--endpoints",
        nargs="+",
        default=["/health", "/api/users", "/api/data"],
    )

    args = parser.parse_args()

    monitor = APIHealthMonitor(args.base_url, args.interval)
    monitor.run(args.endpoints, duration=args.duration)


if __name__ == "__main__":
    main()
