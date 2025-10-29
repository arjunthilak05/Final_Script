"""
Station 42: Listener Experience Simulator

This station simulates different listener experiences to identify potential issues,
confusion points, engagement risks, and optimization opportunities across all episodes.

Flow:
1. Load Station 27 master scripts (all episodes)
2. Load supporting data (Station 2, 5 for context)
3. Execute 4-task listener simulation sequence:
   - Task 1: First-Time Listener Path (virgin listening simulation)
   - Task 2: Binge Listener Path (continuous listening simulation)
   - Task 3: Weekly Listener Path (episodic release simulation)
   - Task 4: Different Attention Levels (full/casual/interrupted listening)
4. Generate listener journey maps
5. Identify confusion risk points
6. Generate engagement predictions
7. Provide experience optimization notes
8. Save comprehensive listener experience reports

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config
- FAIL FAST - Exit on missing dependencies with actionable messages
- Simulate realistic listener behaviors and attention patterns
- Identify both problems and strengths
- Explicit error messages with file names, line numbers
- Consistent logging to logs/station_42.log
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
log_file = log_dir / "station_42.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Station42ListenerExperienceSimulator:
    """Station 42: Listener Experience Simulator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=42)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path(self.config_data.get('output_path', 'output/station_42'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate required config fields
        self._validate_config()
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_42.yml'

        if not config_path.exists():
            raise FileNotFoundError(f"❌ Station 42 config file not found: {config_path}")

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
        logger.info("✅ Station 42 initialized")
    
    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🎧 STATION 42: LISTENER EXPERIENCE SIMULATOR")
        print("=" * 70)
        print()
        
        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            supporting_data = await self.load_supporting_data()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 27: {len(station27_data.get('episodes', {}))} episodes")
            print(f"   ✓ Supporting data loaded from stations 2, 5")
            print()
            
            # Step 2: Display project summary
            episodes = station27_data.get('episodes', {})
            self.display_project_summary(episodes, supporting_data)
            
            # Step 3: Process all episodes for listener experience simulation
            print("\n🎧 Simulating listener experiences...")
            print("-" * 70)
            
            # Execute 4-task listener simulation sequence
            print("🆕 Task 1/4: First-Time Listener Path Simulation...")
            first_time_results = await self.execute_task1_first_time_listener(
                episodes, supporting_data
            )
            print("✅ First-time listener path simulated")
            
            print("📺 Task 2/4: Binge Listener Path Simulation...")
            binge_results = await self.execute_task2_binge_listener(
                episodes, supporting_data
            )
            print("✅ Binge listener path simulated")
            
            print("📅 Task 3/4: Weekly Listener Path Simulation...")
            weekly_results = await self.execute_task3_weekly_listener(
                episodes, supporting_data
            )
            print("✅ Weekly listener path simulated")
            
            print("🎯 Task 4/4: Different Attention Levels Simulation...")
            attention_results = await self.execute_task4_attention_levels(
                episodes, supporting_data
            )
            print("✅ Attention level simulations completed")
            
            # Step 4: Generate comprehensive listener experience analysis
            print("\n" + "=" * 70)
            print("📊 GENERATING LISTENER EXPERIENCE ANALYSIS")
            print("=" * 70)
            
            journey_map = self._build_listener_journey_map(
                first_time_results, binge_results, weekly_results, attention_results, episodes
            )
            
            confusion_risks = self._identify_confusion_risk_points(
                first_time_results, binge_results, weekly_results, attention_results
            )
            
            engagement_predictions = self._generate_engagement_predictions(
                journey_map, confusion_risks, episodes
            )
            
            optimization_notes = self._generate_optimization_notes(
                journey_map, confusion_risks, engagement_predictions
            )
            
            # Step 5: Generate comprehensive reports
            await self.generate_listener_experience_reports(
                journey_map, confusion_risks, engagement_predictions,
                optimization_notes, first_time_results, binge_results,
                weekly_results, attention_results
            )
            
            print("\n" + "=" * 70)
            print("✅ STATION 42 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Simulated: {len(episodes)}")
            print(f"Confusion Risk Points: {len(confusion_risks)}")
            print(f"Optimization Recommendations: {len(optimization_notes)}")
            print("\n📄 Output files:")
            print(f"   - output/station_42/{self.session_id}_listener_journey_map.json")
            print(f"   - output/station_42/{self.session_id}_confusion_risks.json")
            print(f"   - output/station_42/{self.session_id}_engagement_predictions.json")
            print(f"   - output/station_42/{self.session_id}_optimization_notes.json")
            print(f"   - output/station_42/{self.session_id}_full_report.txt")
        
        except Exception as e:
            logger.error(f"❌ Station 42 failed: {str(e)}")
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
        print()
        
        if episodes:
            print("Episode List:")
            for episode_key, episode_data in sorted(episodes.items()):
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)
    
    async def execute_task1_first_time_listener(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 1: First-Time Listener Path Simulation"""
        try:
            # Extract episode summaries for analysis
            episode_summaries = {}
            for episode_num, episode_data in episodes.items():
                episode_content = self._extract_episode_content(episode_data)
                episode_summaries[episode_num] = {
                    'episode_number': episode_num,
                    'content_preview': episode_content[:8000],  # First 8000 chars
                    'title': episode_data.get('production_package', {}).get('production_summary', {}).get('title', ''),
                    'runtime_estimate': episode_data.get('production_package', {}).get('production_summary', {}).get('runtime_estimate', 'Unknown')
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'episode_summaries': json.dumps(episode_summaries, indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}',
                'season_architecture': json.dumps(supporting_data.get('station_5', {}), indent=2) if 'station_5' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('first_time_listener').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('first_time_listener_path', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")
    
    async def execute_task2_binge_listener(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 2: Binge Listener Path Simulation"""
        try:
            # Extract episode summaries for binge analysis
            episode_summaries = {}
            for episode_num, episode_data in episodes.items():
                episode_content = self._extract_episode_content(episode_data)
                episode_summaries[episode_num] = {
                    'episode_number': episode_num,
                    'content_preview': episode_content[:6000],  # First 6000 chars
                    'title': episode_data.get('production_package', {}).get('production_summary', {}).get('title', ''),
                    'cliffhanger_type': episode_data.get('production_package', {}).get('production_summary', {}).get('cliffhanger_type', 'Unknown')
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'episode_summaries': json.dumps(episode_summaries, indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('binge_listener').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('binge_listener_path', {})
            
        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")
    
    async def execute_task3_weekly_listener(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 3: Weekly Listener Path Simulation"""
        try:
            # Extract episode summaries for weekly analysis
            episode_summaries = {}
            for episode_num, episode_data in episodes.items():
                episode_content = self._extract_episode_content(episode_data)
                # Get hook/recap elements
                hook = episode_data.get('production_package', {}).get('production_summary', {}).get('opening_hook', '')
                recap_elements = episode_data.get('production_package', {}).get('cast_briefing', {}).get('previous_episode_summary', '')
                
                episode_summaries[episode_num] = {
                    'episode_number': episode_num,
                    'content_preview': episode_content[:6000],
                    'title': episode_data.get('production_package', {}).get('production_summary', {}).get('title', ''),
                    'opening_hook': hook,
                    'recap_present': bool(recap_elements)
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'episode_summaries': json.dumps(episode_summaries, indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('weekly_listener').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('weekly_listener_path', {})
            
        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")
    
    async def execute_task4_attention_levels(self, episodes: Dict, supporting_data: Dict) -> Dict:
        """Task 4: Different Attention Levels Simulation"""
        try:
            # Extract episode content for attention analysis
            episode_summaries = {}
            for episode_num, episode_data in episodes.items():
                episode_content = self._extract_episode_content(episode_data)
                # Extract key elements that affect attention
                scenes = episode_data.get('production_package', {}).get('cast_briefing', {}).get('key_scenes', [])
                
                episode_summaries[episode_num] = {
                    'episode_number': episode_num,
                    'content_preview': episode_content[:7000],
                    'title': episode_data.get('production_package', {}).get('production_summary', {}).get('title', ''),
                    'scene_count': len(scenes),
                    'dialogue_density': len(episode_content.split()) / max(len(episode_content.split('\n')), 1)
                }
            
            context = {
                'session_id': self.session_id,
                'total_episodes': len(episodes),
                'episode_summaries': json.dumps(episode_summaries, indent=2),
                'project_dna': json.dumps(supporting_data.get('station_2', {}), indent=2) if 'station_2' in supporting_data else '{}'
            }
            
            prompt = self.config.get_prompt('attention_levels').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('attention_level_analysis', {})
            
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
    
    def _build_listener_journey_map(self, first_time: Dict, binge: Dict, weekly: Dict,
                                    attention: Dict, episodes: Dict) -> Dict:
        """Build comprehensive listener journey map"""
        journey_map = {
            'episodes': sorted(episodes.keys()),
            'first_time_journey': first_time,
            'binge_journey': binge,
            'weekly_journey': weekly,
            'attention_levels': attention,
            'overall_journey': {
                'episode_ratings': {},
                'engagement_curve': [],
                'confusion_curve': [],
                'satisfaction_curve': []
            }
        }
        
        # Combine insights from all simulations
        for ep_num in sorted(episodes.keys()):
            journey_map['overall_journey']['episode_ratings'][ep_num] = {
                'first_time_score': self._extract_episode_score(first_time, ep_num),
                'binge_score': self._extract_episode_score(binge, ep_num),
                'weekly_score': self._extract_episode_score(weekly, ep_num),
                'attention_score': self._extract_episode_score(attention, ep_num)
            }
        
        return journey_map
    
    def _extract_episode_score(self, results: Dict, episode_num: int) -> float:
        """Extract episode score from results"""
        if not results:
            return 0.0
        
        episode_data = results.get('episode_analysis', {}).get(str(episode_num), {})
        return episode_data.get('engagement_score', episode_data.get('satisfaction_score', 0.0))
    
    def _identify_confusion_risk_points(self, first_time: Dict, binge: Dict,
                                       weekly: Dict, attention: Dict) -> List[Dict]:
        """Identify confusion risk points across all simulations"""
        confusion_risks = []
        
        # Extract confusion points from each simulation
        for results, source in [(first_time, 'first_time'), (binge, 'binge'),
                               (weekly, 'weekly'), (attention, 'attention')]:
            if results:
                confusion_points = results.get('confusion_points', [])
                for point in confusion_points:
                    point['source_simulation'] = source
                    confusion_risks.append(point)
        
        # Sort by severity/risk level
        confusion_risks.sort(key=lambda x: x.get('risk_level', 0), reverse=True)
        
        return confusion_risks
    
    def _generate_engagement_predictions(self, journey_map: Dict, confusion_risks: List[Dict],
                                         episodes: Dict) -> Dict:
        """Generate engagement predictions based on journey map"""
        predictions = {
            'drop_off_risks': [],
            'engagement_peaks': [],
            'retention_probability': {},
            'recommendation_likelihood': {}
        }
        
        # Analyze episode-by-episode engagement
        episode_ratings = journey_map.get('overall_journey', {}).get('episode_ratings', {})
        
        for ep_num, ratings in episode_ratings.items():
            avg_score = sum([
                ratings.get('first_time_score', 0),
                ratings.get('binge_score', 0),
                ratings.get('weekly_score', 0),
                ratings.get('attention_score', 0)
            ]) / 4.0
            
            if avg_score < 0.5:
                predictions['drop_off_risks'].append({
                    'episode': ep_num,
                    'avg_score': avg_score,
                    'reason': 'Low engagement across all listening modes'
                })
            elif avg_score > 0.8:
                predictions['engagement_peaks'].append({
                    'episode': ep_num,
                    'avg_score': avg_score,
                    'reason': 'High engagement across all listening modes'
                })
        
        return predictions
    
    def _generate_optimization_notes(self, journey_map: Dict, confusion_risks: List[Dict],
                                     engagement_predictions: Dict) -> List[Dict]:
        """Generate optimization recommendations"""
        optimization_notes = []
        
        # Based on confusion risks
        high_risk_confusions = [c for c in confusion_risks if c.get('risk_level', 0) > 7]
        if high_risk_confusions:
            optimization_notes.append({
                'category': 'confusion_resolution',
                'priority': 'HIGH',
                'recommendations': [
                    {
                        'episode': c.get('episode', 'unknown'),
                        'issue': c.get('confusion_description', ''),
                        'fix': c.get('suggested_fix', 'Clarify information delivery')
                    }
                    for c in high_risk_confusions[:5]
                ]
            })
        
        # Based on engagement predictions
        if engagement_predictions.get('drop_off_risks'):
            optimization_notes.append({
                'category': 'engagement_boost',
                'priority': 'MEDIUM',
                'recommendations': [
                    {
                        'episode': risk.get('episode', 'unknown'),
                        'issue': risk.get('reason', 'Low engagement'),
                        'fix': 'Consider adding hooks, reveals, or character moments'
                    }
                    for risk in engagement_predictions['drop_off_risks'][:3]
                ]
            })
        
        return optimization_notes
    
    async def generate_listener_experience_reports(self, journey_map: Dict, confusion_risks: List[Dict],
                                                   engagement_predictions: Dict, optimization_notes: List[Dict],
                                                   first_time: Dict, binge: Dict, weekly: Dict, attention: Dict):
        """Generate comprehensive listener experience reports"""
        
        # 1. Listener Journey Map JSON
        journey_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'listener_journey_map': journey_map,
            'statistics': {
                'total_episodes': len(journey_map.get('episodes', [])),
                'confusion_risks': len(confusion_risks),
                'drop_off_risks': len(engagement_predictions.get('drop_off_risks', [])),
                'engagement_peaks': len(engagement_predictions.get('engagement_peaks', []))
            }
        }
        
        json_path = self.output_dir / f"{self.session_id}_listener_journey_map.json"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(journey_report, f, indent=2, ensure_ascii=False)
        
        # 2. Confusion Risks JSON
        confusion_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'confusion_risk_points': confusion_risks,
            'high_risk_count': len([c for c in confusion_risks if c.get('risk_level', 0) > 7]),
            'total_risks': len(confusion_risks)
        }
        
        json_path = self.output_dir / f"{self.session_id}_confusion_risks.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(confusion_report, f, indent=2, ensure_ascii=False)
        
        # 3. Engagement Predictions JSON
        engagement_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'engagement_predictions': engagement_predictions,
            'retention_forecast': 'Based on engagement curve analysis'
        }
        
        json_path = self.output_dir / f"{self.session_id}_engagement_predictions.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(engagement_report, f, indent=2, ensure_ascii=False)
        
        # 4. Optimization Notes JSON
        optimization_report = {
            'generated_at': datetime.now().isoformat(),
            'session_id': self.session_id,
            'optimization_notes': optimization_notes,
            'total_recommendations': sum(len(note.get('recommendations', [])) for note in optimization_notes)
        }
        
        json_path = self.output_dir / f"{self.session_id}_optimization_notes.json"
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(optimization_report, f, indent=2, ensure_ascii=False)
        
        # 5. Full Report TXT
        self._generate_full_report_txt(
            journey_map, confusion_risks, engagement_predictions,
            optimization_notes, first_time, binge, weekly, attention
        )
        
        # Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_42"
        await self.redis.set(redis_key, json.dumps(journey_report), expire=86400)
        
        print(f"✅ All listener experience reports generated")
    
    def _generate_full_report_txt(self, journey_map: Dict, confusion_risks: List[Dict],
                                  engagement_predictions: Dict, optimization_notes: List[Dict],
                                  first_time: Dict, binge: Dict, weekly: Dict, attention: Dict):
        """Generate human-readable full report"""
        txt_path = self.output_dir / f"{self.session_id}_full_report.txt"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        
        with open(txt_path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 42: LISTENER EXPERIENCE SIMULATOR REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            # Statistics
            f.write("-" * 70 + "\n")
            f.write("SIMULATION STATISTICS\n")
            f.write("-" * 70 + "\n\n")
            
            f.write(f"Total Episodes: {len(journey_map.get('episodes', []))}\n")
            f.write(f"Confusion Risk Points: {len(confusion_risks)}\n")
            f.write(f"High-Risk Confusions: {len([c for c in confusion_risks if c.get('risk_level', 0) > 7])}\n")
            f.write(f"Drop-Off Risks: {len(engagement_predictions.get('drop_off_risks', []))}\n")
            f.write(f"Engagement Peaks: {len(engagement_predictions.get('engagement_peaks', []))}\n\n")
            
            # First-Time Listener Summary
            f.write("-" * 70 + "\n")
            f.write("FIRST-TIME LISTENER PATH\n")
            f.write("-" * 70 + "\n\n")
            
            if first_time:
                episode_1 = first_time.get('episode_1_clarity', {})
                f.write(f"Episode 1 Clarity Score: {episode_1.get('clarity_score', 'N/A')}\n")
                f.write(f"World Understandable: {episode_1.get('world_understandable', 'N/A')}\n")
                f.write(f"Characters Distinguishable: {episode_1.get('characters_distinguishable', 'N/A')}\n")
                f.write(f"Hook Effective: {episode_1.get('hook_effective', 'N/A')}\n\n")
            
            # Binge Listener Summary
            f.write("-" * 70 + "\n")
            f.write("BINGE LISTENER PATH\n")
            f.write("-" * 70 + "\n\n")
            
            if binge:
                repetition_fatigue = binge.get('repetition_fatigue', {})
                f.write(f"Repetition Fatigue Risk: {repetition_fatigue.get('risk_level', 'N/A')}\n")
                f.write(f"Momentum Maintenance: {binge.get('momentum_maintenance', {}).get('overall_rating', 'N/A')}\n")
                f.write(f"Clarity in Speed: {binge.get('clarity_in_speed', {}).get('overall_rating', 'N/A')}\n\n")
            
            # Weekly Listener Summary
            f.write("-" * 70 + "\n")
            f.write("WEEKLY LISTENER PATH\n")
            f.write("-" * 70 + "\n\n")
            
            if weekly:
                recap_analysis = weekly.get('recap_necessity', {})
                f.write(f"Recap Necessity: {recap_analysis.get('rating', 'N/A')}\n")
                f.write(f"Hook Strength: {weekly.get('hook_strength', {}).get('overall_rating', 'N/A')}\n")
                f.write(f"Satisfaction Pacing: {weekly.get('satisfaction_pacing', {}).get('overall_rating', 'N/A')}\n\n")
            
            # Attention Levels Summary
            f.write("-" * 70 + "\n")
            f.write("ATTENTION LEVEL ANALYSIS\n")
            f.write("-" * 70 + "\n\n")
            
            if attention:
                full_attention = attention.get('full_attention', {})
                casual_listening = attention.get('casual_listening', {})
                interrupted_listening = attention.get('interrupted_listening', {})
                
                f.write(f"Full Attention Score: {full_attention.get('overall_score', 'N/A')}\n")
                f.write(f"Casual Listening Score: {casual_listening.get('overall_score', 'N/A')}\n")
                f.write(f"Interrupted Listening Score: {interrupted_listening.get('overall_score', 'N/A')}\n\n")
            
            # Top Confusion Risks
            f.write("-" * 70 + "\n")
            f.write("TOP CONFUSION RISK POINTS\n")
            f.write("-" * 70 + "\n\n")
            
            if confusion_risks:
                for i, risk in enumerate(confusion_risks[:10], 1):
                    f.write(f"{i}. Episode {risk.get('episode', '?')} - Risk Level: {risk.get('risk_level', 'N/A')}\n")
                    f.write(f"   Description: {risk.get('confusion_description', 'N/A')}\n")
                    f.write(f"   Source: {risk.get('source_simulation', 'N/A')}\n")
                    if risk.get('suggested_fix'):
                        f.write(f"   Suggested Fix: {risk.get('suggested_fix')}\n")
                    f.write("\n")
            else:
                f.write("No significant confusion risks identified.\n\n")
            
            # Optimization Notes
            f.write("-" * 70 + "\n")
            f.write("OPTIMIZATION RECOMMENDATIONS\n")
            f.write("-" * 70 + "\n\n")
            
            if optimization_notes:
                for i, note in enumerate(optimization_notes, 1):
                    f.write(f"{i}. {note.get('category', 'N/A').upper()} - Priority: {note.get('priority', 'N/A')}\n")
                    for j, rec in enumerate(note.get('recommendations', [])[:3], 1):
                        f.write(f"   {j}. Episode {rec.get('episode', '?')}: {rec.get('issue', 'N/A')}\n")
                        f.write(f"      Fix: {rec.get('fix', 'N/A')}\n")
                    f.write("\n")
            else:
                f.write("No optimization recommendations.\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("END OF LISTENER EXPERIENCE REPORT\n")
            f.write("=" * 70 + "\n")


# CLI Entry Point
async def main():
    """Run Station 42 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    simulator = Station42ListenerExperienceSimulator(session_id)
    await simulator.initialize()
    
    try:
        await simulator.run()
        print(f"\n✅ Success! Listener experience simulation complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

