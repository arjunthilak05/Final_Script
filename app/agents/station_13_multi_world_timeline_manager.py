"""
Station 13: Multi-World/Timeline Manager

This station manages multiple worlds, timelines, or realities for projects that require it.
It's a CONDITIONAL station - only needed for projects with multiple worlds/timelines.

Flow:
1. Load data from previous stations (1, 2, 3, 4, 4.5, 5, 6, 7, 8, 9, 10, 11, 12)
2. Extract required inputs from previous stations
3. Analyze if multi-world/timeline management is needed
4. If needed, create comprehensive management system:
   - World/timeline per episode
   - Transition sounds between worlds
   - Rules for each world
   - How differences are conveyed in audio
5. Save comprehensive multi-world/timeline management document

Conditional Management Agent - Only runs for projects with multiple worlds/timelines
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


class Station13MultiWorldTimelineManager:
    """Station 13: Multi-World/Timeline Manager"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=13)
        self.output_dir = Path("output/station_13")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🌍 STATION 13: MULTI-WORLD/TIMELINE MANAGER")
        print("=" * 60)
        print()

        try:
            # Load data from previous stations
            station_data = await self.load_previous_stations_data()
            
            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs(station_data)
            
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
            print("🌍 Building Multi-World/Timeline Analysis Prompt...")
            prompt = await self.build_multi_world_prompt(extracted_inputs)
            print("✅ Prompt built successfully")
            print()

            # Generate multi-world/timeline analysis
            print("🤖 Analyzing Multi-World/Timeline Requirements...")
            print("   This may take 30-60 seconds for comprehensive analysis...")
            print()
            
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            print("✅ Multi-world/timeline analysis completed")
            print()

            # Extract and validate JSON
            print("🔍 Extracting and validating analysis data...")
            analysis_data = extract_json(response)
            
            if not analysis_data:
                print("❌ Failed to extract valid JSON from response")
                return
            
            print("✅ Analysis data extracted and validated")
            print()

            # Check if multi-world management is needed
            requires_management = analysis_data.get('multi_world_analysis', {}).get('requires_management', False)
            reasoning = analysis_data.get('multi_world_analysis', {}).get('reasoning', 'No reasoning provided')
            
            print("=" * 60)
            print("🔍 MULTI-WORLD/TIMELINE ANALYSIS RESULT")
            print("=" * 60)
            print(f"Requires Management: {'YES' if requires_management else 'NO'}")
            print(f"Reasoning: {reasoning}")
            print()

            if not requires_management:
                print("✅ This project does not require multi-world/timeline management.")
                print("   Station 13 is conditionally skipped for this project.")
                print("   Proceeding to Station 14: Simple Episode Blueprint")
                
                # Save minimal output for record-keeping
                await self.save_minimal_output(analysis_data, extracted_inputs)
                
            else:
                print("🌍 This project requires multi-world/timeline management.")
                print("   Processing comprehensive management system...")
                
                # Save comprehensive outputs
                await self.save_comprehensive_outputs(analysis_data, extracted_inputs)

            print("=" * 60)
            print("✅ STATION 13 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Project: {extracted_inputs.get('working_title', 'Untitled')}")
            print(f"Session ID: {self.session_id}")
            print()
            if requires_management:
                print("📊 MULTI-WORLD/TIMELINE MANAGEMENT STATISTICS:")
                worlds = analysis_data.get('worlds_timelines', [])
                print(f"   • {len(worlds)} Worlds/Timelines identified")
                print(f"   • Transition strategies documented")
                print(f"   • Audio differentiation rules established")
                print(f"   • Listener guidance provided")
            else:
                print("📊 CONDITIONAL STATION RESULT:")
                print(f"   • Multi-world management not required")
                print(f"   • Station conditionally skipped")
            print()
            print("📁 OUTPUT FILES:")
            print(f"   • {self.output_dir}/multi_world_timeline_management.json")
            print(f"   • {self.output_dir}/multi_world_timeline_management.txt")
            print()
            print("🎯 NEXT STEPS:")
            print("   • Proceed to Station 14: Simple Episode Blueprint")
            print("   • Multi-world management data available for future stations")

        except Exception as e:
            print(f"❌ Error in Station 13: {str(e)}")
            logging.error(f"Station 13 error: {str(e)}")
            raise

    async def load_previous_stations_data(self) -> Dict[str, Any]:
        """Load data from all previous stations"""
        station_data = {}
        
        # Load from Redis first
        try:
            # Station 1: Seed Processor
            station1_data = await self.redis_client.get(f"station_1:{self.session_id}")
            if station1_data:
                station_data['station_1'] = json.loads(station1_data)
            
            # Station 2: Project DNA Builder
            station2_data = await self.redis_client.get(f"station_2:{self.session_id}")
            if station2_data:
                station_data['station_2'] = json.loads(station2_data)
            
            # Station 3: Age & Genre Optimizer
            station3_data = await self.redis_client.get(f"station_3:{self.session_id}")
            if station3_data:
                station_data['station_3'] = json.loads(station3_data)
            
            # Station 4: Reference Mining
            station4_data = await self.redis_client.get(f"station_4:{self.session_id}")
            if station4_data:
                station_data['station_4'] = json.loads(station4_data)
            
            # Station 4.5: Narrator Strategy
            station45_data = await self.redis_client.get(f"station_45:{self.session_id}")
            if station45_data:
                station_data['station_45'] = json.loads(station45_data)
            
            # Station 5: Season Architecture
            station5_data = await self.redis_client.get(f"station_5:{self.session_id}")
            if station5_data:
                station_data['station_5'] = json.loads(station5_data)
            
            # Station 6: Master Style Guide
            station6_data = await self.redis_client.get(f"station_6:{self.session_id}")
            if station6_data:
                station_data['station_6'] = json.loads(station6_data)
            
            # Station 7: Character Architecture
            station7_data = await self.redis_client.get(f"station_7:{self.session_id}")
            if station7_data:
                station_data['station_7'] = json.loads(station7_data)
            
            # Station 8: World Builder
            station8_data = await self.redis_client.get(f"station_8:{self.session_id}")
            if station8_data:
                station_data['station_8'] = json.loads(station8_data)
            
            # Station 9: World Building System
            station9_data = await self.redis_client.get(f"station_9:{self.session_id}")
            if station9_data:
                station_data['station_9'] = json.loads(station9_data)
            
            # Station 10: Narrative Reveal Strategy
            station10_data = await self.redis_client.get(f"station_10:{self.session_id}")
            if station10_data:
                station_data['station_10'] = json.loads(station10_data)
            
            # Station 11: Runtime Planning
            station11_data = await self.redis_client.get(f"station_11:{self.session_id}")
            if station11_data:
                station_data['station_11'] = json.loads(station11_data)
            
            # Station 12: Hook & Cliffhanger Designer
            station12_data = await self.redis_client.get(f"station_12:{self.session_id}")
            if station12_data:
                station_data['station_12'] = json.loads(station12_data)
                
        except Exception as e:
            print(f"⚠️ Warning: Could not load some station data from Redis: {str(e)}")
        
        # If no data loaded from Redis, try loading from JSON files
        if not station_data:
            print("🔄 No data found in Redis, loading from JSON files...")
            station_data = await self.load_from_json_files()
        
        return station_data

    async def load_from_json_files(self) -> Dict[str, Any]:
        """Load data from JSON files as fallback"""
        station_data = {}
        
        # List of stations and their corresponding JSON files
        stations_to_load = [
            ('station_1', f'output/station_01/{self.session_id}_output.json'),
            ('station_2', f'output/station_02/{self.session_id}_bible.json'),
            ('station_3', f'output/station_03/{self.session_id}_style_guide.json'),
            ('station_4', f'output/station_04/{self.session_id}_output.json'),
            ('station_45', f'output/station_045/{self.session_id}_output.json'),
            ('station_5', f'output/station_05/{self.session_id}_output.json'),
            ('station_6', f'output/station_06/{self.session_id}_output.json'),
            ('station_7', f'output/station_07/{self.session_id}_character_bible.json'),
            ('station_8', f'output/station_08/{self.session_id}_world_bible.json'),
            ('station_9', f'output/station_09/{self.session_id}_world_building_system.json'),
            ('station_10', f'output/station_10/{self.session_id}_reveal_matrix.json'),
            ('station_11', f'output/station_11/{self.session_id}_runtime_planning.json'),
            ('station_12', f'output/station_12/{self.session_id}_hook_cliffhanger_design.json')
        ]
        
        for station_name, file_path in stations_to_load:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Extract the actual data from the JSON structure
                        if 'project_title' in data or 'session_id' in data:
                            # This is a wrapped JSON file, extract the actual data
                            station_data[station_name] = data
                        else:
                            station_data[station_name] = data
                        print(f"✅ Loaded {station_name} from {file_path}")
                else:
                    print(f"⚠️ File not found: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not load {station_name} from {file_path}: {str(e)}")
        
        return station_data

    async def extract_required_inputs(self, station_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract required inputs from previous stations"""
        extracted = {}
        
        # From Station 1: Basic project info
        if 'station_1' in station_data:
            station1 = station_data['station_1']
            extracted['working_title'] = station1.get('chosen_title', station1.get('working_title', 'Untitled'))
            
            # Extract episode count and length from option_details
            option_details = station1.get('option_details', {})
            extracted['episode_count'] = option_details.get('episode_count', 'Unknown')
            extracted['episode_length'] = option_details.get('episode_length', 'Unknown')
        
        # From Station 2: Project Bible
        if 'station_2' in station_data:
            station2 = station_data['station_2']
            extracted['primary_genre'] = station2.get('primary_genre', 'Unknown')
            extracted['target_age'] = station2.get('target_age', 'Unknown')
        
        # From Station 3: Genre blend
        if 'station_3' in station_data:
            station3 = station_data['station_3']
            chosen_blend = station3.get('chosen_blend_details', {})
            extracted['chosen_genre_blend'] = f"{chosen_blend.get('primary_genre', '')} + {chosen_blend.get('secondary_genre', '')}"
        
        # From Station 4.5: Narrator Strategy
        if 'station_45' in station_data:
            station45 = station_data['station_45']
            extracted['narrator_strategy'] = station45.get('recommended_approach', 'Unknown')
        
        # Build context strings for the prompt
        extracted['season_architecture'] = self._format_station_data(station_data.get('station_5', {}), "Season Architecture")
        extracted['character_bible'] = self._format_station_data(station_data.get('station_7', {}), "Character Bible")
        extracted['world_building'] = self._format_station_data(station_data.get('station_8', {}), "World Building")
        extracted['narrative_reveal_strategy'] = self._format_station_data(station_data.get('station_10', {}), "Narrative Reveal Strategy")
        extracted['runtime_planning'] = self._format_station_data(station_data.get('station_11', {}), "Runtime Planning")
        extracted['hook_cliffhanger_design'] = self._format_station_data(station_data.get('station_12', {}), "Hook & Cliffhanger Design")
        
        return extracted

    def _format_station_data(self, data: Dict[str, Any], title: str) -> str:
        """Format station data for inclusion in prompt"""
        if not data:
            return f"{title}: No data available"
        
        # Convert to readable format
        formatted = f"{title}:\n"
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                formatted += f"  {key}: {json.dumps(value, indent=2)}\n"
            else:
                formatted += f"  {key}: {value}\n"
        
        return formatted

    async def build_multi_world_prompt(self, inputs: Dict[str, Any]) -> str:
        """Build the comprehensive LLM prompt"""
        return self.config.prompts['main'].format(
            working_title=inputs.get('working_title', 'Untitled'),
            primary_genre=inputs.get('primary_genre', 'Unknown'),
            target_age=inputs.get('target_age', 'Unknown'),
            episode_count=inputs.get('episode_count', 'Unknown'),
            episode_length=inputs.get('episode_length', 'Unknown'),
            narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
            chosen_genre_blend=inputs.get('chosen_genre_blend', 'Unknown'),
            season_architecture=inputs.get('season_architecture', 'No data available'),
            character_bible=inputs.get('character_bible', 'No data available'),
            world_building=inputs.get('world_building', 'No data available'),
            narrative_reveal_strategy=inputs.get('narrative_reveal_strategy', 'No data available'),
            runtime_planning=inputs.get('runtime_planning', 'No data available'),
            hook_cliffhanger_design=inputs.get('hook_cliffhanger_design', 'No data available')
        )

    async def save_minimal_output(self, analysis_data: Dict[str, Any], inputs: Dict[str, Any]):
        """Save minimal output when multi-world management is not needed"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON output
        json_file = self.output_dir / f"{self.session_id}_multi_world_timeline_management.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": timestamp,
                "project_title": inputs.get('working_title', 'Untitled'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "analysis_result": "NOT_APPLICABLE",
                "analysis_data": analysis_data
            }, f, indent=2, ensure_ascii=False)
        
        # Save readable text output
        readable_file = self.output_dir / f"{self.session_id}_multi_world_timeline_management.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 13: MULTI-WORLD/TIMELINE MANAGER - ANALYSIS RESULT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Project: {inputs.get('working_title', 'Untitled')}\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("ANALYSIS RESULT: NOT APPLICABLE\n")
            f.write("=" * 60 + "\n\n")
            f.write("This project does not require multi-world/timeline management.\n\n")
            f.write("REASONING:\n")
            f.write(analysis_data.get('multi_world_analysis', {}).get('reasoning', 'No reasoning provided') + "\n\n")
            f.write("Station 13 is conditionally skipped for this project.\n")
            f.write("Proceed to Station 14: Simple Episode Blueprint.\n")
        
        # Save to Redis
        await self.redis_client.set(
            f"station_13:{self.session_id}",
            json.dumps(analysis_data, ensure_ascii=False)
        )

    async def save_comprehensive_outputs(self, analysis_data: Dict[str, Any], inputs: Dict[str, Any]):
        """Save comprehensive outputs when multi-world management is needed"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON output
        json_file = self.output_dir / f"{self.session_id}_multi_world_timeline_management.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": timestamp,
                "project_title": inputs.get('working_title', 'Untitled'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "analysis_result": "APPLICABLE",
                "analysis_data": analysis_data
            }, f, indent=2, ensure_ascii=False)
        
        # Save readable text output
        readable_file = self.output_dir / f"{self.session_id}_multi_world_timeline_management.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 13: MULTI-WORLD/TIMELINE MANAGER - COMPREHENSIVE OUTPUT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Project: {inputs.get('working_title', 'Untitled')}\n\n")
            
            # Write analysis result
            f.write("=" * 60 + "\n")
            f.write("ANALYSIS RESULT: APPLICABLE\n")
            f.write("=" * 60 + "\n\n")
            f.write("This project requires multi-world/timeline management.\n\n")
            f.write("REASONING:\n")
            f.write(analysis_data.get('multi_world_analysis', {}).get('reasoning', 'No reasoning provided') + "\n\n")
            
            # Write worlds/timelines
            worlds = analysis_data.get('worlds_timelines', [])
            if worlds:
                f.write("=" * 60 + "\n")
                f.write("WORLDS/TIMELINES\n")
                f.write("=" * 60 + "\n\n")
                for world in worlds:
                    f.write(f"World: {world.get('world_name', 'Unknown')}\n")
                    f.write(f"Description: {world.get('description', 'No description')}\n")
                    f.write(f"Audio Signature: {world.get('audio_signature', 'No signature')}\n\n")
                    
                    f.write("Rules:\n")
                    for rule in world.get('rules', []):
                        f.write(f"  • {rule}\n")
                    f.write("\n")
                    
                    f.write("Episode Usage:\n")
                    for episode in world.get('episodes_used', []):
                        f.write(f"  • Episode {episode.get('episode_number', 'N/A')}: {episode.get('duration_percentage', 'N/A')} - {episode.get('key_scenes', [])}\n")
                    f.write("\n" + "-" * 40 + "\n\n")
            
            # Write transition strategy
            transition_strategy = analysis_data.get('transition_strategy', {})
            if transition_strategy:
                f.write("=" * 60 + "\n")
                f.write("TRANSITION STRATEGY\n")
                f.write("=" * 60 + "\n\n")
                
                f.write("Transition Sounds:\n")
                for transition in transition_strategy.get('transition_sounds', []):
                    f.write(f"  • {transition.get('from_world', 'Unknown')} → {transition.get('to_world', 'Unknown')}\n")
                    f.write(f"    Sound: {transition.get('transition_sound', 'No sound')}\n")
                    f.write(f"    Duration: {transition.get('duration', 'Unknown')}\n")
                    f.write(f"    Frequency: {transition.get('usage_frequency', 'Unknown')}\n\n")
                
                f.write("Audio Differentiation:\n")
                for diff in transition_strategy.get('audio_differentiation', []):
                    f.write(f"  • {diff.get('world_name', 'Unknown')}:\n")
                    f.write(f"    Ambient: {diff.get('ambient_sounds', 'No ambient')}\n")
                    f.write(f"    Acoustics: {diff.get('acoustic_properties', 'No properties')}\n")
                    f.write(f"    Voice Treatment: {diff.get('voice_treatments', 'No treatment')}\n\n")
            
            # Write listener guidance
            guidance = analysis_data.get('listener_guidance', {})
            if guidance:
                f.write("=" * 60 + "\n")
                f.write("LISTENER GUIDANCE\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"World Identification: {guidance.get('world_identification', 'No guidance')}\n\n")
                f.write(f"Transition Clarity: {guidance.get('transition_clarity', 'No guidance')}\n\n")
                f.write(f"Consistency Rules: {guidance.get('consistency_rules', 'No rules')}\n")
        
        # Save to Redis
        await self.redis_client.set(
            f"station_13:{self.session_id}",
            json.dumps(analysis_data, ensure_ascii=False)
        )


async def main():
    """Main execution function"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return
    
    station = Station13MultiWorldTimelineManager(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
