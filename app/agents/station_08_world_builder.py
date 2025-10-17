"""
Station 8: World Builder

This station functions as a World Builder for audio drama production.
It constructs the World Bible, a detailed, audio-focused guide to the story's 
setting, systems, and history, which serves as a foundational document for 
sound design and narrative consistency.

Flow:
1. Load Project Bible from Station 2
2. Load Character Bible from Station 7
3. Extract required inputs from previous stations
4. Execute world building analysis:
   - Geography_Spaces: Key locations with sonic signatures and ambient sounds
   - Social_Systems: Government, economy, hierarchies with associated sounds
   - Technology_Magic: Systems with specific sound design elements
   - History_Lore: Past events and myths with sonic themes
   - Sensory_Palette: Comprehensive audio cue library
5. Save comprehensive World Bible document

Critical World Building Agent - Output guides all world-related creative decisions
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


class Station08WorldBuilder:
    """Station 8: World Builder"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=8)
        # Load additional config from YAML directly
        self._load_additional_config()
        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_08'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path
        
        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_8.yml'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🌍 STATION 8: WORLD BUILDER")
        print("=" * 60)
        print()

        try:
            # Load Project Bible from Station 2
            project_bible_data = await self.load_project_bible()
            
            # Load Character Bible from Station 7
            character_bible_data = await self.load_character_bible()
            
            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs()
            
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
            print(f"Story Complexity: {extracted_inputs.get('story_complexity', 'N/A')}")
            print(f"Tone: {extracted_inputs.get('tone', 'N/A')}")
            print(f"Core Premise: {extracted_inputs.get('core_premise', 'N/A')}")
            print(f"Main Characters: {', '.join(extracted_inputs.get('main_characters', []))}")
            print("-" * 60)
            print()

            # Build the comprehensive LLM prompt
            print("🌍 Building World Bible Construction Prompt...")
            prompt = await self.build_world_bible_prompt(extracted_inputs, project_bible_data, character_bible_data)
            print("✅ Prompt built successfully")
            print(f"📊 Prompt length: {len(prompt)} characters")
            print(f"📊 Estimated tokens: ~{len(prompt) // 4} tokens")
            print()

            # Execute the world building analysis
            print("=" * 60)
            print("🎯 EXECUTING WORLD BIBLE CONSTRUCTION")
            print("=" * 60)
            print()

            print("📝 Sending request to LLM...")
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            print("✅ LLM response received")
            print(f"📊 Response length: {len(response) if response else 0} characters")
            if response:
                print(f"📊 Response preview: {response[:200]}...")
            else:
                print("❌ Response is empty or None")
            print()

            # Process the response
            print("🔍 Processing LLM response...")
            world_bible_data = extract_json(response)
            
            if not world_bible_data:
                raise ValueError("❌ Failed to extract valid JSON from LLM response")

            # Validate world bible structure
            await self.validate_world_bible_structure(world_bible_data)

            # Generate human-readable summary
            print("📄 Generating human-readable summary...")
            readable_summary = await self.generate_readable_summary(world_bible_data, extracted_inputs)
            print("✅ Summary generated")
            print()

            # Compile final report
            final_report = await self.compile_final_report(
                extracted_inputs, world_bible_data, readable_summary
            )

            # Save outputs
            await self.save_outputs(final_report)

            print()
            print("=" * 60)
            print("✅ STATION 8 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Session ID: {self.session_id}")
            title = extracted_inputs.get('working_title', 'N/A')
            print(TitleValidator.format_title_for_display(title, "Station 8"))
            print()
            print("📄 Output files:")
            print(f"   - {self.output_dir}/{self.session_id}_world_bible.json")
            print(f"   - {self.output_dir}/{self.session_id}_readable.txt")
            print()
            print("🌍 WORLD BIBLE COMPLETE")
            print("📌 Ready to proceed to Station 9")
            print()

        except Exception as e:
            print(f"❌ Station 8 failed: {str(e)}")
            logging.error(f"Station 8 error: {str(e)}")
            raise

    async def load_project_bible(self) -> Dict:
        """Load Project Bible from Station 2"""
        try:
            # Construct the path to the Project Bible
            bible_path = Path(self.config_data.get('input', {}).get('project_bible_path', 'output/station_02/{session_id}_bible.json').format(session_id=self.session_id))
            
            if not bible_path.exists():
                raise ValueError(f"❌ Project Bible not found at {bible_path}\n   Please run Station 2 first to generate the Project Bible")
            
            # Load and parse the Project Bible
            with open(bible_path, 'r', encoding='utf-8') as f:
                project_bible_data = json.load(f)
            
            print(f"✅ Loaded Project Bible from {bible_path}")
            return project_bible_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Project Bible: {str(e)}")
        except FileNotFoundError:
            raise ValueError(f"❌ Project Bible file not found at {bible_path}\n   Please run Station 2 first")
        except Exception as e:
            raise ValueError(f"❌ Error loading Project Bible: {str(e)}")

    async def load_character_bible(self) -> Dict:
        """Load Character Bible from Station 7"""
        try:
            # Construct the path to the Character Bible
            character_bible_path = Path(self.config_data.get('input', {}).get('character_bible_path', 'output/station_07/{session_id}_character_bible.json').format(session_id=self.session_id))
            
            if not character_bible_path.exists():
                raise ValueError(f"❌ Character Bible not found at {character_bible_path}\n   Please run Station 7 first to generate the Character Bible")
            
            # Load and parse the Character Bible
            with open(character_bible_path, 'r', encoding='utf-8') as f:
                character_bible_data = json.load(f)
            
            print(f"✅ Loaded Character Bible from {character_bible_path}")
            return character_bible_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Character Bible: {str(e)}")
        except FileNotFoundError:
            raise ValueError(f"❌ Character Bible file not found at {character_bible_path}\n   Please run Station 7 first")
        except Exception as e:
            raise ValueError(f"❌ Error loading Character Bible: {str(e)}")

    async def extract_required_inputs(self) -> Dict:
        """Extract required inputs from previous stations"""
        try:
            # Load Station 1 data for story complexity, episode count, length, main characters
            station1_key = f"audiobook:{self.session_id}:station_01"
            station1_raw = await self.redis_client.get(station1_key)
            if not station1_raw:
                raise ValueError(f"❌ No Station 1 data found for session {self.session_id}")
            station1_data = json.loads(station1_raw)

            # Load Station 2 data for working title, core premise
            station2_key = f"audiobook:{self.session_id}:station_02"
            station2_raw = await self.redis_client.get(station2_key)
            if not station2_raw:
                raise ValueError(f"❌ No Station 2 data found for session {self.session_id}")
            station2_data = json.loads(station2_raw)

            # Load Station 3 data for genre and tone
            station3_key = f"audiobook:{self.session_id}:station_03"
            station3_raw = await self.redis_client.get(station3_key)
            if not station3_raw:
                raise ValueError(f"❌ No Station 3 data found for session {self.session_id}")
            station3_data = json.loads(station3_raw)

            # Extract required fields with error handling
            extracted = {}
            
            # From Station 1
            station1_options = station1_data.get('option_details', {})
            extracted['story_complexity'] = station1_data.get('story_complexity', 'Unknown')
            extracted['episode_count'] = station1_options.get('episode_count', 'Unknown')
            extracted['episode_length'] = station1_options.get('episode_length', 'Unknown')
            extracted['main_characters'] = station1_data.get('main_characters', [])
            
            # Use bulletproof title extraction
            extracted['working_title'] = TitleValidator.extract_bulletproof_title(station1_data, station2_data)
            extracted['core_premise'] = station2_data.get('world_setting', {}).get('core_premise', 'Unknown')
            
            # From Station 3
            chosen_blend = station3_data.get('chosen_blend_details', {})
            extracted['primary_genre'] = chosen_blend.get('primary_genre', 'Unknown')
            
            age_guidelines = station3_data.get('age_guidelines', {})
            extracted['target_age'] = age_guidelines.get('target_age_range', 'Unknown')
            
            tone_calibration = station3_data.get('tone_calibration', {})
            extracted['tone'] = tone_calibration.get('light_dark_balance', 'Balanced')

            return extracted

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing station data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error extracting required inputs: {str(e)}")

    async def build_world_bible_prompt(self, inputs: Dict, project_bible_data: Dict, character_bible_data: Dict) -> str:
        """Build the comprehensive world bible construction prompt"""
        try:
            # Get the base prompt from config
            base_prompt = self.config.get_prompt('world_bible_construction')
            
            # Create summaries to reduce prompt size
            project_bible_summary = self._create_project_bible_summary(project_bible_data)
            character_bible_summary = self._create_character_bible_summary(character_bible_data)
            
            # Format the prompt with project data
            formatted_prompt = base_prompt.format(
                working_title=inputs.get('working_title', 'Unknown'),
                primary_genre=inputs.get('primary_genre', 'Unknown'),
                target_age=inputs.get('target_age', 'Unknown'),
                episode_count=inputs.get('episode_count', 'Unknown'),
                episode_length=inputs.get('episode_length', 'Unknown'),
                story_complexity=inputs.get('story_complexity', 'Unknown'),
                tone=inputs.get('tone', 'Balanced'),
                core_premise=inputs.get('core_premise', 'Unknown'),
                main_characters=', '.join(inputs.get('main_characters', [])),
                project_bible_summary=project_bible_summary,
                character_bible_summary=character_bible_summary
            )
            
            return formatted_prompt
            
        except Exception as e:
            raise ValueError(f"❌ Error building prompt: {str(e)}")

    def _create_project_bible_summary(self, project_bible_data: Dict) -> str:
        """Create a concise summary of the Project Bible data"""
        try:
            # Extract key information from Project Bible
            project_bible = project_bible_data.get('Project Bible Document', {})
            world_setting = project_bible.get('world_setting', {})
            creative_promises = project_bible.get('creative_promises', {})
            
            summary_parts = []
            
            # Core premise and world
            summary_parts.append(f"Core Premise: {world_setting.get('core_premise', 'N/A')}")
            summary_parts.append(f"Primary Location: {world_setting.get('primary_location', 'N/A')}")
            summary_parts.append(f"Time Period: {world_setting.get('time_period', 'N/A')}")
            
            # Key locations
            key_locations = world_setting.get('key_locations', [])
            if key_locations:
                summary_parts.append(f"Key Locations: {', '.join(key_locations[:5])}")  # Limit to 5
            
            # Creative promises
            unique_selling_points = creative_promises.get('unique_selling_points', [])
            if unique_selling_points:
                summary_parts.append(f"Unique Elements: {', '.join(unique_selling_points[:3])}")  # Limit to 3
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            return f"Error creating Project Bible summary: {str(e)}"

    def _create_character_bible_summary(self, character_bible_data: Dict) -> str:
        """Create a concise summary of the Character Bible data"""
        try:
            # Extract key information from Character Bible
            character_bible_doc = character_bible_data.get('Character Bible Document', {})
            character_bible = character_bible_doc.get('character_bible', {})
            
            summary_parts = []
            
            # Character counts by tier
            tier1_count = len(character_bible.get('tier_1_protagonists', []))
            tier2_count = len(character_bible.get('tier_2_major_supporting', []))
            tier3_count = len(character_bible.get('tier_3_recurring', []))
            
            summary_parts.append(f"Tier 1 Protagonists: {tier1_count}")
            summary_parts.append(f"Tier 2 Major Supporting: {tier2_count}")
            summary_parts.append(f"Tier 3 Recurring: {tier3_count}")
            
            # Main character names
            tier1_characters = character_bible.get('tier_1_protagonists', [])
            if tier1_characters:
                protagonist_names = [char.get('name', 'Unknown') for char in tier1_characters]
                summary_parts.append(f"Main Protagonists: {', '.join(protagonist_names)}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            return f"Error creating Character Bible summary: {str(e)}"

    async def validate_world_bible_structure(self, world_bible_data: Dict):
        """Validate that world bible structure matches requirements"""
        try:
            world_bible = world_bible_data.get('world_bible', {})
            
            # Check required top-level sections
            required_sections = [
                'Geography_Spaces', 'Social_Systems', 'Technology_Magic', 
                'History_Lore', 'Sensory_Palette'
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in world_bible:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"⚠️  Warning: Missing required sections: {', '.join(missing_sections)}")
            
            # Check Geography_Spaces structure
            geography = world_bible.get('Geography_Spaces', {})
            key_locations = geography.get('key_locations', [])
            location_count = len(key_locations)
            
            print(f"📊 World Bible Structure Validation:")
            print(f"   Key Locations: {location_count}")
            print(f"   Required Sections: {len([s for s in required_sections if s in world_bible])}/{len(required_sections)}")
            
            # Validate location count (5-10 as specified)
            if location_count < 5:
                print(f"⚠️  Warning: Location count ({location_count}) is below minimum (5)")
            elif location_count > 10:
                print(f"⚠️  Warning: Location count ({location_count}) exceeds maximum (10)")
            
            print("✅ World Bible structure validation complete")
            
        except Exception as e:
            print(f"⚠️  Warning: World Bible structure validation failed: {str(e)}")

    async def generate_readable_summary(self, world_bible_data: Dict, inputs: Dict) -> str:
        """Generate human-readable summary from structured JSON data"""
        try:
            summary_parts = []
            
            # Header
            summary_parts.append("=" * 70)
            summary_parts.append("STATION 8: WORLD BUILDER")
            summary_parts.append("=" * 70)
            summary_parts.append("")
            summary_parts.append(f"Working Title: {inputs.get('working_title', 'N/A')}")
            summary_parts.append(f"Primary Genre: {inputs.get('primary_genre', 'N/A')}")
            summary_parts.append(f"Target Age: {inputs.get('target_age', 'N/A')}")
            summary_parts.append(f"Episode Count: {inputs.get('episode_count', 'N/A')}")
            summary_parts.append(f"Core Premise: {inputs.get('core_premise', 'N/A')}")
            summary_parts.append("")
            
            # World Bible sections
            world_bible = world_bible_data.get('world_bible', {})
            
            # Geography_Spaces
            geography = world_bible.get('Geography_Spaces', {})
            if geography:
                summary_parts.append("-" * 70)
                summary_parts.append("GEOGRAPHY & SPACES")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                key_locations = geography.get('key_locations', [])
                for i, location in enumerate(key_locations, 1):
                    name = location.get('name', 'Unknown')
                    sonic_sig = location.get('sonic_signature', 'N/A')
                    ambient = location.get('ambient_sounds', 'N/A')
                    summary_parts.append(f"{i}. {name}")
                    summary_parts.append(f"   Sonic Signature: {sonic_sig}")
                    summary_parts.append(f"   Ambient Sounds: {ambient}")
                    summary_parts.append("")
                
                travel_times = geography.get('travel_times', 'N/A')
                summary_parts.append(f"Travel Times & Sounds: {travel_times}")
                summary_parts.append("")
            
            # Social_Systems
            social_systems = world_bible.get('Social_Systems', {})
            if social_systems:
                summary_parts.append("-" * 70)
                summary_parts.append("SOCIAL SYSTEMS")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                government = social_systems.get('government_authority', {})
                if government:
                    summary_parts.append(f"Government: {government.get('description', 'N/A')}")
                    summary_parts.append(f"Associated Sounds: {government.get('associated_sounds', 'N/A')}")
                    summary_parts.append("")
                
                economy = social_systems.get('economic_structure', {})
                if economy:
                    summary_parts.append(f"Economy: {economy.get('description', 'N/A')}")
                    summary_parts.append(f"Economic Sounds: {economy.get('sounds', 'N/A')}")
                    summary_parts.append("")
                
                hierarchies = social_systems.get('social_hierarchies', {})
                if hierarchies:
                    summary_parts.append(f"Social Hierarchies: {hierarchies.get('description', 'N/A')}")
                    summary_parts.append(f"Sonic Representation: {hierarchies.get('sonic_representation', 'N/A')}")
                    summary_parts.append("")
            
            # Technology_Magic
            tech_magic = world_bible.get('Technology_Magic', {})
            if tech_magic:
                summary_parts.append("-" * 70)
                summary_parts.append("TECHNOLOGY & MAGIC")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                summary_parts.append(f"Overview: {tech_magic.get('overview', 'N/A')}")
                summary_parts.append(f"Sound Design: {tech_magic.get('sound_design', 'N/A')}")
                summary_parts.append(f"Limitations: {tech_magic.get('limitations', 'N/A')}")
                summary_parts.append(f"Prevalence: {tech_magic.get('prevalence', 'N/A')}")
                summary_parts.append("")
            
            # History_Lore
            history_lore = world_bible.get('History_Lore', {})
            if history_lore:
                summary_parts.append("-" * 70)
                summary_parts.append("HISTORY & LORE")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                key_events = history_lore.get('key_past_events', [])
                if key_events:
                    summary_parts.append("Key Past Events:")
                    for i, event in enumerate(key_events, 1):
                        event_desc = event.get('event', 'N/A')
                        sonic_impact = event.get('sonic_impact', 'N/A')
                        summary_parts.append(f"  {i}. {event_desc}")
                        summary_parts.append(f"     Sonic Impact: {sonic_impact}")
                    summary_parts.append("")
                
                myths_legends = history_lore.get('myths_legends', [])
                if myths_legends:
                    summary_parts.append("Myths & Legends:")
                    for i, myth in enumerate(myths_legends, 1):
                        story = myth.get('story', 'N/A')
                        sonic_themes = myth.get('sonic_themes', 'N/A')
                        summary_parts.append(f"  {i}. {story}")
                        summary_parts.append(f"     Sonic Themes: {sonic_themes}")
                    summary_parts.append("")
            
            # Sensory_Palette
            sensory_palette = world_bible.get('Sensory_Palette', {})
            if sensory_palette:
                summary_parts.append("-" * 70)
                summary_parts.append("SENSORY PALETTE")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                audio_cue_library = sensory_palette.get('audio_cue_library', [])
                if audio_cue_library:
                    summary_parts.append("Audio Cue Library:")
                    for i, cue in enumerate(audio_cue_library, 1):
                        location_situation = cue.get('location_situation', 'N/A')
                        ambient_sounds = cue.get('ambient_sounds', 'N/A')
                        summary_parts.append(f"  {i}. {location_situation}")
                        summary_parts.append(f"     Ambient Sounds: {ambient_sounds}")
                    summary_parts.append("")
            
            summary_parts.append("=" * 70)
            summary_parts.append("END OF WORLD BIBLE")
            summary_parts.append("=" * 70)
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            raise ValueError(f"❌ Error generating readable summary: {str(e)}")

    async def compile_final_report(self, inputs: Dict, world_bible_data: Dict, readable_summary: str) -> Dict:
        """Compile the final comprehensive report"""
        return {
            "World Bible Document": {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "working_title": inputs.get('working_title', 'Unknown'),
                "primary_genre": inputs.get('primary_genre', 'Unknown'),
                "target_age": inputs.get('target_age', 'Unknown'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "episode_length": inputs.get('episode_length', 'Unknown'),
                "story_complexity": inputs.get('story_complexity', 'Unknown'),
                "tone": inputs.get('tone', 'Unknown'),
                "core_premise": inputs.get('core_premise', 'Unknown'),
                "world_bible": world_bible_data.get('world_bible', {}),
                "readable_summary": readable_summary
            }
        }

    async def save_outputs(self, report: Dict):
        """Save all output files (JSON + TXT + Redis)"""
        try:
            # Save JSON
            json_filename = self.config_data.get('output', {}).get('json_filename', '{session_id}_world_bible.json').format(session_id=self.session_id)
            json_path = self.output_dir / json_filename
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved JSON: {json_path}")

            # Save TXT
            readable_filename = self.config_data.get('output', {}).get('readable_filename', '{session_id}_readable.txt').format(session_id=self.session_id)
            txt_path = self.output_dir / readable_filename
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(report['World Bible Document']['readable_summary'])
            print(f"✅ Saved TXT: {txt_path}")

            # Save to Redis
            redis_key = f"audiobook:{self.session_id}:station_08"
            await self.redis_client.set(redis_key, json.dumps(report), expire=86400)
            print(f"✅ Saved to Redis: {redis_key}")

        except Exception as e:
            raise ValueError(f"❌ Error saving outputs: {str(e)}")


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station08WorldBuilder(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
