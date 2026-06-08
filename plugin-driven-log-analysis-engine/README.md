# Plugin-Driven Log Analysis Engine

## What This Does

This implementation provides a plugin-driven log analysis engine for modular security detection. It dynamically loads analyzer plugins from a plugin directory, runs each plugin against log entries, detects security and operational patterns, and exports structured JSON reports with severity counts, plugin counts, loaded plugin metadata, findings, and load-error tracking.

The engine is designed so new detection logic can be added without modifying the core analyzer. A new plugin can be dropped into the plugins directory, and the engine discovers and executes it automatically if it follows the required plugin interface.

This type of architecture is used in SIEM platforms, EDR systems, detection engineering pipelines, threat hunting tools, incident response automation, and enterprise security analytics products.

## Architecture

    +-----------------------------+
    | Log Sources                  |
    | logs/sample.log              |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Core Analysis Engine         |
    | log_analyzer.py              |
    | - Reads log lines            |
    | - Runs loaded plugins        |
    | - Tracks findings            |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Dynamic Plugin Loader        |
    | plugin_loader.py             |
    | - Discovers *_analyzer.py    |
    | - Loads modules dynamically  |
    | - Validates plugin interface |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Analyzer Plugins             |
    | failed_login_analyzer.py     |
    | error_pattern_analyzer.py    |
    | warning_analyzer.py          |
    | privilege_escalation         |
    | service_restart_analyzer.py  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report Output       |
    | output/report.json           |
    | output/report_with_extension |
    | - Severity counts            |
    | - Plugin counts              |
    | - Finding details            |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-venv tree git

mkdir -p ~/plugin-log-analysis-engine/{plugins,logs,output}

cd ~/plugin-log-analysis-engine

touch plugins/__init__.py

## How to Reproduce

Run the analyzer with the default sample log:

python3 log_analyzer.py

View the generated JSON report:

python3 -m json.tool output/report.json

View severity and plugin summary:

python3 << 'PY'
import json

with open("output/report.json", "r", encoding="utf-8") as file:
    report = json.load(file)

print("Total findings:", report["total_findings"])
print("Severity counts:", report["severity_counts"])
print("Plugin counts:", report["plugin_counts"])
PY

Add a new plugin at runtime:

cat > plugins/service_restart_analyzer.py << 'PY'
from plugin_base import PluginBase

class ServiceRestartAnalyzer(PluginBase):
    def __init__(self):
        super().__init__()
        self.name = "Service Restart Analyzer"
        self.description = "Detects service restart events"
        self.severity = "LOW"

    def analyze(self, log_line: str) -> dict:
        if "service restarted" in log_line.lower():
            return {
                "severity": self.severity,
                "message": "Service restart detected",
                "details": {"log_line": log_line.strip()},
            }
        return None

def get_plugin():
    return ServiceRestartAnalyzer()
PY

Rerun the analyzer with the extension plugin:

python3 log_analyzer.py --output output/report_with_extension.json

Verify loaded plugins:

python3 << 'PY'
import json

with open("output/report_with_extension.json", "r", encoding="utf-8") as file:
    report = json.load(file)

for plugin in report["plugins_loaded"]:
    print(plugin["name"])
PY

Verify Python syntax:

python3 -m py_compile plugin_base.py plugin_loader.py log_analyzer.py plugins/*.py

Review file tree:

tree .

## Tools Used

- Python 3
- importlib
- pathlib
- JSON
- regular expressions
- Counter
- dynamic module loading
- Bash
- Linux
- tree
- Git

## Key Skills Demonstrated

- Plugin architecture design
- Dynamic module loading
- Security detection engineering
- Log analysis automation
- Extensible analyzer development
- Interface validation
- Failed login detection
- Error pattern detection
- Warning detection
- Privilege escalation detection
- Runtime plugin extension
- Structured JSON reporting
- Severity aggregation
- Plugin-level finding counts
- Load-error tracking
- SIEM-style architecture fundamentals

## Real-World Use Case

A security engineering team can use this architecture as the foundation for a modular detection engine. For example, one plugin can detect failed SSH logins, another can detect privilege escalation, another can detect suspicious process launches, and another can detect cloud audit log anomalies. New detections can be added by creating new plugin files instead of editing the core engine, which is how scalable SIEM, EDR, and detection engineering systems are commonly designed.

## Lessons Learned

- Plugin architectures make security tools easier to extend without changing core engine logic.
- Dynamic module loading should validate that plugins expose the expected entry point and analyzer interface.
- Detection results are more useful when reports include severity counts, plugin counts, source file names, and line numbers.
- Avoiding fragile sys.path manipulation makes dynamic imports more predictable.
- Adding a plugin at runtime proves that the architecture supports extension without rewriting the engine.

## Troubleshooting Log

Issue:
The original plugin examples used sys.path.append('..'), which can break depending on the execution directory.

Resolution:
Removed fragile path manipulation and imported plugin_base directly from the root execution directory.

Issue:
The original plugin loader assumed every plugin had get_plugin() and did not validate the returned object.

Resolution:
Added validation to confirm get_plugin() exists and the plugin instance has an analyze() method.

Issue:
The original report only stored findings and did not summarize detection coverage.

Resolution:
Added severity_counts, plugin_counts, files_processed, plugins_loaded, and plugin_load_errors to the JSON report.

Issue:
The base implementation only included failed login and generic error detection.

Resolution:
Added warning detection, privilege escalation detection, and runtime extension testing with a service restart detector.

Issue:
The original engine analyzed only one fixed file and output path.

Resolution:
Added CLI arguments for --log-file, --plugin-dir, and --output.
