#!/usr/bin/env python3
"""
Station Registry - Auto-Discovery and Dynamic Pipeline Builder

Automatically discovers all stations, reads their metadata, resolves dependencies,
and builds execution pipelines dynamically.
"""

import importlib
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class StationMetadata:
    """Metadata for a discovered station"""
    number: float  # Support for stations like 4.5
    name: str
    class_name: str
    module_path: str
    file_path: Path
    config_path: Optional[Path]
    dependencies: List[int]  # List of station numbers this depends on
    station_type: str
    purpose: str
    enabled: bool = True


class StationRegistry:
    """
    Auto-discovers and manages all stations in the pipeline
    """
    
    def __init__(self, agents_dir: Path = None):
        if agents_dir is None:
            agents_dir = Path(__file__).parent
        
        self.agents_dir = agents_dir
        self.configs_dir = agents_dir / "configs"
        self.stations: Dict[float, StationMetadata] = {}
        self._discover_stations()
    
    def _discover_stations(self):
        """Discover all station files and load their metadata"""
        logger.info("🔍 Discovering stations...")
        
        # Find all station_*.py files
        station_files = list(self.agents_dir.glob("station_*.py"))
        
        for file_path in station_files:
            try:
                metadata = self._extract_station_metadata(file_path)
                if metadata:
                    self.stations[metadata.number] = metadata
                    logger.info(f"   ✓ Discovered Station {metadata.number}: {metadata.name}")
            except Exception as e:
                logger.warning(f"   ⚠️  Could not load {file_path.name}: {e}")
        
        logger.info(f"✅ Discovered {len(self.stations)} stations")
    
    def _extract_station_metadata(self, file_path: Path) -> Optional[StationMetadata]:
        """Extract metadata from a station file"""
        filename = file_path.stem  # e.g., "station_08_character_architecture"
        
        # Parse station number from filename
        match = re.match(r'station_(\d+(?:_\d+)?)', filename)
        if not match:
            return None
        
        station_num_str = match.group(1)
        
        # Handle special cases like "04_5" -> 4.5
        if '_' in station_num_str and station_num_str.count('_') == 1:
            parts = station_num_str.split('_')
            try:
                station_num = float(f"{int(parts[0])}.{parts[1]}")
            except:
                station_num = int(station_num_str.replace('_', ''))
        else:
            station_num = int(station_num_str)
        
        # Read config file for metadata
        # Normalize config filename (remove leading zeros for single-digit stations)
        if station_num == int(station_num):
            config_filename = f"station_{int(station_num)}.yml"
        else:
            config_filename = f"station_{str(station_num).replace('.', '_')}.yml"
        
        config_file = self.configs_dir / config_filename
        dependencies = []
        station_type = "Unknown"
        purpose = ""
        enabled = True
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                    
                    # Extract dependencies
                    deps = config.get('dependencies', [])
                    if isinstance(deps, list):
                        for dep in deps:
                            if isinstance(dep, dict) and 'station' in dep:
                                dep_num = dep['station']
                                # Handle both int and float dependencies
                                if isinstance(dep_num, (int, float)):
                                    dependencies.append(dep_num)
                    elif isinstance(deps, dict) and not deps.get('none'):
                        # Handle other dependency formats
                        pass
                    
                    # Extract metadata
                    metadata = config.get('metadata', {})
                    station_type = metadata.get('station_type', 'Unknown')
                    purpose = metadata.get('purpose', '')
                    enabled = config.get('enabled', True)
                    
            except Exception as e:
                logger.warning(f"Could not read config for station {station_num}: {e}")
        
        # Extract station name from filename
        name_part = filename.replace(f"station_{station_num_str}_", "")
        name = name_part.replace("_", " ").title()
        
        # Generate class name (look for it in the file)
        class_name = self._find_class_name(file_path)
        
        return StationMetadata(
            number=station_num,
            name=name,
            class_name=class_name,
            module_path=f"app.agents.{filename}",
            file_path=file_path,
            config_path=config_file if config_file.exists() else None,
            dependencies=dependencies,
            station_type=station_type,
            purpose=purpose,
            enabled=enabled
        )
    
    def _find_class_name(self, file_path: Path) -> str:
        """Find the main station class name in the file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Look for class Station##ClassName pattern
                match = re.search(r'class (Station\d+\w+)(?:\(|:)', content)
                if match:
                    return match.group(1)
        except:
            pass
        
        # Fallback: generate from filename
        filename = file_path.stem
        parts = filename.split('_')[1:]  # Remove 'station'
        return 'Station' + ''.join(p.capitalize() for p in parts)
    
    def get_execution_order(self) -> List[float]:
        """
        Determine the correct execution order based on dependencies.
        Uses topological sort to resolve dependency graph.
        """
        # Build dependency graph - only include enabled stations
        graph = {num: set(meta.dependencies) for num, meta in self.stations.items() if meta.enabled}
        
        # Topological sort
        ordered = []
        visited = set()
        temp_mark = set()
        
        def visit(node):
            if node in temp_mark:
                raise ValueError(f"Circular dependency detected involving station {node}")
            if node in visited:
                return
            
            temp_mark.add(node)
            
            # Visit dependencies first
            for dep in graph.get(node, []):
                if dep in graph:  # Only visit if dependency exists and is enabled
                    visit(dep)
            
            temp_mark.remove(node)
            visited.add(node)
            ordered.append(node)
        
        # Visit all nodes
        for node in sorted(graph.keys()):
            if node not in visited:
                visit(node)
        
        return ordered
    
    def get_station_metadata(self, station_num: float) -> Optional[StationMetadata]:
        """Get metadata for a specific station"""
        return self.stations.get(station_num)
    
    def load_station_class(self, station_num: float):
        """Dynamically load and return a station class"""
        metadata = self.stations.get(station_num)
        if not metadata:
            raise ValueError(f"Station {station_num} not found in registry")
        
        # Import the module
        module = importlib.import_module(metadata.module_path)
        
        # Get the class
        station_class = getattr(module, metadata.class_name)
        
        return station_class
    
    def get_all_stations(self) -> Dict[float, StationMetadata]:
        """Get all discovered stations"""
        return self.stations.copy()
    
    def get_enabled_stations(self) -> Dict[float, StationMetadata]:
        """Get only enabled stations"""
        return {num: meta for num, meta in self.stations.items() if meta.enabled}
    
    def print_pipeline(self):
        """Print the execution pipeline"""
        try:
            order = self.get_execution_order()
        except ValueError as e:
            print(f"\n❌ Error in pipeline: {e}\n")
            return
        
        print("\n🏭 PIPELINE EXECUTION ORDER")
        print("=" * 70)
        
        for i, station_num in enumerate(order, 1):
            meta = self.stations[station_num]
            deps_str = f"depends on: {meta.dependencies}" if meta.dependencies else "no dependencies"
            print(f"  {i:2d}. Station {station_num}: {meta.name}")
            print(f"      Type: {meta.station_type} | {deps_str}")
        
        print("=" * 70)
        print(f"Total stations: {len(order)}\n")


# Global registry instance
_registry = None

def get_station_registry() -> StationRegistry:
    """Get the global station registry (singleton)"""
    global _registry
    if _registry is None:
        _registry = StationRegistry()
    return _registry


def reload_registry():
    """Force reload of the station registry"""
    global _registry
    _registry = StationRegistry()
    return _registry

