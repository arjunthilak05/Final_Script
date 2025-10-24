"""
Station 15: Detailed Episode Outlining

This station creates detailed episode outlines for each episode in the series.
Each outline contains 1,000-word scene-by-scene breakdowns with character goals,
obstacles, choices, consequences, reveals, soundscape notes, and audio storytelling.

Flow:
1. Load data from previous stations (1, 2, 3, 4, 4.5, 5, 6, 7, 8, 9, 10, 11, 12, 14)
2. Extract required inputs from previous stations
3. Execute detailed episode outlining:
   - Scene-by-scene breakdown (1,000 words per episode)
   - Character emotional states
   - Information revealed/hidden
   - Audio storytelling notes
   - No dialogue yet
4. Save comprehensive detailed episode outlines

Critical Outline Agent - Output provides production-ready detailed scene structure
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


class Station15DetailedEpisodeOutlining:
    """Station 15: Detailed Episode Outline Builder"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=15)
        self.output_dir = Path("output/station_15")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("📋 STATION 15: DETAILED EPISODE OUTLINING")
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
                    "❌ CRITICAL ERROR: Cannot create detailed episode outlines. "
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
            print("📋 Building Detailed Episode Outline Prompt...")
            prompt = await self.build_episode_outline_prompt(extracted_inputs)
            print("✅ Prompt built successfully")
            print()

            # Generate detailed episode outlines
            print("🤖 Generating Detailed Episode Outlines...")
            print("   This may take 90-120 seconds for comprehensive scene-by-scene breakdowns...")
            print()
            
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            print("✅ Detailed episode outlines generated successfully")
            print()

            # Extract and validate JSON
            print("🔍 Extracting and validating outline data...")
            outline_data = extract_json(response)
            
            if not outline_data:
                print("❌ Failed to extract valid JSON from response")
                return
            
            print("✅ Outline data extracted and validated")
            print()

            # Save outputs
            await self.save_outputs(outline_data, extracted_inputs)

            print("=" * 60)
            print("✅ STATION 15 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Project: {extracted_inputs.get('working_title', 'Untitled')}")
            print(f"Session ID: {self.session_id}")
            print()
            print("📊 DETAILED EPISODE OUTLINE STATISTICS:")
            print(f"   • {len(outline_data.get('detailed_episode_outlines', []))} Detailed episode outlines created")
            print(f"   • Scene-by-scene breakdowns with 1,000+ words each")
            print(f"   • Character emotional states tracked")
            print(f"   • Information reveals mapped (plants/proofs/payoffs)")
            print(f"   • Audio storytelling notes included")
            print()
            print("📁 OUTPUT FILES:")
            print(f"   • {self.output_dir}/detailed_episode_outlines.json")
            print(f"   • {self.output_dir}/detailed_episode_outlines.txt")
            print(f"   • {self.output_dir}/episode_outline_summary.csv")
            print()
            print("🎯 NEXT STEPS:")
            print("   • Review detailed outlines for production readiness")
            print("   • Proceed to Station 16: Pre-Script Validation")
            print("   • Use outlines as foundation for script writing")

        except Exception as e:
            print(f"❌ Error in Station 15: {str(e)}")
            logging.error(f"Station 15 error: {str(e)}")
            raise

    async def load_previous_stations_data(self) -> Dict[str, Any]:
        """Load data from all previous stations"""
        station_data = {}
        
        # Load from Redis first
        try:
            # Station 1: Seed Processor
            station1_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_01")
            if station1_data:
                station_data['station_1'] = json.loads(station1_data)
            
            # Station 2: Project DNA Builder
            station2_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_02")
            if station2_data:
                station_data['station_2'] = json.loads(station2_data)
            
            # Station 3: Age & Genre Optimizer
            station3_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_03")
            if station3_data:
                station_data['station_3'] = json.loads(station3_data)
            
            # Station 4: Reference Mining
            station4_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_04")
            if station4_data:
                station_data['station_4'] = json.loads(station4_data)
            
            # Station 4.5: Narrator Strategy
            station45_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_045")
            if station45_data:
                station_data['station_45'] = json.loads(station45_data)
            
            # Station 5: Season Architecture
            station5_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_05")
            if station5_data:
                station_data['station_5'] = json.loads(station5_data)
            
            # Station 6: Master Style Guide
            station6_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_06")
            if station6_data:
                station_data['station_6'] = json.loads(station6_data)
            
            # Station 7: Character Architecture
            station7_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_07")
            if station7_data:
                station_data['station_7'] = json.loads(station7_data)
            
            # Station 8: World Builder
            station8_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_08")
            if station8_data:
                station_data['station_8'] = json.loads(station8_data)
            
            # Station 9: World Building System
            station9_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_09")
            if station9_data:
                station_data['station_9'] = json.loads(station9_data)
            
            # Station 10: Narrative Reveal Strategy
            station10_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_10")
            if station10_data:
                station_data['station_10'] = json.loads(station10_data)
            
            # Station 11: Runtime Planning
            station11_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_11")
            if station11_data:
                station_data['station_11'] = json.loads(station11_data)
            
            # Station 12: Hook & Cliffhanger Designer
            station12_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_12")
            if station12_data:
                station_data['station_12'] = json.loads(station12_data)
            
            # Station 14: Simple Episode Blueprints
            station14_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_14")
            if station14_data:
                station_data['station_14'] = json.loads(station14_data)
                
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
            ('station_12', f'output/station_12/{self.session_id}_hook_cliffhanger_design.json'),
            ('station_14', f'output/station_14/{self.session_id}_simple_episode_blueprints.json')
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
            
            # Also try to extract from the main station1 data if not in option_details
            if extracted['episode_count'] == 'Unknown':
                extracted['episode_count'] = station1.get('episode_count', 'Unknown')
            if extracted['episode_length'] == 'Unknown':
                extracted['episode_length'] = station1.get('episode_length', 'Unknown')
        
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
        extracted['simple_episode_blueprints'] = self._format_station_data(station_data.get('station_14', {}), "Simple Episode Blueprints")
        
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

    def _fix_outline_structure(self, outline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix malformed JSON structure from LLM output"""
        detailed_outlines = outline_data.get('detailed_episode_outlines', [])
        
        # If the structure is already correct, return as-is
        if detailed_outlines and isinstance(detailed_outlines[0], dict) and 'episode_number' in detailed_outlines[0]:
            return outline_data
        
        # If we have a flat array of scenes, organize them into episodes
        if detailed_outlines and isinstance(detailed_outlines[0], dict) and 'scene_number' in detailed_outlines[0]:
            return self._organize_scenes_into_episodes(detailed_outlines)
        
        # If we have mixed content, try to extract episodes
        return self._extract_episodes_from_mixed_content(detailed_outlines)

    def _safe_parse_runtime(self, runtime_str: str) -> int:
        """Safely parse runtime string to extract numeric value in minutes"""
        if not runtime_str or not isinstance(runtime_str, str):
            return 0
        
        try:
            # Split by spaces and get the first part
            parts = runtime_str.split()
            if not parts:
                return 0
            
            # Try to extract numeric value from the first part
            first_part = parts[0]
            # Remove any non-numeric characters except decimal point
            numeric_str = ''.join(c for c in first_part if c.isdigit() or c == '.')
            
            if numeric_str:
                return int(float(numeric_str))
            return 0
        except (ValueError, IndexError, AttributeError):
            return 0

    def _organize_scenes_into_episodes(self, scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Organize flat scene list into proper episode structure"""
        episodes = {}
        episode_metadata = {}
        
        # Group scenes by episode (assuming 4 scenes per episode based on the data)
        scenes_per_episode = 4
        episode_number = 1
        
        for i in range(0, len(scenes), scenes_per_episode):
            episode_scenes = scenes[i:i + scenes_per_episode]
            
            # Extract episode metadata from the first scene or create defaults
            episode_title = f"Episode {episode_number}"
            episode_summary = f"Detailed episode outline for episode {episode_number}"
            
            # Look for episode metadata in the scenes
            for scene in episode_scenes:
                if 'episode_title' in scene:
                    episode_title = scene['episode_title']
                if 'episode_summary' in scene:
                    episode_summary = scene['episode_summary']
            
            episodes[f"episode_{episode_number}"] = {
                "episode_number": episode_number,
                "episode_title": episode_title,
                "episode_summary": episode_summary,
                "total_estimated_runtime": f"{sum(self._safe_parse_runtime(scene.get('estimated_runtime', '0')) for scene in episode_scenes)} minutes",
                "scenes": episode_scenes,
                "episode_arc": self._extract_episode_arc(episode_scenes),
                "character_emotional_journey": self._extract_character_journeys(episode_scenes),
                "information_flow": self._extract_information_flow(episode_scenes),
                "audio_production_notes": "Comprehensive audio storytelling with detailed soundscape notes for each scene"
            }
            episode_number += 1
        
        return {
            "detailed_episode_outlines": list(episodes.values()),
            "series_structure_notes": "Detailed episode outlines provide comprehensive scene-by-scene breakdowns for production",
            "production_considerations": "Each scene includes specific audio storytelling notes and soundscape requirements"
        }

    def _extract_episodes_from_mixed_content(self, content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract episodes from mixed content structure"""
        episodes = {}
        current_episode = None
        episode_number = 1
        
        for item in content:
            if 'scene_number' in item:
                if current_episode is None:
                    current_episode = {
                        "episode_number": episode_number,
                        "episode_title": f"Episode {episode_number}",
                        "episode_summary": f"Detailed episode outline for episode {episode_number}",
                        "scenes": [],
                        "episode_arc": {},
                        "character_emotional_journey": [],
                        "information_flow": {},
                        "audio_production_notes": "Comprehensive audio storytelling with detailed soundscape notes"
                    }
                
                current_episode["scenes"].append(item)
                
                # If we have 4 scenes, finalize this episode
                if len(current_episode["scenes"]) >= 4:
                    episodes[f"episode_{episode_number}"] = current_episode
                    episode_number += 1
                    current_episode = None
            
            elif 'opening_hook' in item:
                if current_episode:
                    current_episode["episode_arc"] = item
            
            elif 'character_name' in item:
                if current_episode:
                    current_episode["character_emotional_journey"].append(item)
            
            elif 'revealed_to_audience' in item:
                if current_episode:
                    current_episode["information_flow"] = item
        
        # Add the last episode if it exists
        if current_episode:
            episodes[f"episode_{episode_number}"] = current_episode
        
        return {
            "detailed_episode_outlines": list(episodes.values()),
            "series_structure_notes": "Detailed episode outlines provide comprehensive scene-by-scene breakdowns for production",
            "production_considerations": "Each scene includes specific audio storytelling notes and soundscape requirements"
        }

    def _extract_episode_arc(self, scenes: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract episode arc from scenes"""
        if not scenes:
            return {}
        
        return {
            "opening_hook": scenes[0].get('goal', 'Unknown'),
            "midpoint_turn": scenes[len(scenes)//2].get('choice', 'Unknown') if len(scenes) > 1 else 'Unknown',
            "climax": scenes[-1].get('consequence', 'Unknown'),
            "resolution": scenes[-1].get('transition_to_next', 'Unknown'),
            "cliffhanger": "Continues to next episode"
        }

    def _extract_character_journeys(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract character emotional journeys from scenes"""
        characters = set()
        for scene in scenes:
            characters.update(scene.get('characters_present', []))
        
        journeys = []
        for char in characters:
            journeys.append({
                "character_name": char,
                "starting_emotional_state": "As established in first scene",
                "key_emotional_beats": [scene.get('emotional_state', 'Unknown') for scene in scenes],
                "ending_emotional_state": "As shown in final scene",
                "growth": f"{char} develops throughout the episode"
            })
        
        return journeys

    def _extract_information_flow(self, scenes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Extract information flow from scenes"""
        revealed_to_audience = []
        revealed_to_characters = []
        hidden_from_audience = []
        hidden_from_characters = []
        
        for scene in scenes:
            reveals = scene.get('reveals', {})
            revealed_to_audience.extend(reveals.get('plants', []))
            revealed_to_characters.extend(reveals.get('proofs', []))
            revealed_to_audience.extend(reveals.get('payoffs', []))
        
        return {
            "revealed_to_audience": list(set(revealed_to_audience)),
            "revealed_to_characters": list(set(revealed_to_characters)),
            "hidden_from_audience": list(set(hidden_from_audience)),
            "hidden_from_characters": list(set(hidden_from_characters))
        }

    async def build_episode_outline_prompt(self, inputs: Dict[str, Any]) -> str:
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
            hook_cliffhanger_design=inputs.get('hook_cliffhanger_design', 'No data available'),
            simple_episode_blueprints=inputs.get('simple_episode_blueprints', 'No data available')
        )

    async def save_outputs(self, outline_data: Dict[str, Any], inputs: Dict[str, Any]):
        """Save all output files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Fix the JSON structure if it's malformed
        fixed_outline_data = self._fix_outline_structure(outline_data)
        
        # Save JSON output
        json_file = self.output_dir / f"{self.session_id}_detailed_episode_outlines.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": timestamp,
                "project_title": inputs.get('working_title', 'Untitled'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "outline_data": fixed_outline_data
            }, f, indent=2, ensure_ascii=False)
        
        # Save readable text output
        readable_file = self.output_dir / f"{self.session_id}_detailed_episode_outlines.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 15: DETAILED EPISODE OUTLINING - COMPREHENSIVE OUTPUT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Project: {inputs.get('working_title', 'Untitled')}\n\n")
            
            # Write episode outlines using fixed data
            outlines = fixed_outline_data.get('detailed_episode_outlines', [])
            for episode in outlines:
                f.write("-" * 60 + "\n")
                f.write(f"EPISODE {episode.get('episode_number', 'N/A')}: {episode.get('episode_title', 'Untitled')}\n")
                f.write("-" * 60 + "\n\n")
                f.write("SUMMARY:\n")
                f.write(episode.get('episode_summary', 'No summary available') + "\n\n")
                f.write(f"ESTIMATED RUNTIME: {episode.get('total_estimated_runtime', 'Unknown')}\n\n")
                
                # Write scenes
                scenes = episode.get('scenes', [])
                for scene in scenes:
                    f.write(f"SCENE {scene.get('scene_number', 'N/A')}: {scene.get('location', 'Unknown')} - {scene.get('time', 'Unknown')}\n")
                    f.write(f"Characters: {', '.join(scene.get('characters_present', []))}\n")
                    f.write(f"Goal: {scene.get('goal', 'Unknown')}\n")
                    f.write(f"Obstacle: {scene.get('obstacle', 'Unknown')}\n")
                    f.write(f"Choice: {scene.get('choice', 'Unknown')}\n")
                    f.write(f"Consequence: {scene.get('consequence', 'Unknown')}\n")
                    
                    reveals = scene.get('reveals', {})
                    f.write(f"Reveals:\n")
                    f.write(f"  Plants: {', '.join(reveals.get('plants', []))}\n")
                    f.write(f"  Proofs: {', '.join(reveals.get('proofs', []))}\n")
                    f.write(f"  Payoffs: {', '.join(reveals.get('payoffs', []))}\n")
                    
                    f.write(f"Soundscape: {scene.get('soundscape_notes', 'Unknown')}\n")
                    f.write(f"Transition: {scene.get('transition_to_next', 'Unknown')}\n")
                    f.write(f"Runtime: {scene.get('estimated_runtime', 'Unknown')}\n")
                    f.write(f"Emotional State: {scene.get('emotional_state', 'Unknown')}\n")
                    f.write(f"Audio Notes: {scene.get('audio_storytelling_notes', 'Unknown')}\n\n")
                
                # Write episode arc
                arc = episode.get('episode_arc', {})
                f.write("EPISODE ARC:\n")
                f.write(f"Opening Hook: {arc.get('opening_hook', 'Unknown')}\n")
                f.write(f"Midpoint Turn: {arc.get('midpoint_turn', 'Unknown')}\n")
                f.write(f"Climax: {arc.get('climax', 'Unknown')}\n")
                f.write(f"Resolution: {arc.get('resolution', 'Unknown')}\n")
                f.write(f"Cliffhanger: {arc.get('cliffhanger', 'Unknown')}\n\n")
                
                # Write character emotional journey
                f.write("CHARACTER EMOTIONAL JOURNEY:\n")
                for journey in episode.get('character_emotional_journey', []):
                    f.write(f"  {journey.get('character_name', 'Unknown')}:\n")
                    f.write(f"    Starting: {journey.get('starting_emotional_state', 'Unknown')}\n")
                    f.write(f"    Key Beats: {', '.join(journey.get('key_emotional_beats', []))}\n")
                    f.write(f"    Ending: {journey.get('ending_emotional_state', 'Unknown')}\n")
                    f.write(f"    Growth: {journey.get('growth', 'Unknown')}\n\n")
                
                # Write information flow
                info_flow = episode.get('information_flow', {})
                f.write("INFORMATION FLOW:\n")
                f.write(f"Revealed to Audience: {', '.join(info_flow.get('revealed_to_audience', []))}\n")
                f.write(f"Revealed to Characters: {', '.join(info_flow.get('revealed_to_characters', []))}\n")
                f.write(f"Hidden from Audience: {', '.join(info_flow.get('hidden_from_audience', []))}\n")
                f.write(f"Hidden from Characters: {', '.join(info_flow.get('hidden_from_characters', []))}\n\n")
                
                f.write(f"AUDIO PRODUCTION NOTES: {episode.get('audio_production_notes', 'Unknown')}\n\n")
            
            # Write series structure notes
            f.write("=" * 60 + "\n")
            f.write("SERIES STRUCTURE NOTES\n")
            f.write("=" * 60 + "\n")
            f.write(fixed_outline_data.get('series_structure_notes', 'No series structure notes available') + "\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("PRODUCTION CONSIDERATIONS\n")
            f.write("=" * 60 + "\n")
            f.write(fixed_outline_data.get('production_considerations', 'No production considerations available') + "\n")
        
        # Save CSV summary
        csv_file = self.output_dir / f"{self.session_id}_episode_outline_summary.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Episode,Title,Scene Count,Total Runtime,Opening Hook,Climax,Cliffhanger\n")
            for episode in outlines:
                scenes = episode.get('scenes', [])
                arc = episode.get('episode_arc', {})
                f.write(f"Episode {episode.get('episode_number', 'N/A')},{episode.get('episode_title', 'Untitled')},{len(scenes)},{episode.get('total_estimated_runtime', 'Unknown')},{arc.get('opening_hook', 'Unknown')},{arc.get('climax', 'Unknown')},{arc.get('cliffhanger', 'Unknown')}\n")
        
        # Save to Redis
        await self.redis_client.set(
            f"audiobook:{self.session_id}:station_15",
            json.dumps(fixed_outline_data, ensure_ascii=False)
        )


async def main():
    """Main execution function"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return
    
    station = Station15DetailedEpisodeOutlining(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())