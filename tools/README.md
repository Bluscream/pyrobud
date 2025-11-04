# Pyrobud Tools

This directory contains utility scripts for building, running, and managing pyrobud.

## Scripts

### build.ps1

PowerShell script for building and publishing Docker images.

**Usage:**

```powershell
# Local build only (for testing)
.\tools\build.ps1

# Publish with patch version bump
.\tools\build.ps1 -Publish

# Publish with minor version bump
.\tools\build.ps1 -Publish -BumpType minor

# Publish with major version bump
.\tools\build.ps1 -Publish -BumpType major

# Publish current version without bumping (re-publish)
.\tools\build.ps1 -Publish -BumpType none

# Skip Git operations
.\tools\build.ps1 -Publish -SkipGit

# Skip specific registries
.\tools\build.ps1 -Publish -SkipDockerHub
.\tools\build.ps1 -Publish -SkipGHCR
```

**Features:**
- Version bumping (major, minor, patch, or none)
- Git commit and tagging
- Multi-platform Docker builds (linux/amd64, linux/arm64)
- Push to Docker Hub and GitHub Container Registry
- Automatic Docker Desktop startup
- Image verification after publishing

**Environment Variables:**
```powershell
# Docker Hub
$env:DOCKERHUB_TOKEN = "dckr_pat_YOUR_TOKEN"
$env:DOCKERHUB_USERNAME = "your-username"  # Optional, defaults to bluscream1

# GitHub Container Registry
$env:GITHUB_TOKEN = "ghp_YOUR_TOKEN"
$env:GITHUB_USERNAME = "your-username"  # Optional, defaults to Bluscream
```

### run.py

Standalone Python launcher that runs pyrobud without requiring pip install.

**Usage:**

```bash
# Run from project root
python tools/run.py

# Or make executable and run directly (Linux/Mac)
chmod +x tools/run.py
./tools/run.py
```

**Features:**
- Runs pyrobud directly from source
- No pip install required
- Automatically adds project to Python path
- Useful for development and testing

## Directory Structure

```
pyrobud/
├── tools/
│   ├── README.md      # This file
│   ├── build.ps1      # Docker build script
│   └── run.py         # Standalone launcher
├── pyrobud/           # Main package
├── pyproject.toml     # Project config
└── ...
```

## Notes

- All scripts are designed to work from the project root
- `build.ps1` automatically changes to project root directory
- `run.py` automatically finds project root from tools/

## Development

When adding new tools:
1. Place them in this directory
2. Update this README with usage info
3. Ensure they work from project root
4. Add executable permissions for shell scripts (Linux/Mac)

