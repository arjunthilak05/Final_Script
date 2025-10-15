"""
Station 18: Evergreen Check Agent

This agent identifies and removes dated references to ensure the audiobook
remains timeless and relevant for years to come. Emphasizes universal themes
over temporary cultural moments.

Dependencies: All stations (comprehensive content review)
Outputs: Evergreen validation report (TXT, JSON)
Human Gate: None - validation gate before script writing
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient


class Station18EvergreenCheck:
    def __init__(self, session_id: str, output_dir: str = "outputs"):
        self.session_id = session_id
        self.output_dir = output_dir
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_18_evergreen_check"

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()

    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from all stations for comprehensive review"""
        dependencies = {}

        # Load all stations that contain content/story elements
        station_keys = {
            'station_02': 'project_dna',
            'station_05': 'season_architecture',
            'station_06': 'style_guide',
            'station_08': 'character_bible',
            'station_09': 'world_bible',
            'station_14': 'episode_blueprints',
            'station_15': 'detailed_outlines'
        }

        for redis_key, dependency_name in station_keys.items():
            raw_data = await self.redis_client.get(f"audiobook:{self.session_id}:{redis_key}")
            if raw_data:
                dependencies[dependency_name] = json.loads(raw_data)

        return dependencies

    async def detect_dated_technology_references(self, dependencies: Dict) -> Dict[str, Any]:
        """Detect technology references that will become obsolete using LLM"""

        world_bible = dependencies.get('world_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract tech/magic systems
        tech_systems = world_bible.get('tech_magic_systems', [])
        if isinstance(tech_systems, list):
            tech_systems_sample = tech_systems[:3]
        else:
            tech_systems_sample = []

        world_summary = json.dumps({
            'tech_magic_systems': tech_systems_sample,
            'world_setting': world_bible.get('world_setting', {})
        }, indent=2)[:2000]

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
You are an Evergreen Content Validator analyzing technology references for long-term relevance.

WORLD BUILDING:
{world_summary}

EPISODE CONTENT:
{episodes_summary}

Identify DATED TECHNOLOGY REFERENCES that will feel outdated in 5-10 years:

1. SPECIFIC DEVICES:
   - Brand names (iPhone, iPad, specific models)
   - Obsolete technology (floppy disks, CD-ROMs, pagers)
   - Current but rapidly evolving tech (smart speakers, VR headsets)
   - Any technology tied to specific year/model

2. DIGITAL PLATFORMS:
   - Social media platforms by name (Facebook, TikTok, etc.)
   - Specific apps or services
   - Website references
   - Streaming platforms

3. COMMUNICATION METHODS:
   - Specific messaging apps
   - Video call platforms
   - Email providers
   - Text messaging specifics

4. COMPUTING CONCEPTS:
   - Operating system versions
   - Software specifics
   - Cloud service names
   - Tech jargon that may evolve

For EACH dated reference found:
- Type: "technology", "device", "platform", "software", "communication"
- Content: The specific reference
- Location: Station and Episode
- Risk_level: "high" (will feel dated in 1-2 years), "medium" (3-5 years), "low" (5-10 years)
- Expiration_estimate: How long until it feels dated
- Suggested_replacement: Evergreen alternative (e.g., "smartphone" instead of "iPhone 12")

Generate as detailed JSON structure.

Expected JSON format:
{{
  "technology_references_found": 5,
  "flagged_content": [
    {{
      "type": "device",
      "content": "iPhone 12",
      "location": "Station 15, Episode 3",
      "risk_level": "high",
      "expiration_estimate": "2 years",
      "suggested_replacement": "smartphone"
    }}
  ],
  "technology_score": 85
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'technology_references_found': 0,
            'flagged_content': [],
            'technology_score': 0
        })

    async def detect_cultural_temporal_references(self, dependencies: Dict) -> Dict[str, Any]:
        """Detect cultural/celebrity references that may become obscure using LLM"""

        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})
        character_bible = dependencies.get('character_bible', {})

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
You are an Evergreen Content Validator analyzing cultural references for long-term relevance.

EPISODE CONTENT:
{episodes_summary}

Identify CULTURAL/TEMPORAL REFERENCES that may become obscure or dated:

1. CELEBRITY REFERENCES:
   - Current celebrities, influencers
   - Athletes, musicians, actors
   - Political figures
   - Internet personalities

2. CURRENT EVENTS:
   - Specific news events
   - Political movements
   - Social trends
   - Viral moments

3. TRENDS & FADS:
   - Fashion trends
   - Food trends
   - Slang/memes
   - Dance crazes
   - Internet challenges

4. BRAND REFERENCES:
   - Specific brands/products
   - Restaurant chains
   - Retail stores
   - Service brands

5. TIME-SPECIFIC CULTURAL MOMENTS:
   - Movie/TV show references (unless classics)
   - Music references (unless timeless)
   - Book references (unless classics)
   - Video game references

For EACH dated reference found:
- Type: "celebrity", "event", "trend", "brand", "media"
- Content: The specific reference
- Location: Station and Episode
- Risk_level: "high", "medium", "low"
- Expiration_estimate: How long until obscure
- Suggested_replacement: Evergreen alternative or removal

Generate as detailed JSON structure.

Expected JSON format:
{{
  "cultural_references_found": 8,
  "flagged_content": [
    {{
      "type": "celebrity",
      "content": "Reference to current pop star",
      "location": "Station 15, Episode 5",
      "risk_level": "high",
      "expiration_estimate": "5 years",
      "suggested_replacement": "Remove or replace with fictional musician"
    }}
  ],
  "cultural_score": 82
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'cultural_references_found': 0,
            'flagged_content': [],
            'cultural_score': 0
        })

    async def analyze_theme_universality(self, dependencies: Dict) -> Dict[str, Any]:
        """Analyze themes for universal, timeless appeal using LLM"""

        project_dna = dependencies.get('project_dna', {})
        season_architecture = dependencies.get('season_architecture', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})

        project_summary = json.dumps({
            'genre_tone': project_dna.get('genre_tone', {}),
            'creative_promises': project_dna.get('creative_promises', {})
        }, indent=2)[:2000]

        season_summary = json.dumps({
            'season_overview': episode_blueprints.get('season_overview', {})
        }, indent=2)[:3000]

        prompt = f"""
You are an Evergreen Content Validator analyzing themes for universal, timeless appeal.

PROJECT DNA:
{project_summary}

SEASON OVERVIEW:
{season_summary}

Analyze THEME UNIVERSALITY:

1. CORE THEMES:
   - What are the central themes of this story?
   - Are they universal human experiences? (love, loss, courage, identity, family, etc.)
   - Do themes transcend specific time periods?
   - Are themes culturally universal or region-specific?

2. EMOTIONAL RESONANCE:
   - Do emotions explored apply across generations?
   - Are conflicts relatable regardless of era?
   - Do character struggles feel timeless?

3. CULTURAL SPECIFICITY:
   - Is the story tied to specific culture/location? (Not necessarily bad)
   - Are cultural elements explained for broader audience?
   - Does cultural specificity enhance or limit universality?

4. TEMPORAL INDEPENDENCE:
   - Could this story work in multiple time periods?
   - Are plot drivers dependent on current era?
   - Do conflicts require modern context?

5. LONGEVITY FACTORS:
   - What gives this story staying power?
   - Classic storytelling elements present?
   - Archetypal characters and conflicts?

Generate detailed analysis of universal vs. time-specific elements.

Expected JSON format:
{{
  "core_themes": ["identity", "family", "courage"],
  "theme_universality_score": 90,
  "cultural_specificity": "western",
  "longevity_rating": "20+ years",
  "universal_elements": [
    "Coming-of-age journey",
    "Family conflict and reconciliation"
  ],
  "time_specific_elements": [
    "Minor: References to current technology"
  ],
  "recommendations": [
    "Strengthen universal themes",
    "Replace specific tech references"
  ]
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'core_themes': [],
            'theme_universality_score': 0,
            'cultural_specificity': 'unknown',
            'longevity_rating': 'unknown',
            'universal_elements': [],
            'time_specific_elements': [],
            'recommendations': []
        })

    async def detect_temporal_specificity(self, dependencies: Dict) -> Dict[str, Any]:
        """Detect specific dates, years, and time markers using LLM"""

        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

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
You are an Evergreen Content Validator analyzing temporal specificity.

EPISODE CONTENT:
{episodes_summary}

Identify TEMPORAL SPECIFICITY that dates the content:

1. SPECIFIC DATES/YEARS:
   - Exact years mentioned (unless historical necessity)
   - Specific dates (unless plot-critical)
   - "Current year" references
   - Age references tied to specific years

2. TIME PERIOD MARKERS:
   - "In 2023..." or similar
   - References to decades unnecessarily
   - Era-specific details without purpose
   - Anniversary dates

3. TIMELINE ANCHORS:
   - Events tied to real-world dates
   - Character ages revealing time period
   - Historical events as timeline markers
   - Technology implying specific era

For EACH temporal reference:
- Type: "specific_date", "year", "era_reference", "timeline_anchor"
- Content: The specific reference
- Location: Station and Episode
- Necessity: "required" (historically necessary), "optional" (could be removed), "problematic" (dates content)
- Suggested_replacement: Evergreen alternative or justification for keeping

Generate as detailed JSON structure.

Expected JSON format:
{{
  "temporal_references_found": 3,
  "flagged_content": [
    {{
      "type": "year",
      "content": "Set in 2023",
      "location": "Station 14, Episode 1",
      "necessity": "optional",
      "suggested_replacement": "Remove specific year, use 'present day' or 'near future'"
    }}
  ],
  "temporal_specificity_score": 88
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'temporal_references_found': 0,
            'flagged_content': [],
            'temporal_specificity_score': 0
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

    def export_txt(self, evergreen_report: Dict, filepath: str):
        """Export human-readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("STATION 18: EVERGREEN CONTENT VALIDATION REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Validation Status: {evergreen_report.get('validation_status', 'UNKNOWN')}\n")
            f.write(f"Evergreen Score: {evergreen_report.get('evergreen_score', 0)}/100\n\n")

            # Summary
            f.write("VALIDATION SUMMARY\n")
            f.write("-"*70 + "\n")
            f.write(f"Total Dated References: {evergreen_report.get('dated_references_found', 0)}\n")
            f.write(f"Technology References: {evergreen_report.get('technology_validation', {}).get('technology_references_found', 0)}\n")
            f.write(f"Cultural References: {evergreen_report.get('cultural_validation', {}).get('cultural_references_found', 0)}\n")
            f.write(f"Temporal References: {evergreen_report.get('temporal_validation', {}).get('temporal_references_found', 0)}\n\n")

            # Theme Universality
            f.write("THEME UNIVERSALITY ANALYSIS\n")
            f.write("-"*70 + "\n")
            theme_analysis = evergreen_report.get('theme_universality', {})
            f.write(f"Universality Score: {theme_analysis.get('theme_universality_score', 0)}/100\n")
            f.write(f"Cultural Specificity: {theme_analysis.get('cultural_specificity', 'N/A')}\n")
            f.write(f"Longevity Rating: {theme_analysis.get('longevity_rating', 'N/A')}\n\n")

            if theme_analysis.get('core_themes'):
                f.write(f"Core Themes: {', '.join(theme_analysis.get('core_themes', []))}\n\n")

            if theme_analysis.get('universal_elements'):
                f.write("Universal Elements:\n")
                for element in theme_analysis.get('universal_elements', []):
                    f.write(f"  • {element}\n")
                f.write("\n")

            # Flagged Content
            if evergreen_report.get('flagged_content'):
                f.write("\n" + "="*70 + "\n")
                f.write("DATED REFERENCES REQUIRING ATTENTION\n")
                f.write("="*70 + "\n\n")

                # Group by risk level
                for risk_level in ['high', 'medium', 'low']:
                    risk_items = [item for item in evergreen_report.get('flagged_content', [])
                                if item.get('risk_level') == risk_level]

                    if risk_items:
                        risk_label = {
                            'high': '🔴 HIGH RISK (Will date quickly)',
                            'medium': '🟠 MEDIUM RISK (May date in 3-5 years)',
                            'low': '🟡 LOW RISK (Long-term concern)'
                        }.get(risk_level, risk_level.upper())

                        f.write(f"\n{risk_label}\n")
                        f.write("-"*70 + "\n")

                        for item in risk_items:
                            f.write(f"Type: {item.get('type', 'unknown').upper()}\n")
                            f.write(f"Content: {item.get('content', 'N/A')}\n")
                            f.write(f"Location: {item.get('location', 'N/A')}\n")
                            f.write(f"Expiration: {item.get('expiration_estimate', 'Unknown')}\n")
                            f.write(f"Replacement: {item.get('suggested_replacement', 'N/A')}\n\n")

            # Recommendations
            f.write("\n" + "="*70 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("="*70 + "\n\n")

            if theme_analysis.get('recommendations'):
                for rec in theme_analysis.get('recommendations', []):
                    f.write(f"• {rec}\n")
                f.write("\n")

            # Final Assessment
            f.write("\n" + "="*70 + "\n")
            f.write("FINAL ASSESSMENT\n")
            f.write("="*70 + "\n\n")

            status = evergreen_report.get('validation_status', 'UNKNOWN')
            score = evergreen_report.get('evergreen_score', 0)

            if status == 'PASS':
                f.write("✅ VALIDATION PASSED\n")
                f.write(f"Content has strong evergreen qualities (Score: {score}/100).\n")
                f.write("Story will remain relevant for years to come.\n")
            elif status == 'WARNING':
                f.write("⚠️  VALIDATION PASSED WITH WARNINGS\n")
                f.write(f"Some dated references detected (Score: {score}/100).\n")
                f.write("Review and update flagged content for longevity.\n")
            else:
                f.write("❌ VALIDATION FAILED\n")
                f.write(f"Significant dated content detected (Score: {score}/100).\n")
                f.write("Address high-risk references before proceeding.\n")

    def export_json(self, evergreen_report: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(evergreen_report, f, indent=2, ensure_ascii=False)

    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"⏳ STATION 18: EVERGREEN CONTENT CHECK")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")

        try:
            await self.initialize()

            # Load dependencies
            print("📥 Loading all station outputs...")
            dependencies = await self.load_dependencies()

            if not dependencies.get('episode_blueprints'):
                raise ValueError("Missing episode_blueprints from Station 14")

            print("✅ Dependencies loaded\n")

            # Run validation checks
            print("💻 Detecting dated technology references...")
            technology_validation = await self.detect_dated_technology_references(dependencies)
            print(f"  ✅ Technology Score: {technology_validation.get('technology_score', 0)}/100\n")

            print("🎭 Detecting cultural/temporal references...")
            cultural_validation = await self.detect_cultural_temporal_references(dependencies)
            print(f"  ✅ Cultural Score: {cultural_validation.get('cultural_score', 0)}/100\n")

            print("🌍 Analyzing theme universality...")
            theme_universality = await self.analyze_theme_universality(dependencies)
            print(f"  ✅ Universality Score: {theme_universality.get('theme_universality_score', 0)}/100\n")

            print("📅 Detecting temporal specificity...")
            temporal_validation = await self.detect_temporal_specificity(dependencies)
            print(f"  ✅ Temporal Score: {temporal_validation.get('temporal_specificity_score', 0)}/100\n")

            # Compile all flagged content
            all_flagged = []
            all_flagged.extend(technology_validation.get('flagged_content', []))
            all_flagged.extend(cultural_validation.get('flagged_content', []))
            all_flagged.extend(temporal_validation.get('flagged_content', []))

            # Calculate overall evergreen score
            scores = [
                int(technology_validation.get('technology_score', 0)) if technology_validation.get('technology_score') is not None else 0,
                int(cultural_validation.get('cultural_score', 0)) if cultural_validation.get('cultural_score') is not None else 0,
                int(theme_universality.get('theme_universality_score', 0)) if theme_universality.get('theme_universality_score') is not None else 0,
                int(temporal_validation.get('temporal_specificity_score', 0)) if temporal_validation.get('temporal_specificity_score') is not None else 0
            ]
            # Ensure all scores are integers and calculate average
            scores = [s for s in scores if isinstance(s, int)]
            evergreen_score = sum(scores) // len(scores) if scores else 0

            # Determine validation status
            high_risk_count = len([i for i in all_flagged if i.get('risk_level') == 'high'])
            medium_risk_count = len([i for i in all_flagged if i.get('risk_level') == 'medium'])

            if high_risk_count > 5:
                validation_status = "FAIL"
            elif high_risk_count > 0 or medium_risk_count > 3 or evergreen_score < 75:
                validation_status = "WARNING"
            else:
                validation_status = "PASS"

            # Compile final report
            evergreen_report = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'validation_status': validation_status,
                'evergreen_score': evergreen_score,
                'dated_references_found': len(all_flagged),
                'flagged_content': all_flagged,
                'technology_validation': technology_validation,
                'cultural_validation': cultural_validation,
                'theme_universality': theme_universality,
                'temporal_validation': temporal_validation
            }

            # Export outputs
            print("💾 Exporting evergreen validation report...")
            output_dir = self.output_dir
            os.makedirs(output_dir, exist_ok=True)

            base_filename = f"station18_evergreen_check_{self.session_id}"

            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")

            self.export_txt(evergreen_report, txt_path)
            print(f"  ✅ Text Report: {txt_path}")

            self.export_json(evergreen_report, json_path)
            print(f"  ✅ JSON Data: {json_path}")

            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_18",
                json.dumps(evergreen_report)
            )
            print("✅ Saved to Redis\n")

            result = {
                'station': 'station_18_evergreen_check',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path
                },
                'statistics': {
                    'validation_status': validation_status,
                    'evergreen_score': evergreen_score,
                    'dated_references': len(all_flagged),
                    'high_risk': high_risk_count,
                    'medium_risk': medium_risk_count,
                    'low_risk': len([i for i in all_flagged if i.get('risk_level') == 'low'])
                },
                'evergreen_report': evergreen_report
            }

            # Show status
            status_icon = "✅" if validation_status == "PASS" else "⚠️" if validation_status == "WARNING" else "❌"
            print(f"{'='*70}")
            print(f"{status_icon} STATION 18 COMPLETE: Evergreen Check {validation_status}")
            print(f"{'='*70}\n")
            print(f"Evergreen Score: {evergreen_score}/100")
            print(f"Dated References: {len(all_flagged)} ({high_risk_count} high risk)\n")

            return result

        except Exception as e:
            print(f"\n❌ Error in Station 18: {str(e)}")
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
        station = Station18EvergreenCheck(session_id)
        result = await station.run()
        print("\n📊 Station 18 Results:")
        print(json.dumps(result['statistics'], indent=2))

    asyncio.run(main())
