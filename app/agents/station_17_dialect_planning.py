"""
Station 17: Dialect Planning Agent

This agent validates character voice consistency and ensures age-appropriate
language across the audiobook series before script writing begins.

Dependencies: Stations 3, 6, 8, 15
Outputs: Dialect consistency validation report (TXT, JSON)
Human Gate: None - validation gate before script writing
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient


class Station17DialectPlanning:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_17_dialect_planning"

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()

    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from previous stations"""
        dependencies = {}

        # Load required stations
        station_keys = {
            'station_03': 'age_genre',
            'station_06': 'style_guide',
            'station_08': 'character_bible',
            'station_15': 'detailed_outlines'
        }

        for redis_key, dependency_name in station_keys.items():
            raw_data = await self.redis_client.get(f"audiobook:{self.session_id}:{redis_key}")
            if raw_data:
                dependencies[dependency_name] = json.loads(raw_data)

        return dependencies

    async def validate_character_voice_consistency(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate character voice patterns using LLM"""

        character_bible = dependencies.get('character_bible', {})
        style_guide = dependencies.get('style_guide', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        characters_summary = json.dumps({
            'tier1_protagonists': character_bible.get('tier1_protagonists', []),
            'tier2_supporting': character_bible.get('tier2_supporting', [])
        }, indent=2)[:3000]

        style_summary = json.dumps({
            'dialect_accent_map': style_guide.get('dialect_accent_map', {}),
            'dialogue_principles': style_guide.get('dialogue_principles', {})
        }, indent=2)[:2000]

        # Safely extract outlines
        outlines_episodes = detailed_outlines.get('episodes', [])
        if isinstance(outlines_episodes, list):
            outlines_sample = outlines_episodes[:5]
        else:
            outlines_sample = []

        episodes_summary = json.dumps({
            'outlines': outlines_sample
        }, indent=2)[:4000]

        prompt = f"""
You are a Dialect & Voice Consistency Validator analyzing character speech patterns across an audiobook series.

CHARACTER BIBLE (Station 8):
{characters_summary}

STYLE GUIDE (Station 6):
{style_summary}

EPISODE OUTLINES (Station 15):
{episodes_summary}

Perform COMPREHENSIVE CHARACTER VOICE ANALYSIS for each main character:

1. VOICE PATTERN CONSISTENCY:
   - Does each character have a distinct, recognizable voice?
   - Speech patterns consistent across all episodes?
   - Vocabulary choices match character background/education?
   - Sentence structure reflects personality?

2. DIALECT CONSISTENCY:
   - If character has accent/dialect, is it maintained consistently?
   - Regional language patterns appropriate and sustained?
   - No accidental dialect shifts or breaks?

3. SPEECH RHYTHMS:
   - Character speaking tempo consistent?
   - Pause patterns match personality?
   - Verbal tics/habits maintained?

4. EMOTIONAL RANGE:
   - Character expresses emotions in character-appropriate ways?
   - Emotional vocabulary fits character development level?
   - Voice changes under stress remain in character?

For EACH CHARACTER, generate a voice profile with:
- Character name
- Voice consistency score (0-100)
- Dialect type: "formal", "casual", "regional", "technical", "mixed"
- Signature phrases: list of recurring character-specific phrases
- Speech patterns: sentence length, formality level, emotion range
- Issues: any inconsistencies found (type, description, episodes)

Generate as detailed JSON structure.

Expected JSON format:
{{
  "character_voice_profiles": [
    {{
      "character_name": "Character Name",
      "voice_consistency_score": 85,
      "dialect_type": "casual",
      "vocabulary_level": "middle-grade",
      "signature_phrases": ["phrase1", "phrase2"],
      "speech_patterns": {{
        "sentence_length": "medium",
        "formality": 60,
        "emotion_range": ["joy", "fear", "anger"]
      }},
      "issues": [
        {{
          "type": "dialect_shift",
          "description": "Character accent drops in Episode 5",
          "episodes": [5],
          "recommended_fix": "Maintain consistent dialect throughout"
        }}
      ]
    }}
  ],
  "overall_voice_consistency": 88
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'character_voice_profiles': [],
            'overall_voice_consistency': 0
        })

    async def validate_age_appropriateness(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate age-appropriate language using LLM"""

        age_genre = dependencies.get('age_genre', {})
        character_bible = dependencies.get('character_bible', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        age_guidelines = json.dumps({
            'age_guidelines': age_genre.get('age_guidelines', {}),
            'target_age': age_genre.get('target_age', 'unknown')
        }, indent=2)[:1500]

        # Safely extract outlines
        outlines_episodes = detailed_outlines.get('episodes', [])
        if isinstance(outlines_episodes, list):
            outlines_sample = outlines_episodes[:5]
        else:
            outlines_sample = []

        episodes_summary = json.dumps({
            'outlines': outlines_sample
        }, indent=2)[:4000]

        prompt = f"""
You are an Age-Appropriateness Validator analyzing language suitability for the target audience.

AGE GUIDELINES (Station 3):
{age_guidelines}

EPISODE OUTLINES (Station 15):
{episodes_summary}

Perform COMPREHENSIVE AGE-APPROPRIATENESS ANALYSIS:

1. VOCABULARY COMPLEXITY:
   - Word choices appropriate for target age group?
   - No overly complex or obscure words?
   - Reading level matches target audience?

2. SENTENCE STRUCTURE:
   - Sentence complexity appropriate?
   - Too simple/complex for age group?
   - Variety in sentence structures?

3. CONCEPTUAL COMPLEXITY:
   - Ideas and themes age-appropriate?
   - Abstract concepts explained sufficiently?
   - Emotional complexity matches developmental level?

4. CONTENT APPROPRIATENESS:
   - No inappropriate themes/language for age group?
   - Violence/scary content within acceptable bounds?
   - Relationship complexity age-appropriate?

5. ENGAGEMENT LEVEL:
   - Language engaging for target age?
   - Pacing appropriate?
   - Tone matches audience expectations?

For EACH ISSUE found, provide:
- Type: "vocabulary", "sentence_structure", "concept_complexity", "content", "engagement"
- Severity: "critical", "major", "minor"
- Description: specific concern
- Episodes affected
- Recommended fix: age-appropriate alternative

Generate as detailed JSON structure.

Expected JSON format:
{{
  "age_appropriateness_score": 90,
  "target_age_group": "middle-grade",
  "vocabulary_level": "appropriate",
  "issues": [
    {{
      "type": "vocabulary",
      "severity": "minor",
      "description": "Word 'obfuscate' may be too complex for target age",
      "episodes": [3],
      "recommended_fix": "Replace with 'confuse' or 'hide'"
    }}
  ],
  "approved_vocabulary_examples": ["word1", "word2", "word3"]
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'age_appropriateness_score': 0,
            'target_age_group': 'unknown',
            'vocabulary_level': 'unknown',
            'issues': [],
            'approved_vocabulary_examples': []
        })

    async def validate_dialect_consistency_across_episodes(self, dependencies: Dict) -> Dict[str, Any]:
        """Validate dialect patterns across all episodes using LLM"""

        character_bible = dependencies.get('character_bible', {})
        detailed_outlines = dependencies.get('detailed_outlines', {})

        # Safely extract protagonists
        protagonists = character_bible.get('tier1_protagonists', [])
        if isinstance(protagonists, list):
            protagonists_sample = protagonists[:3]
        else:
            protagonists_sample = []

        characters_summary = json.dumps({
            'protagonists': protagonists_sample
        }, indent=2)[:2000]

        # Safely extract all episodes
        all_episodes = detailed_outlines.get('episodes', [])
        if isinstance(all_episodes, list):
            episodes_sample = all_episodes
        else:
            episodes_sample = []

        episodes_summary = json.dumps({
            'all_episodes': episodes_sample
        }, indent=2)[:5000]

        prompt = f"""
You are a Cross-Episode Dialect Validator analyzing speech consistency throughout the entire series.

MAIN CHARACTERS:
{characters_summary}

ALL EPISODE OUTLINES:
{episodes_summary}

Perform CROSS-EPISODE DIALECT CONSISTENCY ANALYSIS:

1. CHARACTER-SPECIFIC ANALYSIS:
   For each main character, check:
   - Consistent dialect/accent usage from first to last episode?
   - Vocabulary evolution matches character arc?
   - Speech patterns remain recognizable?
   - No unexplained voice changes?

2. DIALOGUE MARKERS:
   - Signature phrases appear appropriately?
   - Character-specific verbal tics maintained?
   - Speaking style matches emotional state?

3. REGIONAL CONSISTENCY:
   - If characters from same region, do they share speech patterns?
   - Regional dialects geographically consistent?
   - No mixing of incompatible dialects?

4. TEMPORAL CONSISTENCY:
   - Speech appropriate for story time period?
   - Language evolution logical if time passes?
   - Slang/colloquialisms era-appropriate?

Generate detailed analysis with specific episode references.

Expected JSON format:
{{
  "cross_episode_consistency_score": 87,
  "characters_analyzed": 5,
  "episodes_analyzed": 10,
  "consistency_issues": [
    {{
      "character": "Character Name",
      "issue_type": "dialect_shift",
      "description": "Character loses accent in Episodes 5-7",
      "episodes": [5, 6, 7],
      "severity": "major",
      "recommended_fix": "Maintain consistent accent across all episodes"
    }}
  ],
  "positive_notes": [
    "Character A maintains distinctive speech throughout",
    "Regional dialects well-differentiated"
  ]
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'cross_episode_consistency_score': 0,
            'characters_analyzed': 0,
            'episodes_analyzed': 0,
            'consistency_issues': [],
            'positive_notes': []
        })

    async def generate_approved_vocabulary_bank(self, dependencies: Dict) -> Dict[str, Any]:
        """Generate age-appropriate vocabulary bank for each character using LLM"""

        age_genre = dependencies.get('age_genre', {})
        character_bible = dependencies.get('character_bible', {})

        age_guidelines = json.dumps({
            'age_guidelines': age_genre.get('age_guidelines', {}),
            'target_age': age_genre.get('target_age', 'unknown')
        }, indent=2)[:1500]

        # Safely extract and combine characters
        tier1 = character_bible.get('tier1_protagonists', [])
        tier2 = character_bible.get('tier2_supporting', [])

        if isinstance(tier1, list) and isinstance(tier2, list):
            all_characters = tier1 + tier2[:3]
        elif isinstance(tier1, list):
            all_characters = tier1
        elif isinstance(tier2, list):
            all_characters = tier2[:3]
        else:
            all_characters = []

        characters_summary = json.dumps({
            'all_characters': all_characters
        }, indent=2)[:3000]

        prompt = f"""
You are a Vocabulary Bank Generator creating age-appropriate word lists for character dialogue.

AGE GUIDELINES:
{age_guidelines}

CHARACTERS:
{characters_summary}

Generate CHARACTER-SPECIFIC VOCABULARY BANKS:

For EACH CHARACTER, create approved vocabulary lists:

1. CORE VOCABULARY:
   - 20-30 words that fit character's background, education, personality
   - All words age-appropriate for target audience
   - Words reflect character's profession/interests

2. EMOTIONAL VOCABULARY:
   - 10-15 emotion words character would naturally use
   - Match character's emotional intelligence level
   - Age-appropriate expression of feelings

3. SIGNATURE PHRASES:
   - 5-10 character-specific catchphrases or expressions
   - Memorable and distinctive
   - Appropriate for audio format

4. TECHNICAL/SPECIALIZED TERMS:
   - If character has expertise, provide 10-15 specialized terms
   - Explained or contextual for younger audiences
   - Used naturally, not forced

5. WORDS TO AVOID:
   - 5-10 words that would be OUT of character
   - Too complex/simple for this character
   - Anachronistic or inappropriate

Generate comprehensive vocabulary banks for script writers.

Expected JSON format:
{{
  "vocabulary_banks": [
    {{
      "character_name": "Character Name",
      "core_vocabulary": ["word1", "word2", ...],
      "emotional_vocabulary": ["happy", "frustrated", ...],
      "signature_phrases": ["phrase1", "phrase2", ...],
      "technical_terms": ["term1", "term2", ...],
      "words_to_avoid": ["word1", "word2", ...]
    }}
  ],
  "general_age_appropriate_words": ["common", "appropriate", "words", ...]
}}
"""

        response = await self.openrouter.process_message(prompt, "qwen-72b")
        return self._parse_json_response(response, {
            'vocabulary_banks': [],
            'general_age_appropriate_words': []
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

    def export_txt(self, dialect_report: Dict, filepath: str):
        """Export human-readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("STATION 17: DIALECT PLANNING & VOICE CONSISTENCY REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Validation Status: {dialect_report.get('validation_status', 'UNKNOWN')}\n\n")

            # Summary
            f.write("VALIDATION SUMMARY\n")
            f.write("-"*70 + "\n")
            f.write(f"Overall Voice Consistency: {dialect_report.get('voice_validation', {}).get('overall_voice_consistency', 0)}/100\n")
            f.write(f"Age Appropriateness Score: {dialect_report.get('age_validation', {}).get('age_appropriateness_score', 0)}/100\n")
            f.write(f"Cross-Episode Consistency: {dialect_report.get('dialect_consistency', {}).get('cross_episode_consistency_score', 0)}/100\n")
            f.write(f"Total Issues: {dialect_report.get('total_issues', 0)}\n\n")

            # Character Voice Profiles
            f.write("\n" + "="*70 + "\n")
            f.write("CHARACTER VOICE PROFILES\n")
            f.write("="*70 + "\n\n")

            for profile in dialect_report.get('character_voice_profiles', []):
                f.write(f"CHARACTER: {profile.get('character_name', 'Unknown')}\n")
                f.write("-"*70 + "\n")
                f.write(f"Voice Consistency Score: {profile.get('voice_consistency_score', 0)}/100\n")
                f.write(f"Dialect Type: {profile.get('dialect_type', 'N/A')}\n")
                f.write(f"Vocabulary Level: {profile.get('vocabulary_level', 'N/A')}\n")

                if profile.get('signature_phrases'):
                    f.write(f"Signature Phrases: {', '.join(profile.get('signature_phrases', []))}\n")

                speech = profile.get('speech_patterns', {})
                f.write(f"Speech Patterns:\n")
                f.write(f"  - Sentence Length: {speech.get('sentence_length', 'N/A')}\n")
                f.write(f"  - Formality: {speech.get('formality', 'N/A')}\n")
                f.write(f"  - Emotion Range: {', '.join(speech.get('emotion_range', []))}\n")

                if profile.get('issues'):
                    f.write(f"Issues Found: {len(profile.get('issues', []))}\n")
                    for issue in profile.get('issues', []):
                        f.write(f"  • {issue.get('type', 'unknown')}: {issue.get('description', 'N/A')}\n")

                f.write("\n")

            # Age Appropriateness
            f.write("\n" + "="*70 + "\n")
            f.write("AGE APPROPRIATENESS ANALYSIS\n")
            f.write("="*70 + "\n\n")
            age_val = dialect_report.get('age_validation', {})
            f.write(f"Target Age Group: {age_val.get('target_age_group', 'N/A')}\n")
            f.write(f"Vocabulary Level: {age_val.get('vocabulary_level', 'N/A')}\n")
            f.write(f"Appropriateness Score: {age_val.get('age_appropriateness_score', 0)}/100\n\n")

            if age_val.get('issues'):
                f.write("Issues Requiring Attention:\n")
                f.write("-"*70 + "\n")
                for issue in age_val.get('issues', []):
                    f.write(f"• [{issue.get('severity', 'unknown').upper()}] {issue.get('type', 'unknown')}\n")
                    f.write(f"  Description: {issue.get('description', 'N/A')}\n")
                    f.write(f"  Episodes: {', '.join(map(str, issue.get('episodes', [])))}\n")
                    f.write(f"  Fix: {issue.get('recommended_fix', 'N/A')}\n\n")

            # Vocabulary Banks
            f.write("\n" + "="*70 + "\n")
            f.write("APPROVED VOCABULARY BANKS\n")
            f.write("="*70 + "\n\n")

            for vocab_bank in dialect_report.get('vocabulary_banks', []):
                f.write(f"CHARACTER: {vocab_bank.get('character_name', 'Unknown')}\n")
                f.write("-"*70 + "\n")

                if vocab_bank.get('core_vocabulary'):
                    f.write(f"Core Vocabulary: {', '.join(vocab_bank.get('core_vocabulary', [])[:15])}\n")

                if vocab_bank.get('emotional_vocabulary'):
                    f.write(f"Emotional Vocabulary: {', '.join(vocab_bank.get('emotional_vocabulary', []))}\n")

                if vocab_bank.get('signature_phrases'):
                    f.write(f"Signature Phrases: {', '.join(vocab_bank.get('signature_phrases', []))}\n")

                if vocab_bank.get('words_to_avoid'):
                    f.write(f"Words to Avoid: {', '.join(vocab_bank.get('words_to_avoid', []))}\n")

                f.write("\n")

            # Final Assessment
            f.write("\n" + "="*70 + "\n")
            f.write("FINAL ASSESSMENT\n")
            f.write("="*70 + "\n\n")

            status = dialect_report.get('validation_status', 'UNKNOWN')
            if status == 'PASS':
                f.write("✅ VALIDATION PASSED\n")
                f.write("Character voices are consistent and age-appropriate.\n")
                f.write("Ready to proceed to script writing phase.\n")
            elif status == 'WARNING':
                f.write("⚠️  VALIDATION PASSED WITH WARNINGS\n")
                f.write("Minor voice inconsistencies detected.\n")
                f.write("Review warnings before script writing.\n")
            else:
                f.write("❌ VALIDATION FAILED\n")
                f.write("Critical voice/language issues must be resolved.\n")
                f.write("Address all issues and re-run validation.\n")

    def export_json(self, dialect_report: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dialect_report, f, indent=2, ensure_ascii=False)

    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"🗣️  STATION 17: DIALECT PLANNING & VOICE CONSISTENCY")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")

        try:
            await self.initialize()

            # Load dependencies
            print("📥 Loading dependencies...")
            dependencies = await self.load_dependencies()

            if not dependencies.get('character_bible'):
                raise ValueError("Missing character_bible from Station 8")
            if not dependencies.get('age_genre'):
                raise ValueError("Missing age_genre from Station 3")

            print("✅ Dependencies loaded\n")

            # Run validation checks
            print("🎭 Validating character voice consistency...")
            voice_validation = await self.validate_character_voice_consistency(dependencies)
            print(f"  ✅ Voice Consistency: {voice_validation.get('overall_voice_consistency', 0)}/100\n")

            print("👶 Validating age-appropriate language...")
            age_validation = await self.validate_age_appropriateness(dependencies)
            print(f"  ✅ Age Appropriateness: {age_validation.get('age_appropriateness_score', 0)}/100\n")

            print("📊 Validating dialect consistency across episodes...")
            dialect_consistency = await self.validate_dialect_consistency_across_episodes(dependencies)
            print(f"  ✅ Cross-Episode Consistency: {dialect_consistency.get('cross_episode_consistency_score', 0)}/100\n")

            print("📚 Generating approved vocabulary banks...")
            vocabulary_banks = await self.generate_approved_vocabulary_bank(dependencies)
            print(f"  ✅ Vocabulary Banks: {len(vocabulary_banks.get('vocabulary_banks', []))} characters\n")

            # Compile all issues
            all_issues = []
            for profile in voice_validation.get('character_voice_profiles', []):
                all_issues.extend(profile.get('issues', []))
            all_issues.extend(age_validation.get('issues', []))
            all_issues.extend(dialect_consistency.get('consistency_issues', []))

            # Calculate overall score
            scores = [
                voice_validation.get('overall_voice_consistency', 0),
                age_validation.get('age_appropriateness_score', 0),
                dialect_consistency.get('cross_episode_consistency_score', 0)
            ]
            overall_score = sum(scores) // len(scores) if scores else 0

            # Determine validation status
            critical_count = len([i for i in all_issues if i.get('severity') == 'critical'])
            major_count = len([i for i in all_issues if i.get('severity') == 'major'])

            if critical_count > 0:
                validation_status = "FAIL"
            elif major_count > 0 or overall_score < 80:
                validation_status = "WARNING"
            else:
                validation_status = "PASS"

            # Compile final report
            dialect_report = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'validation_status': validation_status,
                'overall_score': overall_score,
                'total_issues': len(all_issues),
                'voice_validation': voice_validation,
                'age_validation': age_validation,
                'dialect_consistency': dialect_consistency,
                'character_voice_profiles': voice_validation.get('character_voice_profiles', []),
                'vocabulary_banks': vocabulary_banks.get('vocabulary_banks', []),
                'language_consistency_issues': all_issues
            }

            # Export outputs
            print("💾 Exporting dialect planning report...")
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)

            base_filename = f"station17_dialect_planning_{self.session_id}"

            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")

            self.export_txt(dialect_report, txt_path)
            print(f"  ✅ Text Report: {txt_path}")

            self.export_json(dialect_report, json_path)
            print(f"  ✅ JSON Data: {json_path}")

            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_17",
                json.dumps(dialect_report)
            )
            print("✅ Saved to Redis\n")

            result = {
                'station': 'station_17_dialect_planning',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path
                },
                'statistics': {
                    'validation_status': validation_status,
                    'overall_score': overall_score,
                    'total_issues': len(all_issues),
                    'critical_issues': critical_count,
                    'major_issues': major_count,
                    'characters_analyzed': len(voice_validation.get('character_voice_profiles', []))
                },
                'dialect_report': dialect_report
            }

            # Show status
            status_icon = "✅" if validation_status == "PASS" else "⚠️" if validation_status == "WARNING" else "❌"
            print(f"{'='*70}")
            print(f"{status_icon} STATION 17 COMPLETE: Dialect Planning {validation_status}")
            print(f"{'='*70}\n")
            print(f"Overall Score: {overall_score}/100")
            print(f"Issues: {len(all_issues)} ({critical_count} critical, {major_count} major)\n")

            return result

        except Exception as e:
            print(f"\n❌ Error in Station 17: {str(e)}")
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
        station = Station17DialectPlanning(session_id)
        result = await station.run()
        print("\n📊 Station 17 Results:")
        print(json.dumps(result['statistics'], indent=2))

    asyncio.run(main())
