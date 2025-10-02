#!/usr/bin/env python3
"""
Test script for Stations 12-14 integration
Tests each station individually and together with existing session data
"""

import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / "app"))

from app.redis_client import RedisClient
from app.agents.station_12_hook_cliffhanger import Station12HookCliffhanger
from app.agents.station_13_multiworld_timeline import Station13MultiworldTimeline
from app.agents.station_14_episode_blueprint import Station14EpisodeBlueprint

async def test_station_12(session_id: str):
    """Test Station 12: Hook & Cliffhanger Designer"""
    print("\n" + "="*70)
    print("TESTING STATION 12: HOOK & CLIFFHANGER DESIGNER")
    print("="*70)
    
    try:
        station = Station12HookCliffhanger(session_id)
        await station.initialize()
        result = await station.run()
        
        # Validate result structure
        assert 'station' in result
        assert 'status' in result
        assert 'statistics' in result
        assert 'outputs' in result
        
        assert result['status'] == 'complete'
        assert result['station'] == 'station_12_hook_cliffhanger'
        
        # Validate statistics
        stats = result['statistics']
        assert 'total_episodes' in stats
        assert 'hooks_designed' in stats
        assert 'cliffhangers_designed' in stats
        assert 'bridges_created' in stats
        
        assert stats['total_episodes'] > 0
        assert stats['hooks_designed'] == stats['total_episodes']
        assert stats['cliffhangers_designed'] == stats['total_episodes']
        
        # Validate outputs exist
        outputs = result['outputs']
        assert 'txt' in outputs
        assert 'json' in outputs
        assert 'pdf' in outputs
        
        # Check files exist
        for file_path in outputs.values():
            assert Path(file_path).exists(), f"Output file missing: {file_path}"
        
        print("\n✅ Station 12 Test PASSED")
        print(f"   Episodes processed: {stats['total_episodes']}")
        print(f"   Hooks designed: {stats['hooks_designed']}")
        print(f"   Cliffhangers designed: {stats['cliffhangers_designed']}")
        print(f"   Bridges created: {stats['bridges_created']}")
        print(f"   Files generated: {len(outputs)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Station 12 Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_station_13(session_id: str):
    """Test Station 13: Multi-World/Timeline Manager"""
    print("\n" + "="*70)
    print("TESTING STATION 13: MULTI-WORLD/TIMELINE MANAGER")
    print("="*70)
    
    try:
        station = Station13MultiworldTimeline(session_id)
        await station.initialize()
        result = await station.run()
        
        # Validate result structure
        assert 'station' in result
        assert 'status' in result
        assert 'is_applicable' in result
        assert 'statistics' in result
        assert 'outputs' in result
        
        assert result['status'] == 'complete'
        assert result['station'] == 'station_13_multiworld_timeline'
        
        # Validate statistics
        stats = result['statistics']
        assert 'world_count' in stats
        assert 'transition_types' in stats
        assert 'complexity_level' in stats
        
        # Validate outputs exist
        outputs = result['outputs']
        assert 'txt' in outputs
        assert 'json' in outputs
        assert 'pdf' in outputs
        
        # Check files exist
        for file_path in outputs.values():
            assert Path(file_path).exists(), f"Output file missing: {file_path}"
        
        print("\n✅ Station 13 Test PASSED")
        print(f"   Applicable: {result['is_applicable']}")
        print(f"   World count: {stats['world_count']}")
        print(f"   Transition types: {stats['transition_types']}")
        print(f"   Complexity: {stats['complexity_level']}")
        print(f"   Files generated: {len(outputs)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Station 13 Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_station_14(session_id: str):
    """Test Station 14: Simple Episode Blueprint"""
    print("\n" + "="*70)
    print("TESTING STATION 14: SIMPLE EPISODE BLUEPRINT")
    print("="*70)
    
    try:
        station = Station14EpisodeBlueprint(session_id)
        await station.initialize()
        result = await station.run()
        
        # Validate result structure
        assert 'station' in result
        assert 'status' in result
        assert 'statistics' in result
        assert 'outputs' in result
        
        assert result['status'] == 'complete'
        assert result['station'] == 'station_14_episode_blueprint'
        
        # Validate statistics
        stats = result['statistics']
        assert 'total_episodes' in stats
        assert 'blueprints_generated' in stats
        assert 'ready_for_approval' in stats
        
        assert stats['total_episodes'] > 0
        assert stats['blueprints_generated'] == stats['total_episodes']
        assert stats['ready_for_approval'] == True
        
        # Validate outputs exist
        outputs = result['outputs']
        assert 'txt' in outputs
        assert 'json' in outputs
        assert 'pdf' in outputs
        
        # Check files exist
        for file_path in outputs.values():
            assert Path(file_path).exists(), f"Output file missing: {file_path}"
        
        # Validate blueprint structure
        blueprint_bible = result['blueprint_bible']
        assert 'session_id' in blueprint_bible
        assert 'generated_at' in blueprint_bible
        assert 'total_episodes' in blueprint_bible
        assert 'episodes' in blueprint_bible
        assert 'season_overview' in blueprint_bible
        assert 'approval_checklist' in blueprint_bible
        
        assert blueprint_bible['session_id'] == session_id
        assert len(blueprint_bible['episodes']) == stats['total_episodes']
        
        # Validate episode blueprint structure
        for episode in blueprint_bible['episodes']:
            assert 'episode_number' in episode
            assert 'episode_title' in episode
            assert 'simple_summary' in episode
            assert 'why_it_matters' in episode
            assert 'character_goals' in episode
            assert 'story_connection' in episode
            assert 'production_essentials' in episode
            
            # Ensure simple_summary is substantial
            assert len(episode['simple_summary']) > 100, "Summary too short"
            
            # Ensure no dialogue markers
            summary = episode['simple_summary'].lower()
            dialogue_markers = ['"', "'", " said", " asked", " replied", " shouted"]
            for marker in dialogue_markers:
                assert marker not in summary, f"Summary contains dialogue marker: {marker}"
        
        print("\n✅ Station 14 Test PASSED")
        print(f"   Blueprints generated: {stats['blueprints_generated']}")
        print(f"   Ready for approval: {stats['ready_for_approval']}")
        print(f"   PDF location: {outputs['pdf']}")
        print(f"   Files generated: {len(outputs)}")
        print("   ✅ All blueprints validated for content structure")
        print("   ✅ No dialogue detected in summaries")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Station 14 Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_integration(session_id: str):
    """Test full integration of Stations 12-14"""
    print("\n" + "="*70)
    print("TESTING STATIONS 12-14 INTEGRATION")
    print("="*70)
    
    try:
        # Check Redis connectivity
        redis = RedisClient()
        await redis.connect()
        
        # Verify required dependencies exist
        required_keys = [
            f"audiobook:{session_id}:station_5",  # Season architecture
            f"audiobook:{session_id}:station_8",  # Character bible
            f"audiobook:{session_id}:station_9",  # World bible
        ]
        
        missing_deps = []
        for key in required_keys:
            exists = await redis.exists(key)
            if not exists:
                missing_deps.append(key)
        
        await redis.disconnect()
        
        if missing_deps:
            print(f"❌ Missing dependencies in Redis:")
            for dep in missing_deps:
                print(f"   - {dep}")
            print("\nRun the full automation pipeline through Station 9 first.")
            return False
        
        print("✅ All dependencies found in Redis")
        
        # Test sequential execution
        print("\n📋 Testing sequential execution...")
        
        # Station 12
        station12_success = await test_station_12(session_id)
        if not station12_success:
            return False
        
        # Station 13
        station13_success = await test_station_13(session_id)
        if not station13_success:
            return False
        
        # Station 14
        station14_success = await test_station_14(session_id)
        if not station14_success:
            return False
        
        # Verify Redis storage
        print(f"\n🔍 Verifying Redis storage...")
        redis = RedisClient()
        await redis.connect()
        
        station_keys = [
            f"audiobook:{session_id}:station_12",
            f"audiobook:{session_id}:station_13", 
            f"audiobook:{session_id}:station_14"
        ]
        
        for key in station_keys:
            exists = await redis.exists(key)
            assert exists, f"Station data not saved to Redis: {key}"
            
            # Verify data is valid JSON
            data = await redis.get(key)
            json.loads(data)  # Should not raise exception
        
        await redis.disconnect()
        print("✅ All station data verified in Redis")
        
        print(f"\n🎉 INTEGRATION TEST PASSED")
        print("   ✅ All stations executed successfully")
        print("   ✅ Output files generated")
        print("   ✅ Data stored in Redis")
        print("   ✅ Station 14 ready for human approval")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def check_existing_sessions():
    """Check for existing sessions that can be used for testing"""
    try:
        redis = RedisClient()
        await redis.connect()
        
        # Look for sessions with Station 9 completed
        keys = await redis.redis.keys("audiobook:*:station_9")
        sessions = []
        
        for key in keys:
            # Extract session ID: audiobook:session_id:station_9
            parts = key.decode().split(':')
            if len(parts) >= 3:
                session_id = parts[1]
                sessions.append(session_id)
        
        await redis.disconnect()
        return sessions
        
    except Exception as e:
        print(f"Error checking sessions: {e}")
        return []

def main():
    """Main test function"""
    print("🧪 STATIONS 12-14 INTEGRATION TESTS")
    print("="*70)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
        print(f"📝 Using provided session: {session_id}")
    else:
        print("🔍 Checking for existing sessions...")
        
        # Check for existing sessions
        existing_sessions = asyncio.run(check_existing_sessions())
        
        if not existing_sessions:
            print("❌ No existing sessions found!")
            print("💡 Please run the full automation pipeline first through Station 9")
            print("   Example: python full_automation.py")
            print("\nAlternatively, provide a session ID:")
            print("   python test_stations_12_14.py <session_id>")
            sys.exit(1)
        
        print(f"✅ Found {len(existing_sessions)} existing sessions:")
        for i, session in enumerate(existing_sessions[:5], 1):  # Show first 5
            print(f"   {i}. {session}")
        
        if len(existing_sessions) > 5:
            print(f"   ... and {len(existing_sessions) - 5} more")
        
        # Use the most recent session
        session_id = existing_sessions[0]
        print(f"\n🎯 Using most recent session: {session_id}")
    
    print(f"\n🚀 Starting tests with session: {session_id}")
    
    # Run integration test
    success = asyncio.run(test_integration(session_id))
    
    if success:
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED")
        print("="*70)
        print("✅ Stations 12-14 are ready for production use")
        print("✅ Integration with existing pipeline confirmed")
        print("✅ Output files generated and validated")
        print("✅ Redis storage working correctly")
        print(f"✅ Session {session_id} fully processed through Station 14")
        print("\n📄 Review the episode blueprint PDF for human approval")
        
        # Show file paths
        output_dir = Path("outputs")
        if output_dir.exists():
            print(f"\n📁 Generated files in {output_dir}:")
            for station in [12, 13, 14]:
                for ext in ['txt', 'json', 'pdf']:
                    pattern = f"station{station}_*_{session_id}.{ext}"
                    files = list(output_dir.glob(pattern))
                    for file in files:
                        print(f"   📄 {file}")
    else:
        print("\n" + "="*70)
        print("💥 TESTS FAILED")
        print("="*70)
        print("❌ One or more tests failed - check errors above")
        print("💡 Ensure you have:")
        print("   - Valid OpenRouter API key in .env")
        print("   - Redis running (if configured)")
        print("   - Completed stations 1-9 for the session")
        sys.exit(1)

if __name__ == "__main__":
    main()