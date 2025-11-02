# Quick Installation Guide for Unraid

## Step-by-Step Setup

### 1. Create Application Directory
```bash
mkdir -p /mnt/user/appdata/pyrobud
cd /mnt/user/appdata/pyrobud
```

### 2. Create Configuration File
```bash
# Download example config
wget https://raw.githubusercontent.com/kdrag0n/pyrobud/master/config.example.toml -O config.toml

# Or manually create config.toml with nano/vi
nano config.toml
```

### 3. Configure Telegram API Credentials

Edit `config.toml` and set:
```toml
[telegram]
api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"
session_name = "main"

[bot]
default_prefix = "."
db_path = "main.db"
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
Repository: ghcr.io/bluscream/pyrobud:latest
Network Type: bridge

Path Mapping:
  Container Path: /data
  Host Path: /mnt/user/appdata/pyrobud
  Access Mode: Read/Write

Environment Variables:
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
├── config.toml          # Your configuration
├── main.session         # Telegram session
├── main.session-journal # Session journal
└── main.db/            # LevelDB database
```

## Backup Your Data

**Important files to backup:**
- `config.toml` - Your configuration
- `*.session*` - Telegram authentication
- `*.db/` - All your bot data

### Backup Command:
```bash
tar -czf pyrobud-backup-$(date +%Y%m%d).tar.gz \
  /mnt/user/appdata/pyrobud/
```

## Troubleshooting

### Container won't start
1. Check logs: `docker logs pyrobud`
2. Verify `config.toml` exists
3. Check API credentials are correct

### "Session file is corrupted"
Delete session files and re-authenticate:
```bash
rm /mnt/user/appdata/pyrobud/*.session*
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

- **Issues**: https://github.com/kdrag0n/pyrobud/issues
- **Telegram Chat**: https://t.me/pyrobud
- **Documentation**: https://github.com/kdrag0n/pyrobud/blob/master/README.md
- **Module Dev**: https://github.com/kdrag0n/pyrobud/blob/master/DEVELOPMENT.md

