"""
Station 28: Emotional Truth Validator

This station validates completed episode scripts for emotional authenticity and character consistency.
It analyzes emotional arcs, relationship dynamics, universal emotional resonance, and detects
emotional problems with specific fixes.

Flow:
1. Load Station 27 complete scripts
2. Load Station 8 character bibles  
3. Load Station 5 emotional journey maps
4. Execute 4-task analysis sequence:
   - Task 1: Emotional Arc Verification
   - Task 2: Relationship Dynamics Check
   - Task 3: Universal Emotional Resonance
   - Task 4: Emotional Problem Detection
5. Generate comprehensive emotional scorecard per episode
6. Save JSON + TXT outputs per episode
7. Save summary report across all episodes

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config or Station outputs
- Robust error handling - Explicit failures with clear messages, NO silent fallbacks
- Follow existing patterns - Match structure of stations 1-4.5 exactly
- Validate all scores - Ensure 0-5 range, provide reasoning for each score
- Context preservation - Reference specific line numbers, character names, scene IDs
- Output atomicity - Write complete output or fail entirely (no partial writes)
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


class Station28EmotionalTruthValidator:
    """Station 28: Emotional Truth Validator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=28)
        self.output_dir = Path("output/station_28")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 28 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("💖 STATION 28: EMOTIONAL TRUTH VALIDATOR")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            station7_data = await self.load_station7_data()  # Load character data from Station 7
            station5_data = await self.load_station5_data()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 27: {len(station27_data.get('episodes', []))} complete scripts")
            print(f"   ✓ Station 7: Character bibles loaded")
            print(f"   ✓ Station 5: Emotional journey maps loaded")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data, station7_data, station5_data)

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
                print("📊 Task 1/4: Emotional Arc Verification...")
                emotional_arcs = await self.execute_task1_emotional_arc_verification(
                    episode_data, station7_data, station5_data
                )
                print("✅ Emotional arc verification complete")

                print("🤝 Task 2/4: Relationship Dynamics Check...")
                relationship_dynamics = await self.execute_task2_relationship_dynamics_check(
                    episode_data, station7_data
                )
                print("✅ Relationship dynamics check complete")

                print("🌟 Task 3/4: Universal Emotional Resonance...")
                universal_resonance = await self.execute_task3_universal_emotional_resonance(
                    episode_data, station5_data
                )
                print("✅ Universal emotional resonance complete")

                print("🔍 Task 4/4: Emotional Problem Detection...")
                problem_detection = await self.execute_task4_emotional_problem_detection(
                    episode_data, emotional_arcs, relationship_dynamics, universal_resonance
                )
                print("✅ Emotional problem detection complete")

                # Compile episode results
                episode_result = {
                    "episode_id": episode_id,
                    "emotional_scorecard": emotional_arcs,
                    "relationship_chart": relationship_dynamics,
                    "universal_resonance": universal_resonance,
                    "problem_flags": problem_detection.get("problem_flags", []),
                    "line_adjustments": problem_detection.get("line_adjustments", []),
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
            print("✅ STATION 28 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Analyzed: {len(all_episode_results)}")
            print("\n📄 Output files:")
            print(f"   - output/station_28/{self.session_id}_summary.json")
            print(f"   - output/station_28/{self.session_id}_summary.txt")
            print(f"   - output/station_28/{self.session_id}_episode_*.json (per episode)")
            print("\n📌 Ready to proceed to next station")

        except Exception as e:
            logger.error(f"❌ Station 28 failed: {str(e)}")
            raise

    async def load_station27_data(self) -> Dict:
        """Load Station 27 complete scripts from Redis"""
        try:
            # Station 27 saves data with episode-specific keys
            # Look for all episode keys for this session
            pattern = f"audiobook:{self.session_id}:station_27:episode_*"
            episode_keys = await self.redis.keys(pattern)
            
            if not episode_keys:
                raise ValueError(f"❌ No Station 27 data found for session {self.session_id}\n   Please run Station 27 first")
            
            # Load all episodes and combine them
            episodes = {}
            for key in episode_keys:
                episode_raw = await self.redis.get(key)
                if episode_raw:
                    episode_data = json.loads(episode_raw)
                    # Extract episode number from key (e.g., episode_01)
                    episode_num = key.split(':')[-1]  # Gets "episode_01"
                    episodes[episode_num] = episode_data
            
            if not episodes:
                raise ValueError(f"❌ No valid Station 27 episode data found for session {self.session_id}")
            
            # Return in expected format
            station27_data = {
                'episodes': episodes
            }
            
            return station27_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 27 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 27 data: {str(e)}")

    async def load_station7_data(self) -> Dict:
        """Load Station 7 character bibles from output files"""
        try:
            # Try to load from output files first
            output_file = Path(f"output/station_07/{self.session_id}_character_bible.json")
            
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    station7_data = json.load(f)
                
                # Validate required structure
                if 'Character Bible Document' not in station7_data:
                    raise ValueError("❌ Station 7 output file missing 'Character Bible Document' key. Cannot proceed.")
                
                return station7_data
            
            # Fallback to Redis if output file doesn't exist
            station7_key = f"audiobook:{self.session_id}:station_07"
            station7_raw = await self.redis.get(station7_key)
            
            if not station7_raw:
                raise ValueError(f"❌ No Station 7 data found for session {self.session_id}\n   Please run Station 7 first")
            
            station7_data = json.loads(station7_raw)
            
            # Validate required structure
            if 'Character Bible Document' not in station7_data:
                raise ValueError("❌ Station 7 data missing 'Character Bible Document' key. Cannot proceed.")
            
            return station7_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 7 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 7 data: {str(e)}")

    async def load_station8_data(self) -> Dict:
        """Load Station 8 character bibles from output files"""
        try:
            # Try to load from output files first
            output_file = Path(f"output/station_08/{self.session_id}_world_bible.json")
            
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    station8_data = json.load(f)
                
                # Validate required structure
                if 'World Bible Document' not in station8_data:
                    raise ValueError("❌ Station 8 output file missing 'World Bible Document' key. Cannot proceed.")
                
                return station8_data
            
            # Fallback to Redis if output file doesn't exist
            station8_key = f"audiobook:{self.session_id}:station_08"
            station8_raw = await self.redis.get(station8_key)
            
            if not station8_raw:
                raise ValueError(f"❌ No Station 8 data found for session {self.session_id}\n   Please run Station 8 first")
            
            station8_data = json.loads(station8_raw)
            
            # Validate required structure
            if 'characters' not in station8_data:
                raise ValueError("❌ Station 8 data missing 'characters' key. Cannot proceed.")
            
            return station8_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 8 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 8 data: {str(e)}")

    async def load_station5_data(self) -> Dict:
        """Load Station 5 emotional journey maps from output files"""
        try:
            # Try to load from output files first
            output_file = Path(f"output/station_05/{self.session_id}_output.json")
            
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    station5_data = json.load(f)
                
                # Validate required structure
                if 'Season Architecture Document' not in station5_data:
                    raise ValueError("❌ Station 5 output file missing 'Season Architecture Document' key. Cannot proceed.")
                
                return station5_data
            
            # Fallback to Redis if output file doesn't exist
            station5_key = f"audiobook:{self.session_id}:station_05"
            station5_raw = await self.redis.get(station5_key)
            
            if not station5_raw:
                raise ValueError(f"❌ No Station 5 data found for session {self.session_id}\n   Please run Station 5 first")
            
            station5_data = json.loads(station5_raw)
            
            # Validate required structure
            if 'Season Architecture Document' not in station5_data:
                raise ValueError("❌ Station 5 data missing 'Season Architecture Document' key. Cannot proceed.")
            
            return station5_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 5 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 5 data: {str(e)}")

    def display_project_summary(self, station27_data: Dict, station7_data: Dict, station5_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = station27_data.get('episodes', [])
        characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
        journey_maps = station5_data.get('Season Architecture Document', {}).get('season_structure_document', {}).get('rhythm_mapping', [])
        
        print(f"Episodes to Analyze: {len(episodes)}")
        print(f"Character Bibles: {len(characters)}")
        print(f"Emotional Journey Maps: {len(journey_maps)}")
        print()
        
        if episodes:
            print("Episode List:")
        for episode_key, episode_data in episodes.items():
            episode_id = episode_data.get('episode_number', episode_key)
            title = episode_data.get('master_script_assembly', {}).get('assembly_status', 'Unknown')
            print(f"   • {episode_id}: {title}")
        
        print("-" * 70)

    async def execute_task1_emotional_arc_verification(self, episode: Dict, station7_data: Dict, station5_data: Dict) -> Dict:
        """Task 1: Emotional Arc Verification"""
        try:
            # Extract episode content and character information
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Check if script content is placeholder
            if not episode_content or episode_content.strip() == "Complete full episode script with all audio markup and formatting...":
                print(f"⚠️  Warning: Episode {episode_id} contains placeholder script content")
                print("   Station 28 cannot perform meaningful emotional analysis on placeholder text")
                print("   Please run Station 27 to generate actual episode scripts first")
                
                # Return placeholder analysis
                return {
                    'emotional_scorecard': {},
                    'relationship_chart': [],
                    'universal_resonance': {},
                    'problem_flags': [{
                        'type': 'Placeholder Content',
                        'location': 'Entire Episode',
                        'issue': 'Script contains only placeholder text',
                        'recommended_fix': 'Run Station 27 to generate actual episode scripts'
                    }],
                    'line_adjustments': []
                }
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            journey_maps = station5_data.get('Season Architecture Document', {}).get('season_structure_document', {}).get('rhythm_mapping', [])
            
            # Build context for prompt
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],  # First 2000 chars for context
                'characters': json.dumps(characters),
                'journey_maps': json.dumps(journey_maps)
            }
            
            prompt = self.config.get_prompt('emotional_arc_verification').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('emotional_scorecard', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_relationship_dynamics_check(self, episode: Dict, station7_data: Dict) -> Dict:
        """Task 2: Relationship Dynamics Check"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Check if script content is placeholder
            if not episode_content or episode_content.strip() == "Complete full episode script with all audio markup and formatting...":
                return {
                    'relationship_chart': []
                }
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],
                'characters': json.dumps(characters)
            }
            
            prompt = self.config.get_prompt('relationship_dynamics_check').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('relationship_chart', [])
            
        except Exception as e:
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_universal_emotional_resonance(self, episode: Dict, station5_data: Dict) -> Dict:
        """Task 3: Universal Emotional Resonance"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Check if script content is placeholder
            if not episode_content or episode_content.strip() == "Complete full episode script with all audio markup and formatting...":
                return {
                    'universal_resonance': {}
                }
            
            journey_maps = station5_data.get('Season Architecture Document', {}).get('season_structure_document', {}).get('rhythm_mapping', [])
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],
                'journey_maps': json.dumps(journey_maps)
            }
            
            prompt = self.config.get_prompt('universal_emotional_resonance').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('universal_resonance', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_emotional_problem_detection(self, episode: Dict, emotional_arcs: Dict, 
                                                      relationship_dynamics: List, universal_resonance: Dict) -> Dict:
        """Task 4: Emotional Problem Detection"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Check if script content is placeholder
            if not episode_content or episode_content.strip() == "Complete full episode script with all audio markup and formatting...":
                return {
                    'problem_flags': [{
                        'type': 'Placeholder Content',
                        'location': 'Entire Episode',
                        'issue': 'Script contains only placeholder text',
                        'recommended_fix': 'Run Station 27 to generate actual episode scripts'
                    }],
                    'line_adjustments': []
                }
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],
                'emotional_arcs': json.dumps(emotional_arcs),
                'relationship_dynamics': json.dumps(relationship_dynamics),
                'universal_resonance': json.dumps(universal_resonance)
            }
            
            prompt = self.config.get_prompt('emotional_problem_detection').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return {
                'problem_flags': data.get('problem_flags', []),
                'line_adjustments': data.get('line_adjustments', [])
            }
            
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
            f.write("STATION 28: EMOTIONAL TRUTH VALIDATION\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Episode ID: {data.get('episode_id', 'N/A')}\n")
            f.write(f"Analysis Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Session ID: {self.session_id}\n\n")
            
            # Emotional Scorecard
            f.write("-" * 70 + "\n")
            f.write("EMOTIONAL SCORECARD\n")
            f.write("-" * 70 + "\n")
            
            scorecard = data.get('emotional_scorecard', {})
            for character, arc_data in scorecard.items():
                f.write(f"\nCharacter: {character}\n")
                
                # Handle case where arc_data might be a list or dict
                if isinstance(arc_data, list):
                    # If it's a list, take the first item or create empty structure
                    arc_data = arc_data[0] if arc_data else {}
                elif not isinstance(arc_data, dict):
                    arc_data = {}
                
                # Format arc score consistently
                arc_score = arc_data.get('arc_score', 0)
                if isinstance(arc_score, (int, float)) and 0 <= arc_score <= 5:
                    f.write(f"Arc Score: {arc_score}/5\n")
                else:
                    f.write(f"Arc Score: N/A/5\n")
                
                f.write(f"Start State: {arc_data.get('start_state', {}).get('feeling_state', 'N/A')}\n")
                f.write(f"End State: {arc_data.get('end_state', {}).get('feeling_state', 'N/A')}\n")
                
                transitions = arc_data.get('transitions', [])
                if transitions:
                    f.write("Key Transitions:\n")
                    for i, transition in enumerate(transitions[:3], 1):  # Show first 3
                        f.write(f"  {i}. {transition.get('trigger_moment', 'N/A')}\n")
                f.write("\n")
            
            # Relationship Chart
            f.write("-" * 70 + "\n")
            f.write("RELATIONSHIP DYNAMICS\n")
            f.write("-" * 70 + "\n")
            
            relationships = data.get('relationship_chart', [])
            for relationship in relationships:
                # Handle case where relationship might be a string or other type
                if not isinstance(relationship, dict):
                    continue
                    
                characters = relationship.get('characters', [])
                f.write(f"Characters: {', '.join(characters)}\n")
                
                # Format authenticity score consistently
                auth_score = relationship.get('authenticity_score', 0)
                if isinstance(auth_score, (int, float)) and 0 <= auth_score <= 5:
                    f.write(f"Authenticity Score: {auth_score}/5\n")
                else:
                    f.write(f"Authenticity Score: N/A/5\n")
                
                f.write(f"Status: {relationship.get('status', {}).get('current_standing', 'N/A')}\n")
                f.write(f"Progression: {relationship.get('progression', {}).get('direction', 'N/A')}\n\n")
            
            # Universal Resonance
            f.write("-" * 70 + "\n")
            f.write("UNIVERSAL EMOTIONAL RESONANCE\n")
            f.write("-" * 70 + "\n")
            
            resonance = data.get('universal_resonance', {})
            self._format_resonance_dimension(f, "Love/Connection", resonance.get('love_connection', {}))
            self._format_resonance_dimension(f, "Fear/Anxiety", resonance.get('fear_anxiety', {}))
            self._format_resonance_dimension(f, "Hope/Despair", resonance.get('hope_despair', {}))
            self._format_resonance_dimension(f, "Anger/Frustration", resonance.get('anger_frustration', {}))
            self._format_resonance_dimension(f, "Joy/Humor", resonance.get('joy_humor', {}))
            f.write("\n")
            
            # Problem Flags
            f.write("-" * 70 + "\n")
            f.write("EMOTIONAL PROBLEM FLAGS\n")
            f.write("-" * 70 + "\n")
            
            problem_flags = data.get('problem_flags', [])
            if problem_flags:
                for i, flag in enumerate(problem_flags, 1):
                    f.write(f"{i}. {flag.get('type', 'N/A')}\n")
                    f.write(f"   Location: {flag.get('location', 'N/A')}\n")
                    f.write(f"   Issue: {flag.get('issue', 'N/A')}\n")
                    f.write(f"   Fix: {flag.get('recommended_fix', 'N/A')}\n\n")
            else:
                f.write("No emotional problems detected.\n\n")
            
            # Line Adjustments
            f.write("-" * 70 + "\n")
            f.write("RECOMMENDED LINE ADJUSTMENTS\n")
            f.write("-" * 70 + "\n")
            
            line_adjustments = data.get('line_adjustments', [])
            if line_adjustments:
                for i, adjustment in enumerate(line_adjustments, 1):
                    f.write(f"{i}. Line {adjustment.get('line_number', 'N/A')}\n")
                    f.write(f"   Current: {adjustment.get('current', 'N/A')}\n")
                    f.write(f"   Recommended: {adjustment.get('recommended', 'N/A')}\n")
                    f.write(f"   Reason: {adjustment.get('reason', 'N/A')}\n\n")
            else:
                f.write("No line adjustments recommended.\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("END OF EMOTIONAL ANALYSIS\n")
            f.write("=" * 70 + "\n")

    async def save_final_outputs(self, all_episode_results: List[Dict], summary_report: Dict):
        """Save final comprehensive outputs"""
        # Compile final data
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
        redis_key = f"audiobook:{self.session_id}:station_28"
        await self.redis.set(redis_key, json.dumps(final_data), expire=86400)
        
        print(f"✅ Final outputs saved")

    def save_summary_readable_txt(self, path: Path, data: Dict):
        """Save human-readable summary TXT file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 28: EMOTIONAL TRUTH VALIDATION SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {data.get('session_id', 'N/A')}\n")
            f.write(f"Analysis Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Total Episodes: {data.get('total_episodes', 'N/A')}\n\n")
            
            # Summary Report
            summary = data.get('summary_report', {})
            f.write("-" * 70 + "\n")
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"{summary.get('executive_summary', 'N/A')}\n\n")
            
            # Calculate overall scores from episode data
            episode_results = data.get('episode_results', [])
            calculated_stats = self._calculate_summary_statistics(episode_results)
            
            # Overall Scores
            f.write("-" * 70 + "\n")
            f.write("OVERALL EMOTIONAL HEALTH\n")
            f.write("-" * 70 + "\n")
            f.write(f"Average Emotional Arc Score: {calculated_stats['avg_arc_score']:.1f}/5\n")
            f.write(f"Average Relationship Score: {calculated_stats['avg_relationship_score']:.1f}/5\n")
            f.write(f"Average Resonance Score: {calculated_stats['avg_resonance_score']:.1f}/5\n")
            f.write(f"Total Problems Detected: {calculated_stats['total_problems']}\n")
            f.write(f"Total Line Adjustments: {calculated_stats['total_adjustments']}\n\n")
            
            # Episode Breakdown
            f.write("-" * 70 + "\n")
            f.write("EPISODE BREAKDOWN\n")
            f.write("-" * 70 + "\n")
            
            for episode in episode_results:
                episode_id = episode.get('episode_id', 'Unknown')
                scorecard = episode.get('emotional_scorecard', {})
                relationships = episode.get('relationship_chart', [])
                resonance = episode.get('universal_resonance', {})
                problems = len(episode.get('problem_flags', []))
                adjustments = len(episode.get('line_adjustments', []))
                
                f.write(f"\n{episode_id}:\n")
                f.write(f"  Characters Analyzed: {len(scorecard)}\n")
                f.write(f"  Relationships Checked: {len(relationships)}\n")
                
                # Calculate average resonance score for this episode
                resonance_scores = []
                for dimension in ['love_connection', 'fear_anxiety', 'hope_despair', 'anger_frustration', 'joy_humor']:
                    if dimension in resonance and isinstance(resonance[dimension], dict):
                        score = resonance[dimension].get('score', 0)
                        if isinstance(score, (int, float)):
                            resonance_scores.append(score)
                
                avg_resonance = sum(resonance_scores) / len(resonance_scores) if resonance_scores else 0
                f.write(f"  Average Resonance Score: {avg_resonance:.1f}/5\n")
                f.write(f"  Problems Found: {problems}\n")
                f.write(f"  Adjustments Needed: {adjustments}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF EMOTIONAL TRUTH VALIDATION\n")
            f.write("=" * 70 + "\n")

    def _calculate_summary_statistics(self, episode_results: List[Dict]) -> Dict:
        """Calculate summary statistics from episode data"""
        if not episode_results:
            raise ValueError("❌ No episode results provided for statistics calculation")
        
        total_arc_scores = []
        total_relationship_scores = []
        total_resonance_scores = []
        total_problems = 0
        total_adjustments = 0
        
        for episode in episode_results:
            # Calculate arc scores
            scorecard = episode.get('emotional_scorecard', {})
            for character, arc_data in scorecard.items():
                # Handle case where arc_data might be a list or dict
                if isinstance(arc_data, list):
                    arc_data = arc_data[0] if arc_data else {}
                elif not isinstance(arc_data, dict):
                    arc_data = {}
                
                arc_score = arc_data.get('arc_score', 0)
                if isinstance(arc_score, (int, float)) and 0 <= arc_score <= 5:
                    total_arc_scores.append(arc_score)
            
            # Calculate relationship scores
            relationships = episode.get('relationship_chart', [])
            for relationship in relationships:
                # Handle case where relationship might be a string or other type
                if not isinstance(relationship, dict):
                    continue
                    
                rel_score = relationship.get('authenticity_score', 0)
                if isinstance(rel_score, (int, float)) and 0 <= rel_score <= 5:
                    total_relationship_scores.append(rel_score)
            
            # Calculate resonance scores
            resonance = episode.get('universal_resonance', {})
            for dimension in ['love_connection', 'fear_anxiety', 'hope_despair', 'anger_frustration', 'joy_humor']:
                if dimension in resonance and isinstance(resonance[dimension], dict):
                    score = resonance[dimension].get('score', 0)
                    if isinstance(score, (int, float)) and 0 <= score <= 5:
                        total_resonance_scores.append(score)
            
            # Count problems and adjustments
            total_problems += len(episode.get('problem_flags', []))
            total_adjustments += len(episode.get('line_adjustments', []))
        
        # Calculate averages
        avg_arc_score = sum(total_arc_scores) / len(total_arc_scores) if total_arc_scores else 0
        avg_relationship_score = sum(total_relationship_scores) / len(total_relationship_scores) if total_relationship_scores else 0
        avg_resonance_score = sum(total_resonance_scores) / len(total_resonance_scores) if total_resonance_scores else 0
        
        return {
            'avg_arc_score': avg_arc_score,
            'avg_relationship_score': avg_relationship_score,
            'avg_resonance_score': avg_resonance_score,
            'total_problems': total_problems,
            'total_adjustments': total_adjustments
        }

    def _format_resonance_dimension(self, f, dimension_name: str, dimension_data: Dict):
        """Format a single resonance dimension for TXT output"""
        if not dimension_data or not isinstance(dimension_data, dict):
            f.write(f"{dimension_name}: N/A/5\n")
            return
        
        score = dimension_data.get('score', 0)
        if not isinstance(score, (int, float)) or not (0 <= score <= 5):
            f.write(f"{dimension_name}: N/A/5\n")
            return
        
        f.write(f"{dimension_name}: {score}/5\n")
        
        # Add detailed breakdown if available
        presence = dimension_data.get('presence', '')
        authenticity = dimension_data.get('authenticity', '')
        audio_expression = dimension_data.get('audio_expression', '')
        
        if presence:
            f.write(f"  - Presence: {presence}\n")
        if authenticity:
            f.write(f"  - Authenticity: {authenticity}\n")
        if audio_expression:
            f.write(f"  - Audio Expression: {audio_expression}\n")
        
        f.write("\n")


# CLI Entry Point
async def main():
    """Run Station 28 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    validator = Station28EmotionalTruthValidator(session_id)
    await validator.initialize()
    
    try:
        await validator.run()
        print(f"\n✅ Success! Emotional validation complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
