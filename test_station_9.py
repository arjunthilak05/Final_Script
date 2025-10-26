"""
Test script for Station 9 - Auto-accepts review for testing
"""
import asyncio
import sys

# Mock input to auto-accept
original_input = input

def mock_input(prompt):
    """Auto-accept all prompts"""
    if "Your choice:" in prompt or "session ID" in prompt:
        if "session ID" in prompt:
            return "session_20251016_235335"
        return ""  # Auto-accept
    return original_input(prompt)

# Replace input
__builtins__.input = mock_input

from app.agents.station_09_world_building_system import Station09WorldBuildingSystem

async def test_station_9():
    """Test Station 9"""
    session_id = "session_20251016_235335"

    station = Station09WorldBuildingSystem(session_id, skip_review=True)
    await station.initialize()
    await station.run()

if __name__ == "__main__":
    asyncio.run(test_station_9())
