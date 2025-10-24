"""
Station 12: Hook & Cliffhanger Designer

This station designs opening hooks, three act turns, cliffhanger types and intensity, 
and connections to next episode for each episode in the series.

Flow:
1. Load data from previous stations (1, 2, 3, 4, 4.5, 5, 11)
2. Extract required inputs from previous stations
3. Execute hook and cliffhanger design analysis:
   - Opening Hook Design (first 60 seconds)
   - Three Act Turns (plot advancement points)
   - Cliffhanger Design (type and intensity 1-10)
   - Episode Connections (narrative flow)
4. Save comprehensive hook and cliffhanger design document

Critical Engagement Agent - Output guides all subsequent episode development
"""

import asyncio
import json
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json
from app.agents.title_validator import TitleValidator


class Station12HookCliffhangerDesigner:
    """Station 12: Hook & Cliffhanger Designer"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=12)
        self.output_dir = Path("output/station_12")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🎣 STATION 12: HOOK & CLIFFHANGER DESIGNER")
        print("=" * 60)
        print()

        try:
            # Load data from previous stations
            station_data = await self.load_previous_stations_data()
            
            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs(station_data)
            
            # --- START CRITICAL VALIDATION ---
            episode_count = extracted_inputs.get('episode_count', 'Unknown')
            episode_length = extracted_inputs.get('episode_length', 'Unknown')

            if episode_count == 'Unknown' or episode_length == 'Unknown' or not episode_count:
                error_msg = (
                    "❌ CRITICAL ERROR: Cannot create hook and cliffhanger design. "
                    f"Episode Count ('{episode_count}') or Episode Length ('{episode_length}') is undefined. "
                    "This value is expected from Station 1's 'option_details'."
                )
                print(error_msg)
                raise ValueError(error_msg)
            
            print("✅ Critical data validated (Episode Count, Episode Length)")
            # --- END CRITICAL VALIDATION ---
            
            print("✅ Data loaded successfully")
            print()
            print("-" * 60)
            print("📊 PROJECT SUMMARY")
            print("-" * 60)
            print(f"Working Title: {extracted_inputs.get('working_title', 'N/A')}")
            print(f"Primary Genre: {extracted_inputs.get('primary_genre', 'N/A')}")
            print(f"Target Age: {extracted_inputs.get('target_age', 'N/A')}")
            print(f"Episode Count: {extracted_inputs.get('episode_count', 'N/A')}")
            print(f"Episode Length: {extracted_inputs.get('episode_length', 'N/A')}")
            print(f"Narrator Strategy: {extracted_inputs.get('narrator_strategy', 'N/A')}")
            print(f"Chosen Genre Blend: {extracted_inputs.get('chosen_genre_blend', 'N/A')}")
            print("-" * 60)
            print()

            # Build the comprehensive LLM prompt
            print("🎣 Building Hook & Cliffhanger Design Prompt...")
            prompt = await self.build_hook_cliffhanger_prompt(extracted_inputs)
            print("✅ Prompt built successfully")
            print()

            # Execute the hook and cliffhanger design analysis
            print("=" * 60)
            print("🤖 EXECUTING HOOK & CLIFFHANGER DESIGN ANALYSIS")
            print("=" * 60)
            print("⏳ Processing with AI...")
            
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            print("✅ AI analysis completed")
            print()

            # Extract JSON from response
            print("📋 Extracting structured data...")
            hook_cliffhanger_data = extract_json(response)
            print("✅ Data extracted successfully")
            print()

            # Save outputs
            await self.save_outputs(hook_cliffhanger_data)
            
            # Store in Redis
            await self.store_in_redis(hook_cliffhanger_data)
            
            print("=" * 60)
            print("✅ STATION 12 COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"📁 Output files saved to: {self.output_dir}")
            print(f"🔑 Session ID: {self.session_id}")
            print()

        except Exception as e:
            print(f"❌ Station 12 failed: {str(e)}")
            raise

    async def load_previous_stations_data(self) -> Dict[str, Any]:
        """Load data from all required previous stations"""
        print("📥 Loading data from previous stations...")
        
        station_data = {}
        
        # Load Station 1 (Seed Processor)
        station1_key = f"audiobook:{self.session_id}:station_01"
        station1_data = await self.redis_client.get(station1_key)
        if station1_data:
            station_data['station_01'] = json.loads(station1_data)
            print("✅ Station 1 data loaded")
        
        # Load Station 2 (Project DNA Builder) - from file since not in Redis
        station2_file = Path(f"output/station_02/session_{self.session_id}_bible.json")
        if station2_file.exists():
            with open(station2_file, 'r', encoding='utf-8') as f:
                station_data['station_02'] = json.load(f)
            print("✅ Station 2 data loaded from file")
        
        # Load Station 3 (Age Genre Optimizer)
        station3_key = f"audiobook:{self.session_id}:station_03"
        station3_data = await self.redis_client.get(station3_key)
        if station3_data:
            station_data['station_03'] = json.loads(station3_data)
            print("✅ Station 3 data loaded")
        
        # Load Station 4 (Reference Mining)
        station4_key = f"audiobook:{self.session_id}:station_04"
        station4_data = await self.redis_client.get(station4_key)
        if station4_data:
            station_data['station_04'] = json.loads(station4_data)
            print("✅ Station 4 data loaded")
        
        # Load Station 4.5 (Narrator Strategy)
        station45_key = f"audiobook:{self.session_id}:station_045"
        station45_data = await self.redis_client.get(station45_key)
        if station45_data:
            station_data['station_045'] = json.loads(station45_data)
            print("✅ Station 4.5 data loaded")
        
        # Load Station 5 (Season Architect)
        station5_key = f"audiobook:{self.session_id}:station_05"
        station5_data = await self.redis_client.get(station5_key)
        if station5_data:
            station_data['station_05'] = json.loads(station5_data)
            print("✅ Station 5 data loaded")
        
        # Load Station 11 (Runtime Planning)
        station11_key = f"audiobook:{self.session_id}:station_11"
        station11_data = await self.redis_client.get(station11_key)
        if station11_data:
            station_data['station_11'] = json.loads(station11_data)
            print("✅ Station 11 data loaded")
        
        return station_data

    async def extract_required_inputs(self, station_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract required inputs from previous stations"""
        print("🔍 Extracting required inputs...")
        
        inputs = {}
        
        # From Station 1
        if 'station_01' in station_data:
            station1 = station_data['station_01']
            inputs['working_title'] = station1.get('chosen_title', station1.get('working_title', 'Unknown'))
            inputs['episode_count'] = station1.get('option_details', {}).get('episode_count', 'Unknown')
            inputs['episode_length'] = station1.get('option_details', {}).get('episode_length', 'Unknown')
            inputs['core_premise'] = station1.get('core_premise', 'Unknown')
        
        # From Station 2
        if 'station_02' in station_data:
            station2 = station_data['station_02']
            # Station 2 doesn't have primary_genre or target_age - these come from Station 3
        
        # From Station 3
        if 'station_03' in station_data:
            station3 = station_data['station_03']
            chosen_blend = station3.get('chosen_blend_details', {})
            inputs['primary_genre'] = chosen_blend.get('primary_genre', 'Unknown')
            inputs['chosen_genre_blend'] = station3.get('chosen_blend', 'Unknown')
            inputs['tone_calibration'] = station3.get('tone_calibration', {})
            
            age_guidelines = station3.get('age_guidelines', {})
            inputs['target_age'] = age_guidelines.get('target_age_range', 'Unknown')
        
        # From Station 4.5
        if 'station_045' in station_data:
            station45 = station_data['station_045']
            inputs['narrator_strategy'] = station45.get('recommendation', 'Unknown')
        
        # From Station 5
        if 'station_05' in station_data:
            station5 = station_data['station_05']
            inputs['season_structure'] = station5.get('season_structure_document', {})
        
        # From Station 11
        if 'station_11' in station_data:
            station11 = station_data['station_11']
            inputs['runtime_planning'] = station11.get('runtime_planning_grid', {})
        
        print("✅ Required inputs extracted")
        return inputs

    async def build_hook_cliffhanger_prompt(self, inputs: Dict[str, Any]) -> str:
        """Build the comprehensive hook and cliffhanger design prompt"""
        prompt_template = self.config.get_prompt('hook_cliffhanger_design')
        
        # Format the prompt with the extracted inputs
        prompt = prompt_template.format(
            working_title=inputs.get('working_title', 'Unknown'),
            primary_genre=inputs.get('primary_genre', 'Unknown'),
            target_age=inputs.get('target_age', 'Unknown'),
            episode_count=inputs.get('episode_count', 'Unknown'),
            episode_length=inputs.get('episode_length', 'Unknown'),
            season_structure=json.dumps(inputs.get('season_structure', {}), indent=2),
            runtime_planning=json.dumps(inputs.get('runtime_planning', {}), indent=2),
            narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
            chosen_genre_blend=inputs.get('chosen_genre_blend', 'Unknown'),
            tone_calibration=json.dumps(inputs.get('tone_calibration', {}), indent=2)
        )
        
        return prompt

    async def save_outputs(self, hook_cliffhanger_data: Dict[str, Any]):
        """Save outputs to files"""
        print("💾 Saving outputs...")
        
        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON output
        json_filename = f"session_{self.session_id}_hook_cliffhanger_design.json"
        json_path = self.output_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(hook_cliffhanger_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON saved: {json_filename}")
        
        # Save readable text output
        txt_filename = f"session_{self.session_id}_hook_cliffhanger_design.txt"
        txt_path = self.output_dir / txt_filename
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 12: HOOK & CLIFFHANGER DESIGNER - COMPREHENSIVE OUTPUT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write episode hooks
            if 'hook_cliffhanger_design' in hook_cliffhanger_data:
                design = hook_cliffhanger_data['hook_cliffhanger_design']
                
                f.write("EPISODE HOOKS & CLIFFHANGERS\n")
                f.write("-" * 40 + "\n")
                
                if 'episode_hooks' in design:
                    for episode in design['episode_hooks']:
                        f.write(f"\nEpisode {episode.get('episode_number', 'N/A')}:\n")
                        
                        if 'opening_hook' in episode:
                            hook = episode['opening_hook']
                            f.write(f"  Opening Hook ({hook.get('type', 'N/A')}):\n")
                            f.write(f"    Description: {hook.get('description', 'N/A')}\n")
                            f.write(f"    Duration: {hook.get('duration', 'N/A')}\n")
                            f.write(f"    Audio Elements: {', '.join(hook.get('audio_elements', []))}\n")
                            f.write(f"    Emotional Tone: {hook.get('emotional_tone', 'N/A')}\n")
                        
                        if 'act_turns' in episode:
                            turns = episode['act_turns']
                            f.write("  Act Turns:\n")
                            f.write(f"    Act 1: {turns.get('act_1_turn', 'N/A')}\n")
                            f.write(f"    Act 2: {turns.get('act_2_turn', 'N/A')}\n")
                            f.write(f"    Act 3: {turns.get('act_3_turn', 'N/A')}\n")
                        
                        if 'cliffhanger' in episode:
                            cliff = episode['cliffhanger']
                            f.write(f"  Cliffhanger ({cliff.get('type', 'N/A')}, Intensity: {cliff.get('intensity', 'N/A')}):\n")
                            f.write(f"    Description: {cliff.get('description', 'N/A')}\n")
                            f.write(f"    Audio Execution: {cliff.get('audio_execution', 'N/A')}\n")
                        
                        f.write(f"  Next Episode Connection: {episode.get('next_episode_connection', 'N/A')}\n")
                        f.write(f"  Season Position: {episode.get('season_position', 'N/A')}\n")
                
                # Write series patterns
                f.write("\n\nSERIES HOOK PATTERNS\n")
                f.write("-" * 40 + "\n")
                
                if 'series_hook_patterns' in design:
                    patterns = design['series_hook_patterns']
                    f.write(f"Hook Types Used: {', '.join(patterns.get('hook_types_used', []))}\n")
                    f.write(f"Intensity Progression: {patterns.get('intensity_progression', 'N/A')}\n")
                    f.write(f"Cliffhanger Escalation: {patterns.get('cliffhanger_escalation', 'N/A')}\n")
                
                # Write audio considerations
                f.write("\n\nAUDIO CONSIDERATIONS\n")
                f.write("-" * 40 + "\n")
                
                if 'audio_considerations' in design:
                    audio = design['audio_considerations']
                    f.write(f"Hook Audio Signatures: {audio.get('hook_audio_signatures', 'N/A')}\n")
                    f.write(f"Cliffhanger Audio Cues: {audio.get('cliffhanger_audio_cues', 'N/A')}\n")
                    f.write(f"Transition Sounds: {audio.get('transition_sounds', 'N/A')}\n")
        
        print(f"✅ Readable text saved: {txt_filename}")

    async def store_in_redis(self, hook_cliffhanger_data: Dict[str, Any]):
        """Store the hook and cliffhanger design data in Redis"""
        print("💾 Storing in Redis...")
        
        redis_key = f"audiobook:{self.session_id}:station_12"
        await self.redis_client.set(redis_key, json.dumps(hook_cliffhanger_data))
        
        print("✅ Data stored in Redis")


async def main():
    """Main execution function"""
    print("🚀 Starting Station 12: Hook & Cliffhanger Designer")
    print()
    
    # Get session ID from user
    session_id = input("Enter the session ID from a previous station: ").strip()
    
    if not session_id:
        print("❌ Session ID is required")
        return
    
    # Initialize and run the station
    station = Station12HookCliffhangerDesigner(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
