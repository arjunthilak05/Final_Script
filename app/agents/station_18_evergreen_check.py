"""
Station 18: Evergreen Check

This station performs comprehensive evergreen content validation to ensure the story
will remain relevant and timeless. It checks for dated references, emphasizes universal
themes, validates timeless language, ensures cultural universality, and future-proofs
content for long-term relevance.

Flow:
1. Load data from previous stations (1, 2, 3, 4.5, 7, 8, 15)
2. Extract required inputs from previous stations
3. Execute evergreen content validation:
   - Dated reference check (technology, pop culture, brands, slang, dates)
   - Universal theme emphasis (love, loss, growth, friendship, family, justice)
   - Timeless language check (contemporary slang, trending expressions)
   - Cultural universality check (cross-cultural themes and conflicts)
   - Future-proofing check (technology, social structures, communication)
4. Save comprehensive evergreen check results

Quality Control Agent - Output provides detailed evergreen analysis and timeless alternatives
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


class Station18EvergreenCheck:
    """Station 18: Evergreen Content Validator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=18)
        self.output_dir = Path("output/station_18")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🌿 STATION 18: EVERGREEN CHECK")
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
                    "❌ CRITICAL ERROR: Cannot perform evergreen check. "
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
            print(f"Episode Length: {extracted_inputs.get('episode_length', 'N/A')}")
            print(f"Narrator Strategy: {extracted_inputs.get('narrator_strategy', 'N/A')}")
            print()

            # Execute evergreen check
            print("-" * 60)
            print("🌿 EXECUTING EVERGREEN CHECK")
            print("-" * 60)
            print("Checking for:")
            print("• Dated references (technology, pop culture, brands, slang)")
            print("• Universal theme emphasis")
            print("• Timeless language patterns")
            print("• Cultural universality")
            print("• Future-proofing elements")
            print()

            evergreen_results = await self.execute_evergreen_check(extracted_inputs)
            
            print("✅ Evergreen check completed")
            print()

            # Save results
            await self.save_results(evergreen_results)
            
            print("✅ Results saved successfully")
            print()
            print("=" * 60)
            print("🎯 EVERGREEN CHECK COMPLETE")
            print("=" * 60)
            print(f"Session ID: {self.session_id}")
            print(f"Overall Status: {evergreen_results.get('evergreen_check_summary', {}).get('overall_status', 'Unknown')}")
            print(f"Total Issues Found: {evergreen_results.get('evergreen_check_summary', {}).get('total_issues_found', 0)}")
            print()
            print("📁 Output Files:")
            session_id_clean = self.session_id.replace("session_", "") if self.session_id.startswith("session_") else self.session_id
            print(f"• JSON: output/station_18/session_{session_id_clean}_evergreen_check_results.json")
            print(f"• Report: output/station_18/session_{session_id_clean}_evergreen_check_report.txt")
            print(f"• Summary: output/station_18/session_{session_id_clean}_evergreen_check_summary.csv")

        except Exception as e:
            print(f"❌ Error in Station 18: {str(e)}")
            raise

    async def load_previous_stations_data(self) -> Dict[str, Any]:
        """Load data from all previous stations"""
        print("📥 Loading data from previous stations...")
        
        station_data = {}
        
        # Load from Redis first
        try:
            # Station 1: Seed Processor
            station1_data = await self.redis_client.get(f"session:{self.session_id}:station:01:output")
            if station1_data:
                station_data['station_1'] = json.loads(station1_data)
                print("✅ Station 1 data loaded")
            
            # Station 2: Project DNA Builder
            station2_data = await self.redis_client.get(f"session:{self.session_id}:station:02:bible")
            if station2_data:
                station_data['station_2'] = json.loads(station2_data)
                print("✅ Station 2 data loaded")
            
            # Station 3: Age & Genre Optimizer
            station3_data = await self.redis_client.get(f"session:{self.session_id}:station:03:style_guide")
            if station3_data:
                station_data['station_3'] = json.loads(station3_data)
                print("✅ Station 3 data loaded")

            # Station 4.5: Narrator Strategy Designer
            station45_data = await self.redis_client.get(f"session:{self.session_id}:station:045:output")
            if station45_data:
                station_data['station_045'] = json.loads(station45_data)
                print("✅ Station 4.5 data loaded")

            # Station 7: Character Architect
            station7_data = await self.redis_client.get(f"session:{self.session_id}:station:07:character_bible")
            if station7_data:
                station_data['station_7'] = json.loads(station7_data)
                print("✅ Station 7 data loaded")

            # Station 8: World Builder
            station8_data = await self.redis_client.get(f"session:{self.session_id}:station:08:world_bible")
            if station8_data:
                station_data['station_8'] = json.loads(station8_data)
                print("✅ Station 8 data loaded")

            # Station 15: Detailed Episode Outlining
            station15_data = await self.redis_client.get(f"session:{self.session_id}:station:15:detailed_episode_outlines")
            if station15_data:
                station_data['station_15'] = json.loads(station15_data)
                print("✅ Station 15 data loaded")

        except Exception as e:
            print(f"⚠️  Redis data loading error: {e}")

        # Fallback to file system if Redis data not available
        if not station_data:
            print("📁 Loading data from file system...")
            station_data = await self.load_from_filesystem()
        else:
            # Try to load missing stations from filesystem
            print("📁 Loading missing stations from file system...")
            filesystem_data = await self.load_from_filesystem()
            for key, value in filesystem_data.items():
                if key not in station_data:
                    station_data[key] = value

        return station_data

    async def load_from_filesystem(self) -> Dict[str, Any]:
        """Load data from file system as fallback"""
        station_data = {}
        
        # Ensure session_id has the correct format
        session_id_formatted = f"session_{self.session_id}" if not self.session_id.startswith("session_") else self.session_id
        
        try:
            # Load Station 1 data
            station1_file = Path(f"output/station_01/{session_id_formatted}_output.json")
            if station1_file.exists():
                with open(station1_file, 'r', encoding='utf-8') as f:
                    station_data['station_1'] = json.load(f)
                print("✅ Station 1 data loaded from file")
            
            # Load Station 2 data
            station2_file = Path(f"output/station_02/{session_id_formatted}_bible.json")
            if station2_file.exists():
                with open(station2_file, 'r', encoding='utf-8') as f:
                    station_data['station_2'] = json.load(f)
                print("✅ Station 2 data loaded from file")
            
            # Load Station 3 data
            station3_file = Path(f"output/station_03/{session_id_formatted}_style_guide.json")
            if station3_file.exists():
                with open(station3_file, 'r', encoding='utf-8') as f:
                    station_data['station_3'] = json.load(f)
                print("✅ Station 3 data loaded from file")

            # Load Station 4.5 data
            station45_file = Path(f"output/station_045/{session_id_formatted}_output.json")
            if station45_file.exists():
                with open(station45_file, 'r', encoding='utf-8') as f:
                    station_data['station_045'] = json.load(f)
                print("✅ Station 4.5 data loaded from file")

            # Load Station 7 data
            station7_file = Path(f"output/station_07/{session_id_formatted}_character_bible.json")
            if station7_file.exists():
                with open(station7_file, 'r', encoding='utf-8') as f:
                    station_data['station_7'] = json.load(f)
                print("✅ Station 7 data loaded from file")

            # Load Station 8 data
            station8_file = Path(f"output/station_08/{session_id_formatted}_world_bible.json")
            if station8_file.exists():
                with open(station8_file, 'r', encoding='utf-8') as f:
                    station_data['station_8'] = json.load(f)
                print("✅ Station 8 data loaded from file")

            # Load Station 15 data
            station15_file = Path(f"output/station_15/{session_id_formatted}_detailed_episode_outlines.json")
            if station15_file.exists():
                with open(station15_file, 'r', encoding='utf-8') as f:
                    station_data['station_15'] = json.load(f)
                print("✅ Station 15 data loaded from file")

        except Exception as e:
            print(f"⚠️  File system loading error: {e}")

        return station_data

    async def extract_required_inputs(self, station_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract required inputs from previous stations"""
        print("🔍 Extracting required inputs...")
        print(f"Available stations: {list(station_data.keys())}")
        
        extracted = {}
        
        # Extract from Station 1 (Seed Processor)
        if 'station_1' in station_data:
            station_1_data = station_data['station_1']
            # Data is directly in the station data, not nested under 'data'
            extracted['working_title'] = station_1_data.get('chosen_title', 'Unknown')
            extracted['episode_count'] = station_1_data.get('option_details', {}).get('episode_count', 'Unknown')
            extracted['episode_length'] = station_1_data.get('option_details', {}).get('episode_length', 'Unknown')
            print(f"✅ Station 1 extracted: title={extracted['working_title']}")
        else:
            print("❌ Station 1 data not found")

        # Extract from Station 2 (Project DNA Builder)
        if 'station_2' in station_data:
            station_2_data = station_data['station_2']
            # Data is directly in the station data
            extracted['primary_genre'] = station_2_data.get('primary_genre', 'Unknown')
            extracted['target_age'] = station_2_data.get('target_age', 'Unknown')

        # Extract from Station 4.5 (Narrator Strategy Designer)
        if 'station_045' in station_data:
            station_045_data = station_data['station_045']
            # Data is nested under "Narrator Strategy Recommendation"
            if 'Narrator Strategy Recommendation' in station_045_data:
                doc_data = station_045_data['Narrator Strategy Recommendation']
                extracted['narrator_strategy'] = doc_data.get('recommended_approach', 'Unknown')

        # Extract Character Bible from Station 7
        if 'station_7' in station_data:
            station_7_data = station_data['station_7']
            # Data is nested under "Character Bible Document"
            if 'Character Bible Document' in station_7_data:
                doc_data = station_7_data['Character Bible Document']
                extracted['character_bible'] = doc_data.get('character_bible', {})
                print(f"✅ Station 7 extracted: character_bible keys={list(extracted['character_bible'].keys())}")
            else:
                print("❌ Station 7: 'Character Bible Document' not found")
        else:
            print("❌ Station 7 data not found")

        # Extract World Building from Station 8
        if 'station_8' in station_data:
            station_8_data = station_data['station_8']
            # Data is nested under "World Bible Document"
            if 'World Bible Document' in station_8_data:
                doc_data = station_8_data['World Bible Document']
                extracted['world_building'] = doc_data.get('world_bible', {})
                print(f"✅ Station 8 extracted: world_building keys={list(extracted['world_building'].keys())}")
            else:
                print("❌ Station 8: 'World Bible Document' not found")
        else:
            print("❌ Station 8 data not found")

        # Extract Detailed Episode Outlines from Station 15
        if 'station_15' in station_data:
            station_15_data = station_data['station_15']
            # Data is under "outline_data" -> "detailed_episode_outlines"
            if 'outline_data' in station_15_data:
                outline_data = station_15_data['outline_data']
                extracted['detailed_outlines'] = outline_data.get('detailed_episode_outlines', {})
                print(f"✅ Station 15 extracted: detailed_outlines count={len(extracted['detailed_outlines'])}")
            else:
                print("❌ Station 15: 'outline_data' not found")
        else:
            print("❌ Station 15 data not found")

        return extracted

    async def execute_evergreen_check(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the evergreen check using AI"""
        print("🤖 Executing evergreen check with AI...")
        
        # Prepare the prompt
        prompt = self.config.get_prompt('main').format(
            working_title=inputs.get('working_title', 'Unknown'),
            primary_genre=inputs.get('primary_genre', 'Unknown'),
            target_age=inputs.get('target_age', 'Unknown'),
            episode_count=inputs.get('episode_count', 'Unknown'),
            episode_length=inputs.get('episode_length', 'Unknown'),
            narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
            character_bible=json.dumps(inputs.get('character_bible', {}), indent=2),
            world_building=json.dumps(inputs.get('world_building', {}), indent=2),
            detailed_episode_outlines=json.dumps(inputs.get('detailed_outlines', {}), indent=2)
        )

        # Get AI response
        response = await self.agent.process_message(
            user_input=prompt,
            model_name=self.config.model,
            max_tokens=self.config.max_tokens
        )

        # Extract JSON from response
        evergreen_results = extract_json(response)
        
        if not evergreen_results:
            raise ValueError("Failed to extract valid JSON from AI response")

        return evergreen_results

    async def save_results(self, evergreen_results: Dict[str, Any]):
        """Save evergreen check results to files"""
        print("💾 Saving evergreen check results...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results - handle session_id that may already include "session_" prefix
        session_id_clean = self.session_id.replace("session_", "") if self.session_id.startswith("session_") else self.session_id
        json_file = self.output_dir / f"session_{session_id_clean}_evergreen_check_results.json"
        evergreen_results['session_id'] = self.session_id
        evergreen_results['timestamp'] = timestamp
        evergreen_results['project_title'] = evergreen_results.get('working_title', 'Unknown')
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(evergreen_results, f, indent=2, ensure_ascii=False)
        
        # Save readable report
        readable_file = self.output_dir / f"session_{session_id_clean}_evergreen_check_report.txt"
        await self.create_readable_report(evergreen_results, readable_file)
        
        # Save CSV summary
        csv_file = self.output_dir / f"session_{session_id_clean}_evergreen_check_summary.csv"
        await self.create_csv_summary(evergreen_results, csv_file)

    async def create_readable_report(self, evergreen_results: Dict[str, Any], file_path: Path):
        """Create a human-readable report"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("🌿 EVERGREEN CHECK REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Timestamp: {evergreen_results.get('timestamp', 'Unknown')}\n")
            f.write(f"Project Title: {evergreen_results.get('project_title', 'Unknown')}\n\n")
            
            # Summary
            summary = evergreen_results.get('evergreen_check_summary', {})
            f.write("📊 EVERGREEN CHECK SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Overall Status: {summary.get('overall_status', 'Unknown')}\n")
            f.write(f"Total Issues Found: {summary.get('total_issues_found', 0)}\n")
            f.write(f"Dated Reference Issues: {summary.get('dated_reference_issues', 0)}\n")
            f.write(f"Universal Theme Issues: {summary.get('universal_theme_issues', 0)}\n")
            f.write(f"Timeless Language Issues: {summary.get('timeless_language_issues', 0)}\n")
            f.write(f"Cultural Universality Issues: {summary.get('cultural_universality_issues', 0)}\n")
            f.write(f"Future-Proofing Issues: {summary.get('future_proofing_issues', 0)}\n\n")
            
            # Dated Reference Check
            dated_check = evergreen_results.get('dated_reference_check', {})
            f.write("📅 DATED REFERENCE CHECK\n")
            f.write("-" * 40 + "\n")
            f.write(f"Status: {dated_check.get('status', 'Unknown')}\n")
            issues = dated_check.get('issues', [])
            if issues:
                f.write(f"Issues Found: {len(issues)}\n")
                for i, issue in enumerate(issues, 1):
                    f.write(f"\n{i}. {issue.get('issue_type', 'Unknown Issue')}\n")
                    f.write(f"   Description: {issue.get('description', 'No description')}\n")
                    f.write(f"   Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"   Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"   Current Reference: {issue.get('current_reference', 'N/A')}\n")
                    f.write(f"   Timeless Alternative: {issue.get('timeless_alternative', 'N/A')}\n")
                    f.write(f"   Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("✅ No dated references found\n")
            f.write("\n")
            
            # Universal Theme Emphasis
            theme_check = evergreen_results.get('universal_theme_emphasis', {})
            f.write("🎭 UNIVERSAL THEME EMPHASIS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Status: {theme_check.get('status', 'Unknown')}\n")
            themes = theme_check.get('themes_identified', [])
            if themes:
                f.write(f"Themes Identified: {len(themes)}\n")
                for i, theme in enumerate(themes, 1):
                    f.write(f"\n{i}. {theme.get('theme_name', 'Unknown Theme')}\n")
                    f.write(f"   Universality Score: {theme.get('universality_score', 'N/A')}/10\n")
                    f.write(f"   Cultural Applicability: {theme.get('cultural_applicability', 'Unknown')}\n")
                    f.write(f"   Timeless Relevance: {theme.get('timeless_relevance', 'Unknown')}\n")
                    f.write(f"   Emphasis Level: {theme.get('emphasis_level', 'Unknown')}\n")
                    f.write(f"   Recommendation: {theme.get('recommendation', 'No recommendation')}\n")
            
            issues = theme_check.get('issues', [])
            if issues:
                f.write(f"\nTheme Issues Found: {len(issues)}\n")
                for i, issue in enumerate(issues, 1):
                    f.write(f"\n{i}. {issue.get('issue_type', 'Unknown Issue')}\n")
                    f.write(f"   Description: {issue.get('description', 'No description')}\n")
                    f.write(f"   Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"   Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"   Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            f.write("\n")
            
            # Recommendations
            recommendations = evergreen_results.get('evergreen_recommendations', {})
            f.write("💡 RECOMMENDATIONS\n")
            f.write("-" * 40 + "\n")
            
            immediate_fixes = recommendations.get('immediate_fixes', [])
            if immediate_fixes:
                f.write("🚨 IMMEDIATE FIXES:\n")
                for i, fix in enumerate(immediate_fixes, 1):
                    f.write(f"{i}. {fix}\n")
                f.write("\n")
            
            suggested_improvements = recommendations.get('suggested_improvements', [])
            if suggested_improvements:
                f.write("⚠️  SUGGESTED IMPROVEMENTS:\n")
                for i, improvement in enumerate(suggested_improvements, 1):
                    f.write(f"{i}. {improvement}\n")
                f.write("\n")
            
            minor_adjustments = recommendations.get('minor_adjustments', [])
            if minor_adjustments:
                f.write("📝 MINOR ADJUSTMENTS:\n")
                for i, adjustment in enumerate(minor_adjustments, 1):
                    f.write(f"{i}. {adjustment}\n")
                f.write("\n")
            
            # Validation Notes
            validation_notes = evergreen_results.get('validation_notes', '')
            if validation_notes:
                f.write("📋 VALIDATION NOTES\n")
                f.write("-" * 40 + "\n")
                f.write(f"{validation_notes}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("End of Evergreen Check Report\n")
            f.write("=" * 80 + "\n")

    async def create_csv_summary(self, evergreen_results: Dict[str, Any], file_path: Path):
        """Create a CSV summary of evergreen check results"""
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'Session ID',
                'Project Title',
                'Overall Status',
                'Total Issues',
                'Dated Reference Issues',
                'Universal Theme Issues',
                'Timeless Language Issues',
                'Cultural Universality Issues',
                'Future-Proofing Issues',
                'Timestamp'
            ])
            
            # Write summary row
            summary = evergreen_results.get('evergreen_check_summary', {})
            writer.writerow([
                self.session_id,
                evergreen_results.get('project_title', 'Unknown'),
                summary.get('overall_status', 'Unknown'),
                summary.get('total_issues_found', 0),
                summary.get('dated_reference_issues', 0),
                summary.get('universal_theme_issues', 0),
                summary.get('timeless_language_issues', 0),
                summary.get('cultural_universality_issues', 0),
                summary.get('future_proofing_issues', 0),
                evergreen_results.get('timestamp', 'Unknown')
            ])


async def main():
    """Main function for running Station 18"""
    print("🌿 Station 18: Evergreen Check")
    print("=" * 40)
    
    # Get session ID from user
    session_id = input("Enter session ID: ").strip()
    
    if not session_id:
        print("❌ Session ID is required")
        return
    
    # Create and run station
    station = Station18EvergreenCheck(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
