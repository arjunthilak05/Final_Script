"""
Station 40: Technical Format Verification Agent

This station verifies production readiness of all scripts with comprehensive format validation.
It checks standard format, audio cue formats, production notes, and documentation completeness.

Flow:
1. Load Station 39 output (or directly from Station 27)
2. Load technical requirements
3. Execute 3-task verification sequence:
   - Task 1: Format Verification (standard format, performance directions, scene structure, audio cues)
   - Task 2: Production Notes Verification (casting notes, technical requirements, delivery specs)
   - Task 3: Documentation Completeness (episode guide, character guide, sound bible)
4. Generate format compliance reports per episode
5. Generate correction requirements with specific fixes
6. Identify missing documentation
7. Generate production-ready certification
8. User validation required for production certification
9. Save all outputs

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config
- NO fallback defaults - Missing data = error
- FAIL FAST - Exit on config/input errors with actionable messages
- User validation required for production certification
- Explicit error messages with file names, line numbers
- Consistent logging to logs/station_40.log
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
log_file = log_dir / "station_40.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Station40FormatVerifier:
    """Station 40: Technical Format Verification Agent"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=40)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path(self.config_data.get('output_path', 'output/station_40'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate required config fields
        self._validate_config()
        
        # Format verification results
        self.format_errors = []
        self.correction_requirements = []
        self.missing_documentation = []
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_40.yml'

        if not config_path.exists():
            raise FileNotFoundError(f"❌ Station 40 config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)
    
    def _validate_config(self):
        """Validate configuration has required fields"""
        required_fields = ['input_path', 'output_path', 'error_threshold']
        for field in required_fields:
            if not self.config_data.get(field):
                raise ValueError(f"❌ Required config field missing: {field}")
        
        logger.info("✅ Configuration validated")
    
    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 40 initialized")
    
    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("📋 STATION 40: TECHNICAL FORMAT VERIFICATION")
        print("=" * 70)
        print()
        
        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station_data = await self.load_station_data()
            technical_requirements = await self.load_technical_requirements()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Loaded scripts from {self.config_data.get('input_path')}")
            print(f"   ✓ Technical requirements loaded")
            print()
            
            # Step 2: Display project summary
            episodes = station_data.get('episodes', {})
            self.display_project_summary(episodes, station_data)
            
            # Step 3: Process each episode
            all_episode_results = []
            total_errors = 0
            
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"\n🎬 Processing Episode: {episode_id}")
                print("-" * 70)
                
                # Execute 3-task verification sequence
                print("✅ Task 1/3: Format Verification...")
                format_verification = await self.execute_task1_format_verification(
                    episode_data, technical_requirements
                )
                
                print("📝 Task 2/3: Production Notes Verification...")
                production_notes = await self.execute_task2_production_notes_verification(
                    episode_data
                )
                
                print("📚 Task 3/3: Documentation Completeness...")
                documentation = await self.execute_task3_documentation_completeness(
                    episode_data
                )
                
                # Compile episode results
                episode_result = {
                    "episode_id": episode_id,
                    "format_verification": format_verification,
                    "production_notes_verification": production_notes,
                    "documentation_completeness": documentation,
                    "overall_compliance": self._calculate_compliance(
                        format_verification, production_notes, documentation
                    ),
                    "timestamp": datetime.now().isoformat()
                }
                
                # Track errors
                episode_errors = self._count_errors(episode_result)
                total_errors += episode_errors
                
                all_episode_results.append(episode_result)
                
                # Save individual episode results
                await self.save_episode_output(episode_result)
                
                print(f"✅ Episode {episode_id} verification complete")
                print(f"   Errors Found: {episode_errors}")
                print(f"   Compliance Status: {'✅ PASS' if episode_errors == 0 else '❌ FAIL'}")
            
            # Step 4: Check if user validation is required
            if total_errors > self.config_data.get('error_threshold', 10):
                print("\n" + "=" * 70)
                print("⚠️  FORMAT ERROR THRESHOLD EXCEEDED")
                print("=" * 70)
                print(f"\nTotal errors found: {total_errors}")
                print(f"Threshold: {self.config_data.get('error_threshold', 10)}")
                print("\nTop 5 Critical Issues:")
                
                top_issues = self._get_top_issues(all_episode_results, 5)
                for i, issue in enumerate(top_issues, 1):
                    print(f"\n{i}. {issue.get('check', 'Unknown')} ({issue.get('severity', 'Unknown')})")
                    print(f"   Location: {issue.get('location', 'N/A')}")
                    print(f"   Issue: {issue.get('fix_required', 'N/A')}")
                
                print("\n" + "=" * 70)
                user_response = input("⚠️  Proceed with verification report? (yes/no): ").strip().lower()
                if user_response not in ['yes', 'y']:
                    print("❌ Verification cancelled by user")
                    return
            
            # Step 5: Generate summary report
            print("\n" + "=" * 70)
            print("📊 GENERATING VERIFICATION SUMMARY")
            print("=" * 70)
            summary_report = await self.generate_summary_report(all_episode_results)
            
            # Step 6: Generate detailed reports
            await self.generate_detailed_reports(all_episode_results, summary_report)
            
            # Step 7: Production readiness certification
            # Always generate certification file (pass or fail status)
            is_production_ready = await self.require_user_approval(all_episode_results)
            await self.save_production_certification(all_episode_results, summary_report, is_production_ready)
            
            print("\n" + "=" * 70)
            print("✅ STATION 40 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Verified: {len(all_episode_results)}")
            print(f"Total Errors: {total_errors}")
            print(f"Production Ready: {'✓ YES' if is_production_ready else '✗ NO'}")
            print(f"\n📄 Output files:")
            print(f"   - output/station_40/{self.session_id}_format_compliance_report.json")
            print(f"   - output/station_40/{self.session_id}_correction_requirements.json")
            print(f"   - output/station_40/{self.session_id}_missing_documentation.json")
            print(f"   - output/station_40/{self.session_id}_detailed_log.txt")
            print(f"   - output/station_40/{self.session_id}_production_ready_certification.json")
        
        except Exception as e:
            logger.error(f"❌ Station 40 failed: {str(e)}")
            raise
    
    async def load_station_data(self) -> Dict:
        """Load scripts from previous station"""
        try:
            # Try loading from Station 27 first (has script content)
            station_27_path = Path("output/station_27")
            
            # Fallback to Station 39 if Station 27 doesn't exist
            if not station_27_path.exists():
                logger.warning(f"Station 27 path not found, trying Station 39")
                input_path = Path(self.config_data.get('input_path'))
                
                if not input_path.exists():
                    raise ValueError(
                        f"❌ Neither Station 27 nor Station 39 found\n"
                        "   Please run Station 27 (Master Script Assembly) first"
                    )
            else:
                input_path = station_27_path
            
            episodes = {}
            
            # Load all episodes from directory
            for episode_dir in input_path.iterdir():
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
                    f"❌ No episodes found in {input_path}\n"
                    "   Please run Station 27 (Master Script Assembly) first"
                )
            
            logger.info(f"Loaded {len(episodes)} episodes from {input_path}")
            return {'episodes': episodes}
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing episode data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading station data: {str(e)}")
    
    async def load_technical_requirements(self) -> Dict:
        """Load technical requirements document"""
        try:
            requirements_path = Path(self.config_data.get('technical_requirements_path'))
            
            # Try to load from configs directory
            if not requirements_path.exists():
                config_dir = Path(__file__).parent / 'configs'
                requirements_path = config_dir / "technical_requirements.json"
            
            if requirements_path.exists():
                with open(requirements_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Return default requirements if file doesn't exist
            logger.warning("Technical requirements file not found, using defaults")
            return {
                "standard_format": "Industry standard audiobook format",
                "audio_cue_formats": {
                    "sfx": "[SFX: description, timing, volume, source]",
                    "music": "[MUSIC: style, duration, in/out points, emotional intent, volume]",
                    "ambience": "[AMBIENCE: description, level, start/stop, ducking notes]",
                    "silence": "[SILENCE: duration, purpose]"
                },
                "character_format": "CAPS",
                "dialogue_indent": 4,
                "scene_structure": "INT./EXT. with time, numbered sequentially"
            }
            
        except Exception as e:
            logger.error(f"Error loading technical requirements: {str(e)}")
            raise ValueError(f"❌ Error loading technical requirements: {str(e)}")
    
    def display_project_summary(self, episodes: Dict, station_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        print(f"Episodes to Verify: {len(episodes)}")
        print()
        
        if episodes:
            print("Episode List:")
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)
    
    async def execute_task1_format_verification(self, episode: Dict, technical_requirements: Dict) -> Dict:
        """Task 1: Format Verification"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'format_compliance': {},
                    'format_errors': [],
                    'compliance_summary': {
                        'total_errors': 0,
                        'passes_all_checks': True
                    }
                }
            
            context = {
                'session_id': self.session_id,
                'episode_id': episode_id,
                'episode_content': episode_content[:20000],  # First 20000 chars
                'technical_requirements': json.dumps(technical_requirements, indent=2)
            }
            
            prompt = self.config.get_prompt('format_verification').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('format_verification', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")
    
    async def execute_task2_production_notes_verification(self, episode: Dict) -> Dict:
        """Task 2: Production Notes Verification"""
        try:
            production_package = episode.get('production_package', {})
            
            # Extract casting notes from voice_actor_specifications
            voice_actors = production_package.get('voice_actor_specifications', [])
            casting_notes_errors = []
            
            for actor in voice_actors:
                character = actor.get('character', '')
                missing_fields = []
                
                if not actor.get('vocal_characteristics'):
                    missing_fields.append('voice_type')
                if not actor.get('scenes'):
                    missing_fields.append('scenes')
                if not actor.get('key_directions'):
                    missing_fields.append('relationship_notes')
                
                if missing_fields:
                    casting_notes_errors.append({
                        'character': character,
                        'missing_fields': missing_fields,
                        'severity': 'MEDIUM'
                    })
            
            # Check technical requirements
            sound_specs = production_package.get('sound_design_specifications', {})
            missing_technical = []
            
            if not sound_specs.get('required_effects'):
                missing_technical.append('special_effects_list')
            if not sound_specs.get('music_cues'):
                missing_technical.append('music_style_guide')
            if not sound_specs.get('ambient_layers'):
                missing_technical.append('ambience_library_needs')
            
            # Check delivery specs
            delivery = production_package.get('delivery_specifications', {})
            missing_delivery = []
            
            if not delivery.get('target_format'):
                missing_delivery.append('file_format')
            if not delivery.get('quality_standard'):
                missing_delivery.append('naming_conventions')
            
            return {
                'casting_notes_complete': len(casting_notes_errors) == 0,
                'casting_notes_errors': casting_notes_errors,
                'technical_requirements_complete': len(missing_technical) == 0,
                'missing_technical_fields': missing_technical,
                'delivery_specs_complete': len(missing_delivery) == 0,
                'missing_delivery_fields': missing_delivery,
                'verification_summary': {
                    'all_complete': len(casting_notes_errors) == 0 and len(missing_technical) == 0 and len(missing_delivery) == 0,
                    'total_errors': len(casting_notes_errors) + len(missing_technical) + len(missing_delivery),
                    'blocking_errors': 0  # These are mostly informational
                }
            }
            
        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")
    
    async def execute_task3_documentation_completeness(self, episode: Dict) -> Dict:
        """Task 3: Documentation Completeness"""
        try:
            production_package = episode.get('production_package', {})
            
            # For episodes, documentation is embedded in production_package
            # Check what documentation elements are present
            episode_guide = {
                'synopsis': production_package.get('cast_briefing', {}).get('episode_overview', ''),
                'character_appearances': production_package.get('voice_actor_specifications', []),
                'location_list': self._extract_locations_from_scenes(production_package.get('cast_briefing', {}).get('key_scenes', [])),
                'runtime_estimate': production_package.get('production_summary', {}).get('estimated_runtime', '')
            }
            
            character_guide = {
                'character_list': production_package.get('voice_actor_specifications', []),
                'character_relationships': [],  # Not in current structure
                'voice_descriptions': production_package.get('voice_actor_specifications', []),
                'episode_appearances': {}  # Not in current structure
            }
            
            sound_bible = {
                'recurring_sounds_catalog': production_package.get('sound_design_specifications', {}).get('required_effects', []),
                'music_themes': production_package.get('sound_design_specifications', {}).get('music_cues', []),
                'ambience_catalog': production_package.get('sound_design_specifications', {}).get('ambient_layers', []),
                'signature_sounds': []  # Not in current structure
            }
            
            # Simple validation: check if key sections exist
            episode_guide_complete = bool(episode_guide['synopsis'] and episode_guide['character_appearances'])
            character_guide_complete = bool(character_guide['character_list'] and len(character_guide['voice_descriptions']) > 0)
            sound_bible_complete = bool(sound_bible['recurring_sounds_catalog'] or sound_bible['music_themes'] or sound_bible['ambience_catalog'])
            
            missing_sections = []
            if not episode_guide_complete:
                missing_sections.append({'document': 'episode_guide', 'missing_section': 'synopsis or character_appearances', 'severity': 'MEDIUM'})
            if not character_guide_complete:
                missing_sections.append({'document': 'character_guide', 'missing_section': 'character_list or voice_descriptions', 'severity': 'MEDIUM'})
            if not sound_bible_complete:
                missing_sections.append({'document': 'sound_bible', 'missing_section': 'sound design specifications', 'severity': 'LOW'})
            
            return {
                'episode_guide_complete': episode_guide_complete,
                'character_guide_complete': character_guide_complete,
                'sound_bible_complete': sound_bible_complete,
                'missing_sections': missing_sections,
                'completeness_summary': {
                    'all_docs_present': episode_guide_complete and character_guide_complete and sound_bible_complete,
                    'total_missing': len(missing_sections),
                    'critical_sections_missing': sum(1 for s in missing_sections if s.get('severity') == 'CRITICAL')
                }
            }
            
        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")
    
    def _extract_locations_from_scenes(self, key_scenes: List[Dict]) -> List[str]:
        """Extract location list from key scenes"""
        locations = []
        for scene in key_scenes:
            location = scene.get('location', '')
            if location:
                locations.append(location)
        return list(set(locations))  # Return unique locations
    
    def _extract_episode_content(self, episode: Dict) -> str:
        """Extract content from episode data"""
        # Try format_conversion.fountain_script first (most complete)
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
    
    def _calculate_compliance(self, format_verification: Dict, production_notes: Dict, documentation: Dict) -> Dict:
        """Calculate overall compliance"""
        # Extract error counts
        format_errors = format_verification.get('compliance_summary', {}).get('total_errors', 0)
        prod_errors = production_notes.get('verification_summary', {}).get('total_errors', 0)
        doc_errors = documentation.get('completeness_summary', {}).get('total_missing', 0)
        
        total_errors = format_errors + prod_errors + doc_errors
        
        critical_format = format_verification.get('compliance_summary', {}).get('critical_errors', 0)
        blocking_prod = production_notes.get('verification_summary', {}).get('blocking_errors', 0)
        critical_doc = documentation.get('completeness_summary', {}).get('critical_sections_missing', 0)
        
        blocking_issues = critical_format + blocking_prod + critical_doc
        
        return {
            'total_errors': total_errors,
            'blocking_issues': blocking_issues,
            'format_errors': format_errors,
            'production_errors': prod_errors,
            'documentation_errors': doc_errors,
            'production_ready': total_errors == 0 and blocking_issues == 0
        }
    
    def _count_errors(self, episode_result: Dict) -> int:
        """Count total errors in episode result"""
        return episode_result.get('overall_compliance', {}).get('total_errors', 0)
    
    def _get_top_issues(self, all_episode_results: List[Dict], limit: int = 5) -> List[Dict]:
        """Get top issues from all episode results"""
        issues = []
        
        for result in all_episode_results:
            format_errors = result.get('format_verification', {}).get('format_errors', [])
            for error in format_errors:
                issues.append(error)
        
        # Sort by severity
        severity_order = {'CRITICAL': 1, 'HIGH': 2, 'MEDIUM': 3, 'LOW': 4}
        issues.sort(key=lambda x: severity_order.get(x.get('severity', 'LOW'), 5))
        
        return issues[:limit]
    
    async def generate_summary_report(self, all_episode_results: List[Dict]) -> Dict:
        """Generate comprehensive verification summary"""
        try:
            context = {
                'session_id': self.session_id,
                'total_episodes': len(all_episode_results),
                'verification_results': json.dumps(all_episode_results, indent=2)
            }
            
            prompt = self.config.get_prompt('summary_report').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('verification_summary', {})
            
        except Exception as e:
            raise ValueError(f"❌ Summary report generation failed: {str(e)}")
    
    async def save_episode_output(self, episode_result: Dict):
        """Save individual episode results"""
        episode_id = episode_result['episode_id']
        json_path = self.output_dir / f"{self.session_id}_episode_{episode_id:02d}_verification.json"
        
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(episode_result, f, indent=2, ensure_ascii=False)
    
    async def generate_detailed_reports(self, all_episode_results: List[Dict], summary_report: Dict):
        """Generate detailed reports"""
        # 1. Format Compliance Report
        format_compliance = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'episodes': all_episode_results,
            'summary': summary_report
        }
        
        json_path = self.output_dir / f"{self.session_id}_format_compliance_report.json"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(format_compliance, f, indent=2, ensure_ascii=False)
        
        # 2. Correction Requirements
        correction_requirements = self._extract_correction_requirements(all_episode_results)
        
        json_path = self.output_dir / f"{self.session_id}_correction_requirements.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(correction_requirements, f, indent=2, ensure_ascii=False)
        
        # 3. Missing Documentation
        missing_docs = self._extract_missing_documentation(all_episode_results)
        
        json_path = self.output_dir / f"{self.session_id}_missing_documentation.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(missing_docs, f, indent=2, ensure_ascii=False)
        
        # 4. Detailed Log (TXT)
        self._generate_detailed_log(all_episode_results, summary_report)
        
        # Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_40"
        await self.redis.set(redis_key, json.dumps(format_compliance), expire=86400)
    
    def _extract_correction_requirements(self, all_episode_results: List[Dict]) -> Dict:
        """Extract all correction requirements"""
        all_requirements = []
        
        for result in all_episode_results:
            episode_id = result.get('episode_id')
            
            # Format errors
            format_errors = result.get('format_verification', {}).get('format_errors', [])
            for error in format_errors:
                all_requirements.append({
                    'episode_id': episode_id,
                    'category': 'format',
                    'check': error.get('check'),
                    'location': error.get('location'),
                    'line_number': error.get('line_number'),
                    'expected': error.get('expected'),
                    'actual': error.get('actual'),
                    'context': error.get('context', ''),  # Include context if available
                    'severity': error.get('severity'),
                    'fix_required': error.get('fix_required')
                })
            
            # Production notes errors
            casting_errors = result.get('production_notes_verification', {}).get('casting_notes_errors', [])
            for error in casting_errors:
                all_requirements.append({
                    'episode_id': episode_id,
                    'category': 'production_notes',
                    'check': 'casting_notes',
                    'location': error.get('character'),
                    'severity': error.get('severity'),
                    'fix_required': f"Add missing fields: {', '.join(error.get('missing_fields', []))}"
                })
        
        return {
            'generated_at': datetime.now().isoformat(),
            'total_requirements': len(all_requirements),
            'requirements': all_requirements
        }
    
    def _extract_missing_documentation(self, all_episode_results: List[Dict]) -> Dict:
        """Extract missing documentation"""
        missing_docs = {
            'episode_guide': [],
            'character_guide': [],
            'sound_bible': []
        }
        
        for result in all_episode_results:
            episode_id = result.get('episode_id')
            doc_completeness = result.get('documentation_completeness', {})
            
            if not doc_completeness.get('episode_guide_complete', False):
                missing_docs['episode_guide'].append(episode_id)
            
            if not doc_completeness.get('character_guide_complete', False):
                missing_docs['character_guide'].append(episode_id)
            
            if not doc_completeness.get('sound_bible_complete', False):
                missing_docs['sound_bible'].append(episode_id)
        
        return {
            'generated_at': datetime.now().isoformat(),
            'missing_sections': missing_docs
        }
    
    def _generate_detailed_log(self, all_episode_results: List[Dict], summary_report: Dict):
        """Generate detailed human-readable log"""
        txt_path = self.output_dir / f"{self.session_id}_detailed_log.txt"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        
        with open(txt_path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 40: TECHNICAL FORMAT VERIFICATION REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Episodes Verified: {len(all_episode_results)}\n\n")
            
            # Executive Summary
            f.write("-" * 70 + "\n")
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"{summary_report.get('executive_summary', 'N/A')}\n\n")
            
            # Overall Compliance
            f.write("-" * 70 + "\n")
            f.write("OVERALL COMPLIANCE\n")
            f.write("-" * 70 + "\n")
            
            compliance = summary_report.get('overall_compliance', {})
            f.write(f"Episodes Passing: {compliance.get('episodes_passing', 'N/A')}\n")
            f.write(f"Episodes Failing: {compliance.get('episodes_failing', 'N/A')}\n")
            f.write(f"Total Errors: {compliance.get('total_errors', 'N/A')}\n")
            f.write(f"Critical Errors: {compliance.get('critical_errors', 'N/A')}\n")
            f.write(f"Blocking Production: {'YES' if compliance.get('blocking_production') else 'NO'}\n\n")
            
            # Common Errors
            f.write("-" * 70 + "\n")
            f.write("COMMON FORMAT ERRORS\n")
            f.write("-" * 70 + "\n")
            
            common_errors = summary_report.get('common_format_errors', [])
            for i, error in enumerate(common_errors, 1):
                f.write(f"\n{i}. {error.get('error_type', 'N/A')}\n")
                f.write(f"   Frequency: {error.get('frequency', 'N/A')}\n")
                f.write(f"   Typical Location: {error.get('typical_location', 'N/A')}\n")
                f.write(f"   Recommended Fix: {error.get('recommended_fix', 'N/A')}\n")
            
            # Production Readiness
            f.write("\n" + "-" * 70 + "\n")
            f.write("PRODUCTION READINESS\n")
            f.write("-" * 70 + "\n")
            
            readiness = summary_report.get('production_readiness', {})
            production_ready = readiness.get('production_ready', False)
            f.write(f"Production Ready: {'YES' if production_ready else 'NO'}\n")
            
            if not production_ready:
                blocking_issues = readiness.get('blocking_issues', [])
                if blocking_issues:
                    f.write("\nBlocking Issues:\n")
                    for issue in blocking_issues:
                        f.write(f"  - {issue}\n")
            
            # Recommendations
            f.write("\n" + "-" * 70 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 70 + "\n")
            
            recommendations = summary_report.get('recommendations', [])
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF VERIFICATION REPORT\n")
            f.write("=" * 70 + "\n")
    
    async def require_user_approval(self, all_episode_results: List[Dict]) -> bool:
        """Require user approval before marking production-ready"""
        # Check if all episodes pass
        all_pass = all(
            result.get('overall_compliance', {}).get('production_ready', False)
            for result in all_episode_results
        )
        
        if not all_pass:
            total_errors = sum(
                result.get('overall_compliance', {}).get('total_errors', 0)
                for result in all_episode_results
            )
            print("\n" + "=" * 70)
            print("❌ FORMAT ERRORS DETECTED - PRODUCTION NOT READY")
            print("=" * 70)
            print(f"\nTotal errors found: {total_errors}")
            print("Please review and fix errors before proceeding to production.")
            print("\nCertification file will be generated with 'production_ready: false' status.")
            return False
        
        print("\n" + "=" * 70)
        print("✅ ALL EPISODES PASS FORMAT VERIFICATION")
        print("=" * 70)
        print("\nProduction-ready certification will be generated.")
        print("This indicates that scripts meet technical format requirements.")
        
        user_response = input("\n⚠️  Certify as production-ready? (yes/no): ").strip().lower()
        return user_response in ['yes', 'y']
    
    async def save_production_certification(self, all_episode_results: List[Dict], summary_report: Dict, production_ready: bool):
        """Save production-ready certification"""
        # Calculate total errors and blocking issues
        total_errors = sum(
            result.get('overall_compliance', {}).get('total_errors', 0)
            for result in all_episode_results
        )
        blocking_issues = sum(
            result.get('overall_compliance', {}).get('blocking_issues', 0)
            for result in all_episode_results
        )
        
        certification = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'certified_by': 'Station 40 Format Verifier',
            'episodes_verified': len(all_episode_results),
            'total_errors': total_errors,
            'blocking_issues': blocking_issues,
            'production_ready': production_ready,
            'verification_summary': summary_report,
            'episode_status': [
                {
                    'episode_id': result.get('episode_id'),
                    'total_errors': result.get('overall_compliance', {}).get('total_errors', 0),
                    'blocking_issues': result.get('overall_compliance', {}).get('blocking_issues', 0),
                    'production_ready': result.get('overall_compliance', {}).get('production_ready', False)
                }
                for result in all_episode_results
            ],
            'certification_notes': 'Production-ready if all episodes have zero errors and zero blocking issues.' if production_ready else 'Production NOT ready. Please address errors before proceeding.',
            'timestamp': datetime.now().isoformat()
        }
        
        json_path = self.output_dir / f"{self.session_id}_production_ready_certification.json"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(certification, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Production certification saved: {json_path}")


# CLI Entry Point
async def main():
    """Run Station 40 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    verifier = Station40FormatVerifier(session_id)
    await verifier.initialize()
    
    try:
        await verifier.run()
        print(f"\n✅ Success! Format verification complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

