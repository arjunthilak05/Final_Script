"""
Station 14: Simple Episode Blueprint

This station creates simple episode blueprints for each episode in the series.
Each blueprint contains 2-3 paragraph summaries, character goals and obstacles,
and story connections without dialogue.

Flow:
1. Load data from previous stations (1, 2, 3, 4, 4.5, 5, 6, 7, 8, 9, 10, 11, 12)
2. Extract required inputs from previous stations
3. Execute simple episode blueprint creation:
   - Episode summaries (2-3 paragraphs each)
   - Character goals and obstacles
   - Story connections
   - Key story beats
   - Series arc summary
4. Save comprehensive simple episode blueprint document

Critical Blueprint Agent - Output provides stakeholder-ready episode summaries
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


class Station14SimpleEpisodeBlueprint:
    """Station 14: Simple Episode Blueprint Creator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=14)
        self.output_dir = Path("output/station_14")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("📋 STATION 14: SIMPLE EPISODE BLUEPRINT")
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
                    "❌ CRITICAL ERROR: Cannot create simple episode blueprints. "
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
            print("📋 Building Simple Episode Blueprint Prompt...")
            prompt = await self.build_episode_blueprint_prompt(extracted_inputs)
            print("✅ Prompt built successfully")
            print()

            # Generate simple episode blueprints
            print("🤖 Generating Simple Episode Blueprints...")
            print("   This may take 60-90 seconds for comprehensive episode summaries...")
            print()
            
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            print("✅ Simple episode blueprints generated successfully")
            print()

            # Extract and validate JSON
            print("🔍 Extracting and validating blueprint data...")
            blueprint_data = extract_json(response)
            
            if not blueprint_data:
                print("❌ Failed to extract valid JSON from response")
                return
            
            print("✅ Blueprint data extracted and validated")
            print()

            # Save outputs
            await self.save_outputs(blueprint_data, extracted_inputs)

            print("=" * 60)
            print("✅ STATION 14 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Project: {extracted_inputs.get('working_title', 'Untitled')}")
            print(f"Session ID: {self.session_id}")
            print()
            print("📊 SIMPLE EPISODE BLUEPRINT STATISTICS:")
            print(f"   • {len(blueprint_data.get('simple_episode_blueprints', []))} Episode blueprints created")
            print(f"   • Simple language summaries for stakeholder review")
            print(f"   • Character goals and obstacles mapped")
            print(f"   • Story connections documented")
            print()
            print("📁 OUTPUT FILES:")
            print(f"   • {self.output_dir}/simple_episode_blueprints.json")
            print(f"   • {self.output_dir}/simple_episode_blueprints.txt")
            print(f"   • {self.output_dir}/episode_blueprint_summary.csv")
            print()
            print("🎯 NEXT STEPS:")
            print("   • Review episode blueprints for stakeholder approval")
            print("   • Proceed to Station 15: Detailed Episode Outlining")
            print("   • Use blueprints as foundation for detailed scene-by-scene outlines")

        except Exception as e:
            print(f"❌ Error in Station 14: {str(e)}")
            logging.error(f"Station 14 error: {str(e)}")
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

    async def build_episode_blueprint_prompt(self, inputs: Dict[str, Any]) -> str:
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

    async def save_outputs(self, blueprint_data: Dict[str, Any], inputs: Dict[str, Any]):
        """Save all output files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON output
        json_file = self.output_dir / f"{self.session_id}_simple_episode_blueprints.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": timestamp,
                "project_title": inputs.get('working_title', 'Untitled'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "blueprint_data": blueprint_data
            }, f, indent=2, ensure_ascii=False)
        
        # Save readable text output
        readable_file = self.output_dir / f"{self.session_id}_simple_episode_blueprints.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 14: SIMPLE EPISODE BLUEPRINT - COMPREHENSIVE OUTPUT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Project: {inputs.get('working_title', 'Untitled')}\n\n")
            
            # Write episode blueprints
            blueprints = blueprint_data.get('simple_episode_blueprints', [])
            for episode in blueprints:
                f.write("-" * 60 + "\n")
                f.write(f"EPISODE {episode.get('episode_number', 'N/A')}: {episode.get('episode_title', 'Untitled')}\n")
                f.write("-" * 60 + "\n\n")
                f.write("SUMMARY:\n")
                f.write(episode.get('simple_summary', 'No summary available') + "\n\n")
                
                f.write("CHARACTER ARCS:\n")
                for arc in episode.get('character_arcs', []):
                    f.write(f"  • {arc.get('character_name', 'Unknown')}:\n")
                    f.write(f"    Goal: {arc.get('goal', 'Unknown')}\n")
                    f.write(f"    Obstacle: {arc.get('obstacle', 'Unknown')}\n")
                    f.write(f"    Growth: {arc.get('growth', 'Unknown')}\n\n")
                
                f.write("STORY CONNECTIONS:\n")
                for connection in episode.get('story_connections', []):
                    f.write(f"  • {connection}\n")
                f.write("\n")
                
                f.write("KEY BEATS:\n")
                for beat in episode.get('key_beats', []):
                    f.write(f"  • {beat}\n")
                f.write("\n")
                
                f.write(f"EMOTIONAL TONE: {episode.get('emotional_tone', 'Unknown')}\n")
                f.write(f"CLIFFHANGER: {episode.get('cliffhanger_note', 'Unknown')}\n\n")
            
            # Write series summaries
            f.write("=" * 60 + "\n")
            f.write("SERIES ARC SUMMARY\n")
            f.write("=" * 60 + "\n")
            f.write(blueprint_data.get('series_arc_summary', 'No series arc summary available') + "\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("CHARACTER JOURNEY SUMMARY\n")
            f.write("=" * 60 + "\n")
            f.write(blueprint_data.get('character_journey_summary', 'No character journey summary available') + "\n")
        
        # Save CSV summary
        csv_file = self.output_dir / f"{self.session_id}_episode_blueprint_summary.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Episode,Title,Emotional Tone,Key Character Goal,Main Obstacle\n")
            for episode in blueprints:
                main_goal = ""
                main_obstacle = ""
                if episode.get('character_arcs'):
                    main_goal = episode['character_arcs'][0].get('goal', '')
                    main_obstacle = episode['character_arcs'][0].get('obstacle', '')
                
                f.write(f"Episode {episode.get('episode_number', 'N/A')},{episode.get('episode_title', 'Untitled')},{episode.get('emotional_tone', 'Unknown')},{main_goal},{main_obstacle}\n")
        
        # Save to Redis
        await self.redis_client.set(
            f"station_14:{self.session_id}",
            json.dumps(blueprint_data, ensure_ascii=False)
        )


async def main():
    """Main execution function"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return
    
    station = Station14SimpleEpisodeBlueprint(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
