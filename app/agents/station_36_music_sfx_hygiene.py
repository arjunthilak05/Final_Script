"""
Station 36: Music & Sound Effects Hygiene

This station audits all music and sound effects cues across episode scripts, ensuring they
are necessary, properly timed, appropriately mixed, and not redundant.

Flow:
1. Load Station 27 master scripts
2. Extract all sound cues (SFX, MUSIC, AMBIENCE, SILENCE)
3. Execute 4-task audit sequence:
   - Task 1: Sound Effects Audit
   - Task 2: Music Audit
   - Task 3: Ambience Audit
   - Task 4: Silence Audit
4. Generate comprehensive hygiene reports with cut lists and recommendations
5. Save JSON + Markdown outputs
6. Require user approval before applying fixes

Critical Implementation Rules:
- Ensure each sound cue serves a purpose (not decorative)
- Verify timing synchronization with action
- Check volume and mixing appropriateness
- Validate consistency with world/genre
- Limit ambience to max 4 layers
- Audit silence for proper dramatic and natural use
"""
import asyncio
import json
import logging
import re
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


class Station36MusicSfxHygiene:
    """Station 36: Music & Sound Effects Hygiene"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=36)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path("output/station_36")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_36.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 36 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🎵 STATION 36: MUSIC & SOUND EFFECTS HYGIENE")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            
            print("✅ All inputs loaded successfully")
            episodes = station27_data.get('episodes', {})
            print(f"   ✓ Station 27: {len(episodes)} master scripts")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data)

            # Step 3: Process all episodes
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            print(f"🎬 Processing {len(episodes)} episodes for sound hygiene audit...")
            print()

            all_episode_audits = []
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for episode_id, episode_data in episodes.items():
                print(f"\n🎬 Processing Episode: {episode_id}")
                print("-" * 60)

                # Extract sound cues from script
                # Station 27 has script in master_script_assembly.master_script_text
                master_assembly = episode_data.get('master_script_assembly', {})
                script_content = master_assembly.get('master_script_text', '')
                
                if not script_content:
                    # Try alternative location
                    script_content = episode_data.get('script', episode_data.get('master_script_text', ''))
                
                sound_cues = self.extract_sound_cues(script_content)
                
                print(f"   Found {len(sound_cues)} sound cues")
                print(f"   - SFX: {sum(1 for cue in sound_cues if cue['type'] == 'SFX')}")
                print(f"   - MUSIC: {sum(1 for cue in sound_cues if cue['type'] == 'MUSIC')}")
                print(f"   - AMBIENCE: {sum(1 for cue in sound_cues if cue['type'] == 'AMBIENCE')}")
                print(f"   - SILENCE: {sum(1 for cue in sound_cues if cue['type'] == 'SILENCE')}")
                
                # Run 4-task audit sequence
                episode_audit = await self.run_audit_sequence(
                    episode_id, episode_data, sound_cues
                )
                
                all_episode_audits.append(episode_audit)
                print(f"✅ Episode {episode_id} audit complete")

            # Step 4: Generate summary report
            print("\n" + "=" * 70)
            print("📊 GENERATING SUMMARY REPORT")
            print("=" * 70)
            
            summary = await self.generate_summary_report(all_episode_audits)
            
            print("✅ Summary report generated")

            # Step 5: Save outputs
            print("\n💾 Saving outputs...")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_basename = f"session_{self.session_id}_sfx_hygiene"
            
            # Save detailed audit JSON
            audit_file = self.output_dir / f"{output_basename}_audit.json"
            with open(audit_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'session_id': self.session_id,
                    'timestamp': timestamp,
                    'episodes': {audit['episode_id']: audit for audit in all_episode_audits},
                    'summary': summary
                }, f, indent=2, ensure_ascii=False)
            
            # Save summary markdown
            summary_file = self.output_dir / f"{output_basename}_summary.md"
            self.save_summary_markdown(summary_file, summary, all_episode_audits)
            
            # Save fixes JSON
            fixes = self.extract_fixes(all_episode_audits)
            fixes_file = self.output_dir / f"{output_basename}_fixes.json"
            with open(fixes_file, 'w', encoding='utf-8') as f:
                json.dump(fixes, f, indent=2, ensure_ascii=False)
            
            print(f"   ✓ {audit_file}")
            print(f"   ✓ {summary_file}")
            print(f"   ✓ {fixes_file}")

            # Step 6: Display critical issues
            self.display_critical_issues(summary)

            # Step 7: User approval
            print("\n" + "=" * 70)
            print("⚠️  ACTION REQUIRED: REVIEW RECOMMENDATIONS")
            print("=" * 70)
            
            fix_count = len(fixes.get('cut_list', []))
            if fix_count > 0:
                print(f"\n📋 Found {fix_count} recommended changes:")
                print("   - Cut list: Unnecessary sound cues")
                print("   - Add list: Missing essential sounds")
                print("   - Adjustments: Timing, volume, style issues")
                
                response = input("\nWould you like to review the detailed recommendations? (yes/no): ").strip().lower()
                if response == 'yes':
                    self.display_detailed_recommendations(fixes)
            else:
                print("✅ No critical issues found. Sound hygiene looks good!")

            print("\n✅ Station 36 Complete!")
            print(f"📁 Output directory: {self.output_dir}")

        except Exception as e:
            logger.error(f"Error in Station 36: {str(e)}", exc_info=True)
            raise

    def extract_sound_cues(self, script_content: str) -> List[Dict[str, Any]]:
        """Extract all sound cues from script"""
        sound_cues = []
        
        # Pattern to match [SFX: ...], [MUSIC: ...], [AMBIENCE: ...], [SILENCE: ...]
        patterns = {
            'SFX': r'\[SFX:\s*([^\]]+)\]',
            'MUSIC': r'\[MUSIC:\s*([^\]]+)\]',
            'AMBIENCE': r'\[AMBIENCE:\s*([^\]]+)\]',
            'SILENCE': r'\[SILENCE:\s*([^\]]+)\]'
        }
        
        for sound_type, pattern in patterns.items():
            matches = re.finditer(pattern, script_content, re.IGNORECASE)
            for match in matches:
                sound_cues.append({
                    'type': sound_type,
                    'description': match.group(1).strip(),
                    'position': match.start(),
                    'line_context': self._get_line_context(script_content, match.start())
                })
        
        return sound_cues

    def _get_line_context(self, script_content: str, position: int) -> str:
        """Get line context around position"""
        lines = script_content[:position].split('\n')
        if len(lines) > 0:
            return lines[-1].strip()
        return ""

    async def load_station27_data(self) -> Dict[str, Any]:
        """Load Station 27 master scripts"""
        try:
            # Try to load from output files first
            episode_files = []
            
            # Scan for episode directories in station_27
            station27_dir = Path("output/station_27")
            if not station27_dir.exists():
                raise ValueError(f"Station 27 output directory not found")
            
            # Look for episode_XX directories
            episode_dirs = sorted([d for d in station27_dir.iterdir() if d.is_dir() and d.name.startswith("episode_")])
            
            if not episode_dirs:
                raise ValueError(f"No episode data found in Station 27 output")
            
            episodes = {}
            
            for episode_dir in episode_dirs:
                episode_num = episode_dir.name.replace("episode_", "")
                
                # Look for the MASTER JSON file
                master_file = episode_dir / f"{episode_dir.name}_MASTER.json"
                
                if master_file.exists():
                    with open(master_file, 'r', encoding='utf-8') as f:
                        episode_data = json.load(f)
                        
                        # Only include if session_id matches
                        if episode_data.get('session_id') == self.session_id:
                            episodes[f"episode_{episode_num}"] = episode_data
            
            if not episodes:
                raise ValueError(f"""
❌ No Station 27 data found for session: '{self.session_id}'

REQUIRED: Station 36 depends on Station 27 (Master Script Assembly)

SOLUTIONS:
1. Run Station 27 first to generate script data
2. Check that session_id matches in the output files

To run Station 27:
  python -m app.agents.station_27_master_script_assembly <session_id>
""")
            
            # Return in the format expected by Station 36
            return {
                'working_title': episodes.get('episode_01', {}).get('production_package', {}).get('title', 'Unknown'),
                'episodes': episodes
            }
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error loading Station 27 data: {str(e)}")
            raise

    def display_project_summary(self, station27_data: Dict[str, Any]):
        """Display project summary"""
        print("📊 PROJECT SUMMARY")
        print("-" * 60)
        
        working_title = station27_data.get('working_title', 'Unknown Project')
        episodes = station27_data.get('episodes', {})
        
        print(f"   Project: {working_title}")
        print(f"   Episodes: {len(episodes)}")
        print()

    async def run_audit_sequence(self, episode_id: str, episode_data: Dict[str, Any], sound_cues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run 4-task audit sequence"""
        
        # Extract script content from Station 27 format
        master_assembly = episode_data.get('master_script_assembly', {})
        script_content = master_assembly.get('master_script_text', '')
        
        if not script_content:
            script_content = episode_data.get('script', episode_data.get('master_script_text', ''))
        
        # Task 1: Sound Effects Audit
        print("\n   Task 1: Sound Effects Audit...")
        sfx_audit = await self.audit_sound_effects(episode_id, script_content, sound_cues)
        
        # Task 2: Music Audit
        print("   Task 2: Music Audit...")
        music_audit = await self.audit_music(episode_id, script_content, sound_cues)
        
        # Task 3: Ambience Audit
        print("   Task 3: Ambience Audit...")
        ambience_audit = await self.audit_ambience(episode_id, script_content, sound_cues)
        
        # Task 4: Silence Audit
        print("   Task 4: Silence Audit...")
        silence_audit = await self.audit_silence(episode_id, script_content, sound_cues)
        
        return {
            'episode_id': episode_id,
            'sfx_audit': sfx_audit,
            'music_audit': music_audit,
            'ambience_audit': ambience_audit,
            'silence_audit': silence_audit,
            'total_cues': len(sound_cues)
        }

    async def audit_sound_effects(self, episode_id: str, script_content: str, sound_cues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Task 1: Audit sound effects"""
        sfx_cues = [cue for cue in sound_cues if cue['type'] == 'SFX']
        
        prompt = self.config_data['prompts']['sound_effects_audit'].format(
            episode_id=episode_id,
            script_content=script_content,
            sfx_cues=json.dumps(sfx_cues, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('sound_effects_audit', {})

    async def audit_music(self, episode_id: str, script_content: str, sound_cues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Task 2: Audit music"""
        music_cues = [cue for cue in sound_cues if cue['type'] == 'MUSIC']
        
        prompt = self.config_data['prompts']['music_audit'].format(
            episode_id=episode_id,
            script_content=script_content,
            music_cues=json.dumps(music_cues, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('music_audit', {})

    async def audit_ambience(self, episode_id: str, script_content: str, sound_cues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Task 3: Audit ambience"""
        ambience_cues = [cue for cue in sound_cues if cue['type'] == 'AMBIENCE']
        
        prompt = self.config_data['prompts']['ambience_audit'].format(
            episode_id=episode_id,
            script_content=script_content,
            ambience_cues=json.dumps(ambience_cues, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('ambience_audit', {})

    async def audit_silence(self, episode_id: str, script_content: str, sound_cues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Task 4: Audit silence"""
        silence_cues = [cue for cue in sound_cues if cue['type'] == 'SILENCE']
        
        prompt = self.config_data['prompts']['silence_audit'].format(
            episode_id=episode_id,
            script_content=script_content,
            silence_cues=json.dumps(silence_cues, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('silence_audit', {})

    async def generate_summary_report(self, all_audits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        
        prompt = self.config_data['prompts']['summary_report'].format(
            all_audits=json.dumps(all_audits, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('summary_report', {})

    def extract_fixes(self, all_audits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract fix recommendations from audits"""
        fixes = {
            'cut_list': [],
            'add_list': [],
            'adjustments': []
        }
        
        for audit in all_audits:
            episode_id = audit['episode_id']
            
            # Extract from each task
            for task in ['sfx_audit', 'music_audit', 'ambience_audit', 'silence_audit']:
                task_data = audit.get(task, {})
                
                # Cut list
                cuts = task_data.get('cut_list', [])
                fixes['cut_list'].extend([
                    {**item, 'episode': episode_id, 'task': task}
                    for item in cuts
                ])
                
                # Add list
                adds = task_data.get('add_list', [])
                fixes['add_list'].extend([
                    {**item, 'episode': episode_id, 'task': task}
                    for item in adds
                ])
                
                # Adjustments
                adjustments = task_data.get('adjustments', [])
                fixes['adjustments'].extend([
                    {**item, 'episode': episode_id, 'task': task}
                    for item in adjustments
                ])
        
        return fixes

    def display_critical_issues(self, summary: Dict[str, Any]):
        """Display critical issues from summary"""
        critical_issues = summary.get('critical_issues', [])
        
        if critical_issues:
            print("\n⚠️  CRITICAL ISSUES FOUND:")
            for i, issue in enumerate(critical_issues, 1):
                print(f"   {i}. {issue.get('description', 'Unknown issue')}")
                print(f"      Severity: {issue.get('severity', 'UNKNOWN')}")
        else:
            print("\n✅ No critical issues found")

    def display_detailed_recommendations(self, fixes: Dict[str, Any]):
        """Display detailed fix recommendations"""
        print("\n" + "=" * 70)
        print("📋 DETAILED RECOMMENDATIONS")
        print("=" * 70)
        
        if fixes.get('cut_list'):
            print(f"\n🗑️  CUT LIST ({len(fixes['cut_list'])} items):")
            for item in fixes['cut_list'][:10]:  # Show first 10
                print(f"   - Episode {item['episode']}: {item.get('description', 'N/A')}")
                print(f"     Reason: {item.get('reason', 'N/A')}")
        
        if fixes.get('add_list'):
            print(f"\n➕ ADD LIST ({len(fixes['add_list'])} items):")
            for item in fixes['add_list'][:10]:  # Show first 10
                print(f"   - Episode {item['episode']}: {item.get('description', 'N/A')}")
                print(f"     Reason: {item.get('reason', 'N/A')}")
        
        if fixes.get('adjustments'):
            print(f"\n🔧 ADJUSTMENTS ({len(fixes['adjustments'])} items):")
            for item in fixes['adjustments'][:10]:  # Show first 10
                print(f"   - Episode {item['episode']}: {item.get('description', 'N/A')}")
                print(f"     Fix: {item.get('fix', 'N/A')}")

    def save_summary_markdown(self, filepath: Path, summary: Dict[str, Any], all_audits: List[Dict[str, Any]]):
        """Save summary report as markdown"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Music & Sound Effects Hygiene Report\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary text
            f.write("## Summary\n\n")
            f.write(summary.get('summary_text', 'No summary available') + "\n\n")
            
            # Overall scores
            overall = summary.get('overall_scores', {})
            if overall:
                f.write("## Overall Scores\n\n")
                f.write(f"- SFX Necessity: {overall.get('sfx_necessity_score', 'N/A')}/100\n")
                f.write(f"- Music Function: {overall.get('music_function_score', 'N/A')}/100\n")
                f.write(f"- Ambience Layering: {overall.get('ambience_layering_score', 'N/A')}/100\n")
                f.write(f"- Silence Usage: {overall.get('silence_usage_score', 'N/A')}/100\n\n")
            
            # Critical issues
            critical = summary.get('critical_issues', [])
            if critical:
                f.write("## Critical Issues\n\n")
                for issue in critical:
                    f.write(f"### {issue.get('severity', 'UNKNOWN')}: {issue.get('title', 'Untitled')}\n\n")
                    f.write(f"{issue.get('description', 'No description')}\n\n")
            
            # Recommendations
            recommendations = summary.get('recommendations', [])
            if recommendations:
                f.write("## Recommendations\n\n")
                for rec in recommendations[:20]:  # Limit to 20
                    f.write(f"### {rec.get('priority', 'NORMAL')}: {rec.get('title', 'Untitled')}\n\n")
                    f.write(f"{rec.get('description', 'No description')}\n\n")
            
            f.write("---\n\n")
            f.write("*Generated by Station 36: Music & Sound Effects Hygiene*\n")


if __name__ == "__main__":
    import sys
    
    # Get session_id from command line or prompt user
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
    else:
        print("\n" + "="*70)
        print("🎵 STATION 36: MUSIC & SOUND EFFECTS HYGIENE")
        print("="*70)
        print()
        print("Please enter the session ID to process:")
        print("(Default: session_20251023_112749)")
        session_input = input("Session ID: ").strip()
        session_id = session_input if session_input else "session_20251023_112749"
        print()
    
    async def main():
        station = Station36MusicSfxHygiene(session_id=session_id)
        await station.initialize()
        await station.run()
    
    asyncio.run(main())

