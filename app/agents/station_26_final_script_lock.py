"""
Station 26: Final Episode Script Lock

This station finalizes scripts to production-ready state through word count
expansion, complete audio markup finalization, performance notes addition,
and comprehensive production validation. Generates locked script packages for
all production teams.

Flow:
1. Load Station 25 audio-optimized scripts
2. Load Station 11 runtime planning (word count targets)
3. Display episode selection and finalization status
4. Human selects episode to finalize
5. Execute 4 sequential LLM finalization tasks:
   - Word count expansion (expand to target)
   - Audio markup finalization (complete specifications)
   - Performance notes addition (director/actor guidance)
   - Production validation (final quality check)
6. Display expansion areas
7. Display complete audio specifications
8. Display performance notes summary
9. Display final quality check results
10. Human review (approve lock/regenerate/edit)
11. Save final locked script + production package
12. Save to Redis for Station 27+
13. Loop option for next episode

Critical Production Station - Creates locked, production-ready scripts
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


class Station26FinalScriptLock:
    """Station 26: Final Episode Script Lock"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=26)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_26'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store loaded data
        self.script_episodes = {}  # From Station 25
        self.runtime_targets = {}  # From Station 11
        self.locked_episodes = set()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_26.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method with episode loop"""
        print("=" * 70)
        print("🎬 STATION 26: FINAL EPISODE SCRIPT LOCK")
        print("=" * 70)
        print()

        try:
            # Step 1: Load scripts from Station 25
            print("📥 Loading audio-optimized scripts from Station 25...")
            await self.load_scripts()
            print(f"✅ Loaded {len(self.script_episodes)} episode script(s)")
            print()

            if not self.script_episodes:
                print("❌ No scripts found. Please run Station 25 first.")
                return

            # Step 2: Load runtime targets from Station 11
            print("📥 Loading runtime targets from Station 11...")
            await self.load_runtime_targets()
            print("✅ Runtime targets loaded")
            print()

            # Main finalization loop
            while True:
                # Step 3: Display episode selection
                self.display_episode_selection()

                # Step 4: Human selects episode
                episode_number = self.get_episode_selection()

                if episode_number is None:
                    break

                # Step 5-12: Finalize the selected episode
                await self.finalize_episode(episode_number)

                # Step 13: Ask to continue
                if not self.ask_continue_finalization():
                    break

            # Display final summary
            self.display_session_summary()

        except Exception as e:
            print(f"❌ Station 26 failed: {str(e)}")
            logging.error(f"Station 26 error: {str(e)}", exc_info=True)
            raise

    async def load_scripts(self):
        """Load scripts from Station 25"""
        try:
            for episode_num in range(1, 25):
                try:
                    key = f"audiobook:{self.session_id}:station_25:episode_{episode_num:02d}"
                    data_raw = await self.redis_client.get(key)

                    if data_raw:
                        episode_data = json.loads(data_raw)
                        optimized_script = episode_data.get('audio_optimized_script', {})
                        complete_script = optimized_script.get('complete_audio_script', '')

                        # If complete_audio_script is empty, reconstruct from scenes
                        if not complete_script or (isinstance(complete_script, list) and len(complete_script) == 0):
                            complete_script = self._reconstruct_script_from_scenes(optimized_script)

                        # Handle if it's a list
                        if isinstance(complete_script, list):
                            complete_script = '\n'.join(str(item) for item in complete_script)

                        self.script_episodes[episode_num] = {
                            'source': 'station_25',
                            'script': complete_script,
                            'optimized_data': optimized_script,
                            'episode_number': episode_num
                        }
                        print(f"   ✓ Episode {episode_num} (from Station 25 - audio optimized)")

                except Exception:
                    continue

        except Exception as e:
            raise ValueError(f"❌ Error loading scripts: {str(e)}")

    def _convert_to_string(self, content: Any) -> str:
        """Convert any content type to string"""
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            converted_parts = []
            for item in content:
                if isinstance(item, dict):
                    converted_parts.append(json.dumps(item))
                else:
                    converted_parts.append(str(item))
            return '\n'.join(converted_parts)
        elif isinstance(content, dict):
            return json.dumps(content)
        else:
            return str(content)

    def _reconstruct_script_from_scenes(self, optimized_script: Dict) -> str:
        """Reconstruct complete script text from scenes data"""
        parts = []
        scenes = optimized_script.get('scenes', [])

        for scene in scenes:
            # Add scene heading
            heading = scene.get('heading', 'SCENE')
            parts.append(f"\n{heading}")
            parts.append("=" * 70)

            # Add acoustic properties
            acoustic = scene.get('acoustic_properties', '')
            if acoustic:
                parts.append(f"[ACOUSTIC: {acoustic}]")

            # Add ambient layers
            ambient = scene.get('ambient_layers', [])
            if ambient:
                parts.append(f"[AMBIENT: {', '.join(ambient)}]")

            parts.append("")

            # Add audio script
            audio_script = scene.get('audio_script', [])
            if isinstance(audio_script, list):
                for line in audio_script:
                    if isinstance(line, dict):
                        character = line.get('character', '')
                        vocal_direction = line.get('vocal_direction', '')
                        dialogue = line.get('dialogue', '')
                        sound_cues = line.get('sound_cues', [])

                        # Format character line
                        if character:
                            if vocal_direction:
                                parts.append(f"{character}: ({vocal_direction})")
                            else:
                                parts.append(f"{character}:")
                            parts.append(f"  {dialogue}")

                        # Add sound cues
                        if sound_cues:
                            for cue in sound_cues:
                                parts.append(f"  {cue}")
                        parts.append("")
            elif isinstance(audio_script, str):
                parts.append(audio_script)

        return "\n".join(parts)

    async def load_runtime_targets(self):
        """Load runtime targets from Station 11"""
        try:
            key = f"audiobook:{self.session_id}:station_11"
            data_raw = await self.redis_client.get(key)

            if data_raw:
                station11_data = json.loads(data_raw)
                runtime_grid = station11_data.get('runtime_planning_grid', {})
                episode_breakdown = runtime_grid.get('episode_breakdown', [])

                for ep in episode_breakdown:
                    ep_num = ep.get('episode_number')
                    if ep_num:
                        word_budget = ep.get('word_budget', {})
                        self.runtime_targets[ep_num] = {
                            'total_words': word_budget.get('total_words', 4500),
                            'runtime': ep.get('estimated_runtime', '45:00')
                        }
            else:
                print("⚠️  Warning: Station 11 (Runtime Planning) not found")
                # Set default targets
                for ep_num in self.script_episodes.keys():
                    self.runtime_targets[ep_num] = {'total_words': 4500, 'runtime': '45:00'}

        except Exception as e:
            logging.warning(f"Could not load runtime targets: {str(e)}")
            # Set defaults
            for ep_num in self.script_episodes.keys():
                self.runtime_targets[ep_num] = {'total_words': 4500, 'runtime': '45:00'}

    def display_episode_selection(self):
        """Display episode selection with finalization status"""
        print("=" * 70)
        print("📺 EPISODE SELECTION & FINALIZATION STATUS")
        print("=" * 70)
        print()

        print(f"Scripts Available: {len(self.script_episodes)}")
        print()
        print("EPISODE FINALIZATION STATUS:")
        print("━" * 70)
        print()
        print("┌" + "─" * 68 + "┐")
        print("│ " + "Ep".ljust(4) + "Words".ljust(10) + "Target".ljust(12) + "Status".ljust(40) + " │")
        print("├" + "─" * 68 + "┤")

        for episode_num in sorted(self.script_episodes.keys()):
            episode_data = self.script_episodes[episode_num]
            script = episode_data['script']
            word_count = len(script.split())

            target = self.runtime_targets.get(episode_num, {}).get('total_words', 4500)
            gap = target - word_count

            if episode_num in self.locked_episodes:
                status = "🔒 LOCKED v1.0"
            elif gap <= 0:
                status = "✅ READY TO LOCK"
            else:
                status = f"🟡 NEEDS {gap} MORE WORDS"

            row = f"│ {str(episode_num).ljust(4)}{str(word_count).ljust(10)}{str(target).ljust(12)}{status.ljust(40)} │"
            print(row)

        print("└" + "─" * 68 + "┘")
        print()
        print(f"Episodes Locked: {len(self.locked_episodes)}/{len(self.script_episodes)}")
        print()
        print("=" * 70)
        print()

    def get_episode_selection(self) -> Optional[int]:
        """Get episode selection from user"""
        print("=" * 70)
        print("⭐ EPISODE SELECTION REQUIRED")
        print("=" * 70)
        print()
        print("Which episode would you like to finalize and lock?")
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

    async def finalize_episode(self, episode_number: int):
        """Finalize episode to production-ready state"""
        print()
        print("=" * 70)
        print(f"📋 EPISODE {episode_number} STATUS - PRE-FINALIZATION")
        print("=" * 70)
        print()

        # Load episode script
        episode_data = self.script_episodes[episode_number]
        script = episode_data['script']
        current_word_count = len(script.split())
        target_word_count = self.runtime_targets.get(episode_number, {}).get('total_words', 4500)
        word_gap = max(0, target_word_count - current_word_count)

        print(f"Current Word Count: {current_word_count}")
        print(f"Target Word Count: {target_word_count}")
        print(f"Gap: {word_gap} words")
        print()

        # Step 5: Execute 4 sequential LLM finalization tasks
        print("=" * 70)
        print("🔍 EXECUTING FINALIZATION TASKS")
        print("=" * 70)
        print()

        # Task 1: Word Count Expansion
        print("📝 Task 1/4: Word Count Expansion...")
        expanded_script = await self.execute_word_count_expansion(
            episode_number, script, current_word_count, target_word_count, word_gap
        )
        script_content = expanded_script.get('expanded_full_script', '')
        script_content = self._convert_to_string(script_content)
        expanded_word_count = len(script_content.split())
        print(f"✅ Expanded to {expanded_word_count} words")
        print()

        # Task 2: Audio Markup Finalization
        print("🎵 Task 2/4: Audio Markup Finalization...")
        expanded_script_text = self._convert_to_string(expanded_script.get('expanded_full_script', script))
        audio_finalized = await self.execute_audio_finalization(
            episode_number,
            expanded_script_text
        )
        print("✅ Audio markup finalized")
        print()

        # Task 3: Performance Notes Addition
        print("🎭 Task 3/4: Performance Notes Addition...")
        audio_script_text = self._convert_to_string(audio_finalized.get('complete_audio_script', expanded_script_text))
        performance_added = await self.execute_performance_notes(
            episode_number,
            audio_script_text
        )
        print("✅ Performance notes added")
        print()

        # Task 4: Production Validation
        print("✅ Task 4/4: Production Validation...")
        perf_notes_text = self._convert_to_string(performance_added.get('script_with_performance_notes', script))
        validation = await self.execute_production_validation(
            episode_number,
            perf_notes_text
        )
        print("✅ Production validation complete")
        print()

        # Display validation results
        self.display_validation_results(episode_number, validation, expanded_script)

        # Human review
        if not self.skip_review:
            review_result = await self.human_review(episode_number, validation)

            if review_result == "regenerate":
                # Regenerate finalization
                expanded_script = await self.execute_word_count_expansion(
                    episode_number, script, current_word_count, target_word_count, word_gap
                )
                audio_finalized = await self.execute_audio_finalization(
                    episode_number,
                    expanded_script.get('expanded_full_script', script)
                )
                performance_added = await self.execute_performance_notes(
                    episode_number,
                    audio_finalized.get('complete_audio_script', script)
                )
                validation = await self.execute_production_validation(
                    episode_number,
                    performance_added.get('script_with_performance_notes', script)
                )
        else:
            print("✅ Auto-accepting finalized script (skip_review=True)")
            print()

        # Save outputs
        await self.save_episode_outputs(
            episode_number,
            expanded_script,
            audio_finalized,
            performance_added,
            validation
        )

        # Mark as locked
        self.locked_episodes.add(episode_number)

    async def execute_word_count_expansion(self, episode_number: int, script: str,
                                          current_count: int, target_count: int, gap: int) -> Dict:
        """Task 1: Expand script to target word count"""
        try:
            prompt = self.config.get_prompt('word_count_expansion')

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                current_script=script[:15000],
                current_word_count=current_count,
                target_word_count=target_count,
                word_count_gap=gap
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=16384
            )

            # Extract JSON
            expansion_data = extract_json(response)

            return expansion_data.get('word_count_expansion', {})

        except Exception as e:
            print(f"❌ Word count expansion failed: {str(e)}")
            raise

    async def execute_audio_finalization(self, episode_number: int, expanded_script: str) -> Dict:
        """Task 2: Finalize audio markup"""
        try:
            prompt = self.config.get_prompt('audio_markup_finalization')

            # Format prompt
            formatted_prompt = prompt.format(
                expanded_script=expanded_script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            audio_data = extract_json(response)

            return audio_data.get('audio_markup_finalization', {})

        except Exception as e:
            print(f"❌ Audio finalization failed: {str(e)}")
            raise

    async def execute_performance_notes(self, episode_number: int, audio_script: str) -> Dict:
        """Task 3: Add performance notes"""
        try:
            prompt = self.config.get_prompt('performance_notes_addition')

            # Format prompt
            formatted_prompt = prompt.format(
                script=audio_script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            perf_data = extract_json(response)

            return perf_data.get('performance_notes', {})

        except Exception as e:
            print(f"❌ Performance notes failed: {str(e)}")
            raise

    async def execute_production_validation(self, episode_number: int, final_script: str) -> Dict:
        """Task 4: Validate for production"""
        try:
            prompt = self.config.get_prompt('production_validation')

            # Format prompt
            formatted_prompt = prompt.format(
                final_script=final_script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            validation_data = extract_json(response)

            return validation_data.get('production_validation', {})

        except Exception as e:
            print(f"❌ Production validation failed: {str(e)}")
            raise

    def display_validation_results(self, episode_number: int, validation: Dict, expansion: Dict):
        """Display final validation results"""
        print("=" * 70)
        print(f"✅ PRODUCTION VALIDATION - EPISODE {episode_number}")
        print("=" * 70)
        print()

        status = validation.get('validation_status', 'UNKNOWN')
        word_count = validation.get('word_count', 0)
        target_range = validation.get('target_range', 'Unknown')
        ready = validation.get('ready_for_production', False)

        print(f"Status: {status}")
        print(f"Word Count: {word_count}")
        print(f"Target Range: {target_range}")
        print()

        results = validation.get('validation_results', [])
        print("VALIDATION CHECKS:")
        for result in results[:5]:
            check = result.get('check', 'Unknown')
            result_status = result.get('status', '?')
            print(f"  {result_status} {check}")

        print()
        print(f"Production Ready: {'✅ YES' if ready else '❌ NO'}")
        print()
        print("=" * 70)
        print()

    async def human_review(self, episode_number: int, validation: Dict) -> str:
        """Human review interface"""
        print("=" * 70)
        print("⭐ FINAL REVIEW - SCRIPT LOCK DECISION")
        print("=" * 70)
        print()

        ready = validation.get('ready_for_production', False)
        status_msg = "✅ Production Ready" if ready else "⚠️  Needs Review"

        print(f"Episode {episode_number}: {status_msg}")
        print()
        print("⚠️  WARNING: Locking the script means:")
        print("  • No further changes without formal revision")
        print("  • Goes to full production team")
        print("  • Becomes authoritative version")
        print()
        print("OPTIONS:")
        print("  [Enter] - LOCK SCRIPT for production")
        print("  [R]     - Regenerate finalization")
        print("  [V]     - View validation report")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == 'R':
            return "regenerate"
        elif choice == 'V':
            print("\nValidation Details:")
            print(json.dumps(validation, indent=2))
            return await self.human_review(episode_number, validation)
        else:
            print("✅ Script locked for production")
            print()
            return "approved"

    async def save_episode_outputs(self, episode_number: int, expansion: Dict,
                                   audio: Dict, performance: Dict, validation: Dict):
        """Save final locked script and production package"""
        print()
        print("=" * 70)
        print(f"💾 SAVING FINAL LOCKED SCRIPT - EPISODE {episode_number}")
        print("=" * 70)
        print()

        # Create episode subdirectory
        episode_dir = self.output_dir / f"episode_{episode_number:02d}"
        episode_dir.mkdir(exist_ok=True)

        # 1. Save comprehensive JSON
        json_filename = f"episode_{episode_number:02d}_v1.0_FINAL.json"
        json_path = episode_dir / json_filename

        full_data = {
            'session_id': self.session_id,
            'episode_number': episode_number,
            'locked_at': datetime.now().isoformat(),
            'version': '1.0',
            'status': 'LOCKED',
            'word_count_expansion': expansion,
            'audio_markup': audio,
            'performance_notes': performance,
            'validation': validation
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_path.name}")

        # 2. Save Fountain format
        fountain_filename = f"episode_{episode_number:02d}_v1.0_FINAL.fountain"
        fountain_path = episode_dir / fountain_filename

        final_script = expansion.get('expanded_full_script', '')
        final_script = self._convert_to_string(final_script)
        with open(fountain_path, 'w', encoding='utf-8') as f:
            f.write(final_script)
        print(f"✅ Saved Fountain: {fountain_path.name}")

        # 3. Save Production Report
        report_filename = f"episode_{episode_number:02d}_PRODUCTION.txt"
        report_path = episode_dir / report_filename

        report_content = self.generate_production_report(episode_number, expansion, audio, performance, validation)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Saved Report: {report_path.name}")

        # 4. Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_26:episode_{episode_number:02d}"
        await self.redis_client.set(redis_key, json.dumps(full_data), expire=604800)

        print()

    def generate_production_report(self, episode_number: int, expansion: Dict,
                                  audio: Dict, performance: Dict, validation: Dict) -> str:
        """Generate comprehensive production report"""
        lines = []

        lines.append("=" * 70)
        lines.append(f"EPISODE {episode_number} - FINAL LOCKED SCRIPT")
        lines.append("=" * 70)
        lines.append(f"Locked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append(f"Version: 1.0 FINAL")
        lines.append("")

        # Word count
        lines.append("WORD COUNT EXPANSION:")
        lines.append("━" * 70)
        lines.append(f"  Current: {expansion.get('current_word_count', 0)}")
        lines.append(f"  Target: {expansion.get('target_word_count', 0)}")
        lines.append(f"  Final: {expansion.get('final_word_count', 0)}")
        lines.append(f"  Added: {expansion.get('total_words_added', 0)} words")
        lines.append("")

        # Audio
        lines.append("AUDIO MARKUP:")
        lines.append("━" * 70)
        lines.append(f"  Total Elements: {audio.get('total_audio_elements', 0)}")
        lines.append(f"  Completeness: {audio.get('specification_completeness', '0%')}")
        lines.append("")

        # Performance
        lines.append("PERFORMANCE DIRECTION:")
        lines.append("━" * 70)
        lines.append(f"  Total Notes: {performance.get('total_notes_added', 0)}")
        lines.append("")

        # Validation
        lines.append("PRODUCTION VALIDATION:")
        lines.append("━" * 70)
        lines.append(f"  Status: {validation.get('validation_status', 'UNKNOWN')}")
        lines.append(f"  Ready for Production: {'YES' if validation.get('ready_for_production') else 'NO'}")
        lines.append(f"  Issues Found: {validation.get('issues_found', 0)}")
        lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def ask_continue_finalization(self) -> bool:
        """Ask if user wants to continue finalization"""
        print()
        print("=" * 70)
        print("⭐ CONTINUE FINALIZATION?")
        print("=" * 70)
        print()
        print(f"Episodes locked: {len(self.locked_episodes)}/{len(self.script_episodes)}")
        print()
        print("OPTIONS:")
        print("  [Y] - Finalize next episode")
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
        print(f"Episodes locked: {len(self.locked_episodes)}/{len(self.script_episodes)}")
        for ep_num in sorted(self.locked_episodes):
            print(f"  🔒 Episode {ep_num} - v1.0 LOCKED")
        print()
        print(f"Session ID: {self.session_id}")
        print()
        print("✅ Production packages ready for all teams")
        print()
        print("=" * 70)
        print()


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station26FinalScriptLock(session_id, skip_review=False)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
