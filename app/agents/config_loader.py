"""
Configuration Loader for Station Agents

This module provides utilities to load station configurations from YAML files.
Each station has a corresponding YAML file in the configs/ directory with:
- model: The OpenRouter model to use
- temperature: Temperature setting for the model
- max_tokens: Maximum tokens for generation
- prompts: Dictionary of prompts used by the station
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path

class StationConfig:
    """Configuration for a single station"""

    def __init__(self, config_data: Dict[str, Any]):
        self.model = config_data.get('model', 'qwen-72b')
        self.temperature = config_data.get('temperature', 0.7)
        self.max_tokens = config_data.get('max_tokens', 3000)
        self.prompts = config_data.get('prompts', {})
        self.dependencies = config_data.get('dependencies', [])
        self.enabled = config_data.get('enabled', True)
        self.station_name = config_data.get('station_name', 'Unknown Station')
        self.description = config_data.get('description', '')
        
        # Store raw config data for custom fields
        self._config_data = config_data
        
    def get_prompt(self, prompt_name: str = 'main') -> str:
        """Get a specific prompt by name"""
        return self.prompts.get(prompt_name, '')
    
    def get_all_prompts(self) -> Dict[str, str]:
        """Get all prompts as a dictionary"""
        return self.prompts.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get any configuration value by key"""
        return self._config_data.get(key, default)
    
    def __getattr__(self, name: str) -> Any:
        """Allow access to custom configuration fields"""
        if name in self._config_data:
            return self._config_data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


def load_station_config(station_number: int, station_suffix: str = None) -> StationConfig:
    """
    Load configuration for a specific station
    
    Args:
        station_number: The station number (1-15)
        station_suffix: Optional suffix for special stations (e.g., '4_5' for station 4.5)
        
    Returns:
        StationConfig: Configuration object for the station
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the YAML file is invalid
    """
    # Determine config file path
    if station_suffix:
        config_filename = f"station_{station_suffix}.yml"
    else:
        config_filename = f"station_{station_number}.yml"
    
    # Get the config directory path (relative to this file)
    config_dir = Path(__file__).parent / 'configs'
    config_path = config_dir / config_filename
    
    # Check if file exists
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    # Load and parse YAML
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        return StationConfig(config_data)
    
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in {config_path}: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading config from {config_path}: {str(e)}")


def reload_station_config(station_number: int, station_suffix: str = None) -> StationConfig:
    """
    Reload configuration for a station (useful for hot-reloading during development)
    
    Args:
        station_number: The station number (1-15)
        station_suffix: Optional suffix for special stations
        
    Returns:
        StationConfig: Fresh configuration object
    """
    return load_station_config(station_number, station_suffix)


