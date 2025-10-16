"""
Station 2: Project DNA Builder Agent - SIMPLIFIED VERSION

Takes Station 1 output and creates comprehensive Project Bible with 7 sections:
1. World & Setting
2. Format Specifications
3. Genre & Tone
4. Creative Promises
5. Audience Profile
6. Production Constraints
7. Creative Team
"""

import asyncio
import json
import logging
from typing import Dict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProjectBible:
    """Complete Project Bible from Station 2"""
    # From Station 1
    working_title: str
    original_seed: str
    seed_type: str
    scale_type: str
    episode_count: str
    episode_length: str

    # Generated in Station 2
    world_setting: Dict
    format_specifications: Dict
    genre_tone: Dict
    creative_promises: Dict
    audience_profile: Dict
    production_constraints: Dict
    creative_team: Dict

    session_id: str
    timestamp: str


class Station02ProjectDNABuilder:
    """Simplified Station 2: Project DNA Builder"""

    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=2)
        self.output_dir = Path("output/station_02")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 2 initialized")

    async def load_station1_data(self, session_id: str) -> Dict:
        """Load Station 1 output from Redis"""
        print(f"\n📥 Loading Station 1 data for session: {session_id}")

        key = f"audiobook:{session_id}:station_01"
        data_str = await self.redis.get(key)

        if not data_str:
            raise ValueError(f"❌ No Station 1 data found for session {session_id}")

        data = json.loads(data_str)
        print(f"✅ Loaded Station 1 data: {data.get('chosen_title', 'Unknown')}")
        return data

    def display_station1_summary(self, station1_data: Dict):
        """Display Station 1 data summary"""
        print("\n" + "="*60)
        print("📋 STATION 1 OUTPUT SUMMARY")
        print("="*60)
        print(f"\nTitle: {station1_data['chosen_title']}")
        print(f"Scale: {station1_data['option_details']['type']}")
        print(f"Episodes: {station1_data['option_details']['episode_count']}")
        print(f"Length: {station1_data['option_details']['episode_length']}")
        print(f"\nCore Premise: {station1_data['core_premise'][:100]}...")
        print("\n" + "-"*60)

    def _build_context(self, station1_data: Dict) -> str:
        """Build context string for prompts"""
        return f"""
TITLE: {station1_data['chosen_title']}
ORIGINAL SEED: {station1_data['original_seed']}

SCALE: {station1_data['option_details']['type']}
EPISODES: {station1_data['option_details']['episode_count']}
LENGTH: {station1_data['option_details']['episode_length']}
WORD COUNT: {station1_data['option_details']['word_count']}

CORE PREMISE: {station1_data['core_premise']}
CENTRAL CONFLICT: {station1_data['central_conflict']}
EPISODE RATIONALE: {station1_data['episode_rationale']}

MAIN CHARACTERS: {', '.join(station1_data['main_characters'])}
"""

    async def generate_world_setting(self, station1_data: Dict) -> Dict:
        """Generate world & setting section"""
        print("\n🌍 Generating World & Setting...")

        context = self._build_context(station1_data)

        prompt = self.config.get_prompt('world').format(context=context)

        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model
        )

        result = extract_json(response)
        print("   ✅ World & Setting complete")
        return result

    async def generate_format_specifications(self, station1_data: Dict) -> Dict:
        """Generate format specifications section"""
        print("📐 Generating Format Specifications...")

        context = self._build_context(station1_data)

        prompt = self.config.get_prompt('format').format(context=context)

        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model
        )

        result = extract_json(response)
        print("   ✅ Format Specifications complete")
        return result

    async def generate_genre_tone(self, station1_data: Dict) -> Dict:
        """Generate genre & tone section"""
        print("🎭 Generating Genre & Tone...")

        context = self._build_context(station1_data)

        prompt = self.config.get_prompt('genre').format(context=context)

        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model
        )

        result = extract_json(response)
        print("   ✅ Genre & Tone complete")
        return result

    async def generate_creative_promises(self, station1_data: Dict) -> Dict:
        """Generate creative promises section"""
        print("✨ Generating Creative Promises...")

        context = self._build_context(station1_data)

        prompt = f"""Generate creative promises for this audio drama.

PROJECT CONTEXT:
{context}

Return ONLY valid JSON:

```json
{{
  "must_have_elements": [
    "Element 1",
    "Element 2",
    "Element 3"
  ],
  "must_avoid_elements": [
    "Avoid 1",
    "Avoid 2",
    "Avoid 3"
  ],
  "unique_selling_points": [
    "USP 1",
    "USP 2",
    "USP 3"
  ]
}}
```"""

        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model
        )

        result = extract_json(response)
        print("   ✅ Creative Promises complete")
        return result

    async def generate_audience_profile(self, station1_data: Dict) -> Dict:
        """Generate audience profile section"""
        print("👥 Generating Audience Profile...")

        context = self._build_context(station1_data)

        prompt = self.config.get_prompt('audience').format(context=context)

        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model
        )

        result = extract_json(response)
        print("   ✅ Audience Profile complete")
        return result

    async def generate_production_constraints(self, station1_data: Dict) -> Dict:
        """Generate production constraints section"""
        print("🎬 Generating Production Constraints...")

        context = self._build_context(station1_data)

        prompt = self.config.get_prompt('production').format(context=context)

        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model
        )

        result = extract_json(response)
        print("   ✅ Production Constraints complete")
        return result

    async def generate_creative_team(self, station1_data: Dict) -> Dict:
        """Generate creative team section"""
        print("🎯 Generating Creative Team Structure...")

        context = self._build_context(station1_data)

        prompt = self.config.get_prompt('creative').format(context=context)

        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model
        )

        result = extract_json(response)
        print("   ✅ Creative Team complete")
        return result

    def save_output(self, bible: ProjectBible):
        """Save Project Bible to JSON and text files"""
        session_id = bible.session_id

        # Save as JSON
        json_path = self.output_dir / f"{session_id}_bible.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'working_title': bible.working_title,
                'original_seed': bible.original_seed,
                'seed_type': bible.seed_type,
                'scale_type': bible.scale_type,
                'episode_count': bible.episode_count,
                'episode_length': bible.episode_length,
                'world_setting': bible.world_setting,
                'format_specifications': bible.format_specifications,
                'genre_tone': bible.genre_tone,
                'creative_promises': bible.creative_promises,
                'audience_profile': bible.audience_profile,
                'production_constraints': bible.production_constraints,
                'creative_team': bible.creative_team,
                'session_id': bible.session_id,
                'timestamp': bible.timestamp
            }, f, indent=2, ensure_ascii=False)

        # Save as readable text
        txt_path = self.output_dir / f"{session_id}_bible.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("PROJECT BIBLE\n")
            f.write("="*60 + "\n\n")

            f.write(f"PROJECT TITLE: {bible.working_title}\n")
            f.write(f"Session ID: {bible.session_id}\n")
            f.write(f"Created: {bible.timestamp}\n")
            f.write(f"Input Type: {bible.seed_type}\n\n")

            f.write(f"Scale: {bible.scale_type}\n")
            f.write(f"Episodes: {bible.episode_count}\n")
            f.write(f"Length: {bible.episode_length}\n\n")

            f.write("-"*60 + "\n")
            f.write("ORIGINAL SEED:\n")
            f.write("-"*60 + "\n")
            f.write(f"{bible.original_seed}\n\n")

            f.write("-"*60 + "\n")
            f.write("1. WORLD & SETTING\n")
            f.write("-"*60 + "\n")
            ws = bible.world_setting
            f.write(f"Time Period: {ws['time_period']}\n")
            f.write(f"Primary Location: {ws['primary_location']}\n")
            f.write(f"Setting Type: {ws['setting_type']}\n")
            f.write(f"Atmosphere: {ws['atmosphere']}\n")
            f.write(f"Historical Context: {ws['historical_context']}\n\n")
            f.write("Key Locations:\n")
            for loc in ws['key_locations']:
                f.write(f"  • {loc}\n")
            f.write("\nCultural Elements:\n")
            for elem in ws['cultural_elements']:
                f.write(f"  • {elem}\n")
            f.write("\n")

            f.write("-"*60 + "\n")
            f.write("2. FORMAT SPECIFICATIONS\n")
            f.write("-"*60 + "\n")
            fs = bible.format_specifications
            f.write(f"Series Type: {fs['series_type']}\n")
            f.write(f"Episode Count: {fs['episode_count']}\n")
            f.write(f"Episode Length: {fs['episode_length']}\n")
            f.write(f"Season Structure: {fs['season_structure']}\n")
            f.write(f"Pacing Strategy: {fs['pacing_strategy']}\n")
            f.write(f"Narrative Structure: {fs['narrative_structure']}\n\n")

            f.write("-"*60 + "\n")
            f.write("3. GENRE & TONE\n")
            f.write("-"*60 + "\n")
            gt = bible.genre_tone
            f.write(f"Primary Genre: {gt['primary_genre']}\n")
            f.write(f"Secondary Genres: {', '.join(gt['secondary_genres'])}\n")
            f.write(f"Tone: {', '.join(gt['tone_descriptors'])}\n")
            f.write(f"Mood Profile: {gt['mood_profile']}\n")
            f.write("\nGenre Conventions:\n")
            for conv in gt['genre_conventions']:
                f.write(f"  • {conv}\n")
            f.write("\n")

            f.write("-"*60 + "\n")
            f.write("4. CREATIVE PROMISES\n")
            f.write("-"*60 + "\n")
            cp = bible.creative_promises
            f.write("Must-Have Elements:\n")
            for elem in cp['must_have_elements']:
                f.write(f"  ✓ {elem}\n")
            f.write("\nMust-Avoid Elements:\n")
            for elem in cp['must_avoid_elements']:
                f.write(f"  ✗ {elem}\n")
            f.write("\nUnique Selling Points:\n")
            for usp in cp['unique_selling_points']:
                f.write(f"  ★ {usp}\n")
            f.write("\n")

            f.write("-"*60 + "\n")
            f.write("5. AUDIENCE PROFILE\n")
            f.write("-"*60 + "\n")
            ap = bible.audience_profile
            f.write(f"Age Range: {ap['primary_age_range']}\n")
            f.write(f"Demographics: {', '.join(ap['target_demographics'])}\n")
            f.write(f"Listening Context: {ap['listening_context']}\n")
            f.write("\nCore Interests:\n")
            for interest in ap['core_interests']:
                f.write(f"  • {interest}\n")
            f.write("\nContent Preferences:\n")
            for pref in ap['content_preferences']:
                f.write(f"  • {pref}\n")
            if 'emotional_goals' in ap:
                f.write("\nEmotional Goals:\n")
                for goal in ap['emotional_goals']:
                    f.write(f"  • {goal}\n")
            f.write("\n")

            f.write("-"*60 + "\n")
            f.write("6. PRODUCTION CONSTRAINTS\n")
            f.write("-"*60 + "\n")
            pc = bible.production_constraints
            f.write(f"Content Rating: {pc['content_rating']}\n")
            f.write(f"Budget Tier: {pc['budget_tier']}\n")
            f.write("\nTechnical Requirements:\n")
            for req in pc['technical_requirements']:
                f.write(f"  • {req}\n")
            f.write("\nContent Restrictions:\n")
            for rest in pc['content_restrictions']:
                f.write(f"  • {rest}\n")
            if 'distribution_channels' in pc:
                f.write("\nDistribution Channels:\n")
                for chan in pc['distribution_channels']:
                    f.write(f"  • {chan}\n")
            f.write("\n")

            f.write("-"*60 + "\n")
            f.write("7. CREATIVE TEAM\n")
            f.write("-"*60 + "\n")
            ct = bible.creative_team
            f.write(f"Team Structure: {ct['team_structure']}\n")
            f.write(f"Collaboration Style: {ct['collaboration_style']}\n")
            f.write("\nRequired Roles:\n")
            for role in ct['required_roles']:
                f.write(f"  • {role}\n")
            f.write("\nSpecialized Skills:\n")
            for skill in ct['specialized_skills']:
                f.write(f"  • {skill}\n")
            if 'key_decision_makers' in ct:
                f.write("\nKey Decision Makers:\n")
                for dm in ct['key_decision_makers']:
                    f.write(f"  • {dm}\n")
            if 'key_partnerships' in ct:
                f.write("\nKey Partnerships:\n")
                for kp in ct['key_partnerships']:
                    f.write(f"  • {kp}\n")
            f.write("\n")

        print(f"\n✅ Project Bible saved to:")
        print(f"   📄 {json_path}")
        print(f"   📄 {txt_path}")

    async def process(self, session_id: str) -> ProjectBible:
        """Main processing method"""
        try:
            print("\n" + "="*60)
            print("🎬 STATION 2: PROJECT DNA BUILDER")
            print("="*60)

            # Load Station 1 data
            station1_data = await self.load_station1_data(session_id)
            self.display_station1_summary(station1_data)

            # Generate all sections
            print("\n🤖 Generating Project Bible sections...")
            print("⏳ This will take a few moments...\n")

            world_setting = await self.generate_world_setting(station1_data)
            format_specs = await self.generate_format_specifications(station1_data)
            genre_tone = await self.generate_genre_tone(station1_data)
            creative_promises = await self.generate_creative_promises(station1_data)
            audience_profile = await self.generate_audience_profile(station1_data)
            production_constraints = await self.generate_production_constraints(station1_data)
            creative_team = await self.generate_creative_team(station1_data)

            # Create Project Bible
            bible = ProjectBible(
                working_title=station1_data['chosen_title'],
                original_seed=station1_data['original_seed'],
                seed_type=station1_data['seed_type'],
                scale_type=station1_data['option_details']['type'],
                episode_count=station1_data['option_details']['episode_count'],
                episode_length=station1_data['option_details']['episode_length'],
                world_setting=world_setting,
                format_specifications=format_specs,
                genre_tone=genre_tone,
                creative_promises=creative_promises,
                audience_profile=audience_profile,
                production_constraints=production_constraints,
                creative_team=creative_team,
                session_id=session_id,
                timestamp=datetime.now().isoformat()
            )

            # Save output
            self.save_output(bible)

            # Store in Redis for Station 3
            await self.redis.set(
                f"audiobook:{session_id}:station_02",
                json.dumps({
                    'working_title': bible.working_title,
                    'original_seed': bible.original_seed,
                    'seed_type': bible.seed_type,
                    'scale_type': bible.scale_type,
                    'episode_count': bible.episode_count,
                    'episode_length': bible.episode_length,
                    'world_setting': bible.world_setting,
                    'format_specifications': bible.format_specifications,
                    'genre_tone': bible.genre_tone,
                    'creative_promises': bible.creative_promises,
                    'audience_profile': bible.audience_profile,
                    'production_constraints': bible.production_constraints,
                    'creative_team': bible.creative_team
                }),
                expire=86400
            )

            print("\n" + "="*60)
            print("✅ STATION 2 COMPLETE!")
            print("="*60)
            print(f"\nProject Bible created for: {bible.working_title}")
            print(f"Session ID: {session_id}")
            print("\n📌 Ready to proceed to Station 3: Age & Genre Optimizer")

            return bible

        except Exception as e:
            logger.error(f"❌ Station 2 failed: {str(e)}")
            raise


# CLI Entry Point
async def main():
    """Run Station 2 standalone"""
    builder = Station02ProjectDNABuilder()
    await builder.initialize()

    session_id = input("\n👉 Enter Session ID from Station 1: ").strip()

    if not session_id:
        print("❌ Session ID required")
        return

    try:
        bible = await builder.process(session_id)
        print(f"\n✅ Success! Project Bible created for: {bible.working_title}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
