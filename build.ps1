#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build and push pyrobud Docker images to Docker Hub and GHCR
.DESCRIPTION
    This script:
    1. Bumps the version in pyproject.toml (patch, minor, or major)
    2. Commits and tags the version
    3. Builds multi-platform Docker images (linux/amd64, linux/arm64)
    4. Pushes to Docker Hub (bluscream1/pyrobud)
    5. Pushes to GitHub Container Registry (ghcr.io/bluscream/pyrobud)
.PARAMETER BumpType
    Version bump type: patch (default), minor, or major
.PARAMETER SkipVersionBump
    Skip version bumping and use current version
.PARAMETER SkipGit
    Skip git commit and tag
.PARAMETER SkipDockerHub
    Skip pushing to Docker Hub
.PARAMETER SkipGHCR
    Skip pushing to GitHub Container Registry
.PARAMETER DryRun
    Show what would be done without actually doing it
.EXAMPLE
    .\build.ps1
    .\build.ps1 -BumpType minor
    .\build.ps1 -SkipVersionBump
    .\build.ps1 -DryRun
#>

param(
    [ValidateSet("patch", "minor", "major")]
    [string]$BumpType = "patch",
    [switch]$SkipVersionBump,
    [switch]$SkipGit,
    [switch]$SkipDockerHub,
    [switch]$SkipGHCR,
    [switch]$DryRun
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
    
    if (-not $DryRun) {
        $content = Get-Content "pyproject.toml" -Raw
        $content = $content -replace 'version\s*=\s*"[^"]+"', "version = `"$newVersion`""
        Set-Content "pyproject.toml" -Value $content -NoNewline
        Write-Success "Updated pyproject.toml to version $newVersion"
    }
    
    return $newVersion
}

# Main script
try {
    Write-Header "PYROBUD BUILD SCRIPT"
    
    # Step 1: Version Management
    if (-not $SkipVersionBump) {
        Write-Header "STEP 1: VERSION BUMP"
        $version = Update-Version -type $BumpType
    } else {
        $version = Get-CurrentVersion
        Write-Info "Using current version: $version (version bump skipped)"
    }
    
    # Step 2: Git Operations
    if (-not $SkipGit -and -not $DryRun) {
        Write-Header "STEP 2: GIT COMMIT & TAG"
        
        git add pyproject.toml 2>&1 | Out-Host
        git commit -m "chore: bump version to $version" 2>&1 | Out-Host
        git tag -a "v$version" -m "Release v$version" 2>&1 | Out-Host
        git push origin ai 2>&1 | Out-Host
        git push origin "v$version" 2>&1 | Out-Host
        
        Write-Success "Committed and tagged version $version"
    } elseif (-not $SkipGit) {
        Write-Info "[DRY RUN] Would commit and tag version $version"
    }
    
    # Step 3: Docker Build
    Write-Header "STEP 3: DOCKER BUILD"
    Write-Info "Platforms: linux/amd64, linux/arm64"
    Write-Info "Docker Hub: bluscream1/pyrobud:$version, bluscream1/pyrobud:latest"
    Write-Info "GHCR: ghcr.io/bluscream/pyrobud:$version, ghcr.io/bluscream/pyrobud:latest"
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would build and push Docker images"
    } else {
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
        $buildArgs = @(
            "buildx", "build",
            "--platform", "linux/amd64,linux/arm64",
            "-f", "docker/Dockerfile.debian"
        ) + $tags + @(
            "--push",
            "."
        )
        
        Write-Info "Building and pushing images..."
        & docker @buildArgs 2>&1 | Tee-Object -FilePath "..\cursor.log" -Append | Out-Host
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Docker images built and pushed successfully"
        } else {
            throw "Docker build failed with exit code $LASTEXITCODE"
        }
    }
    
    # Step 4: Summary
    Write-Header "BUILD COMPLETE"
    Write-Success "Version: $version"
    
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
    
    Write-Host "`nExit code: 0" -ForegroundColor Green
    exit 0
    
} catch {
    Write-Error $_.Exception.Message
    Write-Host "`nExit code: 1" -ForegroundColor Red
    exit 1
}

