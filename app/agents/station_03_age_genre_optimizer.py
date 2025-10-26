"""
Station 3: Age & Genre Optimizer Agent - SIMPLIFIED VERSION

This agent:
1. Loads Station 2 Project Bible
2. Auto-generates age-appropriate guidelines
3. Auto-generates 3 genre blend options
4. User chooses genre blend (A/B/C)
5. Auto-generates tone calibration for chosen blend
6. Saves complete style guide to JSON + TXT files
"""

import asyncio
import json
import logging
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json
from app.agents.title_validator import TitleValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class StyleGuide:
    """Complete Style Guide from Station 3"""
    # From Station 2
    working_title: str
    original_seed: str
    seed_type: str
    scale_type: str
    episode_count: str
    episode_length: str
    primary_genre: str
    target_age_range: str
    content_rating: str

    # Generated in Station 3
    age_guidelines: Dict
    genre_options: Dict
    chosen_blend: str  # "A", "B", or "C"
    chosen_blend_details: Dict
    tone_calibration: Dict

    session_id: str
    timestamp: str


class Station03AgeGenreOptimizer:
    """Simplified Station 3: Age & Genre Optimizer"""

    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=3)
        self.output_dir = Path("output/station_03")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 3 initialized")

    async def load_station1_data(self, session_id: str) -> Dict:
        """Load Station 1 output from Redis"""
        key = f"audiobook:{session_id}:station_01"
        data_str = await self.redis.get(key)
        
        if not data_str:
            raise ValueError(f"❌ No Station 1 data found for session {session_id}")
        
        return json.loads(data_str)

    async def load_station2_data(self, session_id: str) -> Dict:
        """Load Station 2 output from Redis"""
        print(f"\n📥 Loading Project Bible from Station 2...")
        print(f"   Session ID: {session_id}")

        key = f"audiobook:{session_id}:station_02"
        data_str = await self.redis.get(key)

        if not data_str:
            raise ValueError(f"❌ No Project Bible found for session {session_id}\n   Please run Station 2 first")

        data = json.loads(data_str)

        # Get title and genre info
        title = data.get('working_title', 'Unknown')
        primary_genre = data.get('genre_tone', {}).get('primary_genre', 'Unknown')
        content_rating = data.get('production_constraints', {}).get('content_rating', 'Unknown')

        print(f'✅ Loaded: "{title}" ({content_rating}, {primary_genre})')
        return data

    def display_project_summary(self, station1_data: Dict, station2_data: Dict):
        """Display project summary from Station 2 with bulletproof title"""
        print("\n" + "="*60)
        print("📋 PROJECT SUMMARY FROM STATION 2")
        print("="*60)

        # Use bulletproof title extraction
        title = TitleValidator.extract_bulletproof_title(station1_data, station2_data)
        print(TitleValidator.format_title_for_display(title, "Station 3"))
        scale_type = station2_data.get('scale_type', 'Unknown')
        episode_count = station2_data.get('episode_count', 'Unknown')
        episode_length = station2_data.get('episode_length', 'Unknown')

        genre_tone = station2_data.get('genre_tone', {})
        primary_genre = genre_tone.get('primary_genre', 'Unknown')

        audience = station2_data.get('audience_profile', {})
        target_age = audience.get('primary_age_range', 'Unknown')

        production = station2_data.get('production_constraints', {})
        content_rating = production.get('content_rating', 'Unknown')

        # Try to get original seed
        original_seed = station2_data.get('original_seed', 'N/A')
        if original_seed and original_seed != 'N/A':
            if len(original_seed) > 80:
                original_seed = original_seed[:80] + "..."
            print(f"\nTitle: {title}")
            print(f"Scale: {scale_type} ({episode_count}, {episode_length})")
            print(f"Primary Genre: {primary_genre}")
            print(f"Target Age: {target_age}")
            print(f"Content Rating: {content_rating}")
            print(f"\nCore Premise: {original_seed}")
        else:
            print(f"\nTitle: {title}")
            print(f"Scale: {scale_type} ({episode_count}, {episode_length})")
            print(f"Primary Genre: {primary_genre}")
            print(f"Target Age: {target_age}")
            print(f"Content Rating: {content_rating}")

        print("-"*60)

    async def generate_age_guidelines(self, station2_data: Dict) -> Dict:
        """Generate age-appropriate content guidelines"""
        print("\n🤖 Analyzing age-appropriate content guidelines...")

        # Extract data for prompt - NO DEFAULTS, must come from Station 2
        try:
            audience = station2_data['audience_profile']
            target_age_range = audience['primary_age_range']

            production = station2_data['production_constraints']
            content_rating = production['content_rating']

            genre_tone = station2_data['genre_tone']
            primary_genre = genre_tone['primary_genre']
            mood_profile = genre_tone['mood_profile']
        except KeyError as e:
            raise ValueError(f"Station 2 did not provide required field: {e}. Cannot proceed with Station 3.")

        print(f"   Target: {target_age_range} years, {content_rating} rating")
        print("   Generating restrictions for:")
        print("   - Violence levels ✓")
        print("   - Emotional intensity ✓")
        print("   - Language guidelines ✓")
        print("   - Sound restrictions ✓")
        print("   - Theme complexity ✓")

        # Build prompt
        prompt = self.config.get_prompt('age_analysis').format(
            target_age_range=target_age_range,
            content_rating=content_rating,
            primary_genre=primary_genre,
            mood_profile=mood_profile
        )

        # Generate with retry
        for attempt in range(3):
            try:
                response = await self.openrouter.process_message(
                    prompt,
                    model_name=self.config.model
                )

                result = extract_json(response)
                print("\n✅ Age guidelines generated")
                return result

            except Exception as e:
                if attempt < 2:
                    logger.warning(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying...")
                    await asyncio.sleep(2)
                else:
                    logger.error(f"❌ Failed after 3 attempts: {e}")
                    raise

    def display_age_guidelines(self, guidelines: Dict):
        """Display age guidelines summary"""
        print("\n" + "-"*60)
        print("📋 AGE-APPROPRIATE CONTENT GUIDELINES")
        print("-"*60)
        print(f"Target Age: {guidelines.get('target_age_range', 'N/A')}")
        print(f"Content Rating: {guidelines.get('content_rating', 'N/A')}")

        violence = guidelines.get('violence_level', 'MODERATE')
        print(f"\nViolence Level: {violence}")

        if 'action_scene_limits' in guidelines:
            for limit in guidelines['action_scene_limits'][:3]:
                print(f"  • {limit}")

        emotional = guidelines.get('emotional_intensity', 'MODERATE')
        print(f"\nEmotional Intensity: {emotional}")

        if 'emotional_boundaries' in guidelines:
            for boundary in guidelines['emotional_boundaries'][:3]:
                print(f"  • {boundary}")

        if 'language_guidelines' in guidelines:
            lang = guidelines['language_guidelines']
            print(f"\nLanguage:")
            if isinstance(lang, dict):
                print(f"  • Vocabulary: {lang.get('vocabulary_level', 'N/A')}")
                print(f"  • Forbidden: {lang.get('forbidden_topics', 'N/A')}")
            else:
                print(f"  • {lang}")

        if 'sound_restrictions' in guidelines:
            print(f"\nSound Design:")
            for restriction in guidelines['sound_restrictions'][:3]:
                print(f"  • {restriction}")

        if 'theme_complexity' in guidelines:
            theme = guidelines['theme_complexity']
            if len(theme) > 80:
                theme = theme[:80] + "..."
            print(f"\nTheme Complexity: {theme}")

        print("-"*60)

    async def generate_genre_blends(self, station2_data: Dict) -> Dict:
        """Generate 3 genre blend options"""
        print("\n🤖 Generating genre blend options...")
        print("   Analyzing: Primary + (complementary genres)")
        print("   Creating 3 distinct audio-optimized blends...")

        # Extract data for prompt - NO DEFAULTS, must come from Station 2
        try:
            genre_tone = station2_data['genre_tone']
            primary_genre = genre_tone['primary_genre']
            secondary_genres = genre_tone['secondary_genres']
            tone_descriptors = genre_tone['tone_descriptors']

            episode_length = station2_data['episode_length']

            audience = station2_data['audience_profile']
            target_age = audience['primary_age_range']
            listening_context = audience['listening_context']
        except KeyError as e:
            raise ValueError(f"Station 2 did not provide required field: {e}. Cannot proceed with Station 3.")

        # Build prompt
        prompt = self.config.get_prompt('genre_blending').format(
            primary_genre=primary_genre,
            secondary_genres=', '.join(secondary_genres) if secondary_genres else 'None specified',
            tone_descriptors=', '.join(tone_descriptors) if tone_descriptors else 'Moderate',
            episode_length=episode_length,
            target_age=target_age,
            listening_context=listening_context
        )

        # Generate with retry
        for attempt in range(3):
            try:
                response = await self.openrouter.process_message(
                    prompt,
                    model_name=self.config.model
                )

                result = extract_json(response)
                print("\n✅ Genre blends generated")
                return result

            except Exception as e:
                if attempt < 2:
                    logger.warning(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying...")
                    await asyncio.sleep(2)
                else:
                    logger.error(f"❌ Failed after 3 attempts: {e}")
                    raise

    def display_genre_options(self, options: Dict) -> tuple[str, Dict]:
        """Display genre blend options and get user choice"""
        print("\n" + "="*60)
        print("🎭 GENRE BLEND OPTIONS")
        print("="*60)

        option_map = {
            'option_a': 'A',
            'option_b': 'B',
            'option_c': 'C'
        }

        for opt_key, letter in option_map.items():
            if opt_key not in options:
                continue

            opt = options[opt_key]

            print(f"\n🔸 OPTION {letter}: {opt.get('primary_genre', 'N/A')} + {opt.get('complementary_genre', 'N/A')}")
            print(f"   Primary: {opt.get('primary_genre', 'N/A')}")
            print(f"   Complementary: {opt.get('complementary_genre', 'N/A')}")

            enhancement = opt.get('enhancement_analysis', 'N/A')
            if len(enhancement) > 200:
                enhancement = enhancement[:200] + "..."
            print(f"\n   Enhancement:")
            print(f"   {enhancement}")

            print(f"\n   Audio Elements:")
            for elem in opt.get('audio_elements', [])[:3]:
                print(f"   • {elem}")

            pacing = opt.get('pacing_implications', 'N/A')
            if len(pacing) > 100:
                pacing = pacing[:100] + "..."
            print(f"\n   Pacing: {pacing}")

            expectations = opt.get('audience_expectations', 'N/A')
            if len(expectations) > 100:
                expectations = expectations[:100] + "..."
            print(f"   Audience Expects: {expectations}")

            print("\n" + "-"*60)

        print("\n" + "="*60)

        # Get user choice
        while True:
            choice = input("\n🎯 Which genre blend best fits your vision?\n   Enter A, B, or C (or press Enter for Option A): ").strip().upper()

            if choice == "":
                choice = "A"
                print("✅ Using default: Option A")
                break
            elif choice in ['A', 'B', 'C']:
                break
            else:
                print("❌ Please enter A, B, or C (or press Enter for default)")

        # Map choice to option key
        choice_to_key = {'A': 'option_a', 'B': 'option_b', 'C': 'option_c'}
        chosen_details = options[choice_to_key[choice]]

        print(f"\n✅ You selected: OPTION {choice} ({chosen_details.get('primary_genre', 'N/A')} + {chosen_details.get('complementary_genre', 'N/A')})")
        return choice, chosen_details

    async def generate_tone_calibration(self, station2_data: Dict, chosen_blend: Dict) -> Dict:
        """Generate tone calibration for chosen blend"""
        print("\n🤖 Calibrating tone progression for chosen blend...")
        print("   - Episode-by-episode tone mapping")
        print("   - Identifying tonal shift moments")
        print("   - Audio conveyance strategies")
        print("   - Light/dark balance")

        # Extract data for prompt - NO DEFAULTS, must come from Station 2 and chosen blend
        try:
            episode_count = station2_data['episode_count']
            episode_length = station2_data['episode_length']

            genre_tone = station2_data['genre_tone']
            mood_profile = genre_tone['mood_profile']

            chosen_blend_primary = chosen_blend['primary_genre']
            chosen_blend_complementary = chosen_blend['complementary_genre']
            enhancement_analysis = chosen_blend['enhancement_analysis']
        except KeyError as e:
            raise ValueError(f"Required field missing: {e}. Cannot proceed with tone calibration.")

        # Build prompt
        prompt = self.config.get_prompt('tone_calibration').format(
            episode_count=episode_count,
            episode_length=episode_length,
            mood_profile=mood_profile,
            chosen_blend_primary=chosen_blend_primary,
            chosen_blend_complementary=chosen_blend_complementary,
            enhancement_analysis=enhancement_analysis
        )

        # Generate with retry
        for attempt in range(3):
            try:
                response = await self.openrouter.process_message(
                    prompt,
                    model_name=self.config.model
                )

                result = extract_json(response)
                print("\n✅ Tone calibration complete")
                return result

            except Exception as e:
                if attempt < 2:
                    logger.warning(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying...")
                    await asyncio.sleep(2)
                else:
                    logger.error(f"❌ Failed after 3 attempts: {e}")
                    raise

    def display_style_guide_summary(self, tone_cal: Dict, chosen_blend: Dict):
        """Display complete style guide summary"""
        print("\n" + "="*60)
        print("📖 AGE/GENRE STYLE GUIDE COMPLETE")
        print("="*60)

        blend_name = f"{chosen_blend.get('primary_genre', 'N/A')} + {chosen_blend.get('complementary_genre', 'N/A')}"
        print(f"\nChosen Blend: {blend_name}")

        print("\nTONE PROGRESSION:")
        print("-"*60)
        for progression in tone_cal.get('episode_progression', []):
            print(f"{progression}")

        print("\nTONAL SHIFT MOMENTS:")
        for i, moment in enumerate(tone_cal.get('tonal_shift_moments', []), 1):
            print(f"  {i}. {moment}")

        print("\nAUDIO TONE TECHNIQUES:")
        for technique in tone_cal.get('audio_tone_techniques', [])[:5]:
            print(f"  • {technique}")

        light_dark = tone_cal.get('light_dark_balance', 'Balanced approach')
        if len(light_dark) > 200:
            light_dark = light_dark[:200] + "..."
        print(f"\nLIGHT/DARK BALANCE:")
        print(f"  {light_dark}")

        print("\n" + "-"*60)
        print("✅ Style Guide Complete")
        print("="*60)

    def save_output(self, style_guide: StyleGuide):
        """Save style guide to JSON and text files"""
        session_id = style_guide.session_id

        # Save as JSON
        json_path = self.output_dir / f"{session_id}_style_guide.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'working_title': style_guide.working_title,
                'original_seed': style_guide.original_seed,
                'seed_type': style_guide.seed_type,
                'scale_type': style_guide.scale_type,
                'episode_count': style_guide.episode_count,
                'episode_length': style_guide.episode_length,
                'primary_genre': style_guide.primary_genre,
                'target_age_range': style_guide.target_age_range,
                'content_rating': style_guide.content_rating,
                'age_guidelines': style_guide.age_guidelines,
                'genre_options': style_guide.genre_options,
                'chosen_blend': style_guide.chosen_blend,
                'chosen_blend_details': style_guide.chosen_blend_details,
                'tone_calibration': style_guide.tone_calibration,
                'session_id': style_guide.session_id,
                'timestamp': style_guide.timestamp
            }, f, indent=2, ensure_ascii=False)

        # Save as readable text
        txt_path = self.output_dir / f"{session_id}_style_guide.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("AGE/GENRE STYLE GUIDE\n")
            f.write("="*60 + "\n\n")

            f.write(f"PROJECT TITLE: {style_guide.working_title}\n")
            f.write(f"Session ID: {style_guide.session_id}\n")
            f.write(f"Created: {style_guide.timestamp}\n")
            f.write(f"Input Type: {style_guide.seed_type}\n\n")

            f.write(f"Scale: {style_guide.scale_type}\n")
            f.write(f"Episodes: {style_guide.episode_count}\n")
            f.write(f"Length: {style_guide.episode_length}\n")
            f.write(f"Primary Genre: {style_guide.primary_genre}\n")
            f.write(f"Target Age: {style_guide.target_age_range}\n")
            f.write(f"Content Rating: {style_guide.content_rating}\n\n")

            f.write("-"*60 + "\n")
            f.write("ORIGINAL SEED:\n")
            f.write("-"*60 + "\n")
            f.write(f"{style_guide.original_seed}\n\n")

            f.write("-"*60 + "\n")
            f.write("1. AGE-APPROPRIATE GUIDELINES\n")
            f.write("-"*60 + "\n")
            ag = style_guide.age_guidelines
            f.write(f"Target Age: {ag.get('target_age_range', 'N/A')}\n")
            f.write(f"Content Rating: {ag.get('content_rating', 'N/A')}\n")
            f.write(f"Violence Level: {ag.get('violence_level', 'N/A')}\n")
            f.write(f"Emotional Intensity: {ag.get('emotional_intensity', 'N/A')}\n\n")

            if 'action_scene_limits' in ag:
                f.write("Action Scene Limits:\n")
                for limit in ag['action_scene_limits']:
                    f.write(f"  • {limit}\n")
                f.write("\n")

            if 'emotional_boundaries' in ag:
                f.write("Emotional Boundaries:\n")
                for boundary in ag['emotional_boundaries']:
                    f.write(f"  • {boundary}\n")
                f.write("\n")

            if 'sound_restrictions' in ag:
                f.write("Sound Restrictions:\n")
                for restriction in ag['sound_restrictions']:
                    f.write(f"  • {restriction}\n")
                f.write("\n")

            f.write("-"*60 + "\n")
            f.write("2. GENRE BLEND OPTIONS\n")
            f.write("-"*60 + "\n")
            for opt_key in ['option_a', 'option_b', 'option_c']:
                if opt_key in style_guide.genre_options:
                    opt = style_guide.genre_options[opt_key]
                    letter = opt_key.split('_')[1].upper()
                    marker = "✓" if letter == style_guide.chosen_blend else " "
                    f.write(f"\n[{marker}] OPTION {letter}: {opt.get('primary_genre', 'N/A')} + {opt.get('complementary_genre', 'N/A')}\n")
                    f.write(f"    Enhancement: {opt.get('enhancement_analysis', 'N/A')}\n")

            f.write(f"\nCHOSEN: Option {style_guide.chosen_blend}\n\n")

            f.write("-"*60 + "\n")
            f.write("3. TONE CALIBRATION\n")
            f.write("-"*60 + "\n")
            tc = style_guide.tone_calibration

            blend_name = f"{style_guide.chosen_blend_details.get('primary_genre', 'N/A')} + {style_guide.chosen_blend_details.get('complementary_genre', 'N/A')}"
            f.write(f"Chosen Blend: {blend_name}\n\n")

            if 'episode_progression' in tc:
                f.write("Episode Progression:\n")
                for prog in tc['episode_progression']:
                    f.write(f"  • {prog}\n")
                f.write("\n")

            if 'tonal_shift_moments' in tc:
                f.write("Tonal Shift Moments:\n")
                for i, moment in enumerate(tc['tonal_shift_moments'], 1):
                    f.write(f"  {i}. {moment}\n")
                f.write("\n")

            if 'audio_tone_techniques' in tc:
                f.write("Audio Tone Techniques:\n")
                for technique in tc['audio_tone_techniques']:
                    f.write(f"  • {technique}\n")
                f.write("\n")

            if 'light_dark_balance' in tc:
                f.write(f"Light/Dark Balance:\n  {tc['light_dark_balance']}\n\n")

        print(f"\n💾 Saving Age/Genre Style Guide...\n")
        print(f"✅ Saved to:")
        print(f"   📄 {json_path}")
        print(f"   📄 {txt_path}")
        print(f"\n✅ Stored in Redis for Station 4")

    async def process(self, session_id: str) -> StyleGuide:
        """Main processing method"""
        try:
            print("\n" + "="*60)
            print("🎬 STATION 3: AGE & GENRE OPTIMIZER")
            print("="*60)

            # Load Station 1 and Station 2 data for bulletproof title handling
            station1_data = await self.load_station1_data(session_id)
            station2_data = await self.load_station2_data(session_id)
            self.display_project_summary(station1_data, station2_data)

            # Step 1: Generate age guidelines (auto)
            age_guidelines = await self.generate_age_guidelines(station2_data)
            self.display_age_guidelines(age_guidelines)

            # Step 2: Generate genre blends (auto)
            genre_options = await self.generate_genre_blends(station2_data)

            # Step 3: User chooses blend (HUMAN INTERACTION)
            chosen_blend_letter, chosen_blend_details = self.display_genre_options(genre_options)

            # Step 4: Generate tone calibration (auto)
            tone_calibration = await self.generate_tone_calibration(station2_data, chosen_blend_details)

            # Step 5: Display complete style guide
            self.display_style_guide_summary(tone_calibration, chosen_blend_details)

            # Create style guide object
            audience = station2_data.get('audience_profile', {})
            production = station2_data.get('production_constraints', {})
            genre_tone = station2_data.get('genre_tone', {})

            style_guide = StyleGuide(
                working_title=TitleValidator.extract_bulletproof_title(station1_data, station2_data),
                original_seed=station2_data.get('original_seed', 'N/A'),
                seed_type=station2_data.get('seed_type', 'N/A'),
                scale_type=station2_data.get('scale_type', 'Unknown'),
                episode_count=station2_data.get('episode_count', 'Unknown'),
                episode_length=station2_data.get('episode_length', 'Unknown'),
                primary_genre=genre_tone.get('primary_genre', 'Unknown'),
                target_age_range=audience.get('primary_age_range', 'Unknown'),
                content_rating=production.get('content_rating', 'Unknown'),
                age_guidelines=age_guidelines,
                genre_options=genre_options,
                chosen_blend=chosen_blend_letter,
                chosen_blend_details=chosen_blend_details,
                tone_calibration=tone_calibration,
                session_id=session_id,
                timestamp=datetime.now().isoformat()
            )

            # Save output
            self.save_output(style_guide)

            # Store in Redis for Station 4
            await self.redis.set(
                f"audiobook:{session_id}:station_03",
                json.dumps({
                    'working_title': style_guide.working_title,
                    'seed_type': style_guide.seed_type,
                    'scale_type': style_guide.scale_type,
                    'episode_count': style_guide.episode_count,
                    'chosen_blend': style_guide.chosen_blend,
                    'chosen_blend_details': style_guide.chosen_blend_details,
                    'age_guidelines': style_guide.age_guidelines,
                    'tone_calibration': style_guide.tone_calibration
                }),
                expire=86400
            )

            print("\n" + "="*60)
            print("✅ STATION 3 COMPLETE!")
            print("="*60)
            print(f"\nProject: {style_guide.working_title}")
            blend_name = f"{chosen_blend_details.get('primary_genre', 'N/A')} + {chosen_blend_details.get('complementary_genre', 'N/A')}"
            print(f"Genre Blend: {blend_name}")
            print(f"Age Guidelines: {style_guide.content_rating} ({style_guide.target_age_range} years)")
            print(f"Session ID: {session_id}")

            print("\n📋 Style Guide includes:")
            print("   ✓ Age-appropriate content guidelines")
            print(f"   ✓ Genre blend strategy ({blend_name})")
            print(f"   ✓ Tone calibration for {style_guide.episode_count}")
            print("   ✓ Audio-specific techniques")
            print("   ✓ Light/dark balance strategy")

            print("\n📌 Ready to proceed to Station 4: Reference Mining & Seed Extraction")
            print("\n" + "="*60)

            return style_guide

        except Exception as e:
            logger.error(f"❌ Station 3 failed: {str(e)}")
            raise


# CLI Entry Point
async def main():
    """Run Station 3 standalone"""
    optimizer = Station03AgeGenreOptimizer()
    await optimizer.initialize()

    session_id = input("\n👉 Enter Session ID from Station 2: ").strip()

    if not session_id:
        print("❌ Session ID required")
        return

    try:
        style_guide = await optimizer.process(session_id)
        print(f"\n✅ Success! Style Guide created for: {style_guide.working_title}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
