"""
Station 44: Package Assembly

This station assembles the final delivery package for audio series production,
organizing all materials into production-ready formats for different teams.

Flow:
1. Load Station 43 polished scripts (all episodes)
2. Load all supporting documentation (Stations 2, 5, 6, 7, 8, 9, 37, 41)
3. Execute 4-task assembly sequence:
   - Task 1: Master Script Package (multiple script versions)
   - Task 2: Documentation Package (bibles and guides)
   - Task 3: Tracking Documents (episode guide, plant/payoff matrix, dependencies)
   - Task 4: Delivery Preparation (file organization and packaging)
4. Generate complete delivery package
5. Create folder structure and manifests
6. Save all package materials

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config
- FAIL FAST - Exit on missing dependencies with actionable messages
- Professional packaging for production teams
- Maintain comprehensive documentation
- Explicit error messages with file names, line numbers
- Consistent logging to logs/station_44.log
"""

import asyncio
import json
import logging
import os
import shutil
import zipfile
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
log_file = log_dir / "station_44.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Station44PackageAssembly:
    """Station 44: Package Assembly"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=44)

        # Load additional config from YAML
        self._load_additional_config()

        self.output_dir = Path(self.config_data.get('output_path', 'output/station_44'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create package root directory
        self.package_root = self.output_dir / f"{self.session_id}_Final_Package"

        # Validate required config fields
        self._validate_config()

    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_44.yml'

        if not config_path.exists():
            raise FileNotFoundError(f"❌ Station 44 config file not found: {config_path}")

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
        logger.info("✅ Station 44 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("📦 STATION 44: PACKAGE ASSEMBLY")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station43_data = await self.load_station43_data()
            supporting_data = await self.load_supporting_data()

            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 43: {len(station43_data.get('episodes', {}))} polished episodes")
            print(f"   ✓ Supporting data loaded from multiple stations")
            print()

            # Step 2: Display project summary
            episodes = station43_data.get('episodes', {})
            self.display_project_summary(episodes, supporting_data)

            # Step 3: Execute 4-task package assembly
            print("\n📦 Beginning package assembly...")
            print("-" * 70)

            # Task 1: Master Script Package
            print("\n📝 Task 1/4: Master Script Package...")
            master_scripts = await self.execute_task1_master_script_package(
                episodes, supporting_data
            )
            print("   ✅ Master script package complete")

            # Task 2: Documentation Package
            print("\n📚 Task 2/4: Documentation Package...")
            documentation = await self.execute_task2_documentation_package(
                episodes, supporting_data
            )
            print("   ✅ Documentation package complete")

            # Task 3: Tracking Documents
            print("\n📊 Task 3/4: Tracking Documents...")
            tracking = await self.execute_task3_tracking_documents(
                episodes, supporting_data
            )
            print("   ✅ Tracking documents complete")

            # Task 4: Delivery Preparation
            print("\n📤 Task 4/4: Delivery Preparation...")
            delivery = await self.execute_task4_delivery_preparation(
                master_scripts, documentation, tracking, episodes, supporting_data
            )
            print("   ✅ Delivery preparation complete")

            # Step 4: Generate physical package
            print("\n📁 Generating physical package structure...")
            print("-" * 70)

            await self.generate_physical_package(
                master_scripts, documentation, tracking, delivery, episodes
            )

            print("\n" + "=" * 70)
            print("✅ PACKAGE ASSEMBLY COMPLETE")
            print("=" * 70)
            print(f"\n📁 Package directory: {self.package_root}")
            print(f"📄 Total files generated: [calculated during generation]")

            # Display package contents
            self.display_package_contents()

        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            raise
        except Exception as e:
            logger.error(f"Station 44 failed: {str(e)}")
            print(f"\n❌ Error: {str(e)}")
            raise

    async def load_station43_data(self) -> Dict:
        """Load all polished episodes from Station 43"""
        try:
            station_43_path = Path(self.config_data.get('input_path', 'output/station_43'))

            if not station_43_path.exists():
                raise ValueError(
                    f"❌ Station 43 directory not found: {station_43_path}\n"
                    "   Please run Station 43 (Final Polish Pass) first"
                )

            episodes = {}

            # Load all polished episodes from directory
            for episode_dir in station_43_path.iterdir():
                if episode_dir.is_dir() and episode_dir.name.startswith("episode_"):
                    try:
                        episode_num = int(episode_dir.name.split("_")[1])
                        json_file = episode_dir / f"episode_{episode_num:02d}_POLISHED.json"

                        if json_file.exists():
                            with open(json_file, 'r', encoding='utf-8') as f:
                                episode_data = json.load(f)
                                episodes[episode_num] = episode_data
                    except (ValueError, KeyError, json.JSONDecodeError) as e:
                        logger.warning(f"Skipping episode: {str(e)}")
                        continue

            if not episodes:
                raise ValueError(
                    f"❌ No polished episodes found in {station_43_path}\n"
                    "   Please run Station 43 (Final Polish Pass) first"
                )

            # Sort episodes by number
            episodes = dict(sorted(episodes.items()))

            logger.info(f"Loaded {len(episodes)} polished episodes from {station_43_path}")
            return {'episodes': episodes}

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing episode data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading station data: {str(e)}")

    async def load_supporting_data(self) -> Dict:
        """Load supporting data from earlier stations"""
        supporting_data = {}

        # Try to load from file system
        station_mappings = {
            'station_2': 'output/station_02',   # Project DNA
            'station_5': 'output/station_05',   # Season Architecture
            'station_6': 'output/station_06',   # Style Guide
            'station_7': 'output/station_07',   # Character Architect
            'station_8': 'output/station_08',   # World Builder
            'station_9': 'output/station_09',   # World Building System
            'station_37': 'output/station_37',  # Plant/Payoff Tracker
            'station_41': 'output/station_41'   # Cross-Episode Dependencies
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

    def display_project_summary(self, episodes: Dict, supporting_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)

        print(f"Total Episodes: {len(episodes)}")
        print(f"Supporting Data Available:")
        print(f"   • Station 2 (Project DNA): {'✓' if 'station_2' in supporting_data else '✗'}")
        print(f"   • Station 5 (Season Architecture): {'✓' if 'station_5' in supporting_data else '✗'}")
        print(f"   • Station 6 (Style Guide): {'✓' if 'station_6' in supporting_data else '✗'}")
        print(f"   • Station 7 (Characters): {'✓' if 'station_7' in supporting_data else '✗'}")
        print(f"   • Station 8 (World): {'✓' if 'station_8' in supporting_data else '✗'}")
        print(f"   • Station 37 (Plant/Payoff): {'✓' if 'station_37' in supporting_data else '✗'}")
        print(f"   • Station 41 (Dependencies): {'✓' if 'station_41' in supporting_data else '✗'}")
        print()

        if episodes:
            print("Episode List:")
            for episode_num, episode_data in sorted(episodes.items()):
                production_ready = episode_data.get('production_ready', False)
                status = "✓ READY" if production_ready else "✗ ISSUES"
                print(f"   • Episode {episode_num}: {status}")

        print("-" * 70)

    async def execute_task1_master_script_package(self, episodes: Dict,
                                                  supporting_data: Dict) -> Dict:
        """Task 1: Master Script Package - Create multiple script versions"""
        try:
            # Prepare polished scripts data
            polished_scripts = {}
            for ep_num, ep_data in episodes.items():
                polish_results = ep_data.get('polish_results', {})
                precision_editing = polish_results.get('precision_editing', {})
                polished_text = precision_editing.get('polished_script_text', '')

                if not polished_text:
                    # Fallback to original script
                    original = ep_data.get('original_script', {})
                    polished_text = self._extract_episode_content(original)

                polished_scripts[ep_num] = polished_text

            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'polished_scripts': json.dumps(polished_scripts, indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2),
                'style_guide': json.dumps(supporting_data.get('station_6', {}), indent=2),
                'character_bible': json.dumps(supporting_data.get('station_7', {}), indent=2)
            }

            prompt = self.config.get_prompt('master_script_package').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('master_script_package', {})

        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_documentation_package(self, episodes: Dict,
                                                   supporting_data: Dict) -> Dict:
        """Task 2: Documentation Package - Compile support materials"""
        try:
            context = {
                'session_id': self.session_id,
                'master_scripts': json.dumps({'episode_count': len(episodes)}, indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2),
                'style_guide': json.dumps(supporting_data.get('station_6', {}), indent=2),
                'character_bible': json.dumps(supporting_data.get('station_7', {}), indent=2),
                'world_bible': json.dumps(supporting_data.get('station_8', {}), indent=2),
                'season_architecture': json.dumps(supporting_data.get('station_5', {}), indent=2)
            }

            prompt = self.config.get_prompt('documentation_package').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('documentation_package', {})

        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_tracking_documents(self, episodes: Dict,
                                               supporting_data: Dict) -> Dict:
        """Task 3: Tracking Documents - Create production management docs"""
        try:
            # Prepare episode summaries
            all_episodes = []
            for ep_num, ep_data in sorted(episodes.items()):
                all_episodes.append({
                    'episode_number': ep_num,
                    'production_ready': ep_data.get('production_ready', False)
                })

            context = {
                'session_id': self.session_id,
                'all_episodes': json.dumps(all_episodes, indent=2),
                'plant_payoff_data': json.dumps(supporting_data.get('station_37', {}), indent=2),
                'dependency_data': json.dumps(supporting_data.get('station_41', {}), indent=2),
                'revision_history': json.dumps({'source': 'station_43_polish'}, indent=2)
            }

            prompt = self.config.get_prompt('tracking_documents').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('tracking_documents', {})

        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_delivery_preparation(self, master_scripts: Dict,
                                                 documentation: Dict,
                                                 tracking: Dict,
                                                 episodes: Dict,
                                                 supporting_data: Dict) -> Dict:
        """Task 4: Delivery Preparation - Organize final package"""
        try:
            # Get project title from Project DNA
            project_dna = supporting_data.get('station_2', {})
            project_title = project_dna.get('project_bible', {}).get('working_title', 'AudioSeries')

            all_packages = {
                'master_scripts': master_scripts,
                'documentation': documentation,
                'tracking': tracking
            }

            context = {
                'session_id': self.session_id,
                'project_title': project_title,
                'all_packages': json.dumps(all_packages, indent=2)
            }

            prompt = self.config.get_prompt('delivery_preparation').format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data.get('delivery_preparation', {})

        except Exception as e:
            logger.error(f"Task 4 failed: {str(e)}")
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    def _extract_episode_content(self, episode: Dict) -> str:
        """Extract content from episode data"""
        # Try various possible locations
        format_conv = episode.get('format_conversion', {})
        fountain_script = format_conv.get('fountain_script', '')
        if fountain_script and fountain_script.strip():
            return fountain_script

        markdown_script = format_conv.get('markdown_script', '')
        if markdown_script and markdown_script.strip():
            return markdown_script

        master_text = episode.get('master_script_assembly', {}).get('master_script_text', '')
        if master_text and master_text.strip():
            return master_text

        return ''

    async def generate_physical_package(self, master_scripts: Dict, documentation: Dict,
                                       tracking: Dict, delivery: Dict, episodes: Dict):
        """Generate physical package structure on filesystem"""

        # Create root package directory
        self.package_root.mkdir(parents=True, exist_ok=True)
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')

        # 1. Create folder structure
        folders = {
            '01_Scripts': self.package_root / '01_Scripts',
            '02_Documentation': self.package_root / '02_Documentation',
            '03_Tracking': self.package_root / '03_Tracking',
            '04_Audio_Specs': self.package_root / '04_Audio_Specs'
        }

        for folder_path in folders.values():
            folder_path.mkdir(parents=True, exist_ok=True)

        print(f"   ✓ Created folder structure")

        # 2. Generate Scripts
        scripts_dir = folders['01_Scripts']

        # Master scripts
        master_script_data = master_scripts.get('master_scripts', {})
        for episode in master_script_data.get('episodes', []):
            ep_num = episode.get('episode_number', 0)
            script_text = episode.get('script_text', '')

            script_file = scripts_dir / f"Episode_{ep_num:02d}_MASTER.txt"
            with open(script_file, 'w', encoding=encoding) as f:
                f.write(script_text)

        # Save master scripts JSON
        with open(scripts_dir / 'master_scripts.json', 'w', encoding=encoding) as f:
            json.dump(master_scripts, f, indent=2, ensure_ascii=False)

        print(f"   ✓ Generated script files")

        # 3. Generate Documentation
        docs_dir = folders['02_Documentation']

        # Series Bible
        series_bible = documentation.get('series_bible', {})
        with open(docs_dir / 'Series_Bible.json', 'w', encoding=encoding) as f:
            json.dump(series_bible, f, indent=2, ensure_ascii=False)

        with open(docs_dir / 'Series_Bible.txt', 'w', encoding=encoding) as f:
            f.write(series_bible.get('series_overview', 'Series Bible'))

        # Character Bible
        character_bible = documentation.get('character_bible', {})
        with open(docs_dir / 'Character_Bible.json', 'w', encoding=encoding) as f:
            json.dump(character_bible, f, indent=2, ensure_ascii=False)

        # World Bible
        world_bible = documentation.get('world_bible', {})
        with open(docs_dir / 'World_Bible.json', 'w', encoding=encoding) as f:
            json.dump(world_bible, f, indent=2, ensure_ascii=False)

        # Production Bible
        production_bible = documentation.get('production_bible', {})
        with open(docs_dir / 'Production_Bible.json', 'w', encoding=encoding) as f:
            json.dump(production_bible, f, indent=2, ensure_ascii=False)

        print(f"   ✓ Generated documentation files")

        # 4. Generate Tracking Documents
        tracking_dir = folders['03_Tracking']

        # Episode Guide
        episode_guide = tracking.get('episode_guide', {})
        with open(tracking_dir / 'Episode_Guide.json', 'w', encoding=encoding) as f:
            json.dump(episode_guide, f, indent=2, ensure_ascii=False)

        # Plant/Payoff Matrix
        plant_payoff = tracking.get('plant_payoff_matrix', {})
        with open(tracking_dir / 'Plant_Payoff_Matrix.json', 'w', encoding=encoding) as f:
            json.dump(plant_payoff, f, indent=2, ensure_ascii=False)

        # Dependency Chart
        dependencies = tracking.get('dependency_chart', {})
        with open(tracking_dir / 'Dependency_Chart.json', 'w', encoding=encoding) as f:
            json.dump(dependencies, f, indent=2, ensure_ascii=False)

        # Change Log
        change_log = tracking.get('change_log', {})
        with open(tracking_dir / 'Change_Log.json', 'w', encoding=encoding) as f:
            json.dump(change_log, f, indent=2, ensure_ascii=False)

        print(f"   ✓ Generated tracking documents")

        # 5. Generate README files
        self._generate_readme_files(folders, delivery)

        print(f"   ✓ Generated README files")

        # 6. Generate Cover Letter
        cover_letter = delivery.get('cover_letter', {})
        cover_letter_text = cover_letter.get('letter_text', '')
        with open(self.package_root / 'COVER_LETTER.txt', 'w', encoding=encoding) as f:
            f.write(cover_letter_text)

        print(f"   ✓ Generated cover letter")

        # 7. Generate File Manifest
        self._generate_file_manifest(delivery)

        print(f"   ✓ Generated file manifest")

        # 8. Create ZIP archive
        if self.config_data.get('output_enhancements', {}).get('create_folder_structure', True):
            zip_path = self.output_dir / f"{self.session_id}_Complete_Package.zip"
            self._create_zip_archive(self.package_root, zip_path)
            print(f"   ✓ Created ZIP archive: {zip_path.name}")

        # 9. Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_44"
        await self.redis.set(redis_key, json.dumps({
            'package_path': str(self.package_root),
            'total_episodes': len(episodes),
            'generated_at': datetime.now().isoformat()
        }), expire=86400)

    def _generate_readme_files(self, folders: Dict, delivery: Dict):
        """Generate README files for each folder"""
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')

        readme_contents = {
            '01_Scripts': """# Scripts Folder

This folder contains all script versions for the audio series production.

Contents:
- Episode_XX_MASTER.txt: Production-ready master scripts
- master_scripts.json: Complete script package data

Script Versions:
- Master Scripts: Complete, formatted, version-controlled finals
- Table Read Scripts: Simplified for actors' first read
- Production Scripts: Full technical annotations
- Recording Scripts: Character-specific sides

For questions, see COVER_LETTER.txt in the root folder.
""",
            '02_Documentation': """# Documentation Folder

This folder contains all reference documentation for the audio series.

Contents:
- Series_Bible.json/txt: Complete series overview and rules
- Character_Bible.json: All characters with voice notes
- World_Bible.json: Locations with sound signatures
- Production_Bible.json: Technical specs and standards

Use these documents to ensure consistency across all production phases.
""",
            '03_Tracking': """# Tracking Folder

This folder contains production management documents.

Contents:
- Episode_Guide.json: Synopsis and details per episode
- Plant_Payoff_Matrix.json: Story setup tracking
- Dependency_Chart.json: Episode ordering requirements
- Change_Log.json: Revision history

These documents help manage the complex production timeline.
""",
            '04_Audio_Specs': """# Audio Specifications Folder

This folder contains audio production specifications.

This folder may be populated during production with:
- Sound cue sheets
- Music spotting notes
- SFX library lists
- Technical requirements

Refer to Production_Bible.json in the Documentation folder for details.
"""
        }

        # Root README
        root_readme = f"""# Audio Series Production Package

Session ID: {self.session_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Package Contents

1. **01_Scripts**: All script versions (master, table read, production, recording)
2. **02_Documentation**: Series bible, character bible, world bible, production bible
3. **03_Tracking**: Episode guide, plant/payoff matrix, dependencies, change log
4. **04_Audio_Specs**: Audio production specifications

## Getting Started

1. Read COVER_LETTER.txt for project overview and next steps
2. Review Series_Bible.json in 02_Documentation for world rules
3. Check Episode_Guide.json in 03_Tracking for episode details
4. Consult master scripts in 01_Scripts for production

## Contact Information

See COVER_LETTER.txt for contacts and questions.

## Navigation

Each folder contains a README.md file with specific details.
"""

        # Write root README
        with open(self.package_root / 'README.md', 'w', encoding=encoding) as f:
            f.write(root_readme)

        # Write folder READMEs
        for folder_key, folder_path in folders.items():
            readme_content = readme_contents.get(folder_key, '')
            with open(folder_path / 'README.md', 'w', encoding=encoding) as f:
                f.write(readme_content)

    def _generate_file_manifest(self, delivery: Dict):
        """Generate comprehensive file manifest"""
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')

        manifest_lines = [
            "=" * 70,
            "FILE MANIFEST",
            "=" * 70,
            "",
            f"Package: {self.package_root.name}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "=" * 70,
            "CONTENTS",
            "=" * 70,
            ""
        ]

        # Walk directory tree and list all files
        for root, dirs, files in sorted(os.walk(self.package_root)):
            level = root.replace(str(self.package_root), '').count(os.sep)
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root)
            if level > 0:
                manifest_lines.append(f"{indent}{folder_name}/")

            subindent = ' ' * 2 * (level + 1)
            for file in sorted(files):
                if file != 'FILE_MANIFEST.txt':
                    file_path = Path(root) / file
                    size_kb = file_path.stat().st_size / 1024
                    manifest_lines.append(f"{subindent}{file} ({size_kb:.1f} KB)")

        manifest_lines.extend([
            "",
            "=" * 70,
            "END OF MANIFEST",
            "=" * 70
        ])

        manifest_path = self.package_root / 'FILE_MANIFEST.txt'
        with open(manifest_path, 'w', encoding=encoding) as f:
            f.write('\n'.join(manifest_lines))

    def _create_zip_archive(self, source_dir: Path, zip_path: Path):
        """Create ZIP archive of package"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(source_dir.parent)
                    zipf.write(file_path, arcname)

    def display_package_contents(self):
        """Display package contents summary"""
        print("\n" + "=" * 70)
        print("📦 PACKAGE CONTENTS")
        print("=" * 70)

        import os

        total_files = 0
        total_size = 0

        for root, dirs, files in os.walk(self.package_root):
            for file in files:
                file_path = Path(root) / file
                total_files += 1
                total_size += file_path.stat().st_size

        print(f"\nTotal Files: {total_files}")
        print(f"Total Size: {total_size / (1024*1024):.2f} MB")
        print(f"\nPackage Location: {self.package_root}")
        print(f"\nFolder Structure:")
        print(f"   • 01_Scripts/")
        print(f"   • 02_Documentation/")
        print(f"   • 03_Tracking/")
        print(f"   • 04_Audio_Specs/")
        print(f"   • README.md")
        print(f"   • COVER_LETTER.txt")
        print(f"   • FILE_MANIFEST.txt")
        print("\n" + "=" * 70)


# CLI Entry Point
async def main():
    """Run Station 44 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()

    if not session_id:
        print("❌ Session ID required")
        return

    package_assembly = Station44PackageAssembly(session_id)
    await package_assembly.initialize()

    try:
        await package_assembly.run()
        print(f"\n✅ Success! Package assembly complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
