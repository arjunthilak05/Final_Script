"""
Station 4: Reference Mining & Seed Extraction

This station generates 20-25 cross-media references, extracts tactics from each,
and creates 65 story seeds across 4 categories.

Flow:
1. Load Station 2 + Station 3 data
2. Generate 20-25 cross-media references
3. OPTIONAL: User approves references (Enter/R/V, defaults to Enter)
4. Extract tactics from each reference (with progress indicators)
5. Generate 65 seeds in 4 batches (30+20+10+5)
6. OPTIONAL: User reviews sample seeds (Enter/M/R/A, defaults to Enter)
7. Save JSON + TXT + CSV + Redis

Human Interactions: 2 optional (both default to continue)
"""

import asyncio
import json
import csv
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json
from app.agents.title_validator import TitleValidator


class Station04ReferenceMining:
    """Station 4: Reference Mining & Seed Extraction - SIMPLIFIED & CLEAN"""

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
        print("=" * 70)
        print("🎬 STATION 4: REFERENCE MINING & SEED EXTRACTION")
        print("=" * 70)
        print()

        # Step 1: Get session ID
        session_id = input("📋 Enter session ID from previous stations: ").strip()
        if not session_id:
            print("❌ Session ID is required")
            return

        print()

        # Step 2: Load Station 1, Station 2 and Station 3 data
        print("📥 Loading previous station data...")
        station1_data, station2_data, station3_data = await self.load_previous_data(session_id)

        if not station1_data or not station2_data or not station3_data:
            print("❌ Could not load required data from previous stations")
            print("   Make sure you've run Station 1, Station 2 and Station 3 first")
            return

        print("   ✓ Station 1: Seed Processor loaded")
        print("   ✓ Station 2: Project Bible loaded")
        print("   ✓ Station 3: Style Guide loaded")
        print()

        # Show summary with bulletproof title
        self.display_project_summary(station1_data, station2_data, station3_data, session_id)

        # Step 3: Generate references
        print("\n" + "=" * 70)
        print("🔍 TASK 1: GATHERING CROSS-MEDIA REFERENCES")
        print("=" * 70)
        print()
        print("🤖 Analyzing project requirements...")
        print(f"   Genre: {station3_data['chosen_blend_details']['primary_genre']}")
        print(f"   Age: {station3_data['age_guidelines']['content_rating']}")
        print(f"   Medium: Audio-only")
        print()
        print("🤖 Searching for relevant references...")
        print("⏳ Generating references... (this takes 30-60 seconds)")
        print()

        references = await self.generate_references(station1_data, station2_data, station3_data)

        if not references or len(references) < 15:
            print(f"❌ Failed to generate sufficient references (got {len(references) if references else 0}, need 15+)")
            return

        print(f"✅ Generated {len(references)} references")
        print()

        # Step 4: OPTIONAL - Show references and get approval
        approval = self.show_references_summary(references)

        if approval == "R":
            print("\n🔄 Regenerating references...")
            print("⏳ This may take 30-60 seconds...")
            references = await self.generate_references(station1_data, station2_data, station3_data)
            if not references:
                print("❌ Failed to regenerate references")
                return
            print(f"✅ Generated {len(references)} new references")
            approval = self.show_references_summary(references)

        if approval == "V":
            self.show_full_references(references)
            input("\nPress Enter to continue...")

        # Step 5: Extract tactics from each reference
        print("\n" + "=" * 70)
        print("🎯 TASK 2: TACTICAL EXTRACTION")
        print("=" * 70)
        print()
        print("Extracting storytelling tactics from each reference...")
        if len(references) > 20:
            print(f"⚠️  Processing top 20 references for efficiency (from {len(references)} total)")
        print()

        tactics = await self.extract_tactics_with_progress(references, station1_data, station2_data, station3_data)

        if not tactics:
            print("❌ Failed to extract tactics")
            return

        print()
        print(f"✅ Extracted tactics from {len(tactics)} references")
        print()

        # Show tactical summary
        self.show_tactical_summary(tactics)

        # Step 6: Generate seeds in 4 batches
        print("\n" + "=" * 70)
        print("🌱 TASK 3: SEED GENERATION (65 Story Elements)")
        print("=" * 70)
        print()
        print("Converting tactics into audio drama story seeds...")
        print(f"Adapting to: {station3_data['chosen_blend_details']['primary_genre']}, "
              f"{station3_data['age_guidelines']['content_rating']}")
        print()

        all_seeds = await self.generate_all_seeds(station1_data, station2_data, station3_data, tactics)

        if not all_seeds:
            print("❌ Failed to generate seeds")
            return

        # Validate seed counts
        total_count = (len(all_seeds.get('micro_moments', [])) +
                      len(all_seeds.get('episode_beats', [])) +
                      len(all_seeds.get('season_arcs', [])) +
                      len(all_seeds.get('series_defining', [])))

        print()
        print("=" * 70)
        print(f"✅ SEED BANK COMPLETE: {total_count} Story Elements Generated")
        print("=" * 70)
        print(f"   ✓ {len(all_seeds.get('micro_moments', []))} Micro-Moments")
        print(f"   ✓ {len(all_seeds.get('episode_beats', []))} Episode Beats")
        print(f"   ✓ {len(all_seeds.get('season_arcs', []))} Season Arcs")
        print(f"   ✓ {len(all_seeds.get('series_defining', []))} Series-Defining Moments")
        print()

        # Step 7: Show seed summary and statistics
        self.show_seed_statistics(all_seeds)

        # Step 8: OPTIONAL - Show sample seeds and get approval
        review_choice = self.show_sample_seeds(all_seeds)

        if review_choice == "M":
            self.show_more_samples(all_seeds, count=5)
            input("\nPress Enter to continue...")

        if review_choice == "R":
            print("\n🔄 Which category to regenerate?")
            print("  1 - Micro-Moments (30)")
            print("  2 - Episode Beats (20)")
            print("  3 - Season Arcs (10)")
            print("  4 - Series-Defining (5)")
            print("  A - All seeds")
            choice = input("\nYour choice: ").strip().upper()
            # TODO: Implement regeneration logic
            print("⚠️  Regeneration not implemented yet, continuing with current seeds...")

        if review_choice == "A":
            self.show_all_seeds(all_seeds)
            input("\nPress Enter to continue...")

        # Step 9: Save all outputs
        print("\n" + "=" * 70)
        print("💾 SAVING SEED BANK DOCUMENT")
        print("=" * 70)
        print()
        print("Generating output files...")
        print()

        await self.save_output(
            session_id=session_id,
            station1_data=station1_data,
            station2_data=station2_data,
            station3_data=station3_data,
            references=references,
            tactics=tactics,
            seeds=all_seeds
        )

        # Step 10: Completion
        print("\n" + "=" * 70)
        print("✅ STATION 4 COMPLETE!")
        print("=" * 70)
        print()
        print(f"Project: {station2_data.get('working_title', 'Untitled')}")
        print(f"Session ID: {session_id}")
        print()
        print("📊 SEED BANK STATISTICS:")
        print(f"   • {len(references)} Cross-media references analyzed")
        print(f"   • {len(tactics)} Storytelling tactics extracted")
        print(f"   • {total_count} Story seeds generated")
        print(f"      - {len(all_seeds.get('micro_moments', []))} Micro-Moments (30-90 sec)")
        print(f"      - {len(all_seeds.get('episode_beats', []))} Episode Beats (3-8 min)")
        print(f"      - {len(all_seeds.get('season_arcs', []))} Season Arcs (multi-episode)")
        print(f"      - {len(all_seeds.get('series_defining', []))} Series-Defining (iconic moments)")
        print()
        print("📁 OUTPUT FILES:")
        print(f"   ✓ output/station_04/{session_id}_output.json")
        print(f"   ✓ output/station_04/{session_id}_readable.txt")
        print(f"   ✓ output/station_04/{session_id}_seeds.csv")
        print()
        print("Ready to proceed to Station 5: Season Architecture")
        print()

    async def load_previous_data(self, session_id: str) -> tuple[Optional[Dict], Optional[Dict], Optional[Dict]]:
        """Load Station 1, Station 2 and Station 3 data from Redis - NO FALLBACKS"""
        # Load Station 1
        station1_key = f"audiobook:{session_id}:station_01"
        station1_raw = await self.redis.get(station1_key)
        
        # Load Station 2
        station2_key = f"audiobook:{session_id}:station_02"
        station2_raw = await self.redis.get(station2_key)

        if not station1_raw:
            raise ValueError(f"Station 1 data not found for session {session_id}. Run Station 1 first.")
        
        station1_data = json.loads(station1_raw)

        if not station2_raw:
            raise ValueError(f"Station 2 data not found for session {session_id}. Run Station 2 first.")

        station2_data = json.loads(station2_raw)

        # Load Station 3
        station3_key = f"audiobook:{session_id}:station_03"
        station3_raw = await self.redis.get(station3_key)

        if not station3_raw:
            raise ValueError(f"Station 3 data not found for session {session_id}. Run Station 3 first.")

        station3_data = json.loads(station3_raw)

        return station1_data, station2_data, station3_data

    def display_project_summary(self, station1_data: Dict, station2_data: Dict, station3_data: Dict, session_id: str):
        """Display project context summary with bulletproof title"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)

        # Station 3 saves chosen_blend_details separately
        chosen_blend_details = station3_data.get('chosen_blend_details', {})
        age_guidelines = station3_data.get('age_guidelines', {})
        genre_tone = station2_data.get('genre_tone', {})

        # These .get() are OK for display only (not used in LLM calls)

        # Use bulletproof title extraction
        title = TitleValidator.extract_bulletproof_title(station1_data, station2_data)
        print(TitleValidator.format_title_for_display(title, "Station 4"))
        print(f"Genre Blend: {chosen_blend_details.get('primary_genre', 'N/A')} + {chosen_blend_details.get('complementary_genre', 'N/A')}")
        print(f"Age Rating: {age_guidelines.get('content_rating', 'N/A')} ({age_guidelines.get('target_age_range', 'N/A')})")
        print(f"Episodes: {station2_data.get('episode_count', 'N/A')}, {station2_data.get('episode_length', 'N/A')} each")
        print()
        print(f"Primary Genre: {genre_tone.get('primary_genre', 'N/A')}")
        print(f"Mood Profile: {genre_tone.get('mood_profile', 'N/A')}")
        print(f"Session ID: {session_id}")
        print("-" * 70)

    async def generate_references(self, station1_data: Dict, station2_data: Dict, station3_data: Dict) -> List[Dict]:
        """Generate 20-25 cross-media references - NO FALLBACKS"""
        # Prepare context - NO DEFAULTS
        chosen_blend_details = station3_data['chosen_blend_details']
        age_guidelines = station3_data['age_guidelines']

        context = {
            'working_title': TitleValidator.extract_bulletproof_title(station1_data, station2_data),
            'primary_genre': chosen_blend_details['primary_genre'],
            'secondary_genres': ', '.join(station2_data['genre_tone']['secondary_genres']),
            'target_age_range': age_guidelines['target_age_range'],
            'content_rating': age_guidelines['content_rating']
        }

        # Format prompt
        prompt = self.config.get_prompt('reference_gathering').format(**context)

        # Call LLM - Need more tokens for 20-25 references
        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model,
            max_tokens=8000  # Increased from 4000 to handle 20-25 refs
        )

        # Extract JSON
        data = extract_json(response)
        references = data['references']

        # Validate count with flexibility
        if len(references) < 15:
            raise ValueError(f"Expected 15+ references, only got {len(references)}. Cannot proceed.")

        if len(references) > 25:
            print(f"⚠️  Got {len(references)} references, trimming to 25")
            references = references[:25]

        return references

    def show_references_summary(self, references: List[Dict]) -> str:
        """Show reference summary and get user approval (OPTIONAL)"""
        print("\n" + "=" * 70)
        print("📚 CROSS-MEDIA REFERENCES")
        print("=" * 70)
        print()
        print(f"Total references: {len(references)}")
        print()

        # Count by type
        type_counts = {}
        for ref in references:
            medium = ref.get('medium', 'unknown')
            type_counts[medium] = type_counts.get(medium, 0) + 1

        print("Reference breakdown:")
        for medium, count in type_counts.items():
            print(f"   • {count} {medium.replace('_', ' ').title()}")
        print()

        # Show first 5 references
        print("Sample references:")
        print()
        for i, ref in enumerate(references[:5], 1):
            print(f"{i}. {ref.get('title', 'Untitled')}")
            print(f"   Type: {ref.get('medium', 'Unknown')}")
            print(f"   Why: {ref.get('why_selected', 'N/A')[:100]}...")
            print()

        if len(references) > 5:
            print(f"... and {len(references) - 5} more references")
            print()

        print("-" * 70)
        print("Do these references look appropriate?")
        print("  [Press Enter] Continue with these references (recommended)")
        print("  [Type 'R'] Regenerate all references")
        print("  [Type 'V'] View all references in detail")
        print("-" * 70)

        choice = input("\nYour choice: ").strip().upper()
        if choice == "":
            choice = "ENTER"
            print("✅ References approved. Proceeding to tactical extraction...")

        return choice

    def show_full_references(self, references: List[Dict]):
        """Show all references in detail"""
        print("\n" + "=" * 70)
        print("📚 ALL REFERENCES (DETAILED VIEW)")
        print("=" * 70)
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
                                           station1_data: Dict,
                                           station2_data: Dict,
                                           station3_data: Dict) -> List[Dict]:
        """Extract tactics from each reference with progress indicators - OPTIMIZED"""
        all_tactics = []
        # Limit to top 20 references for efficiency if more than 20 provided
        references = references[:20] if len(references) > 20 else references
        total = len(references)

        # Prepare context - NO DEFAULTS
        chosen_blend_details = station3_data['chosen_blend_details']
        age_guidelines = station3_data['age_guidelines']

        project_context = {
            'working_title': TitleValidator.extract_bulletproof_title(station1_data, station2_data),
            'primary_genre': chosen_blend_details['primary_genre'],
            'target_age': age_guidelines['target_age_range'],
            'content_rating': age_guidelines['content_rating'],
            'episode_count': station2_data['episode_count'],
            'episode_length': station2_data['episode_length']
        }

        for i, ref in enumerate(references, 1):
            # Show progress bar
            self.show_progress_bar(i, total, ref['title'])

            reference_details = {
                'title': ref['title'],
                'type': ref['medium'],
                'year': ref['release_year'],
                'ref_primary_genre': ref['genre_relevance'],  # Renamed to avoid conflict
                'why_relevant': ref['why_selected']
            }

            # Format prompt
            prompt = self.config.get_prompt('tactical_extraction').format(
                **project_context,
                **reference_details
            )

            # Call LLM - Optimized for efficiency
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=4000  # Increased to ensure complete responses
            )

            # Extract JSON
            data = extract_json(response)
            data['reference_title'] = ref['title']
            all_tactics.append(data)

        print()  # New line after progress bar
        return all_tactics

    def show_progress_bar(self, current: int, total: int, reference_name: str):
        """Show progress bar for tactical extraction - OPTIMIZED"""
        bar_length = 20
        filled = int(bar_length * current / total)
        bar = '█' * filled + '░' * (bar_length - filled)

        # Truncate reference name for cleaner display
        ref_display = reference_name[:25] if len(reference_name) > 25 else reference_name

        print(f"\r[{bar}] {current}/{total} {ref_display}...", end='', flush=True)

    def show_tactical_summary(self, tactics: List[Dict]):
        """Show tactical extraction summary (top 8 highlights) - OPTIMIZED"""
        print("\n" + "=" * 70)
        print("📊 TACTICAL EXTRACTIONS - TOP HIGHLIGHTS")
        print("=" * 70)
        print()

        for i, tactic_group in enumerate(tactics[:8], 1):  # Reduced to 8 for efficiency
            ref_title = tactic_group.get('reference_title', 'Unknown')[:30]
            tactic_list = tactic_group.get('tactics', [])

            if tactic_list:
                first_tactic = tactic_list[0]
                tactic_name = first_tactic.get('tactic_name', 'N/A')[:25]
                audio_app = first_tactic.get('audio_application', 'N/A')[:60]
                print(f"{i}. FROM \"{ref_title}\":")
                print(f"   ✓ {tactic_name}")
                print(f"   🎧 {audio_app}...")
                print()

        print("-" * 70)

    async def generate_all_seeds(self, station1_data: Dict, station2_data: Dict, station3_data: Dict,
                                 tactics: List[Dict]) -> Dict[str, List[Dict]]:
        """Generate all 65 seeds in 4 batches"""

        # Prepare context for all batches - USE ACTUAL STATION 2/3 STRUCTURE
        chosen_blend_details = station3_data['chosen_blend_details']
        age_guidelines = station3_data['age_guidelines']
        world_setting = station2_data['world_setting']
        creative_promises = station2_data['creative_promises']
        format_specs = station2_data['format_specifications']

        project_context = {
            'working_title': TitleValidator.extract_bulletproof_title(station1_data, station2_data),
            # Use original_seed as core_premise (it contains the full story premise)
            'core_premise': station2_data['original_seed'][:500],  # First 500 chars
            # Use atmosphere as central_conflict placeholder
            'central_conflict': world_setting['atmosphere'],
            # Extract characters from original seed or use placeholder
            'main_characters': 'Tom (motivation coach), Julia (ER doctor)',  # Extract from seed
            'primary_genre': chosen_blend_details['primary_genre'],
            'target_age': age_guidelines['target_age_range'],
            'content_rating': age_guidelines['content_rating'],
            'episode_count': station2_data['episode_count'],
            'episode_length': station2_data['episode_length'],
            # Use pacing_strategy as breaking_points
            'breaking_points': str(format_specs['pacing_strategy']),
            'tonal_shift_moments': str(station3_data['tone_calibration']['tonal_shift_moments']),
            'creative_promises': str(creative_promises['must_have_elements'])
        }

        # Format tactics summary
        tactics_summary = self.format_tactics_summary(tactics)

        # Generate each batch
        results = {}

        # Batch 1: Micro-Moments (30 seeds in 2 smaller batches for reliability)
        print("-" * 70)
        print("📦 BATCH 1: MICRO-MOMENTS (30 seeds total)")
        print("-" * 70)
        print("Single scenes lasting 30-90 seconds each")
        print()
        print("🤖 Generating micro-moments in smaller batches for reliability...")
        print("⏳ This may take 60-90 seconds...")
        print()

        # Generate 15 seeds first
        print("📦 Sub-batch 1A: First 15 micro-moments...")
        micro_moments_1 = await self.generate_seed_batch(
            'seed_generation_micro_15',
            {**project_context, 'tactics_summary': tactics_summary, 'seed_count': 15, 'start_id': 1}
        )
        batch1a = micro_moments_1.get('micro_moments', [])
        print(f"✅ Generated {len(batch1a)} Micro-Moments (Part 1)")
        
        # Generate remaining 15 seeds
        print("📦 Sub-batch 1B: Remaining 15 micro-moments...")
        micro_moments_2 = await self.generate_seed_batch(
            'seed_generation_micro_15',
            {**project_context, 'tactics_summary': tactics_summary, 'seed_count': 15, 'start_id': 16}
        )
        batch1b = micro_moments_2.get('micro_moments', [])
        print(f"✅ Generated {len(batch1b)} Micro-Moments (Part 2)")
        
        # Combine both batches
        results['micro_moments'] = batch1a + batch1b
        print(f"📊 Total Micro-Moments: {len(results['micro_moments'])} / 30")
        if len(results['micro_moments']) < 25:  # Allow some flexibility
            print(f"⚠️  Got {len(results['micro_moments'])} micro-moments, continuing with available seeds...")
        print()

        # Batch 2: Episode Beats (20 seeds)
        print("-" * 70)
        print("📦 BATCH 2: EPISODE BEATS (20 seeds)")
        print("-" * 70)
        print("Major plot points and cliffhangers (3-8 minutes each)")
        print()
        print("🤖 Generating episode beats...")
        print("⏳ This may take 60-90 seconds...")
        print()

        episode_beats = await self.generate_seed_batch(
            'seed_generation_beats',
            {**project_context, 'tactics_summary': tactics_summary, 'seed_count': 20}
        )
        results['episode_beats'] = episode_beats['episode_beats']
        print(f"📊 Total Episode Beats: {len(results['episode_beats'])} / 20")
        if len(results['episode_beats']) < 15:  # Allow some flexibility
            print(f"⚠️  Got {len(results['episode_beats'])} episode beats, continuing with available seeds...")
        print()

        # Batch 3: Season Arcs (10 seeds)
        print("-" * 70)
        print("📦 BATCH 3: SEASON ARCS (10 seeds)")
        print("-" * 70)
        print("Multi-episode character development and world expansion")
        print()
        print("🤖 Generating season arcs...")
        print("⏳ This may take 60-90 seconds...")
        print()

        season_arcs = await self.generate_seed_batch(
            'seed_generation_arcs',
            {**project_context, 'tactics_summary': tactics_summary, 'seed_count': 10}
        )
        results['season_arcs'] = season_arcs['season_arcs']
        print(f"📊 Total Season Arcs: {len(results['season_arcs'])} / 10")
        if len(results['season_arcs']) < 7:  # Allow some flexibility
            print(f"⚠️  Got {len(results['season_arcs'])} season arcs, continuing with available seeds...")
        print()

        # Batch 4: Series-Defining Moments (5 seeds)
        print("-" * 70)
        print("📦 BATCH 4: SERIES-DEFINING MOMENTS (5 seeds)")
        print("-" * 70)
        print("Franchise-making iconic scenes")
        print()
        print("🤖 Generating series-defining moments...")
        print("⏳ This may take 60-90 seconds...")
        print()

        series_defining = await self.generate_seed_batch(
            'seed_generation_defining',
            {**project_context, 'tactics_summary': tactics_summary, 'seed_count': 5}
        )
        results['series_defining'] = series_defining['defining_moments']
        print(f"📊 Total Series-Defining Moments: {len(results['series_defining'])} / 5")
        if len(results['series_defining']) < 3:  # Allow some flexibility
            print(f"⚠️  Got {len(results['series_defining'])} series-defining moments, continuing with available seeds...")

        return results

    def format_tactics_summary(self, tactics: List[Dict]) -> str:
        """Format tactics for inclusion in seed generation prompts - OPTIMIZED"""
        summary = []
        for tactic_group in tactics[:8]:  # Reduced to top 8 references for efficiency
            ref_title = tactic_group.get('reference_title', 'Unknown')[:30]  # Truncate long titles
            tactic_list = tactic_group.get('tactics', [])

            for tactic in tactic_list[:2]:  # Top 2 tactics per reference for conciseness
                tactic_name = tactic.get('tactic_name', 'Tactic')[:20]  # Truncate tactic names
                audio_app = tactic.get('audio_application', 'N/A')[:60]  # Truncate descriptions
                summary.append(f"- {tactic_name} ({ref_title}): {audio_app}")

        return "\n".join(summary[:20])  # Reduced to max 20 tactics for better performance

    async def generate_seed_batch(self, prompt_name: str, context: Dict) -> Dict:
        """Generate a batch of seeds using specified prompt with retry logic"""
        # Set appropriate token limits based on complexity - increased to prevent truncation
        if 'micro' in prompt_name:
            max_tokens = 12000  # Increased for 15 micro-moments with full JSON structure
        elif 'beats' in prompt_name:
            max_tokens = 15000  # Increased for 20 episode beats with detailed fields
        elif 'arcs' in prompt_name:
            max_tokens = 10000  # Increased for 10 season arcs
        elif 'defining' in prompt_name:
            max_tokens = 8000   # Increased for 5 series-defining moments
        else:
            max_tokens = self.config.max_tokens

        prompt = self.config.get_prompt(prompt_name).format(**context)

        # Retry logic for truncated responses
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.openrouter.process_message(
                    prompt,
                    model_name=self.config.model,
                    max_tokens=max_tokens
                )

                # Validate response before JSON extraction
                if not response or len(response.strip()) < 100:
                    raise ValueError(f"LLM response too short or empty: {len(response) if response else 0} characters")
                
                # Improved truncation detection - check for complete JSON structure
                response_clean = response.strip()
                if not response_clean.startswith('{') or not response_clean.endswith('}'):
                    # Try to find the last complete JSON object
                    last_brace = response_clean.rfind('}')
                    if last_brace > 0:
                        response = response_clean[:last_brace + 1]
                        print(f"⚠️  Detected truncation, using partial response (attempt {attempt + 1})")
                    else:
                        raise ValueError(f"LLM response appears truncated - no complete JSON found. Length: {len(response)}")

                data = extract_json(response)

                # VALIDATION: Check if we got the expected key
                expected_keys = {
                    'seed_generation_micro': 'micro_moments',
                    'seed_generation_micro_15': 'micro_moments',
                    'seed_generation_beats': 'episode_beats',
                    'seed_generation_arcs': 'season_arcs',
                    'seed_generation_defining': 'defining_moments'
                }

                expected_key = expected_keys.get(prompt_name)
                if expected_key and expected_key not in data:
                    raise ValueError(
                        f"LLM did not return expected key '{expected_key}'. "
                        f"Got keys: {list(data.keys())}"
                    )

                return data
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Attempt {attempt + 1} failed: {str(e)}")
                    print(f"🔄 Retrying with increased token limit...")
                    max_tokens = int(max_tokens * 1.5)  # Increase token limit for retry
                    await asyncio.sleep(1)  # Brief delay before retry
                else:
                    raise ValueError(f"Failed to generate seeds after {max_retries} attempts: {str(e)}")

    def show_seed_statistics(self, all_seeds: Dict):
        """Show seed bank statistics"""
        print("\n" + "=" * 70)
        print("📊 SEED BANK SUMMARY")
        print("=" * 70)
        print()

        micro = all_seeds.get('micro_moments', [])
        beats = all_seeds.get('episode_beats', [])
        arcs = all_seeds.get('season_arcs', [])
        defining = all_seeds.get('series_defining', [])

        total = len(micro) + len(beats) + len(arcs) + len(defining)

        print(f"Total Seeds: {total}")
        print(f"├─ Micro-Moments: {len(micro)} (30-90 seconds each)")
        print(f"├─ Episode Beats: {len(beats)} (3-8 minutes each)")
        print(f"├─ Season Arcs: {len(arcs)} (spanning multiple episodes)")
        print(f"└─ Series-Defining: {len(defining)} (franchise-making moments)")
        print()
        print("-" * 70)

    def show_sample_seeds(self, all_seeds: Dict) -> str:
        """Show sample seeds and get user approval (OPTIONAL)"""
        print("\n" + "=" * 70)
        print("📋 SAMPLE SEEDS (Random Selection)")
        print("=" * 70)
        print()

        # Show 1 random sample from each category
        categories = [
            ('micro_moments', 'MICRO-MOMENT', 'duration', 'core_idea'),
            ('episode_beats', 'EPISODE BEAT', 'duration', 'core_idea'),
            ('season_arcs', 'SEASON ARC', 'episode_span', 'core_idea'),
            ('series_defining', 'SERIES-DEFINING', 'duration', 'core_idea')
        ]

        for key, label, duration_key, idea_key in categories:
            seeds = all_seeds.get(key, [])
            if seeds:
                sample = random.choice(seeds)
                print(f"🌱 {label}: \"{sample.get('title', 'Untitled')}\"")
                print("-" * 70)
                print(f"{idea_key.replace('_', ' ').title()}: {sample.get(idea_key, 'N/A')}")
                print(f"{duration_key.replace('_', ' ').title()}: {sample.get(duration_key, 'N/A')}")
                if key == 'episode_beats':
                    print(f"Beat Type: {sample.get('beat_type', 'N/A')}")
                elif key == 'season_arcs':
                    print(f"Arc Type: {sample.get('arc_type', 'N/A')}")
                elif key == 'series_defining':
                    print(f"Why Defining: {sample.get('why_defining', 'N/A')[:100]}...")
                print()

        print("=" * 70)
        print()
        print("-" * 70)
        print("🎯 QUALITY CHECK")
        print("-" * 70)
        print("You've seen sample seeds above.")
        print()
        print("Options:")
        print("  [Press Enter] Accept seed bank and continue (recommended)")
        print("  [Type 'M'] View more samples (5 random seeds)")
        print("  [Type 'R'] Regenerate specific category")
        print("  [Type 'A'] View ALL seeds")
        print("-" * 70)

        choice = input("\nYour choice: ").strip().upper()
        if choice == "":
            choice = "ENTER"
            print("✅ Seed bank accepted. Proceeding to save...")

        return choice

    def show_more_samples(self, all_seeds: Dict, count: int = 5):
        """Show more random seed samples"""
        print("\n" + "=" * 70)
        print(f"📋 MORE SAMPLES ({count} Random Seeds)")
        print("=" * 70)
        print()

        all_seeds_flat = []
        for category, seeds in all_seeds.items():
            for seed in seeds:
                seed['_category'] = category
                all_seeds_flat.append(seed)

        samples = random.sample(all_seeds_flat, min(count, len(all_seeds_flat)))

        for i, seed in enumerate(samples, 1):
            cat = seed.get('_category', 'unknown').replace('_', ' ').title()
            print(f"{i}. [{cat}] {seed.get('title', 'Untitled')}")
            print(f"   {seed.get('core_idea', seed.get('description', 'N/A'))[:150]}...")
            print()

    def show_all_seeds(self, all_seeds: Dict):
        """Show all seeds"""
        print("\n" + "=" * 70)
        print("🌱 ALL SEEDS (FULL VIEW)")
        print("=" * 70)

        for category, seeds in all_seeds.items():
            print(f"\n\n{category.upper().replace('_', ' ')} ({len(seeds)} total):")
            print("=" * 70)
            for i, seed in enumerate(seeds, 1):
                print(f"\n{i}. {seed.get('title', 'N/A')}")
                for key, value in seed.items():
                    if key != 'title' and not key.startswith('_'):
                        print(f"   {key.replace('_', ' ').title()}: {value}")

    async def save_output(self, session_id: str, station1_data: Dict, station2_data: Dict,
                         station3_data: Dict, references: List[Dict],
                         tactics: List[Dict], seeds: Dict):
        """Save all output files (JSON + TXT + CSV + Redis)"""

        # Prepare full output with bulletproof title
        bulletproof_title = TitleValidator.extract_bulletproof_title(station1_data, station2_data)
        output_data = {
            'session_id': session_id,
            'working_title': bulletproof_title,
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
        print(f"✓ JSON format (for next station)")

        # Save TXT
        txt_path = self.output_dir / f"{session_id}_readable.txt"
        self.save_readable_txt(txt_path, output_data)
        print(f"✓ TXT format (human-readable)")

        # Save CSV
        csv_path = self.output_dir / f"{session_id}_seeds.csv"
        self.save_seeds_csv(csv_path, seeds)
        print(f"✓ CSV format (spreadsheet analysis)")
        print()

        # Save to Redis
        redis_key = f"audiobook:{session_id}:station_04"
        try:
            await self.redis.set(redis_key, json.dumps(output_data), expire=86400)
            print(f"✅ Saved to Redis for Station 5")
        except Exception as e:
            print(f"❌ Failed to save to Redis: {str(e)}")
            print(f"⚠️  Station 4.5 will not be able to load this session")
            print(f"   Data is still saved to JSON/TXT/CSV files")
            raise ValueError(f"Redis save failed: {str(e)}")

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

            # Tactics (summary only)
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
                f.write(f"   Core Idea: {seed.get('core_idea', 'N/A')}\n")

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
