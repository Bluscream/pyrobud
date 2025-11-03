import argparse
import logging
import os
from pathlib import Path

from . import DEFAULT_CONFIG_PATH, __description__, launch, logs

def main():
    """Main entry point for the default bot command."""
    
    # Parse arguments
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-c",
        "--config-path",
        metavar="PATH",
        type=str,
        default=DEFAULT_CONFIG_PATH,
        help="config file to use",
    )
    parser.add_argument(
        "--log-file",
        metavar="PATH",
        type=str,
        default=None,
        help="optional log file path (also via PYROBUD_LOG_FILE env var or config [logging] section)",
    )

    args = parser.parse_args()
    
    # Log config path source
    print("[DEBUG] Config path sources:")
    print(f"  - CLI argument: {args.config_path if args.config_path != DEFAULT_CONFIG_PATH else '(not provided)'}")
    print(f"  - Default: {DEFAULT_CONFIG_PATH}")
    print(f"  - CONFIG_FILE env: {os.getenv('CONFIG_FILE', '(not set)')}")
    print(f"  - Resolved path: {args.config_path}")

    # Determine log file from CLI arg, env var, or config file
    # Priority: CLI arg > env var > config file
    log_file = args.log_file or os.getenv("PYROBUD_LOG_FILE")
    
    print(f"[DEBUG] Log file sources:")
    print(f"  - CLI argument: {args.log_file or '(not provided)'}")
    print(f"  - PYROBUD_LOG_FILE env: {os.getenv('PYROBUD_LOG_FILE', '(not set)')}")

    if not log_file:
        # Try to read from config file as last resort
        try:
            import tomlkit
            config_path = Path(args.config_path)
            if config_path.exists():
                config_data = config_path.read_text()
                config = tomlkit.loads(config_data)
                log_file = config.get("logging", {}).get("log_file")
                if log_file:
                    print(f"  - Config file: {log_file}")
        except Exception:
            # Silently ignore config read errors - logging will work without file
            pass

    print(f"[DEBUG] Setting up logging (log_file={log_file or '(console only)'})...")
    
    log = logging.getLogger("launch")
    logs.setup_logging(log_file=log_file)
    
    print(f"[DEBUG] Logging setup complete")

    log.info("Loading code...")
    log.info(f"Config path: {args.config_path}")

    launch.main(config_path=args.config_path)


if __name__ == "__main__":
    main()
