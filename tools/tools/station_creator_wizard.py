#!/usr/bin/env python3
"""
Station Creator Wizard - Interactive AI-Powered Station Builder

This wizard guides customers through creating custom stations with continuous
approval loops. After every step, the AI asks for feedback and makes changes
until the customer is satisfied.

Usage:
    python tools/station_creator_wizard.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient


class StationCreatorWizard:
    """Interactive wizard for creating custom stations with approval loops"""

    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = None
        self.session_data = {
            "station_number": None,
            "station_name": None,
            "station_purpose": None,
            "station_type": None,
            "input_stations": [],
            "output_format": {},
            "ai_complexity": None,
            "ai_model": None,
            "ai_prompt": None,
            "generated_code": None,
            "config_yaml": None
        }
        self.available_stations = self._load_available_stations()

    def _load_available_stations(self) -> List[Dict[str, str]]:
        """Load list of available stations for input selection"""
        return [
            {"number": 1, "name": "Seed Processor", "description": "Story seed and scale options"},
            {"number": 2, "name": "Project DNA Builder", "description": "Genre, audience, world setting"},
            {"number": 3, "name": "Age Genre Optimizer", "description": "Age guidelines and tone calibration"},
            {"number": 4, "name": "Reference Miner", "description": "Story seeds and references"},
            {"number": 5, "name": "Season Architecture", "description": "Episode structure and pacing"},
            {"number": 6, "name": "Master Style Guide", "description": "Audio style guidelines"},
            {"number": 7, "name": "Reality Check", "description": "Feasibility analysis"},
            {"number": 8, "name": "Character Architecture", "description": "Character profiles and arcs"},
            {"number": 9, "name": "World Building", "description": "World details and locations"},
            {"number": 10, "name": "Narrative Reveal Strategy", "description": "Information reveal timing"},
            {"number": 11, "name": "Runtime Planning", "description": "Episode timing and pacing"},
            {"number": 12, "name": "Hook Cliffhanger", "description": "Episode hooks and cliffhangers"},
            {"number": 13, "name": "Multiworld Timeline", "description": "Timeline and continuity"},
            {"number": 14, "name": "Episode Blueprint", "description": "Episode structure"},
            {"number": 15, "name": "Detailed Episode Outlining", "description": "Scene-by-scene details"},
            {"number": 16, "name": "Canon Check", "description": "Consistency validation"},
            {"number": 17, "name": "Dialect Planning", "description": "Character speech patterns"},
            {"number": 18, "name": "Evergreen Check", "description": "Timelessness validation"},
            {"number": 19, "name": "Procedure Check", "description": "Technical accuracy"},
            {"number": 20, "name": "Geography Transit", "description": "Location logistics"}
        ]

    async def initialize(self):
        """Initialize the wizard"""
        self.redis = RedisClient()
        await self.redis.initialize()

    def print_header(self):
        """Print wizard header"""
        print("\n" + "="*80)
        print("🎯 STATION CREATOR WIZARD")
        print("="*80)
        print("✨ Create custom stations with AI assistance")
        print("🔄 Review and approve each step before moving forward")
        print("💡 Request changes anytime - the AI will adapt")
        print("="*80 + "\n")

    def get_input(self, prompt: str, default: str = None) -> str:
        """Get user input with optional default"""
        if default:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            return user_input if user_input else default
        return input(f"{prompt}: ").strip()

    def get_approval(self, item_name: str) -> tuple[bool, Optional[str]]:
        """
        Get user approval for generated content
        Returns: (approved: bool, change_request: Optional[str])
        """
        print(f"\n{'─'*60}")
        print(f"✓ {item_name} generated above")
        print(f"{'─'*60}")
        response = self.get_input(
            "\n👉 Does this look good?\n"
            "   Type 'yes' to continue\n"
            "   OR describe any changes you want"
        ).lower()

        if response in ['yes', 'y', 'ok', 'good', 'looks good', 'perfect']:
            return True, None
        else:
            return False, response

    async def step_1_station_basics(self):
        """Step 1: Get station name and number with approval loop"""
        print("\n" + "🔷 STEP 1: STATION BASICS" + "\n")

        while True:
            # Get next available station number
            script_dir = Path(__file__).parent.parent / "app" / "agents"
            existing_stations = [f for f in script_dir.glob("station_*.py")]
            station_numbers = []
            for f in existing_stations:
                try:
                    num = int(f.stem.split("_")[1])
                    station_numbers.append(num)
                except:
                    pass
            next_number = max(station_numbers) + 1 if station_numbers else 21

            # Get station name
            station_name = self.get_input(
                "\n📝 What would you like to name this station?\n"
                "   (Example: 'Music Cue Generator', 'Dialogue Polisher', 'Emotion Analyzer')"
            )

            # Create file name
            file_name = station_name.lower().replace(" ", "_").replace("-", "_")
            file_name = ''.join(c for c in file_name if c.isalnum() or c == '_')

            # Show what will be created
            print(f"\n✨ STATION CREATED:")
            print(f"   📌 Station Number: {next_number}")
            print(f"   📌 Station Name: Station {next_number}: {station_name}")
            print(f"   📌 File Name: station_{next_number}_{file_name}.py")
            print(f"   📌 Config File: station_{next_number}.yml")

            # Get approval
            approved, change_request = self.get_approval("Station basics")

            if approved:
                self.session_data["station_number"] = next_number
                self.session_data["station_name"] = station_name
                self.session_data["file_name"] = file_name
                break
            else:
                print(f"\n🔄 Got it! Let me adjust based on: '{change_request}'")
                if "number" in change_request.lower():
                    try:
                        # Extract number from change request
                        import re
                        nums = re.findall(r'\d+', change_request)
                        if nums:
                            next_number = int(nums[0])
                            print(f"   ✓ Changed station number to: {next_number}")
                    except:
                        pass
                print("   Let's try again...\n")

    async def step_2_station_purpose(self):
        """Step 2: Define station purpose with AI assistance and approval loop"""
        print("\n" + "🔷 STEP 2: STATION PURPOSE" + "\n")

        while True:
            # Get user's description
            user_description = self.get_input(
                "\n📝 What should this station do? Describe in your own words.\n"
                "   (Be as detailed or brief as you like)"
            )

            # Use AI to create a professional description
            print("\n🤖 Generating professional description...")

            ai_prompt = f"""Based on this user description, create a clear, professional station purpose description:

User Description: {user_description}

Station Name: {self.session_data['station_name']}

Create a 2-3 sentence professional description that:
1. Clearly states what the station does
2. Explains the value it provides
3. Fits into an audiobook production pipeline

Return ONLY the description, no other text."""

            professional_description = await self.openrouter.process_message(
                ai_prompt,
                model_name="qwen-72b"
            )

            professional_description = professional_description.strip()

            # Show generated description
            print(f"\n✨ STATION PURPOSE:")
            print(f"\n   STATION {self.session_data['station_number']}: {self.session_data['station_name'].upper()}")
            print(f"   {'─'*70}")
            print(f"   Purpose: {professional_description}")
            print(f"   {'─'*70}")

            # Get approval
            approved, change_request = self.get_approval("Station purpose")

            if approved:
                self.session_data["station_purpose"] = professional_description
                break
            else:
                print(f"\n🔄 Adjusting based on: '{change_request}'")
                # Re-run with modification request
                user_description = f"{user_description}\n\nModification requested: {change_request}"

    async def step_3_station_type(self):
        """Step 3: Select station type with approval loop"""
        print("\n" + "🔷 STEP 3: STATION TYPE" + "\n")

        station_types = {
            "1": {
                "name": "Analysis Station",
                "description": "Analyzes existing data and provides insights",
                "examples": "Quality checks, validation, consistency analysis"
            },
            "2": {
                "name": "Generation Station",
                "description": "Creates new content based on inputs",
                "examples": "Character dialogue, scene descriptions, music cues"
            },
            "3": {
                "name": "Enhancement Station",
                "description": "Improves or enriches existing content",
                "examples": "Dialogue polishing, description enhancement"
            },
            "4": {
                "name": "Validation Station",
                "description": "Checks correctness and feasibility",
                "examples": "Fact checking, timeline validation, budget checks"
            }
        }

        while True:
            print("\n📋 Select the station type:\n")
            for key, stype in station_types.items():
                print(f"   {key}. {stype['name']}")
                print(f"      → {stype['description']}")
                print(f"      Examples: {stype['examples']}\n")

            choice = self.get_input("Enter choice (1-4)")

            if choice in station_types:
                selected_type = station_types[choice]

                print(f"\n✨ STATION TYPE SELECTED:")
                print(f"   📌 Type: {selected_type['name']}")
                print(f"   📌 Purpose: {selected_type['description']}")

                # Get approval
                approved, change_request = self.get_approval("Station type")

                if approved:
                    self.session_data["station_type"] = selected_type["name"]
                    break
                else:
                    print(f"\n🔄 Let's choose a different type based on: '{change_request}'")
            else:
                print("❌ Invalid choice. Please enter 1-4.")

    async def step_4_input_configuration(self):
        """Step 4: Configure input stations with approval loop"""
        print("\n" + "🔷 STEP 4: INPUT CONFIGURATION" + "\n")

        while True:
            print("\n📥 Which stations should provide data to this station?\n")
            print("   Available stations:\n")

            for station in self.available_stations:
                print(f"   [{station['number']:2d}] Station {station['number']:2d}: {station['name']}")
                print(f"        → {station['description']}")

            print("\n   Type station numbers separated by commas (e.g., 8,14,15)")
            print("   Or type 'none' if this station doesn't need inputs from other stations")

            selection = self.get_input("\n👉 Select inputs").lower()

            if selection == 'none':
                selected_stations = []
            else:
                try:
                    numbers = [int(n.strip()) for n in selection.split(",")]
                    selected_stations = [s for s in self.available_stations if s["number"] in numbers]
                except:
                    print("❌ Invalid format. Please use comma-separated numbers.")
                    continue

            # Show configuration
            print(f"\n✨ INPUT CONFIGURATION:")
            if selected_stations:
                print(f"   Station {self.session_data['station_number']} will receive inputs from:\n")
                for station in selected_stations:
                    print(f"   ✓ Station {station['number']}: {station['name']}")
                    print(f"     → {station['description']}")
            else:
                print(f"   Station {self.session_data['station_number']} requires no inputs from other stations")

            # Get approval
            approved, change_request = self.get_approval("Input configuration")

            if approved:
                self.session_data["input_stations"] = selected_stations
                break
            else:
                print(f"\n🔄 Let's reconfigure inputs based on: '{change_request}'")

    async def step_5_ai_processing_config(self):
        """Step 5: Configure AI processing with approval loop"""
        print("\n" + "🔷 STEP 5: AI PROCESSING CONFIGURATION" + "\n")

        complexity_levels = {
            "1": {
                "name": "Simple",
                "model": "anthropic/claude-3.5-haiku",
                "description": "Fast analysis, basic patterns, quick turnaround",
                "best_for": "Simple validations, basic checks, quick classifications"
            },
            "2": {
                "name": "Medium",
                "model": "qwen-72b",
                "description": "Balanced analysis, nuanced understanding, good quality",
                "best_for": "Content generation, detailed analysis, creative tasks"
            },
            "3": {
                "name": "Complex",
                "model": "anthropic/claude-sonnet-4",
                "description": "Deep analysis, highly creative, best quality output",
                "best_for": "Complex creative work, sophisticated analysis, critical tasks"
            }
        }

        while True:
            print("\n🤖 How complex should the AI processing be?\n")
            for key, level in complexity_levels.items():
                print(f"   {key}. {level['name'].upper()}")
                print(f"      Model: {level['model']}")
                print(f"      → {level['description']}")
                print(f"      Best for: {level['best_for']}\n")

            choice = self.get_input("Enter choice (1-3)")

            if choice in complexity_levels:
                selected_level = complexity_levels[choice]

                # Generate AI prompt using AI
                print("\n🤖 Generating AI prompt template...")

                prompt_generation_request = f"""Create an AI prompt template for this station:

Station Name: {self.session_data['station_name']}
Station Purpose: {self.session_data['station_purpose']}
Station Type: {self.session_data['station_type']}
Input Stations: {', '.join([f"Station {s['number']}" for s in self.session_data['input_stations']]) if self.session_data['input_stations'] else 'None'}

Create a clear, structured prompt that:
1. Explains the task to the AI
2. Shows what inputs it will receive
3. Specifies the expected output format
4. Includes any special instructions

Make it production-ready and professional."""

                generated_prompt = await self.openrouter.process_message(
                    prompt_generation_request,
                    model_name="qwen-72b"
                )

                # Show configuration
                print(f"\n✨ AI PROCESSING CONFIGURATION:")
                print(f"   📌 Complexity: {selected_level['name']}")
                print(f"   📌 AI Model: {selected_level['model']}")
                print(f"   📌 Best For: {selected_level['best_for']}")
                print(f"\n   AI PROMPT TEMPLATE:")
                print(f"   {'─'*70}")
                print(f"{generated_prompt}")
                print(f"   {'─'*70}")

                # Get approval
                approved, change_request = self.get_approval("AI processing configuration")

                if approved:
                    self.session_data["ai_complexity"] = selected_level["name"]
                    self.session_data["ai_model"] = selected_level["model"]
                    self.session_data["ai_prompt"] = generated_prompt
                    break
                else:
                    print(f"\n🔄 Let me adjust based on: '{change_request}'")

                    # If user wants prompt changes, regenerate with modifications
                    if "prompt" in change_request.lower():
                        prompt_generation_request += f"\n\nUser modification request: {change_request}"
                        generated_prompt = await self.openrouter.process_message(
                            prompt_generation_request,
                            model_name="qwen-72b"
                        )
            else:
                print("❌ Invalid choice. Please enter 1-3.")

    async def step_6_output_format(self):
        """Step 6: Define output format with approval loop"""
        print("\n" + "🔷 STEP 6: OUTPUT FORMAT" + "\n")

        while True:
            print("\n📤 Let me suggest an output format for this station...\n")

            # Generate output format using AI
            print("🤖 Analyzing requirements and generating output structure...")

            output_generation_request = f"""Design a JSON output format for this station:

Station Name: {self.session_data['station_name']}
Station Purpose: {self.session_data['station_purpose']}
Station Type: {self.session_data['station_type']}

Create a clear, structured JSON output format that:
1. Contains all necessary data this station should produce
2. Is well-organized and easy to parse
3. Follows naming conventions (snake_case for keys)
4. Includes example values

Return ONLY the JSON structure with example data, formatted nicely."""

            generated_output = await self.openrouter.process_message(
                output_generation_request,
                model_name="qwen-72b"
            )

            # Show output format
            print(f"\n✨ OUTPUT FORMAT:")
            print(f"   {'─'*70}")
            print(generated_output)
            print(f"   {'─'*70}")

            # Get approval
            approved, change_request = self.get_approval("Output format")

            if approved:
                self.session_data["output_format"] = generated_output
                break
            else:
                print(f"\n🔄 Regenerating output format based on: '{change_request}'")
                output_generation_request += f"\n\nUser modification: {change_request}"

    async def step_7_generate_code(self):
        """Step 7: Generate complete station code with approval loop"""
        print("\n" + "🔷 STEP 7: CODE GENERATION" + "\n")

        from station_generator import StationCodeGenerator

        generator = StationCodeGenerator(self.session_data)

        while True:
            print("\n⚙️  Generating complete station code...")
            print("   This includes:")
            print("   ✓ Full Python implementation")
            print("   ✓ Retry logic with exponential backoff")
            print("   ✓ Redis state management")
            print("   ✓ Error handling and logging")
            print("   ✓ Input validation")
            print("   ✓ Output formatting")
            print("   ✓ Integration hooks\n")

            # Generate code
            python_code = generator.generate_station_code()
            yaml_config = generator.generate_yaml_config()

            # Show preview
            print(f"\n✨ CODE GENERATED:")
            print(f"   📁 File: station_{self.session_data['station_number']}_{self.session_data['file_name']}.py")
            print(f"   📏 Size: {len(python_code)} characters ({len(python_code.split(chr(10)))} lines)")
            print(f"\n   📋 Configuration: station_{self.session_data['station_number']}.yml")
            print(f"   📏 Size: {len(yaml_config)} characters")

            print(f"\n   🔍 CODE PREVIEW (first 50 lines):")
            print(f"   {'─'*70}")
            preview_lines = python_code.split('\n')[:50]
            for line in preview_lines:
                print(f"   {line}")
            print(f"   {'─'*70}")
            print(f"   ... ({len(python_code.split(chr(10))) - 50} more lines)")

            print(f"\n   Would you like to:")
            print(f"   1. Accept and create the files (type 'create')")
            print(f"   2. See the full code (type 'show')")
            print(f"   3. Make changes (describe what to change)")

            response = self.get_input("\n👉 Your choice").lower()

            if response == 'create':
                self.session_data["generated_code"] = python_code
                self.session_data["config_yaml"] = yaml_config
                break
            elif response == 'show':
                print(f"\n📄 FULL CODE:")
                print(f"{'='*80}")
                print(python_code)
                print(f"{'='*80}")
                print(f"\n📄 CONFIGURATION:")
                print(f"{'='*80}")
                print(yaml_config)
                print(f"{'='*80}")
            else:
                print(f"\n🔄 Let me adjust the code based on: '{response}'")
                # In a real implementation, we'd regenerate with modifications
                print("   (Code modification not implemented in this version)")
                print("   You can edit the files after they're created.")
                continue

    async def step_8_create_files(self):
        """Step 8: Write files to disk"""
        print("\n" + "🔷 STEP 8: CREATING FILES" + "\n")

        # Get project root (go up 3 levels: tools/tools/wizard.py -> tools/tools/ -> tools/ -> project_root/)
        script_dir = Path(__file__).parent.parent.parent

        # Create Python file
        python_file_path = script_dir / "app" / "agents" / f"station_{self.session_data['station_number']}_{self.session_data['file_name']}.py"
        yaml_file_path = script_dir / "app" / "agents" / "configs" / f"station_{self.session_data['station_number']}.yml"

        print(f"✍️  Writing files...")

        # Write Python file
        with open(python_file_path, 'w') as f:
            f.write(self.session_data["generated_code"])
        print(f"   ✅ Created: {python_file_path}")

        # Write YAML config
        with open(yaml_file_path, 'w') as f:
            f.write(self.session_data["config_yaml"])
        print(f"   ✅ Created: {yaml_file_path}")

        # Create test file
        test_file_path = script_dir / "tools" / f"test_station_{self.session_data['station_number']}.py"
        test_code = self._generate_test_file()
        with open(test_file_path, 'w') as f:
            f.write(test_code)
        print(f"   ✅ Created: {test_file_path}")

        print(f"\n🎉 SUCCESS! Your station is ready!\n")
        print(f"   📁 Station Code: {python_file_path}")
        print(f"   📋 Configuration: {yaml_file_path}")
        print(f"   🧪 Test File: {test_file_path}")

        print(f"\n   🚀 Next Steps:")
        print(f"   1. Test your station: python {test_file_path}")
        print(f"   2. Review the code: {python_file_path}")
        print(f"   3. Customize as needed")
        print(f"   4. Integrate into main pipeline when ready")

    def _generate_test_file(self) -> str:
        """Generate a test file for the station"""
        return f'''#!/usr/bin/env python3
"""
Test file for Station {self.session_data['station_number']}: {self.session_data['station_name']}
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agents.station_{self.session_data['station_number']}_{self.session_data['file_name']} import Station{self.session_data['station_number']:02d}{self.session_data['station_name'].replace(' ', '')}


async def test_station():
    """Test the station"""
    print(f"🧪 Testing Station {self.session_data['station_number']}: {self.session_data['station_name']}")
    print("="*70)

    # Initialize station
    station = Station{self.session_data['station_number']:02d}{self.session_data['station_name'].replace(' ', '')}()
    await station.initialize()

    # Create test session
    test_session_id = "test_station_{self.session_data['station_number']}_001"

    print(f"\\n📝 Session ID: {{test_session_id}}")
    print(f"\\n⚙️  Processing...")

    try:
        # Run station
        result = await station.process(test_session_id)

        print(f"\\n✅ Station completed successfully!")
        print(f"\\n📤 Output:")
        print(f"{{result}}")

    except Exception as e:
        print(f"\\n❌ Error: {{e}}")
        raise


if __name__ == "__main__":
    asyncio.run(test_station())
'''

    async def run(self):
        """Run the complete wizard"""
        await self.initialize()
        self.print_header()

        try:
            await self.step_1_station_basics()
            await self.step_2_station_purpose()
            await self.step_3_station_type()
            await self.step_4_input_configuration()
            await self.step_5_ai_processing_config()
            await self.step_6_output_format()
            await self.step_7_generate_code()
            await self.step_8_create_files()

            print("\n" + "="*80)
            print("🎊 WIZARD COMPLETE!")
            print("="*80)
            print(f"Station {self.session_data['station_number']}: {self.session_data['station_name']} is ready to use!")
            print("\n")

        except KeyboardInterrupt:
            print("\n\n⚠️  Wizard cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            raise


async def main():
    """Main entry point"""
    wizard = StationCreatorWizard()
    await wizard.run()


if __name__ == "__main__":
    asyncio.run(main())
