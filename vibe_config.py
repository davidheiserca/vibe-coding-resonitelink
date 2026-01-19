# ResoniteLink AI World Builder v5.0
# config.py - Configuration loading

"""
Configuration management for the ResoniteLink AI World Builder.
Loads settings from resonite_builder.conf file.
"""

import os
import sys


# Default configuration values
DEFAULTS = {
    "ANTHROPIC_API_KEY": "",
    "RESONITE_WS_URL": "ws://localhost:9000",
    "LOG_DIR": ".",
    "AI_MODEL": "claude-sonnet-4-20250514",
    "COMMAND_TIMEOUT": "10",
    "CONNECTION_TIMEOUT": "10",
}


class Config:
    """Configuration container with attribute access."""
    
    def __init__(self):
        self.anthropic_api_key = ""
        self.resonite_ws_url = "ws://localhost:9000"
        self.log_dir = "."
        self.ai_model = "claude-sonnet-4-20250514"
        self.command_timeout = 10
        self.connection_timeout = 10
    
    def __repr__(self):
        return (
            f"Config(\n"
            f"  resonite_ws_url={self.resonite_ws_url!r},\n"
            f"  log_dir={self.log_dir!r},\n"
            f"  ai_model={self.ai_model!r},\n"
            f"  command_timeout={self.command_timeout},\n"
            f"  connection_timeout={self.connection_timeout}\n"
            f")"
        )


def load_config(config_path="resonite_builder.conf"):
    """Load configuration from file.
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Config: Configuration object with loaded values
    
    Raises:
        SystemExit: If config file not found or API key missing
    """
    config = Config()
    raw_config = dict(DEFAULTS)
    
    # Try to find config file
    if not os.path.exists(config_path):
        # Try in script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_path = os.path.join(script_dir, config_path)
        if os.path.exists(alt_path):
            config_path = alt_path
        else:
            print(f"ERROR: Config file not found: {config_path}")
            print("")
            print("Create resonite_builder.conf with:")
            print("  ANTHROPIC_API_KEY=your-api-key")
            print("  RESONITE_WS_URL=ws://localhost:PORT")
            print("  LOG_DIR=.")
            print("")
            print("Get your API key from: https://console.anthropic.com/")
            print("Get the WebSocket port from Resonite Dashboard -> Sessions -> Enable ResoniteLink")
            sys.exit(1)
    
    # Parse config file
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue
                
                # Parse key=value pairs
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip().upper()
                    value = value.strip()
                    
                    if key in DEFAULTS:
                        raw_config[key] = value
                    else:
                        print(f"Warning: Unknown config key '{key}' on line {line_num}")
    
    except Exception as e:
        print(f"ERROR: Failed to read config file: {e}")
        sys.exit(1)
    
    # Validate required fields
    if not raw_config["ANTHROPIC_API_KEY"]:
        print("ERROR: ANTHROPIC_API_KEY is required in config file")
        print("Get your API key from: https://console.anthropic.com/")
        sys.exit(1)
    
    # Populate config object
    config.anthropic_api_key = raw_config["ANTHROPIC_API_KEY"]
    config.resonite_ws_url = raw_config["RESONITE_WS_URL"]
    config.log_dir = raw_config["LOG_DIR"]
    config.ai_model = raw_config["AI_MODEL"]
    
    try:
        config.command_timeout = int(raw_config["COMMAND_TIMEOUT"])
    except ValueError:
        print(f"Warning: Invalid COMMAND_TIMEOUT value, using default 10")
        config.command_timeout = 10
    
    try:
        config.connection_timeout = int(raw_config["CONNECTION_TIMEOUT"])
    except ValueError:
        print(f"Warning: Invalid CONNECTION_TIMEOUT value, using default 10")
        config.connection_timeout = 10
    
    return config


def create_default_config(config_path="resonite_builder.conf"):
    """Create a default configuration file.
    
    Args:
        config_path: Path to create config file
    """
    content = """# ResoniteLink AI World Builder Configuration File
# Lines starting with # are comments

# Anthropic API Key (get from https://console.anthropic.com/)
ANTHROPIC_API_KEY=your-api-key-here

# Resonite WebSocket URL (get port from Resonite Dashboard -> Sessions -> Enable ResoniteLink)
RESONITE_WS_URL=ws://localhost:9000

# Log file directory (. = current directory)
LOG_DIR=.

# AI Model to use (default: claude-sonnet-4-20250514)
AI_MODEL=claude-sonnet-4-20250514

# Command timeout in seconds
COMMAND_TIMEOUT=10

# Connection timeout in seconds
CONNECTION_TIMEOUT=10
"""
    
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Created default config file: {config_path}")
    print("Please edit it with your API key and WebSocket URL.")
