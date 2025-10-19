#!/usr/bin/env python3
"""
Quick script to retrieve specific data from Redis.

Usage:
    python get_redis_data.py <session_id> <station> <category>
    python get_redis_data.py --list-sessions
    python get_redis_data.py --list-stations
    python get_redis_data.py <session_id> --list-data

Examples:
    python get_redis_data.py session_20251016_235335 04 seeds
    python get_redis_data.py session_20251016_235335 09 audio_cues
    python get_redis_data.py --list-sessions
    python get_redis_data.py session_20251016_235335 --list-data
"""

import asyncio
import json
import sys
from query_redis import RedisQuery


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    query = RedisQuery()
    await query.connect()

    try:
        # List sessions
        if sys.argv[1] == "--list-sessions":
            sessions = await query.get_sessions()
            print("\nAvailable Sessions:")
            for session in sessions:
                stations = await query.get_session_stations(session)
                print(f"  {session}")
                print(f"    Stations: {', '.join(stations)}")
            return

        # List stations
        if sys.argv[1] == "--list-stations":
            stations = await query.get_stations()
            print("\nAvailable Stations:")
            for station in sorted(stations):
                print(f"  Station {station}")
            return

        # List data for a session
        if len(sys.argv) == 3 and sys.argv[2] == "--list-data":
            session_id = sys.argv[1]
            keys = await query.list_session_data(session_id)
            print(f"\nData keys for {session_id}:")
            for key in sorted(keys):
                # Extract station and category from key
                parts = key.split(":")
                if len(parts) >= 4:
                    station = parts[-2]
                    category = parts[-1]
                    print(f"  Station {station:>3} → {category}")
            return

        # Get specific data
        if len(sys.argv) == 4:
            session_id = sys.argv[1]
            station = sys.argv[2]
            category = sys.argv[3]

            data = await query.get_session_station_data(session_id, station, category)

            if data is None:
                print(f"\n❌ No data found for:")
                print(f"   Session: {session_id}")
                print(f"   Station: {station}")
                print(f"   Category: {category}")
                print("\nTry running with --list-sessions or --list-data to see available data")
                sys.exit(1)

            print(json.dumps(data, indent=2))
            return

        print(__doc__)

    finally:
        await query.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
