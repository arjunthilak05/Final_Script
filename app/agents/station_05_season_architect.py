"""
Station 5: Season Architect

This station designs the complete season structure for an audiobook based on the provided project foundation.
It analyzes screenplay styles, recommends top 3 styles, creates season skeleton, and maps rhythm patterns.

Flow:
1. Load Station 4.5 data (narrator strategy recommendation)
2. Extract required inputs from previous stations
3. Execute season architecture analysis:
   - Style Selection (top 3 from 48 screenplay styles)
   - Season Skeleton (macro and micro structure)
   - Rhythm Mapping (tension peaks, breathing room, etc.)
4. Save comprehensive season structure document

Critical Architecture Agent - Output guides all subsequent creative decisions
"""

import asyncio
import json
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json
from app.agents.title_validator import TitleValidator


class Station05SeasonArchitect:
    """Station 5: Season Architect"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.config = load_station_config(station_number=5)
        self.output_dir = Path("output/station_05")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🏗️ STATION 5: SEASON ARCHITECT")
        print("=" * 60)
        print()

        try:
            # Load data from Station 4.5
            station45_data = await self.load_station45_data()
            
            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs()
            
            # --- START CRITICAL VALIDATION ---
            episode_count = extracted_inputs.get('episode_count', 'Unknown')
            episode_length = extracted_inputs.get('episode_length', 'Unknown')

            if episode_count == 'Unknown' or episode_length == 'Unknown' or not episode_count:
                error_msg = (
                    "❌ CRITICAL ERROR: Cannot build season architecture. "
                    f"Episode Count ('{episode_count}') or Episode Length ('{episode_length}') is undefined. "
                    "This value is expected from Station 1's 'option_details'."
                )
                print(error_msg)
                raise ValueError(error_msg)
            
            print("✅ Critical data validated (Episode Count, Episode Length)")
            # --- END CRITICAL VALIDATION ---
            
            print("✅ Data loaded successfully")
            print()
            print("-" * 60)
            print("📊 PROJECT SUMMARY")
            print("-" * 60)
            print(f"Working Title: {extracted_inputs.get('working_title', 'N/A')}")
            print(f"Primary Genre: {extracted_inputs.get('primary_genre', 'N/A')}")
            print(f"Target Age: {extracted_inputs.get('target_age', 'N/A')}")
            print(f"Episode Count: {extracted_inputs.get('episode_count', 'N/A')}")
            print(f"Episode Length: {extracted_inputs.get('episode_length', 'N/A')}")
            print(f"Narrator Strategy: {extracted_inputs.get('narrator_strategy', 'N/A')}")
            print("-" * 60)
            print()

            # Build the comprehensive LLM prompt
            print("🏗️ Building Season Architecture Prompt...")
            prompt = await self.build_season_architecture_prompt(extracted_inputs, station45_data)
            print("✅ Prompt built successfully")
            print()

            # Execute the season architecture analysis
            print("=" * 60)
            print("🎯 EXECUTING SEASON ARCHITECTURE ANALYSIS")
            print("=" * 60)
            print()

            print("📝 Sending request to LLM...")
            response = await self.agent.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            print("✅ LLM response received")
            print()

            # Process the response
            print("🔍 Processing LLM response...")
            season_structure_data = extract_json(response)
            
            if not season_structure_data:
                raise ValueError("❌ Failed to extract valid JSON from LLM response")

            # Generate human-readable summary
            print("📄 Generating human-readable summary...")
            readable_summary = await self.generate_readable_summary(season_structure_data, extracted_inputs)
            print("✅ Summary generated")
            print()

            # Compile final report
            final_report = await self.compile_final_report(
                extracted_inputs, season_structure_data, readable_summary
            )

            # Save outputs
            await self.save_outputs(final_report)

            print()
            print("=" * 60)
            print("✅ STATION 5 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Session ID: {self.session_id}")
            title = extracted_inputs.get('working_title', 'N/A')
            print(TitleValidator.format_title_for_display(title, "Station 5"))
            print()
            print("📄 Output files:")
            print(f"   - output/station_05/{self.session_id}_output.json")
            print(f"   - output/station_05/{self.session_id}_readable.txt")
            print()
            print("🏗️ SEASON ARCHITECTURE COMPLETE")
            print("📌 Ready to proceed to Station 6")
            print()

        except Exception as e:
            print(f"❌ Station 5 failed: {str(e)}")
            logging.error(f"Station 5 error: {str(e)}")
            raise

    async def load_station45_data(self) -> Dict:
        """Load Station 4.5 data from Redis"""
        try:
            station45_key = f"audiobook:{self.session_id}:station_045"
            station45_raw = await self.redis_client.get(station45_key)
            
            if not station45_raw:
                raise ValueError(f"❌ No Station 4.5 data found for session {self.session_id}\n   Please run Station 4.5 first")
            
            station45_data = json.loads(station45_raw)
            return station45_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 4.5 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 4.5 data: {str(e)}")

    async def extract_required_inputs(self) -> Dict:
        """Extract required inputs from previous stations"""
        try:
            # Load Station 1 data for story complexity, episode count, length
            station1_key = f"audiobook:{self.session_id}:station_01"
            station1_raw = await self.redis_client.get(station1_key)
            if not station1_raw:
                raise ValueError(f"❌ No Station 1 data found for session {self.session_id}")
            station1_data = json.loads(station1_raw)

            # Load Station 2 data for working title, core premise
            station2_key = f"audiobook:{self.session_id}:station_02"
            station2_raw = await self.redis_client.get(station2_key)
            if not station2_raw:
                raise ValueError(f"❌ No Station 2 data found for session {self.session_id}")
            station2_data = json.loads(station2_raw)

            # Load Station 3 data for genre and tone
            station3_key = f"audiobook:{self.session_id}:station_03"
            station3_raw = await self.redis_client.get(station3_key)
            if not station3_raw:
                raise ValueError(f"❌ No Station 3 data found for session {self.session_id}")
            station3_data = json.loads(station3_raw)

            # Load Station 4.5 data for narrator strategy
            station45_data = await self.load_station45_data()

            # Extract required fields with error handling
            extracted = {}
            
            # From Station 1
            station1_options = station1_data.get('option_details', {})
            extracted['story_complexity'] = station1_data.get('story_complexity', 'Unknown')
            extracted['episode_count'] = station1_options.get('episode_count', 'Unknown')
            extracted['episode_length'] = station1_options.get('episode_length', 'Unknown')
            
            # Use bulletproof title extraction
            extracted['working_title'] = TitleValidator.extract_bulletproof_title(station1_data, station2_data)
            extracted['core_premise'] = station2_data.get('world_setting', {}).get('core_premise', 'Unknown')
            
            # From Station 3
            chosen_blend = station3_data.get('chosen_blend_details', {})
            extracted['primary_genre'] = chosen_blend.get('primary_genre', 'Unknown')
            
            age_guidelines = station3_data.get('age_guidelines', {})
            extracted['target_age'] = age_guidelines.get('target_age_range', 'Unknown')
            
            tone_calibration = station3_data.get('tone_calibration', {})
            extracted['tone'] = tone_calibration.get('light_dark_balance', 'Balanced')

            # From Station 4.5
            narrator_recommendation = station45_data.get('Narrator Strategy Recommendation', {})
            definitive_rec = narrator_recommendation.get('definitive_recommendation', {})
            extracted['narrator_strategy'] = definitive_rec.get('recommendation', 'Unknown')

            return extracted

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing station data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error extracting required inputs: {str(e)}")

    async def build_season_architecture_prompt(self, inputs: Dict, station45_data: Dict) -> str:
        """Build the comprehensive season architecture prompt"""
        try:
            # Get the base prompt from config
            base_prompt = self.config.get_prompt('season_architecture_analysis')
            
            # Format the prompt with project data
            formatted_prompt = base_prompt.format(
                working_title=inputs.get('working_title', 'Unknown'),
                primary_genre=inputs.get('primary_genre', 'Unknown'),
                target_age=inputs.get('target_age', 'Unknown'),
                episode_count=inputs.get('episode_count', 'Unknown'),
                episode_length=inputs.get('episode_length', 'Unknown'),
                story_complexity=inputs.get('story_complexity', 'Unknown'),
                tone=inputs.get('tone', 'Balanced'),
                narrator_strategy=inputs.get('narrator_strategy', 'Unknown'),
                core_premise=inputs.get('core_premise', 'Unknown')
            )
            
            return formatted_prompt
            
        except Exception as e:
            raise ValueError(f"❌ Error building prompt: {str(e)}")

    async def generate_readable_summary(self, season_data: Dict, inputs: Dict) -> str:
        """Generate human-readable summary from structured JSON data"""
        try:
            summary_parts = []
            
            # Header
            summary_parts.append("=" * 70)
            summary_parts.append("STATION 5: SEASON ARCHITECT")
            summary_parts.append("=" * 70)
            summary_parts.append("")
            summary_parts.append(f"Working Title: {inputs.get('working_title', 'N/A')}")
            summary_parts.append(f"Primary Genre: {inputs.get('primary_genre', 'N/A')}")
            summary_parts.append(f"Target Age: {inputs.get('target_age', 'N/A')}")
            summary_parts.append(f"Episode Count: {inputs.get('episode_count', 'N/A')}")
            summary_parts.append(f"Episode Length: {inputs.get('episode_length', 'N/A')}")
            summary_parts.append(f"Narrator Strategy: {inputs.get('narrator_strategy', 'N/A')}")
            summary_parts.append("")
            
            # Style Recommendations
            style_recs = season_data.get('season_structure_document', {}).get('style_recommendations', [])
            if style_recs:
                summary_parts.append("-" * 70)
                summary_parts.append("STYLE RECOMMENDATIONS")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                for i, style in enumerate(style_recs[:3], 1):
                    summary_parts.append(f"{i}. {style.get('style_name', 'Unknown Style')}")
                    summary_parts.append(f"   Justification: {style.get('justification', 'N/A')}")
                    summary_parts.append(f"   Audio Application: {style.get('audio_application', 'N/A')}")
                    summary_parts.append(f"   Structure Implications: {style.get('structure_implications', 'N/A')}")
                    summary_parts.append("")
            
            # Season Skeleton
            skeleton = season_data.get('season_structure_document', {}).get('season_skeleton', {})
            if skeleton:
                summary_parts.append("-" * 70)
                summary_parts.append("SEASON SKELETON")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                macro_structure = skeleton.get('macro_structure', {})
                if macro_structure:
                    summary_parts.append("MACRO STRUCTURE:")
                    for act, episodes in macro_structure.items():
                        summary_parts.append(f"  {act}: {episodes}")
                    summary_parts.append("")
                
                episode_grid = skeleton.get('episode_grid', [])
                if episode_grid:
                    summary_parts.append("EPISODE GRID:")
                    for episode in episode_grid[:10]:  # Show first 10 episodes
                        ep_num = episode.get('episode_number', 'N/A')
                        function = episode.get('primary_function', 'N/A')
                        energy = episode.get('energy_level', 'N/A')
                        subplot = episode.get('subplot_focus', 'N/A')
                        cliffhanger = episode.get('cliffhanger_type', 'N/A')
                        summary_parts.append(f"  Episode {ep_num}: {function} (Energy: {energy}, Subplot: {subplot}, Cliffhanger: {cliffhanger})")
                    if len(episode_grid) > 10:
                        summary_parts.append(f"  ... and {len(episode_grid) - 10} more episodes")
                    summary_parts.append("")
            
            # Rhythm Mapping
            rhythm = season_data.get('season_structure_document', {}).get('rhythm_mapping', {})
            if rhythm:
                summary_parts.append("-" * 70)
                summary_parts.append("RHYTHM MAPPING")
                summary_parts.append("-" * 70)
                summary_parts.append("")
                
                tension_peaks = rhythm.get('tension_peaks', [])
                if tension_peaks:
                    summary_parts.append(f"Tension Peaks: Episodes {', '.join(map(str, tension_peaks))}")
                
                breathing_room = rhythm.get('breathing_room', [])
                if breathing_room:
                    summary_parts.append(f"Breathing Room: Episodes {', '.join(map(str, breathing_room))}")
                
                format_breaks = rhythm.get('format_breaks', [])
                if format_breaks:
                    summary_parts.append(f"Format Breaks: Episodes {', '.join(map(str, format_breaks))}")
                
                revelation_cascade = rhythm.get('revelation_cascade', [])
                if revelation_cascade:
                    summary_parts.append(f"Revelation Cascade: Episodes {', '.join(map(str, revelation_cascade))}")
                summary_parts.append("")
            
            summary_parts.append("=" * 70)
            summary_parts.append("END OF SEASON ARCHITECTURE")
            summary_parts.append("=" * 70)
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            raise ValueError(f"❌ Error generating readable summary: {str(e)}")

    async def compile_final_report(self, inputs: Dict, season_data: Dict, readable_summary: str) -> Dict:
        """Compile the final comprehensive report"""
        return {
            "Season Architecture Document": {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "working_title": inputs.get('working_title', 'Unknown'),
                "primary_genre": inputs.get('primary_genre', 'Unknown'),
                "target_age": inputs.get('target_age', 'Unknown'),
                "episode_count": inputs.get('episode_count', 'Unknown'),
                "episode_length": inputs.get('episode_length', 'Unknown'),
                "narrator_strategy": inputs.get('narrator_strategy', 'Unknown'),
                "season_structure_document": season_data.get('season_structure_document', {}),
                "readable_summary": readable_summary
            }
        }

    async def save_outputs(self, report: Dict):
        """Save all output files (JSON + TXT + Redis)"""
        try:
            # Save JSON
            json_path = self.output_dir / f"{self.session_id}_output.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved JSON: {json_path}")

            # Save TXT
            txt_path = self.output_dir / f"{self.session_id}_readable.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(report['Season Architecture Document']['readable_summary'])
            print(f"✅ Saved TXT: {txt_path}")

            # Save to Redis
            redis_key = f"audiobook:{self.session_id}:station_05"
            await self.redis_client.set(redis_key, json.dumps(report), expire=86400)
            print(f"✅ Saved to Redis: {redis_key}")

        except Exception as e:
            raise ValueError(f"❌ Error saving outputs: {str(e)}")


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station05SeasonArchitect(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
