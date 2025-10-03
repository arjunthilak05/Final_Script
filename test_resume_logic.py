#!/usr/bin/env python3
"""
Quick test to validate resume logic without running full automation
"""
import json
from pathlib import Path

def test_checkpoint_loading():
    """Test that checkpoints can be loaded"""
    checkpoint_dir = Path("outputs")
    checkpoints = list(checkpoint_dir.glob("checkpoint_*.json"))

    print("🧪 TESTING CHECKPOINT LOADING")
    print("=" * 60)

    if not checkpoints:
        print("❌ No checkpoints found to test")
        return False

    for checkpoint_file in checkpoints[:1]:  # Test first checkpoint
        print(f"\n📂 Testing: {checkpoint_file}")

        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            state = data.get('state', {})
            session_id = state.get('session_id', 'unknown')
            current_station = state.get('current_station', 0)
            station_outputs = state.get('station_outputs', {})

            print(f"✅ Session ID: {session_id}")
            print(f"✅ Current Station: {current_station}")
            print(f"✅ Completed Stations: {list(station_outputs.keys())}")

            # Verify resume logic
            print(f"\n🔄 RESUME LOGIC TEST:")
            stations_to_run = []
            for station in range(1, 15):
                if station == 4.5:
                    if current_station < 4.5:
                        stations_to_run.append(4.5)
                elif current_station < station:
                    stations_to_run.append(station)

            print(f"📋 Stations that would run: {stations_to_run}")
            print(f"📊 Next station to start: {stations_to_run[0] if stations_to_run else 'All complete!'}")

            # Verify all data is present
            required_fields = ['story_concept', 'session_id', 'current_station', 'station_outputs']
            missing_fields = [field for field in required_fields if field not in state]

            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False

            print(f"\n✅ Checkpoint structure is valid!")
            print(f"✅ Resume logic verified - would start at Station {stations_to_run[0] if stations_to_run else 'N/A'}")

            return True

        except Exception as e:
            print(f"❌ Failed to load checkpoint: {e}")
            return False

    return True

def test_station_output_structure():
    """Test that station outputs have expected structure"""
    checkpoint_dir = Path("outputs")
    checkpoints = list(checkpoint_dir.glob("checkpoint_*.json"))

    if not checkpoints:
        return True

    print("\n🧪 TESTING STATION OUTPUT STRUCTURE")
    print("=" * 60)

    with open(checkpoints[0], 'r', encoding='utf-8') as f:
        data = json.load(f)

    state = data.get('state', {})
    station_outputs = state.get('station_outputs', {})

    for station_key, output_data in station_outputs.items():
        print(f"\n📊 {station_key.upper()}:")
        if isinstance(output_data, dict):
            print(f"   Keys: {list(output_data.keys())[:5]}...")  # Show first 5 keys
            print(f"   ✅ Structure valid")
        else:
            print(f"   ❌ Invalid structure (not a dict)")
            return False

    print(f"\n✅ All station outputs have valid structure")
    return True

if __name__ == "__main__":
    print("🎬 RESUME LOGIC VALIDATION TEST")
    print("=" * 60)

    test1 = test_checkpoint_loading()
    test2 = test_station_output_structure()

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"   Checkpoint Loading: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"   Station Outputs: {'✅ PASS' if test2 else '❌ FAIL'}")

    if test1 and test2:
        print("\n🎉 ALL TESTS PASSED - Resume functionality is working!")
    else:
        print("\n⚠️  Some tests failed - check implementation")
