"""
Script to query and retrieve data from Redis.

Provides convenient methods to:
- List all sessions
- List all stations
- Get data for a specific session/station
- Search for specific data types
"""

import asyncio
import json
from typing import List, Dict, Optional
import redis.asyncio as redis
from app.config import settings


class RedisQuery:
    def __init__(self):
        self.redis_client: redis.Redis = None

    async def connect(self):
        """Connect to Redis"""
        self.redis_client = redis.from_url(settings.redis_url)
        await self.redis_client.ping()

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()

    async def get_sessions(self) -> List[str]:
        """Get list of all sessions"""
        data = await self.redis_client.get("sessions:list")
        if data:
            return json.loads(data)
        return []

    async def get_stations(self) -> List[str]:
        """Get list of all stations"""
        data = await self.redis_client.get("stations:list")
        if data:
            return json.loads(data)
        return []

    async def get_session_stations(self, session_id: str) -> List[str]:
        """Get stations available for a specific session"""
        data = await self.redis_client.get(f"session:{session_id}:stations")
        if data:
            return json.loads(data)
        return []

    async def get_session_station_data(self, session_id: str, station_number: str, category: str) -> Optional[Dict]:
        """Get specific data for a session and station"""
        key = f"session:{session_id}:station:{station_number}:{category}"
        data = await self.redis_client.get(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                # Return as text if not JSON
                return {"text": data.decode('utf-8') if isinstance(data, bytes) else data}
        return None

    async def list_session_data(self, session_id: str, station_number: Optional[str] = None) -> List[str]:
        """List all data keys for a session, optionally filtered by station"""
        if station_number:
            pattern = f"session:{session_id}:station:{station_number}:*"
        else:
            pattern = f"session:{session_id}:station:*"

        keys = await self.redis_client.keys(pattern)
        return [key.decode('utf-8') if isinstance(key, bytes) else key for key in keys]

    async def get_all_session_data(self, session_id: str) -> Dict[str, any]:
        """Get all data for a session organized by station"""
        result = {}
        stations = await self.get_session_stations(session_id)

        for station in stations:
            station_data = {}
            keys = await self.list_session_data(session_id, station)

            for key in keys:
                # Extract category from key
                parts = key.split(":")
                if len(parts) >= 4:
                    category = parts[-1]
                    data = await self.redis_client.get(key)
                    if data:
                        try:
                            station_data[category] = json.loads(data)
                        except json.JSONDecodeError:
                            station_data[category] = data.decode('utf-8') if isinstance(data, bytes) else data

            result[f"station_{station}"] = station_data

        return result

    async def search_by_type(self, session_id: str, file_type: str) -> Dict[str, any]:
        """Search for all files of a specific type (e.g., 'seeds', 'output', 'audio_cues')"""
        result = {}
        pattern = f"session:{session_id}:station:*:*{file_type}*"
        keys = await self.redis_client.keys(pattern)

        for key in keys:
            key_str = key.decode('utf-8') if isinstance(key, bytes) else key
            data = await self.redis_client.get(key)
            if data:
                try:
                    result[key_str] = json.loads(data)
                except json.JSONDecodeError:
                    result[key_str] = data.decode('utf-8') if isinstance(data, bytes) else data

        return result


async def interactive_query():
    """Interactive query interface"""
    query = RedisQuery()
    await query.connect()

    try:
        print("\n" + "="*60)
        print("Redis Data Query Tool")
        print("="*60)

        # List sessions
        sessions = await query.get_sessions()
        print(f"\n📋 Available Sessions ({len(sessions)}):")
        for i, session in enumerate(sessions, 1):
            print(f"  {i}. {session}")

        if not sessions:
            print("  No sessions found in Redis")
            return

        # List stations
        stations = await query.get_stations()
        print(f"\n📋 Available Stations ({len(stations)}):")
        for i, station in enumerate(sorted(stations), 1):
            print(f"  {i}. Station {station}")

        # Show sample data
        print("\n" + "="*60)
        print("Sample Data Query")
        print("="*60)

        sample_session = sessions[0]
        print(f"\nQuerying data for: {sample_session}")

        session_stations = await query.get_session_stations(sample_session)
        print(f"\nStations in {sample_session}: {session_stations}")

        # List all keys for this session
        all_keys = await query.list_session_data(sample_session)
        print(f"\nData keys ({len(all_keys)}):")
        for key in sorted(all_keys)[:10]:  # Show first 10
            print(f"  - {key}")
        if len(all_keys) > 10:
            print(f"  ... and {len(all_keys) - 10} more")

        # Show sample content
        if all_keys:
            sample_key = all_keys[0]
            print(f"\n📄 Sample content from: {sample_key}")
            data = await query.redis_client.get(sample_key)
            if data:
                try:
                    parsed = json.loads(data)
                    # Pretty print first few items if it's a list
                    if isinstance(parsed, list) and len(parsed) > 0:
                        print(f"  Type: List with {len(parsed)} items")
                        print(f"  First item: {json.dumps(parsed[0], indent=2)[:200]}...")
                    elif isinstance(parsed, dict):
                        print(f"  Type: Dictionary with {len(parsed)} keys")
                        print(f"  Keys: {list(parsed.keys())}")
                        print(f"  Preview: {json.dumps(parsed, indent=2)[:500]}...")
                    else:
                        print(f"  {json.dumps(parsed, indent=2)[:500]}...")
                except json.JSONDecodeError:
                    text = data.decode('utf-8') if isinstance(data, bytes) else data
                    print(f"  {text[:500]}...")

    finally:
        await query.disconnect()


async def main():
    """Entry point"""
    await interactive_query()


if __name__ == "__main__":
    asyncio.run(main())
