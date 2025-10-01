#!/usr/bin/env python3
"""
Resume Automation Script - Continue from any station using existing Redis data
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / "app"))

from app.redis_client import RedisClient
from app.agents.station_01_seed_processor import Station01SeedProcessor
from app.agents.station_02_project_dna_builder import Station02ProjectDNABuilder  
from app.agents.station_03_age_genre_optimizer import Station03AgeGenreOptimizer
from app.agents.station_04_reference_miner import Station04ReferenceMiner
from app.agents.station_04_5_narrator_strategy import Station045NarratorStrategy
from app.agents.station_05_season_architecture import Station05SeasonArchitect
from app.agents.station_06_master_style_guide import Station06MasterStyleGuideBuilder
from app.agents.station_07_reality_check import Station07RealityCheck
from app.agents.station_08_character_architecture import Station08CharacterArchitecture
from app.agents.station_09_world_building import Station09WorldBuilding

async def check_existing_sessions():
    """Check for existing sessions in Redis"""
    redis = RedisClient()
    await redis.connect()
    
    try:
        # Get all audiobook session keys
        keys = await redis.redis.keys("audiobook:*:station_*")
        sessions = {}
        
        for key in keys:
            # Extract session ID and station from key pattern: audiobook:session_id:station_XX
            parts = key.decode().split(':')
            if len(parts) >= 3:
                session_id = parts[1]
                station = parts[2]
                
                if session_id not in sessions:
                    sessions[session_id] = []
                sessions[session_id].append(station)
        
        return sessions
    finally:
        await redis.disconnect()

async def run_station(station_num: int, session_id: str):
    """Run a specific station"""
    print(f"🔄 Running Station {station_num} for session {session_id}...")
    
    try:
        if station_num == 1:
            # Station 1 needs a story concept, so we'll need to get it from user
            story_concept = input("📝 Enter story concept for new Station 1 run: ").strip()
            if not story_concept:
                print("❌ Story concept required for Station 1")
                return False
            
            station = Station01SeedProcessor()
            await station.initialize()
            result = await station.process(story_concept, session_id)
            print(f"✅ Station 1 completed: {result.original_seed[:100]}...")
            
        elif station_num == 2:
            station = Station02ProjectDNABuilder()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 2 completed: Project DNA for {result.get('working_title', 'Unknown')}")
            
        elif station_num == 3:
            station = Station03AgeGenreOptimizer()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 3 completed: Age & Genre optimization")
            
        elif station_num == 4:
            station = Station04ReferenceMiner()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 4 completed: {len(result.get('seeds', []))} seeds generated")
            
        elif station_num == 4.5:
            station = Station045NarratorStrategy()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 4.5 completed: Narrator strategy - {result.get('recommendation', 'Unknown')}")
            
        elif station_num == 5:
            station = Station05SeasonArchitect()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 5 completed: {result.get('chosen_style', 'Unknown style')}")
            
        elif station_num == 6:
            station = Station06MasterStyleGuideBuilder()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 6 completed: Master Style Guide for {result.working_title if hasattr(result, 'working_title') else 'Unknown'}")
            
        elif station_num == 7:
            station = Station07RealityCheck()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 7 completed: Reality Check - {result.pipeline_status}")
            
        elif station_num == 8:
            station = Station08CharacterArchitecture()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 8 completed: Character Bible - {result.character_count_summary['total_characters']} characters")
            
        elif station_num == 9:
            station = Station09WorldBuilding()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 9 completed: World Bible - {result.world_statistics['total_locations']} locations, {result.world_statistics['audio_cues']} audio cues")
            
        else:
            print(f"❌ Station {station_num} not supported")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Station {station_num} failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function"""
    print("🔄 RESUME AUTOMATION")
    print("=" * 40)
    print("🎯 Continue from any station using existing Redis data")
    print()
    
    # Check for existing sessions
    existing_sessions = await check_existing_sessions()
    
    if not existing_sessions:
        print("❌ No existing sessions found in Redis!")
        print("💡 Run the full automation first to create sessions.")
        return
    
    print("📋 AVAILABLE SESSIONS:")
    print("-" * 30)
    
    resumable_sessions = []
    for session_id, stations in sorted(existing_sessions.items()):
        stations.sort()
        expected_stations = ["station_01", "station_02", "station_03", "station_04", "station_04_5", "station_05", "station_06", "station_07", "station_08", "station_09"]
        
        # Find next station to resume from
        next_station = None
        for i, expected in enumerate(expected_stations, 1):
            if expected not in stations:
                next_station = i
                break
        
        if not next_station and len(stations) >= 9:  # All stations complete
            next_station = None
            
        if next_station:
            resumable_sessions.append((session_id, next_station, len(stations)))
            print(f"🎯 {len(resumable_sessions)}. {session_id}")
            print(f"   📊 {len(stations)} stations complete")
            print(f"   ▶️ Resume from: Station {next_station}")
            print()
    
    if not resumable_sessions:
        print("❌ No resumable sessions found!")
        return
    
    # Get user choice
    while True:
        try:
            choice = input(f"📝 Choose session (1-{len(resumable_sessions)}): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(resumable_sessions):
                session_id, resume_station, completed_count = resumable_sessions[choice_num - 1]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(resumable_sessions)}")
        except ValueError:
            print("❌ Please enter a valid number")
    
    print(f"\n✅ Selected session: {session_id}")
    print(f"📊 Completed stations: {completed_count}")
    print(f"▶️ Starting from: Station {resume_station}")
    print()
    
    # Ask which station to run
    if resume_station <= 9:
        station_choice = input(f"🎯 Run Station {resume_station} or specific station? (Enter station number 1-9 or press Enter for {resume_station}): ").strip()
        
        if station_choice:
            try:
                target_station = float(station_choice)  # Allow 4.5
                if target_station not in [1, 2, 3, 4, 4.5, 5, 6, 7, 8, 9]:
                    print("❌ Please enter a valid station number (1, 2, 3, 4, 4.5, 5, 6, 7, 8, 9)")
                    return
                resume_station = target_station
            except ValueError:
                print("❌ Invalid station number")
                return
    
    print(f"\n🚀 RUNNING STATION {resume_station}")
    print("=" * 40)
    
    # Run the station
    success = await run_station(resume_station, session_id)
    
    if success:
        print(f"\n🎉 Station {resume_station} completed successfully!")
        
        # Offer to continue to next station
        if resume_station < 9:
            next_station = resume_station + 1
            if next_station <= 9:
                continue_choice = input(f"\n🤔 Continue to Station {next_station}? (Y/n): ").lower().strip()
                if continue_choice != 'n':
                    success = await run_station(next_station, session_id)
                    if success:
                        print(f"\n🎉 Station {next_station} completed successfully!")
    else:
        print(f"\n💥 Station {resume_station} failed!")

if __name__ == "__main__":
    asyncio.run(main())