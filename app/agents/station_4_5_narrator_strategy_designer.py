"""
Station 4.5: Narrator Strategy Designer

This station analyzes narrator requirements, generates with/without narrator sample scenes,
and provides a final strategy recommendation for human review.

Flow:
1. Load Station 4 data (references, tactics, seeds)
2. Extract required inputs from previous stations
3. Execute 5-task analysis sequence:
   - Task 1: Quantitative Analysis of Narrator Necessity
   - Task 2: Generate Comparative Sample Scenes
   - Task 3: Define Narrator Strategy Options
   - Task 4: Formulate Definitive Recommendation
   - Task 5: Assess Pipeline Impact
4. Save comprehensive report to JSON + TXT + Redis

Critical Decision Agent - Output requires Human Gate review
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json
from app.agents.title_validator import TitleValidator


class Station045NarratorStrategyDesigner:
    """Station 4.5: Narrator Strategy Designer"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=4, station_suffix="45")
        self.output_dir = Path("output/station_045")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()

    async def run(self):
        """Main execution method"""
        print("=" * 60)
        print("🎭 STATION 4.5: NARRATOR STRATEGY DESIGNER")
        print("=" * 60)
        print()

        try:
            # Load data from Station 4
            station4_data = await self.load_station4_data()
            
            # Extract required inputs from previous stations
            extracted_inputs = await self.extract_required_inputs()
            
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
            print("-" * 60)
            print()

            # Execute 5-task analysis sequence
            print("=" * 60)
            print("🔍 EXECUTING NARRATOR STRATEGY ANALYSIS")
            print("=" * 60)
            print()

            # Task 1: Quantitative Analysis
            print("📊 Task 1/5: Quantitative Analysis of Narrator Necessity...")
            quantitative_analysis = await self.execute_task1_quantitative_analysis(extracted_inputs)
            print("✅ Quantitative analysis complete")
            print()

            # Task 2: Sample Scenes
            print("🎬 Task 2/5: Generating Comparative Sample Scenes...")
            sample_scenes = await self.execute_task2_sample_scenes(extracted_inputs)
            print("✅ Sample scenes generated")
            print()

            # Task 3: Strategy Options
            print("⚙️ Task 3/5: Defining Narrator Strategy Options...")
            strategy_options = await self.execute_task3_strategy_options(extracted_inputs, quantitative_analysis)
            print("✅ Strategy options defined")
            print()

            # Task 4: Definitive Recommendation
            print("🎯 Task 4/5: Formulating Definitive Recommendation...")
            recommendation = await self.execute_task4_definitive_recommendation(
                extracted_inputs, quantitative_analysis, sample_scenes, strategy_options
            )
            print("✅ Definitive recommendation formulated")
            print()

            # Task 5: Pipeline Impact Assessment
            print("📈 Task 5/5: Assessing Pipeline Impact...")
            impact_assessment = await self.execute_task5_pipeline_impact(extracted_inputs, recommendation)
            print("✅ Pipeline impact assessed")
            print()

            # Compile final report
            final_report = await self.compile_final_report(
                extracted_inputs, quantitative_analysis, sample_scenes, 
                strategy_options, recommendation, impact_assessment
            )

            # Save outputs
            await self.save_outputs(final_report)

            print()
            print("=" * 60)
            print("✅ STATION 4.5 COMPLETE!")
            print("=" * 60)
            print()
            print(f"Session ID: {self.session_id}")
            print(f"Working Title: {extracted_inputs.get('working_title', 'N/A')}")
            print()
            print("📄 Output files:")
            print(f"   - output/station_045/{self.session_id}_output.json")
            print(f"   - output/station_045/{self.session_id}_readable.txt")
            print()
            print("🚪 CRITICAL DECISION AGENT - HUMAN GATE REVIEW REQUIRED")
            print("📌 Ready to proceed to Station 5")
            print()

        except Exception as e:
            print(f"❌ Station 4.5 failed: {str(e)}")
            raise

    async def load_station4_data(self) -> Dict:
        """Load Station 4 data from Redis"""
        try:
            station4_key = f"audiobook:{self.session_id}:station_04"
            station4_raw = await self.redis.get(station4_key)
            
            if not station4_raw:
                raise ValueError(f"❌ No Station 4 data found for session {self.session_id}\n   Please run Station 4 first")
            
            station4_data = json.loads(station4_raw)
            return station4_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 4 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 4 data: {str(e)}")

    async def extract_required_inputs(self) -> Dict:
        """Extract required inputs from previous stations"""
        try:
            # Load Station 1 data for story complexity, episode count, length
            station1_key = f"audiobook:{self.session_id}:station_01"
            station1_raw = await self.redis.get(station1_key)
            if not station1_raw:
                raise ValueError(f"❌ No Station 1 data found for session {self.session_id}")
            station1_data = json.loads(station1_raw)

            # Load Station 2 data for working title, core premise
            station2_key = f"audiobook:{self.session_id}:station_02"
            station2_raw = await self.redis.get(station2_key)
            if not station2_raw:
                raise ValueError(f"❌ No Station 2 data found for session {self.session_id}")
            station2_data = json.loads(station2_raw)

            # Load Station 3 data for genre and tone
            station3_key = f"audiobook:{self.session_id}:station_03"
            station3_raw = await self.redis.get(station3_key)
            if not station3_raw:
                raise ValueError(f"❌ No Station 3 data found for session {self.session_id}")
            station3_data = json.loads(station3_raw)

            # Extract required fields with error handling
            extracted = {}
            
            # From Station 1
            extracted['story_complexity'] = station1_data.get('story_complexity', 'Unknown')
            extracted['episode_count'] = station1_data.get('episode_count', 'Unknown')
            extracted['episode_length'] = station1_data.get('episode_length', 'Unknown')
            
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

            return extracted

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing station data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error extracting required inputs: {str(e)}")

    async def execute_task1_quantitative_analysis(self, inputs: Dict) -> Dict:
        """Task 1: Quantitative Analysis of Narrator Necessity"""
        try:
            prompt = self.config.get_prompt('quantitative_analysis').format(**inputs)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('quantitative_analysis', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_sample_scenes(self, inputs: Dict) -> Dict:
        """Task 2: Generate Comparative Sample Scenes"""
        try:
            prompt = self.config.get_prompt('sample_scenes_generation').format(**inputs)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('sample_scenes', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_strategy_options(self, inputs: Dict, analysis: Dict) -> Dict:
        """Task 3: Define Narrator Strategy Options"""
        try:
            # Only proceed if score is above 30
            total_score = analysis.get('total_score', 0)
            if isinstance(total_score, str):
                # Extract numeric score from string
                try:
                    total_score = int(total_score.split(':')[0].split('-')[-1])
                except:
                    total_score = 0
            
            if total_score <= 30:
                return {"narrator_strategy_options": {"note": "Score too low for detailed strategy analysis"}}
            
            prompt_context = {**inputs, 'analysis_score': total_score}
            prompt = self.config.get_prompt('narrator_strategy_options').format(**prompt_context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('narrator_strategy_options', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_definitive_recommendation(self, inputs: Dict, analysis: Dict, 
                                                     scenes: Dict, options: Dict) -> Dict:
        """Task 4: Formulate Definitive Recommendation"""
        try:
            prompt_context = {
                **inputs,
                'analysis_score': analysis.get('total_score', 0),
                'quantitative_analysis': json.dumps(analysis),
                'sample_scenes': json.dumps(scenes),
                'strategy_options': json.dumps(options)
            }
            
            prompt = self.config.get_prompt('definitive_recommendation').format(**prompt_context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('definitive_recommendation', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    async def execute_task5_pipeline_impact(self, inputs: Dict, recommendation: Dict) -> Dict:
        """Task 5: Assess Pipeline Impact"""
        try:
            prompt_context = {
                **inputs,
                'chosen_strategy': recommendation.get('recommendation', 'Unknown')
            }
            
            prompt = self.config.get_prompt('pipeline_impact_assessment').format(**prompt_context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('pipeline_impact_assessment', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 5 failed: {str(e)}")

    async def compile_final_report(self, inputs: Dict, analysis: Dict, scenes: Dict, 
                                 options: Dict, recommendation: Dict, impact: Dict) -> Dict:
        """Compile the final comprehensive report"""
        return {
            "Narrator Strategy Recommendation": {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "working_title": inputs.get('working_title', 'Unknown'),
                "executive_summary": self.generate_executive_summary(recommendation, analysis),
                "quantitative_analysis": analysis,
                "sample_scenes": scenes,
                "narrator_strategy_options": options,
                "definitive_recommendation": recommendation,
                "implementation_guidelines": recommendation.get('implementation_details', {}),
                "pipeline_impact_assessment": impact
            }
        }

    def generate_executive_summary(self, recommendation: Dict, analysis: Dict) -> str:
        """Generate executive summary paragraph"""
        rec_type = recommendation.get('recommendation', 'Unknown')
        justification = recommendation.get('justification', 'Analysis-based recommendation')
        score = analysis.get('total_score', 'Unknown')
        
        return f"Based on comprehensive analysis (score: {score}), this project is recommended for a {rec_type.lower()} approach. {justification}"

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
            self.save_readable_txt(txt_path, report)
            print(f"✅ Saved TXT: {txt_path}")

            # Save to Redis
            redis_key = f"audiobook:{self.session_id}:station_045"
            await self.redis.set(redis_key, json.dumps(report), expire=86400)
            print(f"✅ Saved to Redis: {redis_key}")

        except Exception as e:
            raise ValueError(f"❌ Error saving outputs: {str(e)}")

    def save_readable_txt(self, path: Path, data: Dict):
        """Save human-readable TXT file"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                report = data.get('Narrator Strategy Recommendation', {})
                
                f.write("=" * 70 + "\n")
                f.write("STATION 4.5: NARRATOR STRATEGY DESIGNER\n")
                f.write("=" * 70 + "\n\n")

                f.write(f"Session ID: {report.get('session_id', 'N/A')}\n")
                f.write(f"Working Title: {report.get('working_title', 'N/A')}\n")
                f.write(f"Generated: {report.get('timestamp', 'N/A')}\n")
                f.write("\n")

                # Executive Summary
                f.write("-" * 70 + "\n")
                f.write("EXECUTIVE SUMMARY\n")
                f.write("-" * 70 + "\n")
                f.write(f"{report.get('executive_summary', 'N/A')}\n\n")

                # Quantitative Analysis
                f.write("=" * 70 + "\n")
                f.write("QUANTITATIVE ANALYSIS\n")
                f.write("=" * 70 + "\n\n")
                
                analysis = report.get('quantitative_analysis', {})
                f.write(f"Total Score: {analysis.get('total_score', 'N/A')}\n")
                f.write(f"Classification: {analysis.get('classification', 'N/A')}\n\n")

                complexity = analysis.get('complexity_factors', {})
                f.write("COMPLEXITY FACTORS:\n")
                for factor, score in complexity.items():
                    f.write(f"  • {factor.replace('_', ' ').title()}: {score}/5\n")
                f.write("\n")

                audio_clarity = analysis.get('audio_clarity_factors', {})
                f.write("AUDIO CLARITY FACTORS:\n")
                for factor, score in audio_clarity.items():
                    f.write(f"  • {factor.replace('_', ' ').title()}: {score}/5\n")
                f.write("\n")

                stylistic = analysis.get('stylistic_factors', {})
                f.write("STYLISTIC FACTORS:\n")
                for factor, score in stylistic.items():
                    f.write(f"  • {factor.replace('_', ' ').title()}: {score}/5\n")
                f.write("\n")

                # Sample Scenes
                f.write("=" * 70 + "\n")
                f.write("COMPARATIVE SAMPLE SCENES\n")
                f.write("=" * 70 + "\n\n")
                
                scenes = report.get('sample_scenes', {})
                f.write(f"Scene Context: {scenes.get('scene_context', 'N/A')}\n\n")

                version_a = scenes.get('version_a_with_narrator', {})
                f.write("VERSION A (WITH NARRATOR):\n")
                f.write("-" * 70 + "\n")
                f.write(f"Title: {version_a.get('title', 'N/A')}\n\n")
                f.write(f"{version_a.get('content', 'N/A')}\n\n")

                version_b = scenes.get('version_b_without_narrator', {})
                f.write("VERSION B (WITHOUT NARRATOR):\n")
                f.write("-" * 70 + "\n")
                f.write(f"Title: {version_b.get('title', 'N/A')}\n\n")
                f.write(f"{version_b.get('content', 'N/A')}\n\n")

                # Definitive Recommendation
                f.write("=" * 70 + "\n")
                f.write("DEFINITIVE RECOMMENDATION\n")
                f.write("=" * 70 + "\n\n")
                
                recommendation = report.get('definitive_recommendation', {})
                f.write(f"Recommendation: {recommendation.get('recommendation', 'N/A')}\n\n")
                f.write(f"Justification:\n{recommendation.get('justification', 'N/A')}\n\n")

                implementation = recommendation.get('implementation_details', {})
                if implementation:
                    f.write("IMPLEMENTATION DETAILS:\n")
                    f.write("-" * 70 + "\n")
                    
                    if 'if_with_narrator' in implementation:
                        narrator_details = implementation['if_with_narrator']
                        f.write("WITH NARRATOR APPROACH:\n")
                        f.write(f"  Narrator Type: {narrator_details.get('narrator_type', 'N/A')}\n")
                        f.write(f"  Presence Level: {narrator_details.get('presence_level', 'N/A')}\n")
                        
                        voice_casting = narrator_details.get('voice_casting_notes', {})
                        f.write(f"  Voice Casting: {voice_casting.get('gender', 'N/A')}, {voice_casting.get('age_range', 'N/A')}, {voice_casting.get('voice_quality', 'N/A')}\n")
                        
                        f.write(f"  Key Functions: {', '.join(narrator_details.get('key_functions', []))}\n")
                        f.write("  Example Narrator Lines:\n")
                        for line in narrator_details.get('example_narrator_lines', []):
                            f.write(f"    • \"{line}\"\n")
                        f.write("\n")

                    elif 'if_without_narrator' in implementation:
                        no_narrator_details = implementation['if_without_narrator']
                        f.write("WITHOUT NARRATOR APPROACH:\n")
                        f.write(f"  Character Identification: {no_narrator_details.get('character_identification_strategy', 'N/A')}\n")
                        f.write(f"  Scene Transitions: {no_narrator_details.get('scene_transition_strategy', 'N/A')}\n")
                        f.write(f"  Exposition Delivery: {no_narrator_details.get('exposition_delivery_strategy', 'N/A')}\n")
                        f.write(f"  Internal Thoughts: {no_narrator_details.get('internal_thought_alternatives', 'N/A')}\n")
                        f.write(f"  Timeline Clarification: {no_narrator_details.get('timeline_clarification_strategy', 'N/A')}\n\n")

                    elif 'if_hybrid' in implementation:
                        hybrid_details = implementation['if_hybrid']
                        f.write("HYBRID APPROACH:\n")
                        f.write(f"  When Narrator Appears: {hybrid_details.get('when_narrator_appears', 'N/A')}\n")
                        f.write(f"  Presence Triggers: {hybrid_details.get('presence_triggers', 'N/A')}\n")
                        f.write(f"  Absence Justification: {hybrid_details.get('absence_justification', 'N/A')}\n")
                        f.write(f"  Implementation Guidelines: {hybrid_details.get('implementation_guidelines', 'N/A')}\n\n")

                # Pipeline Impact Assessment
                f.write("=" * 70 + "\n")
                f.write("PIPELINE IMPACT ASSESSMENT\n")
                f.write("=" * 70 + "\n\n")
                
                impact = report.get('pipeline_impact_assessment', {})
                
                episode_impact = impact.get('episode_structure_impact', {})
                f.write("EPISODE STRUCTURE IMPACT:\n")
                f.write(f"  Openings: {episode_impact.get('openings', 'N/A')}\n")
                f.write(f"  Scene Transitions: {episode_impact.get('scene_transitions', 'N/A')}\n")
                f.write(f"  Cliffhanger Delivery: {episode_impact.get('cliffhanger_delivery', 'N/A')}\n")
                f.write(f"  Runtime Allocation: {episode_impact.get('runtime_allocation', 'N/A')}\n\n")

                writing_impact = impact.get('writing_style_impact', {})
                f.write("WRITING STYLE IMPACT:\n")
                f.write(f"  Dialogue Naturalism: {writing_impact.get('dialogue_naturalism', 'N/A')}\n")
                f.write(f"  Sound Design Complexity: {writing_impact.get('sound_design_complexity', 'N/A')}\n")
                f.write(f"  Character Voice Burden: {writing_impact.get('character_voice_burden', 'N/A')}\n")
                f.write(f"  Pacing Control: {writing_impact.get('pacing_control', 'N/A')}\n\n")

                production_impact = impact.get('production_impact', {})
                f.write("PRODUCTION IMPACT:\n")
                f.write(f"  Additional Casting: {production_impact.get('additional_casting', 'N/A')}\n")
                f.write(f"  Recording Logistics: {production_impact.get('recording_logistics', 'N/A')}\n")
                f.write(f"  Edit Complexity: {production_impact.get('edit_complexity', 'N/A')}\n")
                f.write(f"  Budget Implications: {production_impact.get('budget_implications', 'N/A')}\n\n")

                audience_impact = impact.get('audience_experience_impact', {})
                f.write("AUDIENCE EXPERIENCE IMPACT:\n")
                f.write(f"  Intimacy vs Distance: {audience_impact.get('intimacy_vs_distance', 'N/A')}\n")
                f.write(f"  Clarity vs Discovery: {audience_impact.get('clarity_vs_discovery', 'N/A')}\n")
                f.write(f"  Guided vs Independent: {audience_impact.get('guided_vs_independent', 'N/A')}\n")
                f.write(f"  Cognitive Load: {audience_impact.get('cognitive_load', 'N/A')}\n\n")

                f.write("=" * 70 + "\n")
                f.write("END OF STATION 4.5 OUTPUT\n")
                f.write("=" * 70 + "\n")

        except Exception as e:
            raise ValueError(f"❌ Error saving readable TXT: {str(e)}")


async def main():
    """Main entry point"""
    session_id = input("📋 Enter session ID from previous stations: ").strip()
    if not session_id:
        print("❌ Session ID is required")
        return

    station = Station045NarratorStrategyDesigner(session_id)
    await station.initialize()
    await station.run()


if __name__ == "__main__":
    asyncio.run(main())
