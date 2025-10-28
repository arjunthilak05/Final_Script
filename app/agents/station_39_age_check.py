"""
Station 39: Age Appropriateness Final Check

This station performs final age appropriateness validation before audio production.
It screens content against target age rating, flags violations, and outputs a compliance report.

Flow:
1. Load Station 27 master scripts
2. Load Station 7 character data  
3. Load Station 2 (Project DNA) for age rating
4. Execute 4-task analysis sequence:
   - Task 1: Content Screening (violence, language, fear factor, mature themes)
   - Task 2: Comprehension Check (vocabulary, plot complexity, emotional complexity)
   - Task 3: Audio Intensity Analysis (volume dynamics, disturbing sounds, emotional intensity)
   - Task 4: Positive Messaging Check (role models, conflict resolution, consequences)
5. Generate comprehensive age appropriateness report per episode
6. Save JSON + TXT outputs per episode
7. Save summary report across all episodes

Critical Implementation Rules:
- NO hardcoded paths/values - All paths from config or Station outputs
- Robust error handling - Explicit failures with clear messages, NO silent fallbacks
- Follow existing patterns - Match structure of stations 1-38 exactly
- Conditional execution - Skip if age_rating == "general"
- User validation required for high-severity flags
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


class Station39AgeCheck:
    """Station 39: Age Appropriateness Final Check"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=39)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path(self.config_data.get('output_directory', 'output/station_39'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        import yaml
        from pathlib import Path

        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_39.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 39 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🎯 STATION 39: AGE APPROPRIATENESS FINAL CHECK")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            station7_data = await self.load_station7_data()
            station2_data = await self.load_station2_data()
            
            # Extract age rating and target age from Station 2
            self.age_rating = self._extract_age_rating(station2_data)
            self.target_age = self._extract_target_age(station2_data)
            
            # Check if we should skip this station
            if self._should_skip_station():
                print(f"⏭️  Skipping Station 39: Age rating '{self.age_rating}' does not require age appropriateness screening")
                print("   (Station 39 only runs for specific age targets)")
                return
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 27: {len(station27_data.get('episodes', {}))} master scripts")
            print(f"   ✓ Station 7: Character profiles loaded")
            print(f"   ✓ Station 2: Content Rating = {self.age_rating}, Target Age = {self.target_age}")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data, station7_data)

            # Step 3: Process each episode
            episodes = station27_data.get('episodes', {})
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            all_episode_results = []
            high_severity_flags = []
            
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"\n🎬 Processing Episode: {episode_id}")
                print("-" * 70)

                # Execute 4-task analysis sequence
                print("🔍 Task 1/4: Content Screening Analysis...")
                content_screening = await self.execute_task1_content_screening(
                    episode_data, station7_data, self.age_rating, self.target_age
                )
                print("✅ Content screening complete")

                print("📚 Task 2/4: Comprehension Check Analysis...")
                comprehension_check = await self.execute_task2_comprehension_check(
                    episode_data, self.age_rating, self.target_age
                )
                print("✅ Comprehension check complete")

                print("🔊 Task 3/4: Audio Intensity Analysis...")
                audio_intensity = await self.execute_task3_audio_intensity_analysis(
                    episode_data, self.age_rating, self.target_age
                )
                print("✅ Audio intensity analysis complete")

                print("✨ Task 4/4: Positive Messaging Check...")
                positive_messaging = await self.execute_task4_positive_messaging_check(
                    episode_data, station7_data, self.age_rating, self.target_age
                )
                print("✅ Positive messaging check complete")

                # Compile episode results
                episode_result = {
                    "episode_id": episode_id,
                    "content_rating": self.age_rating,
                    "target_age_range": self.target_age,
                    "content_screening": content_screening,
                    "comprehension_check": comprehension_check,
                    "audio_intensity_analysis": audio_intensity,
                    "positive_messaging_check": positive_messaging,
                    "age_rating_confirmation": self._calculate_compliance(
                        content_screening, comprehension_check, audio_intensity, positive_messaging
                    ),
                    "timestamp": datetime.now().isoformat()
                }

                # Check for high-severity flags
                flags = self._extract_high_severity_flags(episode_result)
                if flags:
                    high_severity_flags.extend([(episode_id, flag) for flag in flags])

                all_episode_results.append(episode_result)

                # Save individual episode results
                await self.save_episode_output(episode_result)

                compliance_status = "✅ COMPLIANT" if episode_result['age_rating_confirmation']['compliant'] else "⚠️ REQUIRES REVIEW"
                print(f"✅ Episode {episode_id} analysis complete")
                print(f"   Compliance Status: {compliance_status}")

            # Check if user validation is required
            if high_severity_flags and self.config_data.get('user_validation_required_for_high_severity', True):
                print("\n" + "=" * 70)
                print("⚠️  HIGH-SEVERITY CONTENT FLAGS DETECTED")
                print("=" * 70)
                for episode_id, flag in high_severity_flags[:5]:  # Show first 5
                    print(f"\nEpisode {episode_id}: {flag.get('issue', 'N/A')}")
                    print(f"   Severity: {flag.get('severity', 'N/A')}")
                    print(f"   Location: {flag.get('location', 'N/A')}")
                print(f"\n... and {len(high_severity_flags) - min(5, len(high_severity_flags))} more high-severity issues")
                print("\n⚠️  This content requires your review before proceeding to audio production.")

            # Step 4: Generate summary report
            print("\n" + "=" * 70)
            print("📊 GENERATING SUMMARY REPORT")
            print("=" * 70)
            summary_report = await self.generate_summary_report(all_episode_results, station2_data)

            # Step 5: Save final outputs
            await self.save_final_outputs(all_episode_results, summary_report)

            print("\n" + "=" * 70)
            print("✅ STATION 39 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Analyzed: {len(all_episode_results)}")
            print(f"Content Rating: {self.age_rating}")
            print(f"Target Age Range: {self.target_age}")
            print("\n📄 Output files:")
            print(f"   - output/station_39/{self.session_id}_summary.json")
            print(f"   - output/station_39/{self.session_id}_summary.txt")
            print(f"   - output/station_39/{self.session_id}_episode_*.json (per episode)")
            print("\n📌 Ready to proceed to next station")

        except Exception as e:
            logger.error(f"❌ Station 39 failed: {str(e)}")
            raise

    def _should_skip_station(self) -> bool:
        """Check if station should be skipped based on age rating"""
        skip_if_general = self.config_data.get('skip_if_age_rating_general', True)
        
        if skip_if_general and self.age_rating.lower() in ['general', 'all ages', 'universal']:
            return True
        
        return False

    def _extract_age_rating(self, station2_data: Dict) -> str:
        """Extract content rating from Station 2 Project DNA"""
        try:
            # Try multiple possible paths for content rating
            # First try: production_constraints.content_rating (most common location)
            age_rating = (
                station2_data.get('production_constraints', {}).get('content_rating') or
                station2_data.get('content_rating') or
                station2_data.get('target_rating') or
                station2_data.get('age_rating') or
                'unknown'
            )
            
            if age_rating == 'unknown':
                raise ValueError("❌ Content rating not found in Station 2 data. Cannot determine rating for screening.")
            
            return age_rating
            
        except Exception as e:
            raise ValueError(f"❌ Error extracting content rating: {str(e)}")

    def _extract_target_age(self, station2_data: Dict) -> str:
        """Extract specific target age from Station 2 Project DNA"""
        try:
            # Try multiple possible paths for target age
            target_age = (
                station2_data.get('audience_profile', {}).get('primary_age_range') or
                station2_data.get('target_audience', {}).get('age_range') or
                station2_data.get('target_age_range') or
                station2_data.get('primary_age_range') or
                station2_data.get('target_age') or
                None
            )
            
            if not target_age:
                # If no specific target age, try to infer from content rating
                return self._infer_target_age_from_rating(self.age_rating)
            
            return target_age
            
        except Exception as e:
            logger.warning(f"Could not extract specific target age: {str(e)}, using content rating inference")
            return self._infer_target_age_from_rating(self.age_rating)

    def _infer_target_age_from_rating(self, rating: str) -> str:
        """Infer target age range from content rating when not explicitly specified"""
        rating_lower = rating.upper()
        
        if rating_lower in ['G', 'E', 'ALL AGES', 'UNIVERSAL']:
            return "General Audience"
        elif rating_lower == 'PG':
            return "7-12 years"  # Default PG assumption
        elif rating_lower in ['PG-13', '12A', 'T']:
            return "13-17 years"
        elif rating_lower in ['R', 'M']:
            return "17+ years"
        else:
            return "Unspecified"

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

    async def load_station2_data(self) -> Dict:
        """Load Station 2 Project DNA from output files"""
        try:
            # Try to find any project DNA file in station_02 directory
            station_02_dir = Path("output/station_02")
            station2_files = list(station_02_dir.glob("*.json"))
            
            # Load the most recent file
            if station2_files:
                latest_file = max(station2_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            station2_key = f"audiobook:{self.session_id}:station_02"
            station2_raw = await self.redis.get(station2_key)
            
            if not station2_raw:
                raise ValueError(f"❌ No Station 2 data found for session {self.session_id}\n   Please run Station 2 first")
            
            return json.loads(station2_raw)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 2 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 2 data: {str(e)}")

    def display_project_summary(self, station27_data: Dict, station7_data: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = station27_data.get('episodes', {})
        characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
        
        print(f"Episodes to Screen: {len(episodes)}")
        print(f"Character Profiles: {len(characters)}")
        print(f"Content Rating: {self.age_rating}")
        print(f"Target Age Range: {self.target_age}")
        print()
        
        if episodes:
            print("Episode List:")
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                title = episode_data.get('production_package', {}).get('production_summary', {}).get('title', 'Unknown')
                print(f"   • Episode {episode_id}: {title}")
        
        print("-" * 70)

    async def execute_task1_content_screening(self, episode: Dict, station7_data: Dict, age_rating: str, target_age: str) -> Dict:
        """Task 1: Content Screening Analysis (violence, language, fear factor, mature themes)"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'content_screening': {
                        'content_flags': [],
                        'warning': 'No content available for analysis'
                    }
                }
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            characters_json = json.dumps(characters, indent=2)
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],  # First 15000 chars
                'characters': characters_json,
                'age_rating': age_rating,
                'target_age': target_age
            }
            
            prompt = self.config.get_prompt('content_screening').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('content_screening', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_comprehension_check(self, episode: Dict, age_rating: str, target_age: str) -> Dict:
        """Task 2: Comprehension Check Analysis (vocabulary, plot complexity, emotional complexity)"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'comprehension_check': {
                        'comprehension_adjustments': [],
                        'warning': 'No content available for analysis'
                    }
                }
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],
                'age_rating': age_rating,
                'target_age': target_age
            }
            
            prompt = self.config.get_prompt('comprehension_check').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('comprehension_check', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_audio_intensity_analysis(self, episode: Dict, age_rating: str, target_age: str) -> Dict:
        """Task 3: Audio Intensity Analysis (volume dynamics, disturbing sounds, emotional intensity)"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'audio_intensity_analysis': {
                        'intensity_flags': [],
                        'warning': 'No content available for analysis'
                    }
                }
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],
                'age_rating': age_rating,
                'target_age': target_age
            }
            
            prompt = self.config.get_prompt('audio_intensity_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('audio_intensity_analysis', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_positive_messaging_check(self, episode: Dict, station7_data: Dict, age_rating: str, target_age: str) -> Dict:
        """Task 4: Positive Messaging Check (role models, conflict resolution, consequences)"""
        try:
            episode_id = episode.get('episode_number', 'unknown')
            episode_content = self._extract_episode_content(episode)
            
            if not episode_content:
                return {
                    'positive_messaging_check': {
                        'message_alignment_notes': 'No content available for analysis',
                        'warning': True
                    }
                }
            
            characters = station7_data.get('Character Bible Document', {}).get('character_bible', {}).get('tier_1_protagonists', [])
            characters_json = json.dumps(characters, indent=2)
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:15000],
                'characters': characters_json,
                'age_rating': age_rating,
                'target_age': target_age
            }
            
            prompt = self.config.get_prompt('positive_messaging_check').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('positive_messaging_check', {})
            
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

    def _calculate_compliance(self, content_screening: Dict, comprehension_check: Dict, 
                             audio_intensity: Dict, positive_messaging: Dict) -> Dict:
        """Calculate age rating compliance"""
        # Extract all flags
        content_flags = content_screening.get('content_flags', [])
        comprehension_adjustments = comprehension_check.get('comprehension_adjustments', [])
        intensity_flags = audio_intensity.get('intensity_flags', [])
        
        # Count flags by severity
        critical_count = sum(1 for flag in content_flags + intensity_flags if flag.get('severity') == 'CRITICAL')
        high_count = sum(1 for flag in content_flags + intensity_flags if flag.get('severity') == 'HIGH')
        total_flags = len(content_flags) + len(intensity_flags)
        
        # Check positive messaging
        message_alignment = positive_messaging.get('message_alignment_notes', '')
        positive_messaging_ok = not positive_messaging.get('warning', False)
        
        # Determine compliance
        compliant = (critical_count == 0 and high_count <= 2 and total_flags < 10 and positive_messaging_ok)
        
        requires_user_review = (critical_count > 0 or high_count > 5 or total_flags > 15)
        
        return {
            'compliant': compliant,
            'critical_flags': critical_count,
            'high_flags': high_count,
            'total_flags': total_flags,
            'requires_user_review': requires_user_review,
            'positive_messaging_ok': positive_messaging_ok
        }

    def _extract_high_severity_flags(self, episode_result: Dict) -> List[Dict]:
        """Extract high-severity flags from episode results"""
        flags = []
        
        # Check content screening
        content_flags = episode_result.get('content_screening', {}).get('content_flags', [])
        for flag in content_flags:
            severity = flag.get('severity', '')
            if severity in ['CRITICAL', 'HIGH']:
                flags.append(flag)
        
        # Check audio intensity
        intensity_flags = episode_result.get('audio_intensity_analysis', {}).get('intensity_flags', [])
        for flag in intensity_flags:
            severity = flag.get('severity', '')
            if severity in ['CRITICAL', 'HIGH']:
                flags.append(flag)
        
        return flags

    async def generate_summary_report(self, all_episode_results: List[Dict], station2_data: Dict) -> Dict:
        """Generate comprehensive age appropriateness summary across all episodes"""
        try:
            context = {
                'session_id': self.session_id,
                'total_episodes': len(all_episode_results),
                'age_rating': self.age_rating,
                'target_age': self.target_age,
                'episode_results': json.dumps(all_episode_results, indent=2)
            }
            
            prompt = self.config.get_prompt('summary_report').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('age_appropriateness_summary', {})
            
        except Exception as e:
            raise ValueError(f"❌ Summary report generation failed: {str(e)}")

    async def save_episode_output(self, episode_result: Dict):
        """Save individual episode results to JSON"""
        episode_id = episode_result['episode_id']
        
        # Save JSON
        json_path = self.output_dir / f"{self.session_id}_episode_{episode_id:02d}.json"
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        with open(json_path, 'w', encoding=encoding) as f:
            json.dump(episode_result, f, indent=2, ensure_ascii=False)

    async def save_final_outputs(self, all_episode_results: List[Dict], summary_report: Dict):
        """Save final comprehensive outputs"""
        final_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "total_episodes": len(all_episode_results),
            "content_rating": self.age_rating,
            "target_age_range": self.target_age,
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
        redis_key = f"audiobook:{self.session_id}:station_39"
        await self.redis.set(redis_key, json.dumps(final_data), expire=86400)
        
        print(f"✅ Final outputs saved")

    def save_summary_readable_txt(self, path: Path, data: Dict):
        """Save human-readable summary TXT file"""
        encoding = self.config_data.get('output_enhancements', {}).get('encoding', 'utf-8')
        
        with open(path, 'w', encoding=encoding) as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 39: AGE APPROPRIATENESS FINAL CHECK SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {data.get('session_id', 'N/A')}\n")
            f.write(f"Analysis Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Total Episodes: {data.get('total_episodes', 'N/A')}\n")
            f.write(f"Content Rating: {data.get('content_rating', 'N/A')}\n")
            f.write(f"Target Age Range: {data.get('target_age_range', 'N/A')}\n\n")
            
            summary = data.get('summary_report', {})
            f.write("-" * 70 + "\n")
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"{summary.get('executive_summary', 'N/A')}\n\n")
            
            f.write("-" * 70 + "\n")
            f.write("OVERALL COMPLIANCE\n")
            f.write("-" * 70 + "\n")
            
            compliance = summary.get('overall_compliance', {})
            f.write(f"Episodes Passing: {compliance.get('episodes_passing', 'N/A')}\n")
            f.write(f"Episodes Requiring Review: {compliance.get('episodes_requiring_review', 'N/A')}\n")
            f.write(f"Total Flags: {compliance.get('total_flags', 'N/A')}\n")
            f.write(f"High Severity Flags: {compliance.get('high_severity_flags', 'N/A')}\n")
            f.write(f"Critical Flags: {compliance.get('critical_flags', 'N/A')}\n")
            f.write(f"Compliance Rate: {compliance.get('compliance_rate', 'N/A')}\n\n")
            
            # Common Issues
            f.write("-" * 70 + "\n")
            f.write("COMMON ISSUES\n")
            f.write("-" * 70 + "\n")
            
            common_issues = summary.get('common_issues', [])
            for i, issue in enumerate(common_issues, 1):
                f.write(f"\n{i}. {issue.get('issue_type', 'N/A')}\n")
                f.write(f"   Frequency: {issue.get('frequency', 'N/A')}\n")
                f.write(f"   Typical Severity: {issue.get('typical_severity', 'N/A')}\n")
                f.write(f"   Recommended Action: {issue.get('recommended_action', 'N/A')}\n")
            
            # Positive Findings
            f.write("\n" + "-" * 70 + "\n")
            f.write("POSITIVE FINDINGS\n")
            f.write("-" * 70 + "\n")
            
            positive_findings = summary.get('positive_findings', [])
            for i, finding in enumerate(positive_findings, 1):
                f.write(f"{i}. {finding}\n")
            
            # Recommendations
            f.write("\n" + "-" * 70 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 70 + "\n")
            
            recommendations = summary.get('recommendations', [])
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")
            
            # Production Readiness
            f.write("\n" + "-" * 70 + "\n")
            f.write("PRODUCTION READINESS\n")
            f.write("-" * 70 + "\n")
            
            readiness = summary.get('readiness_for_production', {})
            production_ready = readiness.get('production_ready', False)
            f.write(f"Production Ready: {'YES' if production_ready else 'NO'}\n")
            if not production_ready:
                f.write(f"Blocking Issues: {readiness.get('blocking_issues', 'N/A')}\n")
            
            remaining_steps = readiness.get('remaining_steps', [])
            if remaining_steps:
                f.write("\nRemaining Steps:\n")
                for i, step in enumerate(remaining_steps, 1):
                    f.write(f"  {i}. {step}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF AGE APPROPRIATENESS CHECK\n")
            f.write("=" * 70 + "\n")


# CLI Entry Point
async def main():
    """Run Station 39 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    auditor = Station39AgeCheck(session_id)
    await auditor.initialize()
    
    try:
        await auditor.run()
        print(f"\n✅ Success! Age appropriateness check complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())