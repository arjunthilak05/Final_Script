"""
Station 35: Character Voice Distinction Audit

This station audits character voice distinction across all episode scripts, ensuring each
character has a unique, consistent voice that's distinguishable in audio-only format.

Flow:
1. Load Station 27 master scripts
2. Load Station 8 character bibles
3. Execute 4-task analysis sequence:
   - Task 1: Voice Uniqueness Check
   - Task 2: Voice Evolution Tracking
   - Task 3: Dialogue Attribution Test
   - Task 4: Performance Notes Enhancement
4. Generate comprehensive voice distinction reports
5. Save JSON + Markdown outputs
6. Require user approval before applying fixes

Critical Implementation Rules:
- Ensure each character has unique vocabulary, speech patterns, and verbal tics
- Track voice consistency across episodes
- Test if characters are distinguishable without names
- Add performance direction notes for actors
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


class Station35CharacterVoiceDistinction:
    """Station 35: Character Voice Distinction Audit"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=35)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path("output/station_35")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_35.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 35 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🎤 STATION 35: CHARACTER VOICE DISTINCTION AUDIT")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            station8_data = await self.load_station8_data()
            
            print("✅ All inputs loaded successfully")
            episodes = station27_data.get('episodes', {})
            print(f"   ✓ Station 27: {len(episodes)} master scripts")
            if station8_data:
                print(f"   ✓ Station 8: Character bibles loaded")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data, station8_data)

            # Step 3: Process all episodes
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            print(f"📊 Processing {len(episodes)} episodes for voice distinction analysis...")
            print()

            all_episode_audits = []
            error_log = []

            # Process each episode
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"🎬 Processing Episode: {episode_id}")
                print("-" * 70)

                try:
                    # Execute all 4 tasks for this episode
                    print("🔍 Task 1/4: Voice Uniqueness Check...")
                    uniqueness_check = await self.execute_task1_voice_uniqueness(
                        episode_data, episode_id, station8_data
                    )
                    print("✅ Voice uniqueness check complete")

                    print("🔍 Task 2/4: Voice Evolution Tracking...")
                    evolution_check = await self.execute_task2_voice_evolution(
                        episode_data, episode_id, station8_data
                    )
                    print("✅ Voice evolution check complete")

                    print("🔍 Task 3/4: Dialogue Attribution Test...")
                    attribution_check = await self.execute_task3_dialogue_attribution(
                        episode_data, episode_id, station8_data
                    )
                    print("✅ Dialogue attribution test complete")

                    print("🔍 Task 4/4: Performance Notes Enhancement...")
                    performance_notes = await self.execute_task4_performance_notes(
                        episode_data, episode_id, station8_data, station27_data
                    )
                    print("✅ Performance notes enhanced")

                    audit_results = {
                        'episode_id': episode_id,
                        'uniqueness_check': uniqueness_check,
                        'evolution_check': evolution_check,
                        'attribution_check': attribution_check,
                        'performance_notes': performance_notes
                    }

                    all_episode_audits.append(audit_results)
                    print(f"✅ Episode {episode_id} voice audit complete\n")

                except Exception as e:
                    error_msg = f"Error processing episode {episode_id}: {str(e)}"
                    logger.error(error_msg)
                    error_log.append(error_msg)
                    print(f"⚠️  {error_msg}\n")

            # Step 4: Generate summary report
            print("=" * 70)
            print("📊 GENERATING SUMMARY REPORT")
            print("=" * 70)
            summary_report = await self.generate_summary_report(
                all_episode_audits, station8_data
            )
            print("✅ Summary report generated")

            # Step 5: Generate output files
            print("\n" + "=" * 70)
            print("💾 GENERATING OUTPUT FILES")
            print("=" * 70)
            await self.generate_output_files(
                all_episode_audits,
                summary_report,
                error_log
            )
            print(f"✅ All output files generated in: {self.output_dir}/")

            # Step 6: User validation prompt
            print("\n" + "=" * 70)
            print("🔍 USER VALIDATION REQUIRED")
            print("=" * 70)
            print(f"Review {self.session_id}_voice_distinction_report.md for all issues.")
            
            try:
                response = input("Would you like to review the detailed report? [y/n]: ").strip().lower()
                if response == 'y':
                    print("✅ Report review initiated")
                else:
                    print("⏸️  Skipping report review")
            except (EOFError, KeyboardInterrupt):
                print("⏸️  Report review skipped (no user input available)")
            
            print("\n✅ Station 35 voice distinction audit complete!")

        except Exception as e:
            logger.error(f"Station 35 failed: {str(e)}")
            raise

    async def load_station27_data(self) -> Dict:
        """Load Station 27 master scripts from output files"""
        try:
            station_27_dir = Path("output/station_27")
            episodes = {}
            
            if not station_27_dir.exists():
                raise ValueError(f"❌ Station 27 directory not found: {station_27_dir}")
            
            for episode_dir in station_27_dir.iterdir():
                if episode_dir.is_dir() and episode_dir.name.startswith("episode_"):
                    try:
                        episode_num = int(episode_dir.name.split("_")[1])
                        json_file = episode_dir / f"episode_{episode_num:02d}_MASTER.json"
                        
                        if json_file.exists():
                            with open(json_file, 'r', encoding='utf-8') as f:
                                episode_data = json.load(f)
                                episodes[episode_num] = episode_data
                    except (ValueError, KeyError, json.JSONDecodeError):
                        continue
            
            if not episodes:
                raise ValueError(f"❌ No Station 27 episodes found in {station_27_dir}")
            
            return {'episodes': episodes}
            
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 27 data: {str(e)}")

    async def load_station8_data(self) -> Dict:
        """Load Station 8 character bible data"""
        try:
            station_8_dir = Path("output/station_08")
            if not station_8_dir.exists():
                return {}
            
            # Try to find the character bible file
            for file in station_8_dir.glob("*_character_bible.json"):
                with open(file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return {}
        except Exception as e:
            logger.warning(f"Could not load Station 8 data: {str(e)}")
            return {}

    def display_project_summary(self, station27_data: Dict, station8_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = station27_data.get('episodes', {})
        
        print(f"Total Episodes to Audit: {len(episodes)}")
        
        if station8_data:
            characters = station8_data.get('characters', {})
            print(f"Total Characters: {len(characters)}")
        
        print()

    async def execute_task1_voice_uniqueness(
        self,
        episode: Dict,
        episode_id: Any,
        station8_data: Dict
    ) -> Dict:
        """Task 1: Voice Uniqueness Check"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis'}
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'character_profiles': json.dumps(station8_data.get('characters', {}), ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('voice_uniqueness_check').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('voice_uniqueness_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_voice_evolution(
        self,
        episode: Dict,
        episode_id: Any,
        station8_data: Dict
    ) -> Dict:
        """Task 2: Voice Evolution Tracking"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis'}
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'character_arcs': json.dumps(station8_data.get('character_arcs', {}), ensure_ascii=False),
                'character_profiles': json.dumps(station8_data.get('characters', {}), ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('voice_evolution_tracking').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('voice_evolution_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_dialogue_attribution(
        self,
        episode: Dict,
        episode_id: Any,
        station8_data: Dict
    ) -> Dict:
        """Task 3: Dialogue Attribution Test"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis'}
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'character_profiles': json.dumps(station8_data.get('characters', {}), ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('dialogue_attribution_test').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('attribution_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_performance_notes(
        self,
        episode: Dict,
        episode_id: Any,
        station8_data: Dict,
        all_episodes_data: Dict
    ) -> Dict:
        """Task 4: Performance Notes Enhancement"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis'}
            
            # Get previous audit results from earlier episodes to track evolution
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'character_profiles': json.dumps(station8_data.get('characters', {}), ensure_ascii=False),
                'previous_episodes_data': json.dumps(all_episodes_data, ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('performance_notes_enhancement').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('performance_notes', {})
            
        except Exception as e:
            logger.error(f"Task 4 failed: {str(e)}")
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    async def generate_summary_report(
        self,
        all_audits: List[Dict],
        station8_data: Dict
    ) -> Dict:
        """Generate comprehensive summary report"""
        try:
            context = {
                'all_audits': json.dumps(all_audits, ensure_ascii=False),
                'character_profiles': json.dumps(station8_data.get('characters', {}), ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('summary_report').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('summary_report', {})
            
        except Exception as e:
            logger.error(f"Summary report generation failed: {str(e)}")
            return {}

    def _extract_episode_content(self, episode: Dict) -> str:
        """Extract content from episode data"""
        format_conv = episode.get('format_conversion', {})
        
        fountain = format_conv.get('fountain_script', '')
        if fountain and fountain.strip():
            return fountain
        
        markdown = format_conv.get('markdown_script', '')
        if markdown and markdown.strip():
            return markdown
        
        master_text = episode.get('master_script_assembly', {}).get('master_script_text', '')
        if master_text and master_text.strip():
            return master_text
        
        return ''

    async def generate_output_files(
        self,
        all_audits: List[Dict],
        summary_report: Dict,
        error_log: List[str]
    ):
        """Generate all output files"""
        
        # 1. Voice distinction audit results
        audit_results = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'summary': summary_report,
            'episode_audits': all_audits
        }
        
        with open(self.output_dir / f'{self.session_id}_voice_distinction_audit.json', 'w', encoding='utf-8') as f:
            json.dump(audit_results, f, indent=2, ensure_ascii=False)
        
        # 2. Confusion risk assessment
        confusion_report = self._compile_confusion_risks(all_audits)
        
        with open(self.output_dir / f'{self.session_id}_confusion_risks.json', 'w', encoding='utf-8') as f:
            json.dump(confusion_report, f, indent=2, ensure_ascii=False)
        
        # 3. Performance notes summary
        performance_notes_summary = self._compile_performance_notes(all_audits)
        
        with open(self.output_dir / f'{self.session_id}_performance_notes.json', 'w', encoding='utf-8') as f:
            json.dump(performance_notes_summary, f, indent=2, ensure_ascii=False)
        
        # 4. Markdown report
        markdown_report = self._generate_markdown_report(
            audit_results, confusion_report, performance_notes_summary, error_log
        )
        
        with open(self.output_dir / f'{self.session_id}_voice_distinction_report.md', 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        
        # 5. Error log (if errors exist)
        if error_log:
            with open(self.output_dir / f'{self.session_id}_error_log.txt', 'w', encoding='utf-8') as f:
                f.write("ERROR LOG\n")
                f.write("=" * 70 + "\n\n")
                for error in error_log:
                    f.write(f"❌ {error}\n")
    
    def _compile_confusion_risks(self, all_audits: List[Dict]) -> Dict:
        """Compile all confusion risks from audits"""
        confusion_risks = {
            'high_risk_characters': [],
            'moderate_risk_pairs': [],
            'low_risk_issues': [],
            'identifiability_scores': {}
        }
        
        for audit in all_audits:
            episode_id = audit.get('episode_id')
            
            # Extract confusion data from attribution test
            attribution_check = audit.get('attribution_check', {})
            identifiability = attribution_check.get('identifiability_scores', {})
            confusion_pairs = attribution_check.get('confusion_pairs', [])
            
            for char, score in identifiability.items():
                if score < 50:
                    confusion_risks['high_risk_characters'].append({
                        'character': char,
                        'episode': episode_id,
                        'identifiability_score': score
                    })
                elif score < 75:
                    confusion_risks['moderate_risk_pairs'].append({
                        'character': char,
                        'episode': episode_id,
                        'identifiability_score': score
                    })
            
            confusion_risks['identifiability_scores'][f'episode_{episode_id}'] = identifiability
        
        return confusion_risks
    
    def _compile_performance_notes(self, all_audits: List[Dict]) -> Dict:
        """Compile performance notes from all audits"""
        notes = {
            'character_performance_directions': {},
            'physical_indicators': {},
            'emotional_indicators': {},
            'pace_indicators': {}
        }
        
        for audit in all_audits:
            episode_id = audit.get('episode_id')
            performance_data = audit.get('performance_notes', {})
            
            if performance_data:
                notes['character_performance_directions'][f'episode_{episode_id}'] = performance_data.get('character_directions', {})
                notes['physical_indicators'][f'episode_{episode_id}'] = performance_data.get('physical_indicators', {})
                notes['emotional_indicators'][f'episode_{episode_id}'] = performance_data.get('emotional_indicators', {})
                notes['pace_indicators'][f'episode_{episode_id}'] = performance_data.get('pace_indicators', {})
        
        return notes
    
    def _generate_markdown_report(
        self,
        audit_results: Dict,
        confusion_report: Dict,
        performance_notes: Dict,
        error_log: List[str]
    ) -> str:
        """Generate human-readable markdown report"""
        report = f"""# Character Voice Distinction Audit Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session ID: {self.session_id}

## Executive Summary

{audit_results.get('summary', {}).get('summary_text', 'No summary available')}

## Voice Distinction Scores

"""
        
        summary = audit_results.get('summary', {})
        
        # Add character uniqueness scores
        if 'character_uniqueness_scores' in summary:
            report += "### Character Voice Uniqueness\n\n"
            for char, score in summary['character_uniqueness_scores'].items():
                report += f"- **{char}**: {score}/100\n"
        
        report += "\n## High-Confusion Risk Characters\n\n"
        
        high_risk = confusion_report.get('high_risk_characters', [])
        for i, risk in enumerate(high_risk[:10], 1):
            report += f"{i}. **{risk.get('character', 'Unknown')}** - Episode {risk.get('episode', 'N/A')} (Score: {risk.get('identifiability_score', 'N/A')}/100)\n"
        
        report += "\n## Recommended Fixes\n\n"
        
        fixes = summary.get('recommended_fixes', [])
        for i, fix in enumerate(fixes[:10], 1):
            report += f"{i}. {fix.get('fix_description', 'Unknown')} - Character: {fix.get('character', 'N/A')}\n"
        
        if error_log:
            report += "\n## Errors Encountered\n\n"
            for error in error_log:
                report += f"- ❌ {error}\n"
        
        return report


async def main():
    """Run Station 35 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    auditor = Station35CharacterVoiceDistinction(session_id)
    await auditor.initialize()
    
    try:
        await auditor.run()
        print(f"\n✅ Success! Character voice distinction audit complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

