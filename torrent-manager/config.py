import yaml
from typing import Dict, Any

def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Set default values
    config.setdefault('log_path', '/logs/qbittorrent_cleanup.log')
    config.setdefault('check_interval', 3600)  # Check every hour
    config.setdefault('deletion_mode', 'manual')
    config.setdefault('deletion_delay_days', 30)
    config.setdefault('minimum_ratio', 1.0)
    
    # Validate configuration
    _validate_config(config)
    
    return config

def _validate_config(config: Dict[str, Any]):
    """Validate configuration parameters"""
    # Ensure required keys are present
    required_keys = ['qbittorrent']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # Validate qBittorrent connection details
    qbt_config = config['qbittorrent']
    required_qbt_keys = ['host', 'port', 'username', 'password']
    for key in required_qbt_keys:
        if key not in qbt_config:
            raise ValueError(f"Missing qBittorrent configuration key: {key}")

def save_config(config: Dict[str, Any], config_path: str = 'config.yaml'):
    """Save configuration to YAML file"""
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)