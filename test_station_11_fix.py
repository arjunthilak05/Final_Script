#!/usr/bin/env python3
"""
Quick test to verify Station 11 fixes are working
Tests both enable_debug_mode() and format string handling
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / "app"))

async def test_station_11():
    """Test Station 11 with fixes applied"""

    print("🧪 Testing Station 11 Fixes")
    print("=" * 60)

    try:
        from app.agents.station_11_runtime_planning import Station11RuntimePlanning

        # Test 1: Instantiation
        print("\n1️⃣  Testing instantiation...")
        station = Station11RuntimePlanning()
        print("   ✅ Station 11 instantiated successfully")

        # Test 2: Debug mode
        print("\n2️⃣  Testing debug mode...")
        if hasattr(station, 'enable_debug_mode'):
            station.enable_debug_mode()
            print("   ✅ enable_debug_mode() method exists and works")
        else:
            print("   ❌ enable_debug_mode() method missing!")
            return False

        # Test 3: Check debug_mode attribute
        print("\n3️⃣  Testing debug_mode attribute...")
        if hasattr(station, 'debug_mode'):
            print(f"   ✅ debug_mode attribute exists: {station.debug_mode}")
        else:
            print("   ❌ debug_mode attribute missing!")
            return False

        # Test 4: Initialize
        print("\n4️⃣  Testing initialization...")
        await station.initialize()
        print("   ✅ Station initialized successfully")

        # Test 5: Test _format_txt_output with nested dicts
        print("\n5️⃣  Testing format string handling...")

        # Create a mock RuntimePlanningGrid with nested dict values
        from dataclasses import dataclass
        from typing import Dict, Any, List

        @dataclass
        class MockWordBudget:
            spoken_words_per_minute: int = 155
            total_words_per_episode: int = 8000
            dialogue_ratio: float = 0.65
            narration_ratio: float = 0.35
            sfx_silence_allowance: float = 0.08
            word_count_variation_range: str = "±15%"

        @dataclass
        class MockPacingVariation:
            # Include nested dict values to test formatting
            fast_episodes: Dict[str, Any] = None
            slow_episodes: Dict[str, Any] = None
            standard_episodes: Dict[str, Any] = None
            special_format_episodes: Dict[str, Any] = None
            pacing_rhythm: str = "Test rhythm"
            audience_engagement_strategy: str = "Test strategy"

            def __post_init__(self):
                # Add nested dicts to test the fix
                if self.fast_episodes is None:
                    self.fast_episodes = {
                        "episodes": [3, 7, 10],
                        "characteristics": {"pace": "fast", "tension": "high"}  # Nested dict
                    }
                if self.slow_episodes is None:
                    self.slow_episodes = {
                        "episodes": [5, 8],
                        "word_count": "140-150 words/minute"
                    }
                if self.standard_episodes is None:
                    self.standard_episodes = {
                        "episodes": [1, 2, 4, 6, 9]
                    }
                if self.special_format_episodes is None:
                    self.special_format_episodes = {}

        @dataclass
        class MockSeriesTotals:
            total_runtime_hours: float = 10.0
            total_word_count: int = 100000
            average_pace_words_per_minute: float = 155.0
            variation_range_minutes: str = "45-60"
            total_episodes: int = 12
            average_episode_length: float = 50.0
            production_timeline_estimate: str = "6 months"

        @dataclass
        class MockRuntimeGrid:
            episode_breakdowns: List = None
            word_budgets: MockWordBudget = None
            pacing_variations: MockPacingVariation = None
            series_totals: MockSeriesTotals = None
            production_guidelines: Dict[str, str] = None
            audio_specific_considerations: Dict[str, str] = None
            quality_control_metrics: Dict[str, str] = None

            def __post_init__(self):
                if self.episode_breakdowns is None:
                    self.episode_breakdowns = []
                if self.word_budgets is None:
                    self.word_budgets = MockWordBudget()
                if self.pacing_variations is None:
                    self.pacing_variations = MockPacingVariation()
                if self.series_totals is None:
                    self.series_totals = MockSeriesTotals()
                if self.production_guidelines is None:
                    self.production_guidelines = {"test_key": "test_value"}
                if self.audio_specific_considerations is None:
                    self.audio_specific_considerations = {"test_key": "test_value"}
                if self.quality_control_metrics is None:
                    self.quality_control_metrics = {"test_key": "test_value"}

        # Create mock runtime grid with nested dicts
        mock_grid = MockRuntimeGrid()

        # Test the _format_txt_output method
        try:
            txt_output = station._format_txt_output(mock_grid)
            print("   ✅ Format string handling works with nested dicts!")

            # Verify the output contains converted values
            if "{'pace': 'fast', 'tension': 'high'}" in txt_output or \
               str({'pace': 'fast', 'tension': 'high'}) in txt_output:
                print("   ✅ Nested dict values properly converted to strings")

        except Exception as e:
            if "unsupported format string" in str(e):
                print(f"   ❌ Format string error still present: {e}")
                return False
            else:
                raise

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\n✅ Station 11 fixes verified:")
        print("   • enable_debug_mode() method works")
        print("   • debug_mode attribute exists")
        print("   • Format strings handle nested dicts")
        print("   • Initialization successful")

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test execution"""
    success = await test_station_11()

    if success:
        print("\n✅ Station 11 is ready for production!")
        sys.exit(0)
    else:
        print("\n❌ Station 11 still has issues!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
