"""Utility for managing per-module dependencies."""
import asyncio
import importlib
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from . import system

log = logging.getLogger("dependencies")

# Track installed packages to avoid redundant checks
_installed_packages: Set[str] = set()
_installation_lock = asyncio.Lock()


def _normalize_package_name(name: str) -> str:
    """Normalize package name for comparison (e.g., 'beautifulsoup4' -> 'bs4')."""
    # Common package name mappings
    mappings = {
        "beautifulsoup4": "bs4",
        "pillow": "PIL",
        "python-telegram-bot": "telegram",
        "opencv-python": "cv2",
        "pyyaml": "yaml",
        "python-dateutil": "dateutil",
    }
    return mappings.get(name.lower(), name)


def is_package_installed(package: str) -> bool:
    """Check if a package is installed and importable."""
    if package in _installed_packages:
        return True
    
    # Try to import the package
    import_name = _normalize_package_name(package)
    try:
        importlib.import_module(import_name)
        _installed_packages.add(package)
        return True
    except ImportError:
        return False


async def install_package(
    package: str,
    version: Optional[str] = None,
    upgrade: bool = False
) -> bool:
    """
    Install a Python package using pip.
    
    Args:
        package: Package name (e.g., 'beautifulsoup4', 'requests')
        version: Optional version specifier (e.g., '>=4.0.0', '==1.2.3')
        upgrade: Whether to upgrade if already installed
    
    Returns:
        True if installation succeeded, False otherwise
    """
    async with _installation_lock:
        # Build package specifier
        pkg_spec = package
        if version:
            pkg_spec = f"{package}{version}"
        
        # Determine pip path
        venv_path = system.get_venv_path()
        if venv_path:
            pip_cmd = str(Path(venv_path) / "bin" / "pip")
        else:
            pip_cmd = sys.executable
            pip_args = ["-m", "pip"]
        
        # Build command
        if venv_path:
            cmd_args = [pip_cmd, "install"]
        else:
            cmd_args = [pip_cmd] + pip_args + ["install"]
        
        if upgrade:
            cmd_args.append("--upgrade")
        
        cmd_args.append(pkg_spec)
        
        log.info(f"Installing package: {pkg_spec}")
        
        try:
            stdout, stderr, ret = await system.run_command(*cmd_args, timeout=300)
            
            if ret == 0:
                log.info(f"Successfully installed {pkg_spec}")
                _installed_packages.add(package)
                return True
            else:
                log.error(f"Failed to install {pkg_spec}: {stderr or stdout}")
                return False
        except Exception as e:
            log.error(f"Error installing {pkg_spec}: {e}")
            return False


async def ensure_installed(
    packages: Union[str, List[str], Dict[str, str]],
    upgrade: bool = False
) -> bool:
    """
    Ensure packages are installed, installing them if necessary.
    
    Args:
        packages: Package name(s) to ensure are installed. Can be:
            - A single package name: 'beautifulsoup4'
            - A list of packages: ['beautifulsoup4', 'requests']
            - A dict mapping package to version: {'beautifulsoup4': '>=4.0.0'}
        upgrade: Whether to upgrade packages if already installed
    
    Returns:
        True if all packages are installed/installed successfully
    
    Examples:
        await ensure_installed('beautifulsoup4')
        await ensure_installed(['bs4', 'requests', 'lxml'])
        await ensure_installed({'beautifulsoup4': '>=4.0.0', 'requests': '>=2.0.0'})
    """
    # Normalize input to dict
    if isinstance(packages, str):
        packages = {packages: None}
    elif isinstance(packages, list):
        packages = {pkg: None for pkg in packages}
    
    missing_packages = []
    
    # Check which packages need installation
    for package, version in packages.items():
        if upgrade or not is_package_installed(package):
            missing_packages.append((package, version))
    
    if not missing_packages:
        log.debug(f"All packages already installed: {list(packages.keys())}")
        return True
    
    # Install missing packages
    log.info(f"Installing {len(missing_packages)} package(s): {[p[0] for p in missing_packages]}")
    
    results = []
    for package, version in missing_packages:
        success = await install_package(package, version, upgrade)
        results.append(success)
    
    return all(results)


def requires(*packages: str):
    """
    Decorator to ensure packages are installed before module loads.
    
    Usage:
        @requires('beautifulsoup4', 'requests', 'lxml')
        class MyModule(module.Module):
            ...
    
    Or with versions:
        @requires('beautifulsoup4>=4.0.0', 'requests>=2.0.0')
        class MyModule(module.Module):
            ...
    """
    def decorator(cls):
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            # Store requirements on the instance
            self._required_packages = packages
            original_init(self, *args, **kwargs)
        
        cls.__init__ = new_init
        
        # Add on_load hook if not exists
        if not hasattr(cls, 'on_load') or cls.on_load is Module.on_load:
            async def on_load(self):
                await _ensure_module_deps(self)
        else:
            original_on_load = cls.on_load
            async def on_load(self):
                await _ensure_module_deps(self)
                await original_on_load(self)
        
        cls.on_load = on_load
        return cls
    
    return decorator


async def _ensure_module_deps(module_instance) -> None:
    """Internal helper to ensure module dependencies are installed."""
    if not hasattr(module_instance, '_required_packages'):
        return
    
    packages = module_instance._required_packages
    if not packages:
        return
    
    # Parse package specs
    pkg_dict = {}
    for pkg_spec in packages:
        # Split on common version operators
        for op in ['>=', '<=', '==', '!=', '~=', '>', '<']:
            if op in pkg_spec:
                pkg_name, version = pkg_spec.split(op, 1)
                pkg_dict[pkg_name.strip()] = op + version.strip()
                break
        else:
            pkg_dict[pkg_spec.strip()] = None
    
    module_name = type(module_instance).__name__
    log.info(f"Module '{module_name}' requires: {list(pkg_dict.keys())}")
    
    success = await ensure_installed(pkg_dict)
    
    if not success:
        log.warning(f"Failed to install some dependencies for module '{module_name}'")


# For backwards compatibility with Module base class
class Module:
    """Stub for type checking."""
    async def on_load(self):
        pass
