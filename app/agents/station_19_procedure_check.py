"""
Station 19: Procedure Check Agent

This agent validates accuracy of specialized procedures and timelines to ensure
realistic portrayal of legal, medical, scientific, and other professional processes.

Dependencies: Stations 8, 9, 11, 14, 15
Outputs: Procedural accuracy validation report (TXT, JSON)
Human Gate: None - validation gate before script writing
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient


class Station19ProcedureCheck:
    def __init__(self, session_id: str, output_dir: str = "outputs"):
        self.session_id = session_id
        self.output_dir = output_dir
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_19_procedure_check"

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()

    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from previous stations"""
        dependencies = {}

        # Load stations containing procedural/technical content
        station_keys = {
            'station_08': 'character_bible',
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

    async def validate_professional_procedures(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate legal, medical, scientific, business procedures using LLM"""

        character_bible = dependencies.get('character_bible', {})
        world_bible = dependencies.get('world_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract protagonists
        protagonists = character_bible.get('tier1_protagonists', [])
        if isinstance(protagonists, list):
            protagonists_sample = protagonists[:3]
            character_professions = [
                char.get('profession', 'N/A') if isinstance(char, dict) else 'N/A'
                for char in protagonists
            ]
        else:
            protagonists_sample = []
            character_professions = []

        characters_summary = json.dumps({
            'protagonists': protagonists_sample,
            'character_professions': character_professions
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
        }, indent=2)[:5000]

        prompt = f"""
You are a Procedural Accuracy Validator analyzing professional processes in storytelling.

CHARACTERS & PROFESSIONS:
{characters_summary}

EPISODE CONTENT:
{episodes_summary}

Identify and validate SPECIALIZED PROCEDURES in these categories:

1. LEGAL PROCEDURES:
   - Court processes (arrests, trials, appeals)
   - Legal timelines (investigation to conviction)
   - Rights and procedures (Miranda, lawyer access)
   - Contract law, property law, etc.
   - Law enforcement protocols

2. MEDICAL PROCEDURES:
   - Diagnostic processes
   - Treatment protocols
   - Hospital procedures
   - Medical ethics and consent
   - Emergency medical response
   - Recovery timelines

3. SCIENTIFIC PROCEDURES:
   - Research methodologies
   - Lab protocols
   - Data collection/analysis
   - Peer review processes
   - Scientific equipment usage

4. INVESTIGATIVE PROCEDURES:
   - Police investigation steps
   - Evidence handling
   - Forensics processes
   - Interrogation procedures
   - Chain of custody

5. BUSINESS/PROFESSIONAL PROTOCOLS:
   - Corporate procedures
   - Professional hierarchies
   - Industry-specific protocols
   - Licensing/certification requirements

For EACH procedure found, validate:
- Category: "legal", "medical", "scientific", "investigative", "business"
- Procedure_description: What happens
- Location: Station and Episode
- Accuracy_rating: 0-100 (realistic vs. Hollywood)
- Issues: List of inaccuracies or oversimplifications
- Real_world_version: How it actually works
- Suggested_fix: How to correct while maintaining story needs
- Requires_expert_consultation: boolean
- Disclaimer_needed: boolean (if significantly altered for story)

Generate as detailed JSON structure.

Expected JSON format:
{{
  "procedure_categories_found": ["legal", "medical"],
  "total_procedures_validated": 5,
  "procedure_validations": [
    {{
      "category": "legal",
      "procedure_description": "Character arrested and immediately interrogated without lawyer",
      "location": "Station 15, Episode 3",
      "accuracy_rating": 40,
      "issues": [
        {{
          "type": "missing_steps",
          "description": "Miranda rights not mentioned",
          "real_world_version": "Must read Miranda rights before interrogation",
          "suggested_fix": "Add brief line about rights being read"
        }}
      ],
      "requires_expert_consultation": false,
      "disclaimer_needed": false
    }}
  ],
  "overall_procedural_realism": 75
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'procedure_categories_found': [],
            'total_procedures_validated': 0,
            'procedure_validations': [],
            'overall_procedural_realism': 0
        })

    async def validate_timeline_realism(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate timelines for procedures, healing, travel, etc. using LLM"""

        runtime_planning = dependencies.get('runtime_planning', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract episode breakdowns
        episode_breakdowns = runtime_planning.get('episode_breakdowns', [])
        if isinstance(episode_breakdowns, list):
            breakdowns_sample = episode_breakdowns[:5]
        else:
            breakdowns_sample = []

        runtime_summary = json.dumps({
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
You are a Timeline Realism Validator analyzing temporal accuracy of processes.

RUNTIME PLANNING:
{runtime_summary}

EPISODE CONTENT:
{episodes_summary}

Validate TIMELINE REALISM for various processes:

1. HEALING & RECOVERY TIMELINES:
   - Injury recovery times
   - Illness progression/recovery
   - Surgical recovery
   - Trauma healing (physical & psychological)

2. LEGAL PROCESS TIMELINES:
   - Investigation to arrest
   - Arrest to trial
   - Trial duration
   - Appeal processes
   - Sentence duration

3. TRAVEL TIMELINES:
   - Commute times
   - Long-distance travel
   - International travel (including processing)
   - Weather delays

4. CONSTRUCTION/DEVELOPMENT:
   - Building/renovation timelines
   - Infrastructure projects
   - Technology development

5. RELATIONSHIP/SOCIAL TIMELINES:
   - Trust building
   - Friendship development
   - Romantic relationships
   - Conflict resolution

6. SKILL ACQUISITION:
   - Learning new skills
   - Language learning
   - Professional training
   - Physical training

For EACH timeline issue:
- Event: What's happening
- Stated_duration: Time claimed in story
- Realistic_duration: Actual time required
- Discrepancy: "too fast", "too slow", "accurate"
- Impact: "critical" (breaks believability), "moderate" (noticeable but acceptable), "minor" (artistic license)
- Suggested_adjustment: How to make realistic or justify compressed timeline

Generate as detailed JSON structure.

Expected JSON format:
{{
  "timelines_validated": 8,
  "timeline_validations": [
    {{
      "event": "Character recovers from broken leg",
      "stated_duration": "2 weeks",
      "realistic_duration": "6-8 weeks",
      "discrepancy": "too fast",
      "impact": "moderate",
      "suggested_adjustment": "Extend to 6 weeks or show character still limping/in pain"
    }}
  ],
  "overall_timeline_realism": 82
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'timelines_validated': 0,
            'timeline_validations': [],
            'overall_timeline_realism': 0
        })

    async def validate_technology_usage(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate realistic technology usage and capabilities using LLM"""

        world_bible = dependencies.get('world_bible', {})
        episode_blueprints = dependencies.get('episode_blueprints', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract tech/magic systems
        tech_systems = world_bible.get('tech_magic_systems', [])
        if isinstance(tech_systems, list):
            tech_systems_sample = tech_systems
        else:
            tech_systems_sample = []

        world_summary = json.dumps({
            'tech_magic_systems': tech_systems_sample,
            'time_period': world_bible.get('time_period', 'modern')
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
You are a Technology Realism Validator analyzing tech usage accuracy.

WORLD BUILDING & TECH SYSTEMS:
{world_summary}

EPISODE CONTENT:
{episodes_summary}

Validate TECHNOLOGY USAGE REALISM:

1. DEVICE CAPABILITIES:
   - Computer/smartphone abilities accurate for era?
   - Hacking portrayed realistically?
   - Software capabilities realistic?
   - Network/internet speeds accurate?

2. COMMUNICATION TECH:
   - Phone/messaging tech accurate for time period?
   - Video calling realistic?
   - Signal coverage/dead zones realistic?
   - Communication delays appropriate?

3. SURVEILLANCE & SECURITY:
   - Security systems realistic?
   - Surveillance capabilities accurate?
   - Hacking/bypassing security realistic?
   - Encryption/decryption timelines?

4. MEDICAL/SCIENTIFIC TECH:
   - Medical equipment usage accurate?
   - Lab equipment capabilities realistic?
   - Analysis/test result timelines?
   - Technology limitations acknowledged?

5. FUTURE/ADVANCED TECH (if applicable):
   - Sci-fi technology internally consistent?
   - Tech limitations and trade-offs shown?
   - Technology learning curves realistic?

For EACH technology issue:
- Technology: What tech is used
- Usage_description: How it's used in story
- Location: Station and Episode
- Accuracy_rating: 0-100
- Issues: Unrealistic aspects
- Real_capabilities: What tech can actually do
- Suggested_fix: More realistic portrayal
- Time_period_appropriate: boolean

Generate as detailed JSON structure.

Expected JSON format:
{{
  "technologies_validated": 6,
  "technology_validations": [
    {{
      "technology": "Smartphone hacking",
      "usage_description": "Character hacks phone in 30 seconds",
      "location": "Station 15, Episode 4",
      "accuracy_rating": 30,
      "issues": ["Unrealistically fast", "No security measures shown"],
      "real_capabilities": "Would require specialized software, time, and expertise",
      "suggested_fix": "Show preparation, tools used, or extend timeline",
      "time_period_appropriate": true
    }}
  ],
  "overall_tech_realism": 70
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'technologies_validated': 0,
            'technology_validations': [],
            'overall_tech_realism': 0
        })

    async def identify_expert_consultation_needs(self, dependencies: Dict) -> Dict[str, Any]:
        """Identify areas requiring expert consultation using LLM"""

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
You are an Expert Consultation Recommender analyzing complex content accuracy needs.

EPISODE CONTENT:
{episodes_summary}

Identify areas requiring EXPERT CONSULTATION:

1. HIGH-STAKES PROCEDURES:
   - Medical procedures with life/death consequences
   - Legal procedures with major plot impact
   - Scientific processes central to story
   - Military/tactical operations
   - Financial/economic systems

2. SPECIALIZED KNOWLEDGE:
   - Niche professional expertise
   - Technical jargon and terminology
   - Industry-specific protocols
   - Cultural/religious practices
   - Historical accuracy

3. SENSITIVE TOPICS:
   - Mental health portrayal
   - Disability representation
   - Trauma and recovery
   - Addiction and treatment
   - Cultural authenticity

4. ETHICAL CONSIDERATIONS:
   - Professional ethics (medical, legal)
   - Research ethics
   - Privacy and consent
   - Moral dilemmas

For EACH area needing consultation:
- Expertise_needed: Type of expert required
- Reason: Why consultation is important
- Content_area: What needs review
- Priority: "critical" (affects core plot), "important" (authenticity), "helpful" (polish)
- Potential_experts: Types of professionals to consult
- Questions_to_ask: Specific questions for expert

Generate as detailed JSON structure.

Expected JSON format:
{{
  "consultation_areas": 3,
  "expert_consultations_recommended": [
    {{
      "expertise_needed": "Emergency Medicine",
      "reason": "Major medical emergency is plot turning point",
      "content_area": "Episode 5 hospital scenes",
      "priority": "critical",
      "potential_experts": ["ER doctor", "Paramedic", "Trauma nurse"],
      "questions_to_ask": [
        "Is trauma response timeline realistic?",
        "Are medical procedures accurately portrayed?",
        "Is medical terminology used correctly?"
      ]
    }}
  ],
  "disclaimer_recommendations": [
    "Consider adding: 'Medical procedures dramatized for storytelling'"
  ]
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'consultation_areas': 0,
            'expert_consultations_recommended': [],
            'disclaimer_recommendations': []
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

    def export_txt(self, procedure_report: Dict, filepath: str):
        """Export human-readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("STATION 19: PROCEDURAL ACCURACY VALIDATION REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Validation Status: {procedure_report.get('validation_status', 'UNKNOWN')}\n")
            f.write(f"Overall Realism Score: {procedure_report.get('overall_realism_score', 0)}/100\n\n")

            # Summary
            f.write("VALIDATION SUMMARY\n")
            f.write("-"*70 + "\n")
            proc_val = procedure_report.get('procedure_validation', {})
            time_val = procedure_report.get('timeline_validation', {})
            tech_val = procedure_report.get('technology_validation', {})

            f.write(f"Procedures Validated: {proc_val.get('total_procedures_validated', 0)}\n")
            f.write(f"Timelines Validated: {time_val.get('timelines_validated', 0)}\n")
            f.write(f"Technologies Validated: {tech_val.get('technologies_validated', 0)}\n")
            f.write(f"Procedural Realism: {proc_val.get('overall_procedural_realism', 0)}/100\n")
            f.write(f"Timeline Realism: {time_val.get('overall_timeline_realism', 0)}/100\n")
            f.write(f"Technology Realism: {tech_val.get('overall_tech_realism', 0)}/100\n\n")

            # Procedure Categories
            if proc_val.get('procedure_categories_found'):
                f.write(f"Procedure Categories: {', '.join(proc_val.get('procedure_categories_found', []))}\n\n")

            # Procedure Validations
            if proc_val.get('procedure_validations'):
                f.write("\n" + "="*70 + "\n")
                f.write("PROCEDURE ACCURACY ANALYSIS\n")
                f.write("="*70 + "\n\n")

                for proc in proc_val.get('procedure_validations', []):
                    f.write(f"CATEGORY: {proc.get('category', 'unknown').upper()}\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Procedure: {proc.get('procedure_description', 'N/A')}\n")
                    f.write(f"Location: {proc.get('location', 'N/A')}\n")
                    f.write(f"Accuracy Rating: {proc.get('accuracy_rating', 0)}/100\n")

                    if proc.get('issues'):
                        f.write("\nIssues Found:\n")
                        for issue in proc.get('issues', []):
                            f.write(f"  • {issue.get('type', 'unknown')}: {issue.get('description', 'N/A')}\n")
                            f.write(f"    Real World: {issue.get('real_world_version', 'N/A')}\n")
                            f.write(f"    Fix: {issue.get('suggested_fix', 'N/A')}\n")

                    if proc.get('requires_expert_consultation'):
                        f.write(f"\n⚠️  EXPERT CONSULTATION RECOMMENDED\n")

                    if proc.get('disclaimer_needed'):
                        f.write(f"⚠️  DISCLAIMER RECOMMENDED for dramatized content\n")

                    f.write("\n")

            # Timeline Validations
            if time_val.get('timeline_validations'):
                f.write("\n" + "="*70 + "\n")
                f.write("TIMELINE REALISM ANALYSIS\n")
                f.write("="*70 + "\n\n")

                for timeline in time_val.get('timeline_validations', []):
                    impact_label = {
                        'critical': '🔴 CRITICAL',
                        'moderate': '🟠 MODERATE',
                        'minor': '🟡 MINOR'
                    }.get(timeline.get('impact', 'minor'), timeline.get('impact', 'UNKNOWN'))

                    f.write(f"{impact_label}: {timeline.get('event', 'Unknown')}\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Stated Duration: {timeline.get('stated_duration', 'N/A')}\n")
                    f.write(f"Realistic Duration: {timeline.get('realistic_duration', 'N/A')}\n")
                    f.write(f"Discrepancy: {timeline.get('discrepancy', 'N/A')}\n")
                    f.write(f"Adjustment: {timeline.get('suggested_adjustment', 'N/A')}\n\n")

            # Technology Validations
            if tech_val.get('technology_validations'):
                f.write("\n" + "="*70 + "\n")
                f.write("TECHNOLOGY REALISM ANALYSIS\n")
                f.write("="*70 + "\n\n")

                for tech in tech_val.get('technology_validations', []):
                    f.write(f"TECHNOLOGY: {tech.get('technology', 'Unknown')}\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Usage: {tech.get('usage_description', 'N/A')}\n")
                    f.write(f"Location: {tech.get('location', 'N/A')}\n")
                    f.write(f"Accuracy: {tech.get('accuracy_rating', 0)}/100\n")

                    if tech.get('issues'):
                        f.write(f"Issues: {', '.join(tech.get('issues', []))}\n")

                    f.write(f"Real Capabilities: {tech.get('real_capabilities', 'N/A')}\n")
                    f.write(f"Suggested Fix: {tech.get('suggested_fix', 'N/A')}\n\n")

            # Expert Consultation Recommendations
            expert_rec = procedure_report.get('expert_consultation', {})
            if expert_rec.get('expert_consultations_recommended'):
                f.write("\n" + "="*70 + "\n")
                f.write("EXPERT CONSULTATION RECOMMENDATIONS\n")
                f.write("="*70 + "\n\n")

                for consult in expert_rec.get('expert_consultations_recommended', []):
                    priority_label = {
                        'critical': '🔴 CRITICAL',
                        'important': '🟠 IMPORTANT',
                        'helpful': '🟡 HELPFUL'
                    }.get(consult.get('priority', 'helpful'), consult.get('priority', 'UNKNOWN'))

                    f.write(f"{priority_label}: {consult.get('expertise_needed', 'Unknown')}\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Reason: {consult.get('reason', 'N/A')}\n")
                    f.write(f"Content Area: {consult.get('content_area', 'N/A')}\n")
                    f.write(f"Potential Experts: {', '.join(consult.get('potential_experts', []))}\n")

                    if consult.get('questions_to_ask'):
                        f.write("\nQuestions for Expert:\n")
                        for q in consult.get('questions_to_ask', []):
                            f.write(f"  • {q}\n")

                    f.write("\n")

            # Final Assessment
            f.write("\n" + "="*70 + "\n")
            f.write("FINAL ASSESSMENT\n")
            f.write("="*70 + "\n\n")

            status = procedure_report.get('validation_status', 'UNKNOWN')
            score = procedure_report.get('overall_realism_score', 0)

            if status == 'PASS':
                f.write("✅ VALIDATION PASSED\n")
                f.write(f"Procedural realism is strong (Score: {score}/100).\n")
                f.write("Ready to proceed to script writing.\n")
            elif status == 'WARNING':
                f.write("⚠️  VALIDATION PASSED WITH WARNINGS\n")
                f.write(f"Some procedural inaccuracies detected (Score: {score}/100).\n")
                f.write("Review and correct flagged procedures.\n")
            else:
                f.write("❌ VALIDATION FAILED\n")
                f.write(f"Significant procedural issues detected (Score: {score}/100).\n")
                f.write("Address critical issues before script writing.\n")

    def export_json(self, procedure_report: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(procedure_report, f, indent=2, ensure_ascii=False)

    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"⚖️  STATION 19: PROCEDURAL ACCURACY CHECK")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")

        try:
            await self.initialize()

            # Load dependencies
            print("📥 Loading dependencies...")
            dependencies = await self.load_dependencies()

            if not dependencies.get('episode_blueprints'):
                raise ValueError("Missing episode_blueprints from Station 14")

            print("✅ Dependencies loaded\n")

            # Run validation checks
            print("⚖️  Validating professional procedures...")
            procedure_validation = await self.validate_professional_procedures(dependencies)
            print(f"  ✅ Procedural Realism: {procedure_validation.get('overall_procedural_realism', 0)}/100\n")

            print("⏱️  Validating timeline realism...")
            timeline_validation = await self.validate_timeline_realism(dependencies)
            print(f"  ✅ Timeline Realism: {timeline_validation.get('overall_timeline_realism', 0)}/100\n")

            print("💻 Validating technology usage...")
            technology_validation = await self.validate_technology_usage(dependencies)
            print(f"  ✅ Technology Realism: {technology_validation.get('overall_tech_realism', 0)}/100\n")

            print("🎓 Identifying expert consultation needs...")
            expert_consultation = await self.identify_expert_consultation_needs(dependencies)
            print(f"  ✅ Consultation Areas: {expert_consultation.get('consultation_areas', 0)}\n")

            # Calculate overall realism score
            scores = [
                procedure_validation.get('overall_procedural_realism', 0),
                timeline_validation.get('overall_timeline_realism', 0),
                technology_validation.get('overall_tech_realism', 0)
            ]
            overall_realism_score = sum(scores) // len(scores) if scores else 0

            # Count critical issues
            critical_procedures = len([
                p for p in procedure_validation.get('procedure_validations', [])
                if p.get('accuracy_rating', 100) < 50
            ])
            critical_timelines = len([
                t for t in timeline_validation.get('timeline_validations', [])
                if t.get('impact') == 'critical'
            ])

            # Determine validation status
            if critical_procedures > 3 or critical_timelines > 3 or overall_realism_score < 60:
                validation_status = "FAIL"
            elif critical_procedures > 0 or critical_timelines > 0 or overall_realism_score < 75:
                validation_status = "WARNING"
            else:
                validation_status = "PASS"

            # Compile final report
            procedure_report = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'validation_status': validation_status,
                'overall_realism_score': overall_realism_score,
                'procedure_validation': procedure_validation,
                'timeline_validation': timeline_validation,
                'technology_validation': technology_validation,
                'expert_consultation': expert_consultation
            }

            # Export outputs
            print("💾 Exporting procedure validation report...")
            output_dir = self.output_dir
            os.makedirs(output_dir, exist_ok=True)

            base_filename = f"station19_procedure_check_{self.session_id}"

            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")

            self.export_txt(procedure_report, txt_path)
            print(f"  ✅ Text Report: {txt_path}")

            self.export_json(procedure_report, json_path)
            print(f"  ✅ JSON Data: {json_path}")

            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_19",
                json.dumps(procedure_report)
            )
            print("✅ Saved to Redis\n")

            result = {
                'station': 'station_19_procedure_check',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path
                },
                'statistics': {
                    'validation_status': validation_status,
                    'overall_realism_score': overall_realism_score,
                    'procedures_validated': procedure_validation.get('total_procedures_validated', 0),
                    'timelines_validated': timeline_validation.get('timelines_validated', 0),
                    'technologies_validated': technology_validation.get('technologies_validated', 0),
                    'expert_consultations_needed': expert_consultation.get('consultation_areas', 0)
                },
                'procedure_report': procedure_report
            }

            # Show status
            status_icon = "✅" if validation_status == "PASS" else "⚠️" if validation_status == "WARNING" else "❌"
            print(f"{'='*70}")
            print(f"{status_icon} STATION 19 COMPLETE: Procedure Check {validation_status}")
            print(f"{'='*70}\n")
            print(f"Realism Score: {overall_realism_score}/100")
            print(f"Procedures: {procedure_validation.get('total_procedures_validated', 0)}, Timelines: {timeline_validation.get('timelines_validated', 0)}\n")

            return result

        except Exception as e:
            print(f"\n❌ Error in Station 19: {str(e)}")
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
        station = Station19ProcedureCheck(session_id)
        result = await station.run()
        print("\n📊 Station 19 Results:")
        print(json.dumps(result['statistics'], indent=2))

    asyncio.run(main())
