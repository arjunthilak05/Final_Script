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
from app.agents.station_10_narrative_reveal_strategy import Station10NarrativeRevealStrategy
from app.agents.station_11_runtime_planning import Station11RuntimePlanning
from app.agents.station_12_hook_cliffhanger import Station12HookCliffhanger
from app.agents.station_13_multiworld_timeline import Station13MultiworldTimeline
from app.agents.station_14_episode_blueprint import Station14EpisodeBlueprint
from app.agents.station_15_detailed_episode_outlining import Station15DetailedEpisodeOutlining
from app.agents.station_16_canon_check import Station16CanonCheck
from app.agents.station_17_dialect_planning import Station17DialectPlanning
from app.agents.station_18_evergreen_check import Station18EvergreenCheck
from app.agents.station_19_procedure_check import Station19ProcedureCheck
from app.agents.station_20_geography_transit import Station20GeographyTransit
from app.agents.station_registry import get_station_registry

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
            print(f"✅ Station 2 completed: Project DNA for {result.working_title}")
            
        elif station_num == 3:
            station = Station03AgeGenreOptimizer()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 3 completed: Age & Genre optimization")
            
        elif station_num == 4:
            station = Station04ReferenceMiner()
            await station.initialize()
            result = await station.process(session_id)
            total_seeds = len(result.seed_collection.micro_moments) + len(result.seed_collection.episode_beats) + len(result.seed_collection.season_arcs) + len(result.seed_collection.series_defining)
            print(f"✅ Station 4 completed: {total_seeds} seeds generated")
            
        elif station_num == 4.5:
            station = Station045NarratorStrategy()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 4.5 completed: Narrator strategy - {result.recommendation.value}")
            
        elif station_num == 5:
            station = Station05SeasonArchitect()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 5 completed: {result.chosen_style}")
            
        elif station_num == 6:
            station = Station06MasterStyleGuideBuilder()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 6 completed: Master Style Guide for {result.working_title if hasattr(result, 'working_title') else 'Unknown'}")
            
        elif station_num == 7:
            station = Station07RealityCheck()
            await station.initialize()
            result = await station.process(session_id)
            
            # Check pipeline status and handle accordingly
            if result.pipeline_status == "FAILED":
                print(f"❌ Station 7 completed: Reality Check - FAILED")
                print(f"🚨 Critical Issues: {len(result.critical_issues)}")
                for issue in result.critical_issues[:3]:  # Show first 3 issues
                    print(f"   • {issue}")
                if len(result.critical_issues) > 3:
                    print(f"   ... and {len(result.critical_issues) - 3} more issues")
                
                # Show which stations failed
                failed_stations = [v for v in result.station_validations if v.status == "FAIL"]
                if failed_stations:
                    print(f"🔍 Failed Stations:")
                    for station in failed_stations:
                        print(f"   • Station {station.station_number} ({station.station_name}): {', '.join(station.issues)}")
                
                return False  # Stop automation on failure
            elif result.pipeline_status == "NEEDS_ATTENTION":
                print(f"⚠️ Station 7 completed: Reality Check - NEEDS_ATTENTION")
                print(f"💡 Recommendations: {len(result.recommendations)}")
                for rec in result.recommendations[:2]:  # Show first 2 recommendations
                    print(f"   • {rec}")
            else:  # PASSED
                print(f"✅ Station 7 completed: Reality Check - PASSED")
            
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
            
        elif station_num == 10:
            station = Station10NarrativeRevealStrategy()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 10 completed: Narrative Reveal Strategy - {result['summary']['information_items']} information items")
            
        elif station_num == 11:
            station = Station11RuntimePlanning()
            await station.initialize()
            result = await station.process(session_id)
            print(f"✅ Station 11 completed: Runtime Planning - {result.get('summary', {}).get('total_episodes', 0)} episodes planned")
            
        elif station_num == 12:
            station = Station12HookCliffhanger(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 12 completed: Hook & Cliffhanger Strategy - {result['statistics']['hooks_designed']} hooks, {result['statistics']['cliffhangers_designed']} cliffhangers")
            
        elif station_num == 13:
            station = Station13MultiworldTimeline(session_id)
            await station.initialize()
            result = await station.run()
            if result['is_applicable']:
                print(f"✅ Station 13 completed: Multi-World Management - {result['statistics']['world_count']} worlds, complexity: {result['statistics']['complexity_level']}")
            else:
                print(f"✅ Station 13 completed: Single-world narrative detected (gracefully skipped)")
            
        elif station_num == 14:
            station = Station14EpisodeBlueprint(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 14 completed: Episode Blueprints - {result['statistics']['blueprints_generated']} blueprints ready for approval")
            print(f"📄 Approval Document (TXT): {result['outputs']['txt']}")
            print(f"📄 Approval Document (JSON): {result['outputs']['json']}")
            print("🚨 HUMAN GATE: Review and approve blueprints before proceeding")
            
        elif station_num == 15:
            station = Station15DetailedEpisodeOutlining(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 15 completed: Detailed Episode Outlining - {result['statistics']['outlines_generated']} production-ready outlines")
            print(f"📄 Production Document (TXT): {result['outputs']['txt']}")
            print(f"📄 Production Document (JSON): {result['outputs']['json']}")
            print("🎬 PRODUCTION-READY: Detailed scene-by-scene outlines ready for voice actors")
            
        elif station_num == 16:
            from app.agents.station_16_canon_check import Station16CanonCheck
            station = Station16CanonCheck(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 16 completed: Canon Check")
            
        elif station_num == 17:
            from app.agents.station_17_dialect_planning import Station17DialectPlanning
            station = Station17DialectPlanning(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 17 completed: Dialect Planning")
            
        elif station_num == 18:
            from app.agents.station_18_evergreen_check import Station18EvergreenCheck
            station = Station18EvergreenCheck(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 18 completed: Evergreen Check")
            
        elif station_num == 19:
            from app.agents.station_19_procedure_check import Station19ProcedureCheck
            station = Station19ProcedureCheck(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 19 completed: Procedure Check")
            
        elif station_num == 20:
            from app.agents.station_20_geography_transit import Station20GeographyTransit
            station = Station20GeographyTransit(session_id)
            await station.initialize()
            result = await station.run()
            print(f"✅ Station 20 completed: Geography & Transit Check")
            
        # Handle custom stations (21+) created with station_creator_wizard
        elif station_num > 20:
            registry = get_station_registry()
            metadata = registry.get_station_metadata(station_num)
            
            if not metadata:
                print(f"❌ Station {station_num} not found")
                return False
            
            if not metadata.enabled:
                print(f"⏭️  Station {station_num} is disabled, skipping...")
                return True
            
            print(f"🔄 Running custom Station {station_num}: {metadata.name}")
            
            try:
                # Dynamically load the station class
                StationClass = registry.load_station_class(station_num)
                station = StationClass()
                await station.initialize()
                result = await station.process(session_id)
                print(f"✅ Station {station_num} completed: {metadata.name}")
                return True
            except Exception as e:
                print(f"❌ Custom station {station_num} failed: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
            
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
        expected_stations = ["station_01", "station_02", "station_03", "station_04", "station_04_5", "station_05", "station_06", "station_07", "station_08", "station_09", "station_10", "station_11", "station_12", "station_13", "station_14", "station_15", "station_16", "station_17", "station_18", "station_19", "station_20"]
        station_numbers = [1, 2, 3, 4, 4.5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        
        # Find next station to resume from
        next_station = None
        for i, expected in enumerate(expected_stations):
            if expected not in stations:
                next_station = station_numbers[i]
                break
        
        if not next_station and len(stations) >= 15:  # All stations complete
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
    
    # Auto-discover all available stations (including custom ones)
    registry = get_station_registry()
    all_stations = registry.get_all_stations()
    valid_stations = sorted([num for num in all_stations.keys() if all_stations[num].enabled])
    
    # Show custom stations if any exist
    custom_stations = [num for num in valid_stations if num > 20]
    if custom_stations:
        print(f"\n📦 CUSTOM STATIONS AVAILABLE:")
        for num in custom_stations:
            meta = all_stations[num]
            print(f"   • Station {num}: {meta.name}")
        print()
    
    # Ask which station to run
    station_choice = input(f"🎯 Run Station {resume_station} or specific station? (Enter station number or press Enter for {resume_station}): ").strip()
    
    if station_choice:
        try:
            target_station = float(station_choice)  # Allow 4.5
            if target_station not in valid_stations:
                print(f"❌ Please enter a valid station number: {valid_stations}")
                return
            resume_station = target_station
        except ValueError:
            print("❌ Invalid station number")
            return
    
    print(f"\n🚀 RUNNING STATIONS FROM {resume_station}")
    print("=" * 40)
    
    # Use the auto-discovered valid_stations (already set above, includes custom stations)
    # Find remaining stations to run
    remaining_stations = [s for s in valid_stations if s >= resume_station]
    
    if not remaining_stations:
        print(f"❌ No stations to run from {resume_station}")
        return
    
    print(f"📊 Will run {len(remaining_stations)} station(s): {remaining_stations}")
    print()
    
    # Run all remaining stations
    for current_station in remaining_stations:
        print(f"\n🚀 Running Station {current_station}...")
        print("=" * 40)
        
        success = await run_station(current_station, session_id)
        
        if success:
            print(f"\n🎉 Station {current_station} completed successfully!")
            
            # Check if this is the last station
            if current_station == remaining_stations[-1]:
                total_stations = len(valid_stations)
                built_in = len([s for s in valid_stations if s <= 20])
                custom = len([s for s in valid_stations if s > 20])
                
                print(f"\n🎉 ALL STATIONS COMPLETED!")
                print(f"✅ Built-in stations: {built_in}")
                if custom > 0:
                    print(f"✅ Custom stations: {custom}")
                print("🎬 Production pipeline complete!")
        else:
            print(f"\n💥 Station {current_station} failed!")
            print(f"❌ Stopping automation at Station {current_station}")
            return

if __name__ == "__main__":
    asyncio.run(main())