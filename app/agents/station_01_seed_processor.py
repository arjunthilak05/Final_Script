"""
Station 1: Seed Processor & Scale Evaluator Agent - SIMPLIFIED VERSION

This agent:
1. Asks user for seed type (one-liner/synopsis/script/idea)
2. Takes user's story concept
3. Generates 3 scale options (Mini/Standard/Extended)
4. User chooses scale (A/B/C)
5. Generates 3 working titles
6. User chooses title (1/2/3)
7. Generates initial expansion
8. Saves everything to JSON + TXT files
"""

import asyncio
import json
import logging
from typing import Dict, List
from datetime import datetime
from pathlib import Path

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Station01SeedProcessor:
    """Simplified Station 1: Seed Processor & Scale Evaluator"""

    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=1)
        self.output_dir = Path("output/station_01")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 1 initialized")

    def get_user_seed_input(self) -> tuple[str, str]:
        """Get seed input from user with type selection"""
        print("\n" + "="*60)
        print("🎬 STATION 1: SEED PROCESSOR & SCALE EVALUATOR")
        print("="*60)
        print("\n📝 Welcome! Let's start with your story concept.")
        print("\nYou can provide ONE of the following:\n")
        print("  1. A one-liner concept (single sentence)")
        print("  2. A synopsis (any length)")
        print("  3. A public domain script")
        print("  4. A small idea/theme")
        print("\n" + "-"*60)

        # Get input type
        while True:
            choice = input("\n👉 Which type are you providing? (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                break
            print("❌ Please enter 1, 2, 3, or 4")

        seed_types = {
            '1': 'one-liner',
            '2': 'synopsis',
            '3': 'script',
            '4': 'idea'
        }
        seed_type = seed_types[choice]

        print(f"\n✅ You selected: {seed_type}")
        print("\n📝 Now, please enter your content:")
        print("(For multi-line input, press Enter twice when done)\n")

        # Get multi-line input
        lines = []
        empty_count = 0
        while True:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)

        seed_content = "\n".join(lines).strip()

        if not seed_content or len(seed_content) < 10:
            raise ValueError("❌ Seed content must be at least 10 characters")

        print(f"\n✅ Received {len(seed_content)} characters")
        return seed_content, seed_type

    async def generate_scale_options(self, seed: str, seed_type: str) -> Dict:
        """Generate 3 scale options from LLM"""
        print("\n🤖 Analyzing your concept and generating scale options...")
        print("⏳ This may take a moment...\n")

        # Use the prompt from config
        prompt = self.config.get_prompt('main').format(seed_input=seed)

        # Try generating with retry
        for attempt in range(2):
            try:
                response = await self.openrouter.generate(
                    prompt,
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature
                )

                # Parse JSON
                data = extract_json(response)

                # Validate structure
                required_keys = ['option_a', 'option_b', 'option_c', 'recommended_option', 'initial_expansion']
                if all(key in data for key in required_keys):
                    print("✅ Scale options generated successfully")
                    return data
                else:
                    raise ValueError(f"Missing required keys: {[k for k in required_keys if k not in data]}")

            except Exception as e:
                if attempt == 0:
                    logger.warning(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying...")
                    await asyncio.sleep(2)
                else:
                    logger.error(f"❌ Failed after 2 attempts: {e}")
                    raise

    def display_options_and_get_choice(self, options: Dict) -> tuple[str, Dict]:
        """Display scale options to user and get their choice"""
        print("\n" + "="*60)
        print("📊 SCALE OPTIONS FOR YOUR STORY")
        print("="*60)

        option_map = {
            'option_a': 'A',
            'option_b': 'B',
            'option_c': 'C'
        }

        for opt_key, letter in option_map.items():
            opt = options[opt_key]

            print(f"\n🔸 OPTION {letter}: {opt['type']} SERIES")
            print(f"   Episodes: {opt['episode_count']}")
            print(f"   Length: {opt['episode_length']}")
            print(f"   Word Count: {opt['word_count']}")
            print(f"   Best For: {opt['best_for']}")
            print(f"   Why: {opt['justification']}")

        print("\n" + "-"*60)
        print(f"💡 AI Recommends: Option {options['recommended_option']}")
        print("-"*60)

        # Get user choice
        while True:
            choice = input("\n👉 Which option do you choose? (A/B/C): ").strip().upper()
            if choice in ['A', 'B', 'C']:
                break
            print("❌ Please enter A, B, or C")

        # Map choice to option key
        choice_to_key = {'A': 'option_a', 'B': 'option_b', 'C': 'option_c'}
        option_details = options[choice_to_key[choice]]

        print(f"\n✅ You selected Option {choice}: {option_details['type']}")
        return choice, option_details

    def display_titles_and_get_choice(self, titles: List[str]) -> str:
        """Display working titles and get user choice"""
        print("\n" + "="*60)
        print("📝 WORKING TITLE OPTIONS")
        print("="*60)

        for i, title in enumerate(titles, 1):
            print(f"\n  {i}. {title}")

        print("\n" + "-"*60)

        while True:
            choice = input("\n👉 Which title do you prefer? (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                idx = int(choice) - 1
                chosen_title = titles[idx]
                print(f"\n✅ You selected: {chosen_title}")
                return chosen_title
            print("❌ Please enter 1, 2, or 3")

    def save_output(self, output_data: Dict):
        """Save output to both JSON and readable text file"""
        session_id = output_data['session_id']

        # Save as JSON for next station
        json_path = self.output_dir / f"{session_id}_output.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        # Save as readable text
        txt_path = self.output_dir / f"{session_id}_readable.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("STATION 1: SEED PROCESSOR OUTPUT\n")
            f.write("="*60 + "\n\n")

            f.write(f"Session ID: {output_data['session_id']}\n")
            f.write(f"Timestamp: {output_data['timestamp']}\n")
            f.write(f"Input Type: {output_data['seed_type']}\n\n")

            f.write("-"*60 + "\n")
            f.write("ORIGINAL SEED:\n")
            f.write("-"*60 + "\n")
            f.write(f"{output_data['original_seed']}\n\n")

            f.write("-"*60 + "\n")
            f.write(f"CHOSEN SCALE: OPTION {output_data['chosen_option']}\n")
            f.write("-"*60 + "\n")
            opt = output_data['option_details']
            f.write(f"Type: {opt['type']}\n")
            f.write(f"Episodes: {opt['episode_count']}\n")
            f.write(f"Length: {opt['episode_length']}\n")
            f.write(f"Word Count: {opt['word_count']}\n")
            f.write(f"Best For: {opt['best_for']}\n")
            f.write(f"Justification: {opt['justification']}\n\n")

            f.write("-"*60 + "\n")
            f.write("WORKING TITLES:\n")
            f.write("-"*60 + "\n")
            for i, title in enumerate(output_data['working_titles'], 1):
                marker = "✓" if title == output_data['chosen_title'] else " "
                f.write(f"  [{marker}] {i}. {title}\n")
            f.write(f"\nCHOSEN: {output_data['chosen_title']}\n\n")

            f.write("-"*60 + "\n")
            f.write("INITIAL EXPANSION:\n")
            f.write("-"*60 + "\n")
            f.write(f"\nCore Premise:\n{output_data['core_premise']}\n\n")
            f.write(f"Central Conflict:\n{output_data['central_conflict']}\n\n")
            f.write(f"Episode Rationale:\n{output_data['episode_rationale']}\n\n")

            f.write("Breaking Points:\n")
            for i, bp in enumerate(output_data['breaking_points'], 1):
                f.write(f"  {i}. {bp}\n")

            f.write("\nMain Characters:\n")
            for char in output_data['main_characters']:
                f.write(f"  • {char}\n")

        print(f"\n✅ Output saved to:")
        print(f"   📄 {json_path}")
        print(f"   📄 {txt_path}")

    async def process(self, session_id: str = None) -> Dict:
        """Main processing method"""
        try:
            if not session_id:
                session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Step 1: Get user input
            seed_content, seed_type = self.get_user_seed_input()

            # Step 2: Generate scale options
            llm_output = await self.generate_scale_options(seed_content, seed_type)

            # Step 3: Get user's scale choice
            chosen_letter, chosen_option_details = self.display_options_and_get_choice(llm_output)

            # Step 4: Get working titles from LLM output
            working_titles = llm_output['initial_expansion']['working_titles']

            # Step 5: Get user's title choice
            chosen_title = self.display_titles_and_get_choice(working_titles)

            # Step 6: Show initial expansion
            print("\n" + "="*60)
            print("📖 INITIAL EXPANSION GENERATED")
            print("="*60)
            expansion = llm_output['initial_expansion']
            print(f"\nCore Premise:\n{expansion['core_premise']}\n")
            print(f"Central Conflict:\n{expansion['central_conflict']}\n")
            print(f"Episode Rationale:\n{expansion['episode_rationale']}\n")
            print(f"\nBreaking Points:")
            for i, bp in enumerate(expansion['breaking_points'], 1):
                print(f"  {i}. {bp}")
            print(f"\nMain Characters: {', '.join(expansion['main_characters'])}")

            # Step 7: Create output object
            output_data = {
                'original_seed': seed_content,
                'seed_type': seed_type,
                'chosen_option': chosen_letter,
                'option_details': chosen_option_details,
                'working_titles': working_titles,
                'chosen_title': chosen_title,
                'core_premise': expansion['core_premise'],
                'central_conflict': expansion['central_conflict'],
                'episode_rationale': expansion['episode_rationale'],
                'breaking_points': expansion['breaking_points'],
                'main_characters': expansion['main_characters'],
                'session_id': session_id,
                'timestamp': datetime.now().isoformat()
            }

            # Step 8: Save output
            self.save_output(output_data)

            # Step 9: Store in Redis for Station 2
            await self.redis.set(
                f"audiobook:{session_id}:station_01",
                json.dumps(output_data),
                expire=86400
            )

            print("\n" + "="*60)
            print("✅ STATION 1 COMPLETE!")
            print("="*60)
            print(f"\nProject: {chosen_title}")
            print(f"Scale: {chosen_option_details['type']} ({chosen_option_details['episode_count']})")
            print(f"Session ID: {session_id}")
            print("\n📌 Ready to proceed to Station 2: Project DNA Builder")

            return output_data

        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            raise
        except Exception as e:
            logger.error(f"❌ Station 1 failed: {str(e)}")
            raise


# CLI Entry Point
async def main():
    """Run Station 1 standalone"""
    processor = Station01SeedProcessor()
    await processor.initialize()

    try:
        output = await processor.process()
        print(f"\n✅ Success! Session ID: {output['session_id']}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
