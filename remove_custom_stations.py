#!/usr/bin/env python3
"""
Remove Custom Stations Script

Safely removes custom stations created with station_creator_wizard.py.
Works with the auto-discovery system - no manual code updates needed!

Usage:
    python remove_custom_stations.py
    python remove_custom_stations.py --station 21
    python remove_custom_stations.py --all-custom
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict
import yaml

# Add paths
sys.path.append(str(Path(__file__).parent / "app"))

from app.agents.station_registry import get_station_registry, reload_registry


class StationRemover:
    """Safely removes custom stations"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.agents_dir = self.project_root / "app" / "agents"
        self.configs_dir = self.agents_dir / "configs"
        self.tools_dir = self.project_root / "tools"
        
        # Standard stations that should never be removed (1-20, plus 4.5)
        self.protected_stations = set(range(1, 21)) | {4.5}
    
    def get_custom_stations(self) -> Dict[float, Dict]:
        """Get list of all custom stations (station number > 20)"""
        registry = reload_registry()
        all_stations = registry.get_all_stations()
        
        custom_stations = {}
        for num, meta in all_stations.items():
            if num not in self.protected_stations:
                custom_stations[num] = {
                    'number': num,
                    'name': meta.name,
                    'file_path': meta.file_path,
                    'config_path': meta.config_path,
                    'type': meta.station_type,
                    'dependencies': meta.dependencies
                }
        
        return custom_stations
    
    def find_test_script(self, station_num: float) -> Path:
        """Find test script for a station"""
        # Convert station number to string format used in filenames
        if station_num == int(station_num):
            num_str = str(int(station_num))
        else:
            num_str = str(station_num).replace('.', '_')
        
        test_file = self.tools_dir / f"test_station_{num_str}.py"
        return test_file if test_file.exists() else None
    
    def list_custom_stations(self):
        """Display all custom stations"""
        custom_stations = self.get_custom_stations()
        
        if not custom_stations:
            print("\n📭 No custom stations found.")
            print("   Only built-in stations (1-20) are present.\n")
            return custom_stations
        
        print("\n📋 CUSTOM STATIONS (Created with station_creator_wizard.py)")
        print("="*80)
        
        for num in sorted(custom_stations.keys()):
            station = custom_stations[num]
            print(f"\n🔹 Station {num}: {station['name']}")
            print(f"   Type: {station['type']}")
            print(f"   Dependencies: {station['dependencies'] if station['dependencies'] else 'None'}")
            print(f"   Python: {station['file_path'].name}")
            print(f"   Config: {station['config_path'].name if station['config_path'] else 'None'}")
            
            test_script = self.find_test_script(num)
            if test_script:
                print(f"   Test: {test_script.name}")
        
        print("\n" + "="*80)
        print(f"Total custom stations: {len(custom_stations)}\n")
        
        return custom_stations
    
    def confirm_removal(self, station_num: float, station_info: Dict) -> bool:
        """Ask user to confirm station removal"""
        print("\n⚠️  CONFIRM REMOVAL")
        print("="*80)
        print(f"Station {station_num}: {station_info['name']}")
        print(f"Type: {station_info['type']}")
        print("\nFiles to be deleted:")
        print(f"  • {station_info['file_path']}")
        if station_info['config_path']:
            print(f"  • {station_info['config_path']}")
        
        test_script = self.find_test_script(station_num)
        if test_script:
            print(f"  • {test_script}")
        
        print("="*80)
        
        response = input("\n❓ Proceed with removal? (yes/no): ").strip().lower()
        return response in ['yes', 'y']
    
    def remove_station(self, station_num: float, skip_confirmation: bool = False) -> bool:
        """Remove a specific station"""
        custom_stations = self.get_custom_stations()
        
        if station_num not in custom_stations:
            if station_num in self.protected_stations:
                print(f"\n❌ Cannot remove Station {station_num}: Protected built-in station")
                print("   Only custom stations (number > 20) can be removed.\n")
            else:
                print(f"\n❌ Station {station_num} not found\n")
            return False
        
        station_info = custom_stations[station_num]
        
        # Confirm removal
        if not skip_confirmation:
            if not self.confirm_removal(station_num, station_info):
                print("\n❌ Removal cancelled by user\n")
                return False
        
        # Remove files
        print(f"\n🗑️  Removing Station {station_num}...")
        
        try:
            # Remove Python file
            if station_info['file_path'].exists():
                station_info['file_path'].unlink()
                print(f"   ✓ Deleted: {station_info['file_path'].name}")
            
            # Remove config file
            if station_info['config_path'] and station_info['config_path'].exists():
                station_info['config_path'].unlink()
                print(f"   ✓ Deleted: {station_info['config_path'].name}")
            
            # Remove test script
            test_script = self.find_test_script(station_num)
            if test_script and test_script.exists():
                test_script.unlink()
                print(f"   ✓ Deleted: {test_script.name}")
            
            print(f"\n✅ Station {station_num} removed successfully!")
            print("\nℹ️  The dynamic automation scripts will automatically detect the removal.")
            print("   No manual code updates needed!\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error removing station {station_num}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def remove_all_custom(self):
        """Remove all custom stations"""
        custom_stations = self.get_custom_stations()
        
        if not custom_stations:
            print("\n📭 No custom stations to remove\n")
            return
        
        print("\n⚠️  REMOVE ALL CUSTOM STATIONS")
        print("="*80)
        print(f"This will remove {len(custom_stations)} custom station(s):\n")
        
        for num in sorted(custom_stations.keys()):
            station = custom_stations[num]
            print(f"  • Station {num}: {station['name']}")
        
        print("\n" + "="*80)
        
        response = input("\n❓ Remove ALL custom stations? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            print("\n❌ Operation cancelled\n")
            return
        
        print("\n🗑️  Removing all custom stations...\n")
        
        removed = 0
        failed = 0
        
        for num in sorted(custom_stations.keys()):
            if self.remove_station(num, skip_confirmation=True):
                removed += 1
            else:
                failed += 1
        
        print("\n" + "="*80)
        print(f"✅ Removal complete: {removed} removed, {failed} failed")
        print("="*80 + "\n")
    
    def show_updated_pipeline(self):
        """Show the pipeline after removal"""
        print("\n🔄 Reloading station registry...\n")
        registry = reload_registry()
        registry.print_pipeline()
        
        custom = self.get_custom_stations()
        if custom:
            print(f"ℹ️  {len(custom)} custom station(s) remaining\n")
        else:
            print("ℹ️  All custom stations removed. Only built-in stations remain.\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Remove custom stations created with station_creator_wizard.py'
    )
    parser.add_argument(
        '--station',
        type=float,
        help='Station number to remove (e.g., 21 or 21.5)'
    )
    parser.add_argument(
        '--all-custom',
        action='store_true',
        help='Remove all custom stations (number > 20)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all custom stations without removing'
    )
    
    args = parser.parse_args()
    
    remover = StationRemover()
    
    print("\n" + "🗑️"*40)
    print("   CUSTOM STATION REMOVAL TOOL")
    print("🗑️"*40 + "\n")
    
    # List mode
    if args.list:
        remover.list_custom_stations()
        return
    
    # Remove specific station
    if args.station:
        success = remover.remove_station(args.station)
        if success:
            remover.show_updated_pipeline()
        return
    
    # Remove all custom stations
    if args.all_custom:
        remover.remove_all_custom()
        remover.show_updated_pipeline()
        return
    
    # Interactive mode
    custom_stations = remover.list_custom_stations()
    
    if not custom_stations:
        return
    
    print("Choose an option:")
    print("  1. Remove a specific station")
    print("  2. Remove all custom stations")
    print("  3. Cancel")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        station_num = input("\nEnter station number to remove: ").strip()
        try:
            station_num = float(station_num) if '.' in station_num else int(station_num)
            success = remover.remove_station(station_num)
            if success:
                remover.show_updated_pipeline()
        except ValueError:
            print("\n❌ Invalid station number\n")
    
    elif choice == '2':
        remover.remove_all_custom()
        remover.show_updated_pipeline()
    
    else:
        print("\n❌ Cancelled\n")


if __name__ == "__main__":
    main()

