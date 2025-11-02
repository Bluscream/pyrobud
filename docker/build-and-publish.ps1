# Build and Publish Pyrobud Docker Images
# This script builds and publishes to both Docker Hub and GitHub Container Registry

param(
    [string]$Version = "v2.1.0-py3.14",
    [switch]$SkipLogin,
    [switch]$AmdOnly
)

Write-Host "=== Pyrobud Docker Build & Publish ===" -ForegroundColor Cyan

# Configuration
$DockerHubRepo = "bluscream1/pyrobud"
$GHCRRepo = "ghcr.io/bluscream/pyrobud"
$Platforms = if ($AmdOnly) { "linux/amd64" } else { "linux/amd64,linux/arm64" }

# Check if we're in the right directory
if (-not (Test-Path "../pyproject.toml")) {
    Write-Error "Please run this script from the docker/ directory"
    exit 1
}

# Login to registries (unless skipped)
if (-not $SkipLogin) {
    Write-Host "`nLogging in to Docker Hub..." -ForegroundColor Yellow
    if ($env:DOCKERHUB_TOKEN) {
        $env:DOCKERHUB_TOKEN | docker login -u $env:DOCKER_USERNAME --password-stdin
    } else {
        docker login -u $env:DOCKER_USERNAME
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker Hub login failed"
        exit 1
    }
    
    Write-Host "✓ Logged in to Docker Hub" -ForegroundColor Green
    
    Write-Host "`nLogging in to GitHub Container Registry..." -ForegroundColor Yellow
    if ($env:GITHUB_TOKEN) {
        $env:GITHUB_TOKEN | docker login ghcr.io -u Bluscream --password-stdin
    } else {
        docker login ghcr.io -u Bluscream
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "GHCR login failed"
        exit 1
    }
    
    Write-Host "✓ Logged in to GitHub Container Registry" -ForegroundColor Green
}

# Setup buildx
Write-Host "`nSetting up Docker Buildx..." -ForegroundColor Yellow
docker buildx create --name multiarch --use 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Created multiarch builder" -ForegroundColor Green
} else {
    docker buildx use multiarch
    Write-Host "✓ Using existing multiarch builder" -ForegroundColor Green
}

# Build tags
$Tags = @(
    "-t", "$DockerHubRepo:latest",
    "-t", "$DockerHubRepo:$Version",
    "-t", "$GHCRRepo:latest",
    "-t", "$GHCRRepo:$Version"
)

Write-Host "`nBuilding and pushing images..." -ForegroundColor Yellow
Write-Host "Platforms: $Platforms" -ForegroundColor Cyan
Write-Host "Tags:" -ForegroundColor Cyan
Write-Host "  - $DockerHubRepo:latest" -ForegroundColor Cyan
Write-Host "  - $DockerHubRepo:$Version" -ForegroundColor Cyan
Write-Host "  - $GHCRRepo:latest" -ForegroundColor Cyan
Write-Host "  - $GHCRRepo:$Version" -ForegroundColor Cyan

# Build and push
$BuildArgs = @(
    "buildx", "build",
    "--platform", $Platforms,
    "-f", "Dockerfile.debian",
    "--push"
) + $Tags + @("..")

Write-Host "`nExecuting: docker $($BuildArgs -join ' ')" -ForegroundColor Gray
& docker $BuildArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Successfully built and pushed all images!" -ForegroundColor Green
    Write-Host "`nImages published to:" -ForegroundColor Cyan
    Write-Host "  Docker Hub: https://hub.docker.com/r/$DockerHubRepo" -ForegroundColor Cyan
    Write-Host "  GHCR: https://github.com/Bluscream/pyrobud/pkgs/container/pyrobud" -ForegroundColor Cyan
} else {
    Write-Error "Build or push failed!"
    exit 1
}

Write-Host "`nTo use the images:" -ForegroundColor Yellow
Write-Host "  docker pull $DockerHubRepo:latest" -ForegroundColor White
Write-Host "  docker pull $GHCRRepo:latest" -ForegroundColor White
