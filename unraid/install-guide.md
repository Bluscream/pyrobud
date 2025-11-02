# Quick Installation Guide for Unraid

> **Credits:** Original by [kdrag0n](https://github.com/kdrag0n/pyrobud) | Python 3.14 modernization by [Bluscream](https://github.com/Bluscream) with [Cursor.AI](https://cursor.com)

## Step-by-Step Setup

### 1. Create Application Directory Structure

```bash
# Create organized directory structure
mkdir -p /mnt/user/appdata/pyrobud/{cfg,db,custom_modules}
cd /mnt/user/appdata/pyrobud
```

### 2. Create Configuration File

```bash
# Download Docker-optimized config
wget https://raw.githubusercontent.com/Bluscream/pyrobud/upstream/docker/config.example.docker.toml -O cfg/config.toml

# Or download standard example
wget https://raw.githubusercontent.com/kdrag0n/pyrobud/master/config.example.toml -O cfg/config.toml

# Edit with your credentials
nano cfg/config.toml
```

### 3. Configure Telegram API Credentials

Edit `cfg/config.toml` and set:

```toml
[telegram]
api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"
session_name = "main"

[bot]
default_prefix = "."
db_path = "/data/db/main.db"  # Database in separate directory
```

**Get your API credentials:**

1. Go to https://my.telegram.org/apps
2. Log in with your phone number
3. Create a new application
4. Copy the `api_id` and `api_hash`

### 4. Add Docker Container

#### Option A: Using Community Applications

1. Open Unraid WebUI → **APPS** tab
2. Search for "pyrobud"
3. Click **Install**
4. Verify settings and click **Apply**

#### Option B: Manual Configuration

1. Go to **Docker** tab
2. Click **Add Container**
3. Use these settings:

```
Name: pyrobud
Repository: bluscream1/pyrobud:latest
Network Type: bridge

Path Mappings:
  1. Config Directory
     Container Path: /data/cfg
     Host Path: /mnt/user/appdata/pyrobud/cfg
     Access Mode: Read/Write

  2. Database Directory
     Container Path: /data/db
     Host Path: /mnt/user/appdata/pyrobud/db
     Access Mode: Read/Write

  3. Custom Modules (Optional)
     Container Path: /opt/venv/lib/python3.14/site-packages/pyrobud/custom_modules
     Host Path: /mnt/user/appdata/pyrobud/custom_modules
     Access Mode: Read-Only

Environment Variables:
  CONFIG_FILE: config.toml
  TZ: America/New_York (your timezone)
  PYTHONUNBUFFERED: 1
```

4. Click **Apply**

### 5. First Run Authentication

1. Start the container
2. Click the **Console** icon (terminal)
3. Enter your **full phone number** with country code (no spaces):
   - Example: `12345678910` (for +1 234-567-8910)
4. Enter the verification code sent to Telegram
5. Container will start automatically

### 6. Verify It's Working

Open Telegram on any device and send:

```
.help
```

You should see the help menu!

## Common Commands

### View Logs

```bash
docker logs -f pyrobud
```

### Restart Container

```bash
docker restart pyrobud
```

### Stop Container

```bash
docker stop pyrobud
```

### Update to Latest Version

```bash
docker pull ghcr.io/bluscream/pyrobud:latest
docker restart pyrobud
```

### Access Container Shell

```bash
docker exec -it pyrobud sh
```

## Directory Structure

```
/mnt/user/appdata/pyrobud/
├── cfg/                      # Configuration directory
│   ├── config.toml           # Main configuration
│   ├── main.session          # Telegram session (auto-generated)
│   ├── main.session-journal  # Session journal (auto-generated)
│   ├── account2.toml         # Additional account config (optional)
│   └── account2.session      # Additional session (optional)
├── db/                       # Database directory
│   ├── main.db/              # Main LevelDB database (auto-generated)
│   └── account2.db/          # Additional database (optional)
└── custom_modules/           # Custom modules directory (optional)
    └── example.py            # Your custom modules
```

## Backup Your Data

**Important files to backup:**

- `cfg/` - All configurations and sessions
  - `*.toml` - Configuration files
  - `*.session*` - Telegram authentication
- `db/` - All database directories
  - `*.db/` - LevelDB databases with bot data
- `custom_modules/` - Your custom modules (if any)

### Backup Command:

```bash
# Backup everything
tar -czf pyrobud-backup-$(date +%Y%m%d).tar.gz \
  /mnt/user/appdata/pyrobud/
```

Or backup individual directories:
```bash
# Backup just config and sessions
tar -czf pyrobud-cfg-$(date +%Y%m%d).tar.gz \
  /mnt/user/appdata/pyrobud/cfg/

# Backup just databases
tar -czf pyrobud-db-$(date +%Y%m%d).tar.gz \
  /mnt/user/appdata/pyrobud/db/
```

## Troubleshooting

### Container won't start

1. Check logs: `docker logs pyrobud`
2. Verify directory structure exists:
   ```bash
   ls -la /mnt/user/appdata/pyrobud/
   # Should show: cfg/, db/, custom_modules/
   ```
3. Verify `cfg/config.toml` exists and has correct permissions
4. Check API credentials in `cfg/config.toml`

### "Session file is corrupted"

Delete session files and re-authenticate:

```bash
rm /mnt/user/appdata/pyrobud/cfg/*.session*
docker restart pyrobud
```

### Out of Memory

Increase memory limit in container settings:

```
Extra Parameters: --memory="1g"
```

### Can't send commands in Telegram

1. Check bot is running: `docker ps | grep pyrobud`
2. Verify prefix is correct (default is `.`)
3. Check logs for errors

## Advanced Configuration

### Custom Modules

Place custom modules in:

```
/mnt/user/appdata/pyrobud/custom_modules/
```

Then add volume mount:

```
Container: /opt/venv/lib/python3.14/site-packages/pyrobud/custom_modules
Host: /mnt/user/appdata/pyrobud/custom_modules
Mode: Read-Only
```

### Resource Limits

Adjust in container **Extra Parameters**:

```
--cpus="2.0" --memory="512m" --memory-swap="1g"
```

## Support & Resources

### This Fork (Python 3.14)
- **Issues**: https://github.com/Bluscream/pyrobud/issues
- **Documentation**: [Main README](../README.md)
- **Docker Guide**: [Docker README](../docker/README.md)

### Original Project
- **Original Creator**: [Danny Lin (@kdrag0n)](https://github.com/kdrag0n)
- **Original Repository**: https://github.com/kdrag0n/pyrobud
- **Telegram Chat**: https://t.me/pyrobud
- **Donate to kdrag0n**: [PayPal](https://paypal.me/kdrag0ndonate)
