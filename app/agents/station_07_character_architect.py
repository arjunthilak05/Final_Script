"""
Station 7: Character Architect

This station functions as a Character Architect for audio drama production.
It creates detailed character profiles across three tiers with special emphasis 
on audio identification markers for audio-only format.

Flow:
1. Load Project Bible from Station 2
2. Extract required inputs from previous stations
3. Execute character architecture analysis:
   - Tier 1: Protagonists (1-3) - Full psychological profiles, voice signatures, complete character arcs
   - Tier 2: Major Supporting (3-5) - Relevant backstory, distinct voice, episode-specific arc
   - Tier 3: Recurring (5-10) - Single defining trait, memorable voice hook, narrative purpose
4. Save comprehensive Character Bible document

Critical Character Development Agent - Output guides all character-related creative decisions
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


class Station07CharacterArchitect:
    """Station 7: Character Architect"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=7)
        # Load additional config from YAML directly
        self._load_additional_config()
        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_07'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path
        
        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_7.yml'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("👥 STATION 7: CHARACTER ARCHITECT")
        print("=" * 60)
        print()

        try:
            # Load Project Bible from Station 2
            project_bible_data = await self.load_project_bible()
            
            # Load Master Style Guide from Station 6
            master_style_guide_data = await self.load_master_style_guide()
            
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
            print(f"Narrator Strategy: {extracted_inputs.get('narrator_strategy', 'N/A')}")
            print(f"Main Characters: {', '.join(extracted_inputs.get('main_characters', []))}")
            print("-" * 60)
            print()

            # Build the comprehensive LLM prompt
            print("👥 Building Character Architecture Prompt...")
            prompt = await self.build_character_architecture_prompt(extracted_inputs, project_bible_data, master_style_guide_data)
            print("✅ Prompt built successfully")
            print(f"📊 Prompt length: {len(prompt)} characters")
            print(f"📊 Estimated tokens: ~{len(prompt) // 4} tokens")
            print()

            # Execute the character architecture analysis
            print("=" * 60)
            print("🎯 EXECUTING CHARACTER ARCHITECTURE ANALYSIS")
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
            character_bible_data = extract_json(response)
            
            if not character_bible_data:
                raise ValueError("❌ Failed to extract valid JSON from LLM response")

            # Validate character counts
            await self.validate_character_counts(character_bible_data)

            # Generate human-readable summary
            print("📄 Generating human-readable summary...")
            readable_summary = await self.generate_readable_summary(character_bible_data, extracted_inputs)
            print("✅ Summary generated")
            print()

            # Compile final report
            final_report = await self.compile_final_report(
                extracted_inputs, character_bible_data, readable_summary
            )

            # Save outputs
            await self.save_outputs(final_report)

            print()
            print("=" * 60)
            print("✅ STATION 7 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Session ID: {self.session_id}")
            title = extracted_inputs.get('working_title', 'N/A')
            print(TitleValidator.format_title_for_display(title, "Station 7"))
            print()
            print("📄 Output files:")
            print(f"   - {self.output_dir}/{self.session_id}_character_bible.json")
            print(f"   - {self.output_dir}/{self.session_id}_readable.txt")
            print()
            print("👥 CHARACTER BIBLE COMPLETE")
            print("📌 Ready to proceed to Station 8")
            print()

        except Exception as e:
            print(f"❌ Station 7 failed: {str(e)}")
            logging.error(f"Station 7 error: {str(e)}")
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

    async def load_master_style_guide(self) -> Dict:
        """Load Master Style Guide from Station 6"""
        try:
            # Construct the path to the Master Style Guide
            style_guide_path = Path(self.config_data.get('input', {}).get('master_style_guide_path', 'output/station_06/{session_id}_output.json').format(session_id=self.session_id))
            
            if not style_guide_path.exists():
                raise ValueError(f"❌ Master Style Guide not found at {style_guide_path}\n   Please run Station 6 first to generate the Master Style Guide")
            
            # Load and parse the Master Style Guide
            with open(style_guide_path, 'r', encoding='utf-8') as f:
                master_style_guide_data = json.load(f)
            
            print(f"✅ Loaded Master Style Guide from {style_guide_path}")
            return master_style_guide_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Master Style Guide: {str(e)}")
        except FileNotFoundError:
            raise ValueError(f"❌ Master Style Guide file not found at {style_guide_path}\n   Please run Station 6 first")
        except Exception as e:
            raise ValueError(f"❌ Error loading Master Style Guide: {str(e)}")

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

            # Load Station 4.5 data for narrator strategy
            station45_key = f"audiobook:{self.session_id}:station_045"
            station45_raw = await self.redis_client.get(station45_key)
            if not station45_raw:
                raise ValueError(f"❌ No Station 4.5 data found for session {self.session_id}")
            station45_data = json.loads(station45_raw)

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

            # From Station 4.5
            narrator_recommendation = station45_data.get('Narrator Strategy Recommendation', {})
            definitive_rec = narrator_recommendation.get('definitive_recommendation', {})
            extracted['narrator_strategy'] = definitive_rec.get('recommendation', 'Unknown')

            return extracted

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing station data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error extracting required inputs: {str(e)}")

    async def build_character_architecture_prompt(self, inputs: Dict, project_bible_data: Dict, master_style_guide_data: Dict) -> str:
        """Build the comprehensive character architecture prompt"""
        try:
            # Get the base prompt from config
            base_prompt = self.config.get_prompt('character_architecture_analysis')
            
            # Create summaries to reduce prompt size
            project_bible_summary = self._create_project_bible_summary(project_bible_data)
            master_style_guide_summary = self._create_master_style_guide_summary(master_style_guide_data)
            
            # Format the prompt with project data
            formatted_prompt = base_prompt.format(
                working_title=inputs.get('working_title', 'Unknown'),
                primary_genre=inputs.get('primary_genre', 'Unknown'),
                target_age=inputs.get('target_age', 'Unknown'),
                episode_count=inputs.get('episode_count', 'Unknown'),
                episode_length=inputs.get('episode_length', 'Unknown'),
                story_complexity=inputs.get('story_complexity', 'Unknown'),
                tone=inputs.get('tone', 'Balanced'),
                narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
                core_premise=inputs.get('core_premise', 'Unknown'),
                main_characters=', '.join(inputs.get('main_characters', [])),
                project_bible_summary=project_bible_summary,
                master_style_guide_summary=master_style_guide_summary
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

    def _create_master_style_guide_summary(self, master_style_guide_data: Dict) -> str:
        """Create a concise summary of the Master Style Guide data"""
        try:
            # Extract key information from Master Style Guide
            style_guide_doc = master_style_guide_data.get('Master Style Guide Document', {})
            master_guide = style_guide_doc.get('master_style_guide', {})
            
            summary_parts = []
            
            # Language rules
            language_rules = master_guide.get('language_rules', {})
            if language_rules:
                summary_parts.append(f"Vocabulary Level: {language_rules.get('vocabulary_level', 'N/A')}")
                summary_parts.append(f"Age Appropriate Language: {language_rules.get('age_appropriate_language', 'N/A')}")
            
            # Dialect/Accent map
            dialect_map = master_guide.get('dialect_accent_map', {})
            if dialect_map:
                summary_parts.append(f"Voice Distinctions: {dialect_map.get('character_voice_distinctions', 'N/A')}")
            
            # Audio conventions
            audio_conventions = master_guide.get('audio_conventions', {})
            if audio_conventions:
                summary_parts.append(f"Scene Transitions: {audio_conventions.get('scene_transitions', 'N/A')}")
            
            # Dialogue principles
            dialogue_principles = master_guide.get('dialogue_principles', {})
            if dialogue_principles:
                summary_parts.append(f"Dialogue Style: {dialogue_principles.get('natural_vs_theatrical', 'N/A')}")
            
            # Narration style
            narration_style = master_guide.get('narration_style', {})
            if narration_style:
                summary_parts.append(f"Narrator Presence: {narration_style.get('narrator_presence', 'N/A')}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            return f"Error creating Master Style Guide summary: {str(e)}"

    async def validate_character_counts(self, character_bible_data: Dict):
        """Validate that character counts match configuration"""
        try:
            character_bible = character_bible_data.get('character_bible', {})
            
            # Get actual counts
            tier1_count = len(character_bible.get('tier_1_protagonists', []))
            tier2_count = len(character_bible.get('tier_2_major_supporting', []))
            tier3_count = len(character_bible.get('tier_3_recurring', []))
            
            # Get expected counts from config
            character_tiers = self.config_data.get('character_tiers', {})
            expected_tier1 = character_tiers.get('tier_1_protagonists', {}).get('count', 3)
            expected_tier2 = character_tiers.get('tier_2_major_supporting', {}).get('count', 5)
            expected_tier3 = character_tiers.get('tier_3_recurring', {}).get('count', 10)
            
            print(f"📊 Character Count Validation:")
            print(f"   Tier 1 Protagonists: {tier1_count}/{expected_tier1}")
            print(f"   Tier 2 Major Supporting: {tier2_count}/{expected_tier2}")
            print(f"   Tier 3 Recurring: {tier3_count}/{expected_tier3}")
            
            # Validate counts (allow some flexibility)
            if tier1_count < 1 or tier1_count > expected_tier1:
                print(f"⚠️  Warning: Tier 1 count ({tier1_count}) is outside expected range (1-{expected_tier1})")
            
            if tier2_count < 3 or tier2_count > expected_tier2:
                print(f"⚠️  Warning: Tier 2 count ({tier2_count}) is outside expected range (3-{expected_tier2})")
            
            if tier3_count < 5 or tier3_count > expected_tier3:
                print(f"⚠️  Warning: Tier 3 count ({tier3_count}) is outside expected range (5-{expected_tier3})")
            
            print("✅ Character count validation complete")
            
        except Exception as e:
            print(f"⚠️  Warning: Character count validation failed: {str(e)}")

    async def generate_readable_summary(self, character_bible_data: Dict, inputs: Dict) -> str:
        """Generate human-readable summary from structured JSON data"""
        try:
            summary_parts = []
            
            # Header
            summary_parts.append("=" * 70)
            summary_parts.append("STATION 7: CHARACTER ARCHITECT")
            summary_parts.append("=" * 70)
            summary_parts.append("")
            summary_parts.append(f"Working Title: {inputs.get('working_title', 'N/A')}")
            summary_parts.append(f"Primary Genre: {inputs.get('primary_genre', 'N/A')}")
            summary_parts.append(f"Target Age: {inputs.get('target_age', 'N/A')}")
            summary_parts.append(f"Episode Count: {inputs.get('episode_count', 'N/A')}")
            summary_parts.append(f"Core Premise: {inputs.get('core_premise', 'N/A')}")
            summary_parts.append("")
            
            # Character Bible sections
            character_bible = character_bible_data.get('character_bible', {})
            
            # Tier 1: Protagonists
            tier1_characters = character_bible.get('tier_1_protagonists', [])
            if tier1_characters:
                summary_parts.append("-" * 70)
                summary_parts.append("TIER 1: PROTAGONISTS")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                for i, character in enumerate(tier1_characters, 1):
                    name = character.get('name', 'Unknown')
                    age = character.get('age', 'N/A')
                    role = character.get('role', 'N/A')
                    summary_parts.append(f"{i}. {name} (Age: {age}, Role: {role})")
                    
                    # Psychological Profile
                    psych_profile = character.get('psychological_profile', {})
                    if psych_profile:
                        summary_parts.append(f"   Background: {psych_profile.get('background', 'N/A')}")
                        summary_parts.append(f"   Motivations: {psych_profile.get('motivations', 'N/A')}")
                        summary_parts.append(f"   Fears: {psych_profile.get('fears', 'N/A')}")
                        summary_parts.append(f"   Desires: {psych_profile.get('desires', 'N/A')}")
                    
                    # Voice Signature
                    voice_sig = character.get('voice_signature', {})
                    if voice_sig:
                        summary_parts.append(f"   Voice: {voice_sig.get('pitch', 'N/A')} pitch, {voice_sig.get('pace', 'N/A')} pace")
                        summary_parts.append(f"   Vocabulary: {voice_sig.get('vocabulary_style', 'N/A')}")
                    
                    # Audio Identification Markers
                    audio_markers = character.get('audio_identification_markers', {})
                    if audio_markers:
                        verbal_tics = audio_markers.get('verbal_tics', [])
                        catchphrases = audio_markers.get('catchphrases', [])
                        if verbal_tics:
                            summary_parts.append(f"   Verbal Tics: {', '.join(verbal_tics)}")
                        if catchphrases:
                            summary_parts.append(f"   Catchphrases: {', '.join(catchphrases)}")
                    
                    summary_parts.append("")
            
            # Tier 2: Major Supporting
            tier2_characters = character_bible.get('tier_2_major_supporting', [])
            if tier2_characters:
                summary_parts.append("-" * 70)
                summary_parts.append("TIER 2: MAJOR SUPPORTING")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                for i, character in enumerate(tier2_characters, 1):
                    name = character.get('name', 'Unknown')
                    age = character.get('age', 'N/A')
                    role = character.get('role', 'N/A')
                    summary_parts.append(f"{i}. {name} (Age: {age}, Role: {role})")
                    
                    # Backstory
                    backstory = character.get('relevant_backstory', 'N/A')
                    summary_parts.append(f"   Backstory: {backstory}")
                    
                    # Voice
                    voice = character.get('distinct_voice', {})
                    if voice:
                        summary_parts.append(f"   Voice: {voice.get('pitch', 'N/A')} pitch, {voice.get('pace', 'N/A')} pace")
                    
                    # Story Function
                    story_function = character.get('story_function', 'N/A')
                    summary_parts.append(f"   Story Function: {story_function}")
                    
                    # Relationship to Protagonists
                    relationship_to_protagonists = character.get('relationship_to_protagonists', [])
                    if relationship_to_protagonists:
                        summary_parts.append(f"   Relationship to Protagonists: {', '.join(relationship_to_protagonists)}")
                    
                    # Audio Identification Markers
                    audio_markers = character.get('audio_identification_markers', {})
                    if audio_markers:
                        verbal_tics = audio_markers.get('verbal_tics', [])
                        catchphrases = audio_markers.get('catchphrases', [])
                        if verbal_tics:
                            summary_parts.append(f"   Verbal Tics: {', '.join(verbal_tics)}")
                        if catchphrases:
                            summary_parts.append(f"   Catchphrases: {', '.join(catchphrases)}")
                    
                    summary_parts.append("")
            
            # Tier 3: Recurring
            tier3_characters = character_bible.get('tier_3_recurring', [])
            if tier3_characters:
                summary_parts.append("-" * 70)
                summary_parts.append("TIER 3: RECURRING")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                for i, character in enumerate(tier3_characters, 1):
                    name = character.get('name', 'Unknown')
                    age = character.get('age', 'N/A')
                    role = character.get('role', 'N/A')
                    summary_parts.append(f"{i}. {name} (Age: {age}, Role: {role})")
                    
                    # Defining Trait
                    defining_trait = character.get('defining_trait', 'N/A')
                    summary_parts.append(f"   Defining Trait: {defining_trait}")
                    
                    # Voice Hook
                    voice_hook = character.get('memorable_voice_hook', 'N/A')
                    summary_parts.append(f"   Voice Hook: {voice_hook}")
                    
                    # Narrative Purpose
                    narrative_purpose = character.get('narrative_purpose', 'N/A')
                    summary_parts.append(f"   Narrative Purpose: {narrative_purpose}")
                    
                    # Episodes Appearing
                    episodes_appearing = character.get('episodes_appearing', [])
                    if episodes_appearing:
                        summary_parts.append(f"   Episodes Appearing: {', '.join(map(str, episodes_appearing))}")
                    
                    # Audio Identification Markers
                    audio_markers = character.get('audio_identification_markers', {})
                    if audio_markers:
                        verbal_tics = audio_markers.get('verbal_tics', [])
                        catchphrases = audio_markers.get('catchphrases', [])
                        if verbal_tics:
                            summary_parts.append(f"   Verbal Tics: {', '.join(verbal_tics)}")
                        if catchphrases:
                            summary_parts.append(f"   Catchphrases: {', '.join(catchphrases)}")
                    
                    summary_parts.append("")
            
            summary_parts.append("=" * 70)
            summary_parts.append("END OF CHARACTER BIBLE")
            summary_parts.append("=" * 70)
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            raise ValueError(f"❌ Error generating readable summary: {str(e)}")

    async def compile_final_report(self, inputs: Dict, character_bible_data: Dict, readable_summary: str) -> Dict:
        """Compile the final comprehensive report"""
        return {
            "Character Bible Document": {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "working_title": inputs.get('working_title', 'Unknown'),
                "primary_genre": inputs.get('primary_genre', 'Unknown'),
                "target_age": inputs.get('target_age', 'Unknown'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "episode_length": inputs.get('episode_length', 'Unknown'),
                "story_complexity": inputs.get('story_complexity', 'Unknown'),
                "tone": inputs.get('tone', 'Unknown'),
                "narrator_strategy": inputs.get('narrator_strategy', 'Unknown'),
                "core_premise": inputs.get('core_premise', 'Unknown'),
                "character_bible": character_bible_data.get('character_bible', {}),
                "readable_summary": readable_summary
            }
        }

    async def save_outputs(self, report: Dict):
        """Save all output files (JSON + TXT + Redis)"""
        try:
            # Save JSON
            json_filename = self.config_data.get('output', {}).get('json_filename', '{session_id}_character_bible.json').format(session_id=self.session_id)
            json_path = self.output_dir / json_filename
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved JSON: {json_path}")

            # Save TXT
            readable_filename = self.config_data.get('output', {}).get('readable_filename', '{session_id}_readable.txt').format(session_id=self.session_id)
            txt_path = self.output_dir / readable_filename
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(report['Character Bible Document']['readable_summary'])
            print(f"✅ Saved TXT: {txt_path}")

            # Save to Redis
            redis_key = f"audiobook:{self.session_id}:station_07"
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

    station = Station07CharacterArchitect(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
