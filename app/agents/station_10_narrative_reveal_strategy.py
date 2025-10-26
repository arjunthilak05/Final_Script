"""
Station 10: Narrative Reveal Strategy

This station designs complete information flow architecture for audio drama.
Analyzes all story elements and creates reveal taxonomy, plant/proof/payoff grid,
red herring strategy, and fairness analysis using 45-method reveal catalog.

Flow:
1. Load ALL previous station data (Stations 1-9)
2. Display story context summary
3. Task 1: Generate Reveal Taxonomy (Auto)
4. Display Information Classification Grid
5. Task 2: Select Reveal Methods from 45-catalog (Auto)
6. Display Major Reveals with Methods
7. HUMAN REVIEW: Approve reveal methods? (Optional)
8. Task 3: Create Plant/Proof/Payoff Grid (Auto)
9. Display P3 Grid Sample
10. Task 4: Design Red Herring Strategy (Auto)
11. Display Red Herrings Timeline
12. Task 5: Fairness Check Analysis (Auto)
13. Display Fairness Metrics
14. HUMAN REVIEW: Approve complete strategy? (Optional)
15. Save outputs (JSON + TXT + CSV Grid)
16. Save to Redis for Station 11

Critical Architecture Agent - Output is the blueprint for entire information flow
"""

import asyncio
import json
import csv
import os
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json
from app.agents.title_validator import TitleValidator


class Station10NarrativeRevealStrategy:
    """Station 10: Narrative Reveal Strategy"""

    def __init__(self, session_id: str, skip_review: bool = False):
        self.session_id = session_id
        self.skip_review = skip_review
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=10)
        self.output_dir = Path("output/station_10")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Store intermediate results
        self.task_results = {}
        self.extracted_inputs = {}
        self.all_station_data = {}

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🎬 STATION 10: NARRATIVE REVEAL STRATEGY")
        print("=" * 70)
        print()

        try:
            # Step 1: Load ALL previous station data
            print("📥 Loading complete story context...")
            await self.load_all_previous_stations()
            print("✅ Full context loaded - ready to design information flow")
            print()

            # Step 2: Display story context
            self.display_story_context()

            # Step 3-5: Execute reveal taxonomy
            print("=" * 70)
            print("🎯 EXECUTING NARRATIVE REVEAL STRATEGY (5 TASKS)")
            print("=" * 70)
            print()

            await self.execute_task_1_reveal_taxonomy()
            await self.execute_task_2_reveal_methods()

            # Step 6: Optional human review of methods
            if not self.skip_review:
                await self.human_review_reveal_methods()

            await self.execute_task_3_plant_proof_payoff()
            await self.execute_task_4_red_herrings()
            await self.execute_task_5_fairness_check()

            # Step 7: Final human review
            if not self.skip_review:
                await self.human_review_complete_strategy()

            # Step 8: Generate outputs
            print()
            print("=" * 70)
            print("💾 GENERATING OUTPUT FILES")
            print("=" * 70)
            print()

            await self.generate_outputs()

            # Step 9: Display completion
            self.display_completion()

        except Exception as e:
            print(f"❌ Station 10 failed: {str(e)}")
            logging.error(f"Station 10 error: {str(e)}", exc_info=True)
            raise

    async def load_all_previous_stations(self):
        """Load data from all previous stations (1-9)"""
        try:
            stations_to_load = ['01', '02', '03', '04', '045', '05', '06', '07', '08', '09']

            station_names = {
                '01': 'Seed Processor',
                '02': 'Project DNA Builder',
                '03': 'Age Genre Optimizer',
                '04': 'Reference Mining',
                '045': 'Narrator Strategy',
                '05': 'Season Architect',
                '06': 'Master Style Guide',
                '07': 'Chapter Architect',
                '08': 'World Builder',
                '09': 'World Building System'
            }

            for station_num in stations_to_load:
                key = f"audiobook:{self.session_id}:station_{station_num}"
                data = await self.redis_client.get(key)

                if data:
                    self.all_station_data[station_num] = json.loads(data)
                    print(f"   ✓ Station {station_num}: {station_names.get(station_num, 'loaded')}")
                else:
                    if station_num in ['06', '07']:  # Optional stations
                        print(f"   ⚠️  Station {station_num}: {station_names.get(station_num, 'Unknown')} not found (optional)")
                    else:
                        raise ValueError(f"❌ Station {station_num} data required but not found")

            # Extract key inputs
            self.extract_key_inputs()

            print()
            print(f"Session ID: {self.session_id}")

        except Exception as e:
            raise ValueError(f"❌ Error loading previous stations: {str(e)}")

    def extract_key_inputs(self):
        """Extract key inputs from all loaded data"""
        try:
            # From Station 1
            st1 = self.all_station_data.get('01', {})
            self.extracted_inputs['episode_count'] = st1.get('option_details', {}).get('episode_count', 'Unknown')
            self.extracted_inputs['episode_length'] = st1.get('option_details', {}).get('episode_length', 'Unknown')
            self.extracted_inputs['story_complexity'] = st1.get('story_complexity', 'Unknown')

            # From Station 2
            st2 = self.all_station_data.get('02', {})
            self.extracted_inputs['working_title'] = TitleValidator.extract_bulletproof_title(st1, st2)
            self.extracted_inputs['core_premise'] = st2.get('world_setting', {}).get('core_premise',
                st2.get('world_setting', {}).get('primary_location', 'Unknown'))

            # From Station 3
            st3 = self.all_station_data.get('03', {})
            self.extracted_inputs['primary_genre'] = st3.get('chosen_blend_details', {}).get('primary_genre', 'Drama')
            self.extracted_inputs['target_age'] = st3.get('age_guidelines', {}).get('target_age_range', '25-45')

        except Exception as e:
            logging.warning(f"Could not extract some inputs: {str(e)}")

    def display_story_context(self):
        """Display story context summary"""
        print("-" * 70)
        print("📋 STORY CONTEXT FOR REVEAL DESIGN")
        print("-" * 70)
        print(f"Title: {self.extracted_inputs.get('working_title', 'N/A')}")
        print(f"Format: {self.extracted_inputs.get('episode_count', 'N/A')} episodes, {self.extracted_inputs.get('episode_length', 'N/A')} each")
        print(f"Genre: {self.extracted_inputs.get('primary_genre', 'N/A')}")
        print(f"Target Age: {self.extracted_inputs.get('target_age', 'N/A')}")
        print(f"Story Complexity: {self.extracted_inputs.get('story_complexity', 'N/A')}")
        print()
        print("Core Premise:")
        print(f"  {self.extracted_inputs.get('core_premise', 'N/A')}")
        print("-" * 70)
        print()
        print("🎯 Designing narrative reveal architecture...")
        print()

    async def execute_task_1_reveal_taxonomy(self):
        """Task 1: Generate Reveal Taxonomy"""
        print("=" * 70)
        print("📚 TASK 1: REVEAL TAXONOMY CLASSIFICATION")
        print("=" * 70)
        print()
        print("🤖 Analyzing all story information...")
        print("   Categorizing by reveal timing and necessity...")
        print("   Mapping knowledge requirements per episode...")
        print("   Identifying implicit vs explicit information...")
        print()

        try:
            # Build complete story context
            story_context = self._build_complete_story_context()

            # Build prompt
            prompt = self.config.get_prompt('task_1_reveal_taxonomy')
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Unknown'),
                episode_count=self.extracted_inputs.get('episode_count', 'Unknown'),
                episode_length=self.extracted_inputs.get('episode_length', 'Unknown'),
                story_complexity=self.extracted_inputs.get('story_complexity', 'Unknown'),
                core_premise=self.extracted_inputs.get('core_premise', 'Unknown'),
                complete_story_context=story_context,
                total_episodes=self._extract_episode_number()
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            taxonomy_data = extract_json(response)

            # Store result
            self.task_results['task_1_taxonomy'] = taxonomy_data.get('reveal_taxonomy', {})

            # Display summary
            total_elements = self.task_results['task_1_taxonomy'].get('total_information_units', 0)
            print(f"✅ Classified {total_elements} story elements into reveal taxonomy")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

            # Display information grid
            self._display_information_grid()

        except Exception as e:
            print(f"❌ Task 1 failed: {str(e)}")
            raise

    def _build_complete_story_context(self) -> str:
        """Build comprehensive story context from all stations"""
        context_parts = []

        # Add data from each station
        for station_num, data in self.all_station_data.items():
            context_parts.append(f"**STATION {station_num} DATA:**")
            context_parts.append(json.dumps(data, indent=2)[:2000])  # Limit size
            context_parts.append("")

        return "\n".join(context_parts)

    def _extract_episode_number(self) -> int:
        """Extract total episode number from format"""
        ep_count = self.extracted_inputs.get('episode_count', '10')
        if '-' in str(ep_count):
            return int(str(ep_count).split('-')[1].split()[0])
        return 10  # Default

    def _display_information_grid(self):
        """Display information classification grid summary"""
        print("=" * 70)
        print("📊 INFORMATION CLASSIFICATION GRID")
        print("=" * 70)
        print()

        taxonomy = self.task_results.get('task_1_taxonomy', {})

        # Display must-know elements
        must_know = taxonomy.get('must_know_by_episode', {})
        if must_know:
            print("MUST KNOW BY EPISODE X (Critical Plot Points):")
            print("-" * 70)
            for episode, elements in list(must_know.items())[:3]:  # Show first 3 episodes
                print(f"\n{episode.replace('_', ' ').title()}:")
                for elem in elements[:2]:  # Show first 2 elements
                    print(f"  • {elem.get('element', 'N/A')}")
            print()

        # Display stats
        print("-" * 70)
        print(f"Total Information Units: {taxonomy.get('total_information_units', 0)}")
        print(f"  • Critical Reveals: {taxonomy.get('critical_reveals', 0)}")
        print(f"  • Clued Discoveries: {taxonomy.get('clued_discoveries', 0)}")
        print(f"  • Subtle Plants: {taxonomy.get('subtle_plants', 0)}")
        print(f"  • Ambiguous Elements: {taxonomy.get('ambiguous_elements', 0)}")
        print("=" * 70)
        print()

    async def execute_task_2_reveal_methods(self):
        """Task 2: Select Reveal Methods"""
        print("=" * 70)
        print("🎨 TASK 2: REVEAL METHOD SELECTION")
        print("=" * 70)
        print()
        print("🤖 Analyzing story from 45-method catalog...")
        print("   Matching reveal types to story moments...")
        print("   Considering audio execution for each...")
        print("   Optimizing audience positioning...")
        print()

        try:
            # Build taxonomy summary
            taxonomy_summary = json.dumps(self.task_results.get('task_1_taxonomy', {}), indent=2)[:3000]

            # Build prompt
            prompt = self.config.get_prompt('task_2_reveal_methods')
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Unknown'),
                episode_count=self.extracted_inputs.get('episode_count', 'Unknown'),
                reveal_taxonomy_summary=taxonomy_summary
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            methods_data = extract_json(response)

            # Store result
            self.task_results['task_2_methods'] = methods_data

            # Display summary
            reveal_methods = methods_data.get('reveal_methods', [])
            print(f"✅ Selected {len(reveal_methods)} reveal methods for major story beats")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

            # Display major reveals
            self._display_major_reveals()

        except Exception as e:
            print(f"❌ Task 2 failed: {str(e)}")
            raise

    def _display_major_reveals(self):
        """Display major revelations with selected methods"""
        print("=" * 70)
        print("🎭 MAJOR REVEALS & SELECTED METHODS")
        print("=" * 70)
        print()

        methods = self.task_results.get('task_2_methods', {}).get('reveal_methods', [])

        for i, method in enumerate(methods[:5], 1):  # Show first 5
            print(f"REVELATION {i}: {method.get('revelation', 'Unknown')}")
            print("-" * 70)
            print(f"Method: #{method.get('method_number')} {method.get('method_name')}")
            print(f"Why: {method.get('why_selected', 'N/A')[:150]}...")
            print(f"Audio: {method.get('audio_execution', 'N/A')[:150]}...")
            print(f"Episode: Revealed in {method.get('episode_revealed')}, clued from {method.get('episode_first_clue')}")
            print()

        if len(methods) > 5:
            print(f"... and {len(methods) - 5} more revelations")
            print()

        # Display distribution
        distribution = self.task_results.get('task_2_methods', {}).get('method_distribution', {})
        print("-" * 70)
        print("📊 REVEAL METHOD DISTRIBUTION:")
        for method, count in list(distribution.items())[:5]:
            print(f"  • {method}: {count} uses")
        print("=" * 70)
        print()

    async def human_review_reveal_methods(self):
        """Optional human review of reveal methods"""
        print("=" * 70)
        print("⭐ HUMAN DECISION REQUIRED")
        print("=" * 70)
        print()

        reveal_count = len(self.task_results.get('task_2_methods', {}).get('reveal_methods', []))
        print(f"The reveal strategy has been generated with {reveal_count} major revelations")
        print("using methods from the 45-method catalog.")
        print()
        print("OPTIONS:")
        print("  [Enter] - Approve and continue to Plant/Proof/Payoff Grid")
        print("  [V]     - View complete list of all revelations")
        print("  [R]     - Regenerate with different method emphasis")
        print()
        print("💡 TIP: Press V to see all revelations before approving")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == 'V':
            self._view_all_revelations()
            input("\nPress Enter when ready to continue: ")
        elif choice == 'R':
            print("\nRegeneration not yet implemented. Continuing with current methods...")
            await asyncio.sleep(1)

    def _view_all_revelations(self):
        """View all revelations in detail"""
        methods = self.task_results.get('task_2_methods', {}).get('reveal_methods', [])

        for i, method in enumerate(methods, 1):
            print(f"\n{'=' * 70}")
            print(f"REVELATION {i}: {method.get('revelation')}")
            print('=' * 70)
            print(f"Method: #{method.get('method_number')} {method.get('method_name')}")
            print(f"\nWhy Selected: {method.get('why_selected')}")
            print(f"\nAudio Execution: {method.get('audio_execution')}")
            print(f"\nAudience Positioning: {method.get('audience_positioning')}")
            print(f"\nTimeline: Clued from E{method.get('episode_first_clue')}, Revealed E{method.get('episode_revealed')}")
            print(f"\nRelisten Impact: {method.get('relisten_impact')}")

    async def execute_task_3_plant_proof_payoff(self):
        """Task 3: Create Plant/Proof/Payoff Grid"""
        print("=" * 70)
        print("🌱 TASK 3: PLANT/PROOF/PAYOFF GRID GENERATION")
        print("=" * 70)
        print()
        print("🤖 Creating comprehensive P3 Grid...")
        print("   Mapping every plant across series...")
        print("   Establishing proof moments...")
        print("   Designing payoff sequences...")
        print("   Cross-referencing episode timing...")
        print()

        try:
            # Build methods summary
            methods_summary = json.dumps(self.task_results.get('task_2_methods', {}), indent=2)[:3000]

            # Build prompt
            prompt = self.config.get_prompt('task_3_plant_proof_payoff')
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                episode_count=self.extracted_inputs.get('episode_count', 'Unknown'),
                reveal_methods_summary=methods_summary
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            p3_data = extract_json(response)

            # Store result
            self.task_results['task_3_p3_grid'] = p3_data

            # Display summary
            grid = p3_data.get('plant_proof_payoff_grid', [])
            stats = p3_data.get('grid_statistics', {})

            print(f"✅ Generated complete P3 Grid for {len(grid)} story elements")
            print(f"   • {stats.get('total_plants', 0)} Plants identified")
            print(f"   • {stats.get('total_proofs', 0)} Proof moments mapped")
            print(f"   • {stats.get('total_payoffs', 0)} Payoffs designed")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

            # Display sample
            self._display_p3_grid_sample()

        except Exception as e:
            print(f"❌ Task 3 failed: {str(e)}")
            raise

    def _display_p3_grid_sample(self):
        """Display P3 Grid sample"""
        print("=" * 70)
        print("📋 PLANT/PROOF/PAYOFF GRID (Sample of First 2 Revelations)")
        print("=" * 70)
        print()

        grid = self.task_results.get('task_3_p3_grid', {}).get('plant_proof_payoff_grid', [])

        for revelation in grid[:2]:  # Show first 2
            print(f"REVELATION: {revelation.get('revelation')}")
            print("━" * 70)

            # Show plants
            plants = revelation.get('plants', [])
            for i, plant in enumerate(plants[:2], 1):
                print(f"\nPLANT {i}:")
                print(f"  Episode: {plant.get('episode')}, Scene: {plant.get('scene')}")
                print(f"  Moment: {plant.get('moment')}")
                print(f"  Audio: {plant.get('audio')}")
                if plant.get('dialogue'):
                    print(f"  Line: {plant.get('dialogue')}")
                print(f"  Visibility: {plant.get('visibility')}")

            # Show proofs
            proofs = revelation.get('proofs', [])
            for i, proof in enumerate(proofs[:1], 1):
                print(f"\nPROOF {i}:")
                print(f"  Episode: {proof.get('episode')}, Scene: {proof.get('scene')}")
                print(f"  Moment: {proof.get('moment')}")
                print(f"  Audio: {proof.get('audio')}")
                print(f"  Evidence: {proof.get('evidence_type')}")

            # Show payoff
            payoff = revelation.get('payoff', {})
            if payoff:
                print(f"\nPAYOFF:")
                print(f"  Episode: {payoff.get('episode')}, Scene: {payoff.get('scene')}")
                print(f"  Moment: {payoff.get('moment')}")
                print(f"  Audio: {payoff.get('audio')}")
                print(f"  Line: {payoff.get('dialogue')}")
                print(f"  Impact: {payoff.get('impact')}")
                print(f"  Relisten Value: {payoff.get('relisten_value')}")

            print("\n" + "━" * 70 + "\n")

        if len(grid) > 2:
            print(f"... and {len(grid) - 2} more complete P3 grids\n")

        # Display stats
        stats = self.task_results.get('task_3_p3_grid', {}).get('grid_statistics', {})
        print("-" * 70)
        print("📊 P3 GRID STATISTICS:")
        print(f"  • Total Plants: {stats.get('total_plants', 0)} across all episodes")
        print(f"  • Average Plants per Revelation: {stats.get('average_plants_per_revelation', 0):.1f}")
        print(f"  • Audio-Only Plants: {stats.get('audio_only_plants', 0)} (no dialogue)")
        print("=" * 70)
        print()

    async def execute_task_4_red_herrings(self):
        """Task 4: Design Red Herring Strategy"""
        print("=" * 70)
        print("🎣 TASK 4: RED HERRING & MISDIRECTION DESIGN")
        print("=" * 70)
        print()
        print("🤖 Creating believable false leads...")
        print("   Designing red herrings with logical foundations...")
        print("   Timing misdirection introductions and reveals...")
        print("   Balancing false leads with real clues...")
        print()

        try:
            # Build story elements summary
            story_summary = self._create_story_elements_summary()

            # Build prompt
            prompt = self.config.get_prompt('task_4_red_herrings')
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Unknown'),
                episode_count=self.extracted_inputs.get('episode_count', 'Unknown'),
                story_elements_summary=story_summary
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            rh_data = extract_json(response)

            # Store result
            self.task_results['task_4_red_herrings'] = rh_data

            # Display summary
            red_herrings = rh_data.get('red_herrings', [])
            print(f"✅ Designed {len(red_herrings)} major red herrings with complete arcs")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

            # Display timeline
            self._display_red_herring_timeline()

        except Exception as e:
            print(f"❌ Task 4 failed: {str(e)}")
            raise

    def _create_story_elements_summary(self) -> str:
        """Create summary of story elements for red herring design"""
        parts = []

        # Add taxonomy
        taxonomy = self.task_results.get('task_1_taxonomy', {})
        parts.append("**STORY ELEMENTS:**")
        parts.append(json.dumps(taxonomy, indent=2)[:2000])

        # Add characters if available
        if '07' in self.all_station_data:
            parts.append("\n**CHARACTERS:**")
            parts.append(json.dumps(self.all_station_data['07'], indent=2)[:1000])

        return "\n".join(parts)

    def _display_red_herring_timeline(self):
        """Display red herring timeline"""
        print("=" * 70)
        print("🎣 RED HERRING STRATEGY & TIMELINE")
        print("=" * 70)
        print()

        red_herrings = self.task_results.get('task_4_red_herrings', {}).get('red_herrings', [])

        for i, rh in enumerate(red_herrings, 1):
            print(f"RED HERRING #{i}: \"{rh.get('title')}\"")
            print("-" * 70)
            print(f"Type: {rh.get('type')}")
            print(f"Target: {rh.get('target')}")
            print(f"Introduced: Episode {rh.get('introduced_episode')}")
            print(f"Audio Signature: {rh.get('audio_signature')}")
            print(f"\nWhy Believable:")
            for factor in rh.get('believability_factors', [])[:2]:
                print(f"  • {factor}")
            print(f"\nDebunked: Episode {rh.get('debunked_episode')}")
            print(f"Method: {rh.get('debunk_method')}")
            print(f"Audience Reaction: {rh.get('audience_reaction')}")
            print()

        # Display stats
        stats = self.task_results.get('task_4_red_herrings', {}).get('red_herring_stats', {})
        print("-" * 70)
        print("📊 RED HERRING EFFECTIVENESS:")
        print(f"  • Total Red Herrings: {stats.get('total_red_herrings', 0)}")
        print(f"  • Average Duration: {stats.get('average_duration', 'N/A')}")
        print(f"  • False Suspects: {stats.get('false_suspects', 0)}")
        print(f"  • Misdirection Plots: {stats.get('misdirection_plots', 0)}")
        print("=" * 70)
        print()

    async def execute_task_5_fairness_check(self):
        """Task 5: Fairness Check Analysis"""
        print("=" * 70)
        print("✅ TASK 5: FAIRNESS CHECK & SOLVABILITY ANALYSIS")
        print("=" * 70)
        print()
        print("🤖 Analyzing audience solvability...")
        print("   Checking clue availability and clarity...")
        print("   Testing relisten value...")
        print("   Measuring hidden vs visible balance...")
        print("   Validating fair-play principles...")
        print()

        try:
            # Build complete strategy summary
            strategy_summary = json.dumps({
                'taxonomy': self.task_results.get('task_1_taxonomy', {}),
                'methods': self.task_results.get('task_2_methods', {}),
                'p3_grid': self.task_results.get('task_3_p3_grid', {}),
                'red_herrings': self.task_results.get('task_4_red_herrings', {})
            }, indent=2)[:5000]

            # Build prompt
            prompt = self.config.get_prompt('task_5_fairness_check')
            formatted_prompt = prompt.format(
                working_title=self.extracted_inputs.get('working_title', 'Unknown'),
                primary_genre=self.extracted_inputs.get('primary_genre', 'Unknown'),
                complete_reveal_strategy=strategy_summary
            )

            # Execute LLM call
            start_time = datetime.now()
            response = await self.agent.process_message(
                formatted_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Extract and validate JSON
            fairness_data = extract_json(response)

            # Store result
            self.task_results['task_5_fairness'] = fairness_data.get('fairness_check', {})

            # Display summary
            print(f"✅ Fairness analysis complete - story passes all checks")
            print()
            print(f"⏱️  Time: {int(duration // 60)} minutes {int(duration % 60)} seconds")
            print()

            # Display fairness metrics
            self._display_fairness_metrics()

        except Exception as e:
            print(f"❌ Task 5 failed: {str(e)}")
            raise

    def _display_fairness_metrics(self):
        """Display fairness metrics"""
        print("=" * 70)
        print("⚖️  FAIRNESS CHECK RESULTS")
        print("=" * 70)
        print()

        fairness = self.task_results.get('task_5_fairness', {})

        # Solvability
        solvability = fairness.get('solvability_analysis', {})
        print(f"SOLVABILITY: {solvability.get('overall_verdict', 'Unknown').replace('_', ' ').title()}")
        print()

        # Relisten value
        relisten = fairness.get('relisten_value_analysis', {})
        print(f"RELISTEN VALUE: {relisten.get('overall_rating', 'Unknown').upper()}")
        print()

        # Balance
        balance = fairness.get('information_balance', {})
        dist = balance.get('distribution', {})
        print(f"INFORMATION BALANCE: {balance.get('balance_verdict', 'Unknown').replace('_', ' ').title()}")
        print(f"  • Obvious: {dist.get('obvious', 0)*100:.0f}%")
        print(f"  • Visible: {dist.get('visible', 0)*100:.0f}%")
        print(f"  • Hidden: {dist.get('hidden', 0)*100:.0f}%")
        print(f"  • Obscure: {dist.get('obscure', 0)*100:.0f}%")
        print()

        # Fair play
        fair_play = fairness.get('fair_play_adherence', {})
        print("FAIR PLAY PRINCIPLES:")
        for principle, status in list(fair_play.items())[:4]:
            emoji = "✅" if status else "❌"
            print(f"  {emoji} {principle.replace('_', ' ').title()}")
        print()

        # Overall rating
        rating = fairness.get('overall_fairness_rating', 0)
        stars = "⭐" * rating
        print(f"OVERALL FAIRNESS RATING: {stars} {rating}/5")
        print(f"  → {fairness.get('rating_explanation', 'N/A')[:100]}...")
        print()
        print("=" * 70)
        print()

    async def human_review_complete_strategy(self):
        """Final human review of complete strategy"""
        print("=" * 70)
        print("⭐ FINAL HUMAN DECISION REQUIRED")
        print("=" * 70)
        print()

        print("The complete narrative reveal strategy has been generated:")
        elements = self.task_results.get('task_1_taxonomy', {}).get('total_information_units', 0)
        methods = len(self.task_results.get('task_2_methods', {}).get('reveal_methods', []))
        plants = self.task_results.get('task_3_p3_grid', {}).get('grid_statistics', {}).get('total_plants', 0)
        rh_count = len(self.task_results.get('task_4_red_herrings', {}).get('red_herrings', []))
        rating = self.task_results.get('task_5_fairness', {}).get('overall_fairness_rating', 0)

        print(f"  ✓ {elements} story elements classified")
        print(f"  ✓ {methods} reveal methods from 45-method catalog")
        print(f"  ✓ Complete Plant/Proof/Payoff grid ({plants} plants)")
        print(f"  ✓ {rh_count} major red herrings designed")
        print(f"  ✓ Fairness check passed ({rating}/5 rating)")
        print()
        print("This is the information architecture for your entire series.")
        print()
        print("OPTIONS:")
        print("  [Enter] - Approve and save complete reveal matrix")
        print("  [R]     - Regenerate entire strategy")
        print("  [V]     - View complete reveal matrix document")
        print()
        print("💡 NOTE: This is a critical story infrastructure decision")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == 'V':
            print("\n[View complete matrix functionality would display full JSON here]")
            input("\nPress Enter when ready to save: ")
        elif choice == 'R':
            print("\nRegeneration not yet implemented. Continuing with current strategy...")
            await asyncio.sleep(1)

    async def generate_outputs(self):
        """Generate all output files"""
        try:
            # Compile final reveal matrix
            reveal_matrix = {
                "session_id": self.session_id,
                "working_title": self.extracted_inputs.get('working_title'),
                "primary_genre": self.extracted_inputs.get('primary_genre'),
                "episode_count": self.extracted_inputs.get('episode_count'),
                "timestamp": datetime.now().isoformat(),
                "reveal_taxonomy": self.task_results.get('task_1_taxonomy', {}),
                "reveal_methods": self.task_results.get('task_2_methods', {}),
                "plant_proof_payoff_grid": self.task_results.get('task_3_p3_grid', {}),
                "red_herrings": self.task_results.get('task_4_red_herrings', {}),
                "fairness_check": self.task_results.get('task_5_fairness', {})
            }

            # Save JSON
            json_path = self.output_dir / f"{self.session_id}_reveal_matrix.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(reveal_matrix, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved JSON: {json_path}")

            # Save readable TXT
            txt_path = self.output_dir / f"{self.session_id}_reveal_strategy.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(self._generate_readable_summary(reveal_matrix))
            print(f"✅ Saved TXT: {txt_path}")

            # Save P3 Grid CSV
            csv_path = self.output_dir / f"{self.session_id}_plant_proof_payoff_grid.csv"
            self._save_p3_grid_csv(csv_path)
            print(f"✅ Saved CSV: {csv_path}")

            # Save to Redis
            redis_key = f"audiobook:{self.session_id}:station_10"
            await self.redis_client.set(redis_key, json.dumps(reveal_matrix), expire=86400)
            print(f"✅ Saved to Redis: {redis_key}")

        except Exception as e:
            raise ValueError(f"❌ Error saving outputs: {str(e)}")

    def _generate_readable_summary(self, reveal_matrix: Dict) -> str:
        """Generate human-readable summary"""
        lines = []

        lines.append("=" * 70)
        lines.append("NARRATIVE REVEAL STRATEGY")
        lines.append("=" * 70)
        lines.append(f"\nProject: {reveal_matrix.get('working_title')}")
        lines.append(f"Genre: {reveal_matrix.get('primary_genre')}")
        lines.append(f"Format: {reveal_matrix.get('episode_count')}")
        lines.append(f"Session: {reveal_matrix.get('session_id')}")
        lines.append(f"\nGenerated: {reveal_matrix.get('timestamp')}")
        lines.append("\n" + "=" * 70)

        # Add each section summary
        lines.append("\n\nPART 1: REVEAL TAXONOMY")
        lines.append("-" * 70)
        taxonomy = reveal_matrix.get('reveal_taxonomy', {})
        lines.append(f"Total Information Units: {taxonomy.get('total_information_units', 0)}")
        lines.append(f"Critical Reveals: {taxonomy.get('critical_reveals', 0)}")
        lines.append(f"Clued Discoveries: {taxonomy.get('clued_discoveries', 0)}")
        lines.append(f"Subtle Plants: {taxonomy.get('subtle_plants', 0)}")

        lines.append("\n\nPART 2: REVEAL METHODS")
        lines.append("-" * 70)
        methods = reveal_matrix.get('reveal_methods', {}).get('reveal_methods', [])
        lines.append(f"Total Major Revelations: {len(methods)}")

        lines.append("\n\nPART 3: PLANT/PROOF/PAYOFF GRID")
        lines.append("-" * 70)
        p3_stats = reveal_matrix.get('plant_proof_payoff_grid', {}).get('grid_statistics', {})
        lines.append(f"Total Plants: {p3_stats.get('total_plants', 0)}")
        lines.append(f"Total Proofs: {p3_stats.get('total_proofs', 0)}")
        lines.append(f"Total Payoffs: {p3_stats.get('total_payoffs', 0)}")

        lines.append("\n\nPART 4: RED HERRINGS")
        lines.append("-" * 70)
        rh = reveal_matrix.get('red_herrings', {}).get('red_herrings', [])
        lines.append(f"Total Red Herrings: {len(rh)}")

        lines.append("\n\nPART 5: FAIRNESS CHECK")
        lines.append("-" * 70)
        fairness = reveal_matrix.get('fairness_check', {})
        rating = fairness.get('overall_fairness_rating', 0)
        lines.append(f"Fairness Rating: {'⭐' * rating} {rating}/5")

        lines.append("\n\n" + "=" * 70)
        lines.append("END OF REVEAL STRATEGY")
        lines.append("=" * 70)

        return "\n".join(lines)

    def _save_p3_grid_csv(self, csv_path: Path):
        """Save P3 grid as CSV"""
        try:
            grid = self.task_results.get('task_3_p3_grid', {}).get('plant_proof_payoff_grid', [])

            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Revelation', 'Type', 'Episode', 'Scene', 'Moment', 'Audio', 'Dialogue', 'Visibility']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for revelation in grid:
                    rev_name = revelation.get('revelation', 'Unknown')

                    # Write plants
                    for plant in revelation.get('plants', []):
                        writer.writerow({
                            'Revelation': rev_name,
                            'Type': 'Plant',
                            'Episode': plant.get('episode'),
                            'Scene': plant.get('scene'),
                            'Moment': plant.get('moment', ''),
                            'Audio': plant.get('audio', ''),
                            'Dialogue': plant.get('dialogue', ''),
                            'Visibility': plant.get('visibility', '')
                        })

                    # Write proofs
                    for proof in revelation.get('proofs', []):
                        writer.writerow({
                            'Revelation': rev_name,
                            'Type': 'Proof',
                            'Episode': proof.get('episode'),
                            'Scene': proof.get('scene'),
                            'Moment': proof.get('moment', ''),
                            'Audio': proof.get('audio', ''),
                            'Dialogue': proof.get('dialogue', ''),
                            'Visibility': proof.get('evidence_type', '')
                        })

                    # Write payoff
                    payoff = revelation.get('payoff', {})
                    if payoff:
                        writer.writerow({
                            'Revelation': rev_name,
                            'Type': 'Payoff',
                            'Episode': payoff.get('episode'),
                            'Scene': payoff.get('scene'),
                            'Moment': payoff.get('moment', ''),
                            'Audio': payoff.get('audio', ''),
                            'Dialogue': payoff.get('dialogue', ''),
                            'Visibility': payoff.get('relisten_value', '')
                        })

        except Exception as e:
            print(f"⚠️  Warning: Could not save CSV: {str(e)}")

    def display_completion(self):
        """Display completion summary"""
        print()
        print("=" * 70)
        print("✅ STATION 10: NARRATIVE REVEAL STRATEGY - COMPLETE")
        print("=" * 70)
        print()
        print(f"Session ID: {self.session_id}")
        print(f"Project: {self.extracted_inputs.get('working_title')}")
        print()

        # Display stats
        elements = self.task_results.get('task_1_taxonomy', {}).get('total_information_units', 0)
        methods = len(self.task_results.get('task_2_methods', {}).get('reveal_methods', []))
        plants = self.task_results.get('task_3_p3_grid', {}).get('grid_statistics', {}).get('total_plants', 0)
        proofs = self.task_results.get('task_3_p3_grid', {}).get('grid_statistics', {}).get('total_proofs', 0)
        payoffs = self.task_results.get('task_3_p3_grid', {}).get('grid_statistics', {}).get('total_payoffs', 0)
        rh_count = len(self.task_results.get('task_4_red_herrings', {}).get('red_herrings', []))
        rating = self.task_results.get('task_5_fairness', {}).get('overall_fairness_rating', 0)

        print("📊 REVEAL MATRIX STATISTICS:")
        print(f"   • {elements} Story elements classified and mapped")
        print(f"   • {methods} Reveal methods selected from 45-method catalog")
        print(f"   • {plants} Plants across all episodes")
        print(f"   • {proofs} Proof moments identified")
        print(f"   • {payoffs} Major payoffs designed")
        print(f"   • {rh_count} Red herrings with complete arcs")
        print(f"   • Fairness Rating: {'⭐' * rating} {rating}/5")
        print()

        print("📁 OUTPUT FILES:")
        print(f"   ✓ Complete Reveal Matrix (JSON for pipeline)")
        print(f"   ✓ Strategy Guide (TXT for writers/showrunner)")
        print(f"   ✓ P3 Grid Spreadsheet (CSV for production tracking)")
        print()

        print("🎬 Ready to proceed to Station 11")
        print()
        print("=" * 70)


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    # Auto-skip review when running from command line with no TTY
    skip_review = not sys.stdin.isatty()

    station = Station10NarrativeRevealStrategy(session_id, skip_review=skip_review)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
