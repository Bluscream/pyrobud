---
layout: default
title: Home
nav_order: 1
---

# Pyrobud Documentation

Welcome to the Pyrobud documentation! Pyrobud is a clean selfbot for Telegram with an emphasis on quality and practicality.

## Quick Links

- [Getting Started](../README.md)
- [Module Dependencies Guide](dependencies.md)
- [Development Guide](../DEVELOPMENT.md)
- [Contributing](../CONTRIBUTING.md)

## What's New

### Module Dependency Management System

Pyrobud now includes a powerful module-level dependency management system that allows modules to declare and automatically install their own pip dependencies without modifying the main `pyproject.toml`.

**Quick example:**

```python
from pyrobud import command, module, util

@util.dependencies.requires('beautifulsoup4>=4.9.0', 'requests>=2.28.0')
class MyModule(module.Module):
    name = "MyModule"

    async def on_load(self) -> None:
        # Dependencies are now guaranteed to be installed!
        from bs4 import BeautifulSoup
        import requests
        self.db = self.bot.get_db(self.name)
```

[Learn more about module dependencies →](dependencies.md)

## Features

- **Modular Architecture**: Easy to extend with custom modules
- **Async/Await**: Built on modern Python async patterns
- **Database Support**: Built-in LevelDB support for persistent storage
- **Command System**: Powerful command framework with aliases and usage info
- **Event Listeners**: React to Telegram events easily
- **Auto Dependencies**: Modules can declare their own dependencies
- **Docker Support**: Ready-to-use Docker images
- **Type Hints**: Fully typed for better IDE support

## Documentation Structure

- **[dependencies.md](dependencies.md)** - Complete guide to the module dependency system
- **[quick-start.md](quick-start.md)** - Quick start guide for dependency management
- **[implementation.md](implementation.md)** - Technical implementation details

## Getting Help

- [GitHub Issues](https://github.com/Bluscream/pyrobud/issues)
- [Telegram Community](https://t.me/pyrobud)
- [Original Project](https://github.com/kdrag0n/pyrobud)

## Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details.

## License

Pyrobud is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
