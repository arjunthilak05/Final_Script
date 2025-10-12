#!/usr/bin/env python3
"""
Resume Automation with Dynamic Station Discovery

Automatically discovers stations and resumes from any point.
Picks up where you left off using saved checkpoints.

Usage:
    python resume_automation_dynamic.py
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.append(str(Path(__file__).parent / "app"))

from app.agents.station_registry import get_station_registry, reload_registry
from app.redis_client import RedisClient
from full_automation_dynamic import DynamicAutomationRunner


async def list_existing_sessions():
    """List all existing sessions in Redis"""
    redis = RedisClient()
    await redis.initialize()
    
    try:
        # Get all pipeline state keys
        keys = await redis.redis.keys("audiobook:*:pipeline_state")
        
        if not keys:
            print("\n📭 No existing sessions found in Redis.\n")
            return []
        
        sessions = []
        print("\n📋 EXISTING SESSIONS:")
        print("="*70)
        
        for key in keys:
            key_str = key.decode() if isinstance(key, bytes) else key
            session_id = key_str.split(':')[1]
            
            # Get session data
            data_json = await redis.get(key_str)
            if data_json:
                data = json.loads(data_json)
                
                status = data.get('status', 'unknown')
                completed = len(data.get('completed_stations', []))
                concept = data.get('story_concept', 'N/A')[:50]
                start_time = data.get('start_time', 'unknown')
                
                sessions.append({
                    'session_id': session_id,
                    'status': status,
                    'completed_stations': completed,
                    'concept': concept,
                    'data': data
                })
                
                status_icon = {
                    'completed': '✅',
                    'interrupted': '⚠️',
                    'failed': '❌',
                    'running': '🔄'
                }.get(status, '❓')
                
                print(f"\n{status_icon} Session: {session_id}")
                print(f"   Status: {status}")
                print(f"   Completed: {completed} stations")
                print(f"   Concept: {concept}...")
                print(f"   Started: {start_time}")
        
        print("="*70 + "\n")
        return sessions
        
    finally:
        await redis.disconnect()


async def resume_from_station(session_id: str, start_from_station: float = None):
    """Resume automation from a specific station"""
    
    # Initialize Redis and load state
    redis = RedisClient()
    await redis.initialize()
    
    state_key = f"audiobook:{session_id}:pipeline_state"
    state_json = await redis.get(state_key)
    
    if not state_json:
        print(f"\n❌ No saved state found for session: {session_id}")
        print(f"   Cannot resume. Please start a new session.\n")
        return
    
    state = json.loads(state_json)
    
    # Parse datetime strings back to datetime objects
    if 'start_time' in state and isinstance(state['start_time'], str):
        state['start_time'] = datetime.fromisoformat(state['start_time'])
    
    print(f"\n✅ Found existing session: {session_id}")
    print(f"   Status: {state.get('status', 'unknown')}")
    print(f"   Completed stations: {state.get('completed_stations', [])}")
    print(f"   Concept: {state.get('story_concept', 'N/A')[:60]}...\n")
    
    # Get station registry
    registry = reload_registry()
    registry.print_pipeline()
    
    execution_order = registry.get_execution_order()
    
    # Determine where to start
    completed = set(state.get('completed_stations', []))
    
    if start_from_station is not None:
        # User specified a starting point
        remaining_stations = [s for s in execution_order if s >= start_from_station]
        print(f"\n🔄 Resuming from Station {start_from_station} as requested")
    else:
        # Auto-detect next station
        remaining_stations = [s for s in execution_order if s not in completed]
        if remaining_stations:
            print(f"\n🔄 Auto-resuming from Station {remaining_stations[0]}")
        else:
            print(f"\n✅ All stations already completed!")
            return
    
    if not remaining_stations:
        print(f"\n✅ No stations left to run. Pipeline complete!\n")
        return
    
    print(f"   Will run {len(remaining_stations)} stations: {remaining_stations}\n")
    
    # Confirm with user
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("\n❌ Cancelled by user\n")
        return
    
    # Create runner and resume
    runner = DynamicAutomationRunner(auto_approve=True, debug_mode=False)
    runner.current_session_id = session_id
    runner.redis = redis
    
    try:
        total_stations = len(remaining_stations)
        for idx, station_num in enumerate(remaining_stations, 1):
            print(f"\n{'─'*70}")
            print(f"Progress: [{idx}/{total_stations}] Station {station_num}")
            print(f"{'─'*70}")
            
            state = await runner.run_station(station_num, session_id, state)
            state['completed_stations'].append(station_num)
            
            # Save checkpoint
            await runner._save_checkpoint(session_id, state)
        
        # Mark as complete
        state['status'] = 'completed'
        state['end_time'] = datetime.now()
        await runner._save_checkpoint(session_id, state)
        
        duration = state['end_time'] - state['start_time']
        
        print("\n" + "="*80)
        print("🎉 RESUME COMPLETE!")
        print("="*80)
        print(f"✓ Session ID: {session_id}")
        print(f"✓ Total stations completed: {len(state['completed_stations'])}")
        print(f"✓ Total duration: {duration}")
        print(f"✓ Status: Pipeline completed successfully")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Progress saved.")
        state['status'] = 'interrupted'
        state['interrupted_at'] = datetime.now()
        await runner._save_checkpoint(session_id, state)
        
    except Exception as e:
        print(f"\n\n❌ Error during resume: {e}")
        state['status'] = 'failed'
        state['error'] = str(e)
        state['failed_at'] = datetime.now()
        await runner._save_checkpoint(session_id, state)
        logger.exception("Full error details:")
    
    finally:
        await redis.disconnect()


async def main():
    """Main entry point"""
    print("\n" + "🔄"*40)
    print("   RESUME AUTOMATION (Dynamic Discovery)")
    print("🔄"*40 + "\n")
    
    print("This tool allows you to continue interrupted or failed pipelines.")
    print("All stations are auto-discovered from app/agents/\n")
    
    # List existing sessions
    sessions = await list_existing_sessions()
    
    if not sessions:
        print("Start a new session with: python full_automation_dynamic.py\n")
        return
    
    # Get session ID
    session_id = input("📝 Enter session ID to resume: ").strip()
    
    if not session_id:
        print("❌ Session ID required\n")
        return
    
    # Ask if user wants to start from specific station
    print("\n" + "─"*70)
    print("Resume options:")
    print("  1. Auto-resume (continues from where it left off)")
    print("  2. Start from specific station (re-run from a chosen point)")
    print("─"*70)
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    start_from = None
    if choice == '2':
        station_input = input("Enter station number to start from: ").strip()
        try:
            start_from = float(station_input) if '.' in station_input else int(station_input)
        except:
            print("❌ Invalid station number\n")
            return
    
    # Resume
    await resume_from_station(session_id, start_from)


if __name__ == "__main__":
    asyncio.run(main())

