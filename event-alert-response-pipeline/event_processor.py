#!/usr/bin/env python3
"""
Event Alert Response Processing Pipeline

Processes security events, applies YAML-based detection rules,
generates structured alerts, and records automated response actions.
"""

import argparse
import json
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class EventProcessor:
    def __init__(self, rules_file: str, alerts_dir: str = "alerts", responses_dir: str = "responses"):
        self.rules_file = Path(rules_file)
        self.alerts_dir = Path(alerts_dir)
        self.responses_dir = Path(responses_dir)
        self.alerts_dir.mkdir(parents=True, exist_ok=True)
        self.responses_dir.mkdir(parents=True, exist_ok=True)

        self.rules = self.load_rules(self.rules_file)
        self.event_counter = defaultdict(lambda: defaultdict(int))
        self.processed_events = []
        self.triggered_alerts = []
        self.executed_responses = []

    def load_rules(self, rules_file: Path) -> List[Dict]:
        if not rules_file.exists():
            raise FileNotFoundError(f"Rules file not found: {rules_file}")

        with rules_file.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not data or "rules" not in data:
            raise ValueError("Rules file must contain a top-level 'rules' key")

        required_fields = {"id", "name", "pattern", "threshold", "severity", "response"}

        for rule in data["rules"]:
            missing = required_fields - set(rule)
            if missing:
                raise ValueError(f"Rule is missing required fields: {missing}")

        return data["rules"]

    def parse_event(self, log_line: str) -> Optional[Dict]:
        try:
            parts = [part.strip() for part in log_line.strip().split("|")]

            if len(parts) < 4:
                return None

            return {
                "timestamp": parts[0],
                "source_ip": parts[1],
                "event_type": parts[2],
                "details": "|".join(parts[3:]).strip(),
                "raw_event": log_line.strip(),
            }

        except Exception as error:
            print(f"Error parsing event: {error}")
            return None

    def check_rules(self, event: Dict) -> List[Dict]:
        triggered = []

        for rule in self.rules:
            if rule["pattern"] in event["event_type"]:
                key = f"{event['source_ip']}_{rule['id']}"
                self.event_counter[key]["count"] += 1
                current_count = self.event_counter[key]["count"]

                if current_count >= rule["threshold"]:
                    enriched_rule = dict(rule)
                    enriched_rule["current_count"] = current_count
                    triggered.append(enriched_rule)

        return triggered

    def generate_alert(self, event: Dict, rule: Dict) -> Dict:
        alert = {
            "alert_time": datetime.now().isoformat(),
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "severity": rule["severity"],
            "threshold": rule["threshold"],
            "current_count": rule.get("current_count", 1),
            "source_ip": event["source_ip"],
            "event_type": event["event_type"],
            "details": event["details"],
            "raw_event": event["raw_event"],
        }

        filename = self.alerts_dir / f"alert_{rule['id']}_{event['source_ip'].replace('.', '_')}_{int(time.time() * 1000)}.json"

        with filename.open("w", encoding="utf-8") as file:
            json.dump(alert, file, indent=2)

        self.triggered_alerts.append(alert)

        print(f"[ALERT] {rule['severity']} - {rule['name']} from {event['source_ip']}")

        return alert

    def execute_response(self, event: Dict, rule: Dict) -> Dict:
        response_action = rule["response"]

        response_log = {
            "timestamp": datetime.now().isoformat(),
            "action": response_action,
            "source_ip": event["source_ip"],
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "severity": rule["severity"],
            "status": "simulated",
        }

        filename = self.responses_dir / f"response_{rule['id']}_{event['source_ip'].replace('.', '_')}_{int(time.time() * 1000)}.json"

        with filename.open("w", encoding="utf-8") as file:
            json.dump(response_log, file, indent=2)

        self.executed_responses.append(response_log)

        if response_action == "block_ip":
            print(f"[RESPONSE] Simulated IP block: {event['source_ip']}")
        elif response_action == "alert_admin":
            print(f"[RESPONSE] Simulated admin alert for {event['source_ip']}")
        elif response_action == "log_only":
            print(f"[RESPONSE] Logged event from {event['source_ip']}")
        elif response_action == "isolate_host":
            print(f"[RESPONSE] Simulated host isolation for {event['source_ip']}")
        else:
            print(f"[RESPONSE] Unknown response action: {response_action}")

        return response_log

    def process_event(self, log_line: str) -> None:
        event = self.parse_event(log_line)

        if not event:
            return

        self.processed_events.append(event)

        triggered_rules = self.check_rules(event)

        for rule in triggered_rules:
            self.generate_alert(event, rule)
            self.execute_response(event, rule)

    def process_file_once(self, log_file: str) -> None:
        path = Path(log_file)

        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    self.process_event(line)

    def write_summary(self, output_file: str = "output/pipeline_summary.json") -> None:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        severity_counts = Counter(alert["severity"] for alert in self.triggered_alerts)
        response_counts = Counter(response["action"] for response in self.executed_responses)

        summary = {
            "generated_at": datetime.now().isoformat(),
            "rules_loaded": len(self.rules),
            "events_processed": len(self.processed_events),
            "alerts_generated": len(self.triggered_alerts),
            "responses_executed": len(self.executed_responses),
            "severity_counts": dict(severity_counts),
            "response_counts": dict(response_counts),
            "alerts": self.triggered_alerts,
            "responses": self.executed_responses,
        }

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(summary, file, indent=2)

        print(f"[+] Summary written to {output_path}")


def monitor_file(processor: EventProcessor, log_file: str, poll_interval: float = 1.0) -> None:
    path = Path(log_file)
    path.touch(exist_ok=True)

    print(f"Monitoring {path} for events...")
    print("Press Ctrl+C to stop\n")

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                processor.process_event(line)

        while True:
            line = file.readline()
            if line:
                processor.process_event(line)
            else:
                time.sleep(poll_interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Event alert response processing pipeline")
    parser.add_argument("--rules", default="rules/security_rules.yaml")
    parser.add_argument("--log-file", default="logs/security_events.log")
    parser.add_argument("--mode", choices=["once", "monitor"], default="once")
    parser.add_argument("--summary", default="output/pipeline_summary.json")

    args = parser.parse_args()

    print("=== Security Event Processing Pipeline ===")
    print("Initializing processor...")

    processor = EventProcessor(args.rules)

    if args.mode == "once":
        processor.process_file_once(args.log_file)
        processor.write_summary(args.summary)
    else:
        try:
            monitor_file(processor, args.log_file)
        except KeyboardInterrupt:
            print("\nShutting down processor...")
            processor.write_summary(args.summary)


if __name__ == "__main__":
    main()
