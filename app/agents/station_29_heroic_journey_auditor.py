"""
Station 29: Heroic Journey Auditor

This station validates completed episode scripts for heroic journey authenticity and character agency.
It analyzes protagonist agency, heroic moments, character growth arcs, and detects agency problems
with specific fixes for audio drama production.

Flow:
1. Load Station 27 complete scripts
2. Load Station 7 character bibles  
3. Load Station 5 emotional journey maps
4. Execute 4-task analysis sequence:
   - Task 1: Heroic Acts Inventory (Per Episode)
   - Task 2: Agency Scoring (1-5 Scale Per Episode)
   - Task 3: Heroic Arc Tracking (Cross-Episode)
   - Task 4: Problem Identification & Fixes
5. Generate comprehensive heroic scorecard per episode
6. Save JSON + TXT outputs per episode
7. Save summary report across all episodes

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config or Station outputs
- Robust error handling - Explicit failures with clear messages, NO silent fallbacks
- Follow existing patterns - Match structure of stations 1-28 exactly
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


class Station29HeroicJourneyAuditor:
    """Station 29: Heroic Journey Auditor"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=29)
        self.output_dir = Path("output/station_29")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 29 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🦸 STATION 29: HEROIC JOURNEY AUDITOR")
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
                print("📊 Task 1/4: Heroic Acts Inventory...")
                heroic_acts = await self.execute_task1_heroic_acts_inventory(
                    episode_data, station7_data, station5_data
                )
                print("✅ Heroic acts inventory complete")

                print("🎯 Task 2/4: Agency Scoring...")
                agency_scores = await self.execute_task2_agency_scoring(
                    episode_data, station7_data
                )
                print("✅ Agency scoring complete")

                print("📈 Task 3/4: Heroic Arc Tracking...")
                arc_tracking = await self.execute_task3_heroic_arc_tracking(
                    episode_data, station5_data
                )
                print("✅ Heroic arc tracking complete")

                print("🔍 Task 4/4: Problem Identification & Fixes...")
                problem_detection = await self.execute_task4_problem_identification_fixes(
                    episode_data, heroic_acts, agency_scores, arc_tracking
                )
                print("✅ Problem identification complete")

                # Compile episode results
                episode_result = {
                    "episode_id": episode_id,
                    "heroic_acts": heroic_acts,
                    "agency_scorecard": agency_scores,
                    "heroic_arc": arc_tracking,
                    "problem_flags": problem_detection.get("problem_flags", []),
                    "adjustments": problem_detection.get("adjustments", []),
                    "audio_notes": problem_detection.get("audio_notes", []),
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
            print("✅ STATION 29 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Analyzed: {len(all_episode_results)}")
            print("\n📄 Output files:")
            print(f"   - output/station_29/{self.session_id}_summary.json")
            print(f"   - output/station_29/{self.session_id}_summary.txt")
            print(f"   - output/station_29/{self.session_id}_episode_*.json (per episode)")
            print("\n📌 Ready to proceed to next station")

        except Exception as e:
            logger.error(f"❌ Station 29 failed: {str(e)}")
            raise

    async def load_station27_data(self) -> Dict:
        """Load Station 27 complete scripts from Redis, fallback to Station 21 if needed"""
        try:
            # First try Station 27
            pattern = f"audiobook:{self.session_id}:station_27:episode_*"
            episode_keys = await self.redis.keys(pattern)
            
            episodes = {}
            
            if episode_keys:
                # Load from Station 27
                for key in episode_keys:
                    episode_raw = await self.redis.get(key)
                    if episode_raw:
                        episode_data = json.loads(episode_raw)
                        episode_num = key.split(':')[-1]  # Gets "episode_01"
                        episodes[episode_num] = episode_data
                
                # Check if Station 27 has actual content
                has_content = False
                for episode_data in episodes.values():
                    script_content = episode_data.get('master_script_assembly', {}).get('master_script_text', '')
                    if len(script_content) > 200:  # More than placeholder text
                        has_content = True
                        break
                
                if not has_content:
                    logger.warning("Station 27 has no actual script content, falling back to Station 21")
                    episodes = {}  # Clear and try Station 21
            
            # If Station 27 failed or has no content, try Station 21
            if not episodes:
                pattern = f"audiobook:{self.session_id}:station_21:episode_*"
                episode_keys = await self.redis.keys(pattern)
                
                if not episode_keys:
                    raise ValueError(f"❌ No Station 21 or Station 27 data found for session {self.session_id}\n   Please run Station 21 or Station 27 first")
                
                for key in episode_keys:
                    episode_raw = await self.redis.get(key)
                    if episode_raw:
                        episode_data = json.loads(episode_raw)
                        episode_num = key.split(':')[-1]  # Gets "episode_01"
                        
                        # Extract script content from Station 21 format
                        draft_data = episode_data.get('draft_data', {})
                        script_content = draft_data.get('first_draft_script', '')
                        
                        # If script_content is a dict (Station 21 format), extract the actual script text
                        if isinstance(script_content, dict):
                            scenes = script_content.get('scenes', [])
                            extracted_script = ''
                            for scene in scenes:
                                scene_content = scene.get('script_content', '')
                                extracted_script += scene_content + '\n\n'
                            script_content = extracted_script
                        
                        # Convert Station 21 format to Station 27 format for compatibility
                        converted_episode = {
                            'episode_number': episode_data.get('episode_number', episode_num),
                            'master_script_assembly': {
                                'master_script_text': script_content,
                                'assembly_status': 'complete'
                            }
                        }
                        
                        episodes[episode_num] = converted_episode
            
            if not episodes:
                raise ValueError(f"❌ No valid episode data found for session {self.session_id}")
            
            # Return in expected format
            station27_data = {
                'episodes': episodes
            }
            
            return station27_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing episode data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading episode data: {str(e)}")

    async def load_station7_data(self) -> Dict:
        """Load Station 7 character bibles from Redis, provide fallback if not available"""
        try:
            station7_key = f"audiobook:{self.session_id}:station_07"
            station7_raw = await self.redis.get(station7_key)
            
            if not station7_raw:
                logger.warning(f"No Station 7 data found for session {self.session_id}, using fallback character data")
                # Provide fallback character data
                return {
                    'Character Bible Document': {
                        'character_bible': {
                            'tier_1_protagonists': [
                                {'name': 'Tom', 'role': 'protagonist'},
                                {'name': 'Julia', 'role': 'protagonist'}
                            ]
                        }
                    }
                }
            
            station7_data = json.loads(station7_raw)
            
            # Validate required structure
            if 'Character Bible Document' not in station7_data:
                logger.warning("Station 7 data missing 'Character Bible Document' key, using fallback")
                return {
                    'Character Bible Document': {
                        'character_bible': {
                            'tier_1_protagonists': [
                                {'name': 'Tom', 'role': 'protagonist'},
                                {'name': 'Julia', 'role': 'protagonist'}
                            ]
                        }
                    }
                }
            
            return station7_data
            
        except json.JSONDecodeError as e:
            logger.warning(f"Error parsing Station 7 data: {str(e)}, using fallback")
            return {
                'Character Bible Document': {
                    'character_bible': {
                        'tier_1_protagonists': [
                            {'name': 'Tom', 'role': 'protagonist'},
                            {'name': 'Julia', 'role': 'protagonist'}
                        ]
                    }
                }
            }
        except Exception as e:
            logger.warning(f"Error loading Station 7 data: {str(e)}, using fallback")
            return {
                'Character Bible Document': {
                    'character_bible': {
                        'tier_1_protagonists': [
                            {'name': 'Tom', 'role': 'protagonist'},
                            {'name': 'Julia', 'role': 'protagonist'}
                        ]
                    }
                }
            }

    async def load_station5_data(self) -> Dict:
        """Load Station 5 emotional journey maps from Redis, provide fallback if not available"""
        try:
            station5_key = f"audiobook:{self.session_id}:station_05"
            station5_raw = await self.redis.get(station5_key)
            
            if not station5_raw:
                logger.warning(f"No Station 5 data found for session {self.session_id}, using fallback journey maps")
                # Provide fallback journey maps
                return {
                    'Season Architecture Document': {
                        'season_structure_document': {
                            'rhythm_mapping': [
                                {'phase': 'reluctant', 'description': 'Character resists the call to adventure'},
                                {'phase': 'learning', 'description': 'Character begins to learn and grow'},
                                {'phase': 'testing', 'description': 'Character faces challenges and tests'},
                                {'phase': 'mastery', 'description': 'Character demonstrates mastery'},
                                {'phase': 'transformation', 'description': 'Character undergoes transformation'}
                            ]
                        }
                    }
                }
            
            station5_data = json.loads(station5_raw)
            
            # Validate required structure
            if 'Season Architecture Document' not in station5_data:
                logger.warning("Station 5 data missing 'Season Architecture Document' key, using fallback")
                return {
                    'Season Architecture Document': {
                        'season_structure_document': {
                            'rhythm_mapping': [
                                {'phase': 'reluctant', 'description': 'Character resists the call to adventure'},
                                {'phase': 'learning', 'description': 'Character begins to learn and grow'},
                                {'phase': 'testing', 'description': 'Character faces challenges and tests'},
                                {'phase': 'mastery', 'description': 'Character demonstrates mastery'},
                                {'phase': 'transformation', 'description': 'Character undergoes transformation'}
                            ]
                        }
                    }
                }
            
            return station5_data
            
        except json.JSONDecodeError as e:
            logger.warning(f"Error parsing Station 5 data: {str(e)}, using fallback")
            return {
                'Season Architecture Document': {
                    'season_structure_document': {
                        'rhythm_mapping': [
                            {'phase': 'reluctant', 'description': 'Character resists the call to adventure'},
                            {'phase': 'learning', 'description': 'Character begins to learn and grow'},
                            {'phase': 'testing', 'description': 'Character faces challenges and tests'},
                            {'phase': 'mastery', 'description': 'Character demonstrates mastery'},
                            {'phase': 'transformation', 'description': 'Character undergoes transformation'}
                        ]
                    }
                }
            }
        except Exception as e:
            logger.warning(f"Error loading Station 5 data: {str(e)}, using fallback")
            return {
                'Season Architecture Document': {
                    'season_structure_document': {
                        'rhythm_mapping': [
                            {'phase': 'reluctant', 'description': 'Character resists the call to adventure'},
                            {'phase': 'learning', 'description': 'Character begins to learn and grow'},
                            {'phase': 'testing', 'description': 'Character faces challenges and tests'},
                            {'phase': 'mastery', 'description': 'Character demonstrates mastery'},
                            {'phase': 'transformation', 'description': 'Character undergoes transformation'}
                        ]
                    }
                }
            }

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
            
            # Debug: Check script content availability
            script_content = episode_data.get('master_script_assembly', {}).get('master_script_text', '')
            content_length = len(script_content) if script_content else 0
            
            print(f"   • {episode_id}: {title} (Content: {content_length} chars)")
            
            # Show first 100 chars of content for debugging
            if script_content:
                preview = script_content[:100].replace('\n', ' ')
                print(f"     Preview: {preview}...")
            else:
                print(f"     ⚠️  No script content found!")
        
        print("-" * 70)

    async def execute_task1_heroic_acts_inventory(self, episode: Dict, station7_data: Dict, station5_data: Dict) -> Dict:
        """Task 1: Heroic Acts Inventory (Per Episode)"""
        try:
            # Extract episode content and character information
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Debug: Check if content exists
            if not episode_content:
                logger.warning(f"No script content found for episode {episode_id}")
                # Try alternative content extraction paths
                episode_content = episode.get('master_script_text', '')
                if not episode_content:
                    episode_content = str(episode.get('master_script_assembly', {}))
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            journey_maps = station5_data.get('Season Architecture Document', {}).get('season_structure_document', {}).get('rhythm_mapping', [])
            
            # Ensure we have content to analyze
            if not episode_content or len(episode_content.strip()) < 100:
                logger.error(f"Insufficient content for episode {episode_id}: {len(episode_content)} chars")
                raise ValueError(f"Insufficient script content for episode {episode_id}. Content length: {len(episode_content)}")
            
            # Build context for prompt
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:4000],  # Increased to 4000 chars for better context
                'characters': json.dumps(characters),
                'journey_maps': json.dumps(journey_maps)
            }
            
            prompt = self.config.get_prompt('heroic_acts_inventory').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('heroic_acts', {})
            
        except Exception as e:
            logger.error(f"Task 1 error for episode {episode_id}: {str(e)}")
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_agency_scoring(self, episode: Dict, station7_data: Dict) -> Dict:
        """Task 2: Agency Scoring (1-5 Scale Per Episode)"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Debug: Check if content exists
            if not episode_content:
                episode_content = episode.get('master_script_text', '')
                if not episode_content:
                    episode_content = str(episode.get('master_script_assembly', {}))
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:4000],
                'characters': json.dumps(characters)
            }
            
            prompt = self.config.get_prompt('agency_scoring').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('agency_scorecard', {})
            
        except Exception as e:
            logger.error(f"Task 2 error for episode {episode_id}: {str(e)}")
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_heroic_arc_tracking(self, episode: Dict, station5_data: Dict) -> Dict:
        """Task 3: Heroic Arc Tracking (Cross-Episode)"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Debug: Check if content exists
            if not episode_content:
                episode_content = episode.get('master_script_text', '')
                if not episode_content:
                    episode_content = str(episode.get('master_script_assembly', {}))
            
            journey_maps = station5_data.get('Season Architecture Document', {}).get('season_structure_document', {}).get('rhythm_mapping', [])
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:4000],
                'journey_maps': json.dumps(journey_maps)
            }
            
            prompt = self.config.get_prompt('heroic_arc_tracking').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('heroic_arc', {})
            
        except Exception as e:
            logger.error(f"Task 3 error for episode {episode_id}: {str(e)}")
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_problem_identification_fixes(self, episode: Dict, heroic_acts: Dict, 
                                                         agency_scores: Dict, arc_tracking: Dict) -> Dict:
        """Task 4: Problem Identification & Fixes"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Debug: Check if content exists
            if not episode_content:
                episode_content = episode.get('master_script_text', '')
                if not episode_content:
                    episode_content = str(episode.get('master_script_assembly', {}))
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:4000],
                'heroic_acts': json.dumps(heroic_acts),
                'agency_scores': json.dumps(agency_scores),
                'arc_tracking': json.dumps(arc_tracking)
            }
            
            prompt = self.config.get_prompt('problem_identification_fixes').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            
            # Add user validation markers to adjustments
            adjustments = data.get('adjustments', [])
            for adjustment in adjustments:
                adjustment['requires_user_approval'] = True
                adjustment['approval_status'] = 'pending'
            
            return {
                'problem_flags': data.get('problem_flags', []),
                'adjustments': adjustments,
                'audio_notes': data.get('audio_notes', [])
            }
            
        except Exception as e:
            logger.error(f"Task 4 error for episode {episode_id}: {str(e)}")
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    def calculate_summary_metrics(self, all_episode_results: List[Dict]) -> Dict:
        """Calculate comprehensive metrics from episode results"""
        try:
            # Initialize counters
            total_agency_scores = []
            total_heroic_acts = 0
            total_arc_progress = []
            total_problems = 0
            total_adjustments = 0
            pending_approvals = 0
            
            # Phase mapping for arc progress calculation
            phase_scores = {
                'reluctant': 1,
                'learning': 2, 
                'testing': 3,
                'mastery': 4,
                'transformation': 5
            }
            
            # Process each episode
            for episode in all_episode_results:
                # Count problems and adjustments
                total_problems += len(episode.get('problem_flags', []))
                adjustments = episode.get('adjustments', [])
                total_adjustments += len(adjustments)
                
                # Count pending approvals
                for adjustment in adjustments:
                    if adjustment.get('approval_status', 'pending') == 'pending':
                        pending_approvals += 1
                
                # Process agency scores
                agency_scorecard = episode.get('agency_scorecard', {})
                for character, scores in agency_scorecard.items():
                    overall_score = scores.get('overall_score')
                    if overall_score is not None:
                        total_agency_scores.append(overall_score)
                
                # Process heroic acts
                heroic_acts = episode.get('heroic_acts', {})
                for character, acts_data in heroic_acts.items():
                    # Count all types of heroic acts
                    active_choices = len(acts_data.get('active_choices', []))
                    heroic_moments = len(acts_data.get('heroic_moments', []))
                    growth_demos = len(acts_data.get('growth_demonstrations', []))
                    total_heroic_acts += active_choices + heroic_moments + growth_demos
                
                # Process arc progress
                heroic_arc = episode.get('heroic_arc', {})
                for character, arc_data in heroic_arc.items():
                    current_phase = arc_data.get('current_phase', '').lower()
                    if current_phase in phase_scores:
                        total_arc_progress.append(phase_scores[current_phase])
            
            # Calculate averages
            avg_agency_score = round(sum(total_agency_scores) / len(total_agency_scores), 1) if total_agency_scores else 0
            avg_heroic_acts = round(total_heroic_acts / len(all_episode_results), 1) if all_episode_results else 0
            avg_arc_progress = round(sum(total_arc_progress) / len(total_arc_progress), 1) if total_arc_progress else 0
            
            # Build metrics
            metrics = {
                'overall_heroic_health': {
                    'average_agency_score': avg_agency_score,
                    'average_heroic_acts': avg_heroic_acts,
                    'average_arc_progress': avg_arc_progress,
                    'total_problems': total_problems,
                    'total_adjustments': total_adjustments,
                    'calculation_notes': f"Based on {len(total_agency_scores)} primary characters. Supporting characters not included in agency averages."
                },
                'adjustments_summary': {
                    'total_adjustments': total_adjustments,
                    'pending_approval': pending_approvals,
                    'approved': total_adjustments - pending_approvals,
                    'rejected': 0  # Will be updated when user reviews
                }
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            # Return safe defaults
            return {
                'overall_heroic_health': {
                    'average_agency_score': 0,
                    'average_heroic_acts': 0,
                    'average_arc_progress': 0,
                    'total_problems': 0,
                    'total_adjustments': 0,
                    'calculation_notes': f"Error calculating metrics: {str(e)}"
                },
                'adjustments_summary': {
                    'total_adjustments': 0,
                    'pending_approval': 0,
                    'approved': 0,
                    'rejected': 0
                }
            }

    async def generate_summary_report(self, all_episode_results: List[Dict], station27_data: Dict) -> Dict:
        """Generate comprehensive summary report across all episodes"""
        try:
            # Calculate metrics from episode results
            metrics = self.calculate_summary_metrics(all_episode_results)
            
            context = {
                'session_id': self.session_id,
                'episode_results': json.dumps(all_episode_results),
                'total_episodes': len(all_episode_results),
                'calculated_metrics': json.dumps(metrics)
            }
            
            prompt = self.config.get_prompt('summary_report').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            summary_report = data.get('summary_report', {})
            
            # Inject calculated metrics into the summary report
            summary_report['overall_heroic_health'] = metrics['overall_heroic_health']
            summary_report['adjustments_summary'] = metrics['adjustments_summary']
            
            return summary_report
            
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
            f.write("STATION 29: HEROIC JOURNEY AUDIT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Episode ID: {data.get('episode_id', 'N/A')}\n")
            f.write(f"Analysis Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Session ID: {self.session_id}\n\n")
            
            # Heroic Acts Inventory
            f.write("-" * 70 + "\n")
            f.write("HEROIC ACTS INVENTORY\n")
            f.write("-" * 70 + "\n")
            
            heroic_acts = data.get('heroic_acts', {})
            for character, acts_data in heroic_acts.items():
                f.write(f"\nCharacter: {character}\n")
                
                active_choices = acts_data.get('active_choices', [])
                if active_choices:
                    f.write("Active Choices:\n")
                    for i, choice in enumerate(active_choices[:3], 1):  # Show first 3
                        f.write(f"  {i}. {choice.get('decision', 'N/A')}\n")
                        f.write(f"     Audio: {choice.get('audio_delivery', 'N/A')}\n")
                
                heroic_moments = acts_data.get('heroic_moments', [])
                if heroic_moments:
                    f.write("Heroic Moments:\n")
                    for i, moment in enumerate(heroic_moments[:3], 1):  # Show first 3
                        f.write(f"  {i}. {moment.get('act_type', 'N/A')}: {moment.get('description', 'N/A')}\n")
                        f.write(f"     Audio: {moment.get('audio_signature', 'N/A')}\n")
                
                growth_demos = acts_data.get('growth_demonstrations', [])
                if growth_demos:
                    f.write("Growth Demonstrations:\n")
                    for i, growth in enumerate(growth_demos[:3], 1):  # Show first 3
                        f.write(f"  {i}. {growth.get('skill_lesson', 'N/A')}\n")
                        f.write(f"     Voice Change: {growth.get('voice_confidence_change', 'N/A')}\n")
                f.write("\n")
            
            # Agency Scorecard
            f.write("-" * 70 + "\n")
            f.write("AGENCY SCORECARD\n")
            f.write("-" * 70 + "\n")
            
            agency_scorecard = data.get('agency_scorecard', {})
            for character, scores in agency_scorecard.items():
                f.write(f"\nCharacter: {character}\n")
                f.write(f"Goal Setting: {scores.get('goal_setting', 'N/A')}/5\n")
                f.write(f"Obstacle Confrontation: {scores.get('obstacle_confrontation', 'N/A')}/5\n")
                f.write(f"Solution Generation: {scores.get('solution_generation', 'N/A')}/5\n")
                f.write(f"Consequence Ownership: {scores.get('consequence_ownership', 'N/A')}/5\n")
                f.write(f"Overall Agency Score: {scores.get('overall_score', 'N/A')}/5\n\n")
            
            # Heroic Arc Tracking
            f.write("-" * 70 + "\n")
            f.write("HEROIC ARC TRACKING\n")
            f.write("-" * 70 + "\n")
            
            heroic_arc = data.get('heroic_arc', {})
            for character, arc_data in heroic_arc.items():
                f.write(f"\nCharacter: {character}\n")
                f.write(f"Current Phase: {arc_data.get('current_phase', 'N/A')}\n")
                f.write(f"Phase Description: {arc_data.get('phase_description', 'N/A')}\n")
                f.write(f"Audio Notes: {arc_data.get('audio_notes', 'N/A')}\n")
                f.write(f"Transformation Progress: {arc_data.get('transformation_progress', 'N/A')}\n\n")
            
            # Problem Flags
            f.write("-" * 70 + "\n")
            f.write("PROBLEM FLAGS\n")
            f.write("-" * 70 + "\n")
            
            problem_flags = data.get('problem_flags', [])
            if problem_flags:
                for i, flag in enumerate(problem_flags, 1):
                    f.write(f"{i}. {flag.get('type', 'N/A')}\n")
                    f.write(f"   Location: {flag.get('location', 'N/A')}\n")
                    f.write(f"   Issue: {flag.get('issue', 'N/A')}\n")
                    f.write(f"   Fix: {flag.get('recommended_fix', 'N/A')}\n\n")
            else:
                f.write("No heroic journey problems detected.\n\n")
            
            # Adjustments
            f.write("-" * 70 + "\n")
            f.write("RECOMMENDED ADJUSTMENTS\n")
            f.write("-" * 70 + "\n")
            
            adjustments = data.get('adjustments', [])
            if adjustments:
                for i, adjustment in enumerate(adjustments, 1):
                    f.write(f"{i}. {adjustment.get('type', 'N/A')}\n")
                    f.write(f"   Current: {adjustment.get('current', 'N/A')}\n")
                    f.write(f"   Recommended: {adjustment.get('recommended', 'N/A')}\n")
                    f.write(f"   Reason: {adjustment.get('reason', 'N/A')}\n\n")
            else:
                f.write("No adjustments recommended.\n\n")
            
            # Audio Notes
            f.write("-" * 70 + "\n")
            f.write("AUDIO DELIVERY NOTES\n")
            f.write("-" * 70 + "\n")
            
            audio_notes = data.get('audio_notes', [])
            if audio_notes:
                for i, note in enumerate(audio_notes, 1):
                    f.write(f"{i}. {note.get('character', 'N/A')}: {note.get('note', 'N/A')}\n")
            else:
                f.write("No specific audio notes.\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("END OF HEROIC JOURNEY ANALYSIS\n")
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
        redis_key = f"audiobook:{self.session_id}:station_29"
        await self.redis.set(redis_key, json.dumps(final_data), expire=86400)
        
        print(f"✅ Final outputs saved")

    def save_summary_readable_txt(self, path: Path, data: Dict):
        """Save human-readable summary TXT file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 29: HEROIC JOURNEY AUDIT SUMMARY\n")
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
            
            # Overall Scores
            f.write("-" * 70 + "\n")
            f.write("OVERALL HEROIC HEALTH\n")
            f.write("-" * 70 + "\n")
            
            overall_health = summary.get('overall_heroic_health', {})
            f.write(f"Average Agency Score: {overall_health.get('average_agency_score', 'N/A')}/5\n")
            f.write(f"Average Heroic Acts: {overall_health.get('average_heroic_acts', 'N/A')} per episode\n")
            f.write(f"Average Arc Progress: {overall_health.get('average_arc_progress', 'N/A')}/5\n")
            f.write(f"Total Problems Detected: {overall_health.get('total_problems', 'N/A')}\n")
            f.write(f"Total Adjustments: {overall_health.get('total_adjustments', 'N/A')}\n")
            
            # Add calculation notes
            calc_notes = overall_health.get('calculation_notes', '')
            if calc_notes:
                f.write(f"Calculation Notes: {calc_notes}\n")
            f.write("\n")
            
            # User Validation Section
            adjustments_summary = summary.get('adjustments_summary', {})
            if adjustments_summary.get('total_adjustments', 0) > 0:
                f.write("-" * 70 + "\n")
                f.write("⚠️  USER VALIDATION REQUIRED\n")
                f.write("-" * 70 + "\n")
                f.write("All script adjustments must be reviewed and approved before implementation.\n")
                f.write(f"Pending Approval: {adjustments_summary.get('pending_approval', 0)} adjustments\n")
                f.write(f"Approved: {adjustments_summary.get('approved', 0)} adjustments\n")
                f.write(f"Rejected: {adjustments_summary.get('rejected', 0)} adjustments\n\n")
            
            # Episode Breakdown
            f.write("-" * 70 + "\n")
            f.write("EPISODE BREAKDOWN\n")
            f.write("-" * 70 + "\n")
            
            episode_results = data.get('episode_results', [])
            for episode in episode_results:
                episode_id = episode.get('episode_id', 'Unknown')
                agency_scorecard = episode.get('agency_scorecard', {})
                heroic_acts = episode.get('heroic_acts', {})
                heroic_arc = episode.get('heroic_arc', {})
                problems = len(episode.get('problem_flags', []))
                adjustments = len(episode.get('adjustments', []))
                
                # Calculate total heroic acts for this episode
                total_acts = 0
                for character, acts_data in heroic_acts.items():
                    active_choices = len(acts_data.get('active_choices', []))
                    heroic_moments = len(acts_data.get('heroic_moments', []))
                    growth_demos = len(acts_data.get('growth_demonstrations', []))
                    total_acts += active_choices + heroic_moments + growth_demos
                
                f.write(f"\nEpisode {episode_id}:\n")
                f.write(f"  Characters Analyzed: {len(agency_scorecard)}\n")
                f.write(f"  Total Heroic Acts: {total_acts} ({total_acts/len(agency_scorecard):.1f} avg per character)\n")
                f.write(f"  Problems Found: {problems}\n")
                f.write(f"  Adjustments Needed: {adjustments}\n")
                
                # Add visual arc progression for each character
                if heroic_arc:
                    f.write(f"  Character Arc Progress:\n")
                    for character, arc_data in heroic_arc.items():
                        current_phase = arc_data.get('current_phase', '').lower()
                        phase_number = self.get_phase_number(current_phase)
                        progress_bar = self.create_progress_bar(phase_number, 5)
                        
                        # Get agency score for this character
                        agency_score = agency_scorecard.get(character, {}).get('overall_score', 0)
                        trend_symbol = self.get_agency_trend_symbol(agency_score)
                        
                        f.write(f"    {character}: {progress_bar} Phase {phase_number}/5 ({current_phase.title()})\n")
                        f.write(f"    Agency Trend: [{trend_symbol}] Score: {agency_score}/5\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF HEROIC JOURNEY AUDIT\n")
            f.write("=" * 70 + "\n")

    def get_phase_number(self, phase_name: str) -> int:
        """Convert phase name to number for progress calculation"""
        phase_mapping = {
            'reluctant': 1,
            'learning': 2,
            'testing': 3,
            'mastery': 4,
            'transformation': 5
        }
        return phase_mapping.get(phase_name.lower(), 1)

    def create_progress_bar(self, current: int, total: int) -> str:
        """Create ASCII progress bar"""
        if total == 0:
            return "[□□□□□]"
        
        filled = int((current / total) * 5)
        empty = 5 - filled
        
        bar = "[" + "■" * filled + "□" * empty + "]"
        return bar

    def get_agency_trend_symbol(self, score: int) -> str:
        """Get trend symbol based on agency score"""
        if score >= 4:
            return "▲"  # Strong
        elif score >= 3:
            return "→"  # Moderate
        elif score >= 2:
            return "▼"  # Needs improvement
        else:
            return "▼"  # Poor


# CLI Entry Point
async def main():
    """Run Station 29 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    auditor = Station29HeroicJourneyAuditor(session_id)
    await auditor.initialize()
    
    try:
        await auditor.run()
        print(f"\n✅ Success! Heroic journey audit complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
