"""
Station 4: Reference Mining & Seed Extraction

This station generates 20-25 cross-media references, extracts tactics from each,
and creates 65 story seeds across 4 categories.

Flow:
1. Load Station 2 + Station 3 data
2. Generate 20-25 cross-media references
3. OPTIONAL: User approves references (Enter/R/V, defaults to Enter)
4. Extract tactics from each reference (with progress indicators)
5. Generate 65 seeds in 4 batches:
   - 30 Micro-Moments (30-90 sec)
   - 20 Episode Beats (3-8 min)
   - 10 Season Arcs (multi-episode)
   - 5 Series-Defining Moments (iconic)
6. OPTIONAL: User reviews sample seeds (Enter/M/R/A, defaults to Enter)
7. Save JSON + TXT + CSV + Redis

Human Interactions: 2 optional (both default to continue)
"""

import asyncio
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json


class Station04ReferenceMining:
    """Station 4: Reference Mining & Seed Extraction"""

    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=4)
        self.output_dir = Path("output/station_04")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()

    async def run(self):
        """Main interactive flow"""
        print("=" * 60)
        print("🎬 STATION 4: REFERENCE MINING & SEED EXTRACTION")
        print("=" * 60)
        print()

        # Step 1: Get session ID
        session_id = input("📋 Enter session ID from previous stations: ").strip()
        if not session_id:
            print("❌ Session ID is required")
            return

        print()

        # Step 2: Load Station 2 and Station 3 data
        print("📂 Loading previous station data...")
        station2_data, station3_data = await self.load_previous_data(session_id)

        if not station2_data or not station3_data:
            print("❌ Could not load required data from previous stations")
            print("   Make sure you've run Station 2 and Station 3 first")
            return

        # Show summary
        print("✅ Data loaded successfully")
        print()
        print("-" * 60)
        print("📊 PROJECT SUMMARY")
        print("-" * 60)
        print(f"Working Title: {station2_data.get('working_title', 'N/A') if isinstance(station2_data, dict) else 'N/A'}")
        
        # Safely access nested data from station3_data
        if isinstance(station3_data, dict):
            chosen_blend = station3_data.get('chosen_blend', {})
            if isinstance(chosen_blend, dict):
                primary_genre = chosen_blend.get('primary_genre', 'N/A')
            else:
                primary_genre = 'N/A'
            
            age_guidelines = station3_data.get('age_guidelines', {})
            if isinstance(age_guidelines, dict):
                target_age = age_guidelines.get('target_age_range', 'N/A')
            else:
                target_age = 'N/A'
        else:
            primary_genre = 'N/A'
            target_age = 'N/A'
        
        print(f"Primary Genre: {primary_genre}")
        print(f"Target Age: {target_age}")
        print(f"Episode Count: {station2_data.get('episode_count', 'N/A') if isinstance(station2_data, dict) else 'N/A'}")
        print(f"Episode Length: {station2_data.get('episode_length', 'N/A') if isinstance(station2_data, dict) else 'N/A'}")
        print("-" * 60)
        print()

        # Step 3: Generate references
        print("🔍 Generating 20-25 cross-media references...")
        print("⏳ This may take 30-45 seconds...")
        print()

        references = await self.generate_references(station2_data, station3_data)

        if not references:
            print("❌ Failed to generate references")
            return

        print(f"✅ Generated {len(references)} references")
        print()

        # Step 4: OPTIONAL - Show references and get approval
        user_choice = self.show_references_and_get_approval(references)

        if user_choice == "R":
            print("\n🔄 Regenerating references...")
            print("⏳ This may take 30-45 seconds...")
            references = await self.generate_references(station2_data, station3_data)
            if not references:
                print("❌ Failed to regenerate references")
                return
            print(f"✅ Generated {len(references)} new references")
            user_choice = self.show_references_and_get_approval(references)

        if user_choice == "V":
            self.show_full_references(references)
            input("\nPress Enter to continue...")

        print()
        print("=" * 60)
        print("⚙️  EXTRACTING TACTICS FROM REFERENCES")
        print("=" * 60)
        print()

        # Step 5: Extract tactics from each reference
        tactics = await self.extract_tactics_with_progress(references, station2_data, station3_data)

        if not tactics:
            print("❌ Failed to extract tactics")
            return

        print()
        print(f"✅ Extracted {len(tactics)} tactics from {len(references)} references")
        print()

        # Step 6: Generate seeds in 4 batches
        print("=" * 60)
        print("🌱 GENERATING 65 STORY SEEDS")
        print("=" * 60)
        print()

        all_seeds = await self.generate_all_seeds(station2_data, station3_data, tactics)

        if not all_seeds:
            print("❌ Failed to generate seeds")
            return

        total_count = (len(all_seeds.get('micro_moments', [])) +
                      len(all_seeds.get('episode_beats', [])) +
                      len(all_seeds.get('season_arcs', [])) +
                      len(all_seeds.get('series_defining', [])))

        print()
        print(f"✅ Generated {total_count} seeds total")
        print()

        # Step 7: OPTIONAL - Show sample seeds and get approval
        user_choice = self.show_sample_seeds_and_get_approval(all_seeds)

        if user_choice == "R":
            print("\n🔄 Regenerating all seeds...")
            all_seeds = await self.generate_all_seeds(station2_data, station3_data, tactics)
            if not all_seeds:
                print("❌ Failed to regenerate seeds")
                return
            user_choice = self.show_sample_seeds_and_get_approval(all_seeds)

        if user_choice == "M":
            self.show_more_seeds(all_seeds)
            input("\nPress Enter to continue...")

        if user_choice == "A":
            self.show_all_seeds(all_seeds)
            input("\nPress Enter to continue...")

        print()
        print("=" * 60)
        print("💾 SAVING OUTPUT FILES")
        print("=" * 60)
        print()

        # Step 8: Save all outputs
        await self.save_output(
            session_id=session_id,
            station2_data=station2_data,
            station3_data=station3_data,
            references=references,
            tactics=tactics,
            seeds=all_seeds
        )

        print()
        print("=" * 60)
        print("✅ STATION 4 COMPLETE!")
        print("=" * 60)
        print()
        print(f"Session ID: {session_id}")
        print(f"Working Title: {station2_data.get('working_title', 'N/A')}")
        print()
        print("📄 Output files:")
        print(f"   - output/station_04/{session_id}_output.json")
        print(f"   - output/station_04/{session_id}_readable.txt")
        print(f"   - output/station_04/{session_id}_seeds.csv")
        print()
        print("📌 Ready to proceed to Station 5")
        print()

    async def load_previous_data(self, session_id: str) -> tuple[Optional[Dict], Optional[Dict]]:
        """Load Station 2 and Station 3 data from Redis"""
        try:
            # Load Station 2
            station2_key = f"audiobook:{session_id}:station_02"
            station2_raw = await self.redis.get(station2_key)
            if station2_raw:
                try:
                    station2_data = json.loads(station2_raw)
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing Station 2 data: {str(e)}")
                    station2_data = None
            else:
                station2_data = None

            # Load Station 3
            station3_key = f"audiobook:{session_id}:station_03"
            station3_raw = await self.redis.get(station3_key)
            if station3_raw:
                try:
                    station3_data = json.loads(station3_raw)
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing Station 3 data: {str(e)}")
                    station3_data = None
            else:
                station3_data = None

            return station2_data, station3_data

        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return None, None

    async def generate_references(self, station2_data: Dict, station3_data: Dict) -> List[Dict]:
        """Generate 20-25 cross-media references"""
        try:
            # Prepare context with safe data access
            working_title = station2_data.get('working_title', 'Untitled') if isinstance(station2_data, dict) else 'Untitled'
            
            # Safely get primary genre
            if isinstance(station3_data, dict):
                chosen_blend = station3_data.get('chosen_blend', {})
                primary_genre = chosen_blend.get('primary_genre', 'Drama') if isinstance(chosen_blend, dict) else 'Drama'
                
                age_guidelines = station3_data.get('age_guidelines', {})
                target_age_range = age_guidelines.get('target_age_range', 'General') if isinstance(age_guidelines, dict) else 'General'
                content_rating = age_guidelines.get('content_rating', 'PG') if isinstance(age_guidelines, dict) else 'PG'
            else:
                primary_genre = 'Drama'
                target_age_range = 'General'
                content_rating = 'PG'
            
            # Safely get secondary genres
            if isinstance(station2_data, dict):
                genre_tone = station2_data.get('genre_tone', {})
                secondary_genres = genre_tone.get('secondary_genres', []) if isinstance(genre_tone, dict) else []
            else:
                secondary_genres = []
            
            context = {
                'working_title': working_title,
                'primary_genre': primary_genre,
                'secondary_genres': secondary_genres,
                'target_age_range': target_age_range,
                'content_rating': content_rating
            }

            # Format prompt
            prompt = self.config.get_prompt('reference_gathering').format(**context)

            # Call LLM
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            # Extract JSON
            data = extract_json(response)
            references = data.get('references', [])
            
            # Validate count
            if len(references) < 20:
                print(f"⚠️  Only got {len(references)} references (target: 20-25)")
                print("   Continuing anyway...")

            if len(references) > 25:
                print(f"⚠️  Got {len(references)} references, trimming to 25")
                references = references[:25]

            return references

        except Exception as e:
            print(f"❌ Error generating references: {str(e)}")
            return []

    def show_references_and_get_approval(self, references: List[Dict]) -> str:
        """Show reference summary and get user approval (OPTIONAL)"""
        print("=" * 60)
        print("📚 GENERATED REFERENCES")
        print("=" * 60)
        print()
        print(f"Total references: {len(references)}")
        print()
        print("Sample references:")
        print()

        # Show first 5 references
        for i, ref in enumerate(references[:5], 1):
            print(f"{i}. {ref.get('title', 'Untitled')}")
            print(f"   Type: {ref.get('medium', 'Unknown')}")
            print(f"   Year: {ref.get('release_year', 'Unknown')}")
            print(f"   Relevance: {ref.get('why_selected', 'N/A')[:80]}...")
            print()

        if len(references) > 5:
            print(f"... and {len(references) - 5} more references")
            print()

        print("-" * 60)
        print("Options:")
        print("  [Enter] - Continue with these references (recommended)")
        print("  R - Regenerate all references")
        print("  V - View all references")
        print("-" * 60)

        choice = input("\n👉 Your choice (press Enter to continue): ").strip().upper()

        if choice == "":
            choice = "ENTER"

        return choice

    def show_full_references(self, references: List[Dict]):
        """Show all references in detail"""
        print()
        print("=" * 60)
        print("📚 ALL REFERENCES (DETAILED VIEW)")
        print("=" * 60)
        print()

        for i, ref in enumerate(references, 1):
            print(f"{i}. {ref.get('title', 'Untitled')}")
            print(f"   Type: {ref.get('medium', 'Unknown')}")
            print(f"   Year: {ref.get('release_year', 'Unknown')}")
            print(f"   Creator: {ref.get('creator', 'Unknown')}")
            print(f"   Genre Relevance: {ref.get('genre_relevance', 'N/A')}")
            print(f"   Age Appropriateness: {ref.get('age_appropriateness', 'N/A')}")
            print(f"   Why Selected: {ref.get('why_selected', 'N/A')}")
            print()

    async def extract_tactics_with_progress(self, references: List[Dict],
                                           station2_data: Dict,
                                           station3_data: Dict) -> List[Dict]:
        """Extract tactics from each reference with progress indicators"""
        all_tactics = []
        total = len(references)

        for i, ref in enumerate(references, 1):
            # Handle case where ref might be a string instead of dict
            if isinstance(ref, str):
                try:
                    ref = json.loads(ref)
                except json.JSONDecodeError:
                    print(f"   ⚠️  Failed: Invalid JSON in reference {i}")
                    continue
            
            print(f"⚙️  Extracting from reference {i}/{total}: {ref.get('title', 'Unknown')[:40]}...")

            try:
                # Prepare context with safe nested access
                chosen_blend = station3_data.get('chosen_blend', {})
                if isinstance(chosen_blend, str):
                    try:
                        chosen_blend = json.loads(chosen_blend)
                    except:
                        chosen_blend = {}
                
                age_guidelines = station3_data.get('age_guidelines', {})
                if isinstance(age_guidelines, str):
                    try:
                        age_guidelines = json.loads(age_guidelines)
                    except:
                        age_guidelines = {}
                
                project_context = {
                    'working_title': station2_data.get('working_title', 'Untitled'),
                    'primary_genre': chosen_blend.get('primary_genre', 'Drama'),
                    'target_age': age_guidelines.get('target_age_range', 'General'),
                    'content_rating': age_guidelines.get('content_rating', 'PG'),
                    'episode_count': station2_data.get('episode_count', '8-12'),
                    'episode_length': station2_data.get('episode_length', '35-45 min')
                }

                reference_details = {
                    'title': ref.get('title', 'Unknown'),
                    'type': ref.get('medium', 'Unknown'),
                    'year': ref.get('release_year', 'Unknown'),
                    'ref_primary_genre': ref.get('genre_relevance', 'Unknown'),
                    'secondary_genre': ref.get('genre_relevance', 'Unknown'),
                    'why_relevant': ref.get('why_selected', 'Unknown'),
                    'tactical_value': ref.get('why_selected', 'Unknown'),
                    'audio_lessons': ref.get('genre_relevance', 'Unknown')
                }

                # Format prompt
                prompt = self.config.get_prompt('tactical_extraction').format(
                    **project_context,
                    **reference_details
                )

                # Call LLM
                response = await self.openrouter.process_message(
                    prompt,
                    model_name=self.config.model,
                    max_tokens=2000
                )

                # Extract JSON
                data = extract_json(response)

                # Add reference title
                data['reference_title'] = ref.get('title', 'Unknown')
                all_tactics.append(data)

                print(f"   ✅ Extracted {len(data.get('tactics', []))} tactics")

            except Exception as e:
                print(f"   ⚠️  Failed: {str(e)}")
                continue

        return all_tactics

    async def generate_all_seeds(self, station2_data: Dict, station3_data: Dict,
                                 tactics: List[Dict]) -> Dict[str, List[Dict]]:
        """Generate all 65 seeds in 4 batches"""

        # Prepare context for all batches with safe nested access
        chosen_blend = station3_data.get('chosen_blend', {})
        if isinstance(chosen_blend, str):
            try:
                chosen_blend = json.loads(chosen_blend)
            except:
                chosen_blend = {}
        
        age_guidelines = station3_data.get('age_guidelines', {})
        if isinstance(age_guidelines, str):
            try:
                age_guidelines = json.loads(age_guidelines)
            except:
                age_guidelines = {}
        
        project_context = {
            'working_title': station2_data.get('working_title', 'Untitled'),
            'core_premise': station2_data.get('world_setting', {}).get('core_premise', 'N/A'),
            'central_conflict': station2_data.get('creative_promises', {}).get('premise', 'N/A'),
            'main_characters': age_guidelines.get('theme_complexity', 'Characters TBD'),
            'primary_genre': chosen_blend.get('primary_genre', 'Drama'),
            'target_age': age_guidelines.get('target_age_range', 'General'),
            'content_rating': age_guidelines.get('content_rating', 'PG'),
            'episode_count': station2_data.get('episode_count', '8-12'),
            'episode_length': station2_data.get('episode_length', '35-45 min'),
            'breaking_points': str(station2_data.get('format_specifications', {}).get('episode_structure', 'Standard breaks')),
            'tonal_shift_moments': str(station3_data.get('tone_calibration', {}).get('tonal_shift_moments', [])),
            'creative_promises': str(station2_data.get('creative_promises', {}))
        }

        # Format tactics summary
        tactics_summary = self.format_tactics_summary(tactics)

        # Generate each batch
        results = {}

        # Batch 1: Micro-Moments (30 seeds)
        print("🌱 Batch 1/4: Generating 30 Micro-Moments (30-90 sec)...")
        print("⏳ This may take 45-60 seconds...")
        micro_moments = await self.generate_seed_batch(
            'seed_generation_micro',
            {**project_context, 'tactics_summary': tactics_summary}
        )
        results['micro_moments'] = micro_moments.get('micro_moments', [])
        print(f"   ✅ Generated {len(results['micro_moments'])} micro-moments")
        print()

        # Batch 2: Episode Beats (20 seeds)
        print("🌱 Batch 2/4: Generating 20 Episode Beats (3-8 min)...")
        print("⏳ This may take 45-60 seconds...")
        episode_beats = await self.generate_seed_batch(
            'seed_generation_beats',
            {**project_context, 'tactics_summary': tactics_summary}
        )
        results['episode_beats'] = episode_beats.get('episode_beats', [])
        print(f"   ✅ Generated {len(results['episode_beats'])} episode beats")
        print()

        # Batch 3: Season Arcs (10 seeds)
        print("🌱 Batch 3/4: Generating 10 Season Arcs (multi-episode)...")
        print("⏳ This may take 45-60 seconds...")
        season_arcs = await self.generate_seed_batch(
            'seed_generation_arcs',
            {**project_context, 'tactics_summary': tactics_summary}
        )
        results['season_arcs'] = season_arcs.get('season_arcs', [])
        print(f"   ✅ Generated {len(results['season_arcs'])} season arcs")
        print()

        # Batch 4: Series-Defining Moments (5 seeds)
        print("🌱 Batch 4/4: Generating 5 Series-Defining Moments (iconic)...")
        print("⏳ This may take 45-60 seconds...")
        series_defining = await self.generate_seed_batch(
            'seed_generation_defining',
            {**project_context, 'tactics_summary': tactics_summary}
        )
        results['series_defining'] = series_defining.get('defining_moments', [])
        print(f"   ✅ Generated {len(results['series_defining'])} series-defining moments")

        return results

    def format_tactics_summary(self, tactics: List[Dict]) -> str:
        """Format tactics for inclusion in seed generation prompts"""
        summary = []
        for tactic_group in tactics[:10]:  # Use top 10 references
            ref_title = tactic_group.get('reference_title', 'Unknown')
            tactic_list = tactic_group.get('tactics', [])

            for tactic in tactic_list[:3]:  # Top 3 tactics per reference
                summary.append(
                    f"- {tactic.get('tactic_name', 'Tactic')} (from {ref_title}): "
                    f"{tactic.get('audio_application', 'N/A')[:100]}"
                )

        return "\n".join(summary[:30])  # Max 30 tactics

    async def generate_seed_batch(self, prompt_name: str, context: Dict) -> Dict:
        """Generate a batch of seeds using specified prompt"""
        try:
            prompt = self.config.get_prompt(prompt_name).format(**context)

            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )

            data = extract_json(response)
            return data

        except Exception as e:
            print(f"   ⚠️  Error: {str(e)}")
            return {}

    def show_sample_seeds_and_get_approval(self, all_seeds: Dict) -> str:
        """Show sample seeds and get user approval (OPTIONAL)"""
        print("=" * 60)
        print("🌱 GENERATED SEEDS SAMPLE")
        print("=" * 60)
        print()
        print(f"Micro-Moments: {len(all_seeds.get('micro_moments', []))}")
        print(f"Episode Beats: {len(all_seeds.get('episode_beats', []))}")
        print(f"Season Arcs: {len(all_seeds.get('season_arcs', []))}")
        print(f"Series-Defining: {len(all_seeds.get('series_defining', []))}")
        print()

        # Show 1 sample from each category
        print("Sample Micro-Moment:")
        if all_seeds.get('micro_moments'):
            seed = all_seeds['micro_moments'][0]
            print(f"  Title: {seed.get('title', 'N/A')}")
            print(f"  Duration: {seed.get('duration', 'N/A')}")
            print(f"  Idea: {seed.get('core_idea', 'N/A')[:100]}...")
        print()

        print("Sample Episode Beat:")
        if all_seeds.get('episode_beats'):
            seed = all_seeds['episode_beats'][0]
            print(f"  Title: {seed.get('title', 'N/A')}")
            print(f"  Duration: {seed.get('duration', 'N/A')}")
            print(f"  Idea: {seed.get('core_idea', 'N/A')[:100]}...")
        print()

        print("Sample Season Arc:")
        if all_seeds.get('season_arcs'):
            seed = all_seeds['season_arcs'][0]
            print(f"  Title: {seed.get('title', 'N/A')}")
            print(f"  Span: {seed.get('episode_span', 'N/A')}")
            print(f"  Idea: {seed.get('core_idea', 'N/A')[:100]}...")
        print()

        print("Sample Series-Defining Moment:")
        if all_seeds.get('series_defining'):
            seed = all_seeds['series_defining'][0]
            print(f"  Title: {seed.get('title', 'N/A')}")
            print(f"  Placement: {seed.get('episode_placement', 'N/A')}")
            print(f"  Idea: {seed.get('core_idea', 'N/A')[:100]}...")
        print()

        print("-" * 60)
        print("Options:")
        print("  [Enter] - Continue with these seeds (recommended)")
        print("  M - Show more samples (3 per category)")
        print("  R - Regenerate all seeds")
        print("  A - View all seeds")
        print("-" * 60)

        choice = input("\n👉 Your choice (press Enter to continue): ").strip().upper()

        if choice == "":
            choice = "ENTER"

        return choice

    def show_more_seeds(self, all_seeds: Dict):
        """Show 3 samples from each category"""
        print()
        print("=" * 60)
        print("🌱 MORE SEED SAMPLES (3 PER CATEGORY)")
        print("=" * 60)
        print()

        for category, seeds in all_seeds.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            print("-" * 40)
            for i, seed in enumerate(seeds[:3], 1):
                print(f"\n{i}. {seed.get('title', 'N/A')}")
                print(f"   {seed.get('core_idea', seed.get('description', 'N/A'))[:150]}...")

    def show_all_seeds(self, all_seeds: Dict):
        """Show all seeds"""
        print()
        print("=" * 60)
        print("🌱 ALL SEEDS (FULL VIEW)")
        print("=" * 60)

        for category, seeds in all_seeds.items():
            print(f"\n\n{category.upper().replace('_', ' ')} ({len(seeds)} total):")
            print("=" * 60)
            for i, seed in enumerate(seeds, 1):
                print(f"\n{i}. {seed.get('title', 'N/A')}")
                for key, value in seed.items():
                    if key != 'title':
                        print(f"   {key}: {value}")

    async def save_output(self, session_id: str, station2_data: Dict,
                         station3_data: Dict, references: List[Dict],
                         tactics: List[Dict], seeds: Dict):
        """Save all output files (JSON + TXT + CSV + Redis)"""

        # Prepare full output
        output_data = {
            'session_id': session_id,
            'working_title': station2_data.get('working_title', 'Untitled'),
            'original_seed': station2_data.get('original_seed', 'N/A'),
            'timestamp': datetime.now().isoformat(),
            'references': references,
            'tactical_extractions': tactics,
            'seeds': seeds,
            'summary': {
                'total_references': len(references),
                'total_tactical_extractions': len(tactics),
                'total_seeds': (
                    len(seeds.get('micro_moments', [])) +
                    len(seeds.get('episode_beats', [])) +
                    len(seeds.get('season_arcs', [])) +
                    len(seeds.get('series_defining', []))
                )
            }
        }

        # Save JSON
        json_path = self.output_dir / f"{session_id}_output.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_path}")

        # Save TXT
        txt_path = self.output_dir / f"{session_id}_readable.txt"
        self.save_readable_txt(txt_path, output_data)
        print(f"✅ Saved TXT: {txt_path}")

        # Save CSV
        csv_path = self.output_dir / f"{session_id}_seeds.csv"
        self.save_seeds_csv(csv_path, seeds)
        print(f"✅ Saved CSV: {csv_path}")

        # Save to Redis
        redis_key = f"audiobook:{session_id}:station_04"
        await self.redis.set(redis_key, json.dumps(output_data), expire=86400)
        print(f"✅ Saved to Redis: {redis_key}")

    def save_readable_txt(self, path: Path, data: Dict):
        """Save human-readable TXT file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 4: REFERENCE MINING & SEED EXTRACTION\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Session ID: {data['session_id']}\n")
            f.write(f"Working Title: {data['working_title']}\n")
            f.write(f"Generated: {data['timestamp']}\n")
            f.write("\n")

            f.write("-" * 70 + "\n")
            f.write("SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total References: {data['summary']['total_references']}\n")
            f.write(f"Total Tactical Extractions: {data['summary']['total_tactical_extractions']}\n")
            f.write(f"Total Seeds: {data['summary']['total_seeds']}\n")
            f.write("\n\n")

            # References
            f.write("=" * 70 + "\n")
            f.write("CROSS-MEDIA REFERENCES\n")
            f.write("=" * 70 + "\n\n")

            for i, ref in enumerate(data['references'], 1):
                f.write(f"{i}. {ref.get('title', 'Untitled')}\n")
                f.write(f"   Type: {ref.get('medium', 'Unknown')}\n")
                f.write(f"   Year: {ref.get('release_year', 'Unknown')}\n")
                f.write(f"   Creator: {ref.get('creator', 'Unknown')}\n")
                f.write(f"   Why Selected: {ref.get('why_selected', 'N/A')}\n")
                f.write("\n")

            # Tactics (abbreviated)
            f.write("\n" + "=" * 70 + "\n")
            f.write("TACTICAL EXTRACTIONS (SUMMARY)\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Extracted {len(data['tactical_extractions'])} tactic groups from references\n")
            f.write("(See JSON file for full details)\n\n")

            # Seeds
            f.write("\n" + "=" * 70 + "\n")
            f.write("STORY SEEDS\n")
            f.write("=" * 70 + "\n\n")

            seeds = data['seeds']

            # Micro-Moments
            f.write(f"MICRO-MOMENTS ({len(seeds.get('micro_moments', []))} total)\n")
            f.write("-" * 70 + "\n")
            for i, seed in enumerate(seeds.get('micro_moments', []), 1):
                f.write(f"\n{i}. {seed.get('title', 'Untitled')}\n")
                f.write(f"   Duration: {seed.get('duration', 'N/A')}\n")
                f.write(f"   Placement: {seed.get('placement', 'N/A')}\n")
                f.write(f"   Core Idea: {seed.get('core_idea', 'N/A')}\n")
                f.write(f"   Audio Hook: {seed.get('audio_hook', 'N/A')}\n")

            # Episode Beats
            f.write(f"\n\nEPISODE BEATS ({len(seeds.get('episode_beats', []))} total)\n")
            f.write("-" * 70 + "\n")
            for i, seed in enumerate(seeds.get('episode_beats', []), 1):
                f.write(f"\n{i}. {seed.get('title', 'Untitled')}\n")
                f.write(f"   Duration: {seed.get('duration', 'N/A')}\n")
                f.write(f"   Placement: {seed.get('episode_placement', 'N/A')}\n")
                f.write(f"   Beat Type: {seed.get('beat_type', 'N/A')}\n")
                f.write(f"   Core Idea: {seed.get('core_idea', 'N/A')}\n")

            # Season Arcs
            f.write(f"\n\nSEASON ARCS ({len(seeds.get('season_arcs', []))} total)\n")
            f.write("-" * 70 + "\n")
            for i, seed in enumerate(seeds.get('season_arcs', []), 1):
                f.write(f"\n{i}. {seed.get('title', 'Untitled')}\n")
                f.write(f"   Arc Type: {seed.get('arc_type', 'N/A')}\n")
                f.write(f"   Episode Span: {seed.get('episode_span', 'N/A')}\n")
                f.write(f"   Core Idea: {seed.get('core_idea', 'N/A')}\n")

            # Series-Defining
            f.write(f"\n\nSERIES-DEFINING MOMENTS ({len(seeds.get('series_defining', []))} total)\n")
            f.write("-" * 70 + "\n")
            for i, seed in enumerate(seeds.get('series_defining', []), 1):
                f.write(f"\n{i}. {seed.get('title', 'Untitled')}\n")
                f.write(f"   Moment Type: {seed.get('moment_type', 'N/A')}\n")
                f.write(f"   Placement: {seed.get('episode_placement', 'N/A')}\n")
                f.write(f"   Core Idea: {seed.get('core_idea', 'N/A')}\n")
                f.write(f"   Why Defining: {seed.get('why_defining', 'N/A')}\n")

            f.write("\n\n" + "=" * 70 + "\n")
            f.write("END OF STATION 4 OUTPUT\n")
            f.write("=" * 70 + "\n")

    def save_seeds_csv(self, path: Path, seeds: Dict):
        """Save seeds to CSV for easy analysis"""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Category', 'Title', 'Duration/Span', 'Placement',
                'Core Idea', 'Audio Element', 'Inspired By'
            ])

            # Micro-Moments
            for seed in seeds.get('micro_moments', []):
                writer.writerow([
                    'Micro-Moment',
                    seed.get('title', 'N/A'),
                    seed.get('duration', 'N/A'),
                    seed.get('placement', 'N/A'),
                    seed.get('core_idea', 'N/A')[:200],
                    seed.get('audio_hook', 'N/A')[:100],
                    seed.get('inspired_by_tactic', 'N/A')
                ])

            # Episode Beats
            for seed in seeds.get('episode_beats', []):
                writer.writerow([
                    'Episode Beat',
                    seed.get('title', 'N/A'),
                    seed.get('duration', 'N/A'),
                    seed.get('episode_placement', 'N/A'),
                    seed.get('core_idea', 'N/A')[:200],
                    seed.get('audio_structure', 'N/A')[:100],
                    seed.get('inspired_by_tactic', 'N/A')
                ])

            # Season Arcs
            for seed in seeds.get('season_arcs', []):
                writer.writerow([
                    'Season Arc',
                    seed.get('title', 'N/A'),
                    seed.get('episode_span', 'N/A'),
                    seed.get('episode_span', 'N/A'),
                    seed.get('core_idea', 'N/A')[:200],
                    seed.get('audio_continuity', 'N/A')[:100],
                    seed.get('inspired_by_tactic', 'N/A')
                ])

            # Series-Defining
            for seed in seeds.get('series_defining', []):
                writer.writerow([
                    'Series-Defining',
                    seed.get('title', 'N/A'),
                    seed.get('duration', 'N/A'),
                    seed.get('episode_placement', 'N/A'),
                    seed.get('core_idea', 'N/A')[:200],
                    seed.get('audio_signature', 'N/A')[:100],
                    seed.get('inspired_by_tactic', 'N/A')
                ])


async def main():
    """Main entry point"""
    station = Station04ReferenceMining()
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
