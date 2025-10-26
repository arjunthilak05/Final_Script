"""
Station 31: Dialogue Naturalness Pass

This station evaluates dialogue quality for voice acting through 4 interactive checks:
1. Speakability Check - tongue twisters, breath points, rhythm issues
2. Naturalness Scoring - vocabulary, sentence structure, fillers, interruptions
3. Identity Clarity Check - speaker identification, voice distinction
4. Subtext Verification - layered meaning, emotional authenticity

Interactive Flow:
- Human chooses which episode(s) to analyze
- Auto-runs 4 checks per episode
- Displays detailed findings with examples
- Human review: Approve/Fix/Regenerate
- Saves reports + fixes
- Loop option to analyze another episode

Produces: Dialogue quality reports, fixes, voice actor guidance, production readiness
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


class Station31DialogueNaturalnessPass:
    """Station 31: Dialogue Naturalness Pass"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=31)

        # Load YAML config
        self._load_yaml_config()

        self.output_dir = Path("output/station_31")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store analysis data
        self.episode_scripts = {}
        self.episode_characters = {}
        self.analysis_results = {}

    def _load_yaml_config(self):
        """Load YAML configuration"""
        import yaml
        config_path = Path(__file__).parent / "configs" / "station_31.yml"
        with open(config_path, "r") as f:
            self.yaml_config = yaml.safe_load(f)

    async def initialize(self):
        """Initialize Redis connection"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution loop"""
        print("\n" + "=" * 70)
        print("🎬 STATION 31: DIALOGUE NATURALNESS PASS")
        print("=" * 70)

        try:
            # Load scripts from Station 26
            print("\n📥 Loading locked scripts from Station 26...")
            await self.load_scripts_from_station_26()

            if not self.episode_scripts:
                print("❌ No scripts found. Run Station 26 first.")
                return

            # Main analysis loop
            while True:
                episode_num = self.select_episode()
                if episode_num is None:
                    break

                await self.analyze_episode(episode_num)

                if not self.ask_continue():
                    break

            # Display final summary
            self.display_final_summary()

        except Exception as e:
            logger.error(f"Station 31 error: {str(e)}", exc_info=True)
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

    def select_episode(self) -> Optional[int]:
        """Interactive episode selection"""
        print("\n" + "=" * 70)
        print("SELECT EPISODE FOR ANALYSIS")
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

    async def analyze_episode(self, episode_num):
        """Run all 4 analysis checks on episode"""
        if episode_num == "all":
            for ep in sorted(self.episode_scripts.keys()):
                await self._analyze_single(ep)
        else:
            await self._analyze_single(episode_num)

    async def _analyze_single(self, episode_num: int):
        """Analyze single episode"""
        print("\n" + "=" * 70)
        print(f"🎭 DIALOGUE ANALYSIS - EPISODE {episode_num}")
        print("=" * 70)

        script_data = self.episode_scripts[episode_num]
        script_content = script_data.get("word_count_expansion", {}).get(
            "expanded_full_script", ""
        )

        if not script_content:
            print(f"❌ No script content for Episode {episode_num}")
            return

        results = {}

        # Task 1: Speakability Check
        print("\n[1/4] Running Speakability Check...")
        results["speakability"] = await self._check_speakability(
            episode_num, script_content
        )
        self._display_speakability(results["speakability"])

        # Task 2: Naturalness Scoring
        print("\n[2/4] Running Naturalness Scoring...")
        results["naturalness"] = await self._check_naturalness(
            episode_num, script_content
        )
        self._display_naturalness(results["naturalness"])

        # Task 3: Identity Clarity Check
        print("\n[3/4] Running Identity Clarity Check...")
        results["identity"] = await self._check_identity_clarity(
            episode_num, script_content
        )
        self._display_identity_clarity(results["identity"])

        # Task 4: Subtext Verification
        print("\n[4/4] Running Subtext Verification...")
        results["subtext"] = await self._check_subtext(episode_num, script_content)
        self._display_subtext(results["subtext"])

        # Human Review
        self._human_review(episode_num, results)

        # Save Results
        await self._save_analysis_results(episode_num, results)

    async def _check_speakability(self, episode_num: int, content: str) -> Dict:
        """Task 1: Check speakability"""
        prompt = self.yaml_config["prompts"]["speakability_check"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],  # Limit content size
            characters="Tom, Julia, Dr. Martinez, Sarah, Nurse Linda",
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    async def _check_naturalness(self, episode_num: int, content: str) -> Dict:
        """Task 2: Check naturalness"""
        prompt = self.yaml_config["prompts"]["naturalness_scoring"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],
            characters="Tom, Julia, Dr. Martinez, Sarah, Nurse Linda",
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    async def _check_identity_clarity(self, episode_num: int, content: str) -> Dict:
        """Task 3: Check identity clarity"""
        prompt = self.yaml_config["prompts"]["identity_clarity_check"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],
            characters="Tom, Julia, Dr. Martinez, Sarah, Nurse Linda",
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    async def _check_subtext(self, episode_num: int, content: str) -> Dict:
        """Task 4: Check subtext"""
        prompt = self.yaml_config["prompts"]["subtext_verification"].format(
            episode_id=f"episode_{episode_num:02d}",
            episode_content=content[:3000],
            characters="Tom, Julia, Dr. Martinez, Sarah, Nurse Linda",
        )

        response = await self.agent.generate(prompt, model="anthropic/claude-3.5-sonnet")
        result = extract_json(response)
        return result if isinstance(result, dict) else {}

    def _display_speakability(self, results: Dict):
        """Display speakability findings"""
        analysis = results.get("speakability_analysis", {})
        print("\n" + "━" * 70)
        print("🗣️ SPEAKABILITY CHECK RESULTS")
        print("━" * 70)

        twisters = analysis.get("tongue_twisters", [])
        breath = analysis.get("breath_point_issues", [])
        rhythm = analysis.get("rhythm_issues", [])

        if twisters:
            print(f"\n❌ TONGUE TWISTERS: {len(twisters)} found")
            for i, issue in enumerate(twisters[:3], 1):
                print(f"\n  {i}. {issue.get('location')}")
                print(f"     Current: {issue.get('current_text')}")
                print(f"     Problem: {issue.get('issue_description')}")
                print(f"     Fix: {issue.get('suggested_fix')}")

        if breath:
            print(f"\n⚠️  BREATH ISSUES: {len(breath)} found")
            for i, issue in enumerate(breath[:2], 1):
                print(f"\n  {i}. {issue.get('location')} ({issue.get('word_count')} words)")
                print(f"     Problem: {issue.get('problem')}")

        if rhythm:
            print(f"\n⚠️  RHYTHM ISSUES: {len(rhythm)} found")

        totals = analysis.get("total_issues", {})
        print(f"\n📊 Total Issues: {totals}")

    def _display_naturalness(self, results: Dict):
        """Display naturalness findings"""
        analysis = results.get("naturalness_scoring", {})
        print("\n" + "━" * 70)
        print("📊 NATURALNESS SCORING")
        print("━" * 70)

        for char, data in analysis.items():
            if char != "overall_scores":
                vocab = data.get("vocabulary_appropriateness", {})
                score = vocab.get("score", "?")
                print(f"\n{char}: {score}/5")
                print(f"  • Vocab: {vocab.get('era_appropriate', '?')}")
                print(f"  • Structure: {data.get('sentence_structure', {}).get('score', '?')}/5")

    def _display_identity_clarity(self, results: Dict):
        """Display identity clarity findings"""
        analysis = results.get("identity_clarity", {})
        print("\n" + "━" * 70)
        print("🎭 IDENTITY CLARITY CHECK")
        print("━" * 70)

        test = analysis.get("speaker_identification_test", {})
        print(
            f"\nIdentification Rate: {test.get('identification_rate', '?')}"
        )
        unclear = test.get("unclear_lines", [])
        if unclear:
            print(f"\n⚠️  {len(unclear)} unclear lines found:")
            for line in unclear[:2]:
                print(f"  • \"{line.get('text')}\"")
                print(f"    Could be: {line.get('could_be', [])}")

    def _display_subtext(self, results: Dict):
        """Display subtext findings"""
        analysis = results.get("subtext_analysis", {})
        print("\n" + "━" * 70)
        print("📖 SUBTEXT VERIFICATION")
        print("━" * 70)

        excellent = analysis.get("excellent_subtext", [])
        weak = analysis.get("weak_subtext", [])

        print(f"\n✅ Excellent subtext: {len(excellent)} instances")
        print(f"⚠️  Weak subtext: {len(weak)} instances")

        if weak:
            print(f"\nWeak subtext examples:")
            for ex in weak[:2]:
                print(f"  • Scene: {ex.get('scene')}")
                print(f"    Problem: {ex.get('problem')}")

    def _human_review(self, episode_num: int, results: Dict):
        """Get human approval"""
        print("\n" + "=" * 70)
        print("⭐ HUMAN REVIEW REQUIRED")
        print("=" * 70)

        print("\nAnalysis complete. Options:")
        print("  [Enter] - Approve and save")
        print("  [F]     - View fixes")
        print("  [R]     - Regenerate analysis")
        print("  [V]     - View detailed report")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "f":
            self._show_fixes(results)
        elif choice == "r":
            print("Regeneration requested (manual follow-up needed)")
        elif choice == "v":
            self._show_detailed_report(results)
        else:
            print("✅ Analysis approved")

    def _show_fixes(self, results: Dict):
        """Show recommended fixes"""
        print("\n" + "━" * 70)
        print("🔧 RECOMMENDED FIXES")
        print("━" * 70)

        spec = results.get("speakability", {}).get("speakability_analysis", {})
        fixes_count = 0

        for twisters in spec.get("tongue_twisters", []):
            fixes_count += 1

        print(f"\nTotal fixes recommended: {fixes_count}")

    def _show_detailed_report(self, results: Dict):
        """Show detailed analysis report"""
        print("\n" + "━" * 70)
        print("📄 DETAILED ANALYSIS REPORT")
        print("━" * 70)
        print(json.dumps(results, indent=2)[:2000] + "...")

    async def _save_analysis_results(self, episode_num: int, results: Dict):
        """Save analysis results to files"""
        timestamp = datetime.now().isoformat()

        # Save JSON
        json_file = (
            self.output_dir
            / f"episode_{episode_num:02d}_dialogue_analysis.json"
        )
        with open(json_file, "w") as f:
            json.dump(
                {
                    "episode": episode_num,
                    "analysis_timestamp": timestamp,
                    "results": results,
                },
                f,
                indent=2,
            )

        # Save to Redis
        key = f"audiobook:{self.session_id}:station_31:episode_{episode_num:02d}"
        await self.redis_client.set(
            key,
            json.dumps(
                {
                    "episode": episode_num,
                    "timestamp": timestamp,
                    "dialogue_analysis": results,
                }
            ),
        )

        print(f"\n✅ Saved: {json_file.name}")

    def ask_continue(self) -> bool:
        """Ask to continue analysis"""
        choice = input("\n\nAnalyze another episode? (y/n): ").strip().lower()
        return choice == "y"

    def display_final_summary(self):
        """Display final session summary"""
        print("\n" + "=" * 70)
        print("✅ STATION 31 COMPLETE")
        print("=" * 70)
        print("\nDialogue Naturalness Pass Summary:")
        print(f"  Episodes analyzed: {len(self.episode_scripts)}")
        print(f"  Output directory: {self.output_dir}")
        print("\nNext: Station 32 - Audio-Only Clarity Audit")
        print("=" * 70 + "\n")


async def main():
    """Main entry point"""
    import sys

    session_id = sys.argv[1] if len(sys.argv) > 1 else "session_test"

    station = Station31DialogueNaturalnessPass(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
