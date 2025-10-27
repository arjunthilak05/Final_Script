"""
Script to push specific session data to Redis and remove all other sessions.

Usage:
    python push_session_to_redis.py <session_id>
"""

import asyncio
import json
import csv
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import redis.asyncio as redis
from app.config import settings


class SessionToRedis:
    def __init__(self, target_session: str):
        self.target_session = target_session
        self.redis_client: redis.Redis = None
        self.output_dir = Path("output")
        self.stations: set = set()

    async def connect(self):
        """Connect to Redis"""
        self.redis_client = redis.from_url(settings.redis_url)
        await self.redis_client.ping()
        print("✓ Connected to Redis")

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.aclose()
            print("✓ Disconnected from Redis")

    def extract_session_id(self, filename: str) -> str:
        """Extract session ID from filename"""
        # Format: session_20251016_235335_...
        if "session_" in filename:
            parts = filename.split("_")
            if len(parts) >= 3:
                return f"session_{parts[1]}_{parts[2]}"
        return "unknown"

    def extract_station_number(self, station_dir: str) -> str:
        """Extract station number from directory name"""
        # Format: station_04, station_045, etc.
        return station_dir.replace("station_", "")

    def csv_to_dict_list(self, csv_path: Path) -> List[Dict]:
        """Convert CSV file to list of dictionaries"""
        result = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                result.append(dict(row))
        return result

    async def push_file(self, file_path: Path, station_number: str, session_id: str):
        """Push a single file to Redis"""
        if session_id != self.target_session:
            return  # Skip files not from target session

        file_type = file_path.suffix.lower()
        file_name = file_path.stem

        # Special handling for Station 27 with episode subdirectories
        if station_number == "27":
            # Extract episode info from path
            episode_dir = file_path.parent.name  # e.g., "episode_01"
            category = file_name
            # Create key with episode info
            redis_key = f"station_{station_number}:{session_id}:{episode_dir}:{category}"
        else:
            # Determine the file category from filename
            category = file_name.replace(f"{session_id}_", "")
            # Create Redis key
            redis_key = f"{session_id}:station:{station_number}:{category}"

        try:
            if file_type == ".json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                await self.redis_client.set(redis_key, json.dumps(data))
                print(f"  ✓ Pushed JSON: {redis_key}")

            elif file_type == ".csv":
                data = self.csv_to_dict_list(file_path)
                await self.redis_client.set(redis_key, json.dumps(data))
                print(f"  ✓ Pushed CSV: {redis_key}")

            elif file_type == ".txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                await self.redis_client.set(redis_key, data)
                print(f"  ✓ Pushed TXT: {redis_key}")

            elif file_type == ".md":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                await self.redis_client.set(redis_key, data)
                print(f"  ✓ Pushed MD: {redis_key}")

            else:
                print(f"  ⚠ Skipped: {file_path}")

        except Exception as e:
            print(f"  ✗ Error pushing {file_path}: {e}")

    async def push_station(self, station_path: Path):
        """Push all files from a station directory"""
        station_number = self.extract_station_number(station_path.name)
        self.stations.add(station_number)

        print(f"\n📁 Station {station_number}...")

        pushed_count = 0
        
        # Special handling for Station 27 (episode subdirectories)
        if station_number == "27":
            # Check episode subdirectories
            episode_dirs = [d for d in station_path.iterdir() if d.is_dir() and d.name.startswith("episode_")]
            
            for episode_dir in episode_dirs:
                files = list(episode_dir.glob("*"))
                for file_path in files:
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        # Read file to check session_id
                        if file_path.suffix == '.json':
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                    if data.get('session_id') == self.target_session:
                                        await self.push_file(file_path, station_number, self.target_session)
                                        pushed_count += 1
                            except:
                                pass
                        elif file_path.suffix in ['.txt', '.md', '.fountain']:
                            await self.push_file(file_path, station_number, self.target_session)
                            pushed_count += 1
        
        else:
            # Standard handling for other stations
            files = list(station_path.glob("*"))
            
            for file_path in files:
                if file_path.is_file() and not file_path.name.startswith('.'):
                    session_id = self.extract_session_id(file_path.name)
                    if session_id == self.target_session:
                        await self.push_file(file_path, station_number, session_id)
                        pushed_count += 1

        if pushed_count == 0:
            print(f"  (No files for {self.target_session})")

    async def clear_all_sessions(self):
        """Clear ALL session data from Redis"""
        print("\n🗑️  Clearing all existing session data from Redis...")
        
        # Get all keys matching session pattern
        keys_to_delete = []
        cursor = 0
        
        while True:
            cursor, keys = await self.redis_client.scan(cursor, match="*", count=1000)
            for key in keys:
                # Convert bytes to string
                key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                
                # Delete all keys except those matching target session
                if not key_str.startswith(f"{self.target_session}:"):
                    keys_to_delete.append(key)
            if cursor == 0:
                break
        
        if keys_to_delete:
            await self.redis_client.delete(*keys_to_delete)
            print(f"✓ Cleared {len(keys_to_delete)} keys")
        else:
            print("✓ No existing data to clear")

    async def run(self):
        """Main execution method"""
        try:
            await self.connect()

            # Clear all existing data first
            await self.clear_all_sessions()

            # Check if output directory exists
            if not self.output_dir.exists():
                print(f"✗ Output directory not found: {self.output_dir}")
                return

            # Process each station directory
            station_dirs = [d for d in self.output_dir.iterdir()
                          if d.is_dir() and d.name.startswith("station_")]

            if not station_dirs:
                print("✗ No station directories found in output/")
                return

            print(f"\n📊 Processing {len(station_dirs)} station(s) for session: {self.target_session}")

            for station_path in sorted(station_dirs):
                await self.push_station(station_path)

            # Store list of stations for this session
            await self.redis_client.set(
                f"{self.target_session}:stations",
                json.dumps(sorted(list(self.stations)))
            )
            print(f"\n✓ Stored {len(self.stations)} station(s) for session {self.target_session}")

            print("\n" + "="*70)
            print(f"✅ Successfully pushed session {self.target_session} to Redis!")
            print("="*70)

        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


async def main():
    """Entry point"""
    if len(sys.argv) < 2:
        print("Usage: python push_session_to_redis.py <session_id>")
        print("Example: python push_session_to_redis.py session_20251023_112749")
        sys.exit(1)

    target_session = sys.argv[1]
    
    print("="*70)
    print(f"📤 Pushing Session: {target_session}")
    print("="*70)
    
    pusher = SessionToRedis(target_session)
    await pusher.run()


if __name__ == "__main__":
    asyncio.run(main())

