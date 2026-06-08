"""
Dynamic plugin loader for the log analysis engine.
"""

import importlib.util
from pathlib import Path
from typing import List


class PluginLoader:
    """Loads and manages analyzer plugins dynamically."""

    def __init__(self, plugin_directory: str = "plugins"):
        self.plugin_directory = Path(plugin_directory)
        self.plugins = []
        self.load_errors = []

    def load_plugins(self) -> int:
        if not self.plugin_directory.exists():
            print(f"Plugin directory '{self.plugin_directory}' not found")
            return 0

        loaded_count = 0

        for plugin_path in sorted(self.plugin_directory.glob("*_analyzer.py")):
            try:
                module_name = plugin_path.stem
                spec = importlib.util.spec_from_file_location(module_name, plugin_path)

                if spec is None or spec.loader is None:
                    raise ImportError(f"Could not create import spec for {plugin_path}")

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if not hasattr(module, "get_plugin"):
                    raise AttributeError("Plugin does not define get_plugin()")

                plugin_instance = module.get_plugin()

                if not hasattr(plugin_instance, "analyze"):
                    raise AttributeError("Plugin instance does not define analyze()")

                self.plugins.append(plugin_instance)
                loaded_count += 1
                print(f"[+] Loaded plugin: {plugin_instance.name}")

            except Exception as error:
                message = f"Failed to load {plugin_path.name}: {error}"
                self.load_errors.append(message)
                print(f"[-] {message}")

        return loaded_count

    def get_plugins(self) -> List:
        return self.plugins

    def get_plugin_info(self) -> List[dict]:
        return [plugin.get_info() for plugin in self.plugins]
