"""
Station 24: Dialogue Polish

This station analyzes dialogue for natural speech patterns, character voice consistency,
and subtext opportunities. It automatically polishes dialogue to professional standards
while maintaining character identity and audio-first storytelling.

Flow:
1. Load Station 23 P3-enhanced scripts
2. Load Station 7 character voice profiles
3. Display episode selection and polish status
4. Human selects episode to polish
5. Execute 4 sequential LLM analysis tasks:
   - Natural speech analysis (formality, contractions, fragments)
   - Character voice validation (distinction, consistency)
   - Subtext enhancement (on-the-nose detection)
   - Auto-polish dialogue (generate polished script)
6. Display unnatural dialogue issues
7. Display voice distinction problems
8. Display subtext opportunities
9. Display polished script with comparisons
10. Human review (approve/regenerate)
11. Save polished script + comparison report
12. Save to Redis for Station 25
13. Loop option for next episode

Critical Dialogue Station - Ensures professional, character-specific dialogue
"""

import asyncio
import json
import csv
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json


class Station24DialoguePolish:
    """Station 24: Dialogue Polish"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=24)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_24'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store loaded data
        self.script_episodes = {}  # From Station 23
        self.character_profiles = {}  # From Station 7
        self.polished_episodes = set()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_24.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method with episode loop"""
        print("=" * 70)
        print("💬 STATION 24: DIALOGUE POLISH")
        print("=" * 70)
        print()

        try:
            # Step 1: Load scripts from Station 23
            print("📥 Loading P3-enhanced scripts from Station 23...")
            await self.load_scripts()
            print(f"✅ Loaded {len(self.script_episodes)} episode script(s)")
            print()

            if not self.script_episodes:
                print("❌ No scripts found. Please run Station 23 first.")
                return

            # Step 2: Load character profiles from Station 7
            print("📥 Loading character voice profiles from Station 7...")
            await self.load_character_profiles()
            print("✅ Character profiles loaded")
            print()

            # Main polishing loop
            while True:
                # Step 3: Display episode selection
                self.display_episode_selection()

                # Step 4: Human selects episode
                episode_number = self.get_episode_selection()

                if episode_number is None:
                    # User chose to exit
                    break

                # Step 5-12: Polish the selected episode
                await self.polish_episode(episode_number)

                # Step 13: Ask to continue
                if not self.ask_continue_polishing():
                    break

            # Display final summary
            self.display_session_summary()

        except Exception as e:
            print(f"❌ Station 24 failed: {str(e)}")
            logging.error(f"Station 24 error: {str(e)}", exc_info=True)
            raise

    async def load_scripts(self):
        """Load scripts from Station 23 (P3-enhanced)"""
        try:
            for episode_num in range(1, 25):
                try:
                    key = f"audiobook:{self.session_id}:station_23:episode_{episode_num:02d}"
                    data_raw = await self.redis_client.get(key)

                    if data_raw:
                        episode_data = json.loads(data_raw)
                        # Extract enhanced script from Station 23
                        twist_integration = episode_data.get('twist_integration', {})
                        full_script = twist_integration.get('full_enhanced_script', '')

                        self.script_episodes[episode_num] = {
                            'source': 'station_23',
                            'script': full_script,
                            'twist_data': twist_integration,
                            'episode_number': episode_num
                        }
                        print(f"   ✓ Episode {episode_num} (from Station 23 - P3 enhanced)")

                except Exception:
                    continue

        except Exception as e:
            raise ValueError(f"❌ Error loading scripts: {str(e)}")

    async def load_character_profiles(self):
        """Load character voice profiles from Station 7"""
        try:
            key = f"audiobook:{self.session_id}:station_7"
            data_raw = await self.redis_client.get(key)

            if data_raw:
                station7_data = json.loads(data_raw)
                self.character_profiles = station7_data.get('Character Architect Document', {})
            else:
                print("⚠️  Warning: Station 7 (Character Architect) not found")
                print("    Dialogue polish will use general principles")
                self.character_profiles = {}

        except Exception as e:
            logging.warning(f"Could not load character profiles: {str(e)}")
            self.character_profiles = {}

    def display_episode_selection(self):
        """Display episode selection menu with polish status"""
        print("=" * 70)
        print("📺 EPISODE SELECTION & DIALOGUE POLISH STATUS")
        print("=" * 70)
        print()

        print(f"Scripts Available: {len(self.script_episodes)}")
        print(f"Character Profiles Loaded: {'✅' if self.character_profiles else '⚠️  Limited'}")
        print()

        print("EPISODE DIALOGUE POLISH STATUS:")
        print("━" * 70)
        print()
        print("┌" + "─" * 68 + "┐")
        print("│ " + "Ep".ljust(4) + "Source".ljust(12) + "Chars".ljust(8) + "Status".ljust(42) + " │")
        print("├" + "─" * 68 + "┤")

        for episode_num in sorted(self.script_episodes.keys()):
            episode_data = self.script_episodes[episode_num]

            source = "St23✅"
            script = episode_data['script']
            char_count = len(script) if isinstance(script, str) else 0

            if episode_num in self.polished_episodes:
                status = "✅ DIALOGUE POLISHED"
            else:
                status = "🟡 NEEDS DIALOGUE POLISH"

            # Format row
            row = f"│ {str(episode_num).ljust(4)}{source.ljust(12)}{str(char_count)[:7].ljust(8)}{status.ljust(42)} │"
            print(row)

        print("└" + "─" * 68 + "┘")
        print()

        # Display statistics
        print("📊 DIALOGUE POLISH STATISTICS:")
        print(f"  • Total Episodes Available: {len(self.script_episodes)}")
        print(f"  • Episodes Polished: {len(self.polished_episodes)}/{len(self.script_episodes)}")
        print(f"  • Completion: {int((len(self.polished_episodes) / len(self.script_episodes)) * 100) if self.script_episodes else 0}%")
        print()
        print("=" * 70)
        print()

    def get_episode_selection(self) -> Optional[int]:
        """Get episode selection from user"""
        print("=" * 70)
        print("⭐ EPISODE SELECTION REQUIRED")
        print("=" * 70)
        print()
        print("Which episode would you like to polish dialogue?")
        print()
        print("💡 RECOMMENDATIONS:")
        print("  • Polish in chronological order for best consistency")
        print("  • Character voices should remain consistent across episodes")
        print("  • Sequential polishing helps maintain tone")
        print()

        available_episodes = sorted(self.script_episodes.keys())
        print(f"🎯 Available episodes: {', '.join(map(str, available_episodes))}")
        print()

        while True:
            try:
                choice = input(f"Enter episode number or 'Q' to quit: ").strip().upper()

                if choice == 'Q':
                    return None

                episode_num = int(choice)

                if episode_num in self.script_episodes:
                    return episode_num
                else:
                    print(f"❌ Episode {episode_num} not found. Available: {available_episodes}")

            except ValueError:
                print("❌ Invalid input. Please enter a number or 'Q'")

    async def polish_episode(self, episode_number: int):
        """Polish dialogue for a complete episode"""
        print()
        print("=" * 70)
        print(f"📥 LOADING EPISODE {episode_number} SCRIPT")
        print("=" * 70)
        print()

        # Load episode script
        episode_data = self.script_episodes[episode_number]
        script = episode_data['script']

        # Step 5: Execute 4 sequential LLM analysis tasks
        print()
        print("=" * 70)
        print("🔍 EXECUTING DIALOGUE ANALYSIS")
        print("=" * 70)
        print()

        # Task 1: Natural Speech Analysis
        print("🗣️  Task 1/4: Natural Speech Analysis...")
        natural_speech = await self.execute_natural_speech_analysis(episode_number, script)
        print("✅ Natural speech analysis complete")
        print()

        # Display unnatural dialogue issues
        self.display_unnatural_dialogue(natural_speech)

        # Task 2: Character Voice Validation
        print()
        print("🎭 Task 2/4: Character Voice Validation...")
        voice_validation = await self.execute_voice_validation(episode_number, script)
        print("✅ Voice validation complete")
        print()

        # Display voice distinction problems
        self.display_voice_problems(voice_validation)

        # Task 3: Subtext Enhancement
        print()
        print("📖 Task 3/4: Subtext Enhancement Analysis...")
        subtext_analysis = await self.execute_subtext_analysis(episode_number, script)
        print("✅ Subtext analysis complete")
        print()

        # Display subtext opportunities
        self.display_subtext_opportunities(subtext_analysis)

        # Task 4: Auto-polish dialogue
        print()
        print("✨ Task 4/4: Auto-Polish Dialogue...")
        polished_script = await self.execute_auto_polish(
            episode_number,
            script,
            natural_speech,
            voice_validation,
            subtext_analysis
        )
        print("✅ Polished script generated")
        print()

        # Display polished script with comparisons
        self.display_polished_script(episode_number, script, polished_script)

        # Human review
        if not self.skip_review:
            review_result = await self.human_review(episode_number, polished_script, script)

            if review_result == "regenerate":
                # Regenerate the polish
                polished_script = await self.execute_auto_polish(
                    episode_number,
                    script,
                    natural_speech,
                    voice_validation,
                    subtext_analysis
                )
        else:
            print("✅ Auto-accepting polished script (skip_review=True)")
            print()

        # Save outputs
        await self.save_episode_outputs(
            episode_number,
            polished_script,
            natural_speech,
            voice_validation,
            subtext_analysis
        )

        # Mark as polished
        self.polished_episodes.add(episode_number)

    async def execute_natural_speech_analysis(self, episode_number: int, script: str) -> Dict:
        """Task 1: Analyze natural speech patterns"""
        try:
            prompt = self.config.get_prompt('natural_speech_analysis')

            # Format character profiles
            character_profiles = self._format_character_profiles()

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script[:15000],  # Truncate if very long
                character_profiles=character_profiles
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            analysis_data = extract_json(response)

            return analysis_data.get('natural_speech_analysis', {})

        except Exception as e:
            print(f"❌ Natural speech analysis failed: {str(e)}")
            raise

    async def execute_voice_validation(self, episode_number: int, script: str) -> Dict:
        """Task 2: Validate character voice consistency"""
        try:
            prompt = self.config.get_prompt('character_voice_validation')

            # Format character profiles
            character_profiles = self._format_character_profiles()

            # Format prompt
            formatted_prompt = prompt.format(
                current_script=script[:15000],
                character_profiles=character_profiles
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            validation_data = extract_json(response)

            return validation_data.get('voice_validation', {})

        except Exception as e:
            print(f"❌ Voice validation failed: {str(e)}")
            raise

    async def execute_subtext_analysis(self, episode_number: int, script: str) -> Dict:
        """Task 3: Analyze subtext opportunities"""
        try:
            prompt = self.config.get_prompt('subtext_enhancement')

            # Format prompt
            formatted_prompt = prompt.format(
                current_script=script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            analysis_data = extract_json(response)

            return analysis_data.get('subtext_analysis', {})

        except Exception as e:
            print(f"❌ Subtext analysis failed: {str(e)}")
            raise

    async def execute_auto_polish(self, episode_number: int, original_script: str,
                                  natural_speech: Dict, voice_validation: Dict,
                                  subtext_analysis: Dict) -> Dict:
        """Task 4: Auto-polish dialogue"""
        try:
            prompt = self.config.get_prompt('auto_polish_dialogue')

            # Format fixes needed
            fixes_needed = self._format_fixes_needed(natural_speech, voice_validation, subtext_analysis)

            # Format character profiles
            character_profiles = self._format_character_profiles()

            # Format prompt
            formatted_prompt = prompt.format(
                original_script=original_script[:15000],
                fixes_needed=fixes_needed,
                character_profiles=character_profiles
            )

            # Execute LLM call - may take longer for rewrites
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=16384  # Higher token limit for full script rewrite
            )

            # Extract JSON
            polished_data = extract_json(response)

            return polished_data.get('dialogue_polished_script', {})

        except Exception as e:
            print(f"❌ Auto-polish dialogue failed: {str(e)}")
            raise

    def _format_character_profiles(self) -> str:
        """Format character profiles for prompts"""
        if not self.character_profiles:
            return "Character profiles not available - use general dialogue principles"

        parts = []
        characters = self.character_profiles.get('character_profiles', [])

        for char in characters:
            name = char.get('character_name', 'Unknown')
            age = char.get('age', 'Unknown')
            background = char.get('background_summary', '')
            speech_patterns = char.get('speech_patterns', {})

            parts.append(f"=== {name.upper()} ===")
            parts.append(f"Age: {age}")
            parts.append(f"Background: {background}")
            parts.append(f"Speech Patterns: {json.dumps(speech_patterns, indent=2)}")
            parts.append("")

        return "\n".join(parts)

    def _format_fixes_needed(self, natural_speech: Dict, voice_validation: Dict,
                            subtext_analysis: Dict) -> str:
        """Format all fixes needed for auto-polish prompt"""
        parts = []

        # Natural speech fixes
        parts.append("=== NATURAL SPEECH FIXES ===")
        unnatural = natural_speech.get('unnatural_instances', [])
        for issue in unnatural[:10]:  # Show first 10
            parts.append(f"Scene {issue.get('scene_number', '?')}: {issue.get('character', 'Unknown')}")
            parts.append(f"  Current: {issue.get('current_line', '')}")
            parts.append(f"  Fix: {issue.get('best_fix', '')}")
        parts.append("")

        # Voice validation fixes
        parts.append("=== CHARACTER VOICE FIXES ===")
        violations = voice_validation.get('voice_violations', [])
        for issue in violations[:10]:
            parts.append(f"Scene {issue.get('scene_number', '?')}: {issue.get('character', 'Unknown')}")
            parts.append(f"  Current: {issue.get('current_line', '')}")
            parts.append(f"  Fix: {issue.get('correct_voice', '')}")
        parts.append("")

        # Subtext enhancements
        parts.append("=== SUBTEXT ENHANCEMENTS ===")
        on_the_nose = subtext_analysis.get('on_the_nose_examples', [])
        for issue in on_the_nose[:10]:
            parts.append(f"Scene {issue.get('scene_number', '?')}")
            parts.append(f"  Current: {issue.get('current_dialogue', '')}")
            parts.append(f"  Subtext version: {issue.get('subtext_version', '')}")
        parts.append("")

        return "\n".join(parts)

    def display_unnatural_dialogue(self, natural_speech: Dict):
        """Display unnatural dialogue issues"""
        print("=" * 70)
        print("🗣️  NATURAL SPEECH ANALYSIS")
        print("=" * 70)
        print()

        unnatural = natural_speech.get('unnatural_instances', [])
        total_issues = natural_speech.get('total_issues', len(unnatural))

        print(f"⚠️  UNNATURAL DIALOGUE FOUND: {total_issues} instances")
        print()

        for i, issue in enumerate(unnatural[:5], 1):  # Show first 5
            issue_type = issue.get('issue_type', 'unknown').replace('_', ' ').upper()
            scene_num = issue.get('scene_number', '?')
            character = issue.get('character', 'Unknown')
            current_line = issue.get('current_line', '')
            problem = issue.get('problem', '')
            best_fix = issue.get('best_fix', '')

            print(f"ISSUE {i}: {issue_type} (Scene {scene_num})")
            print("─" * 70)
            print(f"Character: {character}")
            print(f"Line: \"{current_line}\"")
            print()
            print(f"PROBLEM: {problem}")
            print()
            print(f"SUGGESTED FIX:")
            print(f"\"{best_fix}\"")
            print()
            print("━" * 70)
            print()

        if len(unnatural) > 5:
            print(f"... and {len(unnatural) - 5} more issues")
            print()

        # Show principles violated
        principles = natural_speech.get('principles_violated', {})
        print("NATURAL SPEECH PRINCIPLES VIOLATED:")
        for principle, count in principles.items():
            print(f"  ✗ {principle.replace('_', ' ').title()}: {count} instances")
        print()
        print("=" * 70)
        print()

    def display_voice_problems(self, voice_validation: Dict):
        """Display character voice distinction problems"""
        print("=" * 70)
        print("🎭 CHARACTER VOICE VALIDATION")
        print("=" * 70)
        print()

        # Voice distinction test
        test = voice_validation.get('voice_distinction_test', {})
        score = test.get('distinction_score', 'Unknown')

        print("VOICE DISTINCTION TEST:")
        print("━" * 70)
        print(f"Score: {score}")
        print()

        problem_pairs = test.get('problem_pairs', [])
        for pair in problem_pairs:
            chars = pair.get('characters', [])
            issue = pair.get('issue', '')
            print(f"⚠️  {' & '.join(chars)}: {issue}")
        print()

        # Voice violations
        violations = voice_validation.get('voice_violations', [])
        if violations:
            print("CHARACTER VOICE VIOLATIONS:")
            print("━" * 70)
            for i, violation in enumerate(violations[:3], 1):
                char = violation.get('character', 'Unknown')
                scene = violation.get('scene_number', '?')
                current = violation.get('current_line', '')
                correct = violation.get('correct_voice', '')

                print(f"{i}. {char} (Scene {scene})")
                print(f"   Current: \"{current[:60]}...\"")
                print(f"   Correct: \"{correct}\"")
                print()

        print("=" * 70)
        print()

    def display_subtext_opportunities(self, subtext_analysis: Dict):
        """Display subtext enhancement opportunities"""
        print("=" * 70)
        print("📖 SUBTEXT ENHANCEMENT")
        print("=" * 70)
        print()

        current_level = subtext_analysis.get('current_subtext_level', 'Unknown')
        target_level = subtext_analysis.get('target_subtext_level', '7-8/10')

        print(f"Current subtext level: {current_level}")
        print(f"Target subtext level: {target_level}")
        print()

        examples = subtext_analysis.get('on_the_nose_examples', [])
        total = subtext_analysis.get('total_opportunities', len(examples))

        print(f"ON-THE-NOSE EXAMPLES: {total} found")
        print("━" * 70)
        print()

        for i, example in enumerate(examples[:3], 1):
            scene = example.get('scene_number', '?')
            current = example.get('current_dialogue', '')
            subtext_ver = example.get('subtext_version', '')
            why_better = example.get('why_better', '')

            print(f"EXAMPLE {i} (Scene {scene}):")
            print(f"Current (on-the-nose): {current}")
            print()
            print(f"Subtext version: {subtext_ver}")
            print()
            print(f"Why better: {why_better}")
            print()
            print("─" * 70)
            print()

        print("=" * 70)
        print()

    def display_polished_script(self, episode_number: int, original: str, polished: Dict):
        """Display polished script with comparisons"""
        print("=" * 70)
        print(f"✅ EPISODE {episode_number}: DIALOGUE-POLISHED SCRIPT")
        print("=" * 70)
        print()

        total_changes = polished.get('total_changes', 0)
        word_change = polished.get('word_count_change', '+0 words')
        subtext_before = polished.get('subtext_level_before', 'Unknown')
        subtext_after = polished.get('subtext_level_after', 'Unknown')
        voice_before = polished.get('voice_distinction_before', 'Unknown')
        voice_after = polished.get('voice_distinction_after', 'Unknown')

        print("DIALOGUE POLISH STATISTICS:")
        print("━" * 70)
        print(f"  • Total Changes: {total_changes}")
        print(f"  • Word Count Change: {word_change}")
        print(f"  • Subtext Level: {subtext_before} → {subtext_after}")
        print(f"  • Voice Distinction: {voice_before} → {voice_after}")
        print()

        # Show sample changes
        scenes = polished.get('scenes', [])
        if scenes and len(scenes) > 0:
            first_scene = scenes[0]
            changes = first_scene.get('changes_in_scene', [])

            if changes:
                print("SAMPLE CHANGES (First Scene):")
                print("━" * 70)
                for change in changes[:3]:
                    char = change.get('character', 'Unknown')
                    original_line = change.get('original', '')
                    polished_line = change.get('polished', '')
                    change_type = change.get('change_type', 'unknown')

                    print(f"[{change_type.upper()}] {char}:")
                    print(f"  Before: \"{original_line}\"")
                    print(f"  After:  \"{polished_line}\"")
                    print()

        print("=" * 70)
        print()

    async def human_review(self, episode_number: int, polished: Dict, original: str) -> str:
        """Human review interface"""
        print("=" * 70)
        print("⭐ DIALOGUE-POLISHED SCRIPT REVIEW")
        print("=" * 70)
        print()

        total_changes = polished.get('total_changes', 0)

        print(f"Episode {episode_number} dialogue polish complete:")
        print(f"  • {total_changes} dialogue improvements made")
        print()
        print("OPTIONS:")
        print("  [Enter] - Approve and save (recommended)")
        print("  [R]     - Regenerate dialogue polish")
        print("  [V]     - View complete polished script")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == 'R':
            return "regenerate"
        elif choice == 'V':
            self.display_full_script(polished)
            return await self.human_review(episode_number, polished, original)
        else:
            print("✅ Polished script approved. Saving files...")
            print()
            return "approved"

    def display_full_script(self, polished: Dict):
        """Display complete polished script"""
        complete_script = polished.get('complete_polished_script', '')

        print("\n" + "=" * 70)
        print("COMPLETE POLISHED SCRIPT")
        print("=" * 70 + "\n")

        # Display script (truncate if very long)
        if len(complete_script) > 5000:
            print(complete_script[:5000])
            print("\n... (script continues) ...\n")
        else:
            print(complete_script)

        input("\nPress Enter to return to review menu...")

    async def save_episode_outputs(self, episode_number: int, polished: Dict,
                                   natural_speech: Dict, voice_validation: Dict,
                                   subtext_analysis: Dict):
        """Save episode in multiple formats"""
        print()
        print("=" * 70)
        print("💾 SAVING DIALOGUE-POLISHED FILES")
        print("=" * 70)
        print()

        # Create episode subdirectory
        episode_dir = self.output_dir / f"episode_{episode_number:02d}"
        episode_dir.mkdir(exist_ok=True)

        # 1. Save JSON with all analysis + polished script
        json_filename = f"episode_{episode_number:02d}_dialogue_polished.json"
        json_path = episode_dir / json_filename

        full_data = {
            'session_id': self.session_id,
            'episode_number': episode_number,
            'polished_at': datetime.now().isoformat(),
            'natural_speech_analysis': natural_speech,
            'voice_validation': voice_validation,
            'subtext_analysis': subtext_analysis,
            'dialogue_polished_script': polished
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_path}")

        # 2. Save Polished Script (Plain Text)
        txt_filename = f"episode_{episode_number:02d}_dialogue_polished.txt"
        txt_path = episode_dir / txt_filename

        txt_content = polished.get('complete_polished_script', '')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print(f"✅ Saved Polished Script: {txt_path}")

        # 3. Save Comparison Report
        report_filename = f"episode_{episode_number:02d}_dialogue_changes.txt"
        report_path = episode_dir / report_filename

        report_content = self.generate_comparison_report(episode_number, natural_speech,
                                                         voice_validation, subtext_analysis, polished)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Saved Comparison Report: {report_path}")

        # 4. Save to Redis for Station 25
        redis_key = f"audiobook:{self.session_id}:station_24:episode_{episode_number:02d}"
        await self.redis_client.set(redis_key, json.dumps(full_data), expire=604800)  # 7 days
        print(f"✅ Saved to Redis: {redis_key}")

        print()

    def generate_comparison_report(self, episode_number: int, natural_speech: Dict,
                                  voice_validation: Dict, subtext_analysis: Dict,
                                  polished: Dict) -> str:
        """Generate comprehensive comparison report"""
        lines = []

        lines.append("=" * 70)
        lines.append(f"EPISODE {episode_number} DIALOGUE POLISH - COMPARISON REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Session: {self.session_id}")
        lines.append("")

        # Natural Speech Summary
        lines.append("NATURAL SPEECH ANALYSIS:")
        lines.append("━" * 70)
        total_issues = natural_speech.get('total_issues', 0)
        lines.append(f"  Unnatural instances found: {total_issues}")
        lines.append("")

        # Voice Validation Summary
        lines.append("CHARACTER VOICE VALIDATION:")
        lines.append("━" * 70)
        test = voice_validation.get('voice_distinction_test', {})
        score = test.get('distinction_score', 'Unknown')
        lines.append(f"  Voice distinction score: {score}")
        lines.append("")

        # Subtext Summary
        lines.append("SUBTEXT ENHANCEMENT:")
        lines.append("━" * 70)
        current_level = subtext_analysis.get('current_subtext_level', 'Unknown')
        target_level = subtext_analysis.get('target_subtext_level', 'Unknown')
        lines.append(f"  Current subtext level: {current_level}")
        lines.append(f"  Target subtext level: {target_level}")
        lines.append("")

        # Polish Summary
        lines.append("DIALOGUE POLISH RESULTS:")
        lines.append("━" * 70)
        total_changes = polished.get('total_changes', 0)
        word_change = polished.get('word_count_change', '+0 words')
        lines.append(f"  Total changes: {total_changes}")
        lines.append(f"  Word count change: {word_change}")
        lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def ask_continue_polishing(self) -> bool:
        """Ask if user wants to continue polishing"""
        print()
        print("=" * 70)
        print("⭐ CONTINUE DIALOGUE POLISH?")
        print("=" * 70)
        print()
        print(f"Episodes polished: {len(self.polished_episodes)}/{len(self.script_episodes)}")
        print()
        print("OPTIONS:")
        print("  [Y] - Polish another episode")
        print("  [N] - Finish for now")
        print()

        choice = input("Your choice (Y/N): ").strip().upper()

        return choice == 'Y'

    def display_session_summary(self):
        """Display session summary"""
        print()
        print("=" * 70)
        print("📊 SESSION SUMMARY")
        print("=" * 70)
        print()
        print(f"Episodes polished: {len(self.polished_episodes)}/{len(self.script_episodes)}")
        for ep_num in sorted(self.polished_episodes):
            print(f"  ✅ Episode {ep_num}")
        print()
        print(f"Session ID: {self.session_id}")
        print()
        print("Your progress has been saved.")
        print("Resume dialogue polish anytime by running Station 24 again.")
        print()
        print("Next Steps:")
        print("  1. Continue polishing remaining episodes (Station 24)")
        print("  2. OR proceed to Station 25 (Audio Optimization)")
        print()
        print("=" * 70)
        print()


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station24DialoguePolish(session_id, skip_review=False)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
