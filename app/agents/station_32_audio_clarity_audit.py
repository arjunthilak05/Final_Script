"""
Station 32: Audio-Only Clarity Audit

This station evaluates scripts for clarity in audio-only listening context through 4 checks:
1. Scene Setting Clarity - location/time/presence established within 10 seconds
2. Action Comprehension - physical/character/emotional actions trackable from audio
3. Transition Clarity - time/location/POV transitions clear and smooth
4. Information Delivery - natural exposition, no dumps, audio-friendly language

Interactive Flow:
- Human chooses which episode(s) to audit
- Auto-runs 4 clarity checks per episode
- Displays specific issues with scene-by-scene analysis
- Shows audio improvements needed
- Human review: Approve/Fix/Review
- Saves clarity reports + audio improvement specs
- Loop option to audit another episode

Produces: Clarity audit reports, audio improvement specs, sound cue additions, dialogue fixes
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Station32AudioClarityAudit:
    """Station 32: Audio-Only Clarity Audit"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=32)

        # Load YAML config
        self._load_yaml_config()

        self.output_dir = Path("output/station_32")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store analysis data
        self.episode_scripts = {}
        self.audit_results = {}

    def _load_yaml_config(self):
        """Load YAML configuration"""
        import yaml

        config_path = Path(__file__).parent / "configs" / "station_32.yml"
        with open(config_path, "r") as f:
            self.yaml_config = yaml.safe_load(f)

    async def initialize(self):
        """Initialize Redis connection"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution loop"""
        print("\n" + "=" * 70)
        print("🔊 STATION 32: AUDIO-ONLY CLARITY AUDIT")
        print("=" * 70)

        try:
            # Load scripts from Station 26
            print("\n📥 Loading locked scripts from Station 26...")
            await self.load_scripts_from_station_26()

            if not self.episode_scripts:
                print("❌ No scripts found. Run Station 26 first.")
                return

            # Load Station 31 dialogue analysis
            print("📥 Loading Station 31 dialogue analysis...")
            await self.load_station_31_analysis()

            # Main audit loop
            while True:
                episode_num = self.select_episode()
                if episode_num is None:
                    break

                await self.audit_episode(episode_num)

                if not self.ask_continue():
                    break

            # Display final summary
            self.display_final_summary()

        except Exception as e:
            logger.error(f"Station 32 error: {str(e)}", exc_info=True)
            raise

    async def load_scripts_from_station_26(self):
        """Load scripts from Station 26 Redis"""
        for episode_num in range(1, 4):  # Episodes 1-3
            try:
                key = f"audiobook:{self.session_id}:station_26:episode_{episode_num:02d}"
                data = await self.redis_client.get(key)
                if data:
                    episode_data = json.loads(data)
                    self.episode_scripts[episode_num] = episode_data
                    logger.info(f"✓ Loaded Episode {episode_num}")
            except Exception as e:
                logger.warning(f"Episode {episode_num} load failed: {e}")

    async def load_station_31_analysis(self):
        """Load Station 31 dialogue analysis results"""
        self.station_31_data = {}
        for episode_num in range(1, 4):
            try:
                key = f"audiobook:{self.session_id}:station_31:episode_{episode_num:02d}"
                data = await self.redis_client.get(key)
                if data:
                    self.station_31_data[episode_num] = json.loads(data)
                    logger.info(f"✓ Loaded Station 31 data for Episode {episode_num}")
            except Exception as e:
                logger.warning(f"Station 31 data load failed for Episode {episode_num}: {e}")

    def select_episode(self) -> Optional[int]:
        """Interactive episode selection"""
        print("\n" + "=" * 70)
        print("SELECT EPISODE FOR AUDIO CLARITY AUDIT")
        print("=" * 70)

        available = list(self.episode_scripts.keys())
        print(f"\nAvailable episodes: {available}")
        print("Options: 1-3, 'all', 'q' to quit")

        choice = input("\nEnter choice: ").strip().lower()

        if choice == "q":
            return None
        elif choice == "all":
            return "all"
        elif choice.isdigit() and 1 <= int(choice) <= 3:
            return int(choice)
        else:
            print("❌ Invalid choice")
            return self.select_episode()

    async def audit_episode(self, episode_num):
        """Run all 4 clarity audits on episode"""
        if episode_num == "all":
            for ep in sorted(self.episode_scripts.keys()):
                await self._audit_single(ep)
        else:
            await self._audit_single(episode_num)

    async def _audit_single(self, episode_num: int):
        """Audit single episode"""
        print("\n" + "=" * 70)
        print(f"🔊 AUDIO CLARITY AUDIT - EPISODE {episode_num}")
        print("=" * 70)

        script_data = self.episode_scripts[episode_num]
        script_content = script_data.get("word_count_expansion", {}).get(
            "expanded_full_script", ""
        )

        if not script_content:
            print(f"❌ No script content for Episode {episode_num}")
            return

        results = {}

        # Task 1: Scene Setting Clarity
        print("\n[1/4] Auditing Scene Setting Clarity...")
        results["scene_setting"] = await self._audit_scene_setting(
            episode_num, script_content
        )
        self._display_scene_setting(results["scene_setting"])

        # Task 2: Action Comprehension
        print("\n[2/4] Auditing Action Comprehension...")
        results["actions"] = await self._audit_actions(episode_num, script_content)
        self._display_actions(results["actions"])

        # Task 3: Transition Clarity
        print("\n[3/4] Auditing Transition Clarity...")
        results["transitions"] = await self._audit_transitions(
            episode_num, script_content
        )
        self._display_transitions(results["transitions"])

        # Task 4: Information Delivery
        print("\n[4/4] Auditing Information Delivery...")
        results["information"] = await self._audit_information(
            episode_num, script_content
        )
        self._display_information(results["information"])

        # Human Review
        self._human_review(episode_num, results)

        # Save Results
        await self._save_audit_results(episode_num, results)

    async def _audit_scene_setting(self, episode_num: int, content: str) -> Dict:
        """Task 1: Audit scene setting clarity"""
        prompt = self.yaml_config["prompts"]["scene_setting_clarity"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    async def _audit_actions(self, episode_num: int, content: str) -> Dict:
        """Task 2: Audit action comprehension"""
        prompt = self.yaml_config["prompts"]["action_comprehension"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    async def _audit_transitions(self, episode_num: int, content: str) -> Dict:
        """Task 3: Audit transition clarity"""
        prompt = self.yaml_config["prompts"]["transition_clarity"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    async def _audit_information(self, episode_num: int, content: str) -> Dict:
        """Task 4: Audit information delivery"""
        prompt = self.yaml_config["prompts"]["information_delivery"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    def _display_scene_setting(self, results: Dict):
        """Display scene setting findings"""
        analysis = results.get("scene_setting_clarity", {})
        print("\n" + "━" * 70)
        print("📍 SCENE SETTING CLARITY")
        print("━" * 70)

        locations = analysis.get("location_tests", [])
        print(f"\nLocation clarity tested: {len(locations)} scenes")

        unclear = [l for l in locations if l.get("clear_at_seconds", 0) > 10]
        if unclear:
            print(f"\n⚠️  {len(unclear)} locations unclear (>10 seconds):")
            for loc in unclear[:3]:
                print(f"  • Scene {loc.get('scene_number')}: {loc.get('location')}")
                print(f"    Clear at: {loc.get('clear_at_seconds')}s")

        time_tests = analysis.get("time_establishment", [])
        if time_tests:
            unclear_time = [t for t in time_tests if t.get("problem") and "unclear" in t.get("problem", "").lower()]
            if unclear_time:
                print(f"\n⏱️  {len(unclear_time)} time transitions unclear")

    def _display_actions(self, results: Dict):
        """Display action comprehension findings"""
        analysis = results.get("action_comprehension", {})
        print("\n" + "━" * 70)
        print("🎬 ACTION COMPREHENSION")
        print("━" * 70)

        physical = analysis.get("physical_action_tracking", [])
        excellent = [p for p in physical if p.get("clarity_score", 0) >= 9]
        unclear = [p for p in physical if p.get("clarity_score", 0) < 7]

        print(f"\nExcellent action tracking: {len(excellent)}")
        if unclear:
            print(f"⚠️  Unclear actions: {len(unclear)}")
            for act in unclear[:2]:
                print(f"  • {act.get('scene')}")
                print(f"    Problem: {act.get('issue', '')[:60]}...")

    def _display_transitions(self, results: Dict):
        """Display transition clarity findings"""
        analysis = results.get("transition_clarity", {})
        print("\n" + "━" * 70)
        print("🔀 TRANSITION CLARITY")
        print("━" * 70)

        time_trans = analysis.get("time_transitions", [])
        unclear_time = [t for t in time_trans if "unclear" in t.get("assessment", "").lower()]

        print(f"\nTime transitions: {len(time_trans)} total")
        if unclear_time:
            print(f"⚠️  Unclear time passages: {len(unclear_time)}")

        loc_trans = analysis.get("location_transitions", [])
        perfect = [l for l in loc_trans if "perfect" in l.get("assessment", "").lower()]
        print(f"Location transitions: {len(perfect)}/{len(loc_trans)} excellent")

    def _display_information(self, results: Dict):
        """Display information delivery findings"""
        analysis = results.get("information_delivery", {})
        print("\n" + "━" * 70)
        print("📢 INFORMATION DELIVERY")
        print("━" * 70)

        natural = analysis.get("natural_integration", [])
        dumps = analysis.get("exposition_dumps", [])
        overload = analysis.get("information_overload", [])

        print(f"\n✅ Naturally integrated: {len(natural)}")
        if dumps:
            print(f"⚠️  Exposition dumps detected: {len(dumps)}")
        if overload:
            print(f"⚠️  Information overload moments: {len(overload)}")

    def _human_review(self, episode_num: int, results: Dict):
        """Get human approval"""
        print("\n" + "=" * 70)
        print("⭐ AUDIO CLARITY AUDIT COMPLETE - REVIEW REQUIRED")
        print("=" * 70)

        print("\nOptions:")
        print("  [Enter] - Approve and save")
        print("  [F]     - View audio fix specs")
        print("  [R]     - Regenerate audit")
        print("  [S]     - Show summary")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "f":
            self._show_audio_specs(results)
        elif choice == "r":
            print("Regeneration requested (manual follow-up needed)")
        elif choice == "s":
            self._show_summary(results)
        else:
            print("✅ Audit approved")

    def _show_audio_specs(self, results: Dict):
        """Show audio improvement specifications"""
        print("\n" + "━" * 70)
        print("🔧 AUDIO IMPROVEMENT SPECIFICATIONS")
        print("━" * 70)

        analysis = results.get("information", {}).get("information_delivery", {})
        prods = analysis.get("audio_production_notes", {})

        print(f"\nSFX additions needed: {prods.get('sfx_additions_needed', '?')}")
        print(f"Transition bridges: {prods.get('transition_bridges', '?')}")
        print(f"Dialogue rewrites: {prods.get('dialogue_rewrites', '?')}")
        print(f"Action sound cues: {prods.get('action_sound_cues', '?')}")

    def _show_summary(self, results: Dict):
        """Show audit summary"""
        print("\n" + "━" * 70)
        print("📄 AUDIO CLARITY SUMMARY")
        print("━" * 70)

        scene = results.get("scene_setting", {}).get("scene_setting_clarity", {})
        action = results.get("actions", {}).get("action_comprehension", {})

        print(f"\nScene clarity: {scene.get('overall_scene_setting_score', '?')}/10")
        print(f"Action tracking: {action.get('overall_action_comprehension', '?')}/10")

    async def _save_audit_results(self, episode_num: int, results: Dict):
        """Save audit results to files"""
        timestamp = datetime.now().isoformat()

        # Save JSON
        json_file = self.output_dir / f"episode_{episode_num:02d}_clarity_audit.json"
        with open(json_file, "w") as f:
            json.dump(
                {
                    "episode": episode_num,
                    "audit_timestamp": timestamp,
                    "results": results,
                },
                f,
                indent=2,
            )

        # Save to Redis
        key = f"audiobook:{self.session_id}:station_32:episode_{episode_num:02d}"
        await self.redis_client.set(
            key,
            json.dumps(
                {
                    "episode": episode_num,
                    "timestamp": timestamp,
                    "audio_clarity_audit": results,
                }
            ),
        )

        print(f"\n✅ Saved: {json_file.name}")

    def ask_continue(self) -> bool:
        """Ask to continue audits"""
        choice = input("\n\nAudit another episode? (y/n): ").strip().lower()
        return choice == "y"

    def display_final_summary(self):
        """Display final session summary"""
        print("\n" + "=" * 70)
        print("✅ STATION 32 COMPLETE")
        print("=" * 70)
        print("\nAudio-Only Clarity Audit Summary:")
        print(f"  Episodes audited: {len(self.episode_scripts)}")
        print(f"  Output directory: {self.output_dir}")
        print("\n✨ All quality assurance stations complete!")
        print("   Scripts are ready for voice recording and sound design.")
        print("=" * 70 + "\n")


async def main():
    """Main entry point"""
    import sys

    session_id = sys.argv[1] if len(sys.argv) > 1 else "session_test"

    station = Station32AudioClarityAudit(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
