---
layout: default
title: Dependencies Guide
nav_order: 2
---

# Module Dependencies Guide

This guide explains how to manage per-module dependencies in pyrobud without modifying the main `pyproject.toml`.

## Overview

Pyrobud now includes a dependency management system that allows modules to declare and automatically install their own pip dependencies. This keeps the main project lightweight and allows modules to be truly self-contained.

## Usage Methods

### Method 1: Using the `@requires` Decorator (Recommended)

The simplest way to declare dependencies is using the `@requires` decorator:

```python
from pyrobud import command, module, util

@util.dependencies.requires('beautifulsoup4', 'requests', 'lxml')
class MyModule(module.Module):
    name = "MyModule"

    # Dependencies will be automatically installed before on_load is called
    async def on_load(self) -> None:
        # Now safe to import
        from bs4 import BeautifulSoup
        import requests

        self.db = self.bot.get_db(self.name)
```

**With version constraints:**

```python
@util.dependencies.requires('beautifulsoup4>=4.0.0', 'requests>=2.28.0', 'lxml')
class MyModule(module.Module):
    name = "MyModule"
```

### Method 2: Manual Installation in `on_load`

For more control, you can manually ensure dependencies are installed:

```python
from pyrobud import command, module, util

class MyModule(module.Module):
    name = "MyModule"

    async def on_load(self) -> None:
        # Install dependencies if needed
        await util.dependencies.ensure_installed(['beautifulsoup4', 'requests'])

        # Now safe to import
        from bs4 import BeautifulSoup
        import requests

        self.db = self.bot.get_db(self.name)
```

**With version constraints:**

```python
async def on_load(self) -> None:
    await util.dependencies.ensure_installed({
        'beautifulsoup4': '>=4.0.0',
        'requests': '>=2.28.0'
    })
```

### Method 3: Graceful Fallback (Optional Dependencies)

If your module can work without certain dependencies, check for them gracefully:

```python
from pyrobud import command, module, util

class MyModule(module.Module):
    name = "MyModule"
    has_advanced_features = False

    async def on_load(self) -> None:
        self.db = self.bot.get_db(self.name)

        # Try to install optional dependencies
        if await util.dependencies.ensure_installed(['opencv-python']):
            self.has_advanced_features = True
            self.log.info("Advanced features enabled")
        else:
            self.log.warning("OpenCV not available, some features disabled")

    @command.desc("Process image")
    async def cmd_process(self, ctx: command.Context) -> str:
        if not self.has_advanced_features:
            return "⚠️ This feature requires opencv-python"

        import cv2
        # ... your code here
```

## API Reference

### `@util.dependencies.requires(*packages)`

Decorator to ensure packages are installed before module loads.

**Parameters:**

- `*packages`: Variable number of package specifications (e.g., `'requests'`, `'beautifulsoup4>=4.0.0'`)

**Example:**

```python
@util.dependencies.requires('numpy', 'pandas>=1.0.0', 'matplotlib')
class DataAnalysisModule(module.Module):
    pass
```

### `await util.dependencies.ensure_installed(packages, upgrade=False)`

Ensure packages are installed, installing them if necessary.

**Parameters:**

- `packages`: Can be:
  - A single package name: `'beautifulsoup4'`
  - A list of packages: `['beautifulsoup4', 'requests']`
  - A dict mapping package to version: `{'beautifulsoup4': '>=4.0.0'}`
- `upgrade`: Whether to upgrade packages if already installed (default: `False`)

**Returns:** `True` if all packages are installed successfully, `False` otherwise

**Examples:**

```python
# Single package
await util.dependencies.ensure_installed('beautifulsoup4')

# Multiple packages
await util.dependencies.ensure_installed(['bs4', 'requests', 'lxml'])

# With version constraints
await util.dependencies.ensure_installed({
    'beautifulsoup4': '>=4.0.0',
    'requests': '>=2.28.0'
})

# Upgrade existing packages
await util.dependencies.ensure_installed(['requests'], upgrade=True)
```

### `util.dependencies.is_package_installed(package)`

Check if a package is already installed and importable.

**Parameters:**

- `package`: Package name to check

**Returns:** `True` if package is installed, `False` otherwise

**Example:**

```python
if util.dependencies.is_package_installed('opencv-python'):
    import cv2
    # ... use cv2
```

## Common Package Name Mappings

Some packages have different pip install names vs. import names:

| Install Name        | Import Name |
| ------------------- | ----------- |
| beautifulsoup4      | bs4         |
| pillow              | PIL         |
| python-telegram-bot | telegram    |
| opencv-python       | cv2         |
| pyyaml              | yaml        |
| python-dateutil     | dateutil    |

The dependency system automatically handles these common mappings.

## Best Practices

1. **Use the decorator for required dependencies**: If your module absolutely needs certain packages, use `@requires` decorator.

2. **Keep imports inside methods for optional deps**: If dependencies are optional or conditionally needed:

   ```python
   async def cmd_advanced(self, ctx: command.Context):
       if not self.has_opencv:
           return "Feature not available"

       import cv2  # Import only when needed
       # ... your code
   ```

3. **Provide user feedback**: Let users know what's happening:

   ```python
   async def on_load(self) -> None:
       self.log.info("Installing required dependencies...")
       await util.dependencies.ensure_installed(['package1', 'package2'])
       self.log.info("Dependencies installed successfully")
   ```

4. **Handle installation failures gracefully**: Some environments might not allow pip installs:
   ```python
   async def on_load(self) -> None:
       success = await util.dependencies.ensure_installed(['package1'])
       if not success:
           self.log.error("Failed to install dependencies. Please install manually: pip install package1")
           # Consider disabling certain features or raising an error
   ```

## Troubleshooting

### Dependencies not installing

If dependencies aren't installing automatically:

1. Check you're running in a venv or have pip available
2. Check the logs for error messages
3. Try installing manually: `pip install package-name`
4. Check if the package name is correct on PyPI

### Import errors after installation

If packages install but imports fail:

1. The package might have a different import name (see mappings table above)
2. Try importing with the correct name
3. Check if the package requires additional system dependencies

### Permission errors

If you get permission errors during installation:

1. Make sure you're running in a virtual environment
2. Or run the bot with appropriate permissions
3. Consider pre-installing dependencies manually

## Example: Complete Module with Dependencies

```python
from pyrobud import command, module, util
import telethon as tg

@util.dependencies.requires('beautifulsoup4>=4.9.0', 'requests>=2.28.0')
class WebScraperModule(module.Module):
    name = "WebScraper"

    async def on_load(self) -> None:
        """Initialize the module."""
        # Dependencies are already installed by the decorator
        from bs4 import BeautifulSoup
        import requests

        self.db = self.bot.get_db(self.name)
        self.log.info("WebScraper module loaded with dependencies")

    @command.desc("Scrape a website")
    @command.usage("[URL]")
    async def cmd_scrape(self, ctx: command.Context) -> str:
        """Scrape content from a URL."""
        # Safe to import here since dependencies are guaranteed
        from bs4 import BeautifulSoup
        import requests

        if not ctx.input:
            return "⚠️ Please provide a URL"

        try:
            response = requests.get(ctx.input, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.find('title')
            return f"Page title: {title.string if title else 'No title found'}"
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
```
