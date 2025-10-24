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
        print("📖 STATION 23: STORY COHERENCE VALIDATION")
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
        print("📺 EPISODE SELECTION & COHERENCE VALIDATION STATUS")
        print("=" * 70)
        print()

        print(f"Scripts Available: {len(self.script_episodes)}")
        print(f"P3 Grid Loaded: {'✅' if self.p3_grid else '⚠️  Limited'}")
        print()

        print("EPISODE COHERENCE VALIDATION STATUS:")
        print("━" * 70)
        print()
        print("┌" + "─" * 68 + "┐")
        print("│ " + "Ep".ljust(4) + "Source".ljust(12) + "Words".ljust(10) + "Coherence Status".ljust(40) + " │")
        print("├" + "─" * 68 + "┤")

        for episode_num in sorted(self.script_episodes.keys()):
            episode_data = self.script_episodes[episode_num]

            source = "St22✅" if episode_data['source'] == 'station_22' else "St21"
            script = episode_data['script']
            word_count = script.get('total_word_count', 0)

            if episode_num in self.validated_episodes:
                status = "✅ COHERENCE VALIDATED & ENHANCED"
            else:
                status = "🟡 NEEDS COHERENCE VALIDATION"

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
        print("Which episode would you like to validate for coherence?")
        print()
        print("💡 RECOMMENDATIONS:")
        print("  • Validate in chronological order for best results")
        print("  • Earlier episodes establish character consistency")
        print("  • Sequential validation ensures story coherence")
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

        # Step 5: Execute 2 sequential coherence validation tasks
        print()
        print("=" * 70)
        print("🔍 EXECUTING STORY COHERENCE VALIDATION")
        print("=" * 70)
        print()

        # Task 1: Story Coherence Validation
        print("✓ Task 1/2: Validating story logic and character consistency...")
        coherence_check = await self.execute_story_coherence_validation(episode_number, script)
        print("✅ Coherence validation complete")
        print()

        # Display coherence report
        self.display_coherence_report(coherence_check)

        # Task 2: Minimal Enhancement
        print()
        print("✓ Task 2/2: Generating minimal coherence enhancements...")
        enhanced_script = await self.execute_minimal_enhancement(
            episode_number,
            script,
            coherence_check
        )
        print("✅ Minimal enhancements generated")
        print()

        # Display enhanced script
        self.display_enhanced_script(episode_number, script, enhanced_script)

        # Human review
        if not self.skip_review:
            review_result = await self.human_review(episode_number, enhanced_script, script)

            if review_result == "regenerate":
                # Regenerate the enhancements
                enhanced_script = await self.execute_minimal_enhancement(
                    episode_number,
                    script,
                    coherence_check
                )
        else:
            print("✅ Auto-accepting enhanced script (skip_review=True)")
            print()

        # Save outputs
        await self.save_episode_outputs(
            episode_number,
            enhanced_script,
            coherence_check
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

    def display_coherence_report(self, coherence_check: Dict):
        """Display story coherence validation report"""
        print("=" * 70)
        print("📖 STORY COHERENCE VALIDATION REPORT")
        print("=" * 70)
        print()

        # Coherence Score
        coherence_score = coherence_check.get('coherence_score', 'Unknown')
        print(f"📊 COHERENCE SCORE: {coherence_score}")
        print()

        # Story Logic
        story_logic = coherence_check.get('story_logic', {})
        logic_status = story_logic.get('status', 'unknown')
        logic_assessment = story_logic.get('assessment', 'No assessment provided')
        
        print("🧠 STORY LOGIC:")
        print("━" * 70)
        print(f"  Status: {'✅' if logic_status == 'valid' else '⚠️'} {logic_status}")
        print(f"  Assessment: {logic_assessment}")
        print()

        # Character Consistency
        character_consistency = coherence_check.get('character_consistency', {})
        consistent_chars = character_consistency.get('consistent_characters', [])
        authenticity = character_consistency.get('authenticity', 'unknown')
        
        print("👥 CHARACTER CONSISTENCY:")
        print("━" * 70)
        print(f"  Consistent Characters: {', '.join(consistent_chars) if consistent_chars else 'None listed'}")
        print(f"  Authenticity: {'✅' if authenticity == 'genuine' else '⚠️'} {authenticity}")
        print()

        # Emotional Authenticity
        emotional_auth = coherence_check.get('emotional_authenticity', {})
        earned_moments = emotional_auth.get('earned_moments', 0)
        emotional_arc = emotional_auth.get('emotional_arc', 'unknown')
        emotional_assessment = emotional_auth.get('assessment', 'No assessment provided')
        
        print("💝 EMOTIONAL AUTHENTICITY:")
        print("━" * 70)
        print(f"  Earned Moments: {earned_moments}")
        print(f"  Emotional Arc: {'✅' if emotional_arc == 'believable' else '⚠️'} {emotional_arc}")
        print(f"  Assessment: {emotional_assessment}")
        print()

        # Issues and Recommendations
        issues = coherence_check.get('issues_found', [])
        recommendations = coherence_check.get('recommendations', [])
        
        print("🔍 ISSUES FOUND:")
        print("━" * 70)
        if issues:
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("  ✅ No issues found")
        print()

        print("💡 RECOMMENDATIONS:")
        print("━" * 70)
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  ✅ No recommendations")
        print()

        print("=" * 70)
        print()

    async def execute_story_coherence_validation(self, episode_number: int, script: Dict) -> Dict:
        """Task 1: Validate story logic and character consistency"""
        try:
            prompt = self.config.get_prompt('story_coherence_validation')

            # Prepare script content
            script_content = self._format_script_for_analysis(script)

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
            validation_data = extract_json(response)

            return validation_data.get('story_coherence', {})

        except Exception as e:
            print(f"❌ Story coherence validation failed: {str(e)}")
            raise

    async def execute_minimal_enhancement(self, episode_number: int, script: Dict, coherence_check: Dict) -> Dict:
        """Task 2: Generate minimal coherence enhancements"""
        try:
            prompt = self.config.get_prompt('minimal_enhancement')

            # Prepare script content
            script_content = self._format_script_for_analysis(script)

            # Prepare coherence issues
            coherence_issues = self._format_coherence_issues(coherence_check)

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script_content,
                coherence_issues=coherence_issues
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            enhancement_data = extract_json(response)

            return enhancement_data.get('coherence_enhancements', {})

        except Exception as e:
            print(f"❌ Minimal enhancement failed: {str(e)}")
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

    def _format_coherence_issues(self, coherence_check: Dict) -> str:
        """Format coherence issues for enhancement prompt"""
        issues = coherence_check.get('issues_found', [])
        recommendations = coherence_check.get('recommendations', [])
        
        parts = []
        
        if issues:
            parts.append("ISSUES FOUND:")
            for issue in issues:
                parts.append(f"- {issue}")
        else:
            parts.append("ISSUES FOUND: None")
        
        parts.append("")
        
        if recommendations:
            parts.append("RECOMMENDATIONS:")
            for rec in recommendations:
                parts.append(f"- {rec}")
        else:
            parts.append("RECOMMENDATIONS: None")
        
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
        """Display enhanced script with coherence improvements"""
        print("=" * 70)
        print(f"✨ EPISODE {episode_number}: COHERENCE-ENHANCED SCRIPT")
        print("=" * 70)
        print()

        enhancements = enhanced.get('enhancements', [])
        total_changes = enhanced.get('total_changes', len(enhancements))
        enhancement_type = enhanced.get('enhancement_type', 'unknown')
        preservation_status = enhanced.get('preservation_status', 'Unknown')

        print("COHERENCE ENHANCEMENT STATISTICS:")
        print("━" * 70)
        print(f"  • Total Enhancements: {total_changes}")
        print(f"  • Enhancement Type: {enhancement_type}")
        print(f"  • Preservation Status: {preservation_status}")
        print()

        print("COHERENCE ENHANCEMENTS MADE:")
        print("━" * 70)

        for i, enhancement in enumerate(enhancements[:10], 1):
            enhancement_type = enhancement.get('type', 'unknown')
            scene_num = enhancement.get('scene_number', '?')
            reason = enhancement.get('reason', '')

            print(f"  {i}. [{enhancement_type.upper()}] Scene {scene_num}")
            print(f"     Reason: {reason}")

        if len(enhancements) > 10:
            print(f"  ... and {len(enhancements) - 10} more enhancements")

        print()
        print("=" * 70)
        print()

    async def human_review(self, episode_number: int, enhanced: Dict, original: Dict) -> str:
        """Human review interface"""
        print("=" * 70)
        print("⭐ COHERENCE-ENHANCED SCRIPT REVIEW")
        print("=" * 70)
        print()

        total_changes = enhanced.get('total_changes', 0)
        enhancement_type = enhanced.get('enhancement_type', 'Unknown')

        print(f"Episode {episode_number} coherence enhancement complete:")
        print(f"  • {total_changes} coherence improvements made")
        print(f"  • Enhancement Type: {enhancement_type}")
        print()
        print("OPTIONS:")
        print("  [Enter] - Approve and save (recommended)")
        print("  [R]     - Regenerate coherence enhancements")
        print("  [V]     - View complete enhanced script")
        print("  [D]     - View detailed enhancement report")
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
            print("✅ Coherence-enhanced script approved. Saving files...")
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
        """Display detailed coherence enhancement report"""
        enhancements = enhanced.get('enhancements', [])

        print("\n" + "=" * 70)
        print("DETAILED COHERENCE ENHANCEMENT REPORT")
        print("=" * 70 + "\n")

        for i, enhancement in enumerate(enhancements, 1):
            print(f"\nENHANCEMENT {i}:")
            print(f"  Type: {enhancement.get('type', 'unknown')}")
            print(f"  Scene: {enhancement.get('scene_number', '?')}")
            print(f"  Reason: {enhancement.get('reason', '')}")
            print(f"  Explanation: {enhancement.get('explanation', '')}")

            original = enhancement.get('original_content', '')
            enhanced_content = enhancement.get('enhanced_content', '')

            if original:
                print(f"  Original: {original[:200]}")
            if enhanced_content:
                print(f"  Enhanced: {enhanced_content[:200]}")

            print("-" * 70)

        input("\nPress Enter to return to review menu...")

    async def save_episode_outputs(self, episode_number: int, enhanced: Dict,
                                   coherence_check: Dict):
        """Save episode in multiple formats"""
        print()
        print("=" * 70)
        print("💾 SAVING COHERENCE VALIDATION FILES")
        print("=" * 70)
        print()

        # Create episode subdirectory
        episode_dir = self.output_dir / f"episode_{episode_number:02d}"
        episode_dir.mkdir(exist_ok=True)

        # 1. Save JSON with all validation + enhanced script
        json_filename = f"episode_{episode_number:02d}_coherence_enhanced.json"
        json_path = episode_dir / json_filename

        full_data = {
            'session_id': self.session_id,
            'episode_number': episode_number,
            'validated_at': datetime.now().isoformat(),
            'story_coherence_check': coherence_check,
            'coherence_enhancements': enhanced
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_path}")

        # 2. Save Enhanced Script (Plain Text)
        txt_filename = f"episode_{episode_number:02d}_coherence_enhanced.txt"
        txt_path = episode_dir / txt_filename

        txt_content = enhanced.get('full_enhanced_script', '')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print(f"✅ Saved Enhanced Script: {txt_path}")

        # 3. Save Coherence Validation Report
        report_filename = f"episode_{episode_number:02d}_coherence_report.txt"
        report_path = episode_dir / report_filename

        report_content = self.generate_coherence_report(episode_number, coherence_check, enhanced)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Saved Coherence Report: {report_path}")

        # 4. Save to Redis for Station 24+
        redis_key = f"audiobook:{self.session_id}:station_23:episode_{episode_number:02d}"
        await self.redis_client.set(redis_key, json.dumps(full_data), expire=604800)  # 7 days
        print(f"✅ Saved to Redis: {redis_key}")

        print()

    def generate_coherence_report(self, episode_number: int, coherence_check: Dict, enhanced: Dict) -> str:
        """Generate comprehensive coherence validation report"""
        lines = []

        lines.append("=" * 70)
        lines.append(f"EPISODE {episode_number} STORY COHERENCE REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Session: {self.session_id}")
        lines.append("")

        # Coherence Score
        coherence_score = coherence_check.get('coherence_score', 'Unknown')
        lines.append("COHERENCE SCORE:")
        lines.append("━" * 70)
        lines.append(f"  Score: {coherence_score}")
        lines.append("")

        # Story Logic
        story_logic = coherence_check.get('story_logic', {})
        logic_status = story_logic.get('status', 'unknown')
        logic_assessment = story_logic.get('assessment', 'No assessment provided')
        lines.append("STORY LOGIC:")
        lines.append("━" * 70)
        lines.append(f"  Status: {logic_status}")
        lines.append(f"  Assessment: {logic_assessment}")
        lines.append("")

        # Character Consistency
        character_consistency = coherence_check.get('character_consistency', {})
        consistent_chars = character_consistency.get('consistent_characters', [])
        authenticity = character_consistency.get('authenticity', 'unknown')
        lines.append("CHARACTER CONSISTENCY:")
        lines.append("━" * 70)
        lines.append(f"  Consistent Characters: {', '.join(consistent_chars) if consistent_chars else 'None listed'}")
        lines.append(f"  Authenticity: {authenticity}")
        lines.append("")

        # Emotional Authenticity
        emotional_auth = coherence_check.get('emotional_authenticity', {})
        earned_moments = emotional_auth.get('earned_moments', 0)
        emotional_arc = emotional_auth.get('emotional_arc', 'unknown')
        emotional_assessment = emotional_auth.get('assessment', 'No assessment provided')
        lines.append("EMOTIONAL AUTHENTICITY:")
        lines.append("━" * 70)
        lines.append(f"  Earned Moments: {earned_moments}")
        lines.append(f"  Emotional Arc: {emotional_arc}")
        lines.append(f"  Assessment: {emotional_assessment}")
        lines.append("")

        # Issues and Recommendations
        issues = coherence_check.get('issues_found', [])
        recommendations = coherence_check.get('recommendations', [])
        lines.append("ISSUES FOUND:")
        lines.append("━" * 70)
        if issues:
            for i, issue in enumerate(issues, 1):
                lines.append(f"  {i}. {issue}")
        else:
            lines.append("  No issues found")
        lines.append("")

        lines.append("RECOMMENDATIONS:")
        lines.append("━" * 70)
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"  {i}. {rec}")
        else:
            lines.append("  No recommendations")
        lines.append("")

        # Enhancements
        total_changes = enhanced.get('total_changes', 0)
        enhancement_type = enhanced.get('enhancement_type', 'unknown')
        lines.append("COHERENCE ENHANCEMENTS:")
        lines.append("━" * 70)
        lines.append(f"  Total Changes: {total_changes}")
        lines.append(f"  Enhancement Type: {enhancement_type}")
        lines.append("")

        enhancements = enhanced.get('enhancements', [])
        for i, enhancement in enumerate(enhancements, 1):
            lines.append(f"{i}. [{enhancement.get('type', 'unknown').upper()}] Scene {enhancement.get('scene_number', '?')}")
            lines.append(f"   Reason: {enhancement.get('reason', '')}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def ask_continue_validation(self) -> bool:
        """Ask if user wants to continue validation"""
        print()
        print("=" * 70)
        print("⭐ CONTINUE COHERENCE VALIDATION?")
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
        print("Resume coherence validation anytime by running Station 23 again.")
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
