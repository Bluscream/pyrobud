# Example directory structure for organized data storage
# This shows how to configure pyrobud with separate directories

# Copy this file structure to your data directory:
# 
# data/
# ├── cfg/                  <- Config and session files
# │   ├── config.toml       <- Main config (copy from config.example.toml)
# │   ├── *.session         <- Telegram session files (auto-generated)
# │   └── *.session-journal <- Session journals (auto-generated)
# ├── db/                   <- Database directories  
# │   └── main.db/          <- LevelDB database (auto-generated)
# └── custom_modules/       <- Your custom modules (optional)
#     └── example.py

# When using this structure, update your config.toml:
# 
# [telegram]
# session_name = "main"  # Creates main.session in /data/cfg/
# 
# [bot]
# db_path = "/data/db/main.db"  # Database in /data/db/ directory

# For multiple accounts, use different config files:
# - cfg/account1.toml with session_name="account1" and db_path="/data/db/account1.db"
# - cfg/account2.toml with session_name="account2" and db_path="/data/db/account2.db"
# 
# Then run with: docker-compose run pyrobud pyrobud -c /data/cfg/account1.toml
