"""
Station 6: Master Style Guide Builder

This station synthesizes inputs from foundational stations to generate the definitive 
"Master Style Guide" that governs all creative and technical choices in subsequent 
script development and quality control phases.

Flow:
1. Load data from Stations 2, 3, 4.5, and 5
2. Extract required inputs from all previous stations
3. Execute comprehensive style guide synthesis:
   - Language Rules (from Station 3 + 4.5)
   - Dialect/Accent Map (from Station 2)
   - Audio Conventions (from Station 5)
   - Dialogue Principles (synthesized)
   - Narration Style (from Station 4.5)
   - Sonic Signature (from Station 2)
4. Save comprehensive master style guide document

Critical Architecture Agent - Output guides all subsequent creative decisions
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


class Station06MasterStyleGuideBuilder:
    """Station 6: Master Style Guide Builder"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=6)
        self.output_dir = Path("output/station_06")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("📖 STATION 6: MASTER STYLE GUIDE BUILDER")
        print("=" * 60)
        print()

        try:
            # Load data from all required stations
            station_data = await self.load_all_station_data()
            
            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs()
            
            print("✅ Data loaded successfully from all stations")
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
            print("-" * 60)
            print()

            # Build the comprehensive LLM prompt
            print("📖 Building Master Style Guide Synthesis Prompt...")
            prompt = await self.build_style_guide_prompt(extracted_inputs, station_data)
            print("✅ Prompt built successfully")
            print()

            # Execute the style guide synthesis
            print("=" * 60)
            print("🎯 EXECUTING MASTER STYLE GUIDE SYNTHESIS")
            print("=" * 60)
            print()

            print("📝 Sending request to LLM...")
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            print("✅ LLM response received")
            print()

            # Process the response
            print("🔍 Processing LLM response...")
            style_guide_data = extract_json(response)
            
            if not style_guide_data:
                raise ValueError("❌ Failed to extract valid JSON from LLM response")

            # Generate human-readable summary
            print("📄 Generating human-readable summary...")
            readable_summary = await self.generate_readable_summary(style_guide_data, extracted_inputs)
            print("✅ Summary generated")
            print()

            # Compile final report
            final_report = await self.compile_final_report(
                extracted_inputs, style_guide_data, readable_summary
            )

            # Save outputs
            await self.save_outputs(final_report)

            print()
            print("=" * 60)
            print("✅ STATION 6 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Session ID: {self.session_id}")
            print(f"Working Title: {extracted_inputs.get('working_title', 'N/A')}")
            print()
            print("📄 Output files:")
            print(f"   - output/station_06/{self.session_id}_output.json")
            print(f"   - output/station_06/{self.session_id}_readable.txt")
            print()
            print("📖 MASTER STYLE GUIDE COMPLETE")
            print("📌 Ready to proceed to Station 7")
            print()

        except Exception as e:
            print(f"❌ Station 6 failed: {str(e)}")
            logging.error(f"Station 6 error: {str(e)}")
            raise

    async def load_all_station_data(self) -> Dict:
        """Load data from all required stations"""
        try:
            station_data = {}
            
            # Load Station 2 data
            station2_key = f"audiobook:{self.session_id}:station_02"
            station2_raw = await self.redis_client.get(station2_key)
            if not station2_raw:
                raise ValueError(f"❌ No Station 2 data found for session {self.session_id}\n   Please run Station 2 first")
            station_data['station_02'] = json.loads(station2_raw)

            # Load Station 3 data
            station3_key = f"audiobook:{self.session_id}:station_03"
            station3_raw = await self.redis_client.get(station3_key)
            if not station3_raw:
                raise ValueError(f"❌ No Station 3 data found for session {self.session_id}\n   Please run Station 3 first")
            station_data['station_03'] = json.loads(station3_raw)

            # Load Station 4.5 data
            station45_key = f"audiobook:{self.session_id}:station_045"
            station45_raw = await self.redis_client.get(station45_key)
            if not station45_raw:
                raise ValueError(f"❌ No Station 4.5 data found for session {self.session_id}\n   Please run Station 4.5 first")
            station_data['station_045'] = json.loads(station45_raw)

            # Load Station 5 data
            station5_key = f"audiobook:{self.session_id}:station_05"
            station5_raw = await self.redis_client.get(station5_key)
            if not station5_raw:
                raise ValueError(f"❌ No Station 5 data found for session {self.session_id}\n   Please run Station 5 first")
            station_data['station_05'] = json.loads(station5_raw)

            return station_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing station data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading station data: {str(e)}")

    async def extract_required_inputs(self) -> Dict:
        """Extract required inputs from previous stations"""
        try:
            # Load Station 1 data for basic project info
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
            
            # From Station 2 - Enhanced extraction for pronunciation guide
            extracted['working_title'] = station2_data.get('working_title', 'Unknown')
            extracted['core_premise'] = station2_data.get('world_setting', {}).get('core_premise', 'Unknown')
            
            # Extract character names and locations for pronunciation guide
            main_characters = station1_data.get('main_characters', [])
            extracted['character_names'] = main_characters
            
            world_setting = station2_data.get('world_setting', {})
            extracted['primary_location'] = world_setting.get('primary_location', 'Unknown')
            extracted['key_locations'] = world_setting.get('key_locations', [])
            
            # Extract similar shows for musical references
            creative_promises = station2_data.get('creative_promises', {})
            extracted['similar_shows'] = creative_promises.get('unique_selling_points', [])
            
            # From Station 3 - Enhanced extraction for vocabulary examples
            chosen_blend = station3_data.get('chosen_blend_details', {})
            extracted['primary_genre'] = chosen_blend.get('primary_genre', 'Unknown')
            
            age_guidelines = station3_data.get('age_guidelines', {})
            extracted['target_age'] = age_guidelines.get('target_age_range', 'Unknown')
            extracted['age_appropriate_language'] = age_guidelines.get('language_guidelines', {})
            
            tone_calibration = station3_data.get('tone_calibration', {})
            extracted['tone'] = tone_calibration.get('light_dark_balance', 'Balanced')

            # From Station 4.5 - Enhanced extraction for narrator strategy details
            narrator_recommendation = station45_data.get('Narrator Strategy Recommendation', {})
            definitive_rec = narrator_recommendation.get('definitive_recommendation', {})
            extracted['narrator_strategy'] = definitive_rec.get('recommendation', 'Unknown')
            
            # Extract specific narrator type for explicit reference
            implementation_details = definitive_rec.get('implementation_details', {})
            if 'if_with_narrator' in implementation_details:
                narrator_details = implementation_details['if_with_narrator']
                extracted['narrator_type'] = narrator_details.get('narrator_type', 'Unknown')
            elif 'if_without_narrator' in implementation_details:
                extracted['narrator_type'] = 'No Narrator'
            elif 'if_hybrid' in implementation_details:
                extracted['narrator_type'] = 'Hybrid Approach'
            else:
                extracted['narrator_type'] = extracted['narrator_strategy']

            return extracted

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing station data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error extracting required inputs: {str(e)}")

    async def build_style_guide_prompt(self, inputs: Dict, station_data: Dict) -> str:
        """Build the comprehensive style guide synthesis prompt"""
        try:
            # Get the base prompt from config
            base_prompt = self.config.get_prompt('master_style_guide_synthesis')
            
            # Format the prompt with project data and station data
            formatted_prompt = base_prompt.format(
                working_title=inputs.get('working_title', 'Unknown'),
                primary_genre=inputs.get('primary_genre', 'Unknown'),
                target_age=inputs.get('target_age', 'Unknown'),
                episode_count=inputs.get('episode_count', 'Unknown'),
                episode_length=inputs.get('episode_length', 'Unknown'),
                story_complexity=inputs.get('story_complexity', 'Unknown'),
                tone=inputs.get('tone', 'Balanced'),
                narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
                narrator_type=inputs.get('narrator_type', 'Unknown'),
                core_premise=inputs.get('core_premise', 'Unknown'),
                character_names=', '.join(inputs.get('character_names', [])),
                primary_location=inputs.get('primary_location', 'Unknown'),
                key_locations=', '.join(inputs.get('key_locations', [])),
                similar_shows=', '.join(inputs.get('similar_shows', [])),
                age_appropriate_language=json.dumps(inputs.get('age_appropriate_language', {}), indent=2),
                station_02_data=json.dumps(station_data.get('station_02', {}), indent=2),
                station_03_data=json.dumps(station_data.get('station_03', {}), indent=2),
                station_045_data=json.dumps(station_data.get('station_045', {}), indent=2),
                station_05_data=json.dumps(station_data.get('station_05', {}), indent=2)
            )
            
            return formatted_prompt
            
        except Exception as e:
            raise ValueError(f"❌ Error building prompt: {str(e)}")

    async def generate_readable_summary(self, style_guide_data: Dict, inputs: Dict) -> str:
        """Generate human-readable summary from structured JSON data"""
        try:
            summary_parts = []
            
            # Header
            summary_parts.append("=" * 70)
            summary_parts.append("STATION 6: MASTER STYLE GUIDE BUILDER")
            summary_parts.append("=" * 70)
            summary_parts.append("")
            summary_parts.append(f"Working Title: {inputs.get('working_title', 'N/A')}")
            summary_parts.append(f"Primary Genre: {inputs.get('primary_genre', 'N/A')}")
            summary_parts.append(f"Target Age: {inputs.get('target_age', 'N/A')}")
            summary_parts.append(f"Episode Count: {inputs.get('episode_count', 'N/A')}")
            summary_parts.append(f"Episode Length: {inputs.get('episode_length', 'N/A')}")
            summary_parts.append(f"Narrator Strategy: {inputs.get('narrator_strategy', 'N/A')}")
            summary_parts.append("")
            
            # Master Style Guide sections
            master_guide = style_guide_data.get('master_style_guide', {})
            
            # Language Rules
            language_rules = master_guide.get('language_rules', {})
            if language_rules:
                summary_parts.append("-" * 70)
                summary_parts.append("LANGUAGE RULES")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                summary_parts.append(f"Vocabulary Level: {language_rules.get('vocabulary_level', 'N/A')}")
                summary_parts.append(f"Sentence Complexity: {language_rules.get('sentence_complexity', 'N/A')}")
                summary_parts.append(f"Technical Term Handling: {language_rules.get('technical_term_handling', 'N/A')}")
                summary_parts.append(f"Narrator Voice Guidelines: {language_rules.get('narrator_voice_guidelines', 'N/A')}")
                summary_parts.append(f"Age Appropriate Language: {language_rules.get('age_appropriate_language', 'N/A')}")
                summary_parts.append(f"Genre Specific Terminology: {language_rules.get('genre_specific_terminology', 'N/A')}")
                
                # Example Vocabulary
                example_vocab = language_rules.get('example_vocabulary', {})
                if example_vocab:
                    summary_parts.append("")
                    summary_parts.append("Example Vocabulary:")
                    use_words = example_vocab.get('use', [])
                    if use_words:
                        summary_parts.append(f"  Words to Use: {', '.join(use_words)}")
                    avoid_words = example_vocab.get('avoid', [])
                    if avoid_words:
                        summary_parts.append(f"  Words to Avoid: {', '.join(avoid_words)}")
                
                summary_parts.append("")
            
            # Dialect/Accent Map
            dialect_map = master_guide.get('dialect_accent_map', {})
            if dialect_map:
                summary_parts.append("-" * 70)
                summary_parts.append("DIALECT/ACCENT MAP")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                summary_parts.append(f"Character Voice Distinctions: {dialect_map.get('character_voice_distinctions', 'N/A')}")
                summary_parts.append(f"Regional Markers: {dialect_map.get('regional_markers', 'N/A')}")
                
                # Pronunciation Guide
                pronunciation_guide = dialect_map.get('pronunciation_guide', {})
                if pronunciation_guide:
                    summary_parts.append("")
                    summary_parts.append("Pronunciation Guide:")
                    character_names = pronunciation_guide.get('character_names', {})
                    if character_names:
                        summary_parts.append("  Character Names:")
                        for name, pronunciation in character_names.items():
                            summary_parts.append(f"    {name}: {pronunciation}")
                    
                    locations = pronunciation_guide.get('locations', {})
                    if locations:
                        summary_parts.append("  Locations:")
                        for location, pronunciation in locations.items():
                            summary_parts.append(f"    {location}: {pronunciation}")
                else:
                    summary_parts.append(f"Pronunciation Guide: {dialect_map.get('pronunciation_guide', 'N/A')}")
                
                summary_parts.append(f"Voice Casting Notes: {dialect_map.get('voice_casting_notes', 'N/A')}")
                summary_parts.append(f"Accent Consistency Rules: {dialect_map.get('accent_consistency_rules', 'N/A')}")
                summary_parts.append("")
            
            # Audio Conventions
            audio_conventions = master_guide.get('audio_conventions', {})
            if audio_conventions:
                summary_parts.append("-" * 70)
                summary_parts.append("AUDIO CONVENTIONS")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                summary_parts.append(f"Scene Transitions: {audio_conventions.get('scene_transitions', 'N/A')}")
                summary_parts.append(f"Flashback Conventions: {audio_conventions.get('flashback_conventions', 'N/A')}")
                summary_parts.append(f"Location Establishment: {audio_conventions.get('location_establishment', 'N/A')}")
                summary_parts.append(f"Silence Usage: {audio_conventions.get('silence_usage', 'N/A')}")
                summary_parts.append(f"Sound Cue System: {audio_conventions.get('sound_cue_system', 'N/A')}")
                summary_parts.append(f"Time Markers: {audio_conventions.get('time_markers', 'N/A')}")
                summary_parts.append("")
            
            # Dialogue Principles
            dialogue_principles = master_guide.get('dialogue_principles', {})
            if dialogue_principles:
                summary_parts.append("-" * 70)
                summary_parts.append("DIALOGUE PRINCIPLES")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                summary_parts.append(f"Natural vs Theatrical: {dialogue_principles.get('natural_vs_theatrical', 'N/A')}")
                summary_parts.append(f"Interruption Rules: {dialogue_principles.get('interruption_rules', 'N/A')}")
                summary_parts.append(f"Character Identification: {dialogue_principles.get('character_identification', 'N/A')}")
                summary_parts.append(f"Emotional Delivery: {dialogue_principles.get('emotional_delivery', 'N/A')}")
                summary_parts.append(f"Pacing Control: {dialogue_principles.get('pacing_control', 'N/A')}")
                summary_parts.append(f"Subtext Handling: {dialogue_principles.get('subtext_handling', 'N/A')}")
                summary_parts.append("")
            
            # Narration Style
            narration_style = master_guide.get('narration_style', {})
            if narration_style:
                summary_parts.append("-" * 70)
                summary_parts.append("NARRATION STYLE")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                summary_parts.append(f"Narrator Presence: {narration_style.get('narrator_presence', 'N/A')}")
                summary_parts.append(f"Narrator Relationship: {narration_style.get('narrator_relationship', 'N/A')}")
                summary_parts.append(f"Tense and Person: {narration_style.get('tense_and_person', 'N/A')}")
                summary_parts.append(f"Narrator Personality: {narration_style.get('narrator_personality', 'N/A')}")
                summary_parts.append(f"Narrator Functions: {narration_style.get('narrator_functions', 'N/A')}")
                summary_parts.append(f"Narrator Voice Casting: {narration_style.get('narrator_voice_casting', 'N/A')}")
                summary_parts.append("")
            
            # Sonic Signature
            sonic_signature = master_guide.get('sonic_signature', {})
            if sonic_signature:
                summary_parts.append("-" * 70)
                summary_parts.append("SONIC SIGNATURE")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                summary_parts.append(f"Recurring Motifs: {sonic_signature.get('recurring_motifs', 'N/A')}")
                summary_parts.append(f"Character Themes: {sonic_signature.get('character_themes', 'N/A')}")
                summary_parts.append(f"Environmental Soundscapes: {sonic_signature.get('environmental_soundscapes', 'N/A')}")
                summary_parts.append(f"Genre Audio Elements: {sonic_signature.get('genre_audio_elements', 'N/A')}")
                summary_parts.append(f"Mood Sound Palette: {sonic_signature.get('mood_sound_palette', 'N/A')}")
                summary_parts.append(f"Audio Identity: {sonic_signature.get('audio_identity', 'N/A')}")
                summary_parts.append(f"Musical References: {sonic_signature.get('musical_references', 'N/A')}")
                summary_parts.append("")
            
            summary_parts.append("=" * 70)
            summary_parts.append("END OF MASTER STYLE GUIDE")
            summary_parts.append("=" * 70)
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            raise ValueError(f"❌ Error generating readable summary: {str(e)}")

    async def compile_final_report(self, inputs: Dict, style_guide_data: Dict, readable_summary: str) -> Dict:
        """Compile the final comprehensive report"""
        return {
            "Master Style Guide Document": {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "working_title": inputs.get('working_title', 'Unknown'),
                "primary_genre": inputs.get('primary_genre', 'Unknown'),
                "target_age": inputs.get('target_age', 'Unknown'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "episode_length": inputs.get('episode_length', 'Unknown'),
                "narrator_strategy": inputs.get('narrator_strategy', 'Unknown'),
                "master_style_guide": style_guide_data.get('master_style_guide', {}),
                "readable_summary": readable_summary
            }
        }

    async def save_outputs(self, report: Dict):
        """Save all output files (JSON + TXT + Redis)"""
        try:
            # Save JSON
            json_path = self.output_dir / f"{self.session_id}_output.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved JSON: {json_path}")

            # Save TXT
            txt_path = self.output_dir / f"{self.session_id}_readable.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(report['Master Style Guide Document']['readable_summary'])
            print(f"✅ Saved TXT: {txt_path}")

            # Save to Redis
            redis_key = f"audiobook:{self.session_id}:station_06"
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

    station = Station06MasterStyleGuideBuilder(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
