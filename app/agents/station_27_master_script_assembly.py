"""
Station 27: Master Script Assembly

This station performs final assembly of all finalized scripts into production-ready
master scripts with complete specifications, format conversions, and delivery packages.

Flow:
1. Load Station 26 finalized scripts
2. Display episode selection and assembly status
3. Human selects episode to assemble
4. Execute 3 sequential LLM assembly tasks:
   - Script assembly (complete script with specifications)
   - Format conversion (Fountain, Markdown)
   - Production package generation (cast briefing, voice specs, sound specs, editor specs)
5. Display assembly results
6. Display production package
7. Save final master scripts + production package
8. Save to Redis for delivery/external use
9. Loop option for next episode

Creates production-ready master scripts and complete production packages for all
teams involved in audio recording, editing, and delivery.
"""

import asyncio
import json
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json


class Station27MasterScriptAssembly:
    """Station 27: Master Script Assembly"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=27)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output', {}).get('directory', 'output/station_27'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store loaded data
        self.locked_episodes = {}  # From Station 26
        self.assembled_episodes = set()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_27.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method with episode loop"""
        print("=" * 70)
        print("🎬 STATION 27: MASTER SCRIPT ASSEMBLY")
        print("=" * 70)
        print()

        try:
            # Step 1: Load scripts from Station 26
            print("📥 Loading finalized scripts from Station 26...")
            await self.load_scripts()
            print(f"✅ Loaded {len(self.locked_episodes)} finalized episode script(s)")
            print()

            if not self.locked_episodes:
                print("❌ No scripts found. Please run Station 26 first.")
                return

            # Main assembly loop
            while True:
                # Step 2: Display episode selection
                self.display_episode_selection()

                # Step 3: Human selects episode
                episode_number = self.get_episode_selection()

                if episode_number is None:
                    break

                # Step 4-8: Assemble the selected episode
                await self.assemble_episode(episode_number)

                # Step 9: Ask to continue
                if not self.ask_continue_assembly():
                    break

            # Display final summary
            self.display_session_summary()

        except Exception as e:
            print(f"❌ Station 27 failed: {str(e)}")
            logging.error(f"Station 27 error: {str(e)}", exc_info=True)
            raise

    async def load_scripts(self):
        """Load scripts from Station 26"""
        try:
            for episode_num in range(1, 25):
                try:
                    key = f"audiobook:{self.session_id}:station_26:episode_{episode_num:02d}"
                    data_raw = await self.redis_client.get(key)

                    if data_raw:
                        episode_data = json.loads(data_raw)
                        self.locked_episodes[episode_num] = {
                            'source': 'station_26',
                            'data': episode_data,
                            'episode_number': episode_num
                        }
                        print(f"   ✓ Episode {episode_num} (from Station 26 - locked and finalized)")

                except Exception:
                    continue

        except Exception as e:
            raise ValueError(f"❌ Error loading scripts: {str(e)}")

    def display_episode_selection(self):
        """Display episode selection with assembly status"""
        print("=" * 70)
        print("📺 EPISODE SELECTION & ASSEMBLY STATUS")
        print("=" * 70)
        print()

        print(f"Scripts Available: {len(self.locked_episodes)}")
        print()
        print("EPISODE ASSEMBLY STATUS:")
        print("━" * 70)
        print(f"{'Ep':<4} {'Status':<20} {'Production Ready':<25}")
        print("─" * 70)

        for ep_num in sorted(self.locked_episodes.keys()):
            status = "✅ ASSEMBLED" if ep_num in self.assembled_episodes else "🟡 PENDING"
            ready = "✓ Yes" if ep_num in self.assembled_episodes else "⏳ Awaiting"
            print(f"{ep_num:<4} {status:<20} {ready:<25}")

        print("─" * 70)
        print(f"Episodes Assembled: {len(self.assembled_episodes)}/{len(self.locked_episodes)}")
        print()

    def get_episode_selection(self) -> Optional[int]:
        """Get episode selection from user"""
        print("=" * 70)
        print("⭐ EPISODE SELECTION REQUIRED")
        print("=" * 70)
        print()

        available = sorted(self.locked_episodes.keys())
        print(f"Which episode would you like to assemble and package?")
        print()
        print(f"🎯 Available episodes: {', '.join(map(str, available))}")
        print()

        while True:
            choice = input("Enter episode number or 'Q' to quit: ").strip().upper()

            if choice == 'Q':
                return None

            try:
                ep_num = int(choice)
                if ep_num in self.locked_episodes:
                    return ep_num
                else:
                    print(f"❌ Episode {ep_num} not available. Please choose from: {', '.join(map(str, available))}")
            except ValueError:
                print("❌ Please enter a valid episode number or 'Q' to quit")

    async def assemble_episode(self, episode_number: int):
        """Assemble complete master script for episode"""
        print()
        print("=" * 70)
        print(f"📋 EPISODE {episode_number} STATUS - ASSEMBLY")
        print("=" * 70)
        print()

        # Get locked script data
        locked_data = self.locked_episodes[episode_number]['data']
        locked_script = locked_data.get('finalized_script', {})
        final_script_text = locked_script.get('script_with_performance_notes', '')

        print("=" * 70)
        print("🔍 EXECUTING ASSEMBLY TASKS")
        print("=" * 70)
        print()

        # Task 1: Script Assembly
        print("📝 Task 1/3: Master Script Assembly...")
        assembly = await self.execute_script_assembly(
            episode_number,
            final_script_text
        )
        print("✅ Master script assembled")
        print()

        # Task 2: Format Conversion
        print("📄 Task 2/3: Format Conversion...")
        conversion = await self.execute_format_conversion(
            episode_number,
            assembly.get('master_script_text', final_script_text)
        )
        print("✅ Formats converted (Fountain, Markdown)")
        print()

        # Task 3: Production Package Generation
        print("📦 Task 3/3: Production Package Generation...")
        production = await self.execute_production_package_generation(
            episode_number,
            assembly.get('master_script_text', final_script_text)
        )
        print("✅ Production package generated")
        print()

        # Display results
        self.display_assembly_results(episode_number, assembly)
        self.display_production_package_summary(production)

        # Save outputs
        print()
        print("=" * 70)
        print(f"💾 SAVING MASTER SCRIPTS - EPISODE {episode_number}")
        print("=" * 70)
        print()

        await self.save_episode_outputs(
            episode_number,
            locked_data,
            assembly,
            conversion,
            production
        )

        self.assembled_episodes.add(episode_number)

        print()
        print("=" * 70)
        print(f"✅ Episode {episode_number} assembly complete")
        print("=" * 70)
        print()

    async def execute_script_assembly(self, episode_number: int, locked_script: str) -> Dict:
        """Task 1: Assemble complete master script"""
        try:
            prompt = self.config.get_prompt('script_assembly')

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                locked_script=locked_script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=16384
            )

            # Extract JSON
            assembly_data = extract_json(response)

            return assembly_data.get('master_script_assembly', {})

        except Exception as e:
            print(f"❌ Script assembly failed: {str(e)}")
            raise

    async def execute_format_conversion(self, episode_number: int, master_script: str) -> Dict:
        """Task 2: Convert to Fountain and Markdown formats"""
        try:
            prompt = self.config.get_prompt('format_conversion')

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                master_script=master_script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=16384
            )

            # Extract JSON
            conversion_data = extract_json(response)

            return conversion_data.get('format_conversion', {})

        except Exception as e:
            print(f"❌ Format conversion failed: {str(e)}")
            raise

    async def execute_production_package_generation(self, episode_number: int, master_script: str) -> Dict:
        """Task 3: Generate production package with all specifications"""
        try:
            prompt = self.config.get_prompt('production_package_generation')

            # Format prompt
            formatted_prompt = prompt.format(
                episode_number=episode_number,
                master_script=master_script[:15000]
            )

            # Execute LLM call
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=16384
            )

            # Extract JSON
            production_data = extract_json(response)

            return production_data.get('production_package', {})

        except Exception as e:
            print(f"❌ Production package generation failed: {str(e)}")
            raise

    def display_assembly_results(self, episode_number: int, assembly: Dict):
        """Display master script assembly results"""
        print("=" * 70)
        print(f"✅ EPISODE {episode_number}: MASTER SCRIPT ASSEMBLY COMPLETE")
        print("=" * 70)
        print()

        status = assembly.get('assembly_status', 'unknown')
        print(f"Status: {status.upper()}")
        print()

        specs = assembly.get('production_specifications', {})
        print("PRODUCTION SPECIFICATIONS:")
        print("━" * 70)
        print(f"  • Total Runtime: {specs.get('total_runtime', 'Unknown')}")
        print(f"  • Word Count: {specs.get('estimated_word_count', 'Unknown')}")
        print(f"  • Sound Cues: {specs.get('sound_cue_count', 'Unknown')}")
        print(f"  • Strategic Silences: {specs.get('silence_count', 'Unknown')}")
        print(f"  • Ambient Layers: {specs.get('ambient_layers', 'Unknown')}")
        print()

        metrics = assembly.get('quality_metrics', {})
        print("QUALITY METRICS:")
        print("━" * 70)
        for metric, value in metrics.items():
            print(f"  • {metric.replace('_', ' ').title()}: {value}")
        print()

    def display_production_package_summary(self, production: Dict):
        """Display production package summary"""
        print("=" * 70)
        print("📦 PRODUCTION PACKAGE GENERATED")
        print("=" * 70)
        print()

        summary = production.get('production_summary', {})
        print(f"Title: {summary.get('title', 'Unknown')}")
        print(f"Estimated Runtime: {summary.get('estimated_runtime', 'Unknown')}")
        print(f"Tone: {summary.get('tone', 'Unknown')}")
        print()

        print("PACKAGE INCLUDES:")
        print("  ✓ Cast & Crew Briefing")
        print("  ✓ Voice Actor Specifications")
        print("  ✓ Sound Design Specifications")
        print("  ✓ Editor Specifications")
        print("  ✓ Delivery Specifications")
        print()

    async def save_episode_outputs(self, episode_number: int, locked_data: Dict,
                                   assembly: Dict, conversion: Dict, production: Dict):
        """Save all outputs for the episode"""
        episode_dir = self.output_dir / f"episode_{episode_number:02d}"
        episode_dir.mkdir(parents=True, exist_ok=True)

        # 1. Save Master JSON
        json_filename = f"episode_{episode_number:02d}_MASTER.json"
        json_path = episode_dir / json_filename

        full_data = {
            'session_id': self.session_id,
            'episode_number': episode_number,
            'assembled_at': datetime.now().isoformat(),
            'master_script_assembly': assembly,
            'format_conversion': conversion,
            'production_package': production
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved Master JSON: {json_path.name}")

        # 2. Save Plain Text Master Script
        txt_filename = f"episode_{episode_number:02d}_MASTER.txt"
        txt_path = episode_dir / txt_filename

        master_text = assembly.get('master_script_text', '')
        if isinstance(master_text, list):
            master_text = '\n'.join(str(item) for item in master_text)

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(master_text)
        print(f"✅ Saved Master Script: {txt_path.name}")

        # 3. Save Fountain Format
        fountain_filename = f"episode_{episode_number:02d}_MASTER.fountain"
        fountain_path = episode_dir / fountain_filename

        fountain_text = conversion.get('fountain_script', '')
        if isinstance(fountain_text, list):
            fountain_text = '\n'.join(str(item) for item in fountain_text)

        with open(fountain_path, 'w', encoding='utf-8') as f:
            f.write(fountain_text)
        print(f"✅ Saved Fountain Format: {fountain_path.name}")

        # 4. Save Markdown Format
        markdown_filename = f"episode_{episode_number:02d}_MASTER.md"
        markdown_path = episode_dir / markdown_filename

        markdown_text = conversion.get('markdown_script', '')
        if isinstance(markdown_text, list):
            markdown_text = '\n'.join(str(item) for item in markdown_text)

        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        print(f"✅ Saved Markdown Format: {markdown_path.name}")

        # 5. Save Production Package JSON
        package_filename = f"episode_{episode_number:02d}_production_package.json"
        package_path = episode_dir / package_filename

        with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(production, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved Production Package: {package_path.name}")

        # 6. Save Delivery Manifest
        manifest_filename = f"episode_{episode_number:02d}_manifest.txt"
        manifest_path = episode_dir / manifest_filename

        manifest_content = self.generate_delivery_manifest(episode_number, assembly, production)
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(manifest_content)
        print(f"✅ Saved Delivery Manifest: {manifest_path.name}")

        # 7. Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_27:episode_{episode_number:02d}"
        await self.redis_client.set(redis_key, json.dumps(full_data), expire=604800)

        print()
        print(f"📁 Files saved to: {episode_dir}")
        print()

    def generate_delivery_manifest(self, episode_number: int, assembly: Dict, production: Dict) -> str:
        """Generate delivery manifest"""
        lines = []
        lines.append("=" * 70)
        lines.append(f"EPISODE {episode_number} - MASTER SCRIPT DELIVERY MANIFEST")
        lines.append("=" * 70)
        lines.append("")

        summary = production.get('production_summary', {})
        lines.append("EPISODE INFORMATION:")
        lines.append("=" * 70)
        lines.append(f"Title: {summary.get('title', 'Unknown')}")
        lines.append(f"Runtime Target: {summary.get('estimated_runtime', 'Unknown')}")
        lines.append(f"Tone: {summary.get('tone', 'Unknown')}")
        lines.append(f"Themes: {', '.join(summary.get('key_themes', []))}")
        lines.append("")

        specs = assembly.get('production_specifications', {})
        lines.append("TECHNICAL SPECIFICATIONS:")
        lines.append("=" * 70)
        lines.append(f"Final Word Count: {specs.get('estimated_word_count', 'Unknown')}")
        lines.append(f"Final Runtime: {specs.get('total_runtime', 'Unknown')}")
        lines.append(f"Total Scenes: {specs.get('scene_count', 'Unknown')}")
        lines.append(f"Sound Cues: {specs.get('sound_cue_count', 'Unknown')}")
        lines.append(f"Strategic Silences: {specs.get('silence_count', 'Unknown')}")
        lines.append(f"Ambient Layers: {specs.get('ambient_layers', 'Unknown')}")
        lines.append("")

        lines.append("DELIVERY FILES:")
        lines.append("=" * 70)
        lines.append(f"✓ episode_{episode_number:02d}_MASTER.json (Complete structured script)")
        lines.append(f"✓ episode_{episode_number:02d}_MASTER.txt (Production-ready text)")
        lines.append(f"✓ episode_{episode_number:02d}_MASTER.fountain (Fountain format)")
        lines.append(f"✓ episode_{episode_number:02d}_MASTER.md (Markdown format)")
        lines.append(f"✓ episode_{episode_number:02d}_production_package.json (Complete production specs)")
        lines.append("")

        lines.append("PRODUCTION TEAMS:")
        lines.append("=" * 70)
        lines.append("✓ Voice actors (use cast briefing and actor specs)")
        lines.append("✓ Sound designers (use sound design specifications)")
        lines.append("✓ Editor (use editor specifications)")
        lines.append("✓ QA/Review team (use quality metrics)")
        lines.append("")

        lines.append("STATUS:")
        lines.append("=" * 70)
        lines.append("✅ READY FOR PRODUCTION")
        lines.append("")

        return "\n".join(lines)

    def display_session_summary(self):
        """Display session summary"""
        print()
        print("=" * 70)
        print("📊 SESSION SUMMARY")
        print("=" * 70)
        print()

        print(f"Total Episodes Available: {len(self.locked_episodes)}")
        print(f"Episodes Assembled: {len(self.assembled_episodes)}")
        print()

        if len(self.assembled_episodes) == len(self.locked_episodes):
            print("✅ All episodes assembled and packaged for production!")
        else:
            remaining = len(self.locked_episodes) - len(self.assembled_episodes)
            print(f"⏳ {remaining} episode(s) remaining for assembly")

        print()

    def ask_continue_assembly(self) -> bool:
        """Ask if user wants to continue assembly"""
        print()
        print("=" * 70)
        print("⭐ CONTINUE MASTER SCRIPT ASSEMBLY?")
        print("=" * 70)
        print()

        print(f"Episodes assembled: {len(self.assembled_episodes)}/{len(self.locked_episodes)}")
        print()
        print("OPTIONS:")
        print("  [Y] - Assemble another episode")
        print("  [N] - Finish for now")
        print()

        choice = input("Your choice (Y/N): ").strip().upper()

        return choice == 'Y'


async def main():
    """Main execution"""
    session_id = input("📋 Enter session ID: ").strip()

    station = Station27MasterScriptAssembly(session_id, skip_review=True)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
