"""
Station 37: Plant/Payoff Tracker

This station tracks all planted story elements across episodes and ensures they have proper payoffs,
identifying orphaned plants and payoffs, verifying earning/clarity/satisfaction, and mapping the
complete plant/payoff timeline.

Flow:
1. Load Station 27 master scripts
2. Load Station 10 narrative reveal strategy
3. Execute 4-task tracking sequence:
   - Task 1: Plant Inventory (major/minor/thematic/audio)
   - Task 2: Payoff Verification
   - Task 3: Orphan Identification
   - Task 4: Timeline Mapping
4. Generate comprehensive plant/payoff matrix
5. Save JSON + Markdown outputs
6. Flag any unfulfilled plants or unearned payoffs

Critical Implementation Rules:
- Track every plant from introduction to payoff
- Verify sufficient setup before payoff
- Identify orphaned plants without payoffs
- Flag unearned payoffs without plants
- Map complete timeline across all episodes
"""

import asyncio
import json
import logging
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Station37PlantPayoffTracker:
    """Station 37: Plant/Payoff Tracker"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=37)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path("output/station_37")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_37.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 37 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🌱 STATION 37: PLANT/PAYOFF TRACKER")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            station10_data = await self.load_station10_data()
            
            print("✅ All inputs loaded successfully")
            episodes = station27_data.get('episodes', {})
            print(f"   ✓ Station 27: {len(episodes)} master scripts")
            if station10_data:
                print(f"   ✓ Station 10: Narrative reveal strategy loaded")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data, station10_data)

            # Step 3: Process all episodes
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            print(f"📊 Processing {len(episodes)} episodes for plant/payoff tracking...")
            print()

            all_episode_tracks = []
            error_log = []

            # Task 1: Plant Inventory (process all episodes together for comprehensive view)
            print("\n" + "=" * 70)
            print("🌱 TASK 1: PLANT INVENTORY")
            print("=" * 70)
            print("Scanning all episodes for planted elements...")
            
            all_plants = await self.execute_task1_plant_inventory(station27_data, station10_data)
            print(f"✅ Found {len(all_plants.get('major_plants', []))} major plants")
            print(f"   Found {len(all_plants.get('minor_plants', []))} minor plants")
            print(f"   Found {len(all_plants.get('thematic_plants', []))} thematic plants")
            print(f"   Found {len(all_plants.get('audio_plants', []))} audio plants")

            # Task 2: Payoff Verification
            print("\n" + "=" * 70)
            print("✓ TASK 2: PAYOFF VERIFICATION")
            print("=" * 70)
            print("Verifying all payoffs...")
            
            payoff_verification = await self.execute_task2_payoff_verification(
                all_plants, station27_data
            )
            verified_count = payoff_verification.get('verified_payoffs', [])
            print(f"✅ Verified {len(verified_count)} payoffs")

            # Task 3: Orphan Identification
            print("\n" + "=" * 70)
            print("🔍 TASK 3: ORPHAN IDENTIFICATION")
            print("=" * 70)
            print("Identifying orphaned plants and payoffs...")
            
            orphans = await self.execute_task3_orphan_identification(
                all_plants, payoff_verification, station27_data
            )
            print(f"⚠️  Found {len(orphans.get('plants_without_payoffs', []))} plants without payoffs")
            print(f"⚠️  Found {len(orphans.get('payoffs_without_plants', []))} payoffs without plants")

            # Task 4: Timeline Mapping
            print("\n" + "=" * 70)
            print("📅 TASK 4: TIMELINE MAPPING")
            print("=" * 70)
            print("Creating complete plant/payoff timeline...")
            
            timeline = await self.execute_task4_timeline_mapping(
                all_plants, payoff_verification, episodes
            )
            print(f"✅ Timeline mapping complete")

            # Compile complete tracking data
            tracking_data = {
                'session_id': self.session_id,
                'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
                'plant_inventory': all_plants,
                'payoff_verification': payoff_verification,
                'orphans': orphans,
                'timeline': timeline,
                'overall_assessment': await self.generate_overall_assessment(
                    all_plants, payoff_verification, orphans
                )
            }

            # Step 4: Generate output files
            print("\n" + "=" * 70)
            print("💾 GENERATING OUTPUT FILES")
            print("=" * 70)
            
            await self.generate_output_files(tracking_data, station27_data)
            print(f"✅ All output files generated in: {self.output_dir}/")

            # Step 5: Display critical issues
            self.display_critical_issues(tracking_data)

            # Step 6: User validation prompt
            print("\n" + "=" * 70)
            print("🔍 USER VALIDATION REQUIRED")
            print("=" * 70)
            
            if orphans.get('plants_without_payoffs') or orphans.get('payoffs_without_plants'):
                print("⚠️  Action required: Orphaned plants/payoffs identified")
                print("   Review detailed report before proceeding to next station.")
            else:
                print("✅ All plants have payoffs! Ready for next station.")
            
            print(f"\n📁 Output files saved to: {self.output_dir}")
            print("✅ Station 37 complete!")

        except Exception as e:
            logger.error(f"Error in Station 37: {str(e)}", exc_info=True)
            raise

    async def load_station27_data(self) -> Dict[str, Any]:
        """Load Station 27 master scripts"""
        try:
            station_27_dir = Path("output/station_27")
            episodes = {}
            
            if not station_27_dir.exists():
                raise ValueError(f"Station 27 output directory not found")
            
            episode_dirs = sorted([d for d in station_27_dir.iterdir() 
                                  if d.is_dir() and d.name.startswith("episode_")])
            
            if not episode_dirs:
                raise ValueError(f"No episode data found in Station 27 output")
            
            for episode_dir in episode_dirs:
                episode_num = episode_dir.name.replace("episode_", "")
                master_file = episode_dir / f"{episode_dir.name}_MASTER.json"
                
                if master_file.exists():
                    with open(master_file, 'r', encoding='utf-8') as f:
                        episode_data = json.load(f)
                        
                        if episode_data.get('session_id') == self.session_id:
                            episodes[f"episode_{episode_num}"] = episode_data
            
            if not episodes:
                raise ValueError(f"""
❌ No Station 27 data found for session: '{self.session_id}'

REQUIRED: Station 37 depends on Station 27 (Master Script Assembly)

SOLUTIONS:
1. Run Station 27 first to generate script data
2. Check that session_id matches in the output files
""")
            
            return {
                'working_title': episodes.get('episode_01', {}).get('production_package', {}).get('title', 'Unknown'),
                'episodes': episodes
            }
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error loading Station 27 data: {str(e)}")
            raise

    async def load_station10_data(self) -> Optional[Dict[str, Any]]:
        """Load Station 10 narrative reveal strategy (optional)"""
        try:
            station_10_dir = Path("output/station_10")
            
            if not station_10_dir.exists():
                logger.warning("Station 10 data not found (optional)")
                return None
            
            # Look for relevant files
            reveal_strategy_files = list(station_10_dir.glob("*reveal_strategy*.json"))
            
            if reveal_strategy_files:
                with open(reveal_strategy_files[0], 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not load Station 10 data: {str(e)}")
            return None

    def display_project_summary(self, station27_data: Dict[str, Any], station10_data: Optional[Dict[str, Any]]):
        """Display project summary"""
        print("📊 PROJECT SUMMARY")
        print("-" * 60)
        
        working_title = station27_data.get('working_title', 'Unknown Project')
        episodes = station27_data.get('episodes', {})
        
        print(f"   Project: {working_title}")
        print(f"   Episodes: {len(episodes)}")
        if station10_data:
            print(f"   Reveal Strategy: Loaded")
        print()

    async def execute_task1_plant_inventory(self, station27_data: Dict[str, Any], 
                                             station10_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Task 1: Create complete plant inventory"""
        
        episodes = station27_data.get('episodes', {})
        
        # Collect all episode scripts
        episodes_content = {}
        for episode_id, episode_data in episodes.items():
            master_assembly = episode_data.get('master_script_assembly', {})
            script_content = master_assembly.get('master_script_text', '')
            
            if not script_content:
                script_content = episode_data.get('script', episode_data.get('master_script_text', ''))
            
            episodes_content[episode_id] = script_content
        
        # Build comprehensive prompt
        prompt = self.config_data['prompts']['plant_inventory'].format(
            episodes_content=json.dumps(episodes_content, indent=2),
            narrative_reveal_strategy=json.dumps(station10_data or {}, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('plant_inventory', {})

    async def execute_task2_payoff_verification(self, plant_inventory: Dict[str, Any],
                                                station27_data: Dict[str, Any]) -> Dict[str, Any]:
        """Task 2: Verify all payoffs"""
        
        episodes = station27_data.get('episodes', {})
        episodes_content = {}
        
        for episode_id, episode_data in episodes.items():
            master_assembly = episode_data.get('master_script_assembly', {})
            script_content = master_assembly.get('master_script_text', '')
            
            if not script_content:
                script_content = episode_data.get('script', episode_data.get('master_script_text', ''))
            
            episodes_content[episode_id] = script_content
        
        prompt = self.config_data['prompts']['payoff_verification'].format(
            plant_inventory=json.dumps(plant_inventory, indent=2),
            episodes_content=json.dumps(episodes_content, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('payoff_verification', {})

    async def execute_task3_orphan_identification(self, plant_inventory: Dict[str, Any],
                                                  payoff_verification: Dict[str, Any],
                                                  station27_data: Dict[str, Any]) -> Dict[str, Any]:
        """Task 3: Identify orphaned plants and payoffs"""
        
        prompt = self.config_data['prompts']['orphan_identification'].format(
            plant_inventory=json.dumps(plant_inventory, indent=2),
            payoff_verification=json.dumps(payoff_verification, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('orphan_identification', {})

    async def execute_task4_timeline_mapping(self, plant_inventory: Dict[str, Any],
                                             payoff_verification: Dict[str, Any],
                                             episodes: Dict[str, Any]) -> Dict[str, Any]:
        """Task 4: Map complete timeline"""
        
        episode_list = [ep_id for ep_id in episodes.keys()]
        
        prompt = self.config_data['prompts']['timeline_mapping'].format(
            plant_inventory=json.dumps(plant_inventory, indent=2),
            payoff_verification=json.dumps(payoff_verification, indent=2),
            episode_ids=json.dumps(episode_list, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('timeline_mapping', {})

    async def generate_overall_assessment(self, plant_inventory: Dict[str, Any],
                                          payoff_verification: Dict[str, Any],
                                          orphans: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall assessment"""
        
        prompt = self.config_data['prompts']['overall_assessment'].format(
            plant_inventory=json.dumps(plant_inventory, indent=2),
            payoff_verification=json.dumps(payoff_verification, indent=2),
            orphans=json.dumps(orphans, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('overall_assessment', {})

    async def generate_output_files(self, tracking_data: Dict[str, Any], 
                                   station27_data: Dict[str, Any]):
        """Generate all output files"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_basename = f"session_{self.session_id}_plant_payoff"
        
        # Save complete tracking JSON
        tracking_file = self.output_dir / f"{output_basename}_matrix.json"
        with open(tracking_file, 'w', encoding='utf-8') as f:
            json.dump(tracking_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ {tracking_file}")
        
        # Save timeline visualization
        timeline_data = tracking_data.get('timeline', {})
        timeline_file = self.output_dir / f"{output_basename}_timeline.json"
        with open(timeline_file, 'w', encoding='utf-8') as f:
            json.dump(timeline_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ {timeline_file}")
        
        # Save orphan report
        orphans = tracking_data.get('orphans', {})
        orphan_file = self.output_dir / f"{output_basename}_orphans.json"
        with open(orphan_file, 'w', encoding='utf-8') as f:
            json.dump(orphans, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ {orphan_file}")
        
        # Save markdown summary
        summary_file = self.output_dir / f"{output_basename}_summary.md"
        self.save_summary_markdown(summary_file, tracking_data)
        
        print(f"   ✓ {summary_file}")

    def save_summary_markdown(self, filepath: Path, tracking_data: Dict[str, Any]):
        """Save summary report as markdown"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Plant/Payoff Tracking Report\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall assessment
            overall = tracking_data.get('overall_assessment', {})
            if overall:
                f.write("## Overall Assessment\n\n")
                f.write(overall.get('summary_text', 'No summary available') + "\n\n")
                
                scores = overall.get('scores', {})
                if scores:
                    f.write("### Scores\n\n")
                    f.write(f"- Plant Density: {scores.get('plant_density_score', 'N/A')}/100\n")
                    f.write(f"- Payoff Rate: {scores.get('payoff_rate_score', 'N/A')}/100\n")
                    f.write(f"- Earned Payoffs: {scores.get('earned_payoffs_score', 'N/A')}/100\n")
                    f.write(f"- Timeline Balance: {scores.get('timeline_balance_score', 'N/A')}/100\n\n")
            
            # Critical issues
            orphans = tracking_data.get('orphans', {})
            plants_without = orphans.get('plants_without_payoffs', [])
            payoffs_without = orphans.get('payoffs_without_plants', [])
            
            if plants_without or payoffs_without:
                f.write("## Critical Issues\n\n")
                
                if plants_without:
                    f.write(f"### Plants Without Payoffs ({len(plants_without)})\n\n")
                    for plant in plants_without[:10]:  # Limit to 10
                        f.write(f"- **{plant.get('type', 'Unknown')}**: {plant.get('description', 'N/A')}\n")
                        f.write(f"  - Episode planted: {plant.get('episode_planted', 'N/A')}\n")
                        f.write(f"  - Severity: {plant.get('severity', 'N/A')}\n\n")
                
                if payoffs_without:
                    f.write(f"### Payoffs Without Plants ({len(payoffs_without)})\n\n")
                    for payoff in payoffs_without[:10]:  # Limit to 10
                        f.write(f"- **{payoff.get('type', 'Unknown')}**: {payoff.get('description', 'N/A')}\n")
                        f.write(f"  - Episode occurs: {payoff.get('episode', 'N/A')}\n")
                        f.write(f"  - Severity: {payoff.get('severity', 'N/A')}\n\n")
            
            f.write("---\n\n")
            f.write("*Generated by Station 37: Plant/Payoff Tracker*\n")

    def display_critical_issues(self, tracking_data: Dict[str, Any]):
        """Display critical issues"""
        orphans = tracking_data.get('orphans', {})
        plants_without = orphans.get('plants_without_payoffs', [])
        payoffs_without = orphans.get('payoffs_without_plants', [])
        
        if plants_without or payoffs_without:
            print("\n⚠️  CRITICAL ISSUES FOUND:")
            
            if plants_without:
                print(f"\n🌱 Plants Without Payoffs ({len(plants_without)}):")
                for i, plant in enumerate(plants_without[:5], 1):  # Show first 5
                    print(f"   {i}. {plant.get('description', 'N/A')[:60]}...")
                    print(f"      Episode: {plant.get('episode_planted', 'N/A')}")
                    print(f"      Severity: {plant.get('severity', 'N/A')}")
            
            if payoffs_without:
                print(f"\n✓ Payoffs Without Plants ({len(payoffs_without)}):")
                for i, payoff in enumerate(payoffs_without[:5], 1):  # Show first 5
                    print(f"   {i}. {payoff.get('description', 'N/A')[:60]}...")
                    print(f"      Episode: {payoff.get('episode', 'N/A')}")
                    print(f"      Severity: {payoff.get('severity', 'N/A')}")
        else:
            print("\n✅ All plants have payoffs!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
    else:
        print("\n" + "="*70)
        print("🌱 STATION 37: PLANT/PAYOFF TRACKER")
        print("="*70)
        print()
        print("Please enter the session ID to process:")
        print("(Default: session_20251023_112749)")
        session_input = input("Session ID: ").strip()
        session_id = session_input if session_input else "session_20251023_112749"
        print()
    
    async def main():
        station = Station37PlantPayoffTracker(session_id=session_id)
        await station.initialize()
        await station.run()
    
    asyncio.run(main())

