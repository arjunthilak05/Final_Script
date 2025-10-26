"""
Script to push all output folder contents to Redis.

Key structure:
- session:{session_id}:metadata - JSON metadata about the session
- session:{session_id}:station:{station_number}:{file_type} - Specific file data
- sessions:list - List of all session IDs
- stations:list - List of all station numbers

File types handled:
- JSON files: Stored as JSON strings
- CSV files: Stored as JSON array of objects
- TXT files: Stored as text
"""

import asyncio
import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Any
import redis.asyncio as redis
from app.config import settings


class OutputToRedis:
    def __init__(self):
        self.redis_client: redis.Redis = None
        self.output_dir = Path("output")
        self.sessions: set = set()
        self.stations: set = set()

    async def connect(self):
        """Connect to Redis"""
        self.redis_client = redis.from_url(settings.redis_url)
        await self.redis_client.ping()
        print("✓ Connected to Redis")

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
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
        file_type = file_path.suffix.lower()
        file_name = file_path.stem

        # Determine the file category from filename
        category = file_name.replace(f"{session_id}_", "")

        # Create Redis key
        redis_key = f"session:{session_id}:station:{station_number}:{category}"

        try:
            if file_type == ".json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                await self.redis_client.set(redis_key, json.dumps(data))
                print(f"  → Pushed JSON: {redis_key}")

            elif file_type == ".csv":
                data = self.csv_to_dict_list(file_path)
                await self.redis_client.set(redis_key, json.dumps(data))
                print(f"  → Pushed CSV: {redis_key}")

            elif file_type == ".txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                await self.redis_client.set(redis_key, data)
                print(f"  → Pushed TXT: {redis_key}")

            else:
                print(f"  ⚠ Skipped unsupported file type: {file_path}")

        except Exception as e:
            print(f"  ✗ Error pushing {file_path}: {e}")

    async def push_station(self, station_path: Path):
        """Push all files from a station directory"""
        station_number = self.extract_station_number(station_path.name)
        self.stations.add(station_number)

        print(f"\nProcessing Station {station_number}...")

        # Get all files in the station directory
        files = list(station_path.glob("*"))

        for file_path in files:
            if file_path.is_file() and not file_path.name.startswith('.'):
                session_id = self.extract_session_id(file_path.name)
                self.sessions.add(session_id)
                await self.push_file(file_path, station_number, session_id)

    async def push_metadata(self):
        """Push metadata about sessions and stations"""
        # Store list of all sessions
        await self.redis_client.set("sessions:list", json.dumps(list(self.sessions)))
        print(f"\n✓ Stored {len(self.sessions)} session(s)")

        # Store list of all stations
        await self.redis_client.set("stations:list", json.dumps(sorted(list(self.stations))))
        print(f"✓ Stored {len(self.stations)} station(s)")

        # Store session-station mapping
        for session_id in self.sessions:
            session_stations = []
            for station_number in self.stations:
                # Check if this session has data for this station
                pattern = f"session:{session_id}:station:{station_number}:*"
                keys = await self.redis_client.keys(pattern)
                if keys:
                    session_stations.append(station_number)

            await self.redis_client.set(
                f"session:{session_id}:stations",
                json.dumps(sorted(session_stations))
            )
            print(f"  → {session_id} has data for stations: {sorted(session_stations)}")

    async def clear_existing_data(self):
        """Clear existing session data from Redis"""
        print("\nClearing existing session data...")
        keys = await self.redis_client.keys("session:*")
        keys.extend(await self.redis_client.keys("sessions:*"))
        keys.extend(await self.redis_client.keys("stations:*"))

        if keys:
            await self.redis_client.delete(*keys)
            print(f"✓ Cleared {len(keys)} existing keys")
        else:
            print("✓ No existing data to clear")

    async def run(self, clear_first: bool = True):
        """Main execution method"""
        try:
            await self.connect()

            if clear_first:
                await self.clear_existing_data()

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

            print(f"\nFound {len(station_dirs)} station(s) to process")

            for station_path in sorted(station_dirs):
                await self.push_station(station_path)

            # Push metadata
            await self.push_metadata()

            print("\n" + "="*60)
            print("✓ Successfully pushed all data to Redis!")
            print("="*60)

        except Exception as e:
            print(f"\n✗ Error: {e}")
        finally:
            await self.disconnect()


async def main():
    """Entry point"""
    import sys

    clear_first = True
    if len(sys.argv) > 1 and sys.argv[1] == "--no-clear":
        clear_first = False

    pusher = OutputToRedis()
    await pusher.run(clear_first=clear_first)


if __name__ == "__main__":
    print("="*60)
    print("Output to Redis Pusher")
    print("="*60)
    asyncio.run(main())
