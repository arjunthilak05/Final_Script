"""
Station 9: World Building System

This station creates a comprehensive, audio-optimized world architecture through
5 sequential tasks that build upon each other and previous station outputs.

Flow:
1. Load dependencies (Stations 2, 6, 8)
2. Task 1: Generate Geography & Spaces (5-10 locations with sonic signatures)
3. Task 2: Generate Social Systems (with audio manifestations)
4. Task 3: Generate Technology/Magic Systems (with sound profiles)
5. Task 4: Generate History & Lore (with audio integration)
6. Task 5: Generate Sensory Palette (150+ audio cues library)
7. Optional Human Review
8. Save outputs (JSON + TXT + CSV + Audio Cue Reference)

Critical World Building System - Creates production-ready audio cue library
"""

import asyncio
import json
import csv
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


class Station09WorldBuildingSystem:
    """Station 9: World Building System"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review  # For testing/automation
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=9)

        # Load additional config from YAML directly
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_09'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store intermediate results
        self.task_results = {}
        self.extracted_inputs = {}

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_9.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🎬 STATION 9: WORLD BUILDING SYSTEM")
        print("=" * 70)
        print()

        try:
            # Step 1: Load dependencies
            print("📥 Loading previous station data...")
            await self.load_dependencies()
            print("✅ All dependencies loaded successfully")
            print()

            # Step 2: Display context summary
            self.display_context_summary()

            # Step 3: Execute 5 tasks sequentially
            print("=" * 70)
            print("🎯 EXECUTING WORLD BUILDING SYSTEM (5 TASKS)")
            print("=" * 70)
            print()

            # Task 1: Geography & Spaces
            await self.execute_task_1_geography()

            # Task 2: Social Systems
            await self.execute_task_2_social_systems()

            # Task 3: Technology/Magic
            await self.execute_task_3_technology()

            # Task 4: History & Lore
            await self.execute_task_4_history()

            # Task 5: Sensory Palette
            await self.execute_task_5_sensory_palette()

            # Step 4: Optional Human Review
            await self.optional_human_review()

            # Step 5: Generate outputs
            print()
            print("=" * 70)
            print("💾 GENERATING OUTPUT FILES")
            print("=" * 70)
            print()

            await self.generate_outputs()

            # Step 6: Display completion
            self.display_completion()

        except Exception as e:
            print(f"❌ Station 9 failed: {str(e)}")
            logging.error(f"Station 9 error: {str(e)}", exc_info=True)
            raise

    async def load_dependencies(self):
        """Load data from Stations 2, 6, and 8"""
        try:
            # Load Station 2: Project Bible
            project_bible_path = Path(
                self.config_data.get('input', {}).get('project_bible_path',
                'output/station_02/{session_id}_bible.json').format(session_id=self.session_id)
            )
            if not project_bible_path.exists():
                raise ValueError(f"❌ Project Bible not found: {project_bible_path}")

            with open(project_bible_path, 'r', encoding='utf-8') as f:
                self.project_bible = json.load(f)
            print(f"   ✓ Station 2: Project Bible loaded")

            # Load Station 6: Master Style Guide (optional - may not exist yet)
            style_guide_path = Path(
                self.config_data.get('input', {}).get('style_guide_path',
                'output/station_06/{session_id}_master_style_guide.json').format(session_id=self.session_id)
            )
            if style_guide_path.exists():
                with open(style_guide_path, 'r', encoding='utf-8') as f:
                    self.style_guide = json.load(f)
                print(f"   ✓ Station 6: Master Style Guide loaded")
            else:
                self.style_guide = None
                print(f"   ⚠️  Station 6: Master Style Guide not found (optional)")

            # Load Station 8: World Builder
            world_bible_path = Path(
                self.config_data.get('input', {}).get('world_bible_path',
                'output/station_08/{session_id}_world_bible.json').format(session_id=self.session_id)
            )
            if not world_bible_path.exists():
                raise ValueError(f"❌ World Bible not found: {world_bible_path}")

            with open(world_bible_path, 'r', encoding='utf-8') as f:
                self.world_bible = json.load(f)
            print(f"   ✓ Station 8: World Builder loaded")

            # Load Redis data for additional context
            await self.load_redis_data()

        except Exception as e:
            raise ValueError(f"❌ Error loading dependencies: {str(e)}")

    async def load_redis_data(self):
        """Load data from Redis for additional context"""
        try:
            # Station 1 data
            station1_key = f"audiobook:{self.session_id}:station_01"
            station1_raw = await self.redis_client.get(station1_key)
            if station1_raw:
                self.station1_data = json.loads(station1_raw)
            else:
                self.station1_data = {}

            # Station 2 data
            station2_key = f"audiobook:{self.session_id}:station_02"
            station2_raw = await self.redis_client.get(station2_key)
            if station2_raw:
                self.station2_data = json.loads(station2_raw)
            else:
                self.station2_data = {}

            # Station 3 data
            station3_key = f"audiobook:{self.session_id}:station_03"
            station3_raw = await self.redis_client.get(station3_key)
            if station3_raw:
                self.station3_data = json.loads(station3_raw)
            else:
                self.station3_data = {}

            # Extract key inputs
            self.extracted_inputs = self.extract_key_inputs()

        except Exception as e:
            logging.warning(f"Could not load Redis data: {str(e)}")
            self.station1_data = {}
            self.station2_data = {}
            self.station3_data = {}
            self.extracted_inputs = {}

    def extract_key_inputs(self) -> Dict:
        """Extract key inputs from loaded data"""
        try:
            inputs = {}

            # From Station 1
            station1_options = self.station1_data.get('option_details', {})
            inputs['episode_count'] = station1_options.get('episode_count', 'Unknown')
            inputs['episode_length'] = station1_options.get('episode_length', 'Unknown')

            # From Station 2 (Project Bible)
            inputs['working_title'] = TitleValidator.extract_bulletproof_title(
                self.station1_data, self.station2_data
            )

            project_bible_doc = self.project_bible
            world_setting = project_bible_doc.get('world_setting', {})
            genre_tone = project_bible_doc.get('genre_tone', {})

            inputs['core_premise'] = world_setting.get('core_premise',
                world_setting.get('primary_location', 'Unknown'))
            inputs['time_period'] = world_setting.get('time_period', 'Contemporary')
            inputs['setting_type'] = world_setting.get('setting_type', 'Realistic Contemporary')
            inputs['atmosphere'] = world_setting.get('atmosphere', 'Unknown')

            # From Station 3 (for genre - more reliable than Project Bible)
            chosen_blend = self.station3_data.get('chosen_blend_details', {})
            age_guidelines = self.station3_data.get('age_guidelines', {})
            tone_calibration = self.station3_data.get('tone_calibration', {})

            # Get primary genre from Station 3 first, fallback to Project Bible
            inputs['primary_genre'] = chosen_blend.get('primary_genre',
                genre_tone.get('primary_genre', 'Drama'))
            inputs['tone_descriptors'] = genre_tone.get('tone_descriptors', [])
            inputs['target_age'] = age_guidelines.get('target_age_range', '25-45')
            inputs['tone'] = tone_calibration.get('light_dark_balance', 'Balanced')

            # From World Bible (Station 8)
            world_bible_doc = self.world_bible.get('World Bible Document', {})
            inputs['world_bible_data'] = world_bible_doc.get('world_bible', {})

            return inputs

        except Exception as e:
            logging.error(f"Error extracting inputs: {str(e)}")
            return {
                'working_title': 'Unknown',
                'core_premise': 'Unknown',
                'primary_genre': 'Unknown',
                'target_age': '25-45',
                'tone': 'Balanced'
            }

    def display_context_summary(self):
        """Display project context summary"""
        print("-" * 70)
        print("📊 WORLD BUILDING CONTEXT")
        print("-" * 70)
        print(f"Title: {self.extracted_inputs.get('working_title', 'N/A')}")
        print(f"Genre: {self.extracted_inputs.get('primary_genre', 'N/A')}")
        print(f"Setting Type: {self.extracted_inputs.get('setting_type', 'N/A')}")
        print(f"Time Period: {self.extracted_inputs.get('time_period', 'N/A')}")
        print(f"Atmosphere: {self.extracted_inputs.get('atmosphere', 'N/A')}")
        print()
        print(f"Core Premise: {self.extracted_inputs.get('core_premise', 'N/A')}")
        print()
        print(f"Audio Requirements:")
        tone_desc = ', '.join(self.extracted_inputs.get('tone_descriptors', ['Unknown']))
        print(f"  - Tone: {tone_desc}")
        print(f"  - Target Age: {self.extracted_inputs.get('target_age', 'N/A')}")
        print("-" * 70)
        print()
        print("🎯 Building audio-optimized world architecture...")
        print()

    async def execute_task_1_geography(self):
        """Task 1: Generate Geography & Spaces"""
        print("=" * 70)
        print("🗺️  TASK 1: GEOGRAPHY & SPACES")
        print("=" * 70)
        print()
        print("🤖 Generating key locations with sonic signatures...")
        print("   Analyzing story requirements from Project Bible...")
        print("   Creating 5-10 distinct audio environments...")
        print("   Mapping travel times and transitions...")
        print()

        try:
            # Build prompt
            prompt = self.config.get_prompt('task_1_geography')

            # Prepare context
            world_foundation = self._create_world_foundation_summary()
            project_bible_context = self._create_project_bible_context()

            # Format prompt
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Unknown'),
                core_premise=self.extracted_inputs.get('core_premise', 'Unknown'),
                target_age=self.extracted_inputs.get('target_age', 'Unknown'),
                tone=self.extracted_inputs.get('tone', 'Balanced'),
                world_foundation=world_foundation,
                project_bible_context=project_bible_context
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            geography_data = extract_json(response)

            # Store result
            self.task_results['task_1_geography'] = geography_data.get('geography_spaces', {})

            # Display summary
            locations = self.task_results['task_1_geography'].get('key_locations', [])
            location_count = len(locations)

            print(f"✅ Generated {location_count} key locations with audio profiles")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

        except Exception as e:
            print(f"❌ Task 1 failed: {str(e)}")
            raise

    async def execute_task_2_social_systems(self):
        """Task 2: Generate Social Systems"""
        print("=" * 70)
        print("⚖️  TASK 2: SOCIAL SYSTEMS")
        print("=" * 70)
        print()
        print("🤖 Generating social structure and power dynamics...")
        print("   Analyzing authority systems...")
        print("   Creating economic structures...")
        print("   Defining cultural norms...")
        print("   Mapping dialogue sound patterns...")
        print()

        try:
            # Build prompt
            prompt = self.config.get_prompt('task_2_social_systems')

            # Prepare context
            generated_locations = json.dumps(
                self.task_results['task_1_geography'].get('key_locations', [])[:3],  # First 3 for context
                indent=2
            )

            # Format prompt
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Unknown'),
                core_premise=self.extracted_inputs.get('core_premise', 'Unknown'),
                world_type=self.extracted_inputs.get('setting_type', 'Unknown'),
                generated_locations=generated_locations
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            social_data = extract_json(response)

            # Store result
            self.task_results['task_2_social_systems'] = social_data.get('social_systems', {})

            print(f"✅ Social systems generated with audio implications")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

        except Exception as e:
            print(f"❌ Task 2 failed: {str(e)}")
            raise

    async def execute_task_3_technology(self):
        """Task 3: Generate Technology/Magic Systems"""
        print("=" * 70)
        print("🔧 TASK 3: TECHNOLOGY/MAGIC SYSTEMS")
        print("=" * 70)
        print()
        print("🤖 Generating technology systems and audio profiles...")
        print("   (Note: Adapts to setting - contemporary/fantasy/sci-fi)")
        print("   Cataloging available technology...")
        print("   Creating sound signatures for each tech...")
        print("   Defining limitations and audio cues...")
        print()

        try:
            # Build prompt
            prompt = self.config.get_prompt('task_3_technology')

            # Prepare context
            social_summary = self._create_social_systems_summary()

            # Format prompt
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Drama'),
                setting_type=self.extracted_inputs.get('setting_type', 'Unknown'),
                time_period=self.extracted_inputs.get('time_period', 'Unknown'),
                core_premise=self.extracted_inputs.get('core_premise', 'Unknown'),
                social_systems_summary=social_summary
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            tech_data = extract_json(response)

            # Store result
            self.task_results['task_3_technology'] = tech_data.get('technology_magic_systems', {})

            systems = self.task_results['task_3_technology'].get('available_systems', [])
            system_count = len(systems)

            print(f"✅ Technology systems with complete audio library")
            print(f"   Generated {system_count} technology/magic systems")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

        except Exception as e:
            print(f"❌ Task 3 failed: {str(e)}")
            raise

    async def execute_task_4_history(self):
        """Task 4: Generate History & Lore"""
        print("=" * 70)
        print("📜 TASK 4: HISTORY & LORE")
        print("=" * 70)
        print()
        print("🤖 Generating historical timeline and mythology...")
        print("   Creating key past events...")
        print("   Establishing common knowledge vs secrets...")
        print("   Mapping how history affects present...")
        print("   Building departmental legends...")
        print()

        try:
            # Build prompt
            prompt = self.config.get_prompt('task_4_history')

            # Prepare context
            world_summary = self._create_world_elements_summary()

            # Format prompt
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Drama'),
                setting_type=self.extracted_inputs.get('setting_type', 'Unknown'),
                time_period=self.extracted_inputs.get('time_period', 'Unknown'),
                core_premise=self.extracted_inputs.get('core_premise', 'Unknown'),
                world_type=self.extracted_inputs.get('setting_type', 'Unknown'),
                world_elements_summary=world_summary
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            history_data = extract_json(response)

            # Store result
            self.task_results['task_4_history'] = history_data.get('history_lore', {})

            timeline = self.task_results['task_4_history'].get('timeline', [])
            myths = self.task_results['task_4_history'].get('myths_legends', [])

            print(f"✅ Complete historical framework with audio integration")
            print(f"   Generated {len(timeline)} historical events")
            print(f"   Created {len(myths)} myths/legends")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

        except Exception as e:
            print(f"❌ Task 4 failed: {str(e)}")
            raise

    async def execute_task_5_sensory_palette(self):
        """Task 5: Generate Sensory Palette (Complete Audio Cue Library)"""
        print("=" * 70)
        print("🎨 TASK 5: SENSORY PALETTE (AUDIO CUE LIBRARY)")
        print("=" * 70)
        print()
        print("🤖 Creating comprehensive audio cue library...")
        print("   Generating ambient sounds per location...")
        print("   Cataloging distinctive noises...")
        print("   Mapping acoustic properties...")
        print("   Building recurring audio elements...")
        print("   Creating audio emotion map...")
        print()

        try:
            # Build prompt
            prompt = self.config.get_prompt('task_5_sensory_palette')

            # Prepare complete world summary
            complete_summary = self._create_complete_world_summary()

            # Format prompt
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Unknown'),
                complete_world_summary=complete_summary
            )

            # Execute LLM call with retry logic for connection issues
            start_time = datetime.now()
            max_retries = 3
            retry_delay = 5  # seconds

            for attempt in range(max_retries):
                try:
                    response = await self.agent.process_message(
                        formatted_prompt,
                        model_name=self.config.model,
                        max_tokens=16384  # Maximum for comprehensive library
                    )
                    break  # Success, exit retry loop

                except Exception as e:
                    error_msg = str(e)
                    if "peer closed connection" in error_msg or "incomplete chunked read" in error_msg:
                        if attempt < max_retries - 1:
                            print(f"   ⚠️ Connection error (attempt {attempt + 1}/{max_retries})")
                            print(f"   Retrying in {retry_delay} seconds...")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                            continue
                        else:
                            print(f"   ❌ Connection failed after {max_retries} attempts")
                            raise
                    else:
                        # Different error, don't retry
                        raise

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            sensory_data = extract_json(response)

            # Store result
            self.task_results['task_5_sensory'] = sensory_data.get('sensory_palette', {})

            # Count elements
            sfx_library = self.task_results['task_5_sensory'].get('complete_sound_effects_library', [])
            locations = self.task_results['task_5_sensory'].get('location_ambient_profiles', [])
            characters = self.task_results['task_5_sensory'].get('character_sound_signatures', [])
            recurring = self.task_results['task_5_sensory'].get('recurring_series_identity_sounds', [])

            total_sounds = len(sfx_library)

            print(f"✅ Complete Audio Cue Library generated ({total_sounds}+ unique sounds)")
            print(f"   Location Profiles: {len(locations)}")
            print(f"   Character Signatures: {len(characters)}")
            print(f"   Recurring Elements: {len(recurring)}")
            print(f"   SFX Library: {total_sounds} cataloged sounds")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

        except Exception as e:
            print(f"❌ Task 5 failed: {str(e)}")
            raise

    async def optional_human_review(self):
        """Optional human review of generated world bible"""
        print("=" * 70)
        print("🎯 WORLD BIBLE REVIEW")
        print("=" * 70)
        print()
        print("The World Bible is complete with 5 major sections:")
        print(f"  ✓ Geography & Spaces ({len(self.task_results.get('task_1_geography', {}).get('key_locations', []))} locations)")
        print("  ✓ Social Systems (authority, economy, culture)")
        print(f"  ✓ Technology Systems ({len(self.task_results.get('task_3_technology', {}).get('available_systems', []))} systems)")
        print(f"  ✓ History & Lore ({len(self.task_results.get('task_4_history', {}).get('timeline', []))} events)")
        sfx_count = len(self.task_results.get('task_5_sensory', {}).get('complete_sound_effects_library', []))
        print(f"  ✓ Sensory Palette ({sfx_count}+ audio cues)")
        print()

        # Skip review if requested (for automation/testing)
        if self.skip_review:
            print("✅ Auto-accepting World Bible (skip_review=True)")
            print()
            return

        print("Options:")
        print("  [Press Enter] Accept World Bible and save")
        print("  [Type 'V'] View different section in detail")
        print("  [Type 'R'] Regenerate specific section (which?)")
        print("  [Type 'L'] View full audio cue list")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == '':
            print("✅ World Bible accepted. Saving files...")
            print()
        elif choice == 'V':
            # View section detail
            print("\nAvailable sections:")
            print("  1. Geography & Spaces")
            print("  2. Social Systems")
            print("  3. Technology/Magic")
            print("  4. History & Lore")
            print("  5. Sensory Palette")
            section = input("Enter section number (1-5): ").strip()

            if section == '1':
                print(json.dumps(self.task_results.get('task_1_geography', {}), indent=2))
            elif section == '2':
                print(json.dumps(self.task_results.get('task_2_social_systems', {}), indent=2))
            elif section == '3':
                print(json.dumps(self.task_results.get('task_3_technology', {}), indent=2))
            elif section == '4':
                print(json.dumps(self.task_results.get('task_4_history', {}), indent=2))
            elif section == '5':
                print(json.dumps(self.task_results.get('task_5_sensory', {}), indent=2))

            input("\nPress Enter to continue...")

        elif choice == 'L':
            # View audio cue list
            sfx_library = self.task_results.get('task_5_sensory', {}).get('complete_sound_effects_library', [])
            print(f"\n🎵 COMPLETE AUDIO CUE LIBRARY ({len(sfx_library)} sounds)")
            print("=" * 70)
            for i, sfx in enumerate(sfx_library[:20], 1):  # Show first 20
                print(f"{i}. {sfx.get('sound_name', 'Unnamed')} - {sfx.get('category', 'N/A')}")
            if len(sfx_library) > 20:
                print(f"... and {len(sfx_library) - 20} more sounds")
            input("\nPress Enter to continue...")

    async def generate_outputs(self):
        """Generate all output files"""
        try:
            # Compile final data structure
            final_data = {
                "World Building System": {
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "project_info": {
                        "working_title": self.extracted_inputs.get('working_title', 'Unknown'),
                        "primary_genre": self.extracted_inputs.get('primary_genre', 'Unknown'),
                        "setting_type": self.extracted_inputs.get('setting_type', 'Unknown'),
                        "time_period": self.extracted_inputs.get('time_period', 'Unknown'),
                        "core_premise": self.extracted_inputs.get('core_premise', 'Unknown')
                    },
                    "geography_spaces": self.task_results.get('task_1_geography', {}),
                    "social_systems": self.task_results.get('task_2_social_systems', {}),
                    "technology_magic": self.task_results.get('task_3_technology', {}),
                    "history_lore": self.task_results.get('task_4_history', {}),
                    "sensory_palette": self.task_results.get('task_5_sensory', {})
                }
            }

            # 1. Save JSON
            json_filename = self.config_data.get('output', {}).get('json_filename',
                '{session_id}_world_building_system.json').format(session_id=self.session_id)
            json_path = self.output_dir / json_filename

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved JSON: {json_path}")

            # 2. Save Readable TXT
            readable_filename = self.config_data.get('output', {}).get('readable_filename',
                '{session_id}_world_building_readable.txt').format(session_id=self.session_id)
            txt_path = self.output_dir / readable_filename

            readable_content = self.generate_readable_summary(final_data)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(readable_content)
            print(f"✅ Saved TXT: {txt_path}")

            # 3. Save Audio Cues CSV
            csv_filename = self.config_data.get('output', {}).get('audio_cues_csv',
                '{session_id}_audio_cues.csv').format(session_id=self.session_id)
            csv_path = self.output_dir / csv_filename

            self.generate_audio_cues_csv(csv_path)
            print(f"✅ Saved CSV: {csv_path}")

            # 4. Save Audio Cue Reference
            ref_filename = self.config_data.get('output', {}).get('cue_reference',
                '{session_id}_audio_cue_reference.txt').format(session_id=self.session_id)
            ref_path = self.output_dir / ref_filename

            ref_content = self.generate_audio_cue_reference()
            with open(ref_path, 'w', encoding='utf-8') as f:
                f.write(ref_content)
            print(f"✅ Saved Audio Cue Reference: {ref_path}")

            # 5. Save to Redis
            redis_key = f"audiobook:{self.session_id}:station_09"
            await self.redis_client.set(redis_key, json.dumps(final_data), expire=86400)
            print(f"✅ Saved to Redis: {redis_key}")

        except Exception as e:
            raise ValueError(f"❌ Error generating outputs: {str(e)}")

    def generate_readable_summary(self, data: Dict) -> str:
        """Generate human-readable summary"""
        lines = []

        doc = data.get('World Building System', {})

        # Header
        lines.append("=" * 70)
        lines.append("STATION 9: WORLD BUILDING SYSTEM")
        lines.append("=" * 70)
        lines.append("")

        # Project Info
        proj_info = doc.get('project_info', {})
        lines.append(f"Working Title: {proj_info.get('working_title', 'N/A')}")
        lines.append(f"Primary Genre: {proj_info.get('primary_genre', 'N/A')}")
        lines.append(f"Setting Type: {proj_info.get('setting_type', 'N/A')}")
        lines.append(f"Time Period: {proj_info.get('time_period', 'N/A')}")
        lines.append(f"Core Premise: {proj_info.get('core_premise', 'N/A')}")
        lines.append("")

        # Geography & Spaces
        geography = doc.get('geography_spaces', {})
        if geography:
            lines.append("-" * 70)
            lines.append("📍 GEOGRAPHY & SPACES")
            lines.append("-" * 70)
            lines.append("")

            for i, loc in enumerate(geography.get('key_locations', []), 1):
                lines.append(f"LOCATION {i}: {loc.get('name', 'Unknown')}")
                lines.append(f"Description: {loc.get('description', 'N/A')}")

                sonic = loc.get('sonic_signature', {})
                if sonic:
                    lines.append("Sonic Signature:")
                    for layer, sound in sonic.items():
                        lines.append(f"  • {layer}: {sound}")

                lines.append(f"Acoustic Properties: {loc.get('acoustic_properties', {})}")
                lines.append(f"Weather Impact: {loc.get('weather_impact', 'N/A')}")
                lines.append(f"Emotional Tone: {loc.get('emotional_tone', 'N/A')}")
                lines.append("")

        # Social Systems
        social = doc.get('social_systems', {})
        if social:
            lines.append("-" * 70)
            lines.append("⚖️  SOCIAL SYSTEMS")
            lines.append("-" * 70)
            lines.append("")

            gov = social.get('government_authority', {})
            if gov:
                lines.append(f"Government: {gov.get('structure', 'N/A')}")
                lines.append(f"Audio Manifestations: {gov.get('audio_manifestations', [])}")
                lines.append("")

            econ = social.get('economic_structure', {})
            if econ:
                lines.append(f"Economy: {econ.get('description', 'N/A')}")
                lines.append("")

        # Technology/Magic
        tech = doc.get('technology_magic', {})
        if tech:
            lines.append("-" * 70)
            lines.append("🔧 TECHNOLOGY/MAGIC SYSTEMS")
            lines.append("-" * 70)
            lines.append("")

            for i, system in enumerate(tech.get('available_systems', []), 1):
                lines.append(f"{i}. {system.get('name', 'Unknown')} ({system.get('type', 'N/A')})")
                lines.append(f"   How It Works: {system.get('how_it_works', 'N/A')}")
                lines.append(f"   Sound Signature: {system.get('sound_signature', {})}")
                lines.append(f"   Prevalence: {system.get('prevalence', 'N/A')}")
                lines.append("")

        # History & Lore
        history = doc.get('history_lore', {})
        if history:
            lines.append("-" * 70)
            lines.append("📜 HISTORY & LORE")
            lines.append("-" * 70)
            lines.append("")

            for i, event in enumerate(history.get('timeline', []), 1):
                lines.append(f"{i}. {event.get('event_name', 'Unknown')} ({event.get('time_period', 'N/A')})")
                lines.append(f"   What Happened: {event.get('what_happened', 'N/A')}")
                lines.append(f"   Audio Manifestations: {event.get('audio_manifestations', {})}")
                lines.append("")

        # Sensory Palette Summary
        sensory = doc.get('sensory_palette', {})
        if sensory:
            lines.append("-" * 70)
            lines.append("🎵 SENSORY PALETTE (AUDIO CUE LIBRARY)")
            lines.append("-" * 70)
            lines.append("")

            sfx = sensory.get('complete_sound_effects_library', [])
            lines.append(f"Total Sound Effects: {len(sfx)}")
            lines.append(f"Location Profiles: {len(sensory.get('location_ambient_profiles', []))}")
            lines.append(f"Character Signatures: {len(sensory.get('character_sound_signatures', []))}")
            lines.append(f"Recurring Elements: {len(sensory.get('recurring_series_identity_sounds', []))}")
            lines.append("")
            lines.append("See audio_cues.csv for complete sound library")
            lines.append("")

        lines.append("=" * 70)
        lines.append("END OF WORLD BUILDING SYSTEM")
        lines.append("=" * 70)

        return "\n".join(lines)

    def generate_audio_cues_csv(self, csv_path: Path):
        """Generate CSV file with all audio cues"""
        sensory = self.task_results.get('task_5_sensory', {})
        sfx_library = sensory.get('complete_sound_effects_library', [])

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'SFX_ID', 'Category', 'Sound_Name', 'Description',
                'Location_Context', 'Frequency_Content', 'Dynamic_Range',
                'Reverb_Characteristics', 'Emotional_Association',
                'Story_Function', 'Production_Notes'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for sfx in sfx_library:
                writer.writerow({
                    'SFX_ID': sfx.get('sfx_id', 'N/A'),
                    'Category': sfx.get('category', 'N/A'),
                    'Sound_Name': sfx.get('sound_name', 'N/A'),
                    'Description': sfx.get('description', 'N/A'),
                    'Location_Context': sfx.get('location_context', 'N/A'),
                    'Frequency_Content': sfx.get('frequency_content', 'N/A'),
                    'Dynamic_Range': sfx.get('dynamic_range', 'N/A'),
                    'Reverb_Characteristics': sfx.get('reverb_characteristics', 'N/A'),
                    'Emotional_Association': sfx.get('emotional_association', 'N/A'),
                    'Story_Function': sfx.get('story_function', 'N/A'),
                    'Production_Notes': sfx.get('production_notes', 'N/A')
                })

    def generate_audio_cue_reference(self) -> str:
        """Generate quick reference sheet for audio cues"""
        lines = []

        lines.append("=" * 70)
        lines.append("AUDIO CUE QUICK REFERENCE")
        lines.append("=" * 70)
        lines.append("")

        sensory = self.task_results.get('task_5_sensory', {})

        # Location Ambient Profiles
        locations = sensory.get('location_ambient_profiles', [])
        if locations:
            lines.append("LOCATION AMBIENT PROFILES:")
            lines.append("-" * 70)
            for loc in locations:
                lines.append(f"\n{loc.get('location_name', 'Unknown')}:")
                layers = loc.get('ambient_layers', {})
                for layer, sound in layers.items():
                    lines.append(f"  • {layer}: {sound}")
            lines.append("")

        # Character Sound Signatures
        characters = sensory.get('character_sound_signatures', [])
        if characters:
            lines.append("CHARACTER SOUND SIGNATURES:")
            lines.append("-" * 70)
            for char in characters:
                lines.append(f"\n{char.get('character_name', 'Unknown')}:")
                lines.append(f"  Signature: {char.get('signature_sound', 'N/A')}")
                distinctive = char.get('distinctive_sounds', [])
                for sound in distinctive:
                    lines.append(f"  • {sound}")
            lines.append("")

        # Recurring Series Identity Sounds
        recurring = sensory.get('recurring_series_identity_sounds', [])
        if recurring:
            lines.append("RECURRING SERIES IDENTITY SOUNDS:")
            lines.append("-" * 70)
            for sound in recurring:
                lines.append(f"\n{sound.get('sound_name', 'Unknown')}:")
                lines.append(f"  Purpose: {sound.get('purpose', 'N/A')}")
                lines.append(f"  Frequency: {sound.get('frequency', 'N/A')}")
                variations = sound.get('variations', [])
                for var in variations:
                    lines.append(f"  • {var}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def display_completion(self):
        """Display completion message"""
        print()
        print("=" * 70)
        print("✅ STATION 9 COMPLETE!")
        print("=" * 70)
        print()
        print(f"Project: {self.extracted_inputs.get('working_title', 'Unknown')}")
        print(f"Session ID: {self.session_id}")
        print()

        # Statistics
        geography = self.task_results.get('task_1_geography', {})
        social = self.task_results.get('task_2_social_systems', {})
        tech = self.task_results.get('task_3_technology', {})
        history = self.task_results.get('task_4_history', {})
        sensory = self.task_results.get('task_5_sensory', {})

        location_count = len(geography.get('key_locations', []))
        tech_count = len(tech.get('available_systems', []))
        event_count = len(history.get('timeline', []))
        myth_count = len(history.get('myths_legends', []))
        sfx_count = len(sensory.get('complete_sound_effects_library', []))

        print("📊 WORLD BIBLE STATISTICS:")
        print(f"   • {location_count} Key Locations with sonic signatures")
        print("   • 4 Social Systems with audio manifestations")
        print(f"   • {tech_count} Technology systems with sound profiles")
        print(f"   • {event_count} Historical events with audio integration")
        print(f"   • {myth_count} Myths/legends with sonic themes")
        print(f"   • {sfx_count}+ Audio cues cataloged and tagged")
        print()

        print("📁 OUTPUT FILES:")
        print(f"   ✓ World Bible JSON (for production pipeline)")
        print(f"   ✓ Readable World Guide (for writers/directors)")
        print(f"   ✓ Audio Cue Library CSV (for sound designers)")
        print(f"   ✓ Quick Reference Sheet (for recording sessions)")
        print()

        print("🎵 AUDIO LIBRARY INCLUDES:")
        print("   • Location ambient profiles")
        print("   • Character sound signatures")
        print("   • Recurring series identity sounds")
        print("   • Emotional audio mapping")
        print("   • Acoustic property templates")
        print()

        print("📌 Ready to proceed to Station 10")
        print()

    # Helper methods for building context summaries

    def _create_world_foundation_summary(self) -> str:
        """Create summary of world foundation from Station 8"""
        world_bible = self.extracted_inputs.get('world_bible_data', {})

        geography = world_bible.get('Geography_Spaces', {})
        tech = world_bible.get('Technology_Magic', {})

        parts = []
        parts.append(f"Setting Type: {self.extracted_inputs.get('setting_type', 'Unknown')}")
        parts.append(f"Time Period: {self.extracted_inputs.get('time_period', 'Unknown')}")
        parts.append(f"Atmosphere: {self.extracted_inputs.get('atmosphere', 'Unknown')}")

        if geography:
            key_locs = geography.get('key_locations', [])
            if key_locs:
                loc_names = [loc.get('name', 'Unknown') for loc in key_locs[:5]]
                parts.append(f"Foundation Locations: {', '.join(loc_names)}")

        if tech:
            parts.append(f"Technology Level: {tech.get('overview', 'Standard')}")

        return "\n".join(parts)

    def _create_project_bible_context(self) -> str:
        """Create summary of Project Bible"""
        world_setting = self.project_bible.get('world_setting', {})

        parts = []
        parts.append(f"Core Premise: {world_setting.get('core_premise', 'Unknown')}")
        parts.append(f"Primary Location: {world_setting.get('primary_location', 'Unknown')}")

        key_locations = world_setting.get('key_locations', [])
        if key_locations:
            parts.append(f"Key Locations: {', '.join(key_locations[:5])}")

        cultural_elements = world_setting.get('cultural_elements', [])
        if cultural_elements:
            parts.append(f"Cultural Elements: {', '.join(cultural_elements[:3])}")

        return "\n".join(parts)

    def _create_social_systems_summary(self) -> str:
        """Create summary of generated social systems"""
        social = self.task_results.get('task_2_social_systems', {})

        parts = []

        gov = social.get('government_authority', {})
        if gov:
            parts.append(f"Government: {gov.get('structure', 'Unknown')}")

        econ = social.get('economic_structure', {})
        if econ:
            parts.append(f"Economy: {econ.get('description', 'Unknown')}")

        return "\n".join(parts) if parts else "Social systems being developed"

    def _create_world_elements_summary(self) -> str:
        """Create summary of all world elements generated so far"""
        parts = []

        # Geography
        geography = self.task_results.get('task_1_geography', {})
        locations = geography.get('key_locations', [])
        if locations:
            loc_names = [loc.get('name', 'Unknown') for loc in locations]
            parts.append(f"Key Locations: {', '.join(loc_names)}")

        # Social Systems
        social = self.task_results.get('task_2_social_systems', {})
        if social:
            parts.append(f"Social Structure: {social.get('government_authority', {}).get('structure', 'Established')}")

        # Technology
        tech = self.task_results.get('task_3_technology', {})
        systems = tech.get('available_systems', [])
        if systems:
            tech_names = [s.get('name', 'Unknown') for s in systems]
            parts.append(f"Technology: {', '.join(tech_names[:5])}")

        return "\n".join(parts)

    def _create_complete_world_summary(self) -> str:
        """Create complete summary of all 4 tasks for Task 5"""
        parts = []

        # Task 1: Geography
        geography = self.task_results.get('task_1_geography', {})
        locations = geography.get('key_locations', [])
        parts.append(f"GEOGRAPHY: {len(locations)} key locations")
        for loc in locations[:3]:  # First 3 as examples
            parts.append(f"  - {loc.get('name', 'Unknown')}: {loc.get('description', '')[:100]}...")

        # Task 2: Social
        social = self.task_results.get('task_2_social_systems', {})
        parts.append(f"\nSOCIAL SYSTEMS:")
        parts.append(f"  - Government: {social.get('government_authority', {}).get('structure', 'N/A')}")
        parts.append(f"  - Economy: {social.get('economic_structure', {}).get('description', 'N/A')[:80]}...")

        # Task 3: Technology
        tech = self.task_results.get('task_3_technology', {})
        systems = tech.get('available_systems', [])
        parts.append(f"\nTECHNOLOGY: {len(systems)} systems")
        for sys in systems[:3]:
            parts.append(f"  - {sys.get('name', 'Unknown')}: {sys.get('how_it_works', '')[:80]}...")

        # Task 4: History
        history = self.task_results.get('task_4_history', {})
        timeline = history.get('timeline', [])
        myths = history.get('myths_legends', [])
        parts.append(f"\nHISTORY: {len(timeline)} events, {len(myths)} myths")

        return "\n".join(parts)


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    # Auto-skip review when running from command line with no TTY
    import sys
    skip_review = not sys.stdin.isatty()

    station = Station09WorldBuildingSystem(session_id, skip_review=skip_review)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
