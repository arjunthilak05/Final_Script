"""
Station 20: Geography/Transit

This station validates geographical accuracy and transit realism in the story content.
It ensures that travel times are realistic, weather patterns are consistent, and all
location-based elements maintain consistency and believability for the audience.

Flow:
1. Load data from previous stations (1, 2, 3, 8, 15)
2. Extract required inputs from previous stations
3. Execute geography/transit validation:
   - Travel time realism (distance calculations, transportation methods, schedules)
   - Weather consistency (patterns, seasonal changes, climate accuracy)
   - Location consistency (geographical accuracy, local details, cultural appropriateness)
   - Geographical logic (logical placement, natural features, boundaries)
   - Audio geography (location-specific sounds, weather audio, transportation sounds)
4. Save comprehensive geography/transit validation results

Quality Control Agent - Output provides detailed geographical accuracy analysis and corrections
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


class Station20GeographyTransit:
    """Station 20: Geography/Transit Validator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=20)
        self.output_dir = Path("output/station_20")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🌍 STATION 20: GEOGRAPHY/TRANSIT")
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
                    "❌ CRITICAL ERROR: Cannot perform geography/transit validation. "
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

            # Execute geography/transit validation
            print("-" * 60)
            print("🌍 GEOGRAPHY/TRANSIT VALIDATION")
            print("-" * 60)
            print("Validating geographical accuracy and transit realism...")
            print()

            geography_transit_results = await self.execute_geography_transit_validation(extracted_inputs)

            # Save results
            await self.save_results(geography_transit_results)

            print("✅ Geography/Transit validation completed successfully!")
            print(f"📁 Results saved to: {self.output_dir}")

        except Exception as e:
            print(f"❌ Error in Station 20: {str(e)}")
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
            print(f"⚠️  File system data loading error: {e}")

        return station_data

    async def extract_required_inputs(self, station_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract required inputs from previous stations"""
        print("🔍 Extracting required inputs from previous stations...")

        extracted_inputs = {}

        # Extract from Station 1 (Seed Processor)
        if "station_1" in station_data:
            station_1 = station_data["station_1"]
            extracted_inputs["working_title"] = station_1.get("chosen_title", "Unknown")
            extracted_inputs["episode_count"] = station_1.get("option_details", {}).get("episode_count", "Unknown")
            extracted_inputs["episode_length"] = station_1.get("option_details", {}).get("episode_length", "Unknown")

        # Extract from Station 2 (Project DNA Builder)
        if "station_2" in station_data:
            station_2 = station_data["station_2"]
            extracted_inputs["primary_genre"] = station_2.get("genre_tone", {}).get("primary_genre", "Unknown")
            extracted_inputs["target_age"] = station_2.get("audience_profile", {}).get("primary_age_range", "Unknown")

        # Extract from Station 3 (Age/Genre Optimizer)
        if "station_3" in station_data:
            station_3 = station_data["station_3"]
            content_guidelines = station_3
            extracted_inputs["content_guidelines"] = json.dumps(content_guidelines, indent=2)

        # Extract from Station 8 (World Builder)
        if "station_8" in station_data:
            station_8 = station_data["station_8"]
            extracted_inputs["world_building"] = station_8

        # Extract from Station 15 (Detailed Episode Outlining)
        if "station_15" in station_data:
            station_15 = station_data["station_15"]
            extracted_inputs["detailed_outlines"] = station_15
            extracted_inputs["detailed_episode_outlines"] = json.dumps(station_15, indent=2)

        return extracted_inputs

    async def execute_geography_transit_validation(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute geography/transit validation using AI"""
        print("🤖 Executing geography/transit validation with AI...")

        # Prepare the prompt with extracted inputs
        prompt = self.config.get_prompt('main').format(
            working_title=inputs.get('working_title', 'Unknown'),
            primary_genre=inputs.get('primary_genre', 'Unknown'),
            target_age=inputs.get('target_age', 'Unknown'),
            episode_count=inputs.get('episode_count', 'Unknown'),
            episode_length=inputs.get('episode_length', 'Unknown'),
            content_guidelines=inputs.get('content_guidelines', '{}'),
            world_building=json.dumps(inputs.get('world_building', {}), indent=2),
            detailed_episode_outlines=inputs.get('detailed_episode_outlines', '{}')
        )

        try:
            # Get AI response
            response = await self.agent.process_message(
                user_input=prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON from response
            geography_transit_results = extract_json(response)
            
            # Validate the structure
            if not self.validate_geography_transit_structure(geography_transit_results):
                raise ValueError("Invalid geography/transit validation structure returned by AI")

            print("✅ Geography/transit validation completed")
            return geography_transit_results

        except Exception as e:
            print(f"❌ Error in geography/transit validation: {str(e)}")
            raise

    def validate_geography_transit_structure(self, data: Dict[str, Any]) -> bool:
        """Validate the structure of geography/transit validation results"""
        required_sections = [
            "geography_transit_summary",
            "travel_time_validation",
            "weather_consistency_validation",
            "location_consistency_validation",
            "geographical_logic_validation",
            "audio_geography_validation",
            "geography_recommendations",
            "geography_resources",
            "validation_notes"
        ]
        
        for section in required_sections:
            if section not in data:
                print(f"❌ Missing required section: {section}")
                return False
        
        return True

    async def save_results(self, geography_transit_results: Dict[str, Any]):
        """Save geography/transit validation results"""
        print("💾 Saving geography/transit validation results...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_file = self.output_dir / f"session_{self.session_id}_geography_transit_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(geography_transit_results, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON results saved: {json_file}")

        # Save readable report
        readable_file = self.output_dir / f"session_{self.session_id}_geography_transit_report.txt"
        readable_content = self.generate_readable_report(geography_transit_results)
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write(readable_content)
        print(f"✅ Readable report saved: {readable_file}")

        # Save CSV summary
        csv_file = self.output_dir / f"session_{self.session_id}_geography_transit_summary.csv"
        csv_content = self.generate_csv_summary(geography_transit_results)
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        print(f"✅ CSV summary saved: {csv_file}")

        # Store in Redis for future stations
        await self.redis_client.set(
            f"session:{self.session_id}:station:20:geography_transit_results",
            json.dumps(geography_transit_results)
        )
        print("✅ Results stored in Redis")

    def generate_readable_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable report"""
        report = []
        report.append("🌍 GEOGRAPHY/TRANSIT VALIDATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Summary
        summary = results.get("geography_transit_summary", {})
        report.append("📊 VALIDATION SUMMARY")
        report.append("-" * 30)
        report.append(f"Overall Status: {summary.get('overall_status', 'Unknown')}")
        report.append(f"Total Issues Found: {summary.get('total_issues_found', 0)}")
        report.append(f"Travel Time Issues: {summary.get('travel_time_issues', 0)}")
        report.append(f"Weather Consistency Issues: {summary.get('weather_consistency_issues', 0)}")
        report.append(f"Location Consistency Issues: {summary.get('location_consistency_issues', 0)}")
        report.append(f"Geographical Logic Issues: {summary.get('geographical_logic_issues', 0)}")
        report.append(f"Audio Geography Issues: {summary.get('audio_geography_issues', 0)}")
        report.append("")

        # Travel Time Validation
        travel_validation = results.get("travel_time_validation", {})
        if travel_validation.get("issues"):
            report.append("🚗 TRAVEL TIME VALIDATION ISSUES")
            report.append("-" * 40)
            for issue in travel_validation["issues"]:
                report.append(f"• {issue.get('description', 'No description')}")
                report.append(f"  Severity: {issue.get('severity', 'Unknown')}")
                report.append(f"  Location: {issue.get('location', 'Unknown')}")
                report.append(f"  Recommendation: {issue.get('recommendation', 'No recommendation')}")
                report.append("")

        # Weather Consistency Validation
        weather_validation = results.get("weather_consistency_validation", {})
        if weather_validation.get("issues"):
            report.append("🌤️ WEATHER CONSISTENCY VALIDATION ISSUES")
            report.append("-" * 45)
            for issue in weather_validation["issues"]:
                report.append(f"• {issue.get('description', 'No description')}")
                report.append(f"  Severity: {issue.get('severity', 'Unknown')}")
                report.append(f"  Location: {issue.get('location', 'Unknown')}")
                report.append(f"  Recommendation: {issue.get('recommendation', 'No recommendation')}")
                report.append("")

        # Location Consistency Validation
        location_validation = results.get("location_consistency_validation", {})
        if location_validation.get("issues"):
            report.append("📍 LOCATION CONSISTENCY VALIDATION ISSUES")
            report.append("-" * 45)
            for issue in location_validation["issues"]:
                report.append(f"• {issue.get('description', 'No description')}")
                report.append(f"  Severity: {issue.get('severity', 'Unknown')}")
                report.append(f"  Location: {issue.get('location_in_story', 'Unknown')}")
                report.append(f"  Recommendation: {issue.get('recommendation', 'No recommendation')}")
                report.append("")

        # Geographical Logic Validation
        geo_logic_validation = results.get("geographical_logic_validation", {})
        if geo_logic_validation.get("issues"):
            report.append("🗺️ GEOGRAPHICAL LOGIC VALIDATION ISSUES")
            report.append("-" * 45)
            for issue in geo_logic_validation["issues"]:
                report.append(f"• {issue.get('description', 'No description')}")
                report.append(f"  Severity: {issue.get('severity', 'Unknown')}")
                report.append(f"  Location: {issue.get('location', 'Unknown')}")
                report.append(f"  Recommendation: {issue.get('recommendation', 'No recommendation')}")
                report.append("")

        # Audio Geography Validation
        audio_geo_validation = results.get("audio_geography_validation", {})
        if audio_geo_validation.get("issues"):
            report.append("🎵 AUDIO GEOGRAPHY VALIDATION ISSUES")
            report.append("-" * 40)
            for issue in audio_geo_validation["issues"]:
                report.append(f"• {issue.get('description', 'No description')}")
                report.append(f"  Severity: {issue.get('severity', 'Unknown')}")
                report.append(f"  Location: {issue.get('location', 'Unknown')}")
                report.append(f"  Recommendation: {issue.get('recommendation', 'No recommendation')}")
                report.append("")

        # Recommendations
        recommendations = results.get("geography_recommendations", {})
        if recommendations.get("critical_fixes"):
            report.append("🔧 CRITICAL FIXES REQUIRED")
            report.append("-" * 30)
            for fix in recommendations["critical_fixes"]:
                report.append(f"• {fix}")
            report.append("")

        if recommendations.get("suggested_improvements"):
            report.append("💡 SUGGESTED IMPROVEMENTS")
            report.append("-" * 25)
            for improvement in recommendations["suggested_improvements"]:
                report.append(f"• {improvement}")
            report.append("")

        # Validation Notes
        validation_notes = results.get("validation_notes", "")
        if validation_notes:
            report.append("📝 VALIDATION NOTES")
            report.append("-" * 20)
            report.append(validation_notes)
            report.append("")

        return "\n".join(report)

    def generate_csv_summary(self, results: Dict[str, Any]) -> str:
        """Generate CSV summary"""
        csv_lines = []
        csv_lines.append("Issue_Type,Severity,Location,Description,Recommendation")
        
        # Travel Time Issues
        travel_issues = results.get("travel_time_validation", {}).get("issues", [])
        for issue in travel_issues:
            csv_lines.append(f"Travel Time,{issue.get('severity', 'Unknown')},{issue.get('location', 'Unknown')},\"{issue.get('description', 'No description')}\",\"{issue.get('recommendation', 'No recommendation')}\"")

        # Weather Consistency Issues
        weather_issues = results.get("weather_consistency_validation", {}).get("issues", [])
        for issue in weather_issues:
            csv_lines.append(f"Weather Consistency,{issue.get('severity', 'Unknown')},{issue.get('location', 'Unknown')},\"{issue.get('description', 'No description')}\",\"{issue.get('recommendation', 'No recommendation')}\"")

        # Location Consistency Issues
        location_issues = results.get("location_consistency_validation", {}).get("issues", [])
        for issue in location_issues:
            csv_lines.append(f"Location Consistency,{issue.get('severity', 'Unknown')},{issue.get('location_in_story', 'Unknown')},\"{issue.get('description', 'No description')}\",\"{issue.get('recommendation', 'No recommendation')}\"")

        # Geographical Logic Issues
        geo_logic_issues = results.get("geographical_logic_validation", {}).get("issues", [])
        for issue in geo_logic_issues:
            csv_lines.append(f"Geographical Logic,{issue.get('severity', 'Unknown')},{issue.get('location', 'Unknown')},\"{issue.get('description', 'No description')}\",\"{issue.get('recommendation', 'No recommendation')}\"")

        # Audio Geography Issues
        audio_geo_issues = results.get("audio_geography_validation", {}).get("issues", [])
        for issue in audio_geo_issues:
            csv_lines.append(f"Audio Geography,{issue.get('severity', 'Unknown')},{issue.get('location', 'Unknown')},\"{issue.get('description', 'No description')}\",\"{issue.get('recommendation', 'No recommendation')}\"")

        return "\n".join(csv_lines)


async def main():
    """Main execution function"""
    print("🌍 Station 20: Geography/Transit Validator")
    print("=" * 50)
    
    # Get session ID from user
    session_id = input("Enter session ID: ").strip()
    
    if not session_id:
        print("❌ Session ID is required!")
        return
    
    # Initialize and run station
    station = Station20GeographyTransit(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
