"""
Station 16: Canon Check Agent

This agent validates narrative consistency across all previous stations before
script writing begins. Ensures characters, locations, timeline, world rules,
and plot points are consistent with no contradictions.

Dependencies: All stations 1-15
Outputs: Comprehensive canon validation report (TXT, JSON)
Human Gate: None - validation gate before script writing
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient


@dataclass
class CanonIssue:
    """Data structure for a canon consistency issue"""
    type: str  # character_name, location, timeline, world_rules, plot
    severity: str  # critical, major, minor
    description: str
    affected_stations: List[int]
    affected_episodes: List[int]
    recommended_fix: str


class Station16CanonCheck:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_16_canon_check"

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()

    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from all previous stations"""
        dependencies = {}

        # Load all relevant stations for canon checking
        station_keys = {
            'station_05': 'season_architecture',
            'station_08': 'character_bible',
            'station_09': 'world_bible',
            'station_10': 'narrative_reveal',
            'station_11': 'runtime_planning',
            'station_14': 'episode_blueprints',
            'station_15': 'detailed_outlines'
        }

        for redis_key, dependency_name in station_keys.items():
            raw_data = await self.redis_client.get(f"audiobook:{self.session_id}:{redis_key}")
            if raw_data:
                dependencies[dependency_name] = json.loads(raw_data)

        return dependencies

    async def validate_character_consistency(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate character names, ages, relationships consistency using LLM"""

        char_bible = dependencies.get('character_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Extract character data for analysis
        characters_summary = json.dumps({
            'tier1_protagonists': char_bible.get('tier1_protagonists', []),
            'tier2_supporting': char_bible.get('tier2_supporting', []),
            'tier3_recurring': char_bible.get('tier3_recurring', [])
        }, indent=2)[:3000]

        episodes_summary = json.dumps({
            'blueprints': episode_blueprints.get('episodes', []),
            'outlines': detailed_outlines.get('episodes', [])
        }, indent=2)[:4000]

        prompt = f"""
You are a Canon Consistency Validator analyzing character consistency across an audiobook series.

CHARACTER BIBLE (Station 8):
{characters_summary}

EPISODE BLUEPRINTS & OUTLINES (Stations 14-15):
{episodes_summary}

Perform COMPREHENSIVE CHARACTER CONSISTENCY ANALYSIS:

1. NAME CONSISTENCY:
   - Are character names spelled consistently across all episodes?
   - Any accidental name variations or typos?
   - Nickname usage consistent?

2. AGE & PHYSICAL CONSISTENCY:
   - Do character ages remain consistent?
   - Physical descriptions match across episodes?
   - Any impossible age progressions?

3. RELATIONSHIP CONSISTENCY:
   - Character relationships defined clearly?
   - Relationship changes tracked logically?
   - Any contradictory relationship statements?

4. PERSONALITY & BEHAVIOR CONSISTENCY:
   - Character traits consistent across episodes?
   - Behavior patterns match established personality?
   - Any out-of-character actions without justification?

5. BACKSTORY CONSISTENCY:
   - Character histories remain consistent?
   - No contradictory backstory details?
   - Character arcs progress logically?

For EACH issue found, provide:
- Type: "character_name", "character_age", "character_relationship", "character_personality", "character_backstory"
- Severity: "critical" (breaks story logic), "major" (confusing but workable), "minor" (small inconsistency)
- Description: Clear explanation of the inconsistency
- Affected_stations: Which stations contain the conflict
- Affected_episodes: Which episode numbers are involved
- Recommended_fix: Specific actionable correction

Generate as detailed JSON structure.

Expected JSON format:
{{
  "character_consistency_score": 85,
  "issues": [
    {{
      "type": "character_name",
      "severity": "critical",
      "description": "Character 'Sarah' is called 'Sara' in Episode 5",
      "affected_stations": [8, 15],
      "affected_episodes": [5],
      "recommended_fix": "Standardize spelling to 'Sarah' in Episode 5 outline"
    }}
  ],
  "characters_checked": 12,
  "episodes_analyzed": 10
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'character_consistency_score': 0,
            'issues': [],
            'characters_checked': 0,
            'episodes_analyzed': 0
        })

    async def validate_location_consistency(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate location names and geography consistency using LLM"""

        world_bible = dependencies.get('world_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        locations_summary = json.dumps({
            'geography': world_bible.get('geography', []),
            'location_names': world_bible.get('location_names', [])
        }, indent=2)[:3000]

        episodes_summary = json.dumps({
            'blueprints': episode_blueprints.get('episodes', [])[:5],
            'outlines': detailed_outlines.get('episodes', [])[:5]
        }, indent=2)[:4000]

        prompt = f"""
You are a Canon Consistency Validator analyzing location consistency across an audiobook series.

WORLD BIBLE (Station 9):
{locations_summary}

EPISODE BLUEPRINTS & OUTLINES (Stations 14-15):
{episodes_summary}

Perform COMPREHENSIVE LOCATION CONSISTENCY ANALYSIS:

1. NAME CONSISTENCY:
   - Are location names spelled consistently?
   - Any accidental variations or typos?
   - Location naming conventions followed?

2. GEOGRAPHY CONSISTENCY:
   - Spatial relationships between locations logical?
   - Distance mentions consistent?
   - Location descriptions match across episodes?

3. LOCATION FEATURES:
   - Key features of locations remain consistent?
   - No contradictory descriptions of same location?
   - Location capabilities/limitations consistent?

4. LOCATION ACCESSIBILITY:
   - Travel routes between locations logical?
   - Access restrictions mentioned consistently?
   - Location availability matches world rules?

For EACH issue found, provide:
- Type: "location_name", "location_geography", "location_features", "location_accessibility"
- Severity: "critical", "major", "minor"
- Description, affected_stations, affected_episodes, recommended_fix

Generate as detailed JSON structure.

Expected JSON format:
{{
  "location_consistency_score": 90,
  "issues": [],
  "locations_checked": 8,
  "episodes_analyzed": 10
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'location_consistency_score': 0,
            'issues': [],
            'locations_checked': 0,
            'episodes_analyzed': 0
        })

    async def validate_timeline_consistency(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate chronology and timeline consistency using LLM"""

        runtime_planning = dependencies.get('runtime_planning', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        timeline_summary = json.dumps({
            'runtime_plan': runtime_planning,
            'season_timeline': dependencies.get('season_architecture', {}).get('macro_structure', {})
        }, indent=2)[:3000]

        episodes_summary = json.dumps({
            'blueprints': episode_blueprints.get('episodes', []),
            'outlines': detailed_outlines.get('episodes', [])
        }, indent=2)[:4000]

        prompt = f"""
You are a Canon Consistency Validator analyzing timeline consistency across an audiobook series.

TIMELINE & RUNTIME PLANNING (Station 11):
{timeline_summary}

EPISODE BLUEPRINTS & OUTLINES (Stations 14-15):
{episodes_summary}

Perform COMPREHENSIVE TIMELINE CONSISTENCY ANALYSIS:

1. CHRONOLOGICAL ORDER:
   - Events occur in logical sequence?
   - No time paradoxes or impossible timelines?
   - Episode order makes chronological sense?

2. TIME PASSAGE:
   - Time gaps between episodes clearly indicated?
   - Character aging consistent with time passage?
   - Seasonal/yearly progression logical?

3. EVENT TIMING:
   - Event durations realistic?
   - Simultaneous events handled correctly?
   - Flashbacks/time jumps clearly marked?

4. DEADLINE CONSISTENCY:
   - Time-sensitive deadlines tracked accurately?
   - Countdowns remain consistent?
   - No deadline contradictions?

For EACH issue found, provide:
- Type: "timeline_order", "time_passage", "event_timing", "deadline_consistency"
- Severity: "critical", "major", "minor"
- Description, affected_stations, affected_episodes, recommended_fix

Generate as detailed JSON structure.

Expected JSON format:
{{
  "timeline_consistency_score": 88,
  "issues": [],
  "timeline_events_checked": 25,
  "episodes_analyzed": 10
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'timeline_consistency_score': 0,
            'issues': [],
            'timeline_events_checked': 0,
            'episodes_analyzed': 0
        })

    async def validate_world_rules_consistency(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate world rules, magic/tech systems consistency using LLM"""

        world_bible = dependencies.get('world_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        world_rules_summary = json.dumps({
            'tech_magic_systems': world_bible.get('tech_magic_systems', []),
            'system_names': world_bible.get('system_names', []),
            'world_statistics': world_bible.get('world_statistics', {})
        }, indent=2)[:3000]

        episodes_summary = json.dumps({
            'blueprints': episode_blueprints.get('episodes', [])[:5],
            'outlines': detailed_outlines.get('episodes', [])[:5]
        }, indent=2)[:4000]

        prompt = f"""
You are a Canon Consistency Validator analyzing world rules consistency across an audiobook series.

WORLD BIBLE (Station 9):
{world_rules_summary}

EPISODE BLUEPRINTS & OUTLINES (Stations 14-15):
{episodes_summary}

Perform COMPREHENSIVE WORLD RULES CONSISTENCY ANALYSIS:

1. MAGIC/TECH SYSTEMS:
   - Are system rules applied consistently?
   - No contradictory power/ability descriptions?
   - Limitations respected across episodes?

2. WORLD PHYSICS:
   - Physical laws of the world consistent?
   - No impossible actions violating established rules?
   - World mechanics operate predictably?

3. SOCIAL RULES:
   - Cultural norms followed consistently?
   - Social hierarchies remain stable (unless plot dictates change)?
   - Legal/governance systems consistent?

4. RESOURCE CONSISTENCY:
   - Available resources match world building?
   - Technology level consistent?
   - Economic systems logical?

For EACH issue found, provide:
- Type: "magic_tech_system", "world_physics", "social_rules", "resource_consistency"
- Severity: "critical", "major", "minor"
- Description, affected_stations, affected_episodes, recommended_fix

Generate as detailed JSON structure.

Expected JSON format:
{{
  "world_rules_consistency_score": 92,
  "issues": [],
  "systems_checked": 5,
  "episodes_analyzed": 10
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'world_rules_consistency_score': 0,
            'issues': [],
            'systems_checked': 0,
            'episodes_analyzed': 0
        })

    async def validate_plot_consistency(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate plot points and story arc consistency using LLM"""

        season_architecture = dependencies.get('season_architecture', {})
        narrative_reveal = dependencies.get('narrative_reveal', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        plot_summary = json.dumps({
            'season_arc': season_architecture.get('macro_structure', {}),
            'reveal_strategy': narrative_reveal,
            'season_overview': episode_blueprints.get('season_overview', {})
        }, indent=2)[:3000]

        episodes_summary = json.dumps({
            'blueprints': episode_blueprints.get('episodes', []),
            'outlines': detailed_outlines.get('episodes', [])
        }, indent=2)[:4000]

        prompt = f"""
You are a Canon Consistency Validator analyzing plot consistency across an audiobook series.

SEASON ARCHITECTURE & NARRATIVE REVEAL (Stations 5, 10):
{plot_summary}

EPISODE BLUEPRINTS & OUTLINES (Stations 14-15):
{episodes_summary}

Perform COMPREHENSIVE PLOT CONSISTENCY ANALYSIS:

1. PLOT THREADS:
   - All introduced plot threads tracked?
   - No abandoned storylines without resolution?
   - Plot threads weave together logically?

2. CHARACTER ARCS:
   - Character development progresses logically?
   - Character goals and motivations consistent?
   - Arc resolutions satisfying?

3. CAUSE & EFFECT:
   - Story events follow logical causality?
   - Character actions have appropriate consequences?
   - No plot holes or logic gaps?

4. REVEALS & MYSTERIES:
   - Mysteries set up properly?
   - Reveals match earlier clues/setup?
   - No contradictory revelations?

5. STAKES & CONFLICT:
   - Stakes escalate appropriately?
   - Conflicts resolve logically?
   - Tension builds effectively?

For EACH issue found, provide:
- Type: "plot_thread", "character_arc", "cause_effect", "reveal_mystery", "stakes_conflict"
- Severity: "critical", "major", "minor"
- Description, affected_stations, affected_episodes, recommended_fix

Generate as detailed JSON structure.

Expected JSON format:
{{
  "plot_consistency_score": 87,
  "issues": [],
  "plot_points_checked": 30,
  "episodes_analyzed": 10
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'plot_consistency_score': 0,
            'issues': [],
            'plot_points_checked': 0,
            'episodes_analyzed': 0
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

    def export_txt(self, canon_report: Dict, filepath: str):
        """Export human-readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("STATION 16: CANON CONSISTENCY VALIDATION REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Validation Status: {canon_report.get('validation_status', 'UNKNOWN')}\n")
            f.write(f"Overall Consistency Score: {canon_report.get('consistency_score', 0)}/100\n\n")

            # Summary
            f.write("VALIDATION SUMMARY\n")
            f.write("-"*70 + "\n")
            f.write(f"Total Issues Found: {canon_report.get('total_issues', 0)}\n")
            f.write(f"Critical Issues: {len([i for i in canon_report.get('critical_issues', []) if i.get('severity') == 'critical'])}\n")
            f.write(f"Major Issues: {len([i for i in canon_report.get('critical_issues', []) if i.get('severity') == 'major'])}\n")
            f.write(f"Minor Issues: {len([i for i in canon_report.get('critical_issues', []) if i.get('severity') == 'minor'])}\n\n")

            # Elements Checked
            f.write("ELEMENTS CHECKED\n")
            f.write("-"*70 + "\n")
            checked = canon_report.get('checked_elements', {})
            f.write(f"Characters: {checked.get('characters', 0)}\n")
            f.write(f"Locations: {checked.get('locations', 0)}\n")
            f.write(f"Timeline Events: {checked.get('timeline_events', 0)}\n")
            f.write(f"World Rules: {checked.get('world_rules', 0)}\n")
            f.write(f"Plot Points: {checked.get('plot_points', 0)}\n\n")

            # Category Scores
            f.write("CONSISTENCY SCORES BY CATEGORY\n")
            f.write("-"*70 + "\n")
            f.write(f"Character Consistency: {canon_report.get('character_validation', {}).get('character_consistency_score', 0)}/100\n")
            f.write(f"Location Consistency: {canon_report.get('location_validation', {}).get('location_consistency_score', 0)}/100\n")
            f.write(f"Timeline Consistency: {canon_report.get('timeline_validation', {}).get('timeline_consistency_score', 0)}/100\n")
            f.write(f"World Rules Consistency: {canon_report.get('world_rules_validation', {}).get('world_rules_consistency_score', 0)}/100\n")
            f.write(f"Plot Consistency: {canon_report.get('plot_validation', {}).get('plot_consistency_score', 0)}/100\n\n")

            # Critical Issues
            if canon_report.get('critical_issues'):
                f.write("\n" + "="*70 + "\n")
                f.write("CRITICAL ISSUES REQUIRING ATTENTION\n")
                f.write("="*70 + "\n\n")

                for issue in canon_report.get('critical_issues', []):
                    severity_label = {
                        'critical': '🔴 CRITICAL',
                        'major': '🟠 MAJOR',
                        'minor': '🟡 MINOR'
                    }.get(issue.get('severity', 'minor'), issue.get('severity', 'UNKNOWN'))

                    f.write(f"{severity_label}: {issue.get('type', 'unknown').upper()}\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Description: {issue.get('description', 'N/A')}\n")
                    f.write(f"Affected Stations: {', '.join(map(str, issue.get('affected_stations', [])))}\n")
                    f.write(f"Affected Episodes: {', '.join(map(str, issue.get('affected_episodes', [])))}\n")
                    f.write(f"Recommended Fix: {issue.get('recommended_fix', 'N/A')}\n\n")

            # Final Assessment
            f.write("\n" + "="*70 + "\n")
            f.write("FINAL ASSESSMENT\n")
            f.write("="*70 + "\n\n")

            status = canon_report.get('validation_status', 'UNKNOWN')
            if status == 'PASS':
                f.write("✅ VALIDATION PASSED\n")
                f.write("Canon consistency is maintained across all stations.\n")
                f.write("Ready to proceed to script writing phase.\n")
            elif status == 'WARNING':
                f.write("⚠️  VALIDATION PASSED WITH WARNINGS\n")
                f.write("Minor inconsistencies detected but not blocking.\n")
                f.write("Review warnings before proceeding to script writing.\n")
            else:
                f.write("❌ VALIDATION FAILED\n")
                f.write("Critical inconsistencies must be resolved before script writing.\n")
                f.write("Address all critical issues and re-run validation.\n")

    def export_json(self, canon_report: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(canon_report, f, indent=2, ensure_ascii=False)

    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"📋 STATION 16: CANON CONSISTENCY CHECK")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")

        try:
            await self.initialize()

            # Load dependencies
            print("📥 Loading all previous station outputs...")
            dependencies = await self.load_dependencies()

            if not dependencies.get('character_bible'):
                raise ValueError("Missing character_bible from Station 8")
            if not dependencies.get('world_bible'):
                raise ValueError("Missing world_bible from Station 9")

            print("✅ Dependencies loaded\n")

            # Run validation checks
            print("🔍 Running character consistency validation...")
            character_validation = await self.validate_character_consistency(dependencies)
            print(f"  ✅ Character Score: {character_validation.get('character_consistency_score', 0)}/100\n")

            print("🗺️  Running location consistency validation...")
            location_validation = await self.validate_location_consistency(dependencies)
            print(f"  ✅ Location Score: {location_validation.get('location_consistency_score', 0)}/100\n")

            print("⏰ Running timeline consistency validation...")
            timeline_validation = await self.validate_timeline_consistency(dependencies)
            print(f"  ✅ Timeline Score: {timeline_validation.get('timeline_consistency_score', 0)}/100\n")

            print("🌍 Running world rules consistency validation...")
            world_rules_validation = await self.validate_world_rules_consistency(dependencies)
            print(f"  ✅ World Rules Score: {world_rules_validation.get('world_rules_consistency_score', 0)}/100\n")

            print("📖 Running plot consistency validation...")
            plot_validation = await self.validate_plot_consistency(dependencies)
            print(f"  ✅ Plot Score: {plot_validation.get('plot_consistency_score', 0)}/100\n")

            # Compile all issues
            all_issues = []
            all_issues.extend(character_validation.get('issues', []))
            all_issues.extend(location_validation.get('issues', []))
            all_issues.extend(timeline_validation.get('issues', []))
            all_issues.extend(world_rules_validation.get('issues', []))
            all_issues.extend(plot_validation.get('issues', []))

            # Calculate overall consistency score
            scores = [
                character_validation.get('character_consistency_score', 0),
                location_validation.get('location_consistency_score', 0),
                timeline_validation.get('timeline_consistency_score', 0),
                world_rules_validation.get('world_rules_consistency_score', 0),
                plot_validation.get('plot_consistency_score', 0)
            ]
            consistency_score = sum(scores) // len(scores) if scores else 0

            # Determine validation status
            critical_count = len([i for i in all_issues if i.get('severity') == 'critical'])
            major_count = len([i for i in all_issues if i.get('severity') == 'major'])

            if critical_count > 0:
                validation_status = "FAIL"
            elif major_count > 0 or consistency_score < 80:
                validation_status = "WARNING"
            else:
                validation_status = "PASS"

            # Compile final report
            canon_report = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'validation_status': validation_status,
                'consistency_score': consistency_score,
                'total_issues': len(all_issues),
                'critical_issues': all_issues,
                'checked_elements': {
                    'characters': character_validation.get('characters_checked', 0),
                    'locations': location_validation.get('locations_checked', 0),
                    'timeline_events': timeline_validation.get('timeline_events_checked', 0),
                    'world_rules': world_rules_validation.get('systems_checked', 0),
                    'plot_points': plot_validation.get('plot_points_checked', 0)
                },
                'character_validation': character_validation,
                'location_validation': location_validation,
                'timeline_validation': timeline_validation,
                'world_rules_validation': world_rules_validation,
                'plot_validation': plot_validation
            }

            # Export outputs
            print("💾 Exporting canon validation report...")
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)

            base_filename = f"station16_canon_check_{self.session_id}"

            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")

            self.export_txt(canon_report, txt_path)
            print(f"  ✅ Text Report: {txt_path}")

            self.export_json(canon_report, json_path)
            print(f"  ✅ JSON Data: {json_path}")

            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_16",
                json.dumps(canon_report)
            )
            print("✅ Saved to Redis\n")

            result = {
                'station': 'station_16_canon_check',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path
                },
                'statistics': {
                    'validation_status': validation_status,
                    'consistency_score': consistency_score,
                    'total_issues': len(all_issues),
                    'critical_issues': critical_count,
                    'major_issues': major_count,
                    'minor_issues': len([i for i in all_issues if i.get('severity') == 'minor'])
                },
                'canon_report': canon_report
            }

            # Show status
            status_icon = "✅" if validation_status == "PASS" else "⚠️" if validation_status == "WARNING" else "❌"
            print(f"{'='*70}")
            print(f"{status_icon} STATION 16 COMPLETE: Canon Check {validation_status}")
            print(f"{'='*70}\n")
            print(f"Consistency Score: {consistency_score}/100")
            print(f"Issues: {len(all_issues)} ({critical_count} critical, {major_count} major)\n")

            return result

        except Exception as e:
            print(f"\n❌ Error in Station 16: {str(e)}")
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
        station = Station16CanonCheck(session_id)
        result = await station.run()
        print("\n📊 Station 16 Results:")
        print(json.dumps(result['statistics'], indent=2))

    asyncio.run(main())
