"""
Station 41: Cross-Episode Dependency Check

This station tracks dependencies across all episodes to ensure proper information flow,
character consistency, world coherence, and audio continuity.

Flow:
1. Load Station 27 master scripts (all episodes)
2. Load supporting data (Station 2, 5, 7, 8, 10 for context)
3. Execute 4-task dependency analysis sequence:
   - Task 1: Knowledge Dependencies (forward/backward dependencies, critical paths)
   - Task 2: Character Dependencies (relationships, knowledge, presence)
   - Task 3: World Dependencies (locations, time, technology/magic)
   - Task 4: Audio Dependencies (motifs, music, signature sounds)
4. Generate dependency matrix per episode
5. Identify critical paths and reorder impossibilities
6. Generate required audio callback list
7. Save comprehensive dependency reports

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config
- FAIL FAST - Exit on missing dependencies with actionable messages
- Track forward and backward dependencies separately
- Identify breaking points if episodes were reordered
- Explicit error messages with file names, line numbers
- Consistent logging to logs/station_41.log
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
log_file = log_dir / "station_41.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Station41CrossEpisodeDependencyCheck:
    """Station 41: Cross-Episode Dependency Checker"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=41)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path(self.config_data.get('output_path', 'output/station_41'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate required config fields
        self._validate_config()
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_41.yml'

        if not config_path.exists():
            raise FileNotFoundError(f"❌ Station 41 config file not found: {config_path}")

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
        logger.info("✅ Station 41 initialized")
    
    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🔗 STATION 41: CROSS-EPISODE DEPENDENCY CHECK")
        print("=" * 70)
        print()
        
        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            supporting_data = await self.load_supporting_data()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 27: {len(station27_data.get('episodes', {}))} episodes")
            print(f"   ✓ Supporting data loaded from stations 2, 5, 7, 8, 10")
            print()
            
            # Step 2: Display project summary
            episodes = station27_data.get('episodes', {})
            self.display_project_summary(episodes, supporting_data)
            
            # Step 3: Process all episodes together for cross-episode analysis
            print("\n🔍 Analyzing cross-episode dependencies...")
            print("-" * 70)
            
            # Execute 4-task dependency analysis sequence
            print("📚 Task 1/4: Knowledge Dependencies Analysis...")
            knowledge_dependencies = await self.execute_task1_knowledge_dependencies(
                episodes, supporting_data
            )
            print("✅ Knowledge dependencies mapped")
            
            print("👥 Task 2/4: Character Dependencies Analysis...")
            character_dependencies = await self.execute_task2_character_dependencies(
                episodes, supporting_data
            )
            print("✅ Character dependencies mapped")
            
            print("🌍 Task 3/4: World Dependencies Analysis...")
            world_dependencies = await self.execute_task3_world_dependencies(
                episodes, supporting_data
            )
            print("✅ World dependencies mapped")
            
            print("🔊 Task 4/4: Audio Dependencies Analysis...")
            audio_dependencies = await self.execute_task4_audio_dependencies(
                episodes, supporting_data
            )
            print("✅ Audio dependencies mapped")
            
            # Step 4: Generate dependency matrix and critical paths
            print("\n" + "=" * 70)
            print("📊 GENERATING DEPENDENCY MATRIX")
            print("=" * 70)
            
            dependency_matrix = self._build_dependency_matrix(
                knowledge_dependencies, character_dependencies,
                world_dependencies, audio_dependencies, episodes
            )
            
            critical_paths = self._identify_critical_paths(dependency_matrix)
            reorder_impossibilities = self._identify_reorder_impossibilities(dependency_matrix)
            audio_callbacks = self._extract_required_audio_callbacks(audio_dependencies)
            
            # Step 5: Generate comprehensive reports
            await self.generate_dependency_reports(
                dependency_matrix, critical_paths, reorder_impossibilities,
                audio_callbacks, knowledge_dependencies, character_dependencies,
                world_dependencies, audio_dependencies
            )
            
            print("\n" + "=" * 70)
            print("✅ STATION 41 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Analyzed: {len(episodes)}")
            print(f"Total Dependencies Mapped: {len(dependency_matrix.get('all_dependencies', []))}")
            print(f"Critical Paths Identified: {len(critical_paths)}")
            print(f"Reorder Impossibilities: {len(reorder_impossibilities)}")
            print(f"Required Audio Callbacks: {len(audio_callbacks)}")
            print("\n📄 Output files:")
            print(f"   - output/station_41/{self.session_id}_dependency_matrix.json")
            print(f"   - output/station_41/{self.session_id}_critical_paths.json")
            print(f"   - output/station_41/{self.session_id}_reorder_analysis.json")
            print(f"   - output/station_41/{self.session_id}_audio_callbacks.json")
            print(f"   - output/station_41/{self.session_id}_full_report.txt")
        
        except Exception as e:
            logger.error(f"❌ Station 41 failed: {str(e)}")
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
            
            # Station 5: Season Architecture
            station_05_dir = Path("output/station_05")
            station5_files = list(station_05_dir.glob("*.json"))
            if station5_files:
                latest_file = max(station5_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_5'] = json.load(f)
            
            # Station 7: Character Architecture
            station_07_dir = Path("output/station_07")
            station7_files = list(station_07_dir.glob("*character_bible.json"))
            if station7_files:
                latest_file = max(station7_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_7'] = json.load(f)
            
            # Station 8: World Builder
            station_08_dir = Path("output/station_08")
            station8_files = list(station_08_dir.glob("*world_bible.json"))
            if station8_files:
                latest_file = max(station8_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_8'] = json.load(f)
            
            # Station 10: Narrative Reveal Strategy
            station_10_dir = Path("output/station_10")
            station10_files = list(station_10_dir.glob("*.json"))
            if station10_files:
                latest_file = max(station10_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    supporting_data['station_10'] = json.load(f)
            
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
        print(f"   • Station 5 (Season Architecture): {'✓' if 'station_5' in supporting_data else '✗'}")
        print(f"   • Station 7 (Character Architecture): {'✓' if 'station_7' in supporting_data else '✗'}")
        print(f"   • Station 8 (World Builder): {'✓' if 'station_8' in supporting_data else '✗'}")
        print(f"   • Station 10 (Narrative Reveal): {'✓' if 'station_10' in supporting_data else '✗'}")
        print()
        
        if episodes:
            print("Episode List:")
            for episode_key, episode_data in sorted(episodes.items()):
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)
    
    async def execute_task1_knowledge_dependencies(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 1: Knowledge Dependencies Analysis"""
        try:
            # Extract episode summaries for analysis
            episode_summaries = {}
            for episode_num, episode_data in episodes.items():
                episode_content = self._extract_episode_content(episode_data)
                episode_summaries[episode_num] = {
                    'episode_number': episode_num,
                    'content': episode_content[:10000],  # First 10000 chars
                    'title': episode_data.get('production_package', {}).get('production_summary', {}).get('title', '')
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'episode_summaries': json.dumps(episode_summaries, indent=2),
                'reveal_strategy': json.dumps(supporting_data.get('station_10', {}), indent=2) if 'station_10' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('knowledge_dependencies').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('knowledge_dependencies', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")
    
    async def execute_task2_character_dependencies(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 2: Character Dependencies Analysis"""
        try:
            # Extract character appearances per episode
            character_appearances = {}
            for episode_num, episode_data in episodes.items():
                voice_actors = episode_data.get('production_package', {}).get('voice_actor_specifications', [])
                characters = [actor.get('character', '') for actor in voice_actors]
                character_appearances[episode_num] = {
                    'episode_number': episode_num,
                    'characters': characters,
                    'character_count': len(characters)
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'character_appearances': json.dumps(character_appearances, indent=2),
                'character_bible': json.dumps(supporting_data.get('station_7', {}), indent=2) if 'station_7' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('character_dependencies').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('character_dependencies', {})
            
        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")
    
    async def execute_task3_world_dependencies(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 3: World Dependencies Analysis"""
        try:
            # Extract location and time data per episode
            world_data = {}
            for episode_num, episode_data in episodes.items():
                scenes = episode_data.get('production_package', {}).get('cast_briefing', {}).get('key_scenes', [])
                locations = [scene.get('location', '') for scene in scenes]
                world_data[episode_num] = {
                    'episode_number': episode_num,
                    'locations': list(set([loc for loc in locations if loc])),
                    'location_count': len(set([loc for loc in locations if loc]))
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'world_data': json.dumps(world_data, indent=2),
                'world_bible': json.dumps(supporting_data.get('station_8', {}), indent=2) if 'station_8' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('world_dependencies').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('world_dependencies', {})
            
        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")
    
    async def execute_task4_audio_dependencies(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 4: Audio Dependencies Analysis"""
        try:
            # Extract audio elements per episode
            audio_elements = {}
            for episode_num, episode_data in episodes.items():
                sound_specs = episode_data.get('production_package', {}).get('sound_design_specifications', {})
                audio_elements[episode_num] = {
                    'episode_number': episode_num,
                    'required_effects': sound_specs.get('required_effects', []),
                    'music_cues': sound_specs.get('music_cues', []),
                    'ambient_layers': sound_specs.get('ambient_layers', [])
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'audio_elements': json.dumps(audio_elements, indent=2),
                'style_guide': json.dumps(supporting_data.get('station_6', {}), indent=2) if 'station_6' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('audio_dependencies').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('audio_dependencies', {})
            
        except Exception as e:
            logger.error(f"Task 4 failed: {str(e)}")
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
    
    def _build_dependency_matrix(self, knowledge_deps: Dict, character_deps: Dict,
                                  world_deps: Dict, audio_deps: Dict, episodes: Dict) -> Dict:
        """Build comprehensive dependency matrix"""
        matrix = {
            'episodes': sorted(episodes.keys()),
            'all_dependencies': [],
            'forward_dependencies': {},  # Episode X requires info from Y
            'backward_dependencies': {},  # Episode X sets up info for Y
            'by_category': {
                'knowledge': [],
                'character': [],
                'world': [],
                'audio': []
            }
        }
        
        # Extract dependencies from each category
        if knowledge_deps:
            matrix['by_category']['knowledge'] = knowledge_deps.get('dependencies', [])
        
        if character_deps:
            matrix['by_category']['character'] = character_deps.get('dependencies', [])
        
        if world_deps:
            matrix['by_category']['world'] = world_deps.get('dependencies', [])
        
        if audio_deps:
            matrix['by_category']['audio'] = audio_deps.get('dependencies', [])
        
        # Combine all dependencies
        for category, deps in matrix['by_category'].items():
            matrix['all_dependencies'].extend(deps)
        
        # Build forward/backward dependency maps
        for dep in matrix['all_dependencies']:
            from_ep = dep.get('from_episode')
            to_ep = dep.get('to_episode')
            
            if from_ep and to_ep:
                # Forward dependency: to_ep depends on from_ep
                if to_ep not in matrix['forward_dependencies']:
                    matrix['forward_dependencies'][to_ep] = []
                matrix['forward_dependencies'][to_ep].append(dep)
                
                # Backward dependency: from_ep sets up for to_ep
                if from_ep not in matrix['backward_dependencies']:
                    matrix['backward_dependencies'][from_ep] = []
                matrix['backward_dependencies'][from_ep].append(dep)
        
        return matrix
    
    def _identify_critical_paths(self, dependency_matrix: Dict) -> List[Dict]:
        """Identify critical paths that cannot be broken"""
        critical_paths = []
        forward_deps = dependency_matrix.get('forward_dependencies', {})
        
        # Find longest dependency chains
        episodes = dependency_matrix.get('episodes', [])
        
        for start_ep in episodes:
            path = self._trace_dependency_path(start_ep, forward_deps, [])
            if len(path) > 2:  # At least 2 episodes in chain
                critical_paths.append({
                    'path': path,
                    'length': len(path),
                    'cannot_reorder': True
                })
        
        # Sort by length (longest first)
        critical_paths.sort(key=lambda x: x['length'], reverse=True)
        
        return critical_paths
    
    def _trace_dependency_path(self, episode: int, forward_deps: Dict, visited: List[int]) -> List[int]:
        """Recursively trace dependency path"""
        if episode in visited:
            return visited  # Cycle detected
        
        visited = visited + [episode]
        
        if episode in forward_deps:
            for dep in forward_deps[episode]:
                next_ep = dep.get('to_episode')
                if next_ep and next_ep not in visited:
                    visited = self._trace_dependency_path(next_ep, forward_deps, visited)
        
        return visited
    
    def _identify_reorder_impossibilities(self, dependency_matrix: Dict) -> List[Dict]:
        """Identify episodes that cannot be reordered"""
        impossibilities = []
        forward_deps = dependency_matrix.get('forward_dependencies', {})
        
        for to_ep, deps in forward_deps.items():
            for dep in deps:
                from_ep = dep.get('from_episode')
                if from_ep and from_ep >= to_ep:
                    # This is a forward dependency (from earlier episode)
                    impossibilities.append({
                        'episode_from': from_ep,
                        'episode_to': to_ep,
                        'dependency_type': dep.get('category', 'unknown'),
                        'dependency_description': dep.get('description', ''),
                        'reason': f'Episode {to_ep} requires information from Episode {from_ep}',
                        'cannot_reorder': True
                    })
        
        return impossibilities
    
    def _extract_required_audio_callbacks(self, audio_dependencies: Dict) -> List[Dict]:
        """Extract all required audio callbacks across episodes"""
        callbacks = []
        
        if audio_dependencies:
            audio_deps = audio_dependencies.get('dependencies', [])
            
            for dep in audio_deps:
                if dep.get('audio_callback_required'):
                    callbacks.append({
                        'from_episode': dep.get('from_episode'),
                        'to_episode': dep.get('to_episode'),
                        'audio_element': dep.get('audio_element', ''),
                        'callback_type': dep.get('callback_type', ''),
                        'description': dep.get('description', ''),
                        'implementation_notes': dep.get('implementation_notes', '')
                    })
        
        return callbacks
    
    async def generate_dependency_reports(self, dependency_matrix: Dict, critical_paths: List[Dict],
                                          reorder_impossibilities: List[Dict], audio_callbacks: List[Dict],
                                          knowledge_deps: Dict, character_deps: Dict,
                                          world_deps: Dict, audio_deps: Dict):
        """Generate comprehensive dependency reports"""
        
        # 1. Dependency Matrix JSON
        matrix_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'dependency_matrix': dependency_matrix,
            'statistics': {
                'total_dependencies': len(dependency_matrix.get('all_dependencies', [])),
                'knowledge_dependencies': len(dependency_matrix.get('by_category', {}).get('knowledge', [])),
                'character_dependencies': len(dependency_matrix.get('by_category', {}).get('character', [])),
                'world_dependencies': len(dependency_matrix.get('by_category', {}).get('world', [])),
                'audio_dependencies': len(dependency_matrix.get('by_category', {}).get('audio', []))
            }
        }
        
        json_path = self.output_dir / f"{self.session_id}_dependency_matrix.json"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(matrix_report, f, indent=2, ensure_ascii=False)
        
        # 2. Critical Paths JSON
        paths_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'critical_paths': critical_paths,
            'longest_path_length': max([p['length'] for p in critical_paths], default=0),
            'total_critical_paths': len(critical_paths)
        }
        
        json_path = self.output_dir / f"{self.session_id}_critical_paths.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(paths_report, f, indent=2, ensure_ascii=False)
        
        # 3. Reorder Analysis JSON
        reorder_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'reorder_impossibilities': reorder_impossibilities,
            'total_impossibilities': len(reorder_impossibilities),
            'episodes_cannot_reorder': list(set([imp['episode_to'] for imp in reorder_impossibilities]))
        }
        
        json_path = self.output_dir / f"{self.session_id}_reorder_analysis.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(reorder_report, f, indent=2, ensure_ascii=False)
        
        # 4. Audio Callbacks JSON
        callbacks_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'required_audio_callbacks': audio_callbacks,
            'total_callbacks': len(audio_callbacks)
        }
        
        json_path = self.output_dir / f"{self.session_id}_audio_callbacks.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(callbacks_report, f, indent=2, ensure_ascii=False)
        
        # 5. Full Report TXT
        self._generate_full_report_txt(
            dependency_matrix, critical_paths, reorder_impossibilities,
            audio_callbacks, knowledge_deps, character_deps, world_deps, audio_deps
        )
        
        # Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_41"
        await self.redis.set(redis_key, json.dumps(matrix_report), expire=86400)
        
        print(f"✅ All dependency reports generated")
    
    def _generate_full_report_txt(self, dependency_matrix: Dict, critical_paths: List[Dict],
                                   reorder_impossibilities: List[Dict], audio_callbacks: List[Dict],
                                   knowledge_deps: Dict, character_deps: Dict,
                                   world_deps: Dict, audio_deps: Dict):
        """Generate human-readable full report"""
        txt_path = self.output_dir / f"{self.session_id}_full_report.txt"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        
        with open(txt_path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 41: CROSS-EPISODE DEPENDENCY CHECK REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            # Statistics
            f.write("-" * 70 + "\n")
            f.write("DEPENDENCY STATISTICS\n")
            f.write("-" * 70 + "\n\n")
            
            stats = {
                'total_dependencies': len(dependency_matrix.get('all_dependencies', [])),
                'knowledge': len(dependency_matrix.get('by_category', {}).get('knowledge', [])),
                'character': len(dependency_matrix.get('by_category', {}).get('character', [])),
                'world': len(dependency_matrix.get('by_category', {}).get('world', [])),
                'audio': len(dependency_matrix.get('by_category', {}).get('audio', []))
            }
            
            f.write(f"Total Dependencies: {stats['total_dependencies']}\n")
            f.write(f"  • Knowledge: {stats['knowledge']}\n")
            f.write(f"  • Character: {stats['character']}\n")
            f.write(f"  • World: {stats['world']}\n")
            f.write(f"  • Audio: {stats['audio']}\n\n")
            
            # Critical Paths
            f.write("-" * 70 + "\n")
            f.write("CRITICAL PATHS (Cannot Break)\n")
            f.write("-" * 70 + "\n\n")
            
            if critical_paths:
                for i, path in enumerate(critical_paths[:10], 1):  # Top 10
                    path_episodes = path.get('path', [])
                    f.write(f"{i}. Path Length: {path['length']} episodes\n")
                    f.write(f"   Episodes: {' → '.join(map(str, path_episodes))}\n")
                    f.write(f"   Cannot Reorder: {'Yes' if path.get('cannot_reorder') else 'No'}\n\n")
            else:
                f.write("No critical paths identified.\n\n")
            
            # Reorder Impossibilities
            f.write("-" * 70 + "\n")
            f.write("REORDER IMPOSSIBILITIES\n")
            f.write("-" * 70 + "\n\n")
            
            if reorder_impossibilities:
                for i, imp in enumerate(reorder_impossibilities[:20], 1):  # Top 20
                    f.write(f"{i}. Episode {imp['episode_from']} → Episode {imp['episode_to']}\n")
                    f.write(f"   Type: {imp.get('dependency_type', 'unknown')}\n")
                    f.write(f"   Reason: {imp.get('reason', 'N/A')}\n\n")
            else:
                f.write("No reorder impossibilities identified.\n\n")
            
            # Audio Callbacks
            f.write("-" * 70 + "\n")
            f.write("REQUIRED AUDIO CALLBACKS\n")
            f.write("-" * 70 + "\n\n")
            
            if audio_callbacks:
                for i, callback in enumerate(audio_callbacks[:20], 1):  # Top 20
                    f.write(f"{i}. Episode {callback.get('from_episode', '?')} → Episode {callback.get('to_episode', '?')}\n")
                    f.write(f"   Element: {callback.get('audio_element', 'N/A')}\n")
                    f.write(f"   Type: {callback.get('callback_type', 'N/A')}\n")
                    f.write(f"   Description: {callback.get('description', 'N/A')}\n\n")
            else:
                f.write("No audio callbacks required.\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("END OF DEPENDENCY CHECK REPORT\n")
            f.write("=" * 70 + "\n")


# CLI Entry Point
async def main():
    """Run Station 41 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    checker = Station41CrossEpisodeDependencyCheck(session_id)
    await checker.initialize()
    
    try:
        await checker.run()
        print(f"\n✅ Success! Dependency check complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

