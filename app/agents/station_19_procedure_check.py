"""
Station 19: Procedure Check

This station validates legal/medical accuracy and realistic timelines in the story content.
It ensures that any procedures, legal processes, medical situations, or professional scenarios
depicted in the story are accurate and believable, maintaining credibility for the audience.

Flow:
1. Load data from previous stations (1, 2, 3, 7, 8, 15)
2. Extract required inputs from previous stations
3. Execute procedure validation:
   - Legal/procedural accuracy (court proceedings, police procedures, legal rights)
   - Medical accuracy (injuries, treatments, recovery times, medical terminology)
   - Professional accuracy (job procedures, workplace protocols, industry standards)
   - Timeline realism (procedure durations, recovery periods, legal processes)
   - Technical accuracy (specialized knowledge, expert language)
4. Save comprehensive procedure check results

Quality Control Agent - Output provides detailed accuracy analysis and corrections
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


class Station19ProcedureCheck:
    """Station 19: Procedure Check and Accuracy Validator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=19)
        self.output_dir = Path("output/station_19")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("⚖️  STATION 19: PROCEDURE CHECK")
        print("=" * 60)
        print()

        try:
            # Load data from previous stations
            station_data = await self.load_previous_stations_data()

            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs(station_data)

            # --- START CRITICAL VALIDATION ---
            working_title = extracted_inputs.get('working_title', 'Unknown')
            primary_genre = extracted_inputs.get('primary_genre', 'Unknown')
            world_building = extracted_inputs.get('world_building', {})
            detailed_outlines = extracted_inputs.get('detailed_outlines', {})

            if working_title == 'Unknown' or primary_genre == 'Unknown' or not world_building or not detailed_outlines:
                error_msg = (
                    "❌ CRITICAL ERROR: Cannot perform procedure check. "
                    f"Missing required data: Working Title ('{working_title}'), "
                    f"Primary Genre ('{primary_genre}'), "
                    f"World Building ({bool(world_building)}), "
                    f"Detailed Outlines ({bool(detailed_outlines)}). "
                    "This data is expected from previous stations."
                )
                print(error_msg)
                raise ValueError(error_msg)

            print("✅ Critical data validated (Working Title, Genre, World Building, Detailed Outlines)")
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
            print()

            # Execute procedure check
            print("-" * 60)
            print("⚖️  EXECUTING PROCEDURE CHECK")
            print("-" * 60)
            print("Checking for:")
            print("• Legal/procedural accuracy")
            print("• Medical accuracy and realistic recovery times")
            print("• Professional accuracy and workplace protocols")
            print("• Timeline realism for procedures and processes")
            print("• Technical accuracy and specialized knowledge")
            print()

            procedure_results = await self.execute_procedure_check(extracted_inputs)

            print("✅ Procedure check completed")
            print()

            # Save results
            await self.save_results(procedure_results)

            print("✅ Results saved successfully")
            print()
            print("=" * 60)
            print("🎯 PROCEDURE CHECK COMPLETE")
            print("=" * 60)
            print(f"Session ID: {self.session_id}")
            print(f"Overall Status: {procedure_results.get('procedure_check_summary', {}).get('overall_status', 'Unknown')}")
            print(f"Total Issues Found: {procedure_results.get('procedure_check_summary', {}).get('total_issues_found', 0)}")
            print()
            print("📁 Output Files:")
            session_id_clean = self.session_id.replace("session_", "") if self.session_id.startswith("session_") else self.session_id
            print(f"• JSON: output/station_19/session_{session_id_clean}_procedure_check_results.json")
            print(f"• Report: output/station_19/session_{session_id_clean}_procedure_check_report.txt")
            print(f"• Summary: output/station_19/session_{session_id_clean}_procedure_check_summary.csv")

        except Exception as e:
            print(f"❌ Error in Station 19: {str(e)}")
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

        extracted = {}

        # Extract from Station 1 (Seed Processor)
        if 'station_1' in station_data:
            station_1_data = station_data['station_1']
            extracted['working_title'] = station_1_data.get('chosen_title', 'Unknown')
            extracted['episode_count'] = station_1_data.get('option_details', {}).get('episode_count', 'Unknown')
            extracted['episode_length'] = station_1_data.get('option_details', {}).get('episode_length', 'Unknown')
            print(f"✅ Station 1 extracted: title={extracted['working_title']}")

        # Extract from Station 2 (Project DNA Builder)
        if 'station_2' in station_data:
            station_2_data = station_data['station_2']
            extracted['primary_genre'] = station_2_data.get('genre_tone', {}).get('primary_genre', 'Unknown')
            extracted['target_age'] = station_2_data.get('target_age', 'Unknown')
            print(f"✅ Station 2 extracted: primary_genre={extracted['primary_genre']}")
        else:
            print("❌ Station 2 data not found")

        # Extract from Station 3 (Age & Genre Optimizer)
        if 'station_3' in station_data:
            station_3_data = station_data['station_3']
            if 'Age/Genre Style Guide' in station_3_data:
                style_guide = station_3_data['Age/Genre Style Guide']
                extracted['content_guidelines'] = style_guide.get('age_appropriate_modifications', {})

        # Extract Character Bible from Station 7
        if 'station_7' in station_data:
            station_7_data = station_data['station_7']
            if 'Character Bible Document' in station_7_data:
                doc_data = station_7_data['Character Bible Document']
                extracted['character_bible'] = doc_data.get('character_bible', {})

        # Extract World Building from Station 8
        if 'station_8' in station_data:
            station_8_data = station_data['station_8']
            if 'World Bible Document' in station_8_data:
                doc_data = station_8_data['World Bible Document']
                extracted['world_building'] = doc_data.get('world_bible', {})

        # Extract Detailed Episode Outlines from Station 15
        if 'station_15' in station_data:
            station_15_data = station_data['station_15']
            if 'outline_data' in station_15_data:
                outline_data = station_15_data['outline_data']
                extracted['detailed_outlines'] = outline_data.get('detailed_episode_outlines', {})

        return extracted

    async def execute_procedure_check(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the procedure check using AI"""
        print("🤖 Executing procedure check with AI...")

        # Prepare the prompt
        prompt = self.config.get_prompt('main').format(
            working_title=inputs.get('working_title', 'Unknown'),
            primary_genre=inputs.get('primary_genre', 'Unknown'),
            target_age=inputs.get('target_age', 'Unknown'),
            episode_count=inputs.get('episode_count', 'Unknown'),
            episode_length=inputs.get('episode_length', 'Unknown'),
            content_guidelines=json.dumps(inputs.get('content_guidelines', {}), indent=2),
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
        procedure_results = extract_json(response)

        if not procedure_results:
            raise ValueError("Failed to extract valid JSON from AI response")

        return procedure_results

    async def save_results(self, procedure_results: Dict[str, Any]):
        """Save procedure check results to files"""
        print("💾 Saving procedure check results...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON results - handle session_id that may already include "session_" prefix
        session_id_clean = self.session_id.replace("session_", "") if self.session_id.startswith("session_") else self.session_id
        json_file = self.output_dir / f"session_{session_id_clean}_procedure_check_results.json"
        procedure_results['session_id'] = self.session_id
        procedure_results['timestamp'] = timestamp
        procedure_results['project_title'] = procedure_results.get('working_title', 'Unknown')

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(procedure_results, f, indent=2, ensure_ascii=False)

        # Save readable report
        readable_file = self.output_dir / f"session_{session_id_clean}_procedure_check_report.txt"
        await self.create_readable_report(procedure_results, readable_file)

        # Save CSV summary
        csv_file = self.output_dir / f"session_{session_id_clean}_procedure_check_summary.csv"
        await self.create_csv_summary(procedure_results, csv_file)

    async def create_readable_report(self, procedure_results: Dict[str, Any], file_path: Path):
        """Create a human-readable report"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("⚖️  PROCEDURE CHECK REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Timestamp: {procedure_results.get('timestamp', 'Unknown')}\n")
            f.write(f"Project Title: {procedure_results.get('project_title', 'Unknown')}\n\n")

            # Summary
            summary = procedure_results.get('procedure_check_summary', {})
            f.write("📊 PROCEDURE CHECK SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Overall Status: {summary.get('overall_status', 'Unknown')}\n")
            f.write(f"Total Issues Found: {summary.get('total_issues_found', 0)}\n")
            f.write(f"Legal/Procedural Issues: {summary.get('legal_procedural_issues', 0)}\n")
            f.write(f"Medical Accuracy Issues: {summary.get('medical_accuracy_issues', 0)}\n")
            f.write(f"Professional Accuracy Issues: {summary.get('professional_accuracy_issues', 0)}\n")
            f.write(f"Timeline Realism Issues: {summary.get('timeline_realism_issues', 0)}\n")
            f.write(f"Technical Accuracy Issues: {summary.get('technical_accuracy_issues', 0)}\n\n")

            # Legal/Procedural Check
            legal_check = procedure_results.get('legal_procedural_check', {})
            f.write("⚖️  LEGAL/PROCEDURAL CHECK\n")
            f.write("-" * 40 + "\n")
            f.write(f"Status: {legal_check.get('status', 'Unknown')}\n")
            issues = legal_check.get('issues', [])
            if issues:
                f.write(f"Issues Found: {len(issues)}\n")
                for i, issue in enumerate(issues, 1):
                    f.write(f"\n{i}. {issue.get('issue_type', 'Unknown Issue')}\n")
                    f.write(f"   Description: {issue.get('description', 'No description')}\n")
                    f.write(f"   Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"   Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"   Current Depiction: {issue.get('current_depiction', 'N/A')}\n")
                    f.write(f"   Accurate Alternative: {issue.get('accurate_alternative', 'N/A')}\n")
                    f.write(f"   Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("✅ No legal/procedural issues found\n")
            f.write("\n")

            # Medical Accuracy Check
            medical_check = procedure_results.get('medical_accuracy_check', {})
            f.write("🏥 MEDICAL ACCURACY CHECK\n")
            f.write("-" * 40 + "\n")
            f.write(f"Status: {medical_check.get('status', 'Unknown')}\n")
            issues = medical_check.get('issues', [])
            if issues:
                f.write(f"Issues Found: {len(issues)}\n")
                for i, issue in enumerate(issues, 1):
                    f.write(f"\n{i}. {issue.get('issue_type', 'Unknown Issue')}\n")
                    f.write(f"   Description: {issue.get('description', 'No description')}\n")
                    f.write(f"   Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"   Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"   Current Depiction: {issue.get('current_depiction', 'N/A')}\n")
                    f.write(f"   Accurate Alternative: {issue.get('accurate_alternative', 'N/A')}\n")
                    f.write(f"   Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("✅ No medical accuracy issues found\n")
            f.write("\n")

            # Professional Accuracy Check
            professional_check = procedure_results.get('professional_accuracy_check', {})
            f.write("💼 PROFESSIONAL ACCURACY CHECK\n")
            f.write("-" * 40 + "\n")
            f.write(f"Status: {professional_check.get('status', 'Unknown')}\n")
            issues = professional_check.get('issues', [])
            if issues:
                f.write(f"Issues Found: {len(issues)}\n")
                for i, issue in enumerate(issues, 1):
                    f.write(f"\n{i}. {issue.get('issue_type', 'Unknown Issue')}\n")
                    f.write(f"   Description: {issue.get('description', 'No description')}\n")
                    f.write(f"   Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"   Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"   Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("✅ No professional accuracy issues found\n")
            f.write("\n")

            # Timeline Realism Check
            timeline_check = procedure_results.get('timeline_realism_check', {})
            f.write("⏰ TIMELINE REALISM CHECK\n")
            f.write("-" * 40 + "\n")
            f.write(f"Status: {timeline_check.get('status', 'Unknown')}\n")
            issues = timeline_check.get('issues', [])
            if issues:
                f.write(f"Issues Found: {len(issues)}\n")
                for i, issue in enumerate(issues, 1):
                    f.write(f"\n{i}. {issue.get('issue_type', 'Unknown Issue')}\n")
                    f.write(f"   Description: {issue.get('description', 'No description')}\n")
                    f.write(f"   Severity: {issue.get('severity', 'Unknown')}\n")
                    f.write(f"   Location: {issue.get('location', 'Unknown')}\n")
                    f.write(f"   Current Timeline: {issue.get('current_timeline', 'N/A')}\n")
                    f.write(f"   Realistic Timeline: {issue.get('realistic_timeline', 'N/A')}\n")
                    f.write(f"   Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
            else:
                f.write("✅ No timeline realism issues found\n")
            f.write("\n")

            # Recommendations
            recommendations = procedure_results.get('procedure_recommendations', {})
            f.write("💡 RECOMMENDATIONS\n")
            f.write("-" * 40 + "\n")

            critical_fixes = recommendations.get('critical_fixes', [])
            if critical_fixes:
                f.write("🚨 CRITICAL FIXES:\n")
                for i, fix in enumerate(critical_fixes, 1):
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
            validation_notes = procedure_results.get('validation_notes', '')
            if validation_notes:
                f.write("📋 VALIDATION NOTES\n")
                f.write("-" * 40 + "\n")
                f.write(f"{validation_notes}\n\n")

            f.write("=" * 80 + "\n")
            f.write("End of Procedure Check Report\n")
            f.write("=" * 80 + "\n")

    async def create_csv_summary(self, procedure_results: Dict[str, Any], file_path: Path):
        """Create a CSV summary of procedure check results"""
        import csv

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow([
                'Session ID',
                'Project Title',
                'Overall Status',
                'Total Issues',
                'Legal/Procedural Issues',
                'Medical Accuracy Issues',
                'Professional Accuracy Issues',
                'Timeline Realism Issues',
                'Technical Accuracy Issues',
                'Timestamp'
            ])

            # Write summary row
            summary = procedure_results.get('procedure_check_summary', {})
            writer.writerow([
                self.session_id,
                procedure_results.get('project_title', 'Unknown'),
                summary.get('overall_status', 'Unknown'),
                summary.get('total_issues_found', 0),
                summary.get('legal_procedural_issues', 0),
                summary.get('medical_accuracy_issues', 0),
                summary.get('professional_accuracy_issues', 0),
                summary.get('timeline_realism_issues', 0),
                summary.get('technical_accuracy_issues', 0),
                procedure_results.get('timestamp', 'Unknown')
            ])


async def main():
    """Main function for running Station 19"""
    print("⚖️  Station 19: Procedure Check")
    print("=" * 40)

    # Get session ID from user
    session_id = input("Enter session ID: ").strip()

    if not session_id:
        print("❌ Session ID is required")
        return

    # Create and run station
    station = Station19ProcedureCheck(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
