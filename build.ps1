
#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build and optionally publish pyrobud Docker images to Docker Hub and GHCR
.DESCRIPTION
    This script builds Docker images for pyrobud.
    
    Without -Publish flag:
    - Only builds Docker images locally (linux/amd64)
    - No version bumping, no git operations
    - Safe for testing
    
    With -Publish flag:
    - Bumps version in pyproject.toml and pyrobud/version.py
    - Commits and tags the version in git
    - Builds multi-platform Docker images (linux/amd64, linux/arm64)
    - Pushes to Docker Hub (bluscream1/pyrobud) and GHCR (ghcr.io/bluscream/pyrobud)
    - Pushes commits and tags to git
.PARAMETER BumpType
    Version bump type: patch (default), minor, major, or none (only used with -Publish)
    - none: Skip version bumping, use current version
.PARAMETER Publish
    Bump version, commit/tag/push git, and push images to registries
.PARAMETER SkipGit
    Skip git commit and tag operations (only when -Publish is used)
.PARAMETER SkipDockerHub
    Skip pushing to Docker Hub (only when -Publish is used)
.PARAMETER SkipGHCR
    Skip pushing to GitHub Container Registry (only when -Publish is used)
.EXAMPLE
    .\build.ps1
    Build locally only, no changes to version or git
.EXAMPLE
    .\build.ps1 -Publish
    Bump patch version, commit, tag, push git, and publish images
.EXAMPLE
    .\build.ps1 -Publish -BumpType minor
    Bump minor version and publish
.EXAMPLE
    .\build.ps1 -Publish -BumpType none
    Publish current version without bumping (re-publish)
.EXAMPLE
    .\build.ps1 -Publish -SkipGit
    Publish without git operations (for testing)
#>

param(
    [ValidateSet("patch", "minor", "major", "none")]
    [string]$BumpType = "patch",
    [switch]$Publish,
    [switch]$SkipGit,
    [switch]$SkipDockerHub,
    [switch]$SkipGHCR
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Colors for output
function Write-Header { param($msg) Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Yellow }

# Get current version from pyproject.toml
function Get-CurrentVersion {
    $content = Get-Content "pyproject.toml" -Raw
    if ($content -match 'version\s*=\s*"([^"]+)"') {
        return $matches[1]
    }
    throw "Could not find version in pyproject.toml"
}

# Bump version
function Update-Version {
    param([string]$type)
    
    $current = Get-CurrentVersion
    Write-Info "Current version: $current"
    
    $parts = $current.Split('.')
    switch ($type) {
        "major" { $parts[0] = [int]$parts[0] + 1; $parts[1] = 0; $parts[2] = 0 }
        "minor" { $parts[1] = [int]$parts[1] + 1; $parts[2] = 0 }
        "patch" { $parts[2] = [int]$parts[2] + 1 }
    }
    
    $newVersion = $parts -join '.'
    Write-Info "New version: $newVersion ($type bump)"
    
    # Update pyproject.toml (only the main version line, not dependency versions)
    $content = Get-Content "pyproject.toml" -Raw
    # Match only: version = "X.X.X" at the start of a line (after optional whitespace)
    $content = $content -replace '(?m)^version\s*=\s*"[^"]+"', "version = `"$newVersion`""
    Set-Content "pyproject.toml" -Value $content -NoNewline
    Write-Success "Updated pyproject.toml to version $newVersion"
    
    # Update pyrobud/version.py
    $versionPyPath = "pyrobud\version.py"
    if (Test-Path $versionPyPath) {
        $versionContent = Get-Content $versionPyPath -Raw
        $versionContent = $versionContent -replace '__version__\s*=\s*"[^"]+"', "__version__ = `"$newVersion`""
        Set-Content $versionPyPath -Value $versionContent -NoNewline
        Write-Success "Updated pyrobud\version.py to version $newVersion"
    }
    else {
        Write-Error "pyrobud\version.py not found at $versionPyPath"
    }
    
    return $newVersion
}

# Main script
try {
    Write-Header "PYROBUD BUILD SCRIPT"
    
    # Step 1: Version Management (only when publishing)
    if ($Publish) {
        if ($BumpType -eq "none") {
            Write-Header "STEP 1: VERSION CHECK"
            $version = Get-CurrentVersion
            Write-Info "Using current version: $version (bump skipped)"
        } else {
            Write-Header "STEP 1: VERSION BUMP"
            $version = Update-Version -type $BumpType
        }
        
        # Step 2: Git Operations
        if (-not $SkipGit) {
            Write-Header "STEP 2: GIT COMMIT & TAG"
            
            # Get current branch name
            $currentBranch = git rev-parse --abbrev-ref HEAD 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to get current git branch"
            }
            Write-Info "Current branch: $currentBranch"
            
            # Check for uncommitted changes
            $status = git status --porcelain 2>&1
            
            if ($status) {
                Write-Info "Found uncommitted changes, adding all files..."
                git add -A 2>&1 | Out-Host
                $exitCode = $LASTEXITCODE
                Write-Host "Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
                
                $commitMessage = if ($BumpType -ne "none") {
                    "chore: bump version to $version"
                } else {
                    "chore: rebuild version $version"
                }
                
                git commit -m $commitMessage 2>&1 | Out-Host
                $exitCode = $LASTEXITCODE
                Write-Host "Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
            } else {
                Write-Info "No uncommitted changes to commit"
            }
            
            # Check if tag already exists
            $tagExists = git tag -l "v$version" 2>&1
            if ($tagExists) {
                Write-Info "Tag v$version already exists, skipping tag creation"
            } else {
                git tag -a "v$version" -m "Release v$version" 2>&1 | Out-Host
                $exitCode = $LASTEXITCODE
                Write-Host "Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
            }
            
            git push origin $currentBranch 2>&1 | Out-Host
            $exitCode = $LASTEXITCODE
            Write-Host "Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
            
            # Push tag (will show "Everything up-to-date" if already exists remotely)
            git push origin "v$version" 2>&1 | Out-Host
            $exitCode = $LASTEXITCODE
            Write-Host "Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
            
            Write-Success "Committed and tagged version $version"
        }
        else {
            Write-Info "Git operations skipped"
        }
    }
    else {
        $version = Get-CurrentVersion
        Write-Info "Local build mode - using current version: $version"
        Write-Info "No version bump or git operations (use -Publish to publish)"
    }
    
    # Step 3: Docker Build
    Write-Header "STEP 3: DOCKER BUILD"
    
    if ($Publish) {
        Write-Info "Mode: BUILD + PUBLISH"
        Write-Info "Platforms: linux/amd64, linux/arm64"
        Write-Info "Docker Hub: bluscream1/pyrobud:$version, bluscream1/pyrobud:latest"
        Write-Info "GHCR: ghcr.io/bluscream/pyrobud:$version, ghcr.io/bluscream/pyrobud:latest"
    }
    else {
        Write-Info "Mode: LOCAL BUILD ONLY"
        Write-Info "Platform: linux/amd64 only"
    }
    
    # Login to registries if publishing
    if ($Publish) {
        Write-Info "Logging in to Docker registries..."
        
        # Docker Hub login
        if (-not $SkipDockerHub) {
            Write-Info "Logging in to Docker Hub..."
            
            if ($env:DOCKERHUB_TOKEN) {
                # Use token authentication - force lowercase for Docker Hub
                # Check both DOCKERHUB_USERNAME and DOCKER_USERNAME for compatibility
                $dockerUsername = if ($env:DOCKERHUB_USERNAME) { 
                    $env:DOCKERHUB_USERNAME.ToLower() 
                } elseif ($env:DOCKER_USERNAME) { 
                    $env:DOCKER_USERNAME.ToLower() 
                } else { 
                    "bluscream1" 
                }
                Write-Info "Using token authentication for user: $dockerUsername"
                $env:DOCKERHUB_TOKEN | docker login -u $dockerUsername --password-stdin 2>&1 | Out-Host
            }
            else {
                # Interactive login
                Write-Info "No DOCKERHUB_TOKEN found, using interactive login..."
                docker login 2>&1 | Out-Host
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Logged in to Docker Hub"
            }
            else {
                Write-Error "Docker Hub login failed!"
                Write-Info "Set credentials using:"
                Write-Info '  $env:DOCKERHUB_TOKEN = "dckr_pat_YOUR_TOKEN"'
                Write-Info '  $env:DOCKERHUB_USERNAME = "your-username" (optional, defaults to bluscream1)'
                throw "Docker Hub login failed"
            }
        }
        
        # GHCR login
        if (-not $SkipGHCR) {
            Write-Info "Logging in to GitHub Container Registry..."
            
            if ($env:GITHUB_TOKEN) {
                # Use token authentication
                $ghUsername = if ($env:GITHUB_USERNAME) { $env:GITHUB_USERNAME } else { "Bluscream" }
                Write-Info "Using token authentication for user: $ghUsername"
                $env:GITHUB_TOKEN | docker login ghcr.io -u $ghUsername --password-stdin 2>&1 | Out-Host
            }
            else {
                # Interactive login
                Write-Info "No GITHUB_TOKEN found, using interactive login..."
                docker login ghcr.io -u Bluscream 2>&1 | Out-Host
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Logged in to GHCR"
            }
            else {
                Write-Error "GHCR login failed!"
                Write-Info "Set credentials using:"
                Write-Info '  $env:GITHUB_TOKEN = "ghp_YOUR_TOKEN"'
                Write-Info '  $env:GITHUB_USERNAME = "your-username" (optional, defaults to Bluscream)'
                throw "GHCR login failed"
            }
        }
    }
    
    # Setup buildx
    Write-Info "Setting up Docker Buildx..."
    
    # Check if Docker is running
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Info "Docker is not running. Starting Docker Desktop..."
        
        # Try both methods simultaneously
        Start-Process "docker-desktop://" -ErrorAction SilentlyContinue
        
        $dockerDesktopPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        if (Test-Path $dockerDesktopPath) {
            Start-Process $dockerDesktopPath -ErrorAction SilentlyContinue
        }
        
        # Poll for Docker to become available (max 60 seconds)
        Write-Info "Waiting for Docker to start (max 60 seconds)..."
        $maxAttempts = 60
        $attempt = 0
        $dockerStarted = $false
        
        while ($attempt -lt $maxAttempts) {
            Start-Sleep -Seconds 1
            $attempt++
            
            docker info 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $dockerStarted = $true
                Write-Success "Docker is now running (started after $attempt seconds)"
                break
            }
            
            # Show progress every 5 seconds
            if ($attempt % 5 -eq 0) {
                Write-Info "Still waiting... ($attempt/$maxAttempts seconds)"
            }
        }
        
        if (-not $dockerStarted) {
            throw "Docker failed to start after $maxAttempts seconds. Please start Docker Desktop manually and try again."
        }
    } else {
        Write-Success "Docker is already running"
    }
    
    # Try to remove existing builder if it exists (in case it's corrupted)
    docker buildx rm multiarch 2>&1 | Out-Null
    
    # Create fresh builder
    docker buildx create --name multiarch --use 2>&1 | Out-Host
    $exitCode = $LASTEXITCODE
    Write-Host "Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Created fresh multiarch builder"
        
        # Bootstrap the builder
        Write-Info "Bootstrapping builder..."
        docker buildx inspect --bootstrap 2>&1 | Out-Host
        $exitCode = $LASTEXITCODE
        Write-Host "Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
        
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to bootstrap buildx builder"
        }
    }
    else {
        throw "Failed to create buildx builder"
    }
    
    # Build tags for both registries
    $tags = @(
        "-t", "bluscream1/pyrobud:$version",
        "-t", "bluscream1/pyrobud:latest"
    )
    
    if (-not $SkipGHCR) {
        $tags += @(
            "-t", "ghcr.io/bluscream/pyrobud:$version",
            "-t", "ghcr.io/bluscream/pyrobud:latest"
        )
    }
    
    # Build command
    if ($Publish) {
        # Multi-platform build with push
        $buildArgs = @(
            "buildx", "build",
            "--platform", "linux/amd64,linux/arm64",
            "-f", "docker/Dockerfile.debian"
        ) + $tags + @("--push", ".")
        
        Write-Info "Building and pushing multi-platform images..."
    }
    else {
        # Local build (single platform)
        Write-Info "Note: Local builds only support linux/amd64 (multi-platform requires --push)"
        $buildArgs = @(
            "buildx", "build",
            "--platform", "linux/amd64",
            "-f", "docker/Dockerfile.debian"
        ) + $tags + @("--load", ".")
        
        Write-Info "Building image locally..."
    }
    
    & docker @buildArgs 2>&1 | Tee-Object -FilePath "..\cursor.log" -Append | Out-Host
    
    if ($LASTEXITCODE -eq 0) {
        if ($Publish) {
            Write-Success "Docker images built and pushed successfully"
        }
        else {
            Write-Success "Docker image built locally"
        }
    }
    else {
        throw "Docker build failed with exit code $LASTEXITCODE"
    }
    
    # Step 4: Summary
    Write-Header "BUILD COMPLETE"
    Write-Success "Version: $version"
    
    if ($Publish) {
        if (-not $SkipDockerHub) {
            Write-Success "Docker Hub: https://hub.docker.com/r/bluscream1/pyrobud/tags"
        }
        
        if (-not $SkipGHCR) {
            Write-Success "GHCR: https://github.com/bluscream/pyrobud-bluscream-upstream/pkgs/container/pyrobud"
        }
        
        Write-Host "`nNext steps:" -ForegroundColor Cyan
        Write-Host "  - Test the image: docker run --rm bluscream1/pyrobud:$version pyrobud --help" -ForegroundColor White
        Write-Host "  - Update Unraid template if needed" -ForegroundColor White
        Write-Host "  - Update documentation" -ForegroundColor White
    }
    else {
        Write-Host "`nLocal build complete!" -ForegroundColor Cyan
        Write-Host "Test the image:" -ForegroundColor Cyan
        Write-Host "  docker run --rm bluscream1/pyrobud:$version pyrobud --help" -ForegroundColor White
        Write-Host "`nTo publish this build:" -ForegroundColor Cyan
        Write-Host "  .\build.ps1 -Publish -BumpType $BumpType" -ForegroundColor White
    }
    
    Write-Host "`nExit code: 0" -ForegroundColor Green
    exit 0
    
}
catch {
    Write-Error $_.Exception.Message
    Write-Host "`nExit code: 1" -ForegroundColor Red
    exit 1
}
