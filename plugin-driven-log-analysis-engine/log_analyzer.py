#!/usr/bin/env python3
"""
Plugin-driven log analysis engine.

Loads analyzer plugins dynamically, processes log files line by line,
records findings, and exports structured JSON reports.
"""

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from plugin_loader import PluginLoader


class LogAnalyzer:
    """Main engine for analyzing logs using plugins."""

    def __init__(self, plugin_directory: str = "plugins"):
        self.loader = PluginLoader(plugin_directory)
        self.results = []
        self.files_processed = []

    def initialize(self) -> bool:
        print("\n=== Initializing Log Analysis Engine ===")
        count = self.loader.load_plugins()
        print(f"\nTotal plugins loaded: {count}\n")
        return count > 0

    def analyze_file(self, log_file: str) -> None:
        path = Path(log_file)
        print(f"[*] Analyzing log file: {path}")

        if not path.exists():
            print(f"[-] Error: Log file '{path}' not found")
            return

        file_findings_before = len(self.results)

        with path.open("r", encoding="utf-8", errors="replace") as file:
            for line_number, line in enumerate(file, 1):
                for plugin in self.loader.get_plugins():
                    result = plugin.analyze(line)

                    if result:
                        result["line_number"] = line_number
                        result["plugin"] = plugin.name
                        result["source_file"] = str(path)
                        result["timestamp"] = datetime.now().isoformat()
                        self.results.append(result)

        file_findings = len(self.results) - file_findings_before

        self.files_processed.append({
            "file": str(path),
            "findings": file_findings,
        })

        print(f"[+] Analysis complete for {path}. Found {file_findings} findings.")

    def generate_report(self, output_file: str = "output/report.json") -> None:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        severity_counts = Counter(result["severity"] for result in self.results)
        plugin_counts = Counter(result["plugin"] for result in self.results)

        report = {
            "analysis_date": datetime.now().isoformat(),
            "total_findings": len(self.results),
            "severity_counts": dict(severity_counts),
            "plugin_counts": dict(plugin_counts),
            "files_processed": self.files_processed,
            "plugins_loaded": self.loader.get_plugin_info(),
            "plugin_load_errors": self.loader.load_errors,
            "findings": self.results,
        }

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)

        print(f"\n[+] Report saved to: {output_path}")

        print("\n=== Analysis Summary ===")
        if severity_counts:
            for severity, count in sorted(severity_counts.items()):
                print(f"{severity}: {count} findings")
        else:
            print("No findings detected.")

        print("\n=== Findings by Plugin ===")
        if plugin_counts:
            for plugin, count in sorted(plugin_counts.items()):
                print(f"{plugin}: {count}")
        else:
            print("No plugin findings detected.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plugin-driven log analysis engine")
    parser.add_argument("--log-file", default="logs/sample.log", help="Log file to analyze")
    parser.add_argument("--plugin-dir", default="plugins", help="Plugin directory")
    parser.add_argument("--output", default="output/report.json", help="Output JSON report path")

    args = parser.parse_args()

    analyzer = LogAnalyzer(plugin_directory=args.plugin_dir)

    if not analyzer.initialize():
        print("[-] No plugins loaded. Exiting.")
        return

    analyzer.analyze_file(args.log_file)
    analyzer.generate_report(args.output)


if __name__ == "__main__":
    main()
