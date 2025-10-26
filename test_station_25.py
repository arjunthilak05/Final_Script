"""
Test script for Station 25 - Audio Optimization
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
        if "continue" in prompt.lower():
            return "n"
        return ""

# Replace input
__builtins__.input = mock_input

from app.agents.station_25_audio_optimization import Station25AudioOptimization

async def test_station_25():
    """Test Station 25"""
    session_id = "session_20251016_235335"

    station = Station25AudioOptimization(session_id, skip_review=True)
    await station.initialize()
    await station.run()

if __name__ == "__main__":
    asyncio.run(test_station_25())
