"""
Station 33: Pacing & Energy Analyzer

This station analyzes episode pacing at micro (within episodes) and macro (across episodes) 
levels, identifying dead zones, overload points, and providing actionable pacing fixes.

Flow:
1. Load all episode scripts from Station 27
2. Execute 4-task analysis sequence:
   - Task 1: Micro-Pacing (within episodes)
   - Task 2: Macro-Pacing (across episodes)
   - Task 3: Attention Management
   - Task 4: Rhythm Solutions
3. Generate output files:
   - pacing_chart.json
   - energy_curve_data.json
   - problem_zones.json
   - pacing_fixes.json
   - pacing_analysis_report.md
4. Prompt user validation before applying fixes

Critical Pacing Analysis - Ensures optimal rhythm and energy management across series
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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Station33PacingEnergyAnalyzer:
    """Station 33: Pacing & Energy Analyzer"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=33)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path("output/station_33")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_33.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 33 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("⚡ STATION 33: PACING & ENERGY ANALYZER")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading all episode scripts...")
            station27_data = await self.load_station27_data()
            
            print("✅ All inputs loaded successfully")
            episodes = station27_data.get('episodes', {})
            print(f"   ✓ Station 27: {len(episodes)} master scripts")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data)

            # Step 3: Process all episodes - need complete dataset for macro analysis
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            # Verify we have complete dataset
            print(f"📊 Processing {len(episodes)} episodes for macro-pacing analysis...")
            print()

            all_episode_metrics = []
            error_log = []

            # Process each episode
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"🎬 Processing Episode: {episode_id}")
                print("-" * 70)

                try:
                    # Execute Task 1: Micro-Pacing Analysis
                    print("📏 Task 1/4: Micro-Pacing Analysis...")
                    micro_pacing = await self.execute_task1_micro_pacing(episode_data, episode_id)
                    print("✅ Micro-pacing analysis complete")

                    all_episode_metrics.append({
                        'episode_id': episode_id,
                        'micro_pacing': micro_pacing
                    })

                    print(f"✅ Episode {episode_id} analysis complete\n")

                except Exception as e:
                    error_msg = f"Error processing episode {episode_id}: {str(e)}"
                    logger.error(error_msg)
                    error_log.append(error_msg)
                    print(f"⚠️  {error_msg}\n")

            # Step 4: Execute Macro-Pacing Analysis (requires all episodes)
            print("\n" + "=" * 70)
            print("📊 TASK 2/4: MACRO-PACING ANALYSIS")
            print("=" * 70)
            print("Analyzing pacing patterns across all episodes...")
            macro_pacing = await self.execute_task2_macro_pacing(station27_data, all_episode_metrics)
            print("✅ Macro-pacing analysis complete\n")

            # Step 5: Execute Attention Management Analysis
            print("=" * 70)
            print("🎯 TASK 3/4: ATTENTION MANAGEMENT")
            print("=" * 70)
            print("Identifying problem zones...")
            attention_analysis = await self.execute_task3_attention_management(
                station27_data, all_episode_metrics
            )
            print("✅ Attention management analysis complete\n")

            # Step 6: Execute Rhythm Solutions
            print("=" * 70)
            print("🔧 TASK 4/4: RHYTHM SOLUTIONS")
            print("=" * 70)
            print("Generating pacing fixes...")
            rhythm_solutions = await self.execute_task4_rhythm_solutions(
                attention_analysis, all_episode_metrics
            )
            print("✅ Rhythm solutions generated\n")

            # Step 7: Generate output files
            print("=" * 70)
            print("💾 GENERATING OUTPUT FILES")
            print("=" * 70)
            await self.generate_output_files(
                all_episode_metrics,
                macro_pacing,
                attention_analysis,
                rhythm_solutions,
                error_log
            )
            print("✅ All output files generated")

            # Step 8: User validation prompt
            print("\n" + "=" * 70)
            print("🔍 USER VALIDATION REQUIRED")
            print("=" * 70)
            print("Review pacing_fixes.json before applying solutions.")
            
            try:
                response = input("Apply pacing fixes? [y/n]: ").strip().lower()
                if response == 'y':
                    print("✅ User approved pacing fixes")
                    # Here you would apply the fixes (implementation depends on requirements)
                else:
                    print("⏸️  Pacing fixes not applied (user review pending)")
            except (EOFError, KeyboardInterrupt):
                print("⏸️  Pacing fixes not applied (no user input available)")
            
            print("\n✅ Station 33 analysis complete!")

        except Exception as e:
            logger.error(f"Station 33 failed: {str(e)}")
            raise

    async def load_station27_data(self) -> Dict:
        """Load Station 27 master scripts from output files"""
        try:
            station_27_dir = Path("output/station_27")
            episodes = {}
            
            if not station_27_dir.exists():
                raise ValueError(f"❌ Station 27 directory not found: {station_27_dir}\n   Please run Station 27 first")
            
            # Load all episodes from Station 27
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
                raise ValueError(f"❌ No Station 27 episodes found in {station_27_dir}\n   Please run Station 27 first")
            
            return {'episodes': episodes}
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 27 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 27 data: {str(e)}")

    def display_project_summary(self, station27_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = station27_data.get('episodes', {})
        
        print(f"Total Episodes to Analyze: {len(episodes)}")
        print()
        
        if episodes:
            print("Episode List:")
            for episode_id, episode_data in episodes.items():
                production_pkg = episode_data.get('production_package', {})
                title = production_pkg.get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)

    async def execute_task1_micro_pacing(self, episode: Dict, episode_id: Any) -> Dict:
        """Task 1: Micro-Pacing Analysis (within episodes)"""
        try:
            # Extract episode content
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                logger.warning(f"No content found for episode {episode_id}")
                return {
                    'scene_length_distribution': {},
                    'dialogue_density': {},
                    'sound_density': {},
                    'emotional_pacing': {},
                    'warning': 'No content available for analysis'
                }
            
            # Get thresholds from config
            thresholds = self.config_data.get('thresholds', {})
            scene_length = thresholds.get('scene_length', {})
            
            context = {
                'episode_id': str(episode_id),
                'episode_content': episode_content[:15000],  # First 15000 chars
                'thresholds': json.dumps(thresholds),
                'short_max': scene_length.get('short_max', 120),
                'medium_max': scene_length.get('medium_max', 300)
            }
            
            prompt = self.config.get_prompt('micro_pacing_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('micro_pacing_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_macro_pacing(self, station27_data: Dict, episode_metrics: List[Dict]) -> Dict:
        """Task 2: Macro-Pacing Analysis (across episodes)"""
        try:
            # Build context from all episodes
            episodes = station27_data.get('episodes', {})
            episode_summaries = []
            
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                content = self._extract_episode_content(episode_data)
                
                episode_summaries.append({
                    'episode_id': str(episode_id),
                    'title': title,
                    'content_length': len(content) if content else 0
                })
            
            # Get episode metrics
            context = {
                'episode_summaries': json.dumps(episode_summaries),
                'episode_metrics': json.dumps(episode_metrics),
                'thresholds': json.dumps(self.config_data.get('thresholds', {}))
            }
            
            prompt = self.config.get_prompt('macro_pacing_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('macro_pacing_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 2 failed: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_attention_management(self, station27_data: Dict, episode_metrics: List[Dict]) -> Dict:
        """Task 3: Attention Management - Flag Problem Zones"""
        try:
            episodes = station27_data.get('episodes', {})
            episode_data_list = []
            
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                content = self._extract_episode_content(episode_data)
                
                episode_data_list.append({
                    'episode_id': str(episode_id),
                    'content': content[:10000] if content else ''
                })
            
            context = {
                'episode_data': json.dumps(episode_data_list),
                'thresholds': json.dumps(self.config_data.get('thresholds', {}))
            }
            
            prompt = self.config.get_prompt('attention_management').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('attention_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 3 failed: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_rhythm_solutions(self, attention_analysis: Dict, episode_metrics: List[Dict]) -> Dict:
        """Task 4: Rhythm Solutions - Generate Specific Fixes"""
        try:
            context = {
                'attention_analysis': json.dumps(attention_analysis),
                'episode_metrics': json.dumps(episode_metrics)
            }
            
            prompt = self.config.get_prompt('rhythm_solutions').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('rhythm_solutions', {})
            
        except Exception as e:
            logger.error(f"Task 4 failed: {str(e)}")
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    def _extract_episode_content(self, episode: Dict) -> str:
        """Extract content from episode data"""
        # Try multiple locations
        format_conv = episode.get('format_conversion', {})
        
        # Try fountain script first
        fountain = format_conv.get('fountain_script', '')
        if fountain and fountain.strip() and 'Complete full episode script' not in fountain:
            return fountain
        
        # Try markdown
        markdown = format_conv.get('markdown_script', '')
        if markdown and markdown.strip() and 'Complete full episode script' not in markdown:
            return markdown
        
        # Try master script text (but skip if it's a placeholder)
        master_text = episode.get('master_script_assembly', {}).get('master_script_text', '')
        if master_text and master_text.strip() and 'Complete full episode script' not in master_text:
            return master_text
        
        return ''

    async def generate_output_files(
        self,
        episode_metrics: List[Dict],
        macro_pacing: Dict,
        attention_analysis: Dict,
        rhythm_solutions: Dict,
        error_log: List[str]
    ):
        """Generate all output files"""
        
        # 1. pacing_chart.json
        pacing_chart = {
            'generated_at': datetime.now().isoformat(),
            'episode_metrics': episode_metrics,
            'summary': {
                'total_episodes': len(episode_metrics),
                'average_scene_count': self._calculate_avg_scenes(episode_metrics),
                'average_duration': self._calculate_avg_duration(episode_metrics)
            }
        }
        
        with open(self.output_dir / 'pacing_chart.json', 'w', encoding='utf-8') as f:
            json.dump(pacing_chart, f, indent=2, ensure_ascii=False)
        
        # 2. energy_curve_data.json
        energy_curve = {
            'generated_at': datetime.now().isoformat(),
            'energy_ratings': self._extract_energy_ratings(episode_metrics),
            'energy_trend': self._analyze_energy_trend(episode_metrics)
        }
        
        with open(self.output_dir / 'energy_curve_data.json', 'w', encoding='utf-8') as f:
            json.dump(energy_curve, f, indent=2, ensure_ascii=False)
        
        # 3. problem_zones.json
        problem_zones = {
            'generated_at': datetime.now().isoformat(),
            'dead_zones': attention_analysis.get('dead_zones', []),
            'overload_zones': attention_analysis.get('overload_zones', []),
            'repetition_fatigue': attention_analysis.get('repetition_fatigue', []),
            'audio_fatigue': attention_analysis.get('audio_fatigue', [])
        }
        
        with open(self.output_dir / 'problem_zones.json', 'w', encoding='utf-8') as f:
            json.dump(problem_zones, f, indent=2, ensure_ascii=False)
        
        # 4. pacing_fixes.json
        pacing_fixes = {
            'generated_at': datetime.now().isoformat(),
            'fixes': rhythm_solutions.get('fixes', []),
            'recommendations': rhythm_solutions.get('recommendations', []),
            'implementation_notes': rhythm_solutions.get('implementation_notes', [])
        }
        
        with open(self.output_dir / 'pacing_fixes.json', 'w', encoding='utf-8') as f:
            json.dump(pacing_fixes, f, indent=2, ensure_ascii=False)
        
        # 5. pacing_analysis_report.md
        report = self._generate_markdown_report(
            pacing_chart, energy_curve, problem_zones, pacing_fixes, error_log
        )
        
        with open(self.output_dir / 'pacing_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 6. error_log.txt (if errors exist)
        if error_log:
            with open(self.output_dir / 'error_log.txt', 'w', encoding='utf-8') as f:
                f.write("ERROR LOG\n")
                f.write("=" * 70 + "\n\n")
                for error in error_log:
                    f.write(f"❌ {error}\n")
    
    def _calculate_avg_scenes(self, episode_metrics: List[Dict]) -> float:
        """Calculate average scene count"""
        scene_counts = []
        for ep in episode_metrics:
            scenes = ep.get('micro_pacing', {}).get('scene_length_distribution', {}).get('total_scenes', 0)
            if scenes > 0:
                scene_counts.append(scenes)
        return sum(scene_counts) / len(scene_counts) if scene_counts else 0
    
    def _calculate_avg_duration(self, episode_metrics: List[Dict]) -> float:
        """Calculate average duration"""
        durations = []
        for ep in episode_metrics:
            duration = ep.get('micro_pacing', {}).get('total_duration', {}).get('minutes', 0)
            if duration > 0:
                durations.append(duration)
        return sum(durations) / len(durations) if durations else 0
    
    def _extract_energy_ratings(self, episode_metrics: List[Dict]) -> List[Dict]:
        """Extract energy ratings per episode"""
        ratings = []
        for ep in episode_metrics:
            episode_id = ep.get('episode_id')
            energy = ep.get('micro_pacing', {}).get('energy_rating', 5)
            ratings.append({
                'episode_id': episode_id,
                'energy_rating': energy
            })
        return ratings
    
    def _analyze_energy_trend(self, episode_metrics: List[Dict]) -> str:
        """Analyze energy trend"""
        ratings = [ep.get('micro_pacing', {}).get('energy_rating', 5) for ep in episode_metrics]
        if not ratings:
            return "Insufficient data"
        
        first_half = ratings[:len(ratings)//2]
        second_half = ratings[len(ratings)//2:]
        
        avg_first = sum(first_half) / len(first_half) if first_half else 5
        avg_second = sum(second_half) / len(second_half) if second_half else 5
        
        if avg_second > avg_first + 1:
            return "Building"
        elif avg_second < avg_first - 1:
            return "Declining"
        else:
            return "Stable"
    
    def _generate_markdown_report(
        self, 
        pacing_chart: Dict, 
        energy_curve: Dict, 
        problem_zones: Dict, 
        pacing_fixes: Dict,
        error_log: List[str]
    ) -> str:
        """Generate human-readable markdown report"""
        report = f"""# Pacing & Energy Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

Total Episodes Analyzed: {pacing_chart['summary']['total_episodes']}
Average Scene Count: {pacing_chart['summary']['average_scene_count']:.1f}
Average Duration: {pacing_chart['summary']['average_duration']:.1f} minutes

## Energy Analysis

Energy Trend: {energy_curve['energy_trend']}

### Energy Ratings by Episode
"""
        
        for rating in energy_curve['energy_ratings']:
            episode_id = rating['episode_id']
            energy = rating['energy_rating']
            bar = '█' * energy
            report += f"- Episode {episode_id}: {energy}/10 {bar}\n"
        
        report += "\n## Problem Zones Identified\n\n"
        
        dead_zones = problem_zones.get('dead_zones', [])
        report += f"### Dead Zones: {len(dead_zones)}\n"
        for zone in dead_zones[:5]:  # Show first 5
            report += f"- {zone}\n"
        
        overload_zones = problem_zones.get('overload_zones', [])
        report += f"\n### Overload Zones: {len(overload_zones)}\n"
        for zone in overload_zones[:5]:
            report += f"- {zone}\n"
        
        report += "\n## Pacing Fixes Recommended\n\n"
        fixes = pacing_fixes.get('fixes', [])
        for i, fix in enumerate(fixes[:10], 1):  # Show first 10
            report += f"{i}. {fix}\n"
        
        if error_log:
            report += "\n## Errors Encountered\n\n"
            for error in error_log:
                report += f"- ❌ {error}\n"
        
        return report


async def main():
    """Run Station 33 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    analyzer = Station33PacingEnergyAnalyzer(session_id)
    await analyzer.initialize()
    
    try:
        await analyzer.run()
        print(f"\n✅ Success! Pacing & energy analysis complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
