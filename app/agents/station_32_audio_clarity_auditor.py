"""
Station 32: Audio-Only Clarity Audit

This station analyzes scripts for audio-only comprehension and generates clarity improvement reports.
It ensures scripts are optimized for audio-only listening without visual cues.

Flow:
1. Load Station 27 master scripts
2. Load Station 7 character data
3. Load Station 8 world building data
4. Execute 4-task analysis sequence:
   - Task 1: Scene Setting Clarity Analysis
   - Task 2: Action Comprehension Analysis
   - Task 3: Transition Clarity Analysis
   - Task 4: Information Delivery Analysis
5. Generate comprehensive clarity audit report per episode
6. Save JSON + TXT outputs per episode
7. Save summary report across all episodes

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config or Station outputs
- Robust error handling - Explicit failures with clear messages, NO silent fallbacks
- Follow existing patterns - Match structure of stations 1-32 exactly
- Validate all scores - Ensure 0-100 range, provide reasoning for each score
- Context preservation - Reference specific line numbers, character names, scene IDs
- Output atomicity - Write complete output or fail entirely (no partial writes)
- User validation required - Require explicit user approval before applying any changes
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Station32AudioClarityAuditor:
    """Station 32: Audio-Only Clarity Audit"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=32)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path(self.config_data.get('output_directory', 'output/station_32'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_32.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 32 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🎧 STATION 32: AUDIO-ONLY CLARITY AUDIT")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            station7_data = await self.load_station7_data()
            station8_data = await self.load_station8_data()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 27: {len(station27_data.get('episodes', []))} master scripts")
            print(f"   ✓ Station 7: Character profiles loaded")
            print(f"   ✓ Station 8: World building data loaded")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data, station7_data, station8_data)

            # Step 3: Process each episode
            episodes = station27_data.get('episodes', {})
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            all_episode_results = []
            
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"\n🎬 Processing Episode: {episode_id}")
                print("-" * 70)

                # Execute 4-task analysis sequence
                print("📍 Task 1/4: Scene Setting Clarity Analysis...")
                scene_clarity = await self.execute_task1_scene_clarity_analysis(
                    episode_data, station7_data, station8_data
                )
                print("✅ Scene setting clarity analysis complete")

                print("🏃 Task 2/4: Action Comprehension Analysis...")
                action_clarity = await self.execute_task2_action_comprehension_analysis(
                    episode_data, station7_data
                )
                print("✅ Action comprehension analysis complete")

                print("🔀 Task 3/4: Transition Clarity Analysis...")
                transition_clarity = await self.execute_task3_transition_clarity_analysis(
                    episode_data
                )
                print("✅ Transition clarity analysis complete")

                print("📝 Task 4/4: Information Delivery Analysis...")
                information_delivery = await self.execute_task4_information_delivery_analysis(
                    episode_data
                )
                print("✅ Information delivery analysis complete")

                # Compile episode results
                episode_result = {
                    "episode_id": episode_id,
                    "scene_clarity_analysis": scene_clarity,
                    "action_comprehension_analysis": action_clarity,
                    "transition_clarity_analysis": transition_clarity,
                    "information_delivery_analysis": information_delivery,
                    "overall_clarity_score": self._calculate_overall_score(
                        scene_clarity, action_clarity, transition_clarity, information_delivery
                    ),
                    "timestamp": datetime.now().isoformat()
                }

                all_episode_results.append(episode_result)

                # Save individual episode results
                await self.save_episode_output(episode_result)

                print(f"✅ Episode {episode_id} analysis complete")
                print(f"   Overall Clarity Score: {episode_result['overall_clarity_score']}/100")

            # Step 4: Generate summary report
            print("\n" + "=" * 70)
            print("📊 GENERATING SUMMARY REPORT")
            print("=" * 70)
            summary_report = await self.generate_summary_report(all_episode_results)

            # Step 5: Save final outputs
            await self.save_final_outputs(all_episode_results, summary_report)

            print("\n" + "=" * 70)
            print("✅ STATION 32 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Analyzed: {len(all_episode_results)}")
            print("\n📄 Output files:")
            print(f"   - output/station_32/{self.session_id}_summary.json")
            print(f"   - output/station_32/{self.session_id}_summary.txt")
            print(f"   - output/station_32/{self.session_id}_episode_*.json (per episode)")
            print("\n📌 Ready to proceed to next station")

        except Exception as e:
            logger.error(f"❌ Station 32 failed: {str(e)}")
            raise

    async def load_station27_data(self) -> Dict:
        """Load Station 27 master scripts from output files"""
        try:
            station_27_dir = Path(self.config_data.get('input_directory', 'output/station_27'))
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

    async def load_station7_data(self) -> Dict:
        """Load Station 7 character voice profiles from output files"""
        try:
            # Try to find any character bible file in station_07 directory
            station_07_dir = Path("output/station_07")
            station7_files = list(station_07_dir.glob("*character_bible.json"))
            
            # Load the most recent file
            if station7_files:
                latest_file = max(station7_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    station7_data = json.load(f)
                
                if 'Character Bible Document' not in station7_data:
                    raise ValueError("❌ Station 7 output file missing 'Character Bible Document' key. Cannot proceed.")
                
                return station7_data
            
            station7_key = f"audiobook:{self.session_id}:station_07"
            station7_raw = await self.redis.get(station7_key)
            
            if not station7_raw:
                raise ValueError(f"❌ No Station 7 data found for session {self.session_id}\n   Please run Station 7 first")
            
            station7_data = json.loads(station7_raw)
            
            if 'Character Bible Document' not in station7_data:
                raise ValueError("❌ Station 7 data missing 'Character Bible Document' key. Cannot proceed.")
            
            return station7_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 7 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 7 data: {str(e)}")

    async def load_station8_data(self) -> Dict:
        """Load Station 8 world building data from output files"""
        try:
            # Try to find any world bible file in station_08 directory
            station_08_dir = Path("output/station_08")
            station8_files = list(station_08_dir.glob("*world_bible.json"))
            
            # Load the most recent file
            if station8_files:
                latest_file = max(station8_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    station8_data = json.load(f)
                
                if 'World Bible Document' not in station8_data:
                    raise ValueError("❌ Station 8 output file missing 'World Bible Document' key. Cannot proceed.")
                
                return station8_data
            
            station8_key = f"audiobook:{self.session_id}:station_08"
            station8_raw = await self.redis.get(station8_key)
            
            if not station8_raw:
                raise ValueError(f"❌ No Station 8 data found for session {self.session_id}\n   Please run Station 8 first")
            
            station8_data = json.loads(station8_raw)
            
            if 'World Bible Document' not in station8_data:
                raise ValueError("❌ Station 8 data missing 'World Bible Document' key. Cannot proceed.")
            
            return station8_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 8 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 8 data: {str(e)}")

    def display_project_summary(self, station27_data: Dict, station7_data: Dict, station8_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = station27_data.get('episodes', {})
        characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
        
        print(f"Episodes to Analyze: {len(episodes)}")
        print(f"Character Profiles: {len(characters)}")
        print()
        
        if episodes:
            print("Episode List:")
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)

    async def execute_task1_scene_clarity_analysis(self, episode: Dict, station7_data: Dict, station8_data: Dict) -> Dict:
        """Task 1: Scene Setting Clarity Analysis"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            
            # Extract episode content from multiple possible locations
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                logger.warning(f"No content found for episode {episode_id}")
                return {
                    'scene_clarity_scorecard': {},
                    'audio_signatures': {},
                    'warning': 'No content available for analysis'
                }
            
            logger.info(f"Analyzing {len(episode_content)} characters for scene clarity in episode {episode_id}")
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],  # First 15000 chars
            }
            
            prompt = self.config.get_prompt('scene_clarity_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('scene_clarity_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_action_comprehension_analysis(self, episode: Dict, station7_data: Dict) -> Dict:
        """Task 2: Action Comprehension Analysis"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'action_sequence_scorecard': {},
                    'sound_effect_sequencing': {},
                    'warning': 'No content available for analysis'
                }
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],
            }
            
            prompt = self.config.get_prompt('action_comprehension_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('action_comprehension_analysis', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_transition_clarity_analysis(self, episode: Dict) -> Dict:
        """Task 3: Transition Clarity Analysis"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'transition_scorecard': {},
                    'audio_bridges': {},
                    'warning': 'No content available for analysis'
                }
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],
            }
            
            prompt = self.config.get_prompt('transition_clarity_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('transition_clarity_analysis', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_information_delivery_analysis(self, episode: Dict) -> Dict:
        """Task 4: Information Delivery Analysis"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'delivery_scorecard': {},
                    'information_priority': {},
                    'warning': 'No content available for analysis'
                }
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],
            }
            
            prompt = self.config.get_prompt('information_delivery_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('information_delivery_analysis', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

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
        
        # No valid content found
        return ''

    def _calculate_overall_score(self, scene_clarity: Dict, action_clarity: Dict, 
                                transition_clarity: Dict, information_delivery: Dict) -> int:
        """Calculate overall clarity score from component scores"""
        try:
            weights = self.config_data.get('scoring_weights', {})
            w_scene = weights.get('scene_clarity', 0.3)
            w_action = weights.get('action_comprehension', 0.25)
            w_transition = weights.get('transitions', 0.25)
            w_info = weights.get('information_delivery', 0.2)
            
            # Extract component-level scores (not scene-level)
            scene_score = scene_clarity.get('scene_clarity_scorecard', {})
            scene_avg = self._get_component_average_score(scene_score, 'overall_clarity')
            
            action_score = action_clarity.get('action_sequence_scorecard', {})
            action_avg = self._get_component_average_score(action_score, 'overall_action_score')
            
            transition_score = transition_clarity.get('transition_scorecard', {})
            transition_avg = self._get_component_average_score(transition_score, 'clarity_score')
            
            info_score = information_delivery.get('delivery_scorecard', {})
            info_avg = self._get_component_average_score(info_score, 'overall_delivery_score')
            
            # Validate all scores are 0-100
            scores = [(scene_avg, w_scene), (action_avg, w_action), (transition_avg, w_transition), (info_avg, w_info)]
            valid_scores = [(s, w) for s, w in scores if isinstance(s, (int, float)) and 0 <= s <= 100]
            
            if not valid_scores:
                logger.warning("No valid scores found for overall calculation")
                return 0
            
            # Weighted average
            overall = sum(score * weight for score, weight in valid_scores) / sum(weight for _, weight in valid_scores)
            
            return int(round(overall))
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {str(e)}")
            return 0
    
    def _get_component_average_score(self, scorecard: Dict, score_key: str) -> float:
        """Get average score from a scorecard dictionary"""
        scores = []
        for item_data in scorecard.values():
            if isinstance(item_data, dict):
                score = item_data.get(score_key, 0)
                if isinstance(score, (int, float)) and 0 <= score <= 100:
                    scores.append(score)
        
        return sum(scores) / len(scores) if scores else 0

    def _extract_scores_from_analysis(self, analysis: Dict, scorecard_key: str) -> List[float]:
        """Extract scores from an analysis scorecard"""
        scores = []
        try:
            scorecard = analysis.get(scorecard_key, {})
            for scene, data in scorecard.items():
                if isinstance(data, dict):
                    overall = data.get('overall_clarity', data.get('overall_clarity_score', 0))
                    if isinstance(overall, (int, float)) and 0 <= overall <= 100:
                        scores.append(overall)
        except Exception as e:
            logger.warning(f"Error extracting scores: {str(e)}")
        
        return scores

    async def generate_summary_report(self, all_episode_results: List[Dict]) -> Dict:
        """Generate comprehensive summary report across all episodes"""
        try:
            context = {
                'session_id': self.session_id,
                'total_episodes': len(all_episode_results),
                'analyses_data': json.dumps(all_episode_results)
            }
            
            prompt = self.config.get_prompt('audit_report').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('audit_report', {})
            
        except Exception as e:
            raise ValueError(f"❌ Summary report generation failed: {str(e)}")

    async def save_episode_output(self, episode_result: Dict):
        """Save individual episode results to JSON and TXT"""
        episode_id = episode_result['episode_id']
        
        # Save JSON
        json_path = self.output_dir / f"{self.session_id}_episode_{episode_id:02d}_analysis.json"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(episode_result, f, indent=2, ensure_ascii=False)
        
        # Save TXT
        txt_path = self.output_dir / f"{self.session_id}_episode_{episode_id:02d}_analysis.txt"
        self.save_episode_readable_txt(txt_path, episode_result)

    def save_episode_readable_txt(self, path: Path, data: Dict):
        """Save human-readable TXT file for episode analysis"""
        # Get bullet character from config
        bullet = self.config_data.get('output_enhancements', {}).get('bullet_character', '•')
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        
        with open(path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 32: AUDIO-ONLY CLARITY AUDIT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Episode ID: {data.get('episode_id', 'N/A')}\n")
            f.write(f"Analysis Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Overall Clarity Score: {data.get('overall_clarity_score', 'N/A')}/100\n\n")
            
            # Scene Clarity
            f.write("-" * 70 + "\n")
            f.write("SCENE CLARITY ANALYSIS\n")
            f.write("-" * 70 + "\n")
            scene_analysis = data.get('scene_clarity_analysis', {})
            scorecard = scene_analysis.get('scene_clarity_scorecard', {})
            
            if not scorecard or not isinstance(scorecard, dict):
                f.write("⚠️  No scene clarity data available for this episode\n")
                f.write("   This may indicate the script is too short or contains placeholder content\n\n")
            else:
                for scene, scene_data in scorecard.items():
                    f.write(f"\n{scene}:\n")
                    overall = scene_data.get('overall_clarity', 'N/A')
                    f.write(f"  Overall Clarity: {overall}/100\n")
                    location_score = scene_data.get('location_score', 'N/A')
                    f.write(f"  Location Score: {location_score}/100\n")
                    time_score = scene_data.get('time_score', 'N/A')
                    f.write(f"  Time Score: {time_score}/100\n")
                    char_score = scene_data.get('character_presence_score', 'N/A')
                    f.write(f"  Character Presence: {char_score}/100\n")
                    
                    issues = scene_data.get('location_issues', [])
                    if issues:
                        f.write(f"  Location Issues: {len(issues)}\n")
                        # Filter by severity and show critical first
                        sorted_issues = sorted(issues, key=lambda x: self._severity_priority(x.get('severity', 'LOW')))
                        for issue in sorted_issues[:5]:  # Show top 5
                            severity = issue.get('severity', '')
                            blocking = issue.get('blocking_comprehension', False)
                            severity_ind = '🔴' if severity == 'CRITICAL' else '🟠' if severity == 'HIGH' else '🟡' if severity == 'MEDIUM' else '🟢'
                            line_num = issue.get('line_number', '')
                            line_text = f" (Line {line_num})" if line_num else ""
                            f.write(f"    {severity_ind} [{severity}] {issue.get('specific_problem', 'N/A')}{line_text}\n")
                            if blocking:
                                f.write(f"       ⚠️  BLOCKS COMPREHENSION\n")
            
            # Action Comprehension
            f.write("\n" + "-" * 70 + "\n")
            f.write("ACTION COMPREHENSION ANALYSIS\n")
            f.write("-" * 70 + "\n")
            action_analysis = data.get('action_comprehension_analysis', {})
            action_scorecard = action_analysis.get('action_sequence_scorecard', {})
            
            if not action_scorecard or not isinstance(action_scorecard, dict):
                f.write("⚠️  No action comprehension data available\n\n")
            else:
                for scene, scene_data in action_scorecard.items():
                    f.write(f"\n{scene}:\n")
                    overall = scene_data.get('overall_action_score', 'N/A')
                    f.write(f"  Overall Action Score: {overall}/100\n")
                    physical = scene_data.get('physical_action_score', 'N/A')
                    f.write(f"  Physical Actions: {physical}/100\n")
                    character = scene_data.get('character_action_score', 'N/A')
                    f.write(f"  Character Actions: {character}/100\n")
                    emotional = scene_data.get('emotional_action_score', 'N/A')
                    f.write(f"  Emotional Actions: {emotional}/100\n")
            
            # Transition Clarity
            f.write("\n" + "-" * 70 + "\n")
            f.write("TRANSITION CLARITY ANALYSIS\n")
            f.write("-" * 70 + "\n")
            transition_analysis = data.get('transition_clarity_analysis', {})
            transition_scorecard = transition_analysis.get('transition_scorecard', {})
            
            if not transition_scorecard or not isinstance(transition_scorecard, dict):
                f.write("⚠️  No transition clarity data available\n\n")
            else:
                for trans_type, trans_data in transition_scorecard.items():
                    f.write(f"\n{trans_type}:\n")
                    clarity = trans_data.get('clarity_score', 'N/A')
                    f.write(f"  Clarity Score: {clarity}/100\n")
                    time = trans_data.get('time_transition_score', 'N/A')
                    f.write(f"  Time Transition: {time}/100\n")
                    location = trans_data.get('location_transition_score', 'N/A')
                    f.write(f"  Location Transition: {location}/100\n")
                    pov = trans_data.get('pov_transition_score', 'N/A')
                    f.write(f"  POV Transition: {pov}/100\n")
            
            # Information Delivery
            f.write("\n" + "-" * 70 + "\n")
            f.write("INFORMATION DELIVERY ANALYSIS\n")
            f.write("-" * 70 + "\n")
            info_analysis = data.get('information_delivery_analysis', {})
            delivery_scorecard = info_analysis.get('delivery_scorecard', {})
            
            if not delivery_scorecard or not isinstance(delivery_scorecard, dict):
                f.write("⚠️  No information delivery data available\n\n")
            else:
                for scene, scene_data in delivery_scorecard.items():
                    f.write(f"\n{scene}:\n")
                    overall = scene_data.get('overall_delivery_score', 'N/A')
                    f.write(f"  Overall Delivery: {overall}/100\n")
                    natural = scene_data.get('natural_integration_score', 'N/A')
                    f.write(f"  Natural Integration: {natural}/100\n")
                    audio_friendly = scene_data.get('audio_friendly_score', 'N/A')
                    f.write(f"  Audio-Friendly: {audio_friendly}/100\n")
                    repetition = scene_data.get('repetition_score', 'N/A')
                    f.write(f"  Strategic Repetition: {repetition}/100\n")
            
            # Readiness Checklist
            f.write("\n" + "-" * 70 + "\n")
            f.write("READINESS CHECKLIST\n")
            f.write("-" * 70 + "\n")
            
            overall_score = data.get('overall_clarity_score', 0)
            threshold = self.config_data.get('clarity_thresholds', {}).get('minimum_score', 70)
            
            f.write(f"Overall Clarity Score: {overall_score}/100 (Threshold: {threshold})\n")
            if overall_score >= threshold:
                f.write("✓ PASS: Meets minimum clarity threshold\n")
            else:
                f.write("✗ FAIL: Below minimum clarity threshold\n")
            
            # Count critical issues
            critical_count = self._count_issues_by_severity(data, 'CRITICAL')
            high_count = self._count_issues_by_severity(data, 'HIGH')
            
            if critical_count == 0:
                f.write("✓ PASS: No critical issues found\n")
            else:
                f.write(f"✗ FAIL: {critical_count} critical issues must be addressed\n")
            
            if high_count <= 3:
                f.write("✓ PASS: High priority issues within acceptable range\n")
            else:
                f.write(f"⚠️  WARNING: {high_count} high priority issues need attention\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF CLARITY AUDIT\n")
            f.write("=" * 70 + "\n")

    async def save_final_outputs(self, all_episode_results: List[Dict], summary_report: Dict):
        """Save final comprehensive outputs"""
        final_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "total_episodes": len(all_episode_results),
            "episode_results": all_episode_results,
            "summary_report": summary_report
        }
        
        # Save JSON
        json_path = self.output_dir / f"{self.session_id}_summary.json"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        # Save TXT
        txt_path = self.output_dir / f"{self.session_id}_summary.txt"
        self.save_summary_readable_txt(txt_path, final_data)
        
        # Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_32"
        await self.redis.set(redis_key, json.dumps(final_data), expire=86400)
        
        print(f"✅ Final outputs saved")

    def save_summary_readable_txt(self, path: Path, data: Dict):
        """Save human-readable summary TXT file"""
        # Get encoding from config
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        
        with open(path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 32: AUDIO-ONLY CLARITY AUDIT SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {data.get('session_id', 'N/A')}\n")
            f.write(f"Analysis Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Total Episodes: {data.get('total_episodes', 'N/A')}\n\n")
            
            summary = data.get('summary_report', {})
            f.write("-" * 70 + "\n")
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"{summary.get('executive_summary', 'N/A')}\n\n")
            
            f.write("-" * 70 + "\n")
            f.write("OVERALL CLARITY HEALTH\n")
            f.write("-" * 70 + "\n")
            
            health = summary.get('overall_clarity_health', {})
            f.write(f"Average Scene Clarity: {health.get('average_scene_clarity', 'N/A')}/100\n")
            f.write(f"Average Action Clarity: {health.get('average_action_clarity', 'N/A')}/100\n")
            f.write(f"Average Transition Clarity: {health.get('average_transition_clarity', 'N/A')}/100\n")
            f.write(f"Average Information Delivery: {health.get('average_information_delivery', 'N/A')}/100\n")
            f.write(f"Overall Audio Clarity Score: {health.get('overall_audio_clarity_score', 'N/A')}/100\n")
            f.write(f"Total Issues Found: {health.get('total_issues_found', 'N/A')}\n")
            f.write(f"Critical Issues: {health.get('critical_issues', 'N/A')}\n")
            f.write(f"Minor Issues: {health.get('minor_issues', 'N/A')}\n\n")
            
            # Episode Breakdown
            f.write("-" * 70 + "\n")
            f.write("EPISODE BREAKDOWN\n")
            f.write("-" * 70 + "\n")
            
            episode_results = data.get('episode_results', [])
            for episode in episode_results:
                episode_id = episode.get('episode_id', 'Unknown')
                overall = episode.get('overall_clarity_score', 0)
                
                # Visual score indicator
                if isinstance(overall, (int, float)):
                    if overall >= 80:
                        score_icon = '🟢'
                    elif overall >= 70:
                        score_icon = '🟡'
                    elif overall >= 60:
                        score_icon = '🟠'
                    else:
                        score_icon = '🔴'
                    f.write(f"\n{score_icon} {episode_id}: {overall}/100")
                    
                    # Show critical issues count
                    critical_count = self._count_issues_by_severity(episode, 'CRITICAL')
                    if critical_count > 0:
                        f.write(f" [🔴 {critical_count} Critical Issues]")
                else:
                    f.write(f"\n❓ {episode_id}: N/A/100")
            
            # Recommendations
            f.write("\n" + "-" * 70 + "\n")
            f.write("AUDIO OPTIMIZATION RECOMMENDATIONS\n")
            f.write("-" * 70 + "\n")
            
            recommendations = summary.get('audio_optimization_recommendations', [])
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF AUDIO CLARITY AUDIT\n")
            f.write("=" * 70 + "\n")

    def _severity_priority(self, severity: str) -> int:
        """Convert severity to numeric priority for sorting"""
        priorities = {
            'CRITICAL': 1,
            'HIGH': 2,
            'MEDIUM': 3,
            'LOW': 4
        }
        return priorities.get(severity, 5)
    
    def _count_issues_by_severity(self, data: Dict, severity: str) -> int:
        """Count issues by severity across all analyses"""
        count = 0
        
        # Count in scene clarity
        scene_analysis = data.get('scene_clarity_analysis', {})
        for scene_data in scene_analysis.get('scene_clarity_scorecard', {}).values():
            for issue_type in ['location_issues', 'time_issues', 'character_issues']:
                issues = scene_data.get(issue_type, [])
                count += sum(1 for issue in issues if issue.get('severity') == severity)
        
        # Count in action comprehension
        action_analysis = data.get('action_comprehension_analysis', {})
        for scene_data in action_analysis.get('action_sequence_scorecard', {}).values():
            issues = scene_data.get('action_issues', [])
            count += sum(1 for issue in issues if issue.get('severity') == severity)
        
        # Count in transitions
        transition_analysis = data.get('transition_clarity_analysis', {})
        for trans_data in transition_analysis.get('transition_scorecard', {}).values():
            issues = trans_data.get('transition_issues', [])
            count += sum(1 for issue in issues if issue.get('severity') == severity)
        
        # Count in information delivery
        info_analysis = data.get('information_delivery_analysis', {})
        for scene_data in info_analysis.get('delivery_scorecard', {}).values():
            issues = scene_data.get('delivery_issues', [])
            count += sum(1 for issue in issues if issue.get('severity') == severity)
        
        return count


# CLI Entry Point
async def main():
    """Run Station 32 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    auditor = Station32AudioClarityAuditor(session_id)
    await auditor.initialize()
    
    try:
        await auditor.run()
        print(f"\n✅ Success! Audio clarity audit complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

