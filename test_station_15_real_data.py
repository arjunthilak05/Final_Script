#!/usr/bin/env python3
"""
Test Station 15 with Real Data from Station 14

This script loads actual episode blueprints from Station 14 outputs
and generates detailed scene-by-scene outlines using Station 15.
"""

import sys
import json
import asyncio
from pathlib import Path

from app.agents.station_15_detailed_episode_outlining import (
    Station15DetailedEpisodeOutlining,
    Station15Input,
    Station15Output
)


async def test_station_15_with_real_data(session_id: str, episode_number: int = 1):
    """
    Test Station 15 using real data from Station 14 outputs
    
    Args:
        session_id: Session ID (e.g., "auto_20251007_123810")
        episode_number: Which episode to outline (default: 1)
    """
    print("="*70)
    print("TESTING STATION 15 WITH REAL DATA")
    print("="*70)
    print(f"Session ID: {session_id}")
    print(f"Episode Number: {episode_number}\n")
    
    # Step 1: Load Station 14 blueprint data
    blueprint_file = f"outputs/station14_episode_blueprint_{session_id}.json"
    blueprint_path = Path(blueprint_file)
    
    if not blueprint_path.exists():
        print(f"❌ Error: Station 14 blueprint file not found: {blueprint_file}")
        print(f"   Available files in outputs/:")
        outputs_dir = Path("outputs")
        for file in outputs_dir.glob("station14_*.json"):
            print(f"   - {file.name}")
        return None
    
    print(f"📥 Loading Station 14 blueprint from: {blueprint_file}")
    with open(blueprint_path, 'r') as f:
        blueprint_data = json.load(f)
    
    total_episodes = blueprint_data.get('total_episodes', 0)
    episodes = blueprint_data.get('episodes', [])
    
    print(f"✅ Blueprint loaded: {total_episodes} episodes found")
    
    # Validate episode number
    if episode_number < 1 or episode_number > total_episodes:
        print(f"❌ Error: Episode {episode_number} not found. Available: 1-{total_episodes}")
        return None
    
    # Step 2: Extract the specific episode blueprint
    episode_data = episodes[episode_number - 1]
    episode_title = episode_data.get('episode_title', f'Episode {episode_number}')
    blueprint_summary = episode_data.get('simple_summary', '')
    
    if not blueprint_summary:
        print(f"❌ Error: No summary found for episode {episode_number}")
        return None
    
    print(f"\n📖 Episode {episode_number}: {episode_title}")
    print(f"   Summary length: {len(blueprint_summary)} characters")
    print(f"\n   Preview:")
    print(f"   {blueprint_summary[:200]}...\n")
    
    # Step 3: Create Station 15 input
    input_data = Station15Input(
        session_id=session_id,
        episode_number=episode_number,
        blueprint_summary=blueprint_summary
    )
    
    print("✅ Station15Input created and validated\n")
    
    # Step 4: Initialize and run Station 15
    print("🚀 Initializing Station 15 Agent...")
    agent = Station15DetailedEpisodeOutlining(session_id=session_id)
    
    print("⚙️ Running Station 15 (this may take 30-60 seconds)...\n")
    
    try:
        result = await agent.run(input_data)
        
        # Step 5: Display results
        print("\n" + "="*70)
        print("📊 STATION 15 RESULTS")
        print("="*70)
        print(f"Episode Number: {result.episode_number}")
        print(f"Total Scenes: {len(result.scenes)}")
        print(f"\nScene Breakdown:")
        print("-"*70)
        
        total_runtime_mins = 0
        for scene in result.scenes:
            print(f"\n🎬 Scene {scene.scene_number}: {scene.location}")
            print(f"   Time: {scene.time}")
            print(f"   Characters: {', '.join(scene.characters_present)}")
            print(f"   Runtime: {scene.estimated_runtime}")
            print(f"   Reveal: {scene.reveal}")
            print(f"   Goal/Obstacle: {scene.goal_obstacle_choice_consequence[:80]}...")
            print(f"   Soundscape: {scene.soundscape_notes[:80]}...")
            
            # Try to extract runtime in minutes
            try:
                runtime_str = scene.estimated_runtime.lower()
                if 'minute' in runtime_str:
                    import re
                    match = re.search(r'(\d+)', runtime_str)
                    if match:
                        total_runtime_mins += int(match.group(1))
            except:
                pass
        
        print("\n" + "="*70)
        print("📈 STATISTICS")
        print("="*70)
        print(f"Total Scenes: {len(result.scenes)}")
        print(f"Estimated Total Runtime: ~{total_runtime_mins} minutes")
        print(f"Average Scene Length: ~{total_runtime_mins / len(result.scenes):.1f} minutes")
        
        # Count unique characters and locations
        all_characters = set()
        all_locations = set()
        reveal_count = {'Plant': 0, 'Proof': 0, 'Payoff': 0, 'None': 0}
        
        for scene in result.scenes:
            all_characters.update(scene.characters_present)
            all_locations.add(scene.location)
            
            if 'Plant' in scene.reveal:
                reveal_count['Plant'] += 1
            elif 'Proof' in scene.reveal:
                reveal_count['Proof'] += 1
            elif 'Payoff' in scene.reveal:
                reveal_count['Payoff'] += 1
            else:
                reveal_count['None'] += 1
        
        print(f"Unique Characters: {len(all_characters)} ({', '.join(list(all_characters)[:5])}{'...' if len(all_characters) > 5 else ''})")
        print(f"Unique Locations: {len(all_locations)}")
        print(f"Reveals: {reveal_count['Plant']} Plants, {reveal_count['Proof']} Proofs, {reveal_count['Payoff']} Payoffs, {reveal_count['None']} None")
        
        # Step 6: Save to file for inspection
        output_file = f"outputs/station15_episode_{episode_number}_{session_id}.json"
        output_path = Path(output_file)
        
        print(f"\n💾 Saving detailed outline to: {output_file}")
        with open(output_path, 'w') as f:
            f.write(result.model_dump_json(indent=2))
        
        print(f"✅ Saved successfully")
        
        # Also save as pretty text file
        text_file = f"outputs/station15_episode_{episode_number}_{session_id}.txt"
        text_path = Path(text_file)
        
        with open(text_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"STATION 15: DETAILED EPISODE OUTLINE\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {session_id}\n")
            f.write(f"Episode Number: {result.episode_number}\n")
            f.write(f"Total Scenes: {len(result.scenes)}\n")
            f.write(f"Estimated Runtime: ~{total_runtime_mins} minutes\n\n")
            
            for scene in result.scenes:
                f.write("="*70 + "\n")
                f.write(f"SCENE {scene.scene_number}: {scene.location.upper()}\n")
                f.write("="*70 + "\n\n")
                f.write(f"Time: {scene.time}\n")
                f.write(f"Characters Present: {', '.join(scene.characters_present)}\n")
                f.write(f"Estimated Runtime: {scene.estimated_runtime}\n\n")
                
                f.write("DRAMATIC STRUCTURE:\n")
                f.write("-"*70 + "\n")
                f.write(f"{scene.goal_obstacle_choice_consequence}\n\n")
                
                f.write("REVEAL:\n")
                f.write("-"*70 + "\n")
                f.write(f"{scene.reveal}\n\n")
                
                f.write("SOUNDSCAPE NOTES:\n")
                f.write("-"*70 + "\n")
                f.write(f"{scene.soundscape_notes}\n\n")
                
                f.write("TRANSITION:\n")
                f.write("-"*70 + "\n")
                f.write(f"{scene.transition_to_next_scene}\n\n")
        
        print(f"💾 Also saved human-readable version: {text_file}")
        
        print("\n" + "="*70)
        print("✅ STATION 15 TEST COMPLETE")
        print("="*70)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error running Station 15: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def test_multiple_episodes(session_id: str, max_episodes: int = 3):
    """
    Test Station 15 on multiple episodes
    
    Args:
        session_id: Session ID
        max_episodes: Maximum number of episodes to process
    """
    print("="*70)
    print(f"TESTING STATION 15 ON MULTIPLE EPISODES (up to {max_episodes})")
    print("="*70)
    
    # Load blueprint to see how many episodes we have
    blueprint_file = f"outputs/station14_episode_blueprint_{session_id}.json"
    with open(blueprint_file, 'r') as f:
        blueprint_data = json.load(f)
    
    total_episodes = blueprint_data.get('total_episodes', 0)
    episodes_to_process = min(max_episodes, total_episodes)
    
    print(f"Processing {episodes_to_process} of {total_episodes} episodes\n")
    
    results = []
    for ep_num in range(1, episodes_to_process + 1):
        print(f"\n{'='*70}")
        print(f"Processing Episode {ep_num} of {episodes_to_process}")
        print(f"{'='*70}\n")
        
        result = await test_station_15_with_real_data(session_id, ep_num)
        if result:
            results.append(result)
        
        # Small delay between episodes
        if ep_num < episodes_to_process:
            print("\n⏳ Waiting 2 seconds before next episode...")
            await asyncio.sleep(2)
    
    print("\n" + "="*70)
    print("ALL EPISODES COMPLETE")
    print("="*70)
    print(f"Successfully processed: {len(results)} episodes")
    print(f"Failed: {episodes_to_process - len(results)} episodes")
    
    return results


def main():
    """Main entry point"""
    
    # Default session ID from outputs folder
    default_session = "auto_20251007_123810"
    
    if len(sys.argv) < 2:
        print(f"Usage: python test_station_15_real_data.py <session_id> [episode_number]")
        print(f"   or: python test_station_15_real_data.py <session_id> --all [max_episodes]")
        print(f"\nUsing default session: {default_session}")
        print(f"Processing episode 1...\n")
        session_id = default_session
        episode_number = 1
        process_all = False
    elif len(sys.argv) >= 3 and sys.argv[2] == "--all":
        session_id = sys.argv[1]
        max_episodes = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        process_all = True
    else:
        session_id = sys.argv[1]
        episode_number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        process_all = False
    
    if process_all:
        asyncio.run(test_multiple_episodes(session_id, max_episodes))
    else:
        asyncio.run(test_station_15_with_real_data(session_id, episode_number))


if __name__ == "__main__":
    main()

