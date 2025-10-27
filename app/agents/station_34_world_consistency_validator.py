"""
Station 34: World Consistency Validator

This station validates world consistency across all episode scripts, ensuring rules are maintained,
audio signatures are consistent, and character-world interactions are logical.

Flow:
1. Load Station 27 master scripts
2. Load Station 8 world building data
3. Load Station 9 world building system (if exists)
4. Execute 4-task validation sequence:
   - Task 1: World Rules Compliance Check
   - Task 2: Audio World Signature Verification
   - Task 3: Character World Interaction Check
   - Task 4: Cross-World Consistency Check (if multiple worlds/timelines)
5. Generate comprehensive consistency validation reports
6. Save JSON + TXT outputs
7. Require user approval before applying fixes

Critical Implementation Rules:
- Validate against established world rules from Station 8
- Check audio signature consistency across episodes
- Ensure character knowledge/capabilities are world-appropriate
- Flag anachronisms and logical inconsistencies
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


class Station34WorldConsistencyValidator:
    """Station 34: World Consistency Validator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=34)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path("output/station_34")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_34.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 34 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🌍 STATION 34: WORLD CONSISTENCY VALIDATOR")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            station8_data = await self.load_station8_data()
            station9_data = await self.load_station9_data()
            
            print("✅ All inputs loaded successfully")
            episodes = station27_data.get('episodes', {})
            print(f"   ✓ Station 27: {len(episodes)} master scripts")
            print(f"   ✓ Station 8: World building data loaded")
            if station9_data:
                print(f"   ✓ Station 9: World building system loaded")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data, station8_data)

            # Step 3: Process all episodes
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            print(f"📊 Processing {len(episodes)} episodes for world consistency validation...")
            print()

            all_episode_validations = []
            error_log = []

            # Process each episode
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"🎬 Processing Episode: {episode_id}")
                print("-" * 70)

                try:
                    # Execute all 4 tasks for this episode
                    print("🔍 Task 1/4: World Rules Compliance Check...")
                    world_rules_check = await self.execute_task1_world_rules_compliance(
                        episode_data, episode_id, station8_data, station9_data
                    )
                    print("✅ World rules check complete")

                    print("🔍 Task 2/4: Audio World Signature Verification...")
                    audio_signature_check = await self.execute_task2_audio_world_signature(
                        episode_data, episode_id, station8_data
                    )
                    print("✅ Audio signature check complete")

                    print("🔍 Task 3/4: Character World Interaction Check...")
                    character_interaction_check = await self.execute_task3_character_world_interaction(
                        episode_data, episode_id, station8_data
                    )
                    print("✅ Character interaction check complete")

                    print("🔍 Task 4/4: Cross-World Consistency Check...")
                    cross_world_check = await self.execute_task4_cross_world_consistency(
                        episode_data, episode_id, station8_data
                    )
                    print("✅ Cross-world check complete")

                    validation_results = {
                        'episode_id': episode_id,
                        'world_rules_check': world_rules_check,
                        'audio_signature_check': audio_signature_check,
                        'character_interaction_check': character_interaction_check,
                        'cross_world_check': cross_world_check
                    }

                    all_episode_validations.append(validation_results)
                    print(f"✅ Episode {episode_id} validation complete\n")

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
                all_episode_validations, station8_data, station9_data
            )
            print("✅ Summary report generated")

            # Step 5: Generate output files
            print("\n" + "=" * 70)
            print("💾 GENERATING OUTPUT FILES")
            print("=" * 70)
            await self.generate_output_files(
                all_episode_validations,
                summary_report,
                error_log
            )
            print(f"✅ All output files generated in: {self.output_dir}/")

            # Step 6: User validation prompt
            print("\n" + "=" * 70)
            print("🔍 USER VALIDATION REQUIRED")
            print("=" * 70)
            print(f"Review {self.session_id}_world_consistency_report.md for all issues.")
            
            try:
                response = input("Would you like to review the detailed report? [y/n]: ").strip().lower()
                if response == 'y':
                    print("✅ Report review initiated")
                else:
                    print("⏸️  Skipping report review")
            except (EOFError, KeyboardInterrupt):
                print("⏸️  Report review skipped (no user input available)")
            
            print("\n✅ Station 34 validation complete!")

        except Exception as e:
            logger.error(f"Station 34 failed: {str(e)}")
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
        """Load Station 8 world building data"""
        try:
            station_8_dir = Path("output/station_08")
            if not station_8_dir.exists():
                return {}
            
            # Try to find the world bible file
            for file in station_8_dir.glob("*_world_bible.json"):
                with open(file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return {}
        except Exception as e:
            logger.warning(f"Could not load Station 8 data: {str(e)}")
            return {}

    async def load_station9_data(self) -> Optional[Dict]:
        """Load Station 9 world building system data"""
        try:
            station_9_dir = Path("output/station_09")
            if not station_9_dir.exists():
                return None
            
            for file in station_9_dir.glob("*_world_building_system.json"):
                with open(file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
        except Exception as e:
            logger.warning(f"Could not load Station 9 data: {str(e)}")
            return None

    def display_project_summary(self, station27_data: Dict, station8_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = station27_data.get('episodes', {})
        
        print(f"Total Episodes to Validate: {len(episodes)}")
        
        if station8_data:
            world_name = station8_data.get('world_name', 'Unknown')
            print(f"World Name: {world_name}")
        
        print()

    async def execute_task1_world_rules_compliance(
        self, 
        episode: Dict, 
        episode_id: Any, 
        station8_data: Dict,
        station9_data: Optional[Dict]
    ) -> Dict:
        """Task 1: World Rules Compliance Check"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis'}
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'world_rules': json.dumps(station8_data.get('world_rules', {}), ensure_ascii=False),
                'system_data': json.dumps(station9_data or {}, ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('world_rules_compliance').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('world_rules_compliance', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_audio_world_signature(
        self,
        episode: Dict,
        episode_id: Any,
        station8_data: Dict
    ) -> Dict:
        """Task 2: Audio World Signature Verification"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis'}
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'audio_signatures': json.dumps(station8_data.get('audio_signatures', {}), ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('audio_signature_verification').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('audio_signature_check', {})
            
        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_character_world_interaction(
        self,
        episode: Dict,
        episode_id: Any,
        station8_data: Dict
    ) -> Dict:
        """Task 3: Character World Interaction Check"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis'}
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'world_parameters': json.dumps(station8_data.get('world_parameters', {}), ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('character_world_interaction').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('character_interaction_check', {})
            
        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_cross_world_consistency(
        self,
        episode: Dict,
        episode_id: Any,
        station8_data: Dict
    ) -> Dict:
        """Task 4: Cross-World Consistency Check"""
        try:
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {'warning': 'No content available for analysis', 'applicable': False}
            
            # Check if multiple worlds exist
            has_multiple_worlds = station8_data.get('has_multiple_worlds', False)
            
            if not has_multiple_worlds:
                return {'applicable': False, 'note': 'Single world - no cross-world validation needed'}
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],
                'world_transitions': json.dumps(station8_data.get('world_transitions', {}), ensure_ascii=False),
                'world_rules': json.dumps(station8_data.get('world_rules', {}), ensure_ascii=False)
            }
            
            prompt = self.config.get_prompt('cross_world_consistency').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('cross_world_check', {})
            
        except Exception as e:
            logger.error(f"Task 4 failed: {str(e)}")
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    async def generate_summary_report(
        self,
        all_validations: List[Dict],
        station8_data: Dict,
        station9_data: Optional[Dict]
    ) -> Dict:
        """Generate comprehensive summary report"""
        try:
            context = {
                'all_validations': json.dumps(all_validations, ensure_ascii=False),
                'world_context': json.dumps(station8_data, ensure_ascii=False),
                'system_context': json.dumps(station9_data or {}, ensure_ascii=False)
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
        all_validations: List[Dict],
        summary_report: Dict,
        error_log: List[str]
    ):
        """Generate all output files"""
        
        # 1. World consistency validation results
        consistency_results = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'summary': summary_report,
            'episode_validations': all_validations
        }
        
        with open(self.output_dir / f'{self.session_id}_world_consistency_results.json', 'w', encoding='utf-8') as f:
            json.dump(consistency_results, f, indent=2, ensure_ascii=False)
        
        # 2. Violations report
        violations_report = self._compile_violations_report(all_validations)
        
        with open(self.output_dir / f'{self.session_id}_world_consistency_violations.json', 'w', encoding='utf-8') as f:
            json.dump(violations_report, f, indent=2, ensure_ascii=False)
        
        # 3. Fix recommendations
        fix_recommendations = self._compile_fix_recommendations(all_validations)
        
        with open(self.output_dir / f'{self.session_id}_world_consistency_fixes.json', 'w', encoding='utf-8') as f:
            json.dump(fix_recommendations, f, indent=2, ensure_ascii=False)
        
        # 4. Markdown report
        markdown_report = self._generate_markdown_report(
            consistency_results, violations_report, fix_recommendations, error_log
        )
        
        with open(self.output_dir / f'{self.session_id}_world_consistency_report.md', 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        
        # 5. Error log (if errors exist)
        if error_log:
            with open(self.output_dir / f'{self.session_id}_error_log.txt', 'w', encoding='utf-8') as f:
                f.write("ERROR LOG\n")
                f.write("=" * 70 + "\n\n")
                for error in error_log:
                    f.write(f"❌ {error}\n")
    
    def _compile_violations_report(self, all_validations: List[Dict]) -> Dict:
        """Compile all violations from validations"""
        violations = {
            'critical_violations': [],
            'major_violations': [],
            'minor_violations': [],
            'audio_inconsistencies': [],
            'character_world_violations': []
        }
        
        for validation in all_validations:
            episode_id = validation.get('episode_id')
            
            # Extract violations from each task
            for task_name in ['world_rules_check', 'audio_signature_check', 
                            'character_interaction_check', 'cross_world_check']:
                task_result = validation.get(task_name, {})
                task_violations = task_result.get('violations', [])
                
                for violation in task_violations:
                    violation['episode_id'] = episode_id
                    violation['task'] = task_name
                    
                    severity = violation.get('severity', 'MEDIUM')
                    if severity == 'CRITICAL':
                        violations['critical_violations'].append(violation)
                    elif severity == 'HIGH':
                        violations['major_violations'].append(violation)
                    else:
                        violations['minor_violations'].append(violation)
        
        return violations
    
    def _compile_fix_recommendations(self, all_validations: List[Dict]) -> Dict:
        """Compile fix recommendations"""
        fixes = {
            'immediate_fixes': [],
            'review_fixes': [],
            'audio_fixes': [],
            'character_fixes': []
        }
        
        for validation in all_validations:
            episode_id = validation.get('episode_id')
            
            for task_name in ['world_rules_check', 'audio_signature_check',
                            'character_interaction_check', 'cross_world_check']:
                task_result = validation.get(task_name, {})
                recommendations = task_result.get('recommendations', [])
                
                for rec in recommendations:
                    rec['episode_id'] = episode_id
                    rec['task'] = task_name
                    fixes['immediate_fixes'].append(rec)
        
        return fixes
    
    def _generate_markdown_report(
        self,
        consistency_results: Dict,
        violations_report: Dict,
        fix_recommendations: Dict,
        error_log: List[str]
    ) -> str:
        """Generate human-readable markdown report"""
        report = f"""# World Consistency Validation Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session ID: {self.session_id}

## Executive Summary

{consistency_results.get('summary', {}).get('summary_text', 'No summary available')}

## Critical Violations

"""
        
        critical = violations_report.get('critical_violations', [])
        for i, violation in enumerate(critical[:10], 1):  # Show first 10
            report += f"{i}. {violation.get('description', 'Unknown')} - Episode {violation.get('episode_id', 'N/A')}\n"
        
        report += "\n## Major Violations\n\n"
        
        major = violations_report.get('major_violations', [])
        for i, violation in enumerate(major[:10], 1):
            report += f"{i}. {violation.get('description', 'Unknown')} - Episode {violation.get('episode_id', 'N/A')}\n"
        
        report += "\n## Recommended Fixes\n\n"
        
        fixes = fix_recommendations.get('immediate_fixes', [])
        for i, fix in enumerate(fixes[:10], 1):
            report += f"{i}. {fix.get('recommendation', 'Unknown')} - Episode {fix.get('episode_id', 'N/A')}\n"
        
        if error_log:
            report += "\n## Errors Encountered\n\n"
            for error in error_log:
                report += f"- ❌ {error}\n"
        
        return report


async def main():
    """Run Station 34 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    validator = Station34WorldConsistencyValidator(session_id)
    await validator.initialize()
    
    try:
        await validator.run()
        print(f"\n✅ Success! World consistency validation complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
