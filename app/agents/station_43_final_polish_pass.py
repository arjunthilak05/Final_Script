"""
Station 43: Final Polish Pass

This station performs the final polish pass on completed episode scripts,
ensuring production readiness through read-aloud review, precision editing,
audio annotation, and comprehensive sign-off checklist verification.

Flow:
1. Load Station 27 master scripts (all episodes)
2. Load supporting data (Station 2, 6, 7, 8 for context)
3. Execute 4-task polish sequence:
   - Task 1: Read-Aloud Review (final performance check)
   - Task 2: Precision Editing (final tightening)
   - Task 3: Audio Annotation (final production notes)
   - Task 4: Sign-Off Checklist (final verification)
4. Generate polished scripts with annotations
5. Provide production-ready certifications
6. Save comprehensive polish reports

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config
- FAIL FAST - Exit on missing dependencies with actionable messages
- Final quality assurance pass before production
- Maintain character voices and world consistency
- Explicit error messages with file names, line numbers
- Consistent logging to logs/station_43.log
"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

# Set up logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "station_43.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Station43FinalPolishPass:
    """Station 43: Final Polish Pass"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=43)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path(self.config_data.get('output_path', 'output/station_43'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate required config fields
        self._validate_config()
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_43.yml'

        if not config_path.exists():
            raise FileNotFoundError(f"❌ Station 43 config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)
    
    def _validate_config(self):
        """Validate configuration has required fields"""
        required_fields = ['input_path', 'output_path']
        for field in required_fields:
            if not self.config_data.get(field):
                raise ValueError(f"❌ Required config field missing: {field}")
        
        logger.info("✅ Configuration validated")
    
    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 43 initialized")
    
    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("✨ STATION 43: FINAL POLISH PASS")
        print("=" * 70)
        print()
        
        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            supporting_data = await self.load_supporting_data()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 27: {len(station27_data.get('episodes', {}))} episodes")
            print(f"   ✓ Supporting data loaded from stations 2, 6, 7, 8")
            print()
            
            # Step 2: Display project summary
            episodes = station27_data.get('episodes', {})
            self.display_project_summary(episodes, supporting_data)
            
            # Step 3: Process all episodes for final polish
            print("\n✨ Beginning final polish pass...")
            print("-" * 70)
            
            # Execute 4-task polish sequence
            all_polish_results = {}
            
            for episode_num, episode_data in sorted(episodes.items()):
                print(f"\n📝 Processing Episode {episode_num}...")
                
                print("   🎤 Task 1/4: Read-Aloud Review...")
                read_aloud = await self.execute_task1_read_aloud_review(
                    episode_num, episode_data, supporting_data
                )
                print("   ✅ Read-aloud review complete")
                
                print("   ✏️  Task 2/4: Precision Editing...")
                precision_editing = await self.execute_task2_precision_editing(
                    episode_num, episode_data, supporting_data, read_aloud
                )
                print("   ✅ Precision editing complete")
                
                print("   🎧 Task 3/4: Audio Annotation...")
                audio_annotation = await self.execute_task3_audio_annotation(
                    episode_num, episode_data, supporting_data, precision_editing
                )
                print("   ✅ Audio annotation complete")
                
                print("   ✅ Task 4/4: Sign-Off Checklist...")
                sign_off = await self.execute_task4_sign_off_checklist(
                    episode_num, episode_data, supporting_data, audio_annotation
                )
                print("   ✅ Sign-off checklist complete")
                
                all_polish_results[episode_num] = {
                    'read_aloud_review': read_aloud,
                    'precision_editing': precision_editing,
                    'audio_annotation': audio_annotation,
                    'sign_off_checklist': sign_off
                }
            
            # Step 4: Generate polished scripts and reports
            print("\n📦 Generating polished scripts and reports...")
            print("-" * 70)
            
            await self.generate_polish_reports(all_polish_results, episodes, supporting_data)
            
            print("\n" + "=" * 70)
            print("✅ FINAL POLISH PASS COMPLETE")
            print("=" * 70)
            print(f"\n📁 Output directory: {self.output_dir}")
            print(f"📄 Reports generated for {len(episodes)} episodes")
            
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            raise
        except Exception as e:
            logger.error(f"Station 43 failed: {str(e)}")
            print(f"\n❌ Error: {str(e)}")
            raise
    
    async def load_station27_data(self) -> Dict:
        """Load all episodes from Station 27 master scripts"""
        try:
            station_27_path = Path(self.config_data.get('input_path', 'output/station_27'))
            
            if not station_27_path.exists():
                raise ValueError(
                    f"❌ Station 27 directory not found: {station_27_path}\n"
                    "   Please run Station 27 (Master Script Assembly) first"
                )
            
            episodes = {}
            
            # Load all episodes from directory
            for episode_dir in station_27_path.iterdir():
                if episode_dir.is_dir() and episode_dir.name.startswith("episode_"):
                    try:
                        episode_num = int(episode_dir.name.split("_")[1])
                        json_file = episode_dir / f"episode_{episode_num:02d}_MASTER.json"
                        
                        if json_file.exists():
                            with open(json_file, 'r', encoding='utf-8') as f:
                                episode_data = json.load(f)
                                episodes[episode_num] = episode_data
                    except (ValueError, KeyError, json.JSONDecodeError) as e:
                        logger.warning(f"Skipping episode: {str(e)}")
                        continue
            
            if not episodes:
                raise ValueError(
                    f"❌ No episodes found in {station_27_path}\n"
                    "   Please run Station 27 (Master Script Assembly) first"
                )
            
            # Sort episodes by number
            episodes = dict(sorted(episodes.items()))
            
            logger.info(f"Loaded {len(episodes)} episodes from {station_27_path}")
            return {'episodes': episodes}
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing episode data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading station data: {str(e)}")
    
    async def load_supporting_data(self) -> Dict:
        """Load supporting data from earlier stations"""
        supporting_data = {}
        
        # Try to load from file system first (more reliable)
        try:
            # Station 2: Project DNA
            station_02_dir = Path("output/station_02")
            station2_files = list(station_02_dir.glob("*.json"))
            if station2_files:
                latest_file = max(station2_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_2'] = json.load(f)
            
            # Station 6: Master Style Guide
            station_06_dir = Path("output/station_06")
            station6_files = list(station_06_dir.glob("*.json"))
            if station6_files:
                latest_file = max(station6_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_6'] = json.load(f)
            
            # Station 7: Character Architect
            station_07_dir = Path("output/station_07")
            station7_files = list(station_07_dir.glob("*.json"))
            if station7_files:
                latest_file = max(station7_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_7'] = json.load(f)
            
            # Station 8: World Builder
            station_08_dir = Path("output/station_08")
            station8_files = list(station_08_dir.glob("*.json"))
            if station8_files:
                latest_file = max(station8_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_8'] = json.load(f)
            
            logger.info(f"Loaded supporting data from {len(supporting_data)} stations")
            
        except Exception as e:
            logger.warning(f"Could not load some supporting data from files: {str(e)}")
        
        return supporting_data
    
    def display_project_summary(self, episodes: Dict, supporting_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        print(f"Total Episodes: {len(episodes)}")
        print(f"Supporting Data Available:")
        print(f"   • Station 2 (Project DNA): {'✓' if 'station_2' in supporting_data else '✗'}")
        print(f"   • Station 6 (Style Guide): {'✓' if 'station_6' in supporting_data else '✗'}")
        print(f"   • Station 7 (Characters): {'✓' if 'station_7' in supporting_data else '✗'}")
        print(f"   • Station 8 (World): {'✓' if 'station_8' in supporting_data else '✗'}")
        print()
        
        if episodes:
            print("Episode List:")
            for episode_key, episode_data in sorted(episodes.items()):
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)
    
    async def execute_task1_read_aloud_review(self, episode_num: int, episode_data: Dict,
                                              supporting_data: Dict) -> Dict:
        """Task 1: Read-Aloud Review - Final performance check"""
        try:
            episode_content = self._extract_episode_content(episode_data)
            
            context = {
                'session_id': self.session_id,
                'episode_number': episode_num,
                'episode_content': episode_content,
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}',
                'style_guide': json.dumps(supporting_data.get('station_6', {}), indent=2) if 'station_6' in supporting_data else '{}',
                'character_bible': json.dumps(supporting_data.get('station_7', {}), indent=2) if 'station_7' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('read_aloud_review').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('read_aloud_review', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed for episode {episode_num}: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")
    
    async def execute_task2_precision_editing(self, episode_num: int, episode_data: Dict,
                                             supporting_data: Dict, read_aloud: Dict) -> Dict:
        """Task 2: Precision Editing - Final tightening"""
        try:
            episode_content = self._extract_episode_content(episode_data)
            
            context = {
                'session_id': self.session_id,
                'episode_number': episode_num,
                'episode_content': episode_content,
                'read_aloud_issues': json.dumps(read_aloud.get('issues_found', []), indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}',
                'style_guide': json.dumps(supporting_data.get('station_6', {}), indent=2) if 'station_6' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('precision_editing').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('precision_editing', {})
            
        except Exception as e:
            logger.error(f"Task 2 failed for episode {episode_num}: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")
    
    async def execute_task3_audio_annotation(self, episode_num: int, episode_data: Dict,
                                            supporting_data: Dict, precision_editing: Dict) -> Dict:
        """Task 3: Audio Annotation - Final production notes"""
        try:
            episode_content = self._extract_episode_content(episode_data)
            polished_content = precision_editing.get('polished_script_text', episode_content)
            
            context = {
                'session_id': self.session_id,
                'episode_number': episode_num,
                'polished_script': polished_content,
                'editing_changes': json.dumps(precision_editing.get('changes_made', []), indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}',
                'world_bible': json.dumps(supporting_data.get('station_8', {}), indent=2) if 'station_8' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('audio_annotation').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('audio_annotation', {})
            
        except Exception as e:
            logger.error(f"Task 3 failed for episode {episode_num}: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")
    
    async def execute_task4_sign_off_checklist(self, episode_num: int, episode_data: Dict,
                                               supporting_data: Dict, audio_annotation: Dict) -> Dict:
        """Task 4: Sign-Off Checklist - Final verification"""
        try:
            episode_content = self._extract_episode_content(episode_data)
            annotated_content = audio_annotation.get('annotated_script_text', episode_content)
            
            context = {
                'session_id': self.session_id,
                'episode_number': episode_num,
                'final_script': annotated_content,
                'audio_notes': json.dumps(audio_annotation.get('production_notes', []), indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}',
                'character_bible': json.dumps(supporting_data.get('station_7', {}), indent=2) if 'station_7' in supporting_data else '{}',
                'world_bible': json.dumps(supporting_data.get('station_8', {}), indent=2) if 'station_8' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('sign_off_checklist').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('sign_off_checklist', {})
            
        except Exception as e:
            logger.error(f"Task 4 failed for episode {episode_num}: {str(e)}")
            raise ValueError(f"❌ Task 4 failed: {str(e)}")
    
    def _extract_episode_content(self, episode: Dict) -> str:
        """Extract content from episode data"""
        # Try format_conversion.fountain_script first
        format_conv = episode.get('format_conversion', {})
        fountain_script = format_conv.get('fountain_script', '')
        if fountain_script and fountain_script.strip() != '':
            return fountain_script
        
        # Try markdown script
        markdown_script = format_conv.get('markdown_script', '')
        if markdown_script and markdown_script.strip() != '':
            return markdown_script
        
        # Try master_script_text
        master_text = episode.get('master_script_assembly', {}).get('master_script_text', '')
        if master_text and master_text.strip() not in ['Complete full episode script with all audio markup and formatting...', '']:
            return master_text
        
        return ''
    
    async def generate_polish_reports(self, all_polish_results: Dict, episodes: Dict,
                                     supporting_data: Dict):
        """Generate comprehensive polish reports"""
        
        # Generate episode-specific reports
        for episode_num, polish_results in all_polish_results.items():
            episode_data = episodes[episode_num]
            
            # Create episode directory
            episode_dir = self.output_dir / f"episode_{episode_num:02d}"
            episode_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. Polished Script JSON
            polished_episode = {
                'generated_at': datetime.now().isoformat(),
                'session_id': self.session_id,
                'episode_number': episode_num,
                'polish_results': polish_results,
                'production_ready': polish_results['sign_off_checklist'].get('all_checks_passed', False),
                'original_script': episode_data
            }
            
            json_path = episode_dir / f"episode_{episode_num:02d}_POLISHED.json"
            encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
            with open(json_path, 'w', encoding=encoding) as f:
                json.dump(polished_episode, f, indent=2, ensure_ascii=False)
            
            # 2. Polished Script Text
            polished_text = polish_results['precision_editing'].get('polished_script_text', '')
            if not polished_text:
                polished_text = self._extract_episode_content(episode_data)
            
            txt_path = episode_dir / f"episode_{episode_num:02d}_POLISHED.txt"
            with open(txt_path, 'w', encoding=encoding) as f:
                f.write(polished_text)
            
            # 3. Production Notes
            production_notes = polish_results['audio_annotation'].get('production_notes', [])
            notes_path = episode_dir / f"episode_{episode_num:02d}_production_notes.json"
            with open(notes_path, 'w', encoding=encoding) as f:
                json.dump({
                    'episode_number': episode_num,
                    'production_notes': production_notes,
                    'critical_sounds': polish_results['audio_annotation'].get('critical_sounds', []),
                    'performance_notes': polish_results['audio_annotation'].get('performance_notes', []),
                    'technical_notes': polish_results['audio_annotation'].get('technical_notes', [])
                }, f, indent=2, ensure_ascii=False)
        
        # Generate summary report
        self._generate_summary_report(all_polish_results, episodes, supporting_data)
        
        # Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_43"
        await self.redis.set(redis_key, json.dumps({
            'episodes_polished': len(all_polish_results),
            'production_ready': all(
                r['sign_off_checklist'].get('all_checks_passed', False)
                for r in all_polish_results.values()
            )
        }), expire=86400)
        
        print(f"✅ All polish reports generated")
    
    def _generate_summary_report(self, all_polish_results: Dict, episodes: Dict,
                                 supporting_data: Dict):
        """Generate human-readable summary report"""
        txt_path = self.output_dir / f"{self.session_id}_polish_summary.txt"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        
        with open(txt_path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 43: FINAL POLISH PASS SUMMARY REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            # Overall Statistics
            f.write("-" * 70 + "\n")
            f.write("POLISH STATISTICS\n")
            f.write("-" * 70 + "\n\n")
            
            total_episodes = len(all_polish_results)
            production_ready = sum(
                1 for r in all_polish_results.values()
                if r['sign_off_checklist'].get('all_checks_passed', False)
            )
            
            f.write(f"Total Episodes: {total_episodes}\n")
            f.write(f"Production Ready: {production_ready}\n")
            f.write(f"Completion Rate: {(production_ready/total_episodes*100):.1f}%\n\n")
            
            # Per-Episode Summary
            f.write("-" * 70 + "\n")
            f.write("EPISODE POLISH SUMMARY\n")
            f.write("-" * 70 + "\n\n")
            
            for episode_num in sorted(all_polish_results.keys()):
                results = all_polish_results[episode_num]
                episode_data = episodes[episode_num]
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                
                f.write(f"Episode {episode_num}: {title}\n")
                f.write(f"  Read-Aloud Review: {results['read_aloud_review'].get('overall_score', 'N/A')}\n")
                f.write(f"  Precision Editing: {len(results['precision_editing'].get('changes_made', []))} changes\n")
                f.write(f"  Audio Annotation: {len(results['audio_annotation'].get('production_notes', []))} notes\n")
                f.write(f"  Sign-Off Status: {'✓ PASSED' if results['sign_off_checklist'].get('all_checks_passed', False) else '✗ ISSUES'}\n")
                
                # List any issues
                issues = results['sign_off_checklist'].get('failed_checks', [])
                if issues:
                    f.write(f"  Issues: {len(issues)}\n")
                    for issue in issues[:3]:
                        f.write(f"    - {issue}\n")
                
                f.write("\n")
            
            f.write("=" * 70 + "\n")
            f.write("END OF POLISH SUMMARY REPORT\n")
            f.write("=" * 70 + "\n")


# CLI Entry Point
async def main():
    """Run Station 43 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    polish_pass = Station43FinalPolishPass(session_id)
    await polish_pass.initialize()
    
    try:
        await polish_pass.run()
        print(f"\n✅ Success! Final polish pass complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

