#!/bin/bash
set -e

# Path to the installed custom_modules
INSTALLED_CUSTOM_MODULES="/opt/venv/lib/python3.14/site-packages/pyrobud/custom_modules"
MOUNTED_CUSTOM_MODULES="/data/custom_modules"

# If /data/custom_modules exists and is not empty, use it instead of the built-in one
if [ -d "$MOUNTED_CUSTOM_MODULES" ] && [ "$(ls -A $MOUNTED_CUSTOM_MODULES)" ]; then
    echo "[ENTRYPOINT] Found mounted custom_modules directory"
    echo "[ENTRYPOINT] Replacing built-in custom_modules with mounted version"
    
    # Backup the original if it exists (first run only)
    if [ -d "$INSTALLED_CUSTOM_MODULES" ] && [ ! -L "$INSTALLED_CUSTOM_MODULES" ]; then
        echo "[ENTRYPOINT] Backing up built-in custom_modules to ${INSTALLED_CUSTOM_MODULES}.builtin"
        mv "$INSTALLED_CUSTOM_MODULES" "${INSTALLED_CUSTOM_MODULES}.builtin"
    elif [ -L "$INSTALLED_CUSTOM_MODULES" ]; then
        echo "[ENTRYPOINT] Removing existing symlink"
        rm "$INSTALLED_CUSTOM_MODULES"
    fi
    
    # Create symlink from installed location to mounted location
    echo "[ENTRYPOINT] Creating symlink: $INSTALLED_CUSTOM_MODULES -> $MOUNTED_CUSTOM_MODULES"
    ln -sf "$MOUNTED_CUSTOM_MODULES" "$INSTALLED_CUSTOM_MODULES"
    
    echo "[ENTRYPOINT] Custom modules will be loaded from mounted directory"
else
    echo "[ENTRYPOINT] No mounted custom_modules found, using built-in modules"
    
    # If symlink exists but mount is empty, restore the built-in version
    if [ -L "$INSTALLED_CUSTOM_MODULES" ]; then
        echo "[ENTRYPOINT] Restoring built-in custom_modules"
        rm "$INSTALLED_CUSTOM_MODULES"
        if [ -d "${INSTALLED_CUSTOM_MODULES}.builtin" ]; then
            mv "${INSTALLED_CUSTOM_MODULES}.builtin" "$INSTALLED_CUSTOM_MODULES"
        fi
    fi
fi

# Execute the CMD
echo "[ENTRYPOINT] Starting pyrobud..."
exec "$@"
