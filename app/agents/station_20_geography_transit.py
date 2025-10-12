"""
Station 20: Geography & Transit Agent

This agent validates geographic consistency, realistic travel times, weather patterns,
and temporal consistency across the audiobook series.

Dependencies: Stations 9, 11, 14, 15
Outputs: Geography/transit validation report (TXT, JSON)
Human Gate: None - validation gate before script writing
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient

# Configure logging
logger = logging.getLogger(__name__)


class Station20GeographyTransit:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_20_geography_transit"

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()

    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from previous stations"""
        dependencies = {}

        # Load stations with geographic/temporal content
        station_keys = {
            'station_09': 'world_bible',
            'station_11': 'runtime_planning',
            'station_14': 'episode_blueprints',
            'station_15': 'detailed_outlines'
        }

        for redis_key, dependency_name in station_keys.items():
            raw_data = await self.redis_client.get(f"audiobook:{self.session_id}:{redis_key}")
            if raw_data:
                dependencies[dependency_name] = json.loads(raw_data)

        return dependencies

    async def validate_location_network(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate location relationships and travel distances using LLM"""

        world_bible = dependencies.get('world_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Actually load locations from Station 9
        locations = world_bible.get('locations', []) if world_bible else []
        geography = world_bible.get('geography', {})
        
        if not locations and isinstance(geography, dict):
            # Try to get locations from geography dict
            locations = geography.get('locations', [])
        
        if not locations:
            logger.warning("No locations found in Station 9")
            return {
                'total_locations': 0,
                'location_pairs_analyzed': 0,
                'location_pairs': [],
                'geographic_consistency_score': 0
            }

        # Extract location information
        if isinstance(locations, list):
            location_names = [loc.get('name', 'Unknown') if isinstance(loc, dict) else str(loc) for loc in locations]
            geography_sample = locations[:10]  # Sample first 10 locations
        else:
            location_names = []
            geography_sample = []

        locations_summary = json.dumps({
            'locations': geography_sample,
            'location_names': location_names,
            'total_locations': len(locations)
        }, indent=2)[:3000]

        # Safely extract episodes
        blueprints_episodes = episode_blueprints.get('episodes', [])
        if isinstance(blueprints_episodes, list):
            blueprints_sample = blueprints_episodes[:5]
        else:
            blueprints_sample = []

        outlines_episodes = detailed_outlines.get('episodes', [])
        if isinstance(outlines_episodes, list):
            outlines_sample = outlines_episodes[:3]
        else:
            outlines_sample = []

        episodes_summary = json.dumps({
            'blueprints': blueprints_sample,
            'outlines': outlines_sample
        }, indent=2)[:4000]

        prompt = f"""
You are a Geographic Consistency Validator analyzing location relationships and distances.

WORLD GEOGRAPHY (Station 9):
{locations_summary}

EPISODE CONTENT (Stations 14-15):
{episodes_summary}

Analyze LOCATION NETWORK and GEOGRAPHIC CONSISTENCY:

1. LOCATION PAIRS:
   For every pair of locations that characters travel between:
   - From/To locations
   - Estimated distance (if world building provides info)
   - Travel methods mentioned in episodes
   - Stated travel times in story
   - Realistic travel times for each method:
     * Walking: ~3-4 mph (5-6 km/h)
     * Driving: ~30-60 mph depending on roads (50-100 km/h)
     * Flying: ~500 mph average (800 km/h)
     * Public transit: Varies by type and location
   - Consistency issues: Do travel times match across episodes?

2. GEOGRAPHIC RELATIONSHIPS:
   - Relative positions consistent? (A is north of B, B is west of C)
   - Distance mentions consistent?
   - Can characters realistically travel stated distances in stated times?
   - Are geographic barriers (mountains, rivers, oceans) accounted for?

3. LOCATION ACCESSIBILITY:
   - Are some locations harder to reach? Is this consistent?
   - Transportation infrastructure mentioned?
   - Seasonal accessibility (if applicable)?

Generate detailed analysis of location network with specific travel validations.

Expected JSON format:
{{
  "total_locations": 8,
  "location_pairs_analyzed": 12,
  "location_pairs": [
    {{
      "from": "City A",
      "to": "City B",
      "estimated_distance": "50 miles",
      "travel_methods_mentioned": ["driving", "bus"],
      "stated_travel_times": ["45 minutes in Episode 3", "1 hour in Episode 7"],
      "realistic_travel_times": {{
        "walking": "16-17 hours",
        "driving": "50-60 minutes",
        "flying": "Not applicable for short distance",
        "public_transit": "1-1.5 hours"
      }},
      "consistency_issues": [
        "Travel time varies between episodes without explanation"
      ]
    }}
  ],
  "geographic_consistency_score": 85
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'total_locations': 0,
            'location_pairs_analyzed': 0,
            'location_pairs': [],
            'geographic_consistency_score': 0
        })

    async def validate_weather_continuity(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate weather patterns and seasonal consistency using LLM"""

        world_bible = dependencies.get('world_bible', {})
        runtime_planning = dependencies.get('runtime_planning', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract geography
        geography = world_bible.get('geography', [])
        if isinstance(geography, list):
            geography_sample = geography[:3]
        else:
            geography_sample = []

        world_summary = json.dumps({
            'geography': geography_sample,
            'climate_info': 'Extract from world building'
        }, indent=2)[:2000]

        # Safely extract episode breakdowns
        episode_breakdowns = runtime_planning.get('episode_breakdowns', [])
        if isinstance(episode_breakdowns, list):
            breakdowns_sample = episode_breakdowns[:5]
        else:
            breakdowns_sample = []

        timeline_summary = json.dumps({
            'timeline': runtime_planning.get('timeline', {}),
            'episode_breakdowns': breakdowns_sample
        }, indent=2)[:2000]

        # Safely extract episodes
        blueprints_episodes = episode_blueprints.get('episodes', [])
        if isinstance(blueprints_episodes, list):
            blueprints_sample = blueprints_episodes
        else:
            blueprints_sample = []

        outlines_episodes = detailed_outlines.get('episodes', [])
        if isinstance(outlines_episodes, list):
            outlines_sample = outlines_episodes[:5]
        else:
            outlines_sample = []

        episodes_summary = json.dumps({
            'blueprints': blueprints_sample,
            'outlines': outlines_sample
        }, indent=2)[:4000]

        prompt = f"""
You are a Weather & Climate Consistency Validator analyzing environmental continuity.

WORLD GEOGRAPHY & CLIMATE:
{world_summary}

TIMELINE (Station 11):
{timeline_summary}

EPISODE CONTENT:
{episodes_summary}

Analyze WEATHER CONTINUITY and SEASONAL CONSISTENCY:

1. EPISODE-BY-EPISODE WEATHER:
   For each episode, analyze:
   - What season is it? (if determinable from timeline)
   - What weather is described or implied?
   - Is weather consistent with:
     * Stated or implied season?
     * Geographic location?
     * Previous episode weather?
     * Timeline progression?

2. SEASONAL PROGRESSION:
   - Does time passage match seasonal changes?
   - Are seasonal transitions shown appropriately?
   - Do weather patterns follow logical progression?
   - Are there any impossible seasonal jumps?

3. GEOGRAPHIC WEATHER LOGIC:
   - Different locations have appropriate climates?
   - Weather differences between locations make sense?
   - Climate zones consistent with geography?

4. WEATHER IMPACT:
   - Does weather affect travel/activities as expected?
   - Are weather conditions realistic for location/season?
   - Any weather-related plot elements consistent?

For EACH consistency issue:
- Episode number
- Season (if known)
- Weather described
- Consistency_with_timeline: "consistent" or "inconsistent"
- Issues: List of problems
- Recommended_fix

Generate detailed weather continuity analysis.

Expected JSON format:
{{
  "episodes_analyzed": 10,
  "weather_continuity": [
    {{
      "episode": 3,
      "season": "winter",
      "weather_described": "Warm sunny day, characters in t-shirts",
      "consistency_with_timeline": "inconsistent",
      "issues": [
        "Winter setting but summer weather described",
        "Clothing inappropriate for stated season"
      ],
      "recommended_fix": "Change to cold winter day or adjust season"
    }}
  ],
  "seasonal_progression_score": 82,
  "weather_logic_score": 88
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'episodes_analyzed': 0,
            'weather_continuity': [],
            'seasonal_progression_score': 0,
            'weather_logic_score': 0
        })

    async def validate_temporal_consistency(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate day/night cycles, time zones, and temporal logic using LLM"""

        runtime_planning = dependencies.get('runtime_planning', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract episode breakdowns
        episode_breakdowns = runtime_planning.get('episode_breakdowns', [])
        if isinstance(episode_breakdowns, list):
            breakdowns_sample = episode_breakdowns
        else:
            breakdowns_sample = []

        timeline_summary = json.dumps({
            'timeline': runtime_planning.get('timeline', {}),
            'episode_breakdowns': breakdowns_sample
        }, indent=2)[:2000]

        # Safely extract episodes
        blueprints_episodes = episode_blueprints.get('episodes', [])
        if isinstance(blueprints_episodes, list):
            blueprints_sample = blueprints_episodes
        else:
            blueprints_sample = []

        outlines_episodes = detailed_outlines.get('episodes', [])
        if isinstance(outlines_episodes, list):
            outlines_sample = outlines_episodes[:5]
        else:
            outlines_sample = []

        episodes_summary = json.dumps({
            'blueprints': blueprints_sample,
            'outlines': outlines_sample
        }, indent=2)[:5000]

        prompt = f"""
You are a Temporal Logic Validator analyzing time-based consistency.

TIMELINE (Station 11):
{timeline_summary}

EPISODE CONTENT:
{episodes_summary}

Analyze TEMPORAL CONSISTENCY:

1. DAY/NIGHT CYCLES:
   - Are day/night cycles realistic for location/season?
   - Do time references within episodes make sense?
   - Daylight hours appropriate for season/location?
   - Sunrise/sunset timing logical?

2. TIME PASSAGE WITHIN EPISODES:
   - Can stated events fit in stated timeframes?
   - Time references consistent throughout episode?
   - Meal times/daily routines logical?
   - Clock time mentions consistent?

3. TIME ZONES (if multiple locations):
   - Time zone differences accounted for?
   - International travel time changes shown?
   - Communication timing across zones realistic?

4. TEMPORAL IMPOSSIBILITIES:
   - Any impossible timelines? (e.g., two things happening "now" in different locations)
   - Characters in two places at impossible times?
   - Time-of-day inconsistencies?

For EACH temporal issue:
- Issue type: "day_night", "time_passage", "time_zone", "impossibility"
- Description: What's wrong
- Location: Episodes affected
- Severity: "critical", "moderate", "minor"
- Recommended_fix

Generate detailed temporal consistency analysis.

Expected JSON format:
{{
  "day_night_cycles": "realistic",
  "time_zone_handling": "correct",
  "seasonal_progression": "logical",
  "temporal_issues": [
    {{
      "issue_type": "time_passage",
      "description": "Character travels 100 miles and attends 3-hour meeting, all stated as happening in 2 hours",
      "episodes": [5],
      "severity": "critical",
      "recommended_fix": "Extend timeline to 4-5 hours minimum"
    }}
  ],
  "temporal_consistency_score": 78
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'day_night_cycles': 'unknown',
            'time_zone_handling': 'unknown',
            'seasonal_progression': 'unknown',
            'temporal_issues': [],
            'temporal_consistency_score': 0
        })

    async def calculate_transit_realism(self, dependencies: Dict) -> Dict[str, Any]:
        """Calculate overall transit realism score using LLM"""

        world_bible = dependencies.get('world_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract geography
        geography = world_bible.get('geography', [])
        if isinstance(geography, list):
            geography_sample = geography[:3]
        else:
            geography_sample = []

        # Safely extract episodes
        blueprints_episodes = episode_blueprints.get('episodes', [])
        if isinstance(blueprints_episodes, list):
            blueprints_sample = blueprints_episodes[:5]
        else:
            blueprints_sample = []

        outlines_episodes = detailed_outlines.get('episodes', [])
        if isinstance(outlines_episodes, list):
            outlines_sample = outlines_episodes[:3]
        else:
            outlines_sample = []

        all_content = json.dumps({
            'world': geography_sample,
            'episodes': blueprints_sample,
            'outlines': outlines_sample
        }, indent=2)[:5000]

        prompt = f"""
You are a Transit Realism Evaluator providing overall assessment of travel logic.

ALL RELEVANT CONTENT:
{all_content}

Provide COMPREHENSIVE TRANSIT REALISM EVALUATION:

1. OVERALL ASSESSMENT:
   - How realistic are travel times overall?
   - Are distances and geography handled well?
   - Does transit make sense for the world?

2. STRENGTHS:
   - What geographic/travel elements are handled well?
   - Good attention to detail in which areas?
   - Realistic elements to maintain?

3. WEAKNESSES:
   - What needs improvement?
   - Common issues across episodes?
   - Patterns of unrealistic transit?

4. RECOMMENDATIONS:
   - Specific fixes for main issues
   - General improvements for transit realism
   - Areas requiring more detail

5. SCORES:
   - Geography consistency: 0-100
   - Transit time realism: 0-100
   - Weather/climate logic: 0-100
   - Temporal consistency: 0-100
   - Overall geography score: 0-100

Generate comprehensive transit realism report.

Expected JSON format:
{{
  "geography_score": 85,
  "transit_realism_score": 78,
  "weather_climate_score": 90,
  "temporal_score": 82,
  "overall_score": 84,
  "strengths": [
    "Strong geographic consistency",
    "Weather well-integrated"
  ],
  "weaknesses": [
    "Some travel times too compressed",
    "Time zone handling needs work"
  ],
  "recommendations": [
    "Add 20% to stated travel times",
    "Review Episodes 3 and 7 for time zone accuracy"
  ]
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'geography_score': 0,
            'transit_realism_score': 0,
            'weather_climate_score': 0,
            'temporal_score': 0,
            'overall_score': 0,
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        })

    def _parse_json_response(self, response: str, fallback: Any) -> Any:
        """Parse JSON response with fallback"""
        try:
            return json.loads(response)
        except:
            # Try to extract JSON from response text
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
            return fallback

    def export_txt(self, geography_report: Dict, filepath: str):
        """Export human-readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("STATION 20: GEOGRAPHY & TRANSIT VALIDATION REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Validation Status: {geography_report.get('validation_status', 'UNKNOWN')}\n")
            f.write(f"Overall Geography Score: {geography_report.get('geography_score', 0)}/100\n\n")

            # Summary Scores
            f.write("VALIDATION SCORES\n")
            f.write("-"*70 + "\n")
            realism = geography_report.get('transit_realism', {})
            f.write(f"Geography Consistency: {realism.get('geography_score', 0)}/100\n")
            f.write(f"Transit Time Realism: {realism.get('transit_realism_score', 0)}/100\n")
            f.write(f"Weather/Climate Logic: {realism.get('weather_climate_score', 0)}/100\n")
            f.write(f"Temporal Consistency: {realism.get('temporal_score', 0)}/100\n")
            f.write(f"Overall Score: {realism.get('overall_score', 0)}/100\n\n")

            # Location Network Analysis
            location_network = geography_report.get('location_network', {})
            if location_network.get('location_pairs'):
                f.write("\n" + "="*70 + "\n")
                f.write("LOCATION NETWORK ANALYSIS\n")
                f.write("="*70 + "\n\n")
                f.write(f"Total Locations: {location_network.get('total_locations', 0)}\n")
                f.write(f"Location Pairs Analyzed: {location_network.get('location_pairs_analyzed', 0)}\n\n")

                for pair in location_network.get('location_pairs', [])[:10]:  # Limit to first 10
                    f.write(f"FROM: {pair.get('from', 'N/A')} → TO: {pair.get('to', 'N/A')}\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Distance: {pair.get('estimated_distance', 'Not specified')}\n")

                    if pair.get('realistic_travel_times'):
                        f.write("Realistic Travel Times:\n")
                        times = pair.get('realistic_travel_times', {})
                        for method, time in times.items():
                            f.write(f"  • {method.title()}: {time}\n")

                    if pair.get('stated_travel_times'):
                        f.write(f"Story States: {', '.join(pair.get('stated_travel_times', []))}\n")

                    if pair.get('consistency_issues'):
                        f.write("Issues:\n")
                        for issue in pair.get('consistency_issues', []):
                            f.write(f"  ⚠️  {issue}\n")

                    f.write("\n")

            # Weather Continuity
            weather = geography_report.get('weather_continuity', {})
            if weather.get('weather_continuity'):
                f.write("\n" + "="*70 + "\n")
                f.write("WEATHER & SEASONAL CONSISTENCY\n")
                f.write("="*70 + "\n\n")
                f.write(f"Seasonal Progression: {weather.get('seasonal_progression_score', 0)}/100\n")
                f.write(f"Weather Logic: {weather.get('weather_logic_score', 0)}/100\n\n")

                for weather_issue in weather.get('weather_continuity', []):
                    if weather_issue.get('consistency_with_timeline') == 'inconsistent':
                        f.write(f"EPISODE {weather_issue.get('episode', 'N/A')}\n")
                        f.write("-"*70 + "\n")
                        f.write(f"Season: {weather_issue.get('season', 'N/A')}\n")
                        f.write(f"Described: {weather_issue.get('weather_described', 'N/A')}\n")
                        f.write(f"Issues:\n")
                        for issue in weather_issue.get('issues', []):
                            f.write(f"  ⚠️  {issue}\n")
                        f.write(f"Fix: {weather_issue.get('recommended_fix', 'N/A')}\n\n")

            # Temporal Consistency
            temporal = geography_report.get('temporal_consistency', {})
            if temporal.get('temporal_issues'):
                f.write("\n" + "="*70 + "\n")
                f.write("TEMPORAL CONSISTENCY ANALYSIS\n")
                f.write("="*70 + "\n\n")
                f.write(f"Day/Night Cycles: {temporal.get('day_night_cycles', 'N/A')}\n")
                f.write(f"Time Zone Handling: {temporal.get('time_zone_handling', 'N/A')}\n")
                f.write(f"Seasonal Progression: {temporal.get('seasonal_progression', 'N/A')}\n")
                f.write(f"Temporal Score: {temporal.get('temporal_consistency_score', 0)}/100\n\n")

                for issue in temporal.get('temporal_issues', []):
                    severity_label = {
                        'critical': '🔴 CRITICAL',
                        'moderate': '🟠 MODERATE',
                        'minor': '🟡 MINOR'
                    }.get(issue.get('severity', 'minor'), issue.get('severity', 'UNKNOWN'))

                    f.write(f"{severity_label}: {issue.get('issue_type', 'unknown').upper()}\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Description: {issue.get('description', 'N/A')}\n")
                    f.write(f"Episodes: {', '.join(map(str, issue.get('episodes', [])))}\n")
                    f.write(f"Fix: {issue.get('recommended_fix', 'N/A')}\n\n")

            # Strengths and Weaknesses
            f.write("\n" + "="*70 + "\n")
            f.write("OVERALL ASSESSMENT\n")
            f.write("="*70 + "\n\n")

            if realism.get('strengths'):
                f.write("STRENGTHS:\n")
                for strength in realism.get('strengths', []):
                    f.write(f"  ✓ {strength}\n")
                f.write("\n")

            if realism.get('weaknesses'):
                f.write("AREAS FOR IMPROVEMENT:\n")
                for weakness in realism.get('weaknesses', []):
                    f.write(f"  • {weakness}\n")
                f.write("\n")

            if realism.get('recommendations'):
                f.write("RECOMMENDATIONS:\n")
                for rec in realism.get('recommendations', []):
                    f.write(f"  → {rec}\n")
                f.write("\n")

            # Final Assessment
            f.write("\n" + "="*70 + "\n")
            f.write("FINAL ASSESSMENT\n")
            f.write("="*70 + "\n\n")

            status = geography_report.get('validation_status', 'UNKNOWN')
            score = geography_report.get('geography_score', 0)

            if status == 'PASS':
                f.write("✅ VALIDATION PASSED\n")
                f.write(f"Geography and transit are realistic (Score: {score}/100).\n")
                f.write("Ready to proceed to script writing.\n")
            elif status == 'WARNING':
                f.write("⚠️  VALIDATION PASSED WITH WARNINGS\n")
                f.write(f"Some geographic inconsistencies detected (Score: {score}/100).\n")
                f.write("Review and correct flagged issues.\n")
            else:
                f.write("❌ VALIDATION FAILED\n")
                f.write(f"Significant geographic issues detected (Score: {score}/100).\n")
                f.write("Address critical issues before script writing.\n")

    def export_json(self, geography_report: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(geography_report, f, indent=2, ensure_ascii=False)

    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"🗺️  STATION 20: GEOGRAPHY & TRANSIT CHECK")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")

        try:
            await self.initialize()

            # Load dependencies
            print("📥 Loading dependencies...")
            dependencies = await self.load_dependencies()

            if not dependencies.get('world_bible'):
                raise ValueError("Missing world_bible from Station 9")

            print("✅ Dependencies loaded\n")

            # Run validation checks
            print("🗺️  Validating location network...")
            location_network = await self.validate_location_network(dependencies)
            print(f"  ✅ Geographic Consistency: {location_network.get('geographic_consistency_score', 0)}/100\n")

            print("🌤️  Validating weather continuity...")
            weather_continuity = await self.validate_weather_continuity(dependencies)
            print(f"  ✅ Seasonal Progression: {weather_continuity.get('seasonal_progression_score', 0)}/100\n")

            print("⏰ Validating temporal consistency...")
            temporal_consistency = await self.validate_temporal_consistency(dependencies)
            print(f"  ✅ Temporal Score: {temporal_consistency.get('temporal_consistency_score', 0)}/100\n")

            print("📊 Calculating overall transit realism...")
            transit_realism = await self.calculate_transit_realism(dependencies)
            print(f"  ✅ Transit Realism: {transit_realism.get('overall_score', 0)}/100\n")

            # Calculate overall geography score
            geography_score = transit_realism.get('overall_score', 0)

            # Count critical issues
            critical_temporal = len([
                i for i in temporal_consistency.get('temporal_issues', [])
                if i.get('severity') == 'critical'
            ])
            weather_issues = len([
                w for w in weather_continuity.get('weather_continuity', [])
                if w.get('consistency_with_timeline') == 'inconsistent'
            ])

            # Determine validation status
            if critical_temporal > 3 or geography_score < 60:
                validation_status = "FAIL"
            elif critical_temporal > 0 or weather_issues > 5 or geography_score < 75:
                validation_status = "WARNING"
            else:
                validation_status = "PASS"

            # Compile final report
            geography_report = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'validation_status': validation_status,
                'geography_score': geography_score,
                'location_network': location_network,
                'weather_continuity': weather_continuity,
                'temporal_consistency': temporal_consistency,
                'transit_realism': transit_realism
            }

            # Export outputs
            print("💾 Exporting geography validation report...")
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)

            base_filename = f"station20_geography_transit_{self.session_id}"

            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")

            self.export_txt(geography_report, txt_path)
            print(f"  ✅ Text Report: {txt_path}")

            self.export_json(geography_report, json_path)
            print(f"  ✅ JSON Data: {json_path}")

            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_20",
                json.dumps(geography_report)
            )
            print("✅ Saved to Redis\n")

            result = {
                'station': 'station_20_geography_transit',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path
                },
                'statistics': {
                    'validation_status': validation_status,
                    'geography_score': geography_score,
                    'transit_realism_score': transit_realism.get('transit_realism_score', 0),
                    'weather_score': weather_continuity.get('weather_logic_score', 0),
                    'temporal_score': temporal_consistency.get('temporal_consistency_score', 0),
                    'location_pairs_analyzed': location_network.get('location_pairs_analyzed', 0)
                },
                'geography_report': geography_report
            }

            # Show status
            status_icon = "✅" if validation_status == "PASS" else "⚠️" if validation_status == "WARNING" else "❌"
            print(f"{'='*70}")
            print(f"{status_icon} STATION 20 COMPLETE: Geography & Transit {validation_status}")
            print(f"{'='*70}\n")
            print(f"Geography Score: {geography_score}/100")
            print(f"Locations Analyzed: {location_network.get('location_pairs_analyzed', 0)}\n")

            return result

        except Exception as e:
            print(f"\n❌ Error in Station 20: {str(e)}")
            raise
        finally:
            await self.redis_client.disconnect()


if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) > 1:
        session_id = sys.argv[1]
    else:
        session_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    async def main():
        station = Station20GeographyTransit(session_id)
        result = await station.run()
        print("\n📊 Station 20 Results:")
        print(json.dumps(result['statistics'], indent=2))

    asyncio.run(main())
