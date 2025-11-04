---
layout: default
title: Quick Start
nav_order: 3
---

# Module Dependency Management

Pyrobud now includes a powerful module-level dependency management system that allows modules to declare and automatically install their own pip dependencies without modifying the main `pyproject.toml`.

## Quick Start

### For Module Developers

Simply add the `@util.dependencies.requires()` decorator to your module:

```python
from pyrobud import command, module, util

@util.dependencies.requires('beautifulsoup4>=4.9.0', 'requests>=2.28.0')
class MyModule(module.Module):
    name = "MyModule"
    
    async def on_load(self) -> None:
        # Dependencies are now guaranteed to be installed
        from bs4 import BeautifulSoup
        import requests
        
        self.db = self.bot.get_db(self.name)
```

### For Bot Operators

No action needed! Dependencies are automatically installed when modules load for the first time. You'll see log messages indicating what's being installed.

## Features

✅ **Automatic Installation** - Dependencies are installed automatically when modules load  
✅ **Version Constraints** - Support for pip version specifiers (>=, ==, !=, etc.)  
✅ **Caching** - Avoids redundant checks and installations  
✅ **Thread-Safe** - Uses async locks to prevent race conditions  
✅ **Venv-Aware** - Automatically detects and uses your virtual environment  
✅ **Graceful Fallback** - Modules can handle missing optional dependencies  

## Benefits

### Before (Old Way)
- ❌ All dependencies in main `pyproject.toml`
- ❌ Main repo bloated with module-specific deps
- ❌ Hard to distribute individual modules
- ❌ Users install dependencies they don't need

### After (New Way)
- ✅ Each module declares its own dependencies
- ✅ Main repo stays lightweight
- ✅ Modules are self-contained and portable
- ✅ Dependencies installed only when needed

## Usage Examples

### 1. Required Dependencies (Decorator)

```python
@util.dependencies.requires('package1', 'package2>=1.0.0')
class MyModule(module.Module):
    name = "MyModule"
```

### 2. Manual Installation

```python
class MyModule(module.Module):
    name = "MyModule"
    
    async def on_load(self) -> None:
        await util.dependencies.ensure_installed(['package1', 'package2'])
        # Now safe to import
```

### 3. Optional Dependencies

```python
class MyModule(module.Module):
    name = "MyModule"
    has_opencv = False
    
    async def on_load(self) -> None:
        if await util.dependencies.ensure_installed('opencv-python'):
            self.has_opencv = True
```

## API Reference

See [DEPENDENCIES_GUIDE.md](DEPENDENCIES_GUIDE.md) for complete documentation.

## Examples

- **Basic Example**: `pyrobud/custom_modules/example_with_dependencies.py`
- **Real-World**: `pyrobud-modules/reverse_image_search.py`
- **Real-World**: `pyrobud-modules/toplist.py`

## Testing

Run the test script to verify the system works:

```bash
python test_dependencies.py
```

## Migrating Existing Modules

1. Add the `@util.dependencies.requires()` decorator
2. Remove dependencies from main `pyproject.toml` (optional)
3. Test module loads correctly

## Troubleshooting

- **Dependencies not installing?** Check logs for errors, verify package names
- **Import errors?** Some packages have different import names (e.g., `beautifulsoup4` → `bs4`)
- **Permission errors?** Ensure you're in a venv or have proper permissions

## Contributing

When contributing new modules, please use the dependency management system for any module-specific dependencies. Keep the main `pyproject.toml` for core dependencies only.
