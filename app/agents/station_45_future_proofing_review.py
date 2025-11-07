"""
Station 45: Future-Proofing Review

This station performs the final future-proofing review to ensure content longevity,
adaptation potential, proper archival, and legacy documentation.

Flow:
1. Load Station 44 complete package
2. Load all supporting data
3. Execute 4-task future-proofing sequence:
   - Task 1: Timelessness Check (dating factors)
   - Task 2: Adaptation Potential (international, expansion, format)
   - Task 3: Archive Preparation (documentation, rights, preservation)
   - Task 4: Legacy Notes (creator intent, production notes, audience)
4. Generate future-proofing report
5. Create legacy archive
6. Save comprehensive recommendations

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config
- FAIL FAST - Exit on missing dependencies with actionable messages
- Long-term thinking - consider 5-10 year horizon
- Comprehensive documentation for future teams
- Explicit error messages with file names, line numbers
- Consistent logging to logs/station_45.log
"""

import asyncio
import json
import logging
import shutil
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
log_file = log_dir / "station_45.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Station45FutureProofingReview:
    """Station 45: Future-Proofing Review"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=45)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output_path', 'output/station_45'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Validate required config fields
        self._validate_config()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_45.yml'

        if not config_path.exists():
            raise FileNotFoundError(f"❌ Station 45 config file not found: {config_path}")

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
        logger.info("✅ Station 45 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🔮 STATION 45: FUTURE-PROOFING REVIEW")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station44_data = await self.load_station44_data()
            supporting_data = await self.load_supporting_data()

            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 44: Complete package loaded")
            print(f"   ✓ Supporting data from multiple stations")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station44_data, supporting_data)

            # Step 3: Execute 4-task future-proofing review
            print("\n🔮 Beginning future-proofing review...")
            print("-" * 70)

            # Task 1: Timelessness Check
            print("\n⏳ Task 1/4: Timelessness Check...")
            timelessness = await self.execute_task1_timelessness_check(
                station44_data, supporting_data
            )
            print("   ✅ Timelessness check complete")

            # Task 2: Adaptation Potential
            print("\n🌍 Task 2/4: Adaptation Potential...")
            adaptation = await self.execute_task2_adaptation_potential(
                station44_data, supporting_data
            )
            print("   ✅ Adaptation potential assessed")

            # Task 3: Archive Preparation
            print("\n📦 Task 3/4: Archive Preparation...")
            archive = await self.execute_task3_archive_preparation(
                station44_data, supporting_data
            )
            print("   ✅ Archive preparation verified")

            # Task 4: Legacy Notes
            print("\n📜 Task 4/4: Legacy Notes...")
            legacy = await self.execute_task4_legacy_notes(
                station44_data, supporting_data
            )
            print("   ✅ Legacy documentation created")

            # Step 4: Generate future-proofing reports
            print("\n📊 Generating future-proofing reports...")
            print("-" * 70)

            await self.generate_future_proofing_reports(
                timelessness, adaptation, archive, legacy,
                station44_data, supporting_data
            )

            print("\n" + "=" * 70)
            print("✅ FUTURE-PROOFING REVIEW COMPLETE")
            print("=" * 70)
            print(f"\n📁 Output directory: {self.output_dir}")
            print(f"📄 Future-proofing reports generated")

            # Display summary
            self.display_review_summary(timelessness, adaptation, archive, legacy)

        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            raise
        except Exception as e:
            logger.error(f"Station 45 failed: {str(e)}")
            print(f"\n❌ Error: {str(e)}")
            raise

    async def load_station44_data(self) -> Dict:
        """Load complete package from Station 44"""
        try:
            station_44_path = Path(self.config_data.get('input_path', 'output/station_44'))

            if not station_44_path.exists():
                raise ValueError(
                    f"❌ Station 44 directory not found: {station_44_path}\n"
                    "   Please run Station 44 (Package Assembly) first"
                )

            # Find the package directory
            package_dirs = [d for d in station_44_path.iterdir() if d.is_dir() and 'Final_Package' in d.name]

            if not package_dirs:
                raise ValueError(
                    f"❌ No package found in {station_44_path}\n"
                    "   Please run Station 44 (Package Assembly) first"
                )

            # Use the most recent package
            package_dir = max(package_dirs, key=lambda p: p.stat().st_mtime)

            # Load package contents
            package_data = {
                'package_path': str(package_dir),
                'scripts': {},
                'documentation': {},
                'tracking': {}
            }

            # Load scripts
            scripts_dir = package_dir / '01_Scripts'
            if scripts_dir.exists():
                master_scripts_file = scripts_dir / 'master_scripts.json'
                if master_scripts_file.exists():
                    with open(master_scripts_file, 'r', encoding='utf-8') as f:
                        package_data['scripts'] = json.load(f)

            # Load documentation
            docs_dir = package_dir / '02_Documentation'
            if docs_dir.exists():
                for doc_file in docs_dir.glob('*.json'):
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        package_data['documentation'][doc_file.stem] = json.load(f)

            # Load tracking
            tracking_dir = package_dir / '03_Tracking'
            if tracking_dir.exists():
                for track_file in tracking_dir.glob('*.json'):
                    with open(track_file, 'r', encoding='utf-8') as f:
                        package_data['tracking'][track_file.stem] = json.load(f)

            logger.info(f"Loaded complete package from {package_dir}")
            return package_data

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing package data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading package: {str(e)}")

    async def load_supporting_data(self) -> Dict:
        """Load supporting data from earlier stations"""
        supporting_data = {}

        station_mappings = {
            'station_2': 'output/station_02',   # Project DNA
            'station_8': 'output/station_08',   # Character Architect
            'station_9': 'output/station_09',   # World Builder
            'station_43': 'output/station_43'   # Final Polish
        }

        for station_key, station_path in station_mappings.items():
            try:
                station_dir = Path(station_path)
                if station_dir.exists():
                    station_files = list(station_dir.glob("*.json"))
                    if station_files:
                        latest_file = max(station_files, key=lambda p: p.stat().st_mtime)
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            supporting_data[station_key] = json.load(f)
                        logger.info(f"Loaded {station_key} from {latest_file}")
            except Exception as e:
                logger.warning(f"Could not load {station_key}: {str(e)}")

        return supporting_data

    def display_project_summary(self, station44_data: Dict, supporting_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)

        package_path = station44_data.get('package_path', 'Unknown')
        print(f"Package Path: {package_path}")
        print(f"Scripts Loaded: {'✓' if station44_data.get('scripts') else '✗'}")
        print(f"Documentation Loaded: {'✓' if station44_data.get('documentation') else '✗'}")
        print(f"Tracking Loaded: {'✓' if station44_data.get('tracking') else '✗'}")
        print()
        print(f"Supporting Data Available:")
        print(f"   • Station 2 (Project DNA): {'✓' if 'station_2' in supporting_data else '✗'}")
        print(f"   • Station 8 (Characters): {'✓' if 'station_8' in supporting_data else '✗'}")
        print(f"   • Station 9 (World): {'✓' if 'station_9' in supporting_data else '✗'}")
        print(f"   • Station 43 (Polish): {'✓' if 'station_43' in supporting_data else '✗'}")

        print("-" * 70)

    async def execute_task1_timelessness_check(self, station44_data: Dict,
                                                supporting_data: Dict) -> Dict:
        """Task 1: Timelessness Check - Review for dating factors"""
        try:
            # Prepare scripts summary
            scripts = station44_data.get('scripts', {})
            all_scripts = json.dumps(scripts, indent=2)[:5000]  # Limit for prompt

            context = {
                'session_id': self.session_id,
                'complete_package': json.dumps(station44_data, indent=2)[:3000],
                'all_scripts': all_scripts,
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2)
            }

            prompt = self.config.get_prompt('timelessness_check').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('timelessness_check', {})

        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_adaptation_potential(self, station44_data: Dict,
                                                  supporting_data: Dict) -> Dict:
        """Task 2: Adaptation Potential - Consider future possibilities"""
        try:
            context = {
                'session_id': self.session_id,
                'complete_package': json.dumps(station44_data, indent=2)[:3000],
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2),
                'character_bible': json.dumps(supporting_data.get('station_8', {}), indent=2),
                'world_bible': json.dumps(supporting_data.get('station_9', {}), indent=2)
            }

            prompt = self.config.get_prompt('adaptation_potential').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('adaptation_potential', {})

        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_archive_preparation(self, station44_data: Dict,
                                                 supporting_data: Dict) -> Dict:
        """Task 3: Archive Preparation - Prepare for long-term storage"""
        try:
            # Get revision history from tracking data
            tracking = station44_data.get('tracking', {})
            revision_history = tracking.get('Change_Log', {})

            context = {
                'session_id': self.session_id,
                'complete_package': json.dumps(station44_data, indent=2)[:3000],
                'revision_history': json.dumps(revision_history, indent=2)
            }

            prompt = self.config.get_prompt('archive_preparation').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('archive_preparation', {})

        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_legacy_notes(self, station44_data: Dict,
                                         supporting_data: Dict) -> Dict:
        """Task 4: Legacy Notes - Create future reference documentation"""
        try:
            # Gather all production notes
            production_notes = {
                'documentation': station44_data.get('documentation', {}),
                'tracking': station44_data.get('tracking', {})
            }

            context = {
                'session_id': self.session_id,
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2),
                'production_notes': json.dumps(production_notes, indent=2)[:5000]
            }

            prompt = self.config.get_prompt('legacy_notes').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('legacy_notes', {})

        except Exception as e:
            logger.error(f"Task 4 failed: {str(e)}")
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    async def generate_future_proofing_reports(self, timelessness: Dict, adaptation: Dict,
                                                archive: Dict, legacy: Dict,
                                                station44_data: Dict, supporting_data: Dict):
        """Generate comprehensive future-proofing reports"""
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')

        # 1. Complete JSON report
        complete_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'timelessness_check': timelessness,
            'adaptation_potential': adaptation,
            'archive_preparation': archive,
            'legacy_notes': legacy,
            'overall_assessment': self._calculate_overall_assessment(
                timelessness, adaptation, archive, legacy
            )
        }

        json_path = self.output_dir / f"{self.session_id}_future_proofing_report.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(complete_report, f, indent=2, ensure_ascii=False)

        print(f"   ✓ Generated JSON report")

        # 2. Human-readable summary
        self._generate_summary_report(complete_report, encoding)
        print(f"   ✓ Generated summary report")

        # 3. Legacy archive
        if self.config_data.get('output_enhancements', {}).get('generate_legacy_archive', True):
            self._generate_legacy_archive(legacy, station44_data, encoding)
            print(f"   ✓ Generated legacy archive")

        # 4. Adaptation guide
        self._generate_adaptation_guide(adaptation, encoding)
        print(f"   ✓ Generated adaptation guide")

        # 5. Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_45"
        await self.redis.set(redis_key, json.dumps({
            'future_proof_score': complete_report['overall_assessment']['overall_score'],
            'adaptation_ready': complete_report['overall_assessment']['adaptation_ready'],
            'archive_ready': complete_report['overall_assessment']['archive_ready']
        }), expire=86400)

    def _calculate_overall_assessment(self, timelessness: Dict, adaptation: Dict,
                                       archive: Dict, legacy: Dict) -> Dict:
        """Calculate overall future-proofing assessment"""
        timelessness_score = timelessness.get('overall_score', 0.0)
        adaptation_score = adaptation.get('overall_score', 0.0)
        archive_score = archive.get('overall_score', 0.0)
        legacy_score = legacy.get('overall_completion', 0.0)

        overall_score = (timelessness_score + adaptation_score + archive_score + legacy_score) / 4

        return {
            'overall_score': overall_score,
            'timelessness_rating': timelessness.get('overall_rating', 'UNKNOWN'),
            'adaptation_rating': adaptation.get('overall_rating', 'UNKNOWN'),
            'archive_rating': archive.get('overall_rating', 'UNKNOWN'),
            'legacy_completion': legacy_score,
            'future_proof': overall_score >= 0.7,
            'adaptation_ready': adaptation_score >= 0.6,
            'archive_ready': archive_score >= 0.8,
            'projected_shelf_life': timelessness.get('projected_shelf_life_years', 0),
            'recommendations': self._compile_recommendations(timelessness, adaptation, archive)
        }

    def _compile_recommendations(self, timelessness: Dict, adaptation: Dict,
                                  archive: Dict) -> List[str]:
        """Compile all recommendations from tasks"""
        recommendations = []

        # Timelessness recommendations
        for category in ['technology_references', 'cultural_references', 'temporal_markers', 'sound_choices']:
            category_data = timelessness.get(category, {})
            recs = category_data.get('recommendations', [])
            recommendations.extend(recs)

        # Adaptation recommendations
        adapt_recs = adaptation.get('recommended_next_steps', [])
        recommendations.extend(adapt_recs)

        # Archive recommendations
        archive_recs = archive.get('archival_recommendations', [])
        recommendations.extend(archive_recs)

        return recommendations[:10]  # Top 10 recommendations

    def _generate_summary_report(self, complete_report: Dict, encoding: str):
        """Generate human-readable summary report"""
        txt_path = self.output_dir / f"{self.session_id}_future_proofing_summary.txt"

        with open(txt_path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 45: FUTURE-PROOFING REVIEW SUMMARY\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            # Overall Assessment
            assessment = complete_report['overall_assessment']
            f.write("-" * 70 + "\n")
            f.write("OVERALL ASSESSMENT\n")
            f.write("-" * 70 + "\n\n")
            f.write(f"Overall Score: {assessment['overall_score']:.2f}/1.00\n")
            f.write(f"Future-Proof: {'✓ YES' if assessment['future_proof'] else '✗ NEEDS WORK'}\n")
            f.write(f"Adaptation Ready: {'✓ YES' if assessment['adaptation_ready'] else '✗ NEEDS WORK'}\n")
            f.write(f"Archive Ready: {'✓ YES' if assessment['archive_ready'] else '✗ NEEDS WORK'}\n")
            f.write(f"Projected Shelf Life: {assessment['projected_shelf_life']} years\n\n")

            # Timelessness
            timelessness = complete_report['timelessness_check']
            f.write("-" * 70 + "\n")
            f.write("TIMELESSNESS CHECK\n")
            f.write("-" * 70 + "\n\n")
            f.write(f"Rating: {timelessness.get('overall_rating', 'UNKNOWN')}\n")
            f.write(f"Score: {timelessness.get('overall_score', 0.0):.2f}/1.00\n\n")

            critical_issues = timelessness.get('critical_issues', [])
            if critical_issues:
                f.write("Critical Issues:\n")
                for issue in critical_issues[:5]:
                    f.write(f"  • {issue.get('issue', 'Unknown')}\n")
                f.write("\n")

            # Adaptation Potential
            adaptation = complete_report['adaptation_potential']
            f.write("-" * 70 + "\n")
            f.write("ADAPTATION POTENTIAL\n")
            f.write("-" * 70 + "\n\n")
            f.write(f"Rating: {adaptation.get('overall_rating', 'UNKNOWN')}\n")
            f.write(f"Score: {adaptation.get('overall_score', 0.0):.2f}/1.00\n\n")

            # Archive Preparation
            archive = complete_report['archive_preparation']
            f.write("-" * 70 + "\n")
            f.write("ARCHIVE PREPARATION\n")
            f.write("-" * 70 + "\n\n")
            f.write(f"Rating: {archive.get('overall_rating', 'UNKNOWN')}\n")
            f.write(f"Archival Quality: {archive.get('archival_quality', 'UNKNOWN')}\n\n")

            # Top Recommendations
            f.write("-" * 70 + "\n")
            f.write("TOP RECOMMENDATIONS\n")
            f.write("-" * 70 + "\n\n")
            for i, rec in enumerate(assessment.get('recommendations', [])[:10], 1):
                f.write(f"{i}. {rec}\n")

            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF SUMMARY\n")
            f.write("=" * 70 + "\n")

    def _generate_legacy_archive(self, legacy: Dict, station44_data: Dict, encoding: str):
        """Generate legacy archive document"""
        legacy_path = self.output_dir / f"{self.session_id}_LEGACY_ARCHIVE.txt"

        legacy_doc = legacy.get('future_reference_document', '')
        time_capsule = legacy.get('time_capsule_summary', '')

        with open(legacy_path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("LEGACY ARCHIVE\n")
            f.write("Audio Series Production - Future Reference\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Created: {datetime.now().isoformat()}\n")
            f.write(f"Session: {self.session_id}\n\n")

            f.write("-" * 70 + "\n")
            f.write("TIME CAPSULE SUMMARY\n")
            f.write("-" * 70 + "\n\n")
            f.write(time_capsule + "\n\n")

            f.write("-" * 70 + "\n")
            f.write("COMPLETE LEGACY DOCUMENTATION\n")
            f.write("-" * 70 + "\n\n")
            f.write(legacy_doc + "\n\n")

            f.write("=" * 70 + "\n")
            f.write("END OF LEGACY ARCHIVE\n")
            f.write("=" * 70 + "\n")

    def _generate_adaptation_guide(self, adaptation: Dict, encoding: str):
        """Generate adaptation guide"""
        guide_path = self.output_dir / f"{self.session_id}_adaptation_guide.json"

        with open(guide_path, 'w', encoding=encoding) as f:
            json.dump({
                'adaptation_potential': adaptation,
                'recommended_formats': self._extract_recommended_formats(adaptation),
                'international_markets': self._extract_target_markets(adaptation),
                'expansion_opportunities': self._extract_expansions(adaptation)
            }, f, indent=2, ensure_ascii=False)

    def _extract_recommended_formats(self, adaptation: Dict) -> List[Dict]:
        """Extract recommended adaptation formats"""
        formats = []
        format_flex = adaptation.get('format_flexibility', {})

        visual = format_flex.get('visual_adaptation', {})
        if visual.get('feasible'):
            formats.append({
                'format': visual.get('best_format', 'VISUAL'),
                'feasibility': 'HIGH',
                'notes': visual.get('strengths', [])
            })

        stage = format_flex.get('stage_adaptation', {})
        if stage.get('feasible'):
            formats.append({
                'format': stage.get('format', 'STAGE'),
                'feasibility': 'MEDIUM',
                'notes': stage.get('strengths', [])
            })

        return formats

    def _extract_target_markets(self, adaptation: Dict) -> List[str]:
        """Extract target markets"""
        intl = adaptation.get('international_potential', {})
        markets = intl.get('target_markets', [])
        return [m.get('market', 'Unknown') for m in markets if m.get('appeal') in ['HIGH', 'MEDIUM']]

    def _extract_expansions(self, adaptation: Dict) -> List[str]:
        """Extract expansion opportunities"""
        expansion = adaptation.get('expansion_potential', {})
        return expansion.get('expansion_directions', [])

    def display_review_summary(self, timelessness: Dict, adaptation: Dict,
                                archive: Dict, legacy: Dict):
        """Display review summary"""
        print("\n" + "=" * 70)
        print("📊 FUTURE-PROOFING SUMMARY")
        print("=" * 70)

        print(f"\n⏳ Timelessness: {timelessness.get('overall_rating', 'UNKNOWN')}")
        print(f"   Shelf Life: {timelessness.get('projected_shelf_life_years', 0)} years")

        print(f"\n🌍 Adaptation: {adaptation.get('overall_rating', 'UNKNOWN')}")
        print(f"   Best Format: {adaptation.get('format_flexibility', {}).get('best_adaptation_path', 'TBD')}")

        print(f"\n📦 Archive: {archive.get('overall_rating', 'UNKNOWN')}")
        print(f"   Quality: {archive.get('archival_quality', 'UNKNOWN')}")

        print(f"\n📜 Legacy: {legacy.get('overall_completion', 0.0):.0%} Complete")

        print("\n" + "=" * 70)


# CLI Entry Point
async def main():
    """Run Station 45 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()

    if not session_id:
        print("❌ Session ID required")
        return

    future_proofing = Station45FutureProofingReview(session_id)
    await future_proofing.initialize()

    try:
        await future_proofing.run()
        print(f"\n✅ Success! Future-proofing review complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
