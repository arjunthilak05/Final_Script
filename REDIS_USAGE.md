# Redis Data Storage

This project includes scripts to push and query data from the `output/` folder to Redis.

## Overview

All output files are organized in Redis with a hierarchical key structure:

```
session:{session_id}:station:{station_number}:{file_type}
```

For example:
- `session:session_20251016_235335:station:04:seeds` - CSV data for seeds from station 04
- `session:session_20251016_235335:station:01:output` - JSON output from station 01
- `session:session_20251016_235335:station:09:audio_cues` - Audio cues CSV from station 09

## Scripts

### 1. Push Data to Redis (`push_to_redis.py`)

Pushes all data from the `output/` folder to Redis.

**Usage:**
```bash
# Push all data (clears existing data first)
python push_to_redis.py

# Push without clearing existing data
python push_to_redis.py --no-clear
```

**Features:**
- Automatically detects and processes all station directories
- Handles JSON, CSV, and TXT files
- Creates metadata about sessions and stations
- Maps which stations have data for each session

**Data Stored:**
- `sessions:list` - List of all session IDs
- `stations:list` - List of all station numbers
- `session:{session_id}:stations` - List of stations for each session
- All individual file contents with proper key structure

### 2. Query Data from Redis (`query_redis.py`)

Interactive tool to explore data stored in Redis.

**Usage:**
```bash
python query_redis.py
```

**Features:**
- Lists all sessions and stations
- Shows sample data
- Displays key structures
- Pretty-prints JSON data

### 3. Programmatic Access

You can also use the RedisQuery class in your own scripts:

```python
from query_redis import RedisQuery
import asyncio

async def get_data():
    query = RedisQuery()
    await query.connect()

    # Get all sessions
    sessions = await query.get_sessions()

    # Get stations for a session
    stations = await query.get_session_stations("session_20251016_235335")

    # Get specific data
    seeds_data = await query.get_session_station_data(
        "session_20251016_235335",
        "04",
        "seeds"
    )

    # Get all data for a session
    all_data = await query.get_all_session_data("session_20251016_235335")

    await query.disconnect()

asyncio.run(get_data())
```

## Key Structure

### Metadata Keys
- `sessions:list` - Array of all session IDs
- `stations:list` - Array of all station numbers
- `session:{session_id}:stations` - Array of station numbers for this session

### Data Keys
Pattern: `session:{session_id}:station:{station_number}:{category}`

Where:
- `{session_id}` - Format: `session_YYYYMMDD_HHMMSS`
- `{station_number}` - Station identifier (e.g., "01", "04", "045", "10")
- `{category}` - File type/category (e.g., "seeds", "output", "readable", "audio_cues")

## Data Types

### JSON Files
Stored as JSON strings. Examples:
- `output.json` → Stored under key `...:output`
- `style_guide.json` → Stored under key `...:style_guide`

### CSV Files
Converted to JSON array of objects. Examples:
- `seeds.csv` → Array of seed objects
- `audio_cues.csv` → Array of audio cue objects
- `plant_proof_payoff_grid.csv` → Array of grid items

### TXT Files
Stored as plain text. Examples:
- `readable.txt` → Plain text content
- `style_guide.txt` → Plain text content

## Example Queries

### Using redis-cli

```bash
# List all sessions
redis-cli GET sessions:list

# Get all keys for a session
redis-cli KEYS "session:session_20251016_235335:*"

# Get specific data
redis-cli GET "session:session_20251016_235335:station:04:seeds"

# Count total keys
redis-cli DBSIZE

# Get stations for a session
redis-cli GET "session:session_20251016_235335:stations"
```

## Requirements

- Redis server running locally (default: `localhost:6379`)
- Python packages: `redis`, `pydantic-settings`

Install with:
```bash
pip install redis pydantic-settings
```

## Configuration

Redis connection is configured in `app/config.py`:
```python
redis_url: str = "redis://localhost:6379/0"
```

You can override this in your `.env` file:
```env
REDIS_URL=redis://localhost:6379/0
```

## Current Data Summary

After running `push_to_redis.py`, you'll have:
- 5 sessions stored
- 11 stations (01, 02, 03, 04, 045, 05, 06, 07, 08, 09, 10)
- 46 total keys in Redis
- Mix of JSON, CSV (as JSON arrays), and TXT data

The most complete session is `session_20251016_235335` with data across all 11 stations.
