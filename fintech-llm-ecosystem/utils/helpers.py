import yaml
from pathlib import Path

def load_config():
    """Load configuration from YAML file"""
    config_path = Path("config") / "settings.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def validate_config(config):
    """Validate essential configuration parameters"""
    required_keys = {
        "binance": ["api_url", "ws_url", "streams"],
        "models": ["primary", "secondary", "n_ctx", "n_gpu_layers"],
        "system": ["max_retries", "timeout", "cache_dir"]
    }
    
    for section, keys in required_keys.items():
        if section not in config:
            raise ValueError(f"Missing section in config: {section}")
        for key in keys:
            if key not in config[section]:
                raise ValueError(f"Missing key {key} in section {section}")