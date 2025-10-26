"""
Station 16: Canon Check

This station performs comprehensive canon consistency validation across all story elements
before script writing begins. It checks character consistency, world consistency, plot
consistency, audio consistency, and genre/tone consistency to ensure no contradictions
or inconsistencies exist in the story.

Flow:
1. Load data from previous stations (1, 2, 3, 4.5, 7, 8, 15)
2. Extract required inputs from previous stations
3. Execute canon consistency validation:
   - Character consistency (names, ages, abilities, relationships, voices)
   - World consistency (locations, rules, timeline, geography, culture)
   - Plot consistency (cause-effect, motivations, information flow)
   - Audio consistency (sound signatures, voice descriptions, techniques)
   - Genre/tone consistency (genre elements, age appropriateness, style)
4. Save comprehensive canon check results

Critical Validation Agent - Output provides detailed consistency analysis and fixes
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


class Station16CanonCheck:
    """Station 16: Canon Consistency Validator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=16)
        self.output_dir = Path("output/station_16")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🔍 STATION 16: CANON CHECK")
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
                    "❌ CRITICAL ERROR: Cannot perform canon check. "
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
            print("🔍 Building Canon Check Prompt...")
            prompt = await self.build_canon_check_prompt(extracted_inputs)
            print("✅ Prompt built successfully")
            print()

            # Generate canon check results
            print("🤖 Performing Canon Consistency Validation...")
            print("   This may take 60-90 seconds for comprehensive consistency analysis...")
            print()
            
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            print("✅ Canon check completed successfully")
            print()

            # Extract and validate JSON
            print("🔍 Extracting and validating canon check data...")
            canon_data = extract_json(response)
            
            if not canon_data:
                print("❌ Failed to extract valid JSON from response")
                return
            
            print("✅ Canon check data extracted and validated")
            print()

            # Save outputs
            await self.save_outputs(canon_data, extracted_inputs)

            print("=" * 60)
            print("✅ STATION 16 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Project: {extracted_inputs.get('working_title', 'Untitled')}")
            print(f"Session ID: {self.session_id}")
            print()
            print("📊 CANON CHECK STATISTICS:")
            summary = canon_data.get('canon_check_summary', {})
            print(f"   • Overall Status: {summary.get('overall_status', 'Unknown')}")
            print(f"   • Total Issues Found: {summary.get('total_issues_found', 0)}")
            print(f"   • Critical Issues: {summary.get('critical_issues', 0)}")
            print(f"   • Warning Issues: {summary.get('warning_issues', 0)}")
            print(f"   • Minor Issues: {summary.get('minor_issues', 0)}")
            print()
            print("📁 OUTPUT FILES:")
            print(f"   • {self.output_dir}/canon_check_results.json")
            print(f"   • {self.output_dir}/canon_check_report.txt")
            print(f"   • {self.output_dir}/canon_check_summary.csv")
            print()
            print("🎯 NEXT STEPS:")
            if summary.get('critical_issues', 0) > 0:
                print("   ⚠️  CRITICAL ISSUES FOUND - Review and fix before proceeding")
                print("   • Address all critical issues in canon check report")
                print("   • Re-run Station 16 after fixes")
            else:
                print("   ✅ Canon check passed - Ready for script development")
                print("   • Proceed to Station 17: Dialect Planning")
                print("   • Use canon check report for reference during script writing")

        except Exception as e:
            print(f"❌ Error in Station 16: {str(e)}")
            logging.error(f"Station 16 error: {str(e)}")
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

    async def build_canon_check_prompt(self, inputs: Dict[str, Any]) -> str:
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

    async def save_outputs(self, canon_data: Dict[str, Any], inputs: Dict[str, Any]):
        """Save all output files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON output
        json_file = self.output_dir / f"{self.session_id}_canon_check_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": timestamp,
                "project_title": inputs.get('working_title', 'Untitled'),
                "canon_check_data": canon_data
            }, f, indent=2, ensure_ascii=False)
        
        # Save readable text output
        readable_file = self.output_dir / f"{self.session_id}_canon_check_report.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STATION 16: CANON CHECK - COMPREHENSIVE VALIDATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Project: {inputs.get('working_title', 'Untitled')}\n\n")
            
            # Write summary
            summary = canon_data.get('canon_check_summary', {})
            f.write("=" * 60 + "\n")
            f.write("CANON CHECK SUMMARY\n")
            f.write("=" * 60 + "\n")
            f.write(f"Overall Status: {summary.get('overall_status', 'Unknown')}\n")
            f.write(f"Total Issues Found: {summary.get('total_issues_found', 0)}\n")
            f.write(f"Critical Issues: {summary.get('critical_issues', 0)}\n")
            f.write(f"Warning Issues: {summary.get('warning_issues', 0)}\n")
            f.write(f"Minor Issues: {summary.get('minor_issues', 0)}\n\n")
            
            # Write character consistency
            char_consistency = canon_data.get('character_consistency', {})
            f.write("=" * 60 + "\n")
            f.write("CHARACTER CONSISTENCY CHECK\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {char_consistency.get('status', 'Unknown')}\n\n")
            issues = char_consistency.get('issues', [])
            if issues:
                for issue in issues:
                    f.write(f"ISSUE: {issue.get('issue_type', 'Unknown')}\n")
                    f.write(f"Character: {issue.get('character_name', 'Unknown')}\n")
                    f.write(f"Description: {issue.get('description', 'No description')}\n")
                    f.write(f"Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"Recommendation: {issue.get('recommendation', 'No recommendation')}\n\n")
            else:
                f.write("No character consistency issues found.\n\n")
            
            # Write world consistency
            world_consistency = canon_data.get('world_consistency', {})
            f.write("=" * 60 + "\n")
            f.write("WORLD CONSISTENCY CHECK\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {world_consistency.get('status', 'Unknown')}\n\n")
            issues = world_consistency.get('issues', [])
            if issues:
                for issue in issues:
                    f.write(f"ISSUE: {issue.get('issue_type', 'Unknown')}\n")
                    f.write(f"Element Type: {issue.get('element_type', 'Unknown')}\n")
                    f.write(f"Description: {issue.get('description', 'No description')}\n")
                    f.write(f"Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"Recommendation: {issue.get('recommendation', 'No recommendation')}\n\n")
            else:
                f.write("No world consistency issues found.\n\n")
            
            # Write plot consistency
            plot_consistency = canon_data.get('plot_consistency', {})
            f.write("=" * 60 + "\n")
            f.write("PLOT CONSISTENCY CHECK\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {plot_consistency.get('status', 'Unknown')}\n\n")
            issues = plot_consistency.get('issues', [])
            if issues:
                for issue in issues:
                    f.write(f"ISSUE: {issue.get('issue_type', 'Unknown')}\n")
                    f.write(f"Description: {issue.get('description', 'No description')}\n")
                    f.write(f"Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"Recommendation: {issue.get('recommendation', 'No recommendation')}\n\n")
            else:
                f.write("No plot consistency issues found.\n\n")
            
            # Write audio consistency
            audio_consistency = canon_data.get('audio_consistency', {})
            f.write("=" * 60 + "\n")
            f.write("AUDIO CONSISTENCY CHECK\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {audio_consistency.get('status', 'Unknown')}\n\n")
            issues = audio_consistency.get('issues', [])
            if issues:
                for issue in issues:
                    f.write(f"ISSUE: {issue.get('issue_type', 'Unknown')}\n")
                    f.write(f"Description: {issue.get('description', 'No description')}\n")
                    f.write(f"Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"Recommendation: {issue.get('recommendation', 'No recommendation')}\n\n")
            else:
                f.write("No audio consistency issues found.\n\n")
            
            # Write genre/tone consistency
            genre_tone_consistency = canon_data.get('genre_tone_consistency', {})
            f.write("=" * 60 + "\n")
            f.write("GENRE/TONE CONSISTENCY CHECK\n")
            f.write("=" * 60 + "\n")
            f.write(f"Status: {genre_tone_consistency.get('status', 'Unknown')}\n\n")
            issues = genre_tone_consistency.get('issues', [])
            if issues:
                for issue in issues:
                    f.write(f"ISSUE: {issue.get('issue_type', 'Unknown')}\n")
                    f.write(f"Description: {issue.get('description', 'No description')}\n")
                    f.write(f"Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"Recommendation: {issue.get('recommendation', 'No recommendation')}\n\n")
            else:
                f.write("No genre/tone consistency issues found.\n\n")
            
            # Write recommendations
            recommendations = canon_data.get('recommendations', {})
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
            validation_notes = canon_data.get('validation_notes', 'No validation notes available')
            f.write("=" * 60 + "\n")
            f.write("VALIDATION NOTES\n")
            f.write("=" * 60 + "\n")
            f.write(validation_notes + "\n")
        
        # Save CSV summary
        csv_file = self.output_dir / f"{self.session_id}_canon_check_summary.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Category,Status,Issues Found,Critical,Warning,Minor\n")
            
            # Character consistency
            char_consistency = canon_data.get('character_consistency', {})
            char_issues = char_consistency.get('issues', [])
            char_critical = len([i for i in char_issues if i.get('severity') == 'critical'])
            char_warning = len([i for i in char_issues if i.get('severity') == 'warning'])
            char_minor = len([i for i in char_issues if i.get('severity') == 'minor'])
            f.write(f"Character Consistency,{char_consistency.get('status', 'Unknown')},{len(char_issues)},{char_critical},{char_warning},{char_minor}\n")
            
            # World consistency
            world_consistency = canon_data.get('world_consistency', {})
            world_issues = world_consistency.get('issues', [])
            world_critical = len([i for i in world_issues if i.get('severity') == 'critical'])
            world_warning = len([i for i in world_issues if i.get('severity') == 'warning'])
            world_minor = len([i for i in world_issues if i.get('severity') == 'minor'])
            f.write(f"World Consistency,{world_consistency.get('status', 'Unknown')},{len(world_issues)},{world_critical},{world_warning},{world_minor}\n")
            
            # Plot consistency
            plot_consistency = canon_data.get('plot_consistency', {})
            plot_issues = plot_consistency.get('issues', [])
            plot_critical = len([i for i in plot_issues if i.get('severity') == 'critical'])
            plot_warning = len([i for i in plot_issues if i.get('severity') == 'warning'])
            plot_minor = len([i for i in plot_issues if i.get('severity') == 'minor'])
            f.write(f"Plot Consistency,{plot_consistency.get('status', 'Unknown')},{len(plot_issues)},{plot_critical},{plot_warning},{plot_minor}\n")
            
            # Audio consistency
            audio_consistency = canon_data.get('audio_consistency', {})
            audio_issues = audio_consistency.get('issues', [])
            audio_critical = len([i for i in audio_issues if i.get('severity') == 'critical'])
            audio_warning = len([i for i in audio_issues if i.get('severity') == 'warning'])
            audio_minor = len([i for i in audio_issues if i.get('severity') == 'minor'])
            f.write(f"Audio Consistency,{audio_consistency.get('status', 'Unknown')},{len(audio_issues)},{audio_critical},{audio_warning},{audio_minor}\n")
            
            # Genre/tone consistency
            genre_tone_consistency = canon_data.get('genre_tone_consistency', {})
            genre_tone_issues = genre_tone_consistency.get('issues', [])
            genre_tone_critical = len([i for i in genre_tone_issues if i.get('severity') == 'critical'])
            genre_tone_warning = len([i for i in genre_tone_issues if i.get('severity') == 'warning'])
            genre_tone_minor = len([i for i in genre_tone_issues if i.get('severity') == 'minor'])
            f.write(f"Genre/Tone Consistency,{genre_tone_consistency.get('status', 'Unknown')},{len(genre_tone_issues)},{genre_tone_critical},{genre_tone_warning},{genre_tone_minor}\n")
        
        # Save to Redis
        await self.redis_client.set(
            f"station_16:{self.session_id}",
            json.dumps(canon_data, ensure_ascii=False)
        )


async def main():
    """Main execution function"""
    session_id = input("🔍 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return
    
    station = Station16CanonCheck(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
