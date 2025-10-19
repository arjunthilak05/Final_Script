"""
Station 11: Runtime Planning

This station establishes episode parameters, word budgets, pacing variation, and series totals for audio episodes.
It creates a comprehensive runtime planning grid based on the season structure and project requirements.

Flow:
1. Load data from previous stations (1, 2, 3, 4, 4.5, 5)
2. Extract required inputs from previous stations
3. Execute runtime planning analysis:
   - Episode Breakdown (segment allocation)
   - Word Budgets (spoken words, dialogue/narration ratio)
   - Pacing Variation (fast/slow/standard episodes)
   - Series Totals (total runtime, word count, averages)
4. Save comprehensive runtime planning grid

Critical Planning Agent - Output guides all subsequent production decisions
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


class Station11RuntimePlanner:
    """Station 11: Runtime Planning"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=11)
        self.output_dir = Path("output/station_11")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("⏱️ STATION 11: RUNTIME PLANNING")
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
                    "❌ CRITICAL ERROR: Cannot create runtime planning. "
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
            print("⏱️ Building Runtime Planning Prompt...")
            prompt = await self.build_runtime_planning_prompt(extracted_inputs)
            print("✅ Prompt built successfully")
            print()

            # Execute the runtime planning analysis
            print("=" * 60)
            print("🤖 EXECUTING RUNTIME PLANNING ANALYSIS")
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
            runtime_data = extract_json(response)
            print("✅ Data extracted successfully")
            print()

            # Save outputs
            await self.save_outputs(runtime_data)
            
            # Store in Redis
            await self.store_in_redis(runtime_data)
            
            print("=" * 60)
            print("✅ STATION 11 COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"📁 Output files saved to: {self.output_dir}")
            print(f"🔑 Session ID: {self.session_id}")
            print()

        except Exception as e:
            print(f"❌ Station 11 failed: {str(e)}")
            raise

    async def load_previous_stations_data(self) -> Dict[str, Any]:
        """Load data from all required previous stations"""
        print("📥 Loading data from previous stations...")
        
        station_data = {}
        
        # Load Station 1 (Seed Processor)
        station1_key = f"session:{self.session_id}:station:01:output"
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
        station3_key = f"session:{self.session_id}:station:03:style_guide"
        station3_data = await self.redis_client.get(station3_key)
        if station3_data:
            station_data['station_03'] = json.loads(station3_data)
            print("✅ Station 3 data loaded")
        
        # Load Station 4 (Reference Mining)
        station4_key = f"session:{self.session_id}:station:04:output"
        station4_data = await self.redis_client.get(station4_key)
        if station4_data:
            station_data['station_04'] = json.loads(station4_data)
            print("✅ Station 4 data loaded")
        
        # Load Station 4.5 (Narrator Strategy)
        station45_key = f"session:{self.session_id}:station:045:output"
        station45_data = await self.redis_client.get(station45_key)
        if station45_data:
            station_data['station_045'] = json.loads(station45_data)
            print("✅ Station 4.5 data loaded")
        
        # Load Station 5 (Season Architect)
        station5_key = f"session:{self.session_id}:station:05:output"
        station5_data = await self.redis_client.get(station5_key)
        if station5_data:
            station_data['station_05'] = json.loads(station5_data)
            print("✅ Station 5 data loaded")
        
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
            inputs['primary_genre'] = station2.get('genre_tone', {}).get('primary_genre', 'Unknown')
            inputs['target_age'] = station2.get('audience_profile', {}).get('primary_age_range', 'Unknown')
        
        # From Station 3
        if 'station_03' in station_data:
            station3 = station_data['station_03']
            inputs['chosen_genre_blend'] = station3.get('chosen_blend', 'Unknown')
            inputs['tone_calibration'] = station3.get('tone_calibration', {})
        
        # From Station 4.5
        if 'station_045' in station_data:
            station45 = station_data['station_045']
            inputs['narrator_strategy'] = station45.get('recommendation', 'Unknown')
        
        # From Station 5
        if 'station_05' in station_data:
            station5 = station_data['station_05']
            inputs['season_structure'] = station5.get('season_structure_document', {})
        
        print("✅ Required inputs extracted")
        return inputs

    async def build_runtime_planning_prompt(self, inputs: Dict[str, Any]) -> str:
        """Build the comprehensive runtime planning prompt"""
        prompt_template = self.config.get_prompt('runtime_planning_analysis')
        
        # Format the prompt with the extracted inputs
        prompt = prompt_template.format(
            working_title=inputs.get('working_title', 'Unknown'),
            primary_genre=inputs.get('primary_genre', 'Unknown'),
            target_age=inputs.get('target_age', 'Unknown'),
            episode_count=inputs.get('episode_count', 'Unknown'),
            episode_length=inputs.get('episode_length', 'Unknown'),
            season_structure=json.dumps(inputs.get('season_structure', {}), indent=2),
            narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
            chosen_genre_blend=inputs.get('chosen_genre_blend', 'Unknown'),
            tone_calibration=json.dumps(inputs.get('tone_calibration', {}), indent=2)
        )
        
        return prompt

    async def save_outputs(self, runtime_data: Dict[str, Any]):
        """Save outputs to files"""
        print("💾 Saving outputs...")
        
        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON output
        json_filename = f"session_{self.session_id}_runtime_planning.json"
        json_path = self.output_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(runtime_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON saved: {json_filename}")
        
        # Save readable text output
        txt_filename = f"session_{self.session_id}_runtime_planning.txt"
        txt_path = self.output_dir / txt_filename
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 11: RUNTIME PLANNING - COMPREHENSIVE OUTPUT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write episode breakdown
            if 'runtime_planning_grid' in runtime_data:
                grid = runtime_data['runtime_planning_grid']
                
                f.write("EPISODE BREAKDOWN\n")
                f.write("-" * 40 + "\n")
                
                if 'episode_breakdown' in grid:
                    for episode in grid['episode_breakdown']:
                        f.write(f"\nEpisode {episode.get('episode_number', 'N/A')}:\n")
                        f.write(f"  Total Runtime: {episode.get('total_runtime_target', 'N/A')}\n")
                        
                        if 'segment_allocation' in episode:
                            segments = episode['segment_allocation']
                            f.write("  Segment Allocation:\n")
                            for segment, time in segments.items():
                                f.write(f"    {segment.replace('_', ' ').title()}: {time}\n")
                        
                        if 'word_budget' in episode:
                            budget = episode['word_budget']
                            f.write("  Word Budget:\n")
                            f.write(f"    Total Words: {budget.get('total_words', 'N/A')}\n")
                            f.write(f"    Words/Minute: {budget.get('spoken_words_per_minute', 'N/A')}\n")
                            f.write(f"    Dialogue: {budget.get('dialogue_percentage', 'N/A')}%\n")
                            f.write(f"    Narration: {budget.get('narration_percentage', 'N/A')}%\n")
                        
                        f.write(f"  Pacing Type: {episode.get('pacing_type', 'N/A')}\n")
                        if episode.get('special_notes'):
                            f.write(f"  Special Notes: {episode.get('special_notes')}\n")
                
                # Write series totals
                f.write("\n\nSERIES TOTALS\n")
                f.write("-" * 40 + "\n")
                
                if 'series_totals' in grid:
                    totals = grid['series_totals']
                    f.write(f"Total Runtime: {totals.get('total_runtime', 'N/A')}\n")
                    f.write(f"Total Word Count: {totals.get('total_word_count', 'N/A')}\n")
                    f.write(f"Average Pace: {totals.get('average_pace', 'N/A')}\n")
                    f.write(f"Variation Range: {totals.get('variation_range', 'N/A')}\n")
                
                # Write pacing variation
                f.write("\n\nPACING VARIATION\n")
                f.write("-" * 40 + "\n")
                
                if 'pacing_variation' in grid:
                    pacing = grid['pacing_variation']
                    f.write(f"Fast Episodes: {pacing.get('fast_episodes', [])}\n")
                    f.write(f"Slow Episodes: {pacing.get('slow_episodes', [])}\n")
                    f.write(f"Standard Episodes: {pacing.get('standard_episodes', [])}\n")
                    f.write(f"Special Format Episodes: {pacing.get('special_format_episodes', [])}\n")
                
                # Write production notes
                f.write("\n\nPRODUCTION NOTES\n")
                f.write("-" * 40 + "\n")
                
                if 'production_notes' in grid:
                    notes = grid['production_notes']
                    for key, value in notes.items():
                        f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        print(f"✅ Readable text saved: {txt_filename}")

    async def store_in_redis(self, runtime_data: Dict[str, Any]):
        """Store the runtime planning data in Redis"""
        print("💾 Storing in Redis...")
        
        redis_key = f"session:{self.session_id}:station:11:output"
        await self.redis_client.set(redis_key, json.dumps(runtime_data))
        
        print("✅ Data stored in Redis")


async def main():
    """Main execution function"""
    print("🚀 Starting Station 11: Runtime Planning")
    print()
    
    # Get session ID from user
    session_id = input("Enter the session ID from a previous station: ").strip()
    
    if not session_id:
        print("❌ Session ID is required")
        return
    
    # Initialize and run the station
    station = Station11RuntimePlanner(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
