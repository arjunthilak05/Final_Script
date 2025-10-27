"""
Station 31: Dialogue Naturalness Pass

This station analyzes dialogue for audiobook speakability, naturalness, identity clarity, and subtext layers.
It serves as a speech naturalizer that ensures dialogue sounds authentic and speaks naturally.

Flow:
1. Load Station 30 validated scripts
2. Load Station 7 character voice profiles
3. Load Station 24 polished dialogue for reference
4. Execute 4-task analysis sequence:
   - Task 1: Speakability Check (tongue twisters, breath length, word order)
   - Task 2: Naturalness Scoring (vocabulary, sentence structure, filler words)
   - Task 3: Identity Clarity (character identification, verbal tics, uniqueness)
   - Task 4: Subtext Verification (3-layer analysis: surface, underlying, withheld)
5. Generate comprehensive naturalness scorecard per episode
6. Save JSON + TXT outputs per episode
7. Save summary report across all episodes

Critical Speech Naturalization - Ensures dialogue is speakable and natural for audiobook production
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


class Station31DialogueNaturalness:
    """Station 31: Dialogue Naturalness Pass"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=31)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path("output/station_31")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_31.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 31 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🗣️  STATION 31: DIALOGUE NATURALNESS PASS")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station30_data()  # Loads from Station 27
            station7_data = await self.load_station7_data()
            station24_data = await self.load_station24_data()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 27: {len(station27_data.get('episodes', []))} master scripts")
            print(f"   ✓ Station 7: Character voice profiles loaded")
            print(f"   ✓ Station 24: Polished dialogue reference loaded")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data, station7_data, station24_data)

            # Step 3: Process each episode
            episodes = station27_data.get('episodes', [])
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            all_episode_results = []
            
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"\n🎬 Processing Episode: {episode_id}")
                print("-" * 70)

                # Execute 4-task analysis sequence
                print("🔤 Task 1/4: Speakability Check...")
                speakability = await self.execute_task1_speakability_check(
                    episode_data, station7_data
                )
                print("✅ Speakability check complete")

                print("📊 Task 2/4: Naturalness Scoring...")
                naturalness = await self.execute_task2_naturalness_scoring(
                    episode_data, station7_data, station24_data
                )
                print("✅ Naturalness scoring complete")

                print("🎭 Task 3/4: Identity Clarity Analysis...")
                identity_clarity = await self.execute_task3_identity_clarity(
                    episode_data, station7_data
                )
                print("✅ Identity clarity analysis complete")

                print("📖 Task 4/4: Subtext Verification...")
                subtext_verification = await self.execute_task4_subtext_verification(
                    episode_data, naturalness, identity_clarity
                )
                print("✅ Subtext verification complete")

                # Compile episode results
                episode_result = {
                    "episode_id": episode_id,
                    "speakability_analysis": speakability,
                    "naturalness_scorecard": naturalness,
                    "identity_clarity": identity_clarity,
                    "subtext_layers": subtext_verification,
                    "timestamp": datetime.now().isoformat()
                }

                all_episode_results.append(episode_result)

                # Save individual episode results
                await self.save_episode_output(episode_result)

                print(f"✅ Episode {episode_id} analysis complete")

            # Step 4: Generate summary report
            print("\n" + "=" * 70)
            print("📊 GENERATING SUMMARY REPORT")
            print("=" * 70)
            summary_report = await self.generate_summary_report(all_episode_results, station27_data)

            # Step 5: Save final outputs
            await self.save_final_outputs(all_episode_results, summary_report)

            print("\n" + "=" * 70)
            print("✅ STATION 31 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Analyzed: {len(all_episode_results)}")
            print("\n📄 Output files:")
            print(f"   - output/station_31/{self.session_id}_summary.json")
            print(f"   - output/station_31/{self.session_id}_summary.txt")
            print(f"   - output/station_31/{self.session_id}_episode_*.json (per episode)")
            print("\n📌 Ready to proceed to next station")

        except Exception as e:
            logger.error(f"❌ Station 31 failed: {str(e)}")
            raise

    async def load_station30_data(self) -> Dict:
        """Load Station 27 master scripts (which Station 31 analyzes)"""
        try:
            # Station 31 analyzes Station 27 master scripts for naturalness
            # Load from Station 27 episode directories
            station_27_dir = Path("output/station_27")
            episodes = {}
            
            if not station_27_dir.exists():
                raise ValueError(f"❌ Station 27 directory not found for session {self.session_id}\n   Please run Station 27 first")
            
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
                raise ValueError(f"❌ No Station 27 episodes found for session {self.session_id}\n   Please run Station 27 first")
            
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

    async def load_station24_data(self) -> Dict:
        """Load Station 24 polished dialogue for reference"""
        try:
            # Load from episode subdirectories
            station_24_dir = Path("output/station_24")
            episodes_data = {}
            
            if station_24_dir.exists():
                for episode_dir in station_24_dir.iterdir():
                    if episode_dir.is_dir() and episode_dir.name.startswith("episode_"):
                        try:
                            episode_num = int(episode_dir.name.split("_")[1])
                            json_file = episode_dir / f"episode_{episode_num:02d}_dialogue_polished.json"
                            
                            if json_file.exists():
                                with open(json_file, 'r', encoding='utf-8') as f:
                                    episode_data = json.load(f)
                                    episodes_data[episode_num] = episode_data
                        except (ValueError, KeyError, json.JSONDecodeError):
                            continue
            
            return {'episodes': episodes_data}
            
        except Exception as e:
            logger.warning(f"Could not load Station 24 data: {str(e)}")
            return {'episodes': {}}

    def display_project_summary(self, station27_data: Dict, station7_data: Dict, station24_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = station27_data.get('episodes', [])
        characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
        polished_episodes = station24_data.get('episodes', {})
        
        print(f"Episodes to Analyze: {len(episodes)}")
        print(f"Character Profiles: {len(characters)}")
        print(f"Polished Reference Episodes: {len(polished_episodes)}")
        print()
        
        if episodes:
            print("Episode List:")
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)

    async def execute_task1_speakability_check(self, episode: Dict, station7_data: Dict) -> Dict:
        """Task 1: Speakability Check"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            
            # Extract dialogue content from multiple possible locations
            episode_content = self._extract_dialogue_content(episode)
            
            if not episode_content:
                logger.warning(f"No dialogue content found for episode {episode_id}")
                return {
                    'speakability_issues': [],
                    'tongue_twisters_detected': [],
                    'breath_length_problems': [],
                    'word_order_issues': [],
                    'total_issues': 0,
                    'warning': 'No dialogue content available for analysis'
                }
            
            logger.info(f"Analyzing {len(episode_content)} characters of dialogue for episode {episode_id}")
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            
            # Load thresholds from config
            breath_length = self.config_data.get('breath_length_threshold', 150)
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:10000],  # First 10000 chars
                'characters': json.dumps(characters),
                'breath_length_threshold': breath_length
            }
            
            prompt = self.config.get_prompt('speakability_check').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('speakability_analysis', {})
            
        except Exception as e:
            logger.error(f"Task 1 failed: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")
    
    def _extract_dialogue_content(self, episode: Dict) -> str:
        """Extract dialogue content from episode data"""
        # Try format_conversion.fountain_script first (most complete)
        format_conv = episode.get('format_conversion', {})
        fountain_script = format_conv.get('fountain_script', '')
        if fountain_script and fountain_script.strip() != '':
            return fountain_script
        
        # Try markdown script
        markdown_script = format_conv.get('markdown_script', '')
        if markdown_script and markdown_script.strip() != '':
            return markdown_script
        
        # Try master_script_text (but check if it's not a placeholder)
        master_text = episode.get('master_script_assembly', {}).get('master_script_text', '')
        if master_text and master_text.strip() not in ['Complete full episode script with all audio markup and formatting...', '']:
            return master_text
        
        # No valid content found
        return ''

    async def execute_task2_naturalness_scoring(self, episode: Dict, station7_data: Dict, station24_data: Dict) -> Dict:
        """Task 2: Naturalness Scoring"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_dialogue_content(episode)
            
            if not episode_content:
                return {
                    'character_naturalness': {},
                    'vocabulary_scores': {},
                    'sentence_structure_scores': {},
                    'filler_word_analysis': {},
                    'interruption_overlap_analysis': {},
                    'warning': 'No dialogue content available for analysis'
                }
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            # Get polished reference - episode_id might be int already
            ep_id = episode_id if isinstance(episode_id, int) else (int(episode_id) if str(episode_id).isdigit() else 0)
            polished_reference = station24_data.get('episodes', {}).get(ep_id, {})
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:10000],
                'characters': json.dumps(characters),
                'polished_reference': json.dumps(polished_reference.get('dialogue_polished_script', {}))
            }
            
            prompt = self.config.get_prompt('naturalness_scoring').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('naturalness_scorecard', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_identity_clarity(self, episode: Dict, station7_data: Dict) -> Dict:
        """Task 3: Identity Clarity Analysis"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_dialogue_content(episode)
            
            if not episode_content:
                return {
                    'character_identification': {},
                    'voice_distinction_scores': {},
                    'verbal_ticks_usage': {},
                    'relationship_clarity': {},
                    'warning': 'No dialogue content available for analysis'
                }
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            min_score = self.config_data.get('min_character_distinction_score', 0.7)
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:10000],
                'characters': json.dumps(characters),
                'min_distinction_score': min_score
            }
            
            prompt = self.config.get_prompt('identity_clarity').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('identity_clarity', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_subtext_verification(self, episode: Dict, naturalness: Dict, identity_clarity: Dict) -> Dict:
        """Task 4: Subtext Verification"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_dialogue_content(episode)
            
            if not episode_content:
                return {
                    'subtext_layers': {},
                    'surface_meaning_analysis': {},
                    'underlying_meaning_analysis': {},
                    'withheld_information_cues': {},
                    'warning': 'No dialogue content available for analysis'
                }
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:10000],
                'naturalness_data': json.dumps(naturalness),
                'identity_data': json.dumps(identity_clarity)
            }
            
            prompt = self.config.get_prompt('subtext_verification').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('subtext_verification', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    async def generate_summary_report(self, all_episode_results: List[Dict], station27_data: Dict) -> Dict:
        """Generate comprehensive summary report across all episodes"""
        try:
            context = {
                'session_id': self.session_id,
                'episode_results': json.dumps(all_episode_results),
                'total_episodes': len(all_episode_results)
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
            raise ValueError(f"❌ Summary report generation failed: {str(e)}")

    async def save_episode_output(self, episode_result: Dict):
        """Save individual episode results to JSON and TXT"""
        episode_id = episode_result['episode_id']
        
        # Save JSON
        json_path = self.output_dir / f"{self.session_id}_{episode_id}_analysis.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(episode_result, f, indent=2, ensure_ascii=False)
        
        # Save TXT
        txt_path = self.output_dir / f"{self.session_id}_{episode_id}_analysis.txt"
        self.save_episode_readable_txt(txt_path, episode_result)

    def save_episode_readable_txt(self, path: Path, data: Dict):
        """Save human-readable TXT file for episode analysis"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 31: DIALOGUE NATURALNESS ANALYSIS\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Episode ID: {data.get('episode_id', 'N/A')}\n")
            f.write(f"Analysis Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Session ID: {self.session_id}\n\n")
            
            # Speakability Analysis
            f.write("-" * 70 + "\n")
            f.write("SPEAKABILITY CHECK\n")
            f.write("-" * 70 + "\n")
            speakability = data.get('speakability_analysis', {})
            issues = speakability.get('speakability_issues', [])
            f.write(f"Total Issues Found: {speakability.get('total_issues', 0)}\n\n")
            
            for issue in issues[:10]:  # Show first 10
                f.write(f"• {issue.get('issue_type', 'Unknown')}: {issue.get('location', 'N/A')}\n")
                f.write(f"  Problem: {issue.get('problem', 'N/A')}\n")
                f.write(f"  Fix: {issue.get('recommended_fix', 'N/A')}\n\n")
            
            # Naturalness Scorecard
            f.write("-" * 70 + "\n")
            f.write("NATURALNESS SCORECARD\n")
            f.write("-" * 70 + "\n")
            naturalness = data.get('naturalness_scorecard', {})
            character_scores = naturalness.get('character_naturalness', {})
            
            for char, scores in character_scores.items():
                f.write(f"\n{char}:\n")
                f.write(f"  Vocabulary Score: {scores.get('vocabulary_score', 'N/A')}/5\n")
                f.write(f"  Sentence Structure Score: {scores.get('sentence_structure_score', 'N/A')}/5\n")
                f.write(f"  Overall Naturalness: {scores.get('overall_score', 'N/A')}/5\n")
            
            # Identity Clarity
            f.write("\n" + "-" * 70 + "\n")
            f.write("IDENTITY CLARITY\n")
            f.write("-" * 70 + "\n")
            identity = data.get('identity_clarity', {})
            dist_scores = identity.get('voice_distinction_scores', {})
            
            for char, score in dist_scores.items():
                f.write(f"{char}: {score}/5\n")
            
            # Subtext Layers
            f.write("\n" + "-" * 70 + "\n")
            f.write("SUBTEXT VERIFICATION\n")
            f.write("-" * 70 + "\n")
            subtext = data.get('subtext_layers', {})
            layers = subtext.get('dialogue_layers', [])
            
            for layer in layers[:5]:  # Show first 5
                f.write(f"Line: {layer.get('dialogue_line', 'N/A')}\n")
                f.write(f"  Surface: {layer.get('surface_meaning', 'N/A')}\n")
                f.write(f"  Underlying: {layer.get('underlying_meaning', 'N/A')}\n")
                f.write(f"  Withheld: {layer.get('withheld_information', 'N/A')}\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("END OF NATURALNESS ANALYSIS\n")
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
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        # Save TXT
        txt_path = self.output_dir / f"{self.session_id}_summary.txt"
        self.save_summary_readable_txt(txt_path, final_data)
        
        # Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_31"
        await self.redis.set(redis_key, json.dumps(final_data), expire=86400)
        
        print(f"✅ Final outputs saved")

    def save_summary_readable_txt(self, path: Path, data: Dict):
        """Save human-readable summary TXT file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 31: DIALOGUE NATURALNESS SUMMARY\n")
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
            f.write("OVERALL NATURALNESS SCORES\n")
            f.write("-" * 70 + "\n")
            
            episode_results = data.get('episode_results', [])
            for episode in episode_results:
                episode_id = episode.get('episode_id', 'Unknown')
                naturalness = episode.get('naturalness_scorecard', {})
                
                f.write(f"\n{episode_id}:\n")
                f.write(f"  Characters Analyzed: {len(naturalness.get('character_naturalness', {}))}\n")
                avg_score = sum(
                    scores.get('overall_score', 0) 
                    for scores in naturalness.get('character_naturalness', {}).values()
                ) / len(naturalness.get('character_naturalness', {})) if naturalness.get('character_naturalness') else 0
                f.write(f"  Average Naturalness Score: {avg_score:.1f}/5\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF DIALOGUE NATURALNESS ANALYSIS\n")
            f.write("=" * 70 + "\n")


# CLI Entry Point
async def main():
    """Run Station 31 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    validator = Station31DialogueNaturalness(session_id)
    await validator.initialize()
    
    try:
        await validator.run()
        print(f"\n✅ Success! Dialogue naturalness analysis complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
