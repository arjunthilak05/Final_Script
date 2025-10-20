"""
Station 22: Momentum Check

This station analyzes first drafts for pacing and momentum issues, then automatically
fixes detected problems. It validates energy flow, repetition, and rhythm to ensure
engaging audio storytelling.

Flow:
1. Load Station 21 first drafts
2. Display episode selection and analysis status
3. Human selects episode to analyze
4. Execute 4 sequential LLM analysis tasks:
   - Pacing analysis (slow sections, rushed transitions, dead air)
   - Repetition detection (word/phrase patterns, structural repetition)
   - Energy flow analysis (tension/release balance, emotional pacing)
   - Auto-fix momentum (generate corrected script)
5. Display detected issues with examples
6. Display corrected draft with changes highlighted
7. Human review (approve/regenerate/edit)
8. Save corrected script + change report
9. Save to Redis for Station 23
10. Loop option for next episode

Critical Quality Control Station - Ensures professional pacing
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


class Station22MomentumCheck:
    """Station 22: Momentum Check"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=22)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_22'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store loaded data
        self.drafted_episodes = {}
        self.checked_episodes = set()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_22.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method with episode loop"""
        print("=" * 70)
        print("⚡ STATION 22: MOMENTUM CHECK")
        print("=" * 70)
        print()

        try:
            # Step 1: Load Station 21 first drafts
            print("📥 Loading first drafts from Station 21...")
            await self.load_first_drafts()
            print(f"✅ Loaded {len(self.drafted_episodes)} first draft(s)")
            print()

            if not self.drafted_episodes:
                print("❌ No first drafts found. Please run Station 21 first.")
                return

            # Main checking loop
            while True:
                # Step 2: Display episode selection
                self.display_episode_selection()

                # Step 3: Human selects episode
                episode_number = self.get_episode_selection()

                if episode_number is None:
                    # User chose to exit
                    break

                # Step 4-9: Analyze and fix the selected episode
                await self.check_episode(episode_number)

                # Step 10: Ask to continue
                if not self.ask_continue_checking():
                    break

            # Display final summary
            self.display_session_summary()

        except Exception as e:
            print(f"❌ Station 22 failed: {str(e)}")
            logging.error(f"Station 22 error: {str(e)}", exc_info=True)
            raise

    async def load_first_drafts(self):
        """Load all first drafts from Station 21"""
        try:
            # Get all Station 21 keys from Redis
            pattern = f"audiobook:{self.session_id}:station_21:episode_*"

            # For now, try loading episodes 1-24 (typical max)
            for episode_num in range(1, 25):
                try:
                    key = f"audiobook:{self.session_id}:station_21:episode_{episode_num:02d}"
                    data_raw = await self.redis_client.get(key)

                    if data_raw:
                        episode_data = json.loads(data_raw)
                        self.drafted_episodes[episode_num] = episode_data
                        print(f"   ✓ Episode {episode_num} first draft loaded")

                except Exception as e:
                    # Episode doesn't exist, skip silently
                    continue

        except Exception as e:
            raise ValueError(f"❌ Error loading first drafts: {str(e)}")

    def display_episode_selection(self):
        """Display episode selection menu with analysis status"""
        print("=" * 70)
        print("📺 EPISODE SELECTION & MOMENTUM CHECK STATUS")
        print("=" * 70)
        print()

        # Extract project info from first available episode
        first_episode = next(iter(self.drafted_episodes.values()), {})
        working_title = first_episode.get('draft_data', {}).get('first_draft_script', {}).get('title', 'Unknown')

        print(f"Project: {working_title}")
        print(f"First Drafts Available: {len(self.drafted_episodes)}")
        print()

        print("EPISODE MOMENTUM CHECK STATUS:")
        print("━" * 70)
        print()
        print("┌" + "─" * 68 + "┐")
        print("│ " + "Ep".ljust(4) + "Title".ljust(30) + "Words".ljust(10) + "Status".ljust(22) + " │")
        print("├" + "─" * 68 + "┤")

        for episode_num in sorted(self.drafted_episodes.keys()):
            episode_data = self.drafted_episodes[episode_num]

            title = episode_data.get('episode_title', f'Episode {episode_num}')[:29]

            draft_data = episode_data.get('draft_data', {})
            first_draft = draft_data.get('first_draft_script', {})
            word_count = first_draft.get('total_word_count', 0)

            if episode_num in self.checked_episodes:
                status = "✅ MOMENTUM CHECKED"
            else:
                status = "🟡 NEEDS CHECK"

            # Format row
            row = f"│ {str(episode_num).ljust(4)}{title.ljust(30)}{str(word_count).ljust(10)}{status.ljust(22)} │"
            print(row)

        print("└" + "─" * 68 + "┘")
        print()

        # Display statistics
        print("📊 MOMENTUM CHECK STATISTICS:")
        print(f"  • Total Episodes Drafted: {len(self.drafted_episodes)}")
        print(f"  • Episodes Checked: {len(self.checked_episodes)}/{len(self.drafted_episodes)}")
        print(f"  • Completion: {int((len(self.checked_episodes) / len(self.drafted_episodes)) * 100) if self.drafted_episodes else 0}%")
        print()
        print("=" * 70)
        print()

    def get_episode_selection(self) -> Optional[int]:
        """Get episode selection from user"""
        print("=" * 70)
        print("⭐ EPISODE SELECTION REQUIRED")
        print("=" * 70)
        print()
        print("Which episode would you like to check for momentum?")
        print()
        print("💡 RECOMMENDATIONS:")
        print("  • Start with Episode 1 for consistent momentum")
        print("  • OR check the episode that concerns you most")
        print("  • Sequential checking helps maintain consistency")
        print()

        available_episodes = sorted(self.drafted_episodes.keys())
        print(f"🎯 Available episodes: {', '.join(map(str, available_episodes))}")
        print()

        while True:
            try:
                choice = input(f"Enter episode number or 'Q' to quit: ").strip().upper()

                if choice == 'Q':
                    return None

                episode_num = int(choice)

                if episode_num in self.drafted_episodes:
                    return episode_num
                else:
                    print(f"❌ Episode {episode_num} not found. Available: {available_episodes}")

            except ValueError:
                print("❌ Invalid input. Please enter a number or 'Q'")

    async def check_episode(self, episode_number: int):
        """Analyze and fix momentum for a complete episode"""
        print()
        print("=" * 70)
        print(f"📥 LOADING EPISODE {episode_number} FIRST DRAFT")
        print("=" * 70)
        print()

        # Load episode draft
        episode_data = self.drafted_episodes[episode_number]
        draft_data = episode_data.get('draft_data', {})
        first_draft = draft_data.get('first_draft_script', {})

        # Display draft summary
        self.display_draft_summary(episode_number, episode_data)

        # Step 4: Execute 4 sequential LLM analysis tasks
        print()
        print("=" * 70)
        print("🔍 EXECUTING MOMENTUM ANALYSIS")
        print("=" * 70)
        print()

        # Task 1: Pacing Analysis
        print("⏱️  Task 1/4: Pacing Analysis...")
        pacing_analysis = await self.execute_pacing_analysis(episode_number, first_draft)
        print("✅ Pacing analysis complete")
        print()

        # Task 2: Repetition Detection
        print("🔁 Task 2/4: Repetition Detection...")
        repetition_analysis = await self.execute_repetition_detection(episode_number, first_draft)
        print("✅ Repetition detection complete")
        print()

        # Task 3: Energy Flow Analysis
        print("⚡ Task 3/4: Energy Flow Analysis...")
        energy_analysis = await self.execute_energy_flow_analysis(episode_number, first_draft)
        print("✅ Energy flow analysis complete")
        print()

        # Display all detected issues
        self.display_detected_issues(pacing_analysis, repetition_analysis, energy_analysis)

        # Task 4: Auto-fix Momentum
        print()
        print("🔧 Task 4/4: Auto-Fix Momentum Issues...")
        corrected_draft = await self.execute_auto_fix_momentum(
            episode_number,
            first_draft,
            pacing_analysis,
            repetition_analysis,
            energy_analysis
        )
        print("✅ Corrected draft generated")
        print()

        # Display corrected draft with changes
        self.display_corrected_draft(episode_number, first_draft, corrected_draft)

        # Human review
        if not self.skip_review:
            review_result = await self.human_review(episode_number, corrected_draft, first_draft)

            if review_result == "regenerate":
                # Regenerate the corrections
                corrected_draft = await self.execute_auto_fix_momentum(
                    episode_number,
                    first_draft,
                    pacing_analysis,
                    repetition_analysis,
                    energy_analysis
                )
        else:
            print("✅ Auto-accepting corrected draft (skip_review=True)")
            print()

        # Save outputs
        await self.save_episode_outputs(
            episode_number,
            corrected_draft,
            pacing_analysis,
            repetition_analysis,
            energy_analysis
        )

        # Mark as checked
        self.checked_episodes.add(episode_number)

    def display_draft_summary(self, episode_number: int, episode_data: Dict):
        """Display first draft summary"""
        print("=" * 70)
        print(f"📋 EPISODE {episode_number}: FIRST DRAFT SUMMARY")
        print("=" * 70)
        print()

        title = episode_data.get('episode_title', f'Episode {episode_number}')
        draft_data = episode_data.get('draft_data', {})
        first_draft = draft_data.get('first_draft_script', {})

        total_words = first_draft.get('total_word_count', 0)
        scenes = first_draft.get('scenes', [])

        print(f"Title: {title}")
        print(f"Total Words: {total_words}")
        print(f"Total Scenes: {len(scenes)}")
        print()

        print("SCENE BREAKDOWN:")
        print("━" * 70)
        for scene in scenes[:5]:  # Show first 5 scenes
            scene_num = scene.get('scene_number', '?')
            heading = scene.get('heading', 'Unknown')
            word_count = scene.get('word_count', 0)
            print(f"  Scene {scene_num}: {heading} ({word_count} words)")

        if len(scenes) > 5:
            print(f"  ... and {len(scenes) - 5} more scenes")
        print()
        print("=" * 70)
        print()

    async def execute_pacing_analysis(self, episode_number: int, first_draft: Dict) -> Dict:
        """Task 1: Analyze pacing issues"""
        try:
            prompt = self.config.get_prompt('pacing_analysis')

            # Prepare script content
            script_content = self._format_script_for_analysis(first_draft)

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script_content
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            analysis_data = extract_json(response)

            return analysis_data.get('pacing_analysis', {})

        except Exception as e:
            print(f"❌ Pacing analysis failed: {str(e)}")
            raise

    async def execute_repetition_detection(self, episode_number: int, first_draft: Dict) -> Dict:
        """Task 2: Detect repetition issues"""
        try:
            prompt = self.config.get_prompt('repetition_detection')

            # Prepare script content
            script_content = self._format_script_for_analysis(first_draft)

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script_content
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            analysis_data = extract_json(response)

            return analysis_data.get('repetition_analysis', {})

        except Exception as e:
            print(f"❌ Repetition detection failed: {str(e)}")
            raise

    async def execute_energy_flow_analysis(self, episode_number: int, first_draft: Dict) -> Dict:
        """Task 3: Analyze energy flow"""
        try:
            prompt = self.config.get_prompt('energy_flow_analysis')

            # Prepare script content
            script_content = self._format_script_for_analysis(first_draft)

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script_content
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            analysis_data = extract_json(response)

            return analysis_data.get('energy_flow_analysis', {})

        except Exception as e:
            print(f"❌ Energy flow analysis failed: {str(e)}")
            raise

    async def execute_auto_fix_momentum(self, episode_number: int, first_draft: Dict,
                                       pacing: Dict, repetition: Dict, energy: Dict) -> Dict:
        """Task 4: Auto-fix all momentum issues"""
        try:
            prompt = self.config.get_prompt('auto_fix_momentum')

            # Prepare original script
            original_script = self._format_script_for_analysis(first_draft)

            # Prepare fixes needed summary
            fixes_needed = self._format_fixes_needed(pacing, repetition, energy)

            # Format prompt
            formatted_prompt = prompt.format(
                original_script=original_script,
                fixes_needed=fixes_needed
            )

            # Execute LLM call - may take longer for rewrites
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=16384  # Higher token limit for full script rewrite
            )

            # Extract JSON
            corrected_data = extract_json(response)

            return corrected_data.get('momentum_corrected_script', {})

        except Exception as e:
            print(f"❌ Auto-fix momentum failed: {str(e)}")
            raise

    def _format_script_for_analysis(self, first_draft: Dict) -> str:
        """Format script for LLM analysis"""
        scenes = first_draft.get('scenes', [])

        parts = []
        for scene in scenes:
            scene_num = scene.get('scene_number', '?')
            heading = scene.get('heading', 'SCENE')
            script_content = scene.get('script_content', '')

            parts.append(f"=== SCENE {scene_num}: {heading} ===")
            parts.append(script_content)
            parts.append("")

        return "\n".join(parts)

    def _format_fixes_needed(self, pacing: Dict, repetition: Dict, energy: Dict) -> str:
        """Format all fixes needed for auto-fix prompt"""
        parts = []

        parts.append("=== PACING ISSUES ===")
        slow_sections = pacing.get('slow_sections', [])
        for issue in slow_sections:
            parts.append(f"- {issue.get('location', 'Unknown')}: {issue.get('problem', '')}")

        rushed_transitions = pacing.get('rushed_transitions', [])
        for issue in rushed_transitions:
            parts.append(f"- {issue.get('location', 'Unknown')}: {issue.get('problem', '')}")

        parts.append("")
        parts.append("=== REPETITION ISSUES ===")
        word_patterns = repetition.get('repeated_words', [])
        for issue in word_patterns:
            parts.append(f"- Word '{issue.get('word', '')}' repeated {issue.get('count', 0)} times")

        structural = repetition.get('structural_repetition', [])
        for issue in structural:
            parts.append(f"- {issue.get('pattern', '')}: {issue.get('description', '')}")

        parts.append("")
        parts.append("=== ENERGY FLOW ISSUES ===")
        energy_problems = energy.get('energy_problems', [])
        for issue in energy_problems:
            parts.append(f"- {issue.get('location', 'Unknown')}: {issue.get('problem', '')}")

        return "\n".join(parts)

    def display_detected_issues(self, pacing: Dict, repetition: Dict, energy: Dict):
        """Display all detected issues"""
        print("=" * 70)
        print("🔍 DETECTED MOMENTUM ISSUES")
        print("=" * 70)
        print()

        # Pacing issues
        slow_sections = pacing.get('slow_sections', [])
        rushed_transitions = pacing.get('rushed_transitions', [])
        dead_air = pacing.get('dead_air_moments', [])

        print("⏱️  PACING ISSUES:")
        print("━" * 70)

        if slow_sections:
            print(f"  Slow Sections: {len(slow_sections)} found")
            for issue in slow_sections[:3]:
                print(f"    • {issue.get('location', 'Unknown')}: {issue.get('problem', '')}")

        if rushed_transitions:
            print(f"  Rushed Transitions: {len(rushed_transitions)} found")
            for issue in rushed_transitions[:3]:
                print(f"    • {issue.get('location', 'Unknown')}: {issue.get('problem', '')}")

        if dead_air:
            print(f"  Dead Air Moments: {len(dead_air)} found")
            for issue in dead_air[:3]:
                print(f"    • {issue.get('location', 'Unknown')}: {issue.get('problem', '')}")

        if not slow_sections and not rushed_transitions and not dead_air:
            print("  ✅ No pacing issues detected")

        print()

        # Repetition issues
        repeated_words = repetition.get('repeated_words', [])
        structural = repetition.get('structural_repetition', [])

        print("🔁 REPETITION ISSUES:")
        print("━" * 70)

        if repeated_words:
            print(f"  Repeated Words/Phrases: {len(repeated_words)} found")
            for issue in repeated_words[:3]:
                print(f"    • '{issue.get('word', '')}' used {issue.get('count', 0)} times")

        if structural:
            print(f"  Structural Repetition: {len(structural)} patterns found")
            for issue in structural[:3]:
                print(f"    • {issue.get('pattern', '')}")

        if not repeated_words and not structural:
            print("  ✅ No repetition issues detected")

        print()

        # Energy flow issues
        energy_problems = energy.get('energy_problems', [])
        tension_release = energy.get('tension_release_balance', {})

        print("⚡ ENERGY FLOW ISSUES:")
        print("━" * 70)

        if energy_problems:
            print(f"  Energy Problems: {len(energy_problems)} found")
            for issue in energy_problems[:3]:
                print(f"    • {issue.get('location', 'Unknown')}: {issue.get('problem', '')}")

        balance = tension_release.get('balance_assessment', '')
        if balance:
            print(f"  Tension/Release Balance: {balance}")

        if not energy_problems:
            print("  ✅ No energy flow issues detected")

        print()

        # Summary
        total_issues = (
            len(slow_sections) + len(rushed_transitions) + len(dead_air) +
            len(repeated_words) + len(structural) + len(energy_problems)
        )

        print(f"📊 TOTAL ISSUES DETECTED: {total_issues}")
        print()
        print("=" * 70)
        print()

    def display_corrected_draft(self, episode_number: int, original: Dict, corrected: Dict):
        """Display corrected draft with changes highlighted"""
        print("=" * 70)
        print(f"✅ EPISODE {episode_number}: CORRECTED DRAFT")
        print("=" * 70)
        print()

        changes = corrected.get('changes_made', [])
        total_changes = corrected.get('total_changes', len(changes))

        print("CORRECTION STATISTICS:")
        print("━" * 70)
        print(f"  • Total Changes: {total_changes}")

        original_words = original.get('total_word_count', 0)
        corrected_words = corrected.get('total_word_count', 0)
        word_change = corrected_words - original_words

        print(f"  • Original Word Count: {original_words}")
        print(f"  • Corrected Word Count: {corrected_words}")
        print(f"  • Word Count Change: {'+' if word_change >= 0 else ''}{word_change}")
        print()

        print("CHANGES MADE:")
        print("━" * 70)

        for i, change in enumerate(changes[:10], 1):  # Show first 10 changes
            change_type = change.get('change_type', 'unknown')
            location = change.get('scene_number', '?')
            description = change.get('description', '')

            print(f"  {i}. [{change_type.upper()}] Scene {location}")
            print(f"     {description}")

        if len(changes) > 10:
            print(f"  ... and {len(changes) - 10} more changes")

        print()

        # Show sample of corrected content
        corrected_scenes = corrected.get('scenes', [])
        if corrected_scenes:
            print("SAMPLE CORRECTED CONTENT (First Scene):")
            print("━" * 70)
            first_scene = corrected_scenes[0]
            script_content = first_scene.get('script_content', '')
            preview = script_content[:500]
            print(preview)
            if len(script_content) > 500:
                print("...")

        print()
        print("=" * 70)
        print()

    async def human_review(self, episode_number: int, corrected: Dict, original: Dict) -> str:
        """Human review interface"""
        print("=" * 70)
        print("⭐ CORRECTED DRAFT REVIEW")
        print("=" * 70)
        print()

        total_changes = corrected.get('total_changes', 0)

        print(f"Episode {episode_number} momentum check complete: {total_changes} changes made")
        print()
        print("OPTIONS:")
        print("  [Enter] - Approve and save (recommended)")
        print("  [R]     - Regenerate corrections")
        print("  [V]     - View complete corrected script")
        print("  [C]     - View detailed change report")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == 'R':
            return "regenerate"
        elif choice == 'V':
            self.display_full_script(corrected)
            return await self.human_review(episode_number, corrected, original)
        elif choice == 'C':
            self.display_change_report(original, corrected)
            return await self.human_review(episode_number, corrected, original)
        else:
            print("✅ Corrected draft approved. Saving files...")
            print()
            return "approved"

    def display_full_script(self, corrected: Dict):
        """Display complete corrected script"""
        scenes = corrected.get('scenes', [])

        print("\n" + "=" * 70)
        print("COMPLETE CORRECTED SCRIPT")
        print("=" * 70 + "\n")

        for scene in scenes:
            print(f"\n{scene.get('heading', 'SCENE')}\n")
            print(scene.get('script_content', ''))
            print("\n" + "-" * 70 + "\n")

        input("\nPress Enter to return to review menu...")

    def display_change_report(self, original: Dict, corrected: Dict):
        """Display detailed change report"""
        changes = corrected.get('changes_made', [])

        print("\n" + "=" * 70)
        print("DETAILED CHANGE REPORT")
        print("=" * 70 + "\n")

        for i, change in enumerate(changes, 1):
            print(f"\nCHANGE {i}:")
            print(f"  Type: {change.get('change_type', 'unknown')}")
            print(f"  Location: Scene {change.get('scene_number', '?')}")
            print(f"  Description: {change.get('description', '')}")

            before = change.get('before', '')
            after = change.get('after', '')

            if before:
                print(f"  Before: {before[:200]}")
            if after:
                print(f"  After: {after[:200]}")

            print("-" * 70)

        input("\nPress Enter to return to review menu...")

    async def save_episode_outputs(self, episode_number: int, corrected: Dict,
                                   pacing: Dict, repetition: Dict, energy: Dict):
        """Save episode in multiple formats"""
        print()
        print("=" * 70)
        print("💾 SAVING MOMENTUM CHECK FILES")
        print("=" * 70)
        print()

        # Create episode subdirectory
        episode_dir = self.output_dir / f"episode_{episode_number:02d}"
        episode_dir.mkdir(exist_ok=True)

        # 1. Save JSON with all analysis + corrected script
        json_filename = f"episode_{episode_number:02d}_momentum_check.json"
        json_path = episode_dir / json_filename

        full_data = {
            'session_id': self.session_id,
            'episode_number': episode_number,
            'checked_at': datetime.now().isoformat(),
            'pacing_analysis': pacing,
            'repetition_analysis': repetition,
            'energy_flow_analysis': energy,
            'corrected_script': corrected
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_path}")

        # 2. Save Corrected Script (Plain Text)
        txt_filename = f"episode_{episode_number:02d}_momentum_corrected.txt"
        txt_path = episode_dir / txt_filename

        txt_content = self.generate_plain_text_script(episode_number, corrected)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print(f"✅ Saved Corrected Script: {txt_path}")

        # 3. Save Change Report
        report_filename = f"episode_{episode_number:02d}_change_report.txt"
        report_path = episode_dir / report_filename

        report_content = self.generate_change_report(episode_number, pacing, repetition, energy, corrected)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Saved Change Report: {report_path}")

        # 4. Save to Redis for Station 23
        redis_key = f"audiobook:{self.session_id}:station_22:episode_{episode_number:02d}"
        await self.redis_client.set(redis_key, json.dumps(full_data), expire=604800)  # 7 days
        print(f"✅ Saved to Redis: {redis_key}")

        print()

    def generate_plain_text_script(self, episode_number: int, corrected: Dict) -> str:
        """Generate plain text corrected script"""
        lines = []

        lines.append(f"EPISODE {episode_number}: MOMENTUM-CORRECTED SCRIPT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("=" * 70)
        lines.append("")

        scenes = corrected.get('scenes', [])

        for scene in scenes:
            lines.append(scene.get('heading', 'SCENE'))
            lines.append("")
            lines.append(scene.get('script_content', ''))
            lines.append("")
            lines.append("-" * 70)
            lines.append("")

        return "\n".join(lines)

    def generate_change_report(self, episode_number: int, pacing: Dict,
                              repetition: Dict, energy: Dict, corrected: Dict) -> str:
        """Generate comprehensive change report"""
        lines = []

        lines.append("=" * 70)
        lines.append(f"EPISODE {episode_number} MOMENTUM CHECK - CHANGE REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Session: {self.session_id}")
        lines.append("")

        # Pacing Analysis Summary
        lines.append("PACING ANALYSIS:")
        lines.append("━" * 70)
        slow_sections = pacing.get('slow_sections', [])
        rushed_transitions = pacing.get('rushed_transitions', [])
        dead_air = pacing.get('dead_air_moments', [])

        lines.append(f"  Slow Sections: {len(slow_sections)}")
        lines.append(f"  Rushed Transitions: {len(rushed_transitions)}")
        lines.append(f"  Dead Air Moments: {len(dead_air)}")
        lines.append("")

        # Repetition Analysis Summary
        lines.append("REPETITION ANALYSIS:")
        lines.append("━" * 70)
        repeated_words = repetition.get('repeated_words', [])
        structural = repetition.get('structural_repetition', [])

        lines.append(f"  Repeated Words/Phrases: {len(repeated_words)}")
        lines.append(f"  Structural Patterns: {len(structural)}")
        lines.append("")

        # Energy Flow Analysis Summary
        lines.append("ENERGY FLOW ANALYSIS:")
        lines.append("━" * 70)
        energy_problems = energy.get('energy_problems', [])

        lines.append(f"  Energy Problems: {len(energy_problems)}")
        lines.append(f"  Balance: {energy.get('tension_release_balance', {}).get('balance_assessment', 'N/A')}")
        lines.append("")

        # Changes Made
        lines.append("CHANGES MADE:")
        lines.append("━" * 70)
        changes = corrected.get('changes_made', [])
        total_changes = corrected.get('total_changes', len(changes))

        lines.append(f"  Total Changes: {total_changes}")
        lines.append("")

        for i, change in enumerate(changes, 1):
            lines.append(f"{i}. [{change.get('change_type', 'unknown').upper()}] Scene {change.get('scene_number', '?')}")
            lines.append(f"   {change.get('description', '')}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def ask_continue_checking(self) -> bool:
        """Ask if user wants to continue checking"""
        print()
        print("=" * 70)
        print("⭐ CONTINUE MOMENTUM CHECKS?")
        print("=" * 70)
        print()
        print(f"Episodes checked: {len(self.checked_episodes)}/{len(self.drafted_episodes)}")
        print()
        print("OPTIONS:")
        print("  [Y] - Check another episode")
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
        print(f"Episodes checked: {len(self.checked_episodes)}/{len(self.drafted_episodes)}")
        for ep_num in sorted(self.checked_episodes):
            print(f"  ✅ Episode {ep_num}")
        print()
        print(f"Session ID: {self.session_id}")
        print()
        print("Your progress has been saved.")
        print("Resume momentum checks anytime by running Station 22 again.")
        print()
        print("Next Steps:")
        print("  1. Continue checking remaining episodes (Station 22)")
        print("  2. OR proceed to Station 23 (Twist Integration)")
        print()
        print("=" * 70)
        print()


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station22MomentumCheck(session_id, skip_review=False)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
