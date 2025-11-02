# Unraid Installation Guide for Pyrobud

This guide will help you install and run Pyrobud on Unraid using Community Applications.

> **Credits:** Original project by [Danny Lin (@kdrag0n)](https://github.com/kdrag0n/pyrobud)  
> Python 3.14 modernization by [@Bluscream](https://github.com/Bluscream) with [Cursor.AI](https://cursor.com) assistance

## Prerequisites

- Unraid server (version 6.9.0 or newer recommended)
- Community Applications plugin installed
- Docker enabled on your Unraid server

## Installation Methods

### Method 1: Using the Template (Recommended)

1. Open the Unraid WebUI
2. Navigate to **Docker** tab
3. Click **Add Container** at the bottom
4. Click **Template repositories** (or scroll down to advanced view)
5. Add this URL to your template sources:
   ```
   https://github.com/Bluscream/pyrobud/tree/upstream/unraid
   ```
6. Search for "Pyrobud" in Community Applications
7. Click **Install**
8. Configure the required settings (see Configuration below)
9. Click **Apply**

### Method 2: Manual Docker Configuration

1. Navigate to **Docker** tab
2. Click **Add Container**
3. Fill in the following fields:

| Setting | Value |
|---------|-------|
| **Name** | `pyrobud` |
| **Repository** | `ghcr.io/bluscream/pyrobud:latest` |
| **Network Type** | `Bridge` |
| **Console Shell** | `Shell` |

4. Add the following path mapping:

| Container Path | Host Path | Access Mode |
|---------------|-----------|-------------|
| `/data` | `/mnt/user/appdata/pyrobud` | Read/Write |

5. Add environment variables:

| Variable | Value |
|----------|-------|
| `TZ` | Your timezone (e.g., `America/New_York`) |
| `PYTHONUNBUFFERED` | `1` |

6. Click **Apply**

## Configuration

Before starting the container for the first time, you need to create a `config.toml` file:

1. Navigate to `/mnt/user/appdata/pyrobud/` on your Unraid server
2. Copy `config.example.toml` from the repository to `config.toml`
3. Edit `config.toml` with your Telegram API credentials:
   - Get API ID and hash from https://my.telegram.org/apps
   - Set your preferred command prefix
   - Configure other settings as desired

## First Run

1. Start the container from the Docker tab
2. Click the container's **Console** icon
3. You'll be prompted to enter your phone number
4. Enter your full phone number with country code (no spaces, e.g., `12345678910`)
5. Enter the verification code sent to your Telegram account
6. The bot will start and connect to Telegram

## Post-Installation

### Viewing Logs

Click the **Log** icon next to your Pyrobud container to view real-time logs.

### Updating

To update to the latest version:

1. Stop the container
2. Click **Force Update** in the container settings
3. Start the container

### Resource Limits

You can adjust CPU and memory limits in the container's **Extra Parameters** field:

```
--cpus="2.0" --memory="512m"
```

Or use the Unraid Docker settings interface under **Advanced View**.

## Backup

The `/data` directory contains all your important data:
- `config.toml` - Your configuration
- `*.session*` - Telegram session files
- `*.db/` - LevelDB database

**Important**: Regularly backup `/mnt/user/appdata/pyrobud/` to prevent data loss!

## Troubleshooting

### Container won't start
- Check logs for error messages
- Ensure `config.toml` exists and is properly configured
- Verify API ID and hash are correct

### Can't connect to Telegram
- Check your internet connection
- Verify Telegram isn't blocked by your firewall
- Check if Telegram is having service issues

### High memory usage
- This is normal for Python applications
- Adjust memory limits if needed (512MB is recommended minimum)

## Support

### This Fork (Python 3.14 Version)
- **GitHub Issues**: https://github.com/Bluscream/pyrobud/issues
- **Documentation**: [Main README](../README.md)
- **Docker Guide**: [Docker README](../docker/README.md)

### Original Project
- **Original Author**: [Danny Lin (@kdrag0n)](https://github.com/kdrag0n)
- **Original Repository**: https://github.com/kdrag0n/pyrobud
- **Telegram Community**: https://t.me/pyrobud
- **Donate to Creator**: [PayPal](https://paypal.me/kdrag0ndonate)

## Additional Resources

- [Module Development Handbook](../DEVELOPMENT.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Code Style Guide](../CODE_STYLE.md)
