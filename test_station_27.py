"""
Test script for Station 27 - Master Script Assembly
Auto-accepts review for testing
"""
import asyncio
import sys

# Mock input to auto-accept
original_input = input

def mock_input(prompt):
    """Auto-accept all prompts"""
    if "session ID" in prompt:
        return "session_20251016_235335"
    elif "Enter episode number" in prompt or "Your choice:" in prompt:
        return "1"  # Auto-select first episode
    else:
        # For any other input, just auto-accept (return empty or "y")
        if "continue" in prompt.lower() or "again" in prompt.lower():
            return "n"  # Don't continue after first episode
        return ""  # Default to accepting/continuing

# Replace input
__builtins__.input = mock_input

from app.agents.station_27_master_script_assembly import Station27MasterScriptAssembly

async def test_station_27():
    """Test Station 27"""
    session_id = "session_20251016_235335"

    station = Station27MasterScriptAssembly(session_id, skip_review=True)
    await station.initialize()
    await station.run()

if __name__ == "__main__":
    asyncio.run(test_station_27())
