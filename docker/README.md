# Docker Guide for Pyrobud

This directory contains Docker configuration files for running Pyrobud in containers.

## Available Dockerfiles

- **Dockerfile.debian** (Recommended) - Debian 13 (Trixie) based image with Python 3.14
- **Dockerfile.alpine** - Alpine Linux based image (smaller but has compatibility issues with plyvel)

## Quick Start with Docker Compose

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** (optional):

   ```bash
   DOCKER_IMAGE=pyrobud
   DOCKER_TAG=latest
   CONFIG_DIR=./data/cfg
   DB_DIR=./data/db
   CUSTOM_MODULES_DIR=./data/custom_modules
   TZ=America/New_York
   ```

3. **Create directory structure and config:**

   ```bash
   # Create organized directory structure
   mkdir -p data/{cfg,db,custom_modules}
   
   # Copy Docker-optimized config (recommended)
   cp config.docker.toml data/cfg/config.toml
   
   # OR copy standard config
   cp ../config.example.toml data/cfg/config.toml
   
   # Edit with your Telegram API credentials
   nano data/cfg/config.toml
   ```
   
   **Important:** Ensure `db_path = "/data/db/main.db"` in your config!

4. **Start the container:**

   ```bash
   docker-compose up -d
   ```

5. **First run - authenticate:**
   ```bash
   docker-compose logs -f
   ```
   Follow the prompts to enter your phone number and verification code.

## Directory Structure

The new setup uses separate directories for better organization:

```
data/
├── cfg/                      # Configuration & sessions
│   ├── config.toml           # Main config
│   ├── main.session          # Telegram session (auto-created)
│   └── main.session-journal  # Session journal (auto-created)
├── db/                       # Databases
│   └── main.db/              # LevelDB database (auto-created)
└── custom_modules/           # Your custom modules (optional)
    └── example.py
```

**Benefits:**
- ✅ Clean separation of concerns
- ✅ Easy to backup specific components
- ✅ Supports multiple accounts (different config files)
- ✅ Custom modules won't affect container updates
- ✅ Matches structure used by many users

## Manual Docker Build

### Building the Image

**Debian (Recommended):**

```bash
docker build -t pyrobud:latest -f docker/Dockerfile.debian ..
```

**Alpine:**

```bash
docker build -t pyrobud:alpine -f docker/Dockerfile.alpine ..
```

### Running the Container

**With organized directory structure (recommended):**

```bash
docker run -d \
  --name pyrobud \
  --restart unless-stopped \
  -v ./data/cfg:/data/cfg:rw \
  -v ./data/db:/data/db:rw \
  -v ./data/custom_modules:/opt/venv/lib/python3.14/site-packages/pyrobud/custom_modules:ro \
  -e TZ=UTC \
  -e PYTHONUNBUFFERED=1 \
  pyrobud:latest
```

**Or with single data directory (legacy):**

```bash
docker run -d \
  --name pyrobud \
  --restart unless-stopped \
  -v ./data:/data \
  -e TZ=UTC \
  -e PYTHONUNBUFFERED=1 \
  pyrobud:latest pyrobud -c /data/config.toml
```

## Using Pre-built Images

### From GitHub Container Registry (GHCR)

```bash
docker pull ghcr.io/bluscream/pyrobud:latest
docker run -d \
  --name pyrobud \
  --restart unless-stopped \
  -v ./data:/data \
  ghcr.io/bluscream/pyrobud:latest
```

### From Docker Hub

```bash
docker pull kdrag0n/pyrobud:latest
docker run -d \
  --name pyrobud \
  --restart unless-stopped \
  -v ./data:/data \
  kdrag0n/pyrobud:latest
```

## Configuration

Before first run, create a `config.toml` file in the data directory:

```bash
# Create data directory
mkdir -p ./data

# Copy example config
cp ../config.example.toml ./data/config.toml

# Edit with your credentials
nano ./data/config.toml
```

**Required settings:**

- `api_id` - Get from https://my.telegram.org/apps
- `api_hash` - Get from https://my.telegram.org/apps
- `session_name` - Name for your session file

## Docker Compose Commands

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Rebuild and restart
docker-compose up -d --build

# Remove everything (including volumes)
docker-compose down -v
```

## Environment Variables

| Variable           | Default   | Description              |
| ------------------ | --------- | ------------------------ |
| `TZ`               | `UTC`     | Container timezone       |
| `PYTHONUNBUFFERED` | `1`       | Unbuffered Python output |
| `DOCKER_IMAGE`     | `pyrobud` | Docker image name        |
| `DOCKER_TAG`       | `latest`  | Docker image tag         |

## Volume Mounts

| Container Path | Description                         | Required |
| -------------- | ----------------------------------- | -------- |
| `/data`        | Config, database, and session files | Yes      |

## Resource Limits

Adjust in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: "2.0" # Max 2 CPU cores
      memory: 512M # Max 512MB RAM
    reservations:
      cpus: "0.5" # Min 0.5 CPU cores
      memory: 256M # Min 256MB RAM
```

## Multi-Platform Support

The Debian image supports multiple architectures:

- `linux/amd64` (x86_64)
- `linux/arm64` (ARM64/aarch64)

Build for specific platform:

```bash
docker buildx build \
  --platform linux/amd64 \
  -t pyrobud:amd64 \
  -f docker/Dockerfile.debian ..
```

## Troubleshooting

### Container keeps restarting

- Check logs: `docker-compose logs pyrobud`
- Verify config.toml exists and is valid
- Ensure API credentials are correct

### Permission errors

```bash
# Fix permissions on data directory
sudo chown -R 1000:1000 ./data
```

### Can't connect to Telegram

- Check if Telegram is accessible from your network
- Verify API ID and hash are correct
- Check firewall settings

### Out of memory

- Increase memory limit in docker-compose.yml
- Check for memory leaks in custom modules

## Advanced Usage

### Running with custom modules

Mount your custom modules directory:

```yaml
volumes:
  - pyrobud-data:/data
  - ./custom_modules:/opt/venv/lib/python3.14/site-packages/pyrobud/custom_modules:ro
```

### Using a specific Python version

Edit the Dockerfile and change:

```dockerfile
FROM python:3.14-trixie AS python-build
```

### Debugging

Run with interactive shell:

```bash
docker run -it --rm -v ./data:/data pyrobud:latest sh
```

## Security Notes

1. **Never expose ports** - Pyrobud doesn't need any exposed ports
2. **Protect your config** - Keep `config.toml` secure (contains API credentials)
3. **Use read-only mounts** when possible for non-data directories
4. **Regular backups** of the `/data` directory
5. **Keep the image updated** for security patches

## See Also

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Unraid Docker Guide](../unraid/README.md)
- [Main Pyrobud Documentation](../README.md)
