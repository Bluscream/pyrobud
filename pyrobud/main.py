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

    print(f"[DEBUG] Parsed arguments: config_path={args.config_path}, log_file={args.log_file}")

    # Determine log file from CLI arg, env var, or config file
    # Priority: CLI arg > env var > config file
    log_file = args.log_file or os.getenv("PYROBUD_LOG_FILE")

    print(f"[DEBUG] Log file from CLI/ENV: {log_file}")

    if not log_file:
        # Try to read from config file as last resort
        try:
            import tomlkit
            config_path = Path(args.config_path)
            print(f"[DEBUG] Checking config file: {config_path}")
            if config_path.exists():
                config_data = config_path.read_text()
                config = tomlkit.loads(config_data)
                log_file = config.get("logging", {}).get("log_file")
                print(f"[DEBUG] Log file from config: {log_file}")
        except Exception as e:
            # Silently ignore config read errors - logging will work without file
            print(f"[DEBUG] Config read error: {e}")
            pass

    print(f"[DEBUG] Final log_file value: {log_file}")

    log = logging.getLogger("launch")
    logs.setup_logging(log_file=log_file)

    print(f"[DEBUG] Logging setup complete")

    log.info("Loading code...")

    launch.main(config_path=args.config_path)


if __name__ == "__main__":
    main()
