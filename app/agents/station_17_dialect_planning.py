"""
Station 17: Dialect Planning

This station performs comprehensive dialect and voice consistency planning to ensure
character voice consistency and age-appropriate language throughout the series. It
validates voice signatures, speech patterns, age-appropriate language, dialect
consistency, and audio clarity requirements.

Flow:
1. Load data from previous stations (1, 2, 3, 4.5, 7, 8, 15)
2. Extract required inputs from previous stations
3. Execute dialect planning validation:
   - Character voice consistency (pitch, pace, vocabulary, speech patterns)
   - Age-appropriate language validation
   - Dialect and accent consistency
   - Audio clarity and speaker identification
   - Genre-appropriate language usage
4. Save comprehensive dialect planning results

Critical Voice Planning Agent - Output provides detailed voice direction and consistency analysis
"""

import asyncio
import json
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json
from app.agents.title_validator import TitleValidator


class Station17DialectPlanning:
    """Station 17: Dialect and Voice Consistency Planner"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=17)
        self.output_dir = Path("output/station_17")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🗣️ STATION 17: DIALECT PLANNING")
        print("=" * 60)
        print()

        try:
            # Load data from previous stations
            station_data = await self.load_previous_stations_data()
            
            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs(station_data)
            
            # --- START CRITICAL VALIDATION ---
            working_title = extracted_inputs.get('working_title', 'Unknown')
            character_bible = extracted_inputs.get('character_bible', {})
            world_building = extracted_inputs.get('world_building', {})
            detailed_outlines = extracted_inputs.get('detailed_outlines', {})

            if working_title == 'Unknown' or not character_bible or not world_building or not detailed_outlines:
                error_msg = (
                    "❌ CRITICAL ERROR: Cannot perform dialect planning. "
                    f"Missing required data: Working Title ('{working_title}'), "
                    f"Character Bible ({bool(character_bible)}), "
                    f"World Building ({bool(world_building)}), "
                    f"Detailed Outlines ({bool(detailed_outlines)}). "
                    "This data is expected from previous stations."
                )
                print(error_msg)
                raise ValueError(error_msg)
            
            print("✅ Critical data validated (Working Title, Character Bible, World Building, Detailed Outlines)")
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
            print(f"Narrator Strategy: {extracted_inputs.get('narrator_strategy', 'N/A')}")
            print("-" * 60)
            print()

            # Build the comprehensive LLM prompt
            print("🗣️ Building Dialect Planning Prompt...")
            prompt = await self.build_dialect_planning_prompt(extracted_inputs)
            print("✅ Prompt built successfully")
            print()

            # Generate dialect planning results
            print("🤖 Performing Dialect and Voice Consistency Analysis...")
            print("   This may take 60-90 seconds for comprehensive voice analysis...")
            print()
            
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            print("✅ Dialect planning completed successfully")
            print()

            # Extract and validate JSON
            print("🔍 Extracting and validating dialect planning data...")
            dialect_data = extract_json(response)
            
            if not dialect_data:
                print("❌ Failed to extract valid JSON from response")
                return
            
            print("✅ Dialect planning data extracted and validated")
            print()

            # Save outputs
            await self.save_outputs(dialect_data, extracted_inputs)

            print("=" * 60)
            print("✅ STATION 17 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Project: {extracted_inputs.get('working_title', 'Untitled')}")
            print(f"Session ID: {self.session_id}")
            print()
            print("📊 DIALECT PLANNING STATISTICS:")
            summary = dialect_data.get('dialect_planning_summary', {})
            print(f"   • Overall Status: {summary.get('overall_status', 'Unknown')}")
            print(f"   • Total Issues Found: {summary.get('total_issues_found', 0)}")
            print(f"   • Voice Consistency Issues: {summary.get('voice_consistency_issues', 0)}")
            print(f"   • Age Appropriateness Issues: {summary.get('age_appropriateness_issues', 0)}")
            print(f"   • Dialect Consistency Issues: {summary.get('dialect_consistency_issues', 0)}")
            print(f"   • Audio Clarity Issues: {summary.get('audio_clarity_issues', 0)}")
            print()
            print("📁 OUTPUT FILES:")
            print(f"   • {self.output_dir}/dialect_planning_results.json")
            print(f"   • {self.output_dir}/dialect_planning_report.txt")
            print(f"   • {self.output_dir}/dialect_planning_summary.csv")
            print()
            print("🎯 NEXT STEPS:")
            if summary.get('total_issues_found', 0) > 0:
                print("   ⚠️  VOICE/LANGUAGE ISSUES FOUND - Review and address before proceeding")
                print("   • Review voice direction recommendations")
                print("   • Address character voice consistency issues")
                print("   • Ensure age-appropriate language throughout")
            else:
                print("   ✅ Dialect planning passed - Voice consistency validated")
                print("   • Proceed to Station 18: Evergreen Check")
                print("   • Use voice direction notes for casting and production")

        except Exception as e:
            print(f"❌ Error in Station 17: {str(e)}")
            logging.error(f"Station 17 error: {str(e)}")
            raise

    async def load_previous_stations_data(self) -> Dict[str, Any]:
        """Load data from all previous stations"""
        station_data = {}
        
        # Load from Redis first
        try:
            # Station 1: Seed Processor
            station1_data = await self.redis_client.get(f"session:{self.session_id}:station:01:output")
            if station1_data:
                station_data['station_1'] = json.loads(station1_data)
            
            # Station 2: Project DNA Builder
            station2_data = await self.redis_client.get(f"session:{self.session_id}:station:02:bible")
            if station2_data:
                station_data['station_2'] = json.loads(station2_data)
            
            # Station 3: Age & Genre Optimizer
            station3_data = await self.redis_client.get(f"session:{self.session_id}:station:03:style_guide")
            if station3_data:
                station_data['station_3'] = json.loads(station3_data)
            
            # Station 4.5: Narrator Strategy
            station45_data = await self.redis_client.get(f"session:{self.session_id}:station:045:output")
            if station45_data:
                station_data['station_45'] = json.loads(station45_data)
            
            # Station 7: Character Architecture
            station7_data = await self.redis_client.get(f"session:{self.session_id}:station:07:character_bible")
            if station7_data:
                station_data['station_7'] = json.loads(station7_data)
            
            # Station 8: World Builder
            station8_data = await self.redis_client.get(f"session:{self.session_id}:station:08:world_bible")
            if station8_data:
                station_data['station_8'] = json.loads(station8_data)
            
            # Station 15: Detailed Episode Outlines
            station15_data = await self.redis_client.get(f"station_15:{self.session_id}")
            if station15_data:
                station_data['station_15'] = json.loads(station15_data)
                
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
            ('station_45', f'output/station_045/{self.session_id}_output.json'),
            ('station_7', f'output/station_07/{self.session_id}_character_bible.json'),
            ('station_8', f'output/station_08/{self.session_id}_world_bible.json'),
            ('station_15', f'output/station_15/{self.session_id}_detailed_episode_outlines.json')
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
        
        # From Station 4.5: Narrator Strategy
        if 'station_45' in station_data:
            station45 = station_data['station_45']
            extracted['narrator_strategy'] = station45.get('recommended_approach', 'Unknown')
        
        # Build context strings for the prompt
        extracted['character_bible'] = self._format_station_data(station_data.get('station_7', {}), "Character Bible")
        extracted['world_building'] = self._format_station_data(station_data.get('station_8', {}), "World Building")
        
        # Extract detailed outlines
        if 'station_15' in station_data:
            station15 = station_data['station_15']
            # Extract the actual outline data
            if 'outline_data' in station15:
                extracted['detailed_outlines'] = self._format_station_data(station15['outline_data'], "Detailed Episode Outlines")
            else:
                extracted['detailed_outlines'] = self._format_station_data(station15, "Detailed Episode Outlines")
        else:
            extracted['detailed_outlines'] = "No detailed episode outlines available"
        
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

    async def build_dialect_planning_prompt(self, inputs: Dict[str, Any]) -> str:
        """Build the comprehensive LLM prompt"""
        return self.config.prompts['main'].format(
            working_title=inputs.get('working_title', 'Untitled'),
            primary_genre=inputs.get('primary_genre', 'Unknown'),
            target_age=inputs.get('target_age', 'Unknown'),
            episode_count=inputs.get('episode_count', 'Unknown'),
            episode_length=inputs.get('episode_length', 'Unknown'),
            narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
            character_bible=inputs.get('character_bible', 'No data available'),
            world_building=inputs.get('world_building', 'No data available'),
            detailed_episode_outlines=inputs.get('detailed_outlines', 'No data available')
        )

    async def save_outputs(self, dialect_data: Dict[str, Any], inputs: Dict[str, Any]):
        """Save all output files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON output
        json_file = self.output_dir / f"{self.session_id}_dialect_planning_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": timestamp,
                "project_title": inputs.get('working_title', 'Untitled'),
                "dialect_planning_data": dialect_data
            }, f, indent=2, ensure_ascii=False)
        
        # Save readable text output
        readable_file = self.output_dir / f"{self.session_id}_dialect_planning_report.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 17: DIALECT PLANNING - COMPREHENSIVE VOICE ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Project: {inputs.get('working_title', 'Untitled')}\n\n")
            
            # Write summary
            summary = dialect_data.get('dialect_planning_summary', {})
            f.write("=" * 60 + "\n")
            f.write("DIALECT PLANNING SUMMARY\n")
            f.write("=" * 60 + "\n")
            f.write(f"Overall Status: {summary.get('overall_status', 'Unknown')}\n")
            f.write(f"Total Issues Found: {summary.get('total_issues_found', 0)}\n")
            f.write(f"Voice Consistency Issues: {summary.get('voice_consistency_issues', 0)}\n")
            f.write(f"Age Appropriateness Issues: {summary.get('age_appropriateness_issues', 0)}\n")
            f.write(f"Dialect Consistency Issues: {summary.get('dialect_consistency_issues', 0)}\n")
            f.write(f"Audio Clarity Issues: {summary.get('audio_clarity_issues', 0)}\n\n")
            
            # Write character voice consistency
            char_voice_consistency = dialect_data.get('character_voice_consistency', {})
            f.write("=" * 60 + "\n")
            f.write("CHARACTER VOICE CONSISTENCY ANALYSIS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {char_voice_consistency.get('status', 'Unknown')}\n\n")
            character_analyses = char_voice_consistency.get('character_analyses', [])
            if character_analyses:
                for char_analysis in character_analyses:
                    f.write(f"CHARACTER: {char_analysis.get('character_name', 'Unknown')}\n")
                    f.write(f"Voice Status: {char_analysis.get('voice_status', 'Unknown')}\n")
                    
                    voice_signature = char_analysis.get('voice_signature', {})
                    f.write("Voice Signature Analysis:\n")
                    f.write(f"  Pitch: {voice_signature.get('pitch', 'Unknown')}\n")
                    f.write(f"  Pace: {voice_signature.get('pace', 'Unknown')}\n")
                    f.write(f"  Vocabulary: {voice_signature.get('vocabulary', 'Unknown')}\n")
                    f.write(f"  Speech Patterns: {voice_signature.get('speech_patterns', 'Unknown')}\n")
                    f.write(f"  Verbal Tics: {voice_signature.get('verbal_tics', 'Unknown')}\n")
                    
                    issues = char_analysis.get('issues', [])
                    if issues:
                        f.write("Issues Found:\n")
                        for issue in issues:
                            f.write(f"  - {issue.get('issue_type', 'Unknown')}: {issue.get('description', 'No description')}\n")
                            f.write(f"    Severity: {issue.get('severity', 'Unknown')}\n")
                            f.write(f"    Location: {issue.get('location', 'Unknown')}\n")
                            f.write(f"    Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
                    
                    voice_direction = char_analysis.get('voice_direction_notes', 'No voice direction notes')
                    f.write(f"Voice Direction Notes: {voice_direction}\n\n")
            else:
                f.write("No character voice analyses available.\n\n")
            
            # Write age appropriateness
            age_appropriateness = dialect_data.get('age_appropriateness', {})
            f.write("=" * 60 + "\n")
            f.write("AGE APPROPRIATENESS ANALYSIS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {age_appropriateness.get('status', 'Unknown')}\n")
            f.write(f"Target Age: {age_appropriateness.get('target_age', 'Unknown')}\n\n")
            issues = age_appropriateness.get('issues', [])
            if issues:
                f.write("Issues Found:\n")
                for issue in issues:
                    f.write(f"  - {issue.get('issue_type', 'Unknown')}: {issue.get('description', 'No description')}\n")
                    f.write(f"    Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"    Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"    Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("No age appropriateness issues found.\n")
            
            language_guidelines = age_appropriateness.get('language_guidelines', 'No language guidelines available')
            f.write(f"\nLanguage Guidelines: {language_guidelines}\n\n")
            
            # Write dialect consistency
            dialect_consistency = dialect_data.get('dialect_consistency', {})
            f.write("=" * 60 + "\n")
            f.write("DIALECT CONSISTENCY ANALYSIS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {dialect_consistency.get('status', 'Unknown')}\n\n")
            issues = dialect_consistency.get('issues', [])
            if issues:
                f.write("Issues Found:\n")
                for issue in issues:
                    f.write(f"  - {issue.get('issue_type', 'Unknown')}: {issue.get('description', 'No description')}\n")
                    f.write(f"    Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"    Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"    Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("No dialect consistency issues found.\n")
            
            dialect_guidelines = dialect_consistency.get('dialect_guidelines', 'No dialect guidelines available')
            f.write(f"\nDialect Guidelines: {dialect_guidelines}\n\n")
            
            # Write audio clarity
            audio_clarity = dialect_data.get('audio_clarity', {})
            f.write("=" * 60 + "\n")
            f.write("AUDIO CLARITY ANALYSIS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {audio_clarity.get('status', 'Unknown')}\n\n")
            issues = audio_clarity.get('issues', [])
            if issues:
                f.write("Issues Found:\n")
                for issue in issues:
                    f.write(f"  - {issue.get('issue_type', 'Unknown')}: {issue.get('description', 'No description')}\n")
                    f.write(f"    Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"    Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"    Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("No audio clarity issues found.\n")
            
            audio_guidelines = audio_clarity.get('audio_guidelines', 'No audio guidelines available')
            f.write(f"\nAudio Guidelines: {audio_guidelines}\n\n")
            
            # Write genre appropriateness
            genre_appropriateness = dialect_data.get('genre_appropriateness', {})
            f.write("=" * 60 + "\n")
            f.write("GENRE APPROPRIATENESS ANALYSIS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {genre_appropriateness.get('status', 'Unknown')}\n")
            f.write(f"Genre: {genre_appropriateness.get('genre', 'Unknown')}\n\n")
            issues = genre_appropriateness.get('issues', [])
            if issues:
                f.write("Issues Found:\n")
                for issue in issues:
                    f.write(f"  - {issue.get('issue_type', 'Unknown')}: {issue.get('description', 'No description')}\n")
                    f.write(f"    Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"    Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"    Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("No genre appropriateness issues found.\n")
            
            genre_guidelines = genre_appropriateness.get('genre_guidelines', 'No genre guidelines available')
            f.write(f"\nGenre Guidelines: {genre_guidelines}\n\n")
            
            # Write voice direction recommendations
            voice_direction = dialect_data.get('voice_direction_recommendations', {})
            f.write("=" * 60 + "\n")
            f.write("VOICE DIRECTION RECOMMENDATIONS\n")
            f.write("=" * 60 + "\n")
            
            character_voice_notes = voice_direction.get('character_voice_notes', [])
            if character_voice_notes:
                f.write("CHARACTER VOICE NOTES:\n")
                for voice_note in character_voice_notes:
                    f.write(f"\nCharacter: {voice_note.get('character_name', 'Unknown')}\n")
                    f.write(f"Voice Description: {voice_note.get('voice_description', 'No description')}\n")
                    f.write(f"Speech Patterns: {voice_note.get('speech_patterns', 'No patterns')}\n")
                    f.write(f"Key Phrases: {', '.join(voice_note.get('key_phrases', []))}\n")
                    f.write(f"Emotional Range: {voice_note.get('emotional_range', 'No range')}\n")
                    f.write(f"Audio Notes: {voice_note.get('audio_notes', 'No notes')}\n")
            
            casting_guidelines = voice_direction.get('casting_guidelines', 'No casting guidelines available')
            f.write(f"\nCasting Guidelines: {casting_guidelines}\n")
            
            production_notes = voice_direction.get('production_notes', 'No production notes available')
            f.write(f"\nProduction Notes: {production_notes}\n\n")
            
            # Write recommendations
            recommendations = dialect_data.get('recommendations', {})
            f.write("=" * 60 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("=" * 60 + "\n")
            
            immediate_fixes = recommendations.get('immediate_fixes', [])
            if immediate_fixes:
                f.write("IMMEDIATE FIXES REQUIRED:\n")
                for fix in immediate_fixes:
                    f.write(f"  • {fix}\n")
                f.write("\n")
            
            suggested_improvements = recommendations.get('suggested_improvements', [])
            if suggested_improvements:
                f.write("SUGGESTED IMPROVEMENTS:\n")
                for improvement in suggested_improvements:
                    f.write(f"  • {improvement}\n")
                f.write("\n")
            
            minor_adjustments = recommendations.get('minor_adjustments', [])
            if minor_adjustments:
                f.write("MINOR ADJUSTMENTS:\n")
                for adjustment in minor_adjustments:
                    f.write(f"  • {adjustment}\n")
                f.write("\n")
            
            # Write validation notes
            validation_notes = dialect_data.get('validation_notes', 'No validation notes available')
            f.write("=" * 60 + "\n")
            f.write("VALIDATION NOTES\n")
            f.write("=" * 60 + "\n")
            f.write(validation_notes + "\n")
        
        # Save CSV summary
        csv_file = self.output_dir / f"{self.session_id}_dialect_planning_summary.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Category,Status,Issues Found,Voice Issues,Age Issues,Dialect Issues,Audio Issues\n")
            
            # Character voice consistency
            char_voice_consistency = dialect_data.get('character_voice_consistency', {})
            char_analyses = char_voice_consistency.get('character_analyses', [])
            char_issues = sum(len(analysis.get('issues', [])) for analysis in char_analyses)
            f.write(f"Character Voice Consistency,{char_voice_consistency.get('status', 'Unknown')},{char_issues},{char_issues},0,0,0\n")
            
            # Age appropriateness
            age_appropriateness = dialect_data.get('age_appropriateness', {})
            age_issues = len(age_appropriateness.get('issues', []))
            f.write(f"Age Appropriateness,{age_appropriateness.get('status', 'Unknown')},{age_issues},0,{age_issues},0,0\n")
            
            # Dialect consistency
            dialect_consistency = dialect_data.get('dialect_consistency', {})
            dialect_issues = len(dialect_consistency.get('issues', []))
            f.write(f"Dialect Consistency,{dialect_consistency.get('status', 'Unknown')},{dialect_issues},0,0,{dialect_issues},0\n")
            
            # Audio clarity
            audio_clarity = dialect_data.get('audio_clarity', {})
            audio_issues = len(audio_clarity.get('issues', []))
            f.write(f"Audio Clarity,{audio_clarity.get('status', 'Unknown')},{audio_issues},0,0,0,{audio_issues}\n")
            
            # Genre appropriateness
            genre_appropriateness = dialect_data.get('genre_appropriateness', {})
            genre_issues = len(genre_appropriateness.get('issues', []))
            f.write(f"Genre Appropriateness,{genre_appropriateness.get('status', 'Unknown')},{genre_issues},0,0,0,0\n")
        
        # Save to Redis
        await self.redis_client.set(
            f"station_17:{self.session_id}",
            json.dumps(dialect_data, ensure_ascii=False)
        )


async def main():
    """Main execution function"""
    session_id = input("🗣️ Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return
    
    station = Station17DialectPlanning(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
