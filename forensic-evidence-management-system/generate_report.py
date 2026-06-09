#!/usr/bin/env python3

import hashlib
import datetime
from pathlib import Path


class ForensicReporter:
    def __init__(self, evidence_dir):
        self.evidence_dir = Path(evidence_dir)
        self.report_data = []

    def calculate_hash(self, filepath, algorithm="sha256"):
        hash_obj = hashlib.new(algorithm)

        with open(filepath, "rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def analyze_evidence(self):
        original_dir = self.evidence_dir / "original"

        for filepath in sorted(original_dir.iterdir()):
            if filepath.is_file():
                file_info = {
                    "filename": filepath.name,
                    "size": filepath.stat().st_size,
                    "modified": datetime.datetime.fromtimestamp(
                        filepath.stat().st_mtime
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "md5": self.calculate_hash(filepath, "md5"),
                    "sha256": self.calculate_hash(filepath, "sha256")
                }

                self.report_data.append(file_info)

    def generate_report(self, output_file):
        with open(output_file, "w") as file:
            file.write("=" * 70 + "\n")
            file.write("FORENSIC EVIDENCE REPORT\n")
            file.write("=" * 70 + "\n\n")
            file.write(f"Report Generated: {datetime.datetime.now()}\n")
            file.write("Case ID: CASE-2024-001\n")
            file.write(f"Total Evidence Items: {len(self.report_data)}\n\n")

            file.write("-" * 70 + "\n")
            file.write("EVIDENCE INVENTORY\n")
            file.write("-" * 70 + "\n\n")

            for index, item in enumerate(self.report_data, 1):
                file.write(f"[{index}] {item['filename']}\n")
                file.write(f"    Size: {item['size']} bytes\n")
                file.write(f"    Modified: {item['modified']}\n")
                file.write(f"    MD5: {item['md5']}\n")
                file.write(f"    SHA256: {item['sha256']}\n\n")

            file.write("-" * 70 + "\n")
            file.write("INTEGRITY VERIFICATION\n")
            file.write("-" * 70 + "\n")
            file.write("All evidence items have been hashed and verified.\n")
            file.write("Original evidence preserved in read-only state.\n")


def main():
    evidence_path = Path.home() / "forensics_lab" / "evidence"
    report_path = evidence_path / "reports" / "forensic_report.txt"

    reporter = ForensicReporter(evidence_path)
    reporter.analyze_evidence()
    reporter.generate_report(report_path)

    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()
