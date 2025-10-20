"""
Station 23: Twist Integration

This station validates P3 Grid (Plant/Proof/Payoff) compliance and automatically
integrates missing elements. It checks for premature payoffs, weak plants, and
misdirection balance to ensure perfect mystery/thriller storytelling.

Flow:
1. Load Station 21/22 scripts (uses 22 if available, else 21)
2. Load Station 10 P3 Grid (reveal strategy)
3. Display episode selection and P3 validation status
4. Human selects episode to validate
5. Execute 4 sequential LLM validation tasks:
   - P3 cross-reference (find missing/weak/misplaced plants)
   - Payoff validation (detect premature reveals)
   - Misdirection balance (check red herrings)
   - Auto-integrate fixes (rewrite with P3 elements)
6. Display P3 validation report with compliance score
7. Display enhanced script with integrated elements
8. Human review (approve/regenerate)
9. Save enhanced script + P3 compliance report
10. Save to Redis for Station 24+
11. Loop option for next episode

Critical Mystery/Thriller Station - Ensures perfect P3 integration
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


class Station23TwistIntegration:
    """Station 23: Twist Integration"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=23)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_23'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store loaded data
        self.script_episodes = {}  # From Station 21 or 22
        self.p3_grid = {}  # From Station 10
        self.validated_episodes = set()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_23.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method with episode loop"""
        print("=" * 70)
        print("🎭 STATION 23: TWIST INTEGRATION (P3 VALIDATION)")
        print("=" * 70)
        print()

        try:
            # Step 1: Load scripts from Station 21/22
            print("📥 Loading scripts from Station 21/22...")
            await self.load_scripts()
            print(f"✅ Loaded {len(self.script_episodes)} episode script(s)")
            print()

            if not self.script_episodes:
                print("❌ No scripts found. Please run Station 21 first.")
                return

            # Step 2: Load P3 Grid from Station 10
            print("📥 Loading P3 Grid from Station 10...")
            await self.load_p3_grid()
            print("✅ P3 Grid loaded")
            print()

            # Main validation loop
            while True:
                # Step 3: Display episode selection
                self.display_episode_selection()

                # Step 4: Human selects episode
                episode_number = self.get_episode_selection()

                if episode_number is None:
                    # User chose to exit
                    break

                # Step 5-9: Validate and integrate P3 elements
                await self.validate_episode(episode_number)

                # Step 10: Ask to continue
                if not self.ask_continue_validation():
                    break

            # Display final summary
            self.display_session_summary()

        except Exception as e:
            print(f"❌ Station 23 failed: {str(e)}")
            logging.error(f"Station 23 error: {str(e)}", exc_info=True)
            raise

    async def load_scripts(self):
        """Load scripts from Station 22 (preferred) or Station 21"""
        try:
            # Try loading from Station 22 first (momentum-corrected scripts)
            for episode_num in range(1, 25):
                try:
                    key_22 = f"audiobook:{self.session_id}:station_22:episode_{episode_num:02d}"
                    data_raw = await self.redis_client.get(key_22)

                    if data_raw:
                        episode_data = json.loads(data_raw)
                        # Extract corrected script from Station 22
                        corrected_script = episode_data.get('corrected_script', {})
                        self.script_episodes[episode_num] = {
                            'source': 'station_22',
                            'script': corrected_script,
                            'episode_number': episode_num
                        }
                        print(f"   ✓ Episode {episode_num} (from Station 22 - momentum corrected)")
                        continue

                except Exception:
                    pass

                # Try Station 21 if Station 22 not available
                try:
                    key_21 = f"audiobook:{self.session_id}:station_21:episode_{episode_num:02d}"
                    data_raw = await self.redis_client.get(key_21)

                    if data_raw:
                        episode_data = json.loads(data_raw)
                        # Extract first draft from Station 21
                        draft_data = episode_data.get('draft_data', {})
                        first_draft = draft_data.get('first_draft_script', {})
                        self.script_episodes[episode_num] = {
                            'source': 'station_21',
                            'script': first_draft,
                            'episode_number': episode_num
                        }
                        print(f"   ✓ Episode {episode_num} (from Station 21 - first draft)")

                except Exception:
                    continue

        except Exception as e:
            raise ValueError(f"❌ Error loading scripts: {str(e)}")

    async def load_p3_grid(self):
        """Load P3 Grid from Station 10"""
        try:
            key = f"audiobook:{self.session_id}:station_10"
            data_raw = await self.redis_client.get(key)

            if data_raw:
                station10_data = json.loads(data_raw)
                self.p3_grid = station10_data.get('Reveal Strategy Document', {})
            else:
                print("⚠️  Warning: Station 10 (Reveal Strategy) not found")
                print("    P3 validation will be limited")
                self.p3_grid = {}

        except Exception as e:
            logging.warning(f"Could not load P3 Grid: {str(e)}")
            self.p3_grid = {}

    def display_episode_selection(self):
        """Display episode selection menu with P3 validation status"""
        print("=" * 70)
        print("📺 EPISODE SELECTION & P3 VALIDATION STATUS")
        print("=" * 70)
        print()

        print(f"Scripts Available: {len(self.script_episodes)}")
        print(f"P3 Grid Loaded: {'✅' if self.p3_grid else '⚠️  Limited'}")
        print()

        print("EPISODE P3 VALIDATION STATUS:")
        print("━" * 70)
        print()
        print("┌" + "─" * 68 + "┐")
        print("│ " + "Ep".ljust(4) + "Source".ljust(12) + "Words".ljust(10) + "P3 Status".ljust(40) + " │")
        print("├" + "─" * 68 + "┤")

        for episode_num in sorted(self.script_episodes.keys()):
            episode_data = self.script_episodes[episode_num]

            source = "St22✅" if episode_data['source'] == 'station_22' else "St21"
            script = episode_data['script']
            word_count = script.get('total_word_count', 0)

            if episode_num in self.validated_episodes:
                status = "✅ P3 VALIDATED & INTEGRATED"
            else:
                status = "🟡 NEEDS P3 VALIDATION"

            # Format row
            row = f"│ {str(episode_num).ljust(4)}{source.ljust(12)}{str(word_count).ljust(10)}{status.ljust(40)} │"
            print(row)

        print("└" + "─" * 68 + "┘")
        print()

        # Display P3 statistics
        if self.p3_grid:
            total_twists = len(self.p3_grid.get('major_twists', []))
            total_red_herrings = len(self.p3_grid.get('red_herrings', []))

            print("📊 P3 GRID STATISTICS:")
            print(f"  • Major Twists/Reveals: {total_twists}")
            print(f"  • Red Herrings: {total_red_herrings}")
            print(f"  • Episodes Validated: {len(self.validated_episodes)}/{len(self.script_episodes)}")
            print(f"  • Completion: {int((len(self.validated_episodes) / len(self.script_episodes)) * 100) if self.script_episodes else 0}%")
        else:
            print("⚠️  P3 Grid not loaded - validation will be basic")

        print()
        print("=" * 70)
        print()

    def get_episode_selection(self) -> Optional[int]:
        """Get episode selection from user"""
        print("=" * 70)
        print("⭐ EPISODE SELECTION REQUIRED")
        print("=" * 70)
        print()
        print("Which episode would you like to validate for P3 integration?")
        print()
        print("💡 RECOMMENDATIONS:")
        print("  • Validate in chronological order for best results")
        print("  • Earlier episodes establish plants for later payoffs")
        print("  • Sequential validation ensures grid consistency")
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

    async def validate_episode(self, episode_number: int):
        """Validate and integrate P3 elements for an episode"""
        print()
        print("=" * 70)
        print(f"📥 LOADING EPISODE {episode_number} SCRIPT")
        print("=" * 70)
        print()

        # Load episode script
        episode_data = self.script_episodes[episode_number]
        script = episode_data['script']
        source = episode_data['source']

        # Display script summary
        self.display_script_summary(episode_number, script, source)

        # Step 5: Execute 4 sequential LLM validation tasks
        print()
        print("=" * 70)
        print("🔍 EXECUTING P3 VALIDATION")
        print("=" * 70)
        print()

        # Task 1: P3 Cross-Reference
        print("🔍 Task 1/4: P3 Cross-Reference (Plant Detection)...")
        p3_validation = await self.execute_p3_cross_reference(episode_number, script)
        print("✅ P3 cross-reference complete")
        print()

        # Task 2: Payoff Validation
        print("🎯 Task 2/4: Payoff Validation (Premature Reveal Check)...")
        payoff_validation = await self.execute_payoff_validation(episode_number, script)
        print("✅ Payoff validation complete")
        print()

        # Task 3: Misdirection Balance
        print("🎭 Task 3/4: Misdirection Balance (Red Herring Analysis)...")
        misdirection_analysis = await self.execute_misdirection_balance(episode_number, script)
        print("✅ Misdirection analysis complete")
        print()

        # Display P3 validation report
        self.display_p3_validation_report(p3_validation, payoff_validation, misdirection_analysis)

        # Task 4: Auto-integrate fixes
        print()
        print("🔧 Task 4/4: Auto-Integrate P3 Fixes...")
        enhanced_script = await self.execute_auto_integrate_fixes(
            episode_number,
            script,
            p3_validation,
            payoff_validation,
            misdirection_analysis
        )
        print("✅ Enhanced script generated with P3 integrations")
        print()

        # Display enhanced script
        self.display_enhanced_script(episode_number, script, enhanced_script)

        # Human review
        if not self.skip_review:
            review_result = await self.human_review(episode_number, enhanced_script, script)

            if review_result == "regenerate":
                # Regenerate the integrations
                enhanced_script = await self.execute_auto_integrate_fixes(
                    episode_number,
                    script,
                    p3_validation,
                    payoff_validation,
                    misdirection_analysis
                )
        else:
            print("✅ Auto-accepting enhanced script (skip_review=True)")
            print()

        # Save outputs
        await self.save_episode_outputs(
            episode_number,
            enhanced_script,
            p3_validation,
            payoff_validation,
            misdirection_analysis
        )

        # Mark as validated
        self.validated_episodes.add(episode_number)

    def display_script_summary(self, episode_number: int, script: Dict, source: str):
        """Display script summary"""
        print("=" * 70)
        print(f"📋 EPISODE {episode_number}: SCRIPT SUMMARY")
        print("=" * 70)
        print()

        source_name = "Station 22 (Momentum Corrected)" if source == 'station_22' else "Station 21 (First Draft)"
        total_words = script.get('total_word_count', 0)
        scenes = script.get('scenes', [])

        print(f"Source: {source_name}")
        print(f"Total Words: {total_words}")
        print(f"Total Scenes: {len(scenes)}")
        print()
        print("=" * 70)
        print()

    async def execute_p3_cross_reference(self, episode_number: int, script: Dict) -> Dict:
        """Task 1: Cross-reference P3 grid against script"""
        try:
            prompt = self.config.get_prompt('p3_cross_reference')

            # Prepare script content
            script_content = self._format_script_for_analysis(script)

            # Prepare P3 grid for this episode
            p3_grid_for_episode = self._format_p3_grid_for_episode(episode_number)

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script_content,
                p3_grid_for_episode=p3_grid_for_episode
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            validation_data = extract_json(response)

            return validation_data.get('p3_validation', {})

        except Exception as e:
            print(f"❌ P3 cross-reference failed: {str(e)}")
            raise

    async def execute_payoff_validation(self, episode_number: int, script: Dict) -> Dict:
        """Task 2: Validate payoff timing"""
        try:
            prompt = self.config.get_prompt('payoff_validation')

            # Prepare script content
            script_content = self._format_script_for_analysis(script)

            # Prepare reveal schedule
            reveal_schedule = self._format_reveal_schedule()

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script_content,
                reveal_schedule=reveal_schedule
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            validation_data = extract_json(response)

            return validation_data.get('payoff_validation', {})

        except Exception as e:
            print(f"❌ Payoff validation failed: {str(e)}")
            raise

    async def execute_misdirection_balance(self, episode_number: int, script: Dict) -> Dict:
        """Task 3: Analyze misdirection balance"""
        try:
            prompt = self.config.get_prompt('misdirection_balance')

            # Prepare script content
            script_content = self._format_script_for_analysis(script)

            # Prepare red herrings
            red_herrings = self._format_red_herrings()

            # Format prompt
            formatted_prompt = prompt.format(
                current_script=script_content,
                red_herrings=red_herrings
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            analysis_data = extract_json(response)

            return analysis_data.get('misdirection_analysis', {})

        except Exception as e:
            print(f"❌ Misdirection analysis failed: {str(e)}")
            raise

    async def execute_auto_integrate_fixes(self, episode_number: int, script: Dict,
                                          p3_validation: Dict, payoff_validation: Dict,
                                          misdirection: Dict) -> Dict:
        """Task 4: Auto-integrate all P3 fixes"""
        try:
            prompt = self.config.get_prompt('auto_integrate_fixes')

            # Prepare original script
            original_script = self._format_script_for_analysis(script)

            # Prepare fixes needed summary
            fixes_needed = self._format_p3_fixes_needed(p3_validation, payoff_validation, misdirection)

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
            enhanced_data = extract_json(response)

            return enhanced_data.get('twist_integration', {})

        except Exception as e:
            print(f"❌ Auto-integrate fixes failed: {str(e)}")
            raise

    def _format_script_for_analysis(self, script: Dict) -> str:
        """Format script for LLM analysis"""
        scenes = script.get('scenes', [])

        parts = []
        for scene in scenes:
            scene_num = scene.get('scene_number', '?')
            heading = scene.get('heading', 'SCENE')
            script_content = scene.get('script_content', '')

            parts.append(f"=== SCENE {scene_num}: {heading} ===")
            parts.append(script_content)
            parts.append("")

        return "\n".join(parts)

    def _format_p3_grid_for_episode(self, episode_number: int) -> str:
        """Format P3 grid requirements for specific episode"""
        if not self.p3_grid:
            return "P3 Grid not available - perform general validation"

        parts = []
        parts.append(f"=== PLANTS REQUIRED IN EPISODE {episode_number} ===")

        # Extract plants scheduled for this episode
        major_twists = self.p3_grid.get('major_twists', [])

        for twist in major_twists:
            plant_episode = twist.get('plant_episode', 0)
            if plant_episode == episode_number:
                parts.append(f"- {twist.get('twist_id', 'Unknown')}: {twist.get('description', '')}")

        if len(parts) == 1:
            parts.append("No specific plants required for this episode")

        parts.append("")
        parts.append(f"=== PROOFS REQUIRED IN EPISODE {episode_number} ===")

        # Extract proofs scheduled for this episode
        for twist in major_twists:
            proof_episode = twist.get('proof_episode', 0)
            if proof_episode == episode_number:
                parts.append(f"- Evidence for: {twist.get('description', '')}")

        return "\n".join(parts)

    def _format_reveal_schedule(self) -> str:
        """Format reveal schedule from P3 grid"""
        if not self.p3_grid:
            return "Reveal schedule not available - check for obvious premature reveals"

        parts = []
        major_twists = self.p3_grid.get('major_twists', [])

        for twist in major_twists:
            twist_id = twist.get('twist_id', 'Unknown')
            plant_ep = twist.get('plant_episode', '?')
            proof_ep = twist.get('proof_episode', '?')
            payoff_ep = twist.get('payoff_episode', '?')
            description = twist.get('description', '')

            parts.append(f"{twist_id}: {description}")
            parts.append(f"  Plant: Episode {plant_ep}")
            parts.append(f"  Proof: Episode {proof_ep}")
            parts.append(f"  Payoff: Episode {payoff_ep}")
            parts.append("")

        return "\n".join(parts)

    def _format_red_herrings(self) -> str:
        """Format red herrings from P3 grid"""
        if not self.p3_grid:
            return "Red herrings not defined - analyze balance generally"

        red_herrings = self.p3_grid.get('red_herrings', [])

        parts = []
        for rh in red_herrings:
            rh_id = rh.get('red_herring_id', 'Unknown')
            description = rh.get('description', '')
            introduce_ep = rh.get('introduce_episode', '?')
            dismiss_ep = rh.get('dismiss_episode', '?')

            parts.append(f"{rh_id}: {description}")
            parts.append(f"  Introduce: Episode {introduce_ep}")
            parts.append(f"  Dismiss: Episode {dismiss_ep}")
            parts.append("")

        return "\n".join(parts)

    def _format_p3_fixes_needed(self, p3_validation: Dict, payoff_validation: Dict,
                                misdirection: Dict) -> str:
        """Format all P3 fixes needed"""
        parts = []

        # Missing/weak plants
        parts.append("=== PLANT FIXES ===")
        required_plants = p3_validation.get('required_plants', [])

        for plant in required_plants:
            status = plant.get('status', 'unknown')
            if status in ['missing', 'weak']:
                parts.append(f"- {plant.get('plant_id', 'Unknown')}: {plant.get('description', '')}")
                parts.append(f"  Status: {status}")
                parts.append(f"  Fix: {plant.get('fix_needed', '')}")

        # Premature payoffs
        parts.append("")
        parts.append("=== PAYOFF FIXES ===")
        premature_reveals = payoff_validation.get('premature_reveals', [])

        for reveal in premature_reveals:
            parts.append(f"- Scene {reveal.get('scene_number', '?')}: {reveal.get('content_revealed', '')}")
            parts.append(f"  Scheduled for: Episode {reveal.get('scheduled_for_episode', '?')}")
            parts.append(f"  Fix: {reveal.get('fix_needed', '')}")

        # Misdirection balance
        parts.append("")
        parts.append("=== MISDIRECTION FIXES ===")
        suspicion_dist = misdirection.get('suspicion_distribution', {})
        character_levels = suspicion_dist.get('character_suspicion_levels', [])

        for char in character_levels:
            status = char.get('status', '')
            if status != 'correct':
                parts.append(f"- {char.get('character', 'Unknown')}: {char.get('issue', '')}")
                parts.append(f"  Fix: {char.get('fix', '')}")

        return "\n".join(parts)

    def display_p3_validation_report(self, p3_validation: Dict, payoff_validation: Dict,
                                    misdirection: Dict):
        """Display comprehensive P3 validation report"""
        print("=" * 70)
        print("🎭 P3 VALIDATION REPORT")
        print("=" * 70)
        print()

        # P3 Grid Compliance
        summary = p3_validation.get('summary', {})
        total_required = summary.get('total_required', 0)
        strong_plants = summary.get('strong_plants', 0)
        weak_plants = summary.get('weak_plants', 0)
        missing_plants = summary.get('missing_plants', 0)

        print("🌱 PLANT COMPLIANCE:")
        print("━" * 70)
        print(f"  Required Plants: {total_required}")
        print(f"  ✅ Strong Plants: {strong_plants}")
        print(f"  ⚠️  Weak Plants: {weak_plants}")
        print(f"  ❌ Missing Plants: {missing_plants}")

        if total_required > 0:
            compliance = int(((strong_plants + weak_plants) / total_required) * 100)
            print(f"  Compliance: {compliance}%")

        print()

        # Payoff Timing
        premature_reveals = payoff_validation.get('premature_reveals', [])
        unearned_payoffs = payoff_validation.get('unearned_payoffs', [])

        print("🎯 PAYOFF TIMING:")
        print("━" * 70)
        print(f"  ❌ Premature Reveals: {len(premature_reveals)}")
        for reveal in premature_reveals[:3]:
            print(f"    • Scene {reveal.get('scene_number', '?')}: {reveal.get('content_revealed', '')[:50]}")

        print(f"  ⚠️  Unearned Payoffs: {len(unearned_payoffs)}")
        for payoff in unearned_payoffs[:3]:
            print(f"    • {payoff.get('payoff', '')[:50]}")

        if not premature_reveals and not unearned_payoffs:
            print("  ✅ All reveals properly timed")

        print()

        # Misdirection Balance
        suspicion_dist = misdirection.get('suspicion_distribution', {})
        character_levels = suspicion_dist.get('character_suspicion_levels', [])
        fair_play = misdirection.get('fair_play_check', {})

        print("🎭 MISDIRECTION BALANCE:")
        print("━" * 70)

        for char in character_levels[:5]:
            character = char.get('character', 'Unknown')
            current = char.get('current_suspicion', '?')
            target = char.get('target_suspicion', '?')
            status = char.get('status', 'unknown')

            status_icon = "✅" if status == 'correct' else "⚠️"
            print(f"  {status_icon} {character}: {current} (target: {target})")

        print()
        print(f"  Fair Play: {'✅' if fair_play.get('clues_present', False) else '❌'}")
        print(f"  Balance Rating: {fair_play.get('balance_rating', 'unknown')}")

        print()

        # Overall Summary
        total_issues = len(premature_reveals) + len(unearned_payoffs) + weak_plants + missing_plants

        print(f"📊 TOTAL P3 ISSUES: {total_issues}")
        print()
        print("=" * 70)
        print()

    def display_enhanced_script(self, episode_number: int, original: Dict, enhanced: Dict):
        """Display enhanced script with P3 integrations"""
        print("=" * 70)
        print(f"✨ EPISODE {episode_number}: P3-ENHANCED SCRIPT")
        print("=" * 70)
        print()

        changes = enhanced.get('changes', [])
        total_changes = enhanced.get('total_changes', len(changes))
        word_count_change = enhanced.get('word_count_change', '+0 words')

        compliance_before = enhanced.get('p3_compliance_before', 'Unknown')
        compliance_after = enhanced.get('p3_compliance_after', 'Unknown')

        print("P3 INTEGRATION STATISTICS:")
        print("━" * 70)
        print(f"  • Total P3 Integrations: {total_changes}")
        print(f"  • Word Count Change: {word_count_change}")
        print(f"  • P3 Compliance Before: {compliance_before}")
        print(f"  • P3 Compliance After: {compliance_after}")
        print()

        print("P3 INTEGRATIONS MADE:")
        print("━" * 70)

        for i, change in enumerate(changes[:10], 1):
            change_type = change.get('change_type', 'unknown')
            scene_num = change.get('scene_number', '?')
            p3_marker = change.get('p3_marker', '')
            technique = change.get('integration_technique', '')

            print(f"  {i}. [{change_type.upper()}] Scene {scene_num}")
            print(f"     P3 Marker: {p3_marker}")
            print(f"     Technique: {technique}")

        if len(changes) > 10:
            print(f"  ... and {len(changes) - 10} more integrations")

        print()
        print("=" * 70)
        print()

    async def human_review(self, episode_number: int, enhanced: Dict, original: Dict) -> str:
        """Human review interface"""
        print("=" * 70)
        print("⭐ P3-ENHANCED SCRIPT REVIEW")
        print("=" * 70)
        print()

        total_changes = enhanced.get('total_changes', 0)
        compliance_after = enhanced.get('p3_compliance_after', 'Unknown')

        print(f"Episode {episode_number} P3 integration complete:")
        print(f"  • {total_changes} P3 elements integrated")
        print(f"  • P3 Compliance: {compliance_after}")
        print()
        print("OPTIONS:")
        print("  [Enter] - Approve and save (recommended)")
        print("  [R]     - Regenerate P3 integrations")
        print("  [V]     - View complete enhanced script")
        print("  [D]     - View detailed P3 integration report")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == 'R':
            return "regenerate"
        elif choice == 'V':
            self.display_full_script(enhanced)
            return await self.human_review(episode_number, enhanced, original)
        elif choice == 'D':
            self.display_detailed_integration_report(enhanced)
            return await self.human_review(episode_number, enhanced, original)
        else:
            print("✅ P3-enhanced script approved. Saving files...")
            print()
            return "approved"

    def display_full_script(self, enhanced: Dict):
        """Display complete enhanced script"""
        full_script = enhanced.get('full_enhanced_script', '')

        print("\n" + "=" * 70)
        print("COMPLETE P3-ENHANCED SCRIPT")
        print("=" * 70 + "\n")

        # Display script (truncate if very long)
        if len(full_script) > 5000:
            print(full_script[:5000])
            print("\n... (script continues) ...\n")
        else:
            print(full_script)

        input("\nPress Enter to return to review menu...")

    def display_detailed_integration_report(self, enhanced: Dict):
        """Display detailed P3 integration report"""
        changes = enhanced.get('changes', [])

        print("\n" + "=" * 70)
        print("DETAILED P3 INTEGRATION REPORT")
        print("=" * 70 + "\n")

        for i, change in enumerate(changes, 1):
            print(f"\nINTEGRATION {i}:")
            print(f"  Type: {change.get('change_type', 'unknown')}")
            print(f"  Scene: {change.get('scene_number', '?')}")
            print(f"  P3 Marker: {change.get('p3_marker', '')}")
            print(f"  Payoff Episode: {change.get('payoff_episode', '?')}")
            print(f"  Technique: {change.get('integration_technique', '')}")
            print(f"  Explanation: {change.get('explanation', '')}")

            original = change.get('original_content', '')
            enhanced_content = change.get('enhanced_content', '')

            if original:
                print(f"  Original: {original[:200]}")
            if enhanced_content:
                print(f"  Enhanced: {enhanced_content[:200]}")

            print("-" * 70)

        input("\nPress Enter to return to review menu...")

    async def save_episode_outputs(self, episode_number: int, enhanced: Dict,
                                   p3_validation: Dict, payoff_validation: Dict,
                                   misdirection: Dict):
        """Save episode in multiple formats"""
        print()
        print("=" * 70)
        print("💾 SAVING P3 VALIDATION FILES")
        print("=" * 70)
        print()

        # Create episode subdirectory
        episode_dir = self.output_dir / f"episode_{episode_number:02d}"
        episode_dir.mkdir(exist_ok=True)

        # 1. Save JSON with all validation + enhanced script
        json_filename = f"episode_{episode_number:02d}_twist_integrated.json"
        json_path = episode_dir / json_filename

        full_data = {
            'session_id': self.session_id,
            'episode_number': episode_number,
            'validated_at': datetime.now().isoformat(),
            'p3_validation': p3_validation,
            'payoff_validation': payoff_validation,
            'misdirection_analysis': misdirection,
            'twist_integration': enhanced
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_path}")

        # 2. Save Enhanced Script (Plain Text)
        txt_filename = f"episode_{episode_number:02d}_twist_integrated.txt"
        txt_path = episode_dir / txt_filename

        txt_content = enhanced.get('full_enhanced_script', '')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print(f"✅ Saved Enhanced Script: {txt_path}")

        # 3. Save P3 Validation Report
        report_filename = f"episode_{episode_number:02d}_p3_validation.txt"
        report_path = episode_dir / report_filename

        report_content = self.generate_p3_report(episode_number, p3_validation, payoff_validation,
                                                 misdirection, enhanced)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Saved P3 Report: {report_path}")

        # 4. Save to Redis for Station 24+
        redis_key = f"audiobook:{self.session_id}:station_23:episode_{episode_number:02d}"
        await self.redis_client.set(redis_key, json.dumps(full_data), expire=604800)  # 7 days
        print(f"✅ Saved to Redis: {redis_key}")

        print()

    def generate_p3_report(self, episode_number: int, p3_validation: Dict,
                          payoff_validation: Dict, misdirection: Dict, enhanced: Dict) -> str:
        """Generate comprehensive P3 validation report"""
        lines = []

        lines.append("=" * 70)
        lines.append(f"EPISODE {episode_number} P3 VALIDATION REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Session: {self.session_id}")
        lines.append("")

        # P3 Grid Compliance
        summary = p3_validation.get('summary', {})
        lines.append("PLANT COMPLIANCE:")
        lines.append("━" * 70)
        lines.append(f"  Required Plants: {summary.get('total_required', 0)}")
        lines.append(f"  Strong Plants: {summary.get('strong_plants', 0)}")
        lines.append(f"  Weak Plants: {summary.get('weak_plants', 0)}")
        lines.append(f"  Missing Plants: {summary.get('missing_plants', 0)}")
        lines.append("")

        # Payoff Timing
        premature_reveals = payoff_validation.get('premature_reveals', [])
        lines.append("PAYOFF TIMING:")
        lines.append("━" * 70)
        lines.append(f"  Premature Reveals: {len(premature_reveals)}")
        for reveal in premature_reveals:
            lines.append(f"    • Scene {reveal.get('scene_number', '?')}: {reveal.get('content_revealed', '')}")
        lines.append("")

        # Misdirection Balance
        fair_play = misdirection.get('fair_play_check', {})
        lines.append("MISDIRECTION BALANCE:")
        lines.append("━" * 70)
        lines.append(f"  Fair Play: {fair_play.get('balance_rating', 'unknown')}")
        lines.append("")

        # P3 Integrations
        total_changes = enhanced.get('total_changes', 0)
        compliance_before = enhanced.get('p3_compliance_before', 'Unknown')
        compliance_after = enhanced.get('p3_compliance_after', 'Unknown')

        lines.append("P3 INTEGRATIONS:")
        lines.append("━" * 70)
        lines.append(f"  Total Integrations: {total_changes}")
        lines.append(f"  Compliance Before: {compliance_before}")
        lines.append(f"  Compliance After: {compliance_after}")
        lines.append("")

        changes = enhanced.get('changes', [])
        for i, change in enumerate(changes, 1):
            lines.append(f"{i}. [{change.get('change_type', 'unknown').upper()}] Scene {change.get('scene_number', '?')}")
            lines.append(f"   P3 Marker: {change.get('p3_marker', '')}")
            lines.append(f"   Technique: {change.get('integration_technique', '')}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def ask_continue_validation(self) -> bool:
        """Ask if user wants to continue validation"""
        print()
        print("=" * 70)
        print("⭐ CONTINUE P3 VALIDATION?")
        print("=" * 70)
        print()
        print(f"Episodes validated: {len(self.validated_episodes)}/{len(self.script_episodes)}")
        print()
        print("OPTIONS:")
        print("  [Y] - Validate another episode")
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
        print(f"Episodes validated: {len(self.validated_episodes)}/{len(self.script_episodes)}")
        for ep_num in sorted(self.validated_episodes):
            print(f"  ✅ Episode {ep_num}")
        print()
        print(f"Session ID: {self.session_id}")
        print()
        print("Your progress has been saved.")
        print("Resume P3 validation anytime by running Station 23 again.")
        print()
        print("Next Steps:")
        print("  1. Continue validating remaining episodes (Station 23)")
        print("  2. OR proceed to Station 24+ (subsequent stations)")
        print()
        print("=" * 70)
        print()


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station23TwistIntegration(session_id, skip_review=False)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
