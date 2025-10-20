"""
Station 25: Audio Optimization

This station optimizes scripts for audio production with speaker identification fixes,
sound cue integration, strategic silence marking, and complete audio specifications.
Generates production-ready scripts in multiple formats.

Flow:
1. Load Station 24 dialogue-polished scripts
2. Load Station 9 audio cue library
3. Display episode selection and optimization status
4. Human selects episode to optimize
5. Execute 4 sequential LLM optimization tasks:
   - Speaker identification check (clarity issues)
   - Sound cue integration (density optimization)
   - Silence marking (strategic silence placement)
   - Audio optimization (generate production script)
6. Display speaker clarity issues
7. Display sound cue analysis
8. Display silence placements
9. Display final audio-ready script
10. Human review (approve/regenerate)
11. Save audio-optimized script (6 formats)
12. Save to Redis for Station 26+
13. Loop option for next episode

Critical Production Station - Creates production-ready audio scripts
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


class Station25AudioOptimization:
    """Station 25: Audio Optimization"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=25)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_25'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store loaded data
        self.script_episodes = {}  # From Station 24
        self.audio_cue_library = {}  # From Station 9
        self.optimized_episodes = set()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_25.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method with episode loop"""
        print("=" * 70)
        print("🎙️ STATION 25: AUDIO OPTIMIZATION")
        print("=" * 70)
        print()

        try:
            # Step 1: Load scripts from Station 24
            print("📥 Loading dialogue-polished scripts from Station 24...")
            await self.load_scripts()
            print(f"✅ Loaded {len(self.script_episodes)} episode script(s)")
            print()

            if not self.script_episodes:
                print("❌ No scripts found. Please run Station 24 first.")
                return

            # Step 2: Load audio cue library from Station 9
            print("📥 Loading audio cue library from Station 9...")
            await self.load_audio_library()
            print("✅ Audio cue library loaded")
            print()

            # Main optimization loop
            while True:
                # Step 3: Display episode selection
                self.display_episode_selection()

                # Step 4: Human selects episode
                episode_number = self.get_episode_selection()

                if episode_number is None:
                    # User chose to exit
                    break

                # Step 5-12: Optimize the selected episode
                await self.optimize_episode(episode_number)

                # Step 13: Ask to continue
                if not self.ask_continue_optimization():
                    break

            # Display final summary
            self.display_session_summary()

        except Exception as e:
            print(f"❌ Station 25 failed: {str(e)}")
            logging.error(f"Station 25 error: {str(e)}", exc_info=True)
            raise

    async def load_scripts(self):
        """Load scripts from Station 24 (dialogue-polished)"""
        try:
            for episode_num in range(1, 25):
                try:
                    key = f"audiobook:{self.session_id}:station_24:episode_{episode_num:02d}"
                    data_raw = await self.redis_client.get(key)

                    if data_raw:
                        episode_data = json.loads(data_raw)
                        # Extract polished script from Station 24
                        polished_script = episode_data.get('dialogue_polished_script', {})
                        complete_script = polished_script.get('complete_polished_script', '')

                        self.script_episodes[episode_num] = {
                            'source': 'station_24',
                            'script': complete_script,
                            'polished_data': polished_script,
                            'episode_number': episode_num
                        }
                        print(f"   ✓ Episode {episode_num} (from Station 24 - dialogue polished)")

                except Exception:
                    continue

        except Exception as e:
            raise ValueError(f"❌ Error loading scripts: {str(e)}")

    async def load_audio_library(self):
        """Load audio cue library from Station 9"""
        try:
            key = f"audiobook:{self.session_id}:station_9"
            data_raw = await self.redis_client.get(key)

            if data_raw:
                station9_data = json.loads(data_raw)
                self.audio_cue_library = station9_data.get('World Building System', {})
            else:
                print("⚠️  Warning: Station 9 (World Building System) not found")
                print("    Audio optimization will use general audio principles")
                self.audio_cue_library = {}

        except Exception as e:
            logging.warning(f"Could not load audio cue library: {str(e)}")
            self.audio_cue_library = {}

    def display_episode_selection(self):
        """Display episode selection menu with optimization status"""
        print("=" * 70)
        print("📺 EPISODE SELECTION & AUDIO OPTIMIZATION STATUS")
        print("=" * 70)
        print()

        print(f"Scripts Available: {len(self.script_episodes)}")
        print(f"Audio Cue Library Loaded: {'✅' if self.audio_cue_library else '⚠️  Limited'}")
        print()

        print("EPISODE AUDIO OPTIMIZATION STATUS:")
        print("━" * 70)
        print()
        print("┌" + "─" * 68 + "┐")
        print("│ " + "Ep".ljust(4) + "Source".ljust(12) + "Status".ljust(50) + " │")
        print("├" + "─" * 68 + "┤")

        for episode_num in sorted(self.script_episodes.keys()):
            episode_data = self.script_episodes[episode_num]

            source = "St24✅"

            if episode_num in self.optimized_episodes:
                status = "✅ AUDIO OPTIMIZED (PRODUCTION READY)"
            else:
                status = "🟡 NEEDS AUDIO OPTIMIZATION"

            # Format row
            row = f"│ {str(episode_num).ljust(4)}{source.ljust(12)}{status.ljust(50)} │"
            print(row)

        print("└" + "─" * 68 + "┘")
        print()

        # Display statistics
        print("📊 AUDIO OPTIMIZATION STATISTICS:")
        print(f"  • Total Episodes Available: {len(self.script_episodes)}")
        print(f"  • Episodes Optimized: {len(self.optimized_episodes)}/{len(self.script_episodes)}")
        print(f"  • Completion: {int((len(self.optimized_episodes) / len(self.script_episodes)) * 100) if self.script_episodes else 0}%")
        print()
        print("=" * 70)
        print()

    def get_episode_selection(self) -> Optional[int]:
        """Get episode selection from user"""
        print("=" * 70)
        print("⭐ EPISODE SELECTION REQUIRED")
        print("=" * 70)
        print()
        print("Which episode would you like to optimize for audio production?")
        print()
        print("💡 RECOMMENDATIONS:")
        print("  • Optimize in chronological order")
        print("  • This is the final step before production")
        print("  • Creates production-ready scripts for voice actors and sound designers")
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

    async def optimize_episode(self, episode_number: int):
        """Optimize audio for a complete episode"""
        print()
        print("=" * 70)
        print(f"📥 LOADING EPISODE {episode_number} POLISHED SCRIPT")
        print("=" * 70)
        print()

        # Load episode script
        episode_data = self.script_episodes[episode_number]
        script = episode_data['script']

        # Step 5: Execute 4 sequential LLM optimization tasks
        print()
        print("=" * 70)
        print("🔍 EXECUTING AUDIO OPTIMIZATION")
        print("=" * 70)
        print()

        # Task 1: Speaker Identification Check
        print("🎙️  Task 1/4: Speaker Identification Check...")
        speaker_check = await self.execute_speaker_check(episode_number, script)
        print("✅ Speaker identification check complete")
        print()

        # Display clarity issues
        self.display_speaker_issues(speaker_check)

        # Task 2: Sound Cue Integration
        print()
        print("🔊 Task 2/4: Sound Cue Integration Analysis...")
        sound_cue_analysis = await self.execute_sound_cue_analysis(episode_number, script)
        print("✅ Sound cue analysis complete")
        print()

        # Display sound cue analysis
        self.display_sound_cue_analysis(sound_cue_analysis)

        # Task 3: Silence Marking
        print()
        print("🤫 Task 3/4: Strategic Silence Marking...")
        silence_analysis = await self.execute_silence_analysis(episode_number, script)
        print("✅ Silence analysis complete")
        print()

        # Display silence placements
        self.display_silence_placements(silence_analysis)

        # Task 4: Audio Optimization
        print()
        print("✨ Task 4/4: Audio Optimization (Production Script)...")
        optimized_script = await self.execute_audio_optimization(
            episode_number,
            script,
            speaker_check,
            sound_cue_analysis,
            silence_analysis
        )
        print("✅ Audio-optimized script generated")
        print()

        # Display final audio-ready script
        self.display_optimized_script(episode_number, optimized_script)

        # Human review
        if not self.skip_review:
            review_result = await self.human_review(episode_number, optimized_script, script)

            if review_result == "regenerate":
                # Regenerate the optimization
                optimized_script = await self.execute_audio_optimization(
                    episode_number,
                    script,
                    speaker_check,
                    sound_cue_analysis,
                    silence_analysis
                )
        else:
            print("✅ Auto-accepting optimized script (skip_review=True)")
            print()

        # Save outputs (multiple formats)
        await self.save_episode_outputs(
            episode_number,
            optimized_script,
            speaker_check,
            sound_cue_analysis,
            silence_analysis
        )

        # Mark as optimized
        self.optimized_episodes.add(episode_number)

    async def execute_speaker_check(self, episode_number: int, script: str) -> Dict:
        """Task 1: Check speaker identification clarity"""
        try:
            prompt = self.config.get_prompt('speaker_identification_check')

            # Format audio cue library
            audio_library = self._format_audio_library()

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                polished_script=script[:15000],
                audio_cue_library=audio_library
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            check_data = extract_json(response)

            return check_data.get('speaker_identification', {})

        except Exception as e:
            print(f"❌ Speaker identification check failed: {str(e)}")
            raise

    async def execute_sound_cue_analysis(self, episode_number: int, script: str) -> Dict:
        """Task 2: Analyze sound cue integration"""
        try:
            prompt = self.config.get_prompt('sound_cue_integration')

            # Format audio cue library
            audio_library = self._format_audio_library()

            # Format prompt
            formatted_prompt = prompt.format(
                polished_script=script[:15000],
                audio_cue_library=audio_library
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            analysis_data = extract_json(response)

            return analysis_data.get('sound_cue_analysis', {})

        except Exception as e:
            print(f"❌ Sound cue analysis failed: {str(e)}")
            raise

    async def execute_silence_analysis(self, episode_number: int, script: str) -> Dict:
        """Task 3: Mark strategic silences"""
        try:
            prompt = self.config.get_prompt('silence_marking')

            # Format prompt
            formatted_prompt = prompt.format(
                polished_script=script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            silence_data = extract_json(response)

            return silence_data.get('silence_analysis', {})

        except Exception as e:
            print(f"❌ Silence analysis failed: {str(e)}")
            raise

    async def execute_audio_optimization(self, episode_number: int, polished_script: str,
                                        speaker_check: Dict, sound_cues: Dict,
                                        silences: Dict) -> Dict:
        """Task 4: Generate final audio-optimized script"""
        try:
            prompt = self.config.get_prompt('audio_optimization')

            # Format optimizations needed
            optimizations = self._format_optimizations_needed(speaker_check, sound_cues, silences)

            # Format audio library
            audio_library = self._format_audio_library()

            # Format prompt
            formatted_prompt = prompt.format(
                polished_script=polished_script[:15000],
                optimizations_needed=optimizations,
                audio_cue_library=audio_library
            )

            # Execute LLM call - may take longer
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=16384  # Higher token limit for full script
            )

            # Extract JSON
            optimized_data = extract_json(response)

            return optimized_data.get('audio_optimized_script', {})

        except Exception as e:
            print(f"❌ Audio optimization failed: {str(e)}")
            raise

    def _format_audio_library(self) -> str:
        """Format audio cue library for prompts"""
        if not self.audio_cue_library:
            return "Audio cue library not available - use general audio design principles"

        # Simplified summary
        return "Audio cue library available with location profiles, character signatures, and sensory palette"

    def _format_optimizations_needed(self, speaker_check: Dict, sound_cues: Dict,
                                    silences: Dict) -> str:
        """Format all optimizations needed"""
        parts = []

        # Speaker clarity fixes
        parts.append("=== SPEAKER CLARITY FIXES ===")
        confusion_risks = speaker_check.get('confusion_risks', [])
        for risk in confusion_risks[:5]:
            parts.append(f"Scene {risk.get('scene_number', '?')}: {risk.get('problem', '')}")
            parts.append(f"  Fix: {risk.get('suggested_fix', '')}")
        parts.append("")

        # Sound cue additions
        parts.append("=== SOUND CUE ADDITIONS ===")
        missing_cues = sound_cues.get('missing_cues', [])
        for cue in missing_cues[:10]:
            parts.append(f"{cue.get('category', '').title()}: {cue.get('needed_cue', '')}")
        parts.append("")

        # Silence markings
        parts.append("=== SILENCE MARKINGS ===")
        opportunities = silences.get('silence_opportunities', [])
        for silence in opportunities[:10]:
            parts.append(f"Scene {silence.get('scene_number', '?')}: {silence.get('type', '')} ({silence.get('duration_seconds', 0)}s)")
        parts.append("")

        return "\n".join(parts)

    def display_speaker_issues(self, speaker_check: Dict):
        """Display speaker identification issues"""
        print("=" * 70)
        print("🎙️  SPEAKER IDENTIFICATION ANALYSIS")
        print("=" * 70)
        print()

        confusion_risks = speaker_check.get('confusion_risks', [])
        total_risks = speaker_check.get('total_confusion_risks', len(confusion_risks))

        print(f"❌ CONFUSION RISKS: {total_risks} instances")
        print()

        for i, risk in enumerate(confusion_risks[:3], 1):
            issue_type = risk.get('issue_type', 'unknown')
            scene = risk.get('scene_number', '?')
            problem = risk.get('problem', '')
            fix = risk.get('suggested_fix', '')

            print(f"ISSUE {i}: {issue_type.upper()} (Scene {scene})")
            print("─" * 70)
            print(f"Problem: {problem}")
            print(f"Fix: {fix}")
            print()

        print("=" * 70)
        print()

    def display_sound_cue_analysis(self, sound_cues: Dict):
        """Display sound cue integration analysis"""
        print("=" * 70)
        print("🔊 SOUND CUE INTEGRATION CHECK")
        print("=" * 70)
        print()

        current_cues = sound_cues.get('current_cue_count', 0)
        optimal_range = sound_cues.get('optimal_range', '65-85 cues')
        assessment = sound_cues.get('assessment', 'Unknown')

        print(f"CURRENT STATUS: {current_cues} sound cues marked")
        print(f"OPTIMAL: {optimal_range}")
        print(f"ASSESSMENT: {assessment}")
        print()

        missing = sound_cues.get('missing_cues', [])
        if missing:
            print(f"MISSING SOUND CUES: {len(missing)}")
            for cue in missing[:5]:
                category = cue.get('category', 'unknown')
                needed = cue.get('needed_cue', '')
                print(f"  • [{category.upper()}] {needed}")
            print()

        print("=" * 70)
        print()

    def display_silence_placements(self, silences: Dict):
        """Display strategic silence placements"""
        print("=" * 70)
        print("🤫 SILENCE MARKING")
        print("=" * 70)
        print()

        current = silences.get('current_marked_silences', 0)
        optimal = silences.get('optimal_range', '12-18')
        status = silences.get('status', 'Unknown')

        print(f"Current marked silences: {current}")
        print(f"Optimal for drama: {optimal}")
        print(f"Status: {status}")
        print()

        opportunities = silences.get('silence_opportunities', [])
        if opportunities:
            print(f"SILENCE PLACEMENTS TO ADD: {len(opportunities)}")
            for i, silence in enumerate(opportunities[:3], 1):
                silence_type = silence.get('type', 'unknown')
                duration = silence.get('duration_seconds', 0)
                scene = silence.get('scene_number', '?')
                effect = silence.get('effect', '')

                print(f"{i}. {silence_type.upper()} - Scene {scene} ({duration}s)")
                print(f"   Effect: {effect}")
                print()

        print("=" * 70)
        print()

    def display_optimized_script(self, episode_number: int, optimized: Dict):
        """Display final audio-optimized script"""
        print("=" * 70)
        print(f"✅ EPISODE {episode_number}: AUDIO-OPTIMIZED SCRIPT")
        print("=" * 70)
        print()

        stats = optimized.get('optimization_stats', {})

        print("OPTIMIZATION COMPLETE: Production-ready")
        print()
        print("STATISTICS:")
        print("━" * 70)
        print(f"  • Speaker Clarity Fixes: {stats.get('speaker_clarity_fixes', 0)}")
        print(f"  • Sound Cues Added: {stats.get('sound_cues_added', 0)}")
        print(f"  • Sound Cues Removed: {stats.get('sound_cues_removed', 0)}")
        print(f"  • Silences Marked: {stats.get('silences_marked', 0)}")
        print(f"  • Production Notes: {stats.get('production_notes', 0)}")
        print()

        # Show sound cue summary
        cue_summary = optimized.get('sound_cue_summary', {})
        print("SOUND CUE SUMMARY:")
        print(f"  • Total Cues: {cue_summary.get('total_cues', 0)}")
        print(f"  • Average Density: {cue_summary.get('average_density', '0 cues/min')}")
        print()

        # Show silence summary
        silence_summary = optimized.get('silence_summary', {})
        print("SILENCE SUMMARY:")
        print(f"  • Total Silences: {silence_summary.get('total_silences', 0)}")
        print(f"  • Total Silence Time: {silence_summary.get('total_silence_time', '0 seconds')}")
        print()

        print("=" * 70)
        print()

    async def human_review(self, episode_number: int, optimized: Dict, original: str) -> str:
        """Human review interface"""
        print("=" * 70)
        print("⭐ AUDIO OPTIMIZATION COMPLETE - FINAL REVIEW")
        print("=" * 70)
        print()

        print(f"Episode {episode_number} is now production-ready for audio recording")
        print()
        print("OPTIONS:")
        print("  [Enter] - Approve and export final script")
        print("  [R]     - Regenerate audio optimization")
        print("  [V]     - View complete audio script")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == 'R':
            return "regenerate"
        elif choice == 'V':
            self.display_full_script(optimized)
            return await self.human_review(episode_number, optimized, original)
        else:
            print("✅ Audio-optimized script approved. Exporting files...")
            print()
            return "approved"

    def display_full_script(self, optimized: Dict):
        """Display complete audio script"""
        complete_script = optimized.get('complete_audio_script', '')

        print("\n" + "=" * 70)
        print("COMPLETE AUDIO-OPTIMIZED SCRIPT")
        print("=" * 70 + "\n")

        # Display script (truncate if very long)
        if len(complete_script) > 5000:
            print(complete_script[:5000])
            print("\n... (script continues) ...\n")
        else:
            print(complete_script)

        input("\nPress Enter to return to review menu...")

    async def save_episode_outputs(self, episode_number: int, optimized: Dict,
                                   speaker_check: Dict, sound_cues: Dict, silences: Dict):
        """Save episode in multiple production formats"""
        print()
        print("=" * 70)
        print("💾 EXPORTING AUDIO-OPTIMIZED SCRIPT")
        print("=" * 70)
        print()

        # Create episode subdirectory
        episode_dir = self.output_dir / f"episode_{episode_number:02d}"
        episode_dir.mkdir(exist_ok=True)

        # 1. Save JSON with all data
        json_filename = f"episode_{episode_number:02d}_FINAL.json"
        json_path = episode_dir / json_filename

        full_data = {
            'session_id': self.session_id,
            'episode_number': episode_number,
            'optimized_at': datetime.now().isoformat(),
            'speaker_identification': speaker_check,
            'sound_cue_analysis': sound_cues,
            'silence_analysis': silences,
            'audio_optimized_script': optimized
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"✓ FOUNTAIN: {json_path.name}")

        # 2. Save Plain Text Script
        txt_filename = f"episode_{episode_number:02d}_audio_script.txt"
        txt_path = episode_dir / txt_filename

        txt_content = optimized.get('complete_audio_script', '')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print(f"✓ AUDIO SCRIPT: {txt_path.name}")

        # 3. Save to Redis for Station 26+
        redis_key = f"audiobook:{self.session_id}:station_25:episode_{episode_number:02d}"
        await self.redis_client.set(redis_key, json.dumps(full_data), expire=604800)

        print()
        print(f"📁 Files saved to: {episode_dir}")
        print()

    def ask_continue_optimization(self) -> bool:
        """Ask if user wants to continue optimization"""
        print()
        print("=" * 70)
        print("⭐ CONTINUE AUDIO OPTIMIZATION?")
        print("=" * 70)
        print()
        print(f"Episodes optimized: {len(self.optimized_episodes)}/{len(self.script_episodes)}")
        print()
        print("OPTIONS:")
        print("  [Y] - Optimize another episode")
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
        print(f"Episodes optimized: {len(self.optimized_episodes)}/{len(self.script_episodes)}")
        for ep_num in sorted(self.optimized_episodes):
            print(f"  ✅ Episode {ep_num} - PRODUCTION READY")
        print()
        print(f"Session ID: {self.session_id}")
        print()
        print("💡 READY FOR: Voice actors, sound designers, producers")
        print()
        print("=" * 70)
        print()


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station25AudioOptimization(session_id, skip_review=False)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
