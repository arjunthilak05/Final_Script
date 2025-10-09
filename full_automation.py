#!/usr/bin/env python3
"""
Full End-to-End Automation for Audiobook Production System

Complete automated pipeline: Station 1 → Station 2 → Station 3 → Station 4 → Station 4.5
With session management, progress tracking, and error handling.
"""

import asyncio
import sys
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, TypedDict
from dataclasses import asdict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / "app"))

# Import all station processors
from app.agents.station_01_seed_processor import Station01SeedProcessor
from app.agents.station_02_project_dna_builder import Station02ProjectDNABuilder  
from app.agents.station_03_age_genre_optimizer import Station03AgeGenreOptimizer
from app.agents.station_04_reference_miner import Station04ReferenceMiner
from app.agents.station_04_5_narrator_strategy import Station045NarratorStrategy
from app.agents.station_05_season_architecture import Station05SeasonArchitect
from app.agents.station_06_master_style_guide import Station06MasterStyleGuideBuilder
from app.agents.station_07_reality_check import Station07RealityCheck
from app.agents.station_08_character_architecture import Station08CharacterArchitecture
from app.agents.station_09_world_building import Station09WorldBuilding
from app.agents.station_10_narrative_reveal_strategy import Station10NarrativeRevealStrategy
from app.agents.station_11_runtime_planning import Station11RuntimePlanning
from app.agents.station_12_hook_cliffhanger import Station12HookCliffhanger
from app.agents.station_13_multiworld_timeline import Station13MultiworldTimeline
from app.agents.station_14_episode_blueprint import Station14EpisodeBlueprint
from app.agents.station_15_detailed_episode_outlining import Station15DetailedEpisodeOutlining
from app.agents.station_16_canon_check import Station16CanonCheck
from app.agents.station_17_dialect_planning import Station17DialectPlanning
from app.agents.station_18_evergreen_check import Station18EvergreenCheck
from app.agents.station_19_procedure_check import Station19ProcedureCheck
from app.agents.station_20_geography_transit import Station20GeographyTransit
from app.redis_client import RedisClient


class AudiobookProductionState:
    """State management for the full production pipeline"""
    
    def __init__(self, story_concept: str):
        self.story_concept = story_concept
        self.session_id = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_station = 0
        self.station_outputs = {}
        self.chosen_scale = None
        self.chosen_genre_blend = None
        self.generated_files = []
        self.errors = []
        
    def to_dict(self):
        """Convert state to dictionary for storage"""
        return {
            "story_concept": self.story_concept,
            "session_id": self.session_id,
            "current_station": self.current_station,
            "station_outputs": self.station_outputs,
            "chosen_scale": self.chosen_scale,
            "chosen_genre_blend": self.chosen_genre_blend,
            "generated_files": self.generated_files,
            "errors": self.errors
        }


class FullAutomationRunner:
    """Complete automation runner for all stations"""
    
    def __init__(self, auto_approve: bool = True, debug_mode: bool = False):
        self.auto_approve = auto_approve
        self.debug_mode = debug_mode
        self.progress_callback = None
        self.retry_attempts = 3
        self.checkpoint_enabled = True
        self.redis = None
        self.current_session_id = None  # Track current session for resume
        
    def set_progress_callback(self, callback):
        """Set callback function for progress updates"""
        self.progress_callback = callback
        
    def emit_progress(self, station: str, percentage: int, message: str = ""):
        """Emit progress update"""
        progress_info = {
            'station': station,
            'percentage': percentage, 
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if self.progress_callback:
            self.progress_callback(progress_info)
        else:
            print(f"🔄 {station}: {percentage}% - {message}")
            
    async def run_full_automation(self, story_concept: str) -> Dict[str, Any]:
        """Run the complete automation pipeline"""
        
        print("🚀 STARTING FULL AUDIOBOOK PRODUCTION AUTOMATION")
        print("=" * 70)
        print(f"📝 Story Concept: {story_concept[:100]}...")
        print(f"🎯 Mode: {'Auto-approve' if self.auto_approve else 'Interactive'}")
        print(f"🐛 Debug: {'Enabled' if self.debug_mode else 'Disabled'}")
        print(f"🏭 Pipeline: Station 1 → 2 → 3 → 4 → 4.5 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18 → 19 → 20")
        print()
        
        # Initialize state
        state = AudiobookProductionState(story_concept)
        self.current_session_id = state.session_id  # Track for interruption handling

        try:
            # Station 1: Seed Processing & Scale Evaluation
            state = await self._run_station_1(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 2: Project DNA Building
            state = await self._run_station_2(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 3: Age & Genre Optimization
            state = await self._run_station_3(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 4: Reference Mining & Seed Extraction
            state = await self._run_station_4(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 4.5: Narrator Strategy Designer
            state = await self._run_station_4_5(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 5: Season Architecture
            state = await self._run_station_5(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 6: Master Style Guide
            state = await self._run_station_6(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 7: Reality Check
            state = await self._run_station_7(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 8: Character Architecture
            state = await self._run_station_8(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 9: World Building
            state = await self._run_station_9(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 10: Placeholder (Future Implementation)
            state = await self._run_station_10(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 11: Placeholder (Future Implementation)
            state = await self._run_station_11(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 12: Hook & Cliffhanger Designer
            state = await self._run_station_12(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 13: Multi-World/Timeline Manager
            state = await self._run_station_13(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 14: Simple Episode Blueprint
            state = await self._run_station_14(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 15: Detailed Episode Outlining
            state = await self._run_station_15(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 16: Canon Check (Validation Suite)
            state = await self._run_station_16(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 17: Dialect Planning
            state = await self._run_station_17(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 18: Evergreen Check
            state = await self._run_station_18(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 19: Procedure Check
            state = await self._run_station_19(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Station 20: Geography/Transit Check
            state = await self._run_station_20(state)
            if self.checkpoint_enabled:
                await self._save_checkpoint(state)

            # Generate final summary
            await self._generate_final_summary(state)
            
            print("\n🎉 FULL AUTOMATION COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            
            return {
                "success": True,
                "session_id": state.session_id,
                "outputs": state.station_outputs,
                "files": state.generated_files,
                "summary": "All 20 stations completed successfully (including validation suite)"
            }
            
        except Exception as e:
            logger.error(f"Automation failed: {str(e)}")
            state.errors.append(str(e))
            
            return {
                "success": False,
                "session_id": state.session_id,
                "error": str(e),
                "completed_stations": state.current_station,
                "outputs": state.station_outputs
            }
    
    async def _run_station_1(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 1: Seed Processing & Scale Evaluation"""
        
        self.emit_progress("Station 1", 0, "Initializing Seed Processor...")
        
        try:
            processor = Station01SeedProcessor()
            await processor.initialize()
            
            if self.debug_mode:
                processor.debug_mode = True
                
            self.emit_progress("Station 1", 20, "Processing story concept...")
            
            # Process the story concept
            result = await processor.process(state.story_concept, state.session_id)
            
            self.emit_progress("Station 1", 70, "Analyzing scale options...")
            
            # Store Station 1 output
            state.station_outputs["station_1"] = {
                "original_seed": result.original_seed,
                "scale_options": [asdict(opt) for opt in result.scale_options],
                "recommended_option": result.recommended_option,
                "initial_expansion": asdict(result.initial_expansion),
                "processing_timestamp": result.processing_timestamp.isoformat(),
                "session_id": result.session_id
            }
            
            # Auto-select or get user choice for scale
            if self.auto_approve:
                state.chosen_scale = result.recommended_option
                self.emit_progress("Station 1", 90, f"Auto-selected Option {state.chosen_scale}")
            else:
                state.chosen_scale = await self._get_user_scale_choice(result)
                
            self.emit_progress("Station 1", 100, "Station 1 completed successfully!")
            state.current_station = 1
            
            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "01", state.station_outputs["station_1"])
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 1 failed: {str(e)}")
    
    async def _run_station_2(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 2: Project DNA Building"""
        
        self.emit_progress("Station 2", 0, "Initializing Project DNA Builder...")
        
        try:
            processor = Station02ProjectDNABuilder()
            await processor.initialize()
            
            self.emit_progress("Station 2", 20, "Building Project Bible...")
            
            # Process with Station 1 output data
            result = await processor.process(state.station_outputs["station_1"], state.session_id)
            
            self.emit_progress("Station 2", 80, "Finalizing Project Bible...")
            
            # Store Station 2 output
            state.station_outputs["station_2"] = {
                "working_title": result.working_title,
                "world_setting": asdict(result.world_setting),
                "format_specifications": asdict(result.format_specifications),
                "genre_tone": asdict(result.genre_tone),
                "audience_profile": asdict(result.audience_profile),
                "production_constraints": asdict(result.production_constraints),
                "creative_promises": asdict(result.creative_promises),
                "creative_team": asdict(result.creative_team),
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat()
            }
            
            self.emit_progress("Station 2", 100, "Station 2 completed successfully!")
            state.current_station = 2
            
            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "02", state.station_outputs["station_2"])
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 2 failed: {str(e)}")
    
    async def _run_station_3(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 3: Age & Genre Optimization"""
        
        self.emit_progress("Station 3", 0, "Initializing Age & Genre Optimizer...")
        
        try:
            processor = Station03AgeGenreOptimizer()
            await processor.initialize()
            
            self.emit_progress("Station 3", 20, "Analyzing age appropriateness...")
            
            # Process Station 2 output
            result = await processor.process(state.station_outputs["station_2"], state.session_id)
            
            self.emit_progress("Station 3", 60, "Optimizing genre blend...")
            
            # Store Station 3 output
            state.station_outputs["station_3"] = {
                "working_title": result.working_title,
                "age_guidelines": asdict(result.age_guidelines),
                "genre_options": [asdict(opt) for opt in result.genre_options],
                "chosen_genre_blend": result.chosen_genre_blend,
                "tone_calibration": asdict(result.tone_calibration),
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat()
            }
            
            # Auto-select or get user choice for genre blend
            if self.auto_approve:
                state.chosen_genre_blend = result.chosen_genre_blend
                self.emit_progress("Station 3", 90, f"Auto-selected genre blend: {state.chosen_genre_blend}")
            else:
                state.chosen_genre_blend = await self._get_user_genre_choice(result)
                
            self.emit_progress("Station 3", 100, "Station 3 completed successfully!")
            state.current_station = 3
            
            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "03", state.station_outputs["station_3"])
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 3 failed: {str(e)}")
    
    async def _run_station_4(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 4: Reference Mining & Seed Extraction"""
        
        self.emit_progress("Station 4", 0, "Initializing Reference Miner...")
        
        try:
            processor = Station04ReferenceMiner()
            await processor.initialize()
            
            if self.debug_mode:
                processor.enable_debug_mode()
                
            self.emit_progress("Station 4", 10, "Gathering cross-media references...")
            
            # Process Station 3 output to generate seed bank
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 4", 50, "Extracting storytelling tactics...")
            self.emit_progress("Station 4", 80, "Generating story seeds...")
            
            # Store Station 4 output
            total_seeds = processor._count_total_seeds(result.seed_collection)
            state.station_outputs["station_4"] = {
                "working_title": result.working_title,
                "total_references": len(result.references),
                "total_extractions": len(result.tactical_extractions),
                "total_seeds": total_seeds,
                "seed_collection": {
                    "micro_moments": len(result.seed_collection.micro_moments),
                    "episode_beats": len(result.seed_collection.episode_beats),
                    "season_arcs": len(result.seed_collection.season_arcs),
                    "series_defining": len(result.seed_collection.series_defining)
                },
                "quality_metrics": result.quality_metrics,
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat()
            }
            
            
            self.emit_progress("Station 4", 100, f"Station 4 completed! Generated {total_seeds} seeds")
            state.current_station = 4
            
            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "04", state.station_outputs["station_4"])
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 4 failed: {str(e)}")
    
    async def _run_station_4_5(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 4.5: Narrator Strategy Designer"""
        
        self.emit_progress("Station 4.5", 0, "Initializing Narrator Strategy Designer...")
        
        try:
            processor = Station045NarratorStrategy()
            await processor.initialize()
            
            if self.debug_mode:
                processor.enable_debug_mode()
                
            self.emit_progress("Station 4.5", 20, "Analyzing story complexity...")
            
            # Process Station 4 output to determine narrator strategy
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 4.5", 60, "Generating sample scenes...")
            self.emit_progress("Station 4.5", 80, "Creating narrator recommendation...")
            
            # Store Station 4.5 output
            state.station_outputs["station_4_5"] = {
                "working_title": result.working_title,
                "recommendation": result.recommendation.value,
                "executive_summary": result.executive_summary,
                "complexity_score": result.complexity_analysis.total_score,
                "sample_scenes_count": len(result.sample_scenes),
                "narrator_strategy": asdict(result.narrator_strategy) if result.narrator_strategy else None,
                "alternative_strategy": asdict(result.alternative_strategy) if result.alternative_strategy else None,
                "production_impact": asdict(result.production_impact),
                "implementation_guidelines": result.implementation_guidelines,
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat()
            }
            
                
            # Export strategy document as text backup
            try:
                export_filename = f"outputs/station45_narrator_strategy_{state.session_id}.txt"
                
                with open(export_filename, 'w', encoding='utf-8') as f:
                    f.write("STATION 4.5: NARRATOR STRATEGY RECOMMENDATION\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Project: {result.working_title}\n")
                    f.write(f"Session: {state.session_id}\n")
                    f.write(f"Generated: {result.created_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    f.write("RECOMMENDATION:\n")
                    f.write(f"{result.recommendation.value}\n\n")
                    
                    f.write("EXECUTIVE SUMMARY:\n")
                    f.write(f"{result.executive_summary}\n\n")
                    
                    f.write("COMPLEXITY ANALYSIS:\n")
                    f.write(f"Total Score: {result.complexity_analysis.total_score}/75\n")
                    f.write(f"Tier: {result.complexity_analysis.recommendation_tier}\n\n")
                    
                    if result.narrator_strategy:
                        f.write("NARRATOR STRATEGY:\n")
                        f.write(f"Type: {result.narrator_strategy.identity_type.value}\n")
                        f.write(f"Presence: {result.narrator_strategy.presence_level.value}\n")
                        f.write(f"Functions: {', '.join(result.narrator_strategy.key_functions)}\n")
                        f.write(f"Casting: {result.narrator_strategy.voice_casting_notes}\n\n")
                    
                    f.write("PRODUCTION IMPACT:\n")
                    f.write(f"Budget: {result.production_impact.budget_implications}\n")
                    f.write(f"Schedule: {result.production_impact.schedule_changes}\n\n")
                
                state.generated_files.append(export_filename)
            except Exception as e:
                logger.warning(f"Text export failed: {e}")
            
            self.emit_progress("Station 4.5", 100, f"Station 4.5 completed! Recommendation: {result.recommendation.value}")
            state.current_station = 4.5
            
            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "04.5", state.station_outputs["station_4_5"])
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 4.5 failed: {str(e)}")
    
    async def _run_station_5(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 5: Season Architecture"""
        
        self.emit_progress("Station 5", 0, "Initializing Season Architect...")
        
        try:
            processor = Station05SeasonArchitect()
            await processor.initialize()
                
            self.emit_progress("Station 5", 10, "Analyzing 48 screenplay styles...")
            
            # Process season architecture
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 5", 40, "Selecting optimal screenplay style...")
            self.emit_progress("Station 5", 60, "Creating season structure...")
            self.emit_progress("Station 5", 80, "Mapping rhythm and pacing...")
            
            # Store Station 5 output with COMPLETE structure for downstream stations
            from dataclasses import asdict

            # Convert episode_grid to list of dicts
            episode_grid_list = [asdict(ep) for ep in result.episode_grid]

            state.station_outputs["station_5"] = {
                "working_title": result.working_title,
                "chosen_style": result.chosen_style,
                "total_episodes": result.macro_structure.total_episodes,
                "confidence_score": result.style_recommendations[0].confidence_score,
                "style_recommendations": len(result.style_recommendations),
                "tension_peaks": result.rhythm_mapping.tension_peaks,
                "breathing_room": result.rhythm_mapping.breathing_room,
                "narrator_integration": result.narrator_integration,
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat(),
                # Add complete structures for downstream stations
                "episode_grid": episode_grid_list,
                "episodes": episode_grid_list,  # Alias for compatibility
                "macro_structure": asdict(result.macro_structure),
                "rhythm_mapping": asdict(result.rhythm_mapping)
            }
            
            # Export to text file
            try:
                text_content = processor.export_to_text(result)
                text_filename = f"outputs/station5_season_architecture_{state.session_id}.txt"
                os.makedirs(os.path.dirname(text_filename), exist_ok=True)
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                state.generated_files.append(text_filename)
                self.emit_progress("Station 5", 90, f"Exported season structure to {text_filename}")
            except Exception as e:
                logger.warning(f"Text export failed: {e}")
                
            # Export JSON data
            try:
                json_data = processor.export_to_json(result)
                json_filename = f"outputs/station5_season_data_{state.session_id}.json"
                os.makedirs(os.path.dirname(json_filename), exist_ok=True)
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, default=str)
                state.generated_files.append(json_filename)
            except Exception as e:
                logger.warning(f"JSON export failed: {e}")
                
            
            self.emit_progress("Station 5", 100, f"Station 5 completed! Chosen style: {result.chosen_style}")
            state.current_station = 5

            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "05", state.station_outputs["station_5"])

            return state
            
        except Exception as e:
            raise Exception(f"Station 5 failed: {str(e)}")
    
    async def _run_station_6(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 6: Master Style Guide Builder"""
        
        self.emit_progress("Station 6", 0, "Initializing Master Style Guide Builder...")
        
        try:
            processor = Station06MasterStyleGuideBuilder()
            await processor.initialize()
            
            if self.debug_mode:
                processor.debug_mode = True
                
            self.emit_progress("Station 6", 10, "Integrating all previous station outputs...")
            
            # Process master style guide
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 6", 30, "Creating comprehensive language rules...")
            self.emit_progress("Station 6", 50, "Designing character voice mapping...")
            self.emit_progress("Station 6", 70, "Establishing audio conventions...")
            self.emit_progress("Station 6", 85, "Building sonic signature system...")
            
            # Store Station 6 output
            state.station_outputs["station_6"] = {
                "working_title": result.working_title,
                "character_voices_count": len(result.dialect_accent_map.character_voices),
                "audio_conventions_count": len(result.audio_conventions.scene_transitions) + len(result.audio_conventions.temporal_markers),
                "has_narrator": result.narration_style is not None,
                "narrator_personality": result.narration_style.narrator_personality if result.narration_style else "No narrator",
                "sonic_elements_count": len(result.sonic_signature.main_theme_variations),
                "language_rules_complete": bool(result.language_rules),
                "dialogue_principles_complete": bool(result.dialogue_principles),
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat()
            }
            
            # Export to text file
            try:
                text_content = processor.export_to_text(result)
                text_filename = f"outputs/station6_master_style_guide_{state.session_id}.txt"
                os.makedirs(os.path.dirname(text_filename), exist_ok=True)
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                state.generated_files.append(text_filename)
                self.emit_progress("Station 6", 90, f"Exported master style guide to {text_filename}")
            except Exception as e:
                logger.warning(f"Text export failed: {e}")
                
            # Export JSON data
            try:
                json_data = processor.export_to_json(result)
                json_filename = f"outputs/station6_master_style_guide_{state.session_id}.json"
                os.makedirs(os.path.dirname(json_filename), exist_ok=True)
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, default=str)
                state.generated_files.append(json_filename)
            except Exception as e:
                logger.warning(f"JSON export failed: {e}")
                
            
            self.emit_progress("Station 6", 100, f"Station 6 completed! Master Style Guide for {result.working_title}")
            state.current_station = 6

            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "06", state.station_outputs["station_6"])

            return state
            
        except Exception as e:
            raise Exception(f"Station 6 failed: {str(e)}")
    
    async def _run_station_7(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 7: Reality Check - Comprehensive Quality Assurance"""
        
        self.emit_progress("Station 7", 0, "Initializing Reality Check validation...")
        
        try:
            processor = Station07RealityCheck()
            await processor.initialize()
            
            if self.debug_mode:
                processor.enable_debug_mode()
                
            self.emit_progress("Station 7", 10, "Loading all station outputs for validation...")
            
            # Process comprehensive validation
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 7", 30, "Validating station outputs...")
            self.emit_progress("Station 7", 50, "Analyzing LLM content quality...")
            self.emit_progress("Station 7", 70, "Detecting fallback/hardcoded content...")
            self.emit_progress("Station 7", 85, "Generating quality report...")
            
            # Store Station 7 output
            state.station_outputs["station_7"] = {
                "pipeline_status": result.pipeline_status,
                "overall_quality_score": result.quality_metrics.overall_quality_score,
                "pipeline_integrity": result.quality_metrics.pipeline_integrity,
                "stations_passed": result.quality_metrics.stations_passed,
                "stations_failed": result.quality_metrics.stations_failed,
                "stations_with_warnings": result.quality_metrics.stations_with_warnings,
                "creative_uniqueness_score": result.quality_metrics.creative_uniqueness_score,
                "technical_completeness_score": result.quality_metrics.technical_completeness_score,
                "critical_issues_count": len(result.critical_issues),
                "recommendations_count": len(result.recommendations),
                "session_id": result.session_id,
                "validation_timestamp": result.validation_timestamp.isoformat()
            }
            
            # Export validation reports
            try:
                # Text report
                text_content = processor.export_to_text(result)
                text_filename = f"outputs/station7_reality_check_{state.session_id}.txt"
                os.makedirs(os.path.dirname(text_filename), exist_ok=True)
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                state.generated_files.append(text_filename)
                self.emit_progress("Station 7", 90, f"Exported reality check report to {text_filename}")
            except Exception as e:
                logger.warning(f"Text export failed: {e}")
                
            # JSON data export
            try:
                json_data = processor.export_to_json(result)
                json_filename = f"outputs/station7_reality_check_{state.session_id}.json"
                os.makedirs(os.path.dirname(json_filename), exist_ok=True)
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, default=str)
                state.generated_files.append(json_filename)
            except Exception as e:
                logger.warning(f"JSON export failed: {e}")
                
            
            # Show critical validation results
            status_icon = "✅" if result.pipeline_status == "PASSED" else "⚠️" if result.pipeline_status == "NEEDS_ATTENTION" else "❌"
            self.emit_progress("Station 7", 100, f"Station 7 completed! {status_icon} {result.pipeline_status}")
            
            # Log critical issues if any
            if result.critical_issues:
                logger.warning(f"🚨 {len(result.critical_issues)} critical issues detected:")
                for issue in result.critical_issues[:3]:  # Show first 3
                    logger.warning(f"   • {issue}")
                if len(result.critical_issues) > 3:
                    logger.warning(f"   ... and {len(result.critical_issues) - 3} more issues")
            
            state.current_station = 7

            # Save to Redis for next stations
            await self._save_station_output_to_redis(state.session_id, "07", state.station_outputs["station_7"])

            return state
            
        except Exception as e:
            raise Exception(f"Station 7 failed: {str(e)}")
    
    async def _run_station_8(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 8: Character Architecture - 3-Tier Character System"""
        
        self.emit_progress("Station 8", 0, "Initializing Character Architecture...")
        
        try:
            processor = Station08CharacterArchitecture()
            await processor.initialize()
            
            if self.debug_mode:
                processor.enable_debug_mode()
                
            self.emit_progress("Station 8", 10, "Loading project dependencies...")
            
            # Process character architecture
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 8", 30, "Generating Tier 1 protagonists...")
            self.emit_progress("Station 8", 50, "Creating Tier 2 supporting characters...")
            self.emit_progress("Station 8", 70, "Designing Tier 3 recurring characters...")
            self.emit_progress("Station 8", 85, "Building character relationships...")
            
            # Store Station 8 output
            state.station_outputs["station_8"] = {
                "working_title": result.working_title,
                "total_characters": result.character_count_summary['total_characters'],
                "character_count_summary": result.character_count_summary,
                "tier1_protagonists": [asdict(char) for char in result.tier1_protagonists],
                "tier2_supporting": [asdict(char) for char in result.tier2_supporting],
                "tier3_recurring": [asdict(char) for char in result.tier3_recurring],
                "protagonist_names": [char.full_name for char in result.tier1_protagonists],
                "supporting_names": [char.full_name for char in result.tier2_supporting],
                "voice_samples_count": len(result.voice_sample_collection),
                "relationship_count": len(result.relationship_matrix),
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat()
            }
            
            # Export character bible files
            try:
                # Text export
                text_content = processor.export_to_text(result)
                text_filename = f"outputs/station8_character_bible_{state.session_id}.txt"
                os.makedirs(os.path.dirname(text_filename), exist_ok=True)
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                state.generated_files.append(text_filename)
                self.emit_progress("Station 8", 90, f"Exported character bible to {text_filename}")
            except Exception as e:
                logger.warning(f"Text export failed: {e}")
                
            # JSON data export
            try:
                json_data = processor.export_to_json(result)
                json_filename = f"outputs/station8_character_bible_{state.session_id}.json"
                os.makedirs(os.path.dirname(json_filename), exist_ok=True)
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, default=str)
                state.generated_files.append(json_filename)
            except Exception as e:
                logger.warning(f"JSON export failed: {e}")
                
            
            # Save to Redis for potential future stations
            try:
                redis_key = f"audiobook:{state.session_id}:station_08"
                json_data = json.dumps(state.station_outputs["station_8"], default=str)
                await self.redis.set(redis_key, json_data, expire=21600)
                if self.debug_mode:
                    logger.info(f"✅ Saved Station 8 output to Redis: {redis_key}")
            except Exception as e:
                logger.error(f"❌ Failed to save Station 8 to Redis: {e}")
            
            # Show character creation results
            self.emit_progress("Station 8", 100, f"Station 8 completed! Created {result.character_count_summary['total_characters']} characters")
            
            # Log character summary
            logger.info(f"🎭 Character Bible Summary:")
            logger.info(f"   Protagonists: {result.character_count_summary['tier1_protagonists']}")
            logger.info(f"   Supporting: {result.character_count_summary['tier2_supporting']}")
            logger.info(f"   Recurring: {result.character_count_summary['tier3_recurring']}")
            logger.info(f"   Total: {result.character_count_summary['total_characters']} characters")
            
            state.current_station = 8
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 8 failed: {str(e)}")
    
    async def _run_station_9(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 9: World Building System - Audio-Focused World Architecture"""
        
        self.emit_progress("Station 9", 0, "Initializing World Building System...")
        
        try:
            processor = Station09WorldBuilding()
            await processor.initialize()
            
            if self.debug_mode:
                processor.enable_debug_mode()
                
            self.emit_progress("Station 9", 10, "Loading project dependencies...")
            
            # Process world building
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 9", 25, "Generating geography with sonic signatures...")
            self.emit_progress("Station 9", 40, "Creating social systems with audio manifestations...")
            self.emit_progress("Station 9", 55, "Designing technology/magic with signature sounds...")
            self.emit_progress("Station 9", 70, "Building history/lore with audio echoes...")
            self.emit_progress("Station 9", 85, "Compiling sensory palette and audio cue library...")
            
            # Store Station 9 output
            state.station_outputs["station_9"] = {
                "working_title": result.working_title,
                "total_locations": result.world_statistics['total_locations'],
                "tech_magic_systems": result.world_statistics['tech_magic_systems'],
                "historical_events": result.world_statistics['historical_events'],
                "mythology_entries": result.world_statistics['mythology_entries'],
                "audio_cues": result.world_statistics['audio_cues'],
                "glossary_entries": result.world_statistics['glossary_entries'],
                "location_names": [loc.name for loc in result.geography],
                "system_names": [sys.name for sys in result.tech_magic_systems],
                "major_events": [event.name for event in result.historical_events],
                "session_id": result.session_id,
                "created_timestamp": result.created_timestamp.isoformat()
            }
            
            # Export world bible files
            try:
                # Text export
                text_content = processor.export_to_text(result)
                text_filename = f"outputs/station9_world_bible_{state.session_id}.txt"
                os.makedirs(os.path.dirname(text_filename), exist_ok=True)
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                state.generated_files.append(text_filename)
                self.emit_progress("Station 9", 90, f"Exported world bible to {text_filename}")
            except Exception as e:
                logger.warning(f"Text export failed: {e}")
                
            # JSON data export
            try:
                json_data = processor.export_to_json(result)
                json_filename = f"outputs/station9_world_bible_{state.session_id}.json"
                os.makedirs(os.path.dirname(json_filename), exist_ok=True)
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, default=str)
                state.generated_files.append(json_filename)
            except Exception as e:
                logger.warning(f"JSON export failed: {e}")
                
            
            # Save to Redis for potential future stations
            try:
                redis_key = f"audiobook:{state.session_id}:station_09"
                json_data = json.dumps(state.station_outputs["station_9"], default=str)
                await self.redis.set(redis_key, json_data, expire=21600)
                if self.debug_mode:
                    logger.info(f"✅ Saved Station 9 output to Redis: {redis_key}")
            except Exception as e:
                logger.error(f"❌ Failed to save Station 9 to Redis: {e}")
            
            # Show world building results
            self.emit_progress("Station 9", 100, f"Station 9 completed! Created world with {result.world_statistics['total_locations']} locations")
            
            # Log world summary
            logger.info(f"🌍 World Bible Summary:")
            logger.info(f"   Locations: {result.world_statistics['total_locations']}")
            logger.info(f"   Tech/Magic Systems: {result.world_statistics['tech_magic_systems']}")
            logger.info(f"   Historical Events: {result.world_statistics['historical_events']}")
            logger.info(f"   Audio Cues: {result.world_statistics['audio_cues']}")
            logger.info(f"   Glossary Entries: {result.world_statistics['glossary_entries']}")
            
            state.current_station = 9
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 9 failed: {str(e)}")
    
    async def _run_station_10(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 10: Narrative Reveal Strategy - Complete Reveal Matrix"""
        
        self.emit_progress("Station 10", 0, "Initializing Narrative Reveal Strategy...")
        
        try:
            processor = Station10NarrativeRevealStrategy()
            await processor.initialize()
            
            if self.debug_mode:
                logger.info("Debug mode enabled for Station 10")
                
            self.emit_progress("Station 10", 10, "Loading project dependencies...")
            
            # Process narrative reveal strategy
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 10", 25, "Building information taxonomy...")
            self.emit_progress("Station 10", 40, "Selecting reveal methods from 45+ catalog...")
            self.emit_progress("Station 10", 55, "Creating plant/proof/payoff grid...")
            self.emit_progress("Station 10", 70, "Designing misdirection strategy...")
            self.emit_progress("Station 10", 85, "Conducting fairness check...")
            
            # Store Station 10 output
            state.station_outputs["station_10"] = {
                "information_items": result["summary"]["information_items"],
                "reveal_methods": result["summary"]["reveal_methods"],
                "plant_proof_payoffs": result["summary"]["plant_proof_payoffs"],
                "red_herrings": result["summary"]["red_herrings"],
                "outputs": result["outputs"],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }
            
            # Add generated files to state
            if "outputs" in result:
                for output_type, file_path in result["outputs"].items():
                    if file_path and os.path.exists(file_path):
                        state.generated_files.append(file_path)
                        self.emit_progress("Station 10", 90, f"Generated {output_type} output: {file_path}")
            
            # Save to Redis for potential future stations
            try:
                if not self.redis:
                    self.redis = RedisClient()
                    await self.redis.initialize()
                redis_key = f"audiobook:{state.session_id}:station_10"
                json_data = json.dumps(state.station_outputs["station_10"], default=str)
                await self.redis.set(redis_key, json_data, expire=21600)
                if self.debug_mode:
                    logger.info(f"✅ Saved Station 10 output to Redis: {redis_key}")
            except Exception as e:
                logger.error(f"❌ Failed to save Station 10 to Redis: {e}")
            
            # Show narrative reveal strategy results
            self.emit_progress("Station 10", 100, f"Station 10 completed! Created reveal matrix with {result['summary']['information_items']} information items")
            
            # Log reveal strategy summary
            logger.info(f"🎭 Narrative Reveal Strategy Summary:")
            logger.info(f"   Information Items: {result['summary']['information_items']}")
            logger.info(f"   Reveal Methods: {result['summary']['reveal_methods']}")
            logger.info(f"   Plant/Proof/Payoffs: {result['summary']['plant_proof_payoffs']}")
            logger.info(f"   Red Herrings: {result['summary']['red_herrings']}")
            
            state.current_station = 10
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 10 failed: {str(e)}")
    
    async def _run_station_11(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 11: Runtime Planning - Complete Production Timeline"""
        
        self.emit_progress("Station 11", 0, "Initializing Runtime Planning...")
        
        try:
            processor = Station11RuntimePlanning()
            await processor.initialize()
            
            if self.debug_mode:
                processor.enable_debug_mode()
                
            self.emit_progress("Station 11", 10, "Loading project dependencies...")
            
            # Process runtime planning
            result = await processor.process(state.session_id)
            
            self.emit_progress("Station 11", 25, "Analyzing production requirements...")
            self.emit_progress("Station 11", 40, "Creating episode breakdown...")
            self.emit_progress("Station 11", 55, "Generating production timeline...")
            self.emit_progress("Station 11", 70, "Calculating resource requirements...")
            self.emit_progress("Station 11", 85, "Finalizing production plan...")
            
            # Store Station 11 output
            state.station_outputs["station_11"] = {
                "working_title": result.get("working_title", "Unknown"),
                "total_episodes": result.get("summary", {}).get("total_episodes", 0),
                "production_timeline": result.get("summary", {}).get("production_timeline", ""),
                "resource_requirements": result.get("summary", {}).get("resource_requirements", {}),
                "budget_estimate": result.get("summary", {}).get("budget_estimate", ""),
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }
            
            # Add generated files to state
            if "outputs" in result:
                for output_type, file_path in result["outputs"].items():
                    if file_path and os.path.exists(file_path):
                        state.generated_files.append(file_path)
                        self.emit_progress("Station 11", 90, f"Generated {output_type} output: {file_path}")
            
            # Save to Redis for potential future use
            try:
                if not self.redis:
                    self.redis = RedisClient()
                    await self.redis.initialize()
                redis_key = f"audiobook:{state.session_id}:station_11"
                json_data = json.dumps(state.station_outputs["station_11"], default=str)
                await self.redis.set(redis_key, json_data, expire=21600)
                if self.debug_mode:
                    logger.info(f"✅ Saved Station 11 output to Redis: {redis_key}")
            except Exception as e:
                logger.error(f"❌ Failed to save Station 11 to Redis: {e}")
            
            # Show runtime planning results
            self.emit_progress("Station 11", 100, f"Station 11 completed! Created production plan for {result.get('summary', {}).get('total_episodes', 0)} episodes")
            
            # Log runtime planning summary
            logger.info(f"📅 Runtime Planning Summary:")
            logger.info(f"   Total Episodes: {result.get('summary', {}).get('total_episodes', 0)}")
            logger.info(f"   Production Timeline: {result.get('summary', {}).get('production_timeline', 'Unknown')}")
            logger.info(f"   Budget Estimate: {result.get('summary', {}).get('budget_estimate', 'Unknown')}")
            
            state.current_station = 11
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 11 failed: {str(e)}")
    
    async def _run_station_12(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 12: Hook & Cliffhanger Designer"""
        
        self.emit_progress("Station 12", 0, "Initializing Hook & Cliffhanger Designer...")
        
        try:
            processor = Station12HookCliffhanger(state.session_id)
            await processor.initialize()
            
            self.emit_progress("Station 12", 10, "Loading episode and character dependencies...")
            
            # Process hook and cliffhanger design
            result = await processor.run()
            
            self.emit_progress("Station 12", 25, "Generating opening hooks for episodes...")
            self.emit_progress("Station 12", 50, "Designing act turns and cliffhangers...")
            self.emit_progress("Station 12", 75, "Creating episode tension curves...")
            self.emit_progress("Station 12", 90, "Building episode bridges...")
            
            # Store Station 12 output
            state.station_outputs["station_12"] = {
                "total_episodes": result['statistics']['total_episodes'],
                "hooks_designed": result['statistics']['hooks_designed'],
                "cliffhangers_designed": result['statistics']['cliffhangers_designed'],
                "bridges_created": result['statistics']['bridges_created'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }
            
            # Add generated files to state
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])
            
            self.emit_progress("Station 12", 100, f"Station 12 completed! {result['statistics']['hooks_designed']} hooks and cliffhangers designed")
            
            # Log hook summary
            logger.info(f"⚡ Hook & Cliffhanger Summary:")
            logger.info(f"   Episodes: {result['statistics']['total_episodes']}")
            logger.info(f"   Hooks: {result['statistics']['hooks_designed']}")
            logger.info(f"   Cliffhangers: {result['statistics']['cliffhangers_designed']}")
            logger.info(f"   Bridges: {result['statistics']['bridges_created']}")
            
            state.current_station = 12
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 12 failed: {str(e)}")
    
    async def _run_station_13(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 13: Multi-World/Timeline Manager"""
        
        self.emit_progress("Station 13", 0, "Initializing Multi-World/Timeline Manager...")
        
        try:
            processor = Station13MultiworldTimeline(state.session_id)
            await processor.initialize()
            
            self.emit_progress("Station 13", 10, "Analyzing world/timeline structure...")
            
            # Process multi-world management
            result = await processor.run()
            
            self.emit_progress("Station 13", 25, "Detecting scenario complexity...")
            self.emit_progress("Station 13", 50, "Generating world management rules...")
            self.emit_progress("Station 13", 75, "Designing audio differentiation...")
            self.emit_progress("Station 13", 90, "Creating orientation strategies...")
            
            # Store Station 13 output
            state.station_outputs["station_13"] = {
                "is_applicable": result['is_applicable'],
                "world_count": result['statistics']['world_count'],
                "transition_types": result['statistics']['transition_types'],
                "complexity_level": result['statistics']['complexity_level'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }
            
            # Add generated files to state
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])
            
            if result['is_applicable']:
                self.emit_progress("Station 13", 100, f"Station 13 completed! Multi-world system with {result['statistics']['world_count']} worlds")
                logger.info(f"🌐 Multi-World Summary:")
                logger.info(f"   Applicable: {result['is_applicable']}")
                logger.info(f"   Worlds: {result['statistics']['world_count']}")
                logger.info(f"   Complexity: {result['statistics']['complexity_level']}")
            else:
                self.emit_progress("Station 13", 100, "Station 13 completed! Single-world narrative detected")
                logger.info(f"🌐 Single World Detected - Station 13 gracefully skipped")
            
            state.current_station = 13
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 13 failed: {str(e)}")
    
    async def _run_station_14(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 14: Simple Episode Blueprint"""
        
        self.emit_progress("Station 14", 0, "Initializing Episode Blueprint Generator...")
        
        try:
            processor = Station14EpisodeBlueprint(state.session_id)
            await processor.initialize()
            
            self.emit_progress("Station 14", 10, "Loading all station dependencies...")
            
            # Process episode blueprints
            result = await processor.run()
            
            self.emit_progress("Station 14", 25, "Generating episode summaries...")
            self.emit_progress("Station 14", 50, "Creating character goals and obstacles...")
            self.emit_progress("Station 14", 70, "Building season narrative overview...")
            self.emit_progress("Station 14", 85, "Generating approval checklist...")
            
            # Store Station 14 output
            state.station_outputs["station_14"] = {
                "total_episodes": result['statistics']['total_episodes'],
                "blueprints_generated": result['statistics']['blueprints_generated'],
                "ready_for_approval": result['statistics']['ready_for_approval'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }
            
            # Add generated files to state
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])
            
            self.emit_progress("Station 14", 100, f"Station 14 completed! {result['statistics']['blueprints_generated']} episode blueprints ready for approval")
            
            # Log blueprint summary
            logger.info(f"📋 Episode Blueprint Summary:")
            logger.info(f"   Episodes: {result['statistics']['total_episodes']}")
            logger.info(f"   Blueprints: {result['statistics']['blueprints_generated']}")
            logger.info(f"   Ready for Approval: {result['statistics']['ready_for_approval']}")
            logger.info(f"   TXT Approval Doc: {result['outputs']['txt']}")
            logger.info(f"   JSON Data: {result['outputs']['json']}")

            # Important human gate message
            print("\n" + "="*70)
            print("🚨 HUMAN APPROVAL GATE - REVIEW REQUIRED")
            print("="*70)
            print(f"📄 Review Document (TXT): {result['outputs']['txt']}")
            print(f"📄 Review Document (JSON): {result['outputs']['json']}")
            print("👤 Please review and approve episode blueprints before proceeding")
            print("✅ This completes the automated pipeline - human review required")
            print("="*70)
            
            state.current_station = 14
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 14 failed: {str(e)}")
    
    async def _run_station_15(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 15: Detailed Episode Outlining"""
        
        self.emit_progress("Station 15", 0, "Initializing Detailed Episode Outlining...")
        
        try:
            processor = Station15DetailedEpisodeOutlining(state.session_id)
            await processor.initialize()
            
            if self.debug_mode:
                processor.enable_debug_mode()
                
            self.emit_progress("Station 15", 10, "Loading episode blueprint dependencies...")
            
            # Process detailed episode outlining
            result = await processor.run()
            
            self.emit_progress("Station 15", 25, "Generating detailed episode outlines...")
            self.emit_progress("Station 15", 50, "Creating scene-by-scene breakdowns...")
            self.emit_progress("Station 15", 75, "Building character arc progressions...")
            self.emit_progress("Station 15", 90, "Finalizing production-ready outlines...")
            
            # Store Station 15 output
            state.station_outputs["station_15"] = {
                "total_episodes": result['statistics']['total_episodes'],
                "outlines_generated": result['statistics']['outlines_generated'],
                "scenes_per_episode": result['statistics']['scenes_per_episode'],
                "ready_for_production": result['statistics']['ready_for_production'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }
            
            # Add generated files to state
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])
            
            self.emit_progress("Station 15", 100, f"Station 15 completed! {result['statistics']['outlines_generated']} detailed episode outlines ready for production")
            
            # Log detailed outlining summary
            logger.info(f"📝 Detailed Episode Outlining Summary:")
            logger.info(f"   Episodes: {result['statistics']['total_episodes']}")
            logger.info(f"   Outlines: {result['statistics']['outlines_generated']}")
            logger.info(f"   Scenes per Episode: {result['statistics']['scenes_per_episode']}")
            logger.info(f"   Ready for Production: {result['statistics']['ready_for_production']}")
            logger.info(f"   TXT Production Doc: {result['outputs']['txt']}")
            logger.info(f"   JSON Data: {result['outputs']['json']}")

            # Important production-ready message
            print("\n" + "="*70)
            print("🎬 PRODUCTION-READY EPISODE OUTLINES COMPLETED")
            print("="*70)
            print(f"📄 Production Document (TXT): {result['outputs']['txt']}")
            print(f"📄 Production Document (JSON): {result['outputs']['json']}")
            print("🎭 Detailed scene-by-scene outlines ready for voice actors")
            print("✅ Complete audiobook production pipeline finished!")
            print("="*70)
            
            state.current_station = 15

            return state

        except Exception as e:
            raise Exception(f"Station 15 failed: {str(e)}")

    async def _run_station_16(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 16: Canon Consistency Check"""

        self.emit_progress("Station 16", 0, "Initializing Canon Check...")

        try:
            processor = Station16CanonCheck(state.session_id)
            await processor.initialize()

            self.emit_progress("Station 16", 20, "Validating character consistency...")

            # Process canon validation
            result = await processor.run()

            self.emit_progress("Station 16", 50, "Validating location consistency...")
            self.emit_progress("Station 16", 70, "Validating timeline consistency...")
            self.emit_progress("Station 16", 90, "Validating plot consistency...")

            # Store Station 16 output
            state.station_outputs["station_16"] = {
                "validation_status": result['statistics']['validation_status'],
                "consistency_score": result['statistics']['consistency_score'],
                "total_issues": result['statistics']['total_issues'],
                "critical_issues": result['statistics']['critical_issues'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }

            # Add generated files
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])

            self.emit_progress("Station 16", 100, f"Station 16 completed! Validation: {result['statistics']['validation_status']}")

            logger.info(f"📋 Canon Check Summary:")
            logger.info(f"   Status: {result['statistics']['validation_status']}")
            logger.info(f"   Consistency Score: {result['statistics']['consistency_score']}/100")
            logger.info(f"   Issues Found: {result['statistics']['total_issues']}")

            state.current_station = 16

            # Save to Redis
            await self._save_station_output_to_redis(state.session_id, "16", state.station_outputs["station_16"])

            return state

        except Exception as e:
            raise Exception(f"Station 16 failed: {str(e)}")

    async def _run_station_17(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 17: Dialect Planning"""

        self.emit_progress("Station 17", 0, "Initializing Dialect Planning...")

        try:
            processor = Station17DialectPlanning(state.session_id)
            await processor.initialize()

            self.emit_progress("Station 17", 20, "Validating character voices...")

            # Process dialect validation
            result = await processor.run()

            self.emit_progress("Station 17", 50, "Validating age appropriateness...")
            self.emit_progress("Station 17", 70, "Generating vocabulary banks...")

            # Store Station 17 output
            state.station_outputs["station_17"] = {
                "validation_status": result['statistics']['validation_status'],
                "overall_score": result['statistics']['overall_score'],
                "total_issues": result['statistics']['total_issues'],
                "characters_analyzed": result['statistics']['characters_analyzed'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }

            # Add generated files
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])

            self.emit_progress("Station 17", 100, f"Station 17 completed! Validation: {result['statistics']['validation_status']}")

            logger.info(f"🗣️  Dialect Planning Summary:")
            logger.info(f"   Status: {result['statistics']['validation_status']}")
            logger.info(f"   Overall Score: {result['statistics']['overall_score']}/100")
            logger.info(f"   Characters Analyzed: {result['statistics']['characters_analyzed']}")

            state.current_station = 17

            # Save to Redis
            await self._save_station_output_to_redis(state.session_id, "17", state.station_outputs["station_17"])

            return state

        except Exception as e:
            raise Exception(f"Station 17 failed: {str(e)}")

    async def _run_station_18(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 18: Evergreen Content Check"""

        self.emit_progress("Station 18", 0, "Initializing Evergreen Check...")

        try:
            processor = Station18EvergreenCheck(state.session_id)
            await processor.initialize()

            self.emit_progress("Station 18", 20, "Detecting dated references...")

            # Process evergreen validation
            result = await processor.run()

            self.emit_progress("Station 18", 50, "Analyzing cultural references...")
            self.emit_progress("Station 18", 70, "Validating theme universality...")

            # Store Station 18 output
            state.station_outputs["station_18"] = {
                "validation_status": result['statistics']['validation_status'],
                "evergreen_score": result['statistics']['evergreen_score'],
                "dated_references": result['statistics']['dated_references'],
                "high_risk": result['statistics']['high_risk'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }

            # Add generated files
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])

            self.emit_progress("Station 18", 100, f"Station 18 completed! Validation: {result['statistics']['validation_status']}")

            logger.info(f"⏳ Evergreen Check Summary:")
            logger.info(f"   Status: {result['statistics']['validation_status']}")
            logger.info(f"   Evergreen Score: {result['statistics']['evergreen_score']}/100")
            logger.info(f"   Dated References: {result['statistics']['dated_references']}")

            state.current_station = 18

            # Save to Redis
            await self._save_station_output_to_redis(state.session_id, "18", state.station_outputs["station_18"])

            return state

        except Exception as e:
            raise Exception(f"Station 18 failed: {str(e)}")

    async def _run_station_19(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 19: Procedure Accuracy Check"""

        self.emit_progress("Station 19", 0, "Initializing Procedure Check...")

        try:
            processor = Station19ProcedureCheck(state.session_id)
            await processor.initialize()

            self.emit_progress("Station 19", 20, "Validating professional procedures...")

            # Process procedure validation
            result = await processor.run()

            self.emit_progress("Station 19", 50, "Validating timelines...")
            self.emit_progress("Station 19", 70, "Validating technology usage...")

            # Store Station 19 output
            state.station_outputs["station_19"] = {
                "validation_status": result['statistics']['validation_status'],
                "overall_realism_score": result['statistics']['overall_realism_score'],
                "procedures_validated": result['statistics']['procedures_validated'],
                "timelines_validated": result['statistics']['timelines_validated'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }

            # Add generated files
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])

            self.emit_progress("Station 19", 100, f"Station 19 completed! Validation: {result['statistics']['validation_status']}")

            logger.info(f"⚖️  Procedure Check Summary:")
            logger.info(f"   Status: {result['statistics']['validation_status']}")
            logger.info(f"   Realism Score: {result['statistics']['overall_realism_score']}/100")
            logger.info(f"   Procedures Validated: {result['statistics']['procedures_validated']}")

            state.current_station = 19

            # Save to Redis
            await self._save_station_output_to_redis(state.session_id, "19", state.station_outputs["station_19"])

            return state

        except Exception as e:
            raise Exception(f"Station 19 failed: {str(e)}")

    async def _run_station_20(self, state: AudiobookProductionState) -> AudiobookProductionState:
        """Run Station 20: Geography & Transit Check"""

        self.emit_progress("Station 20", 0, "Initializing Geography Check...")

        try:
            processor = Station20GeographyTransit(state.session_id)
            await processor.initialize()

            self.emit_progress("Station 20", 20, "Validating location network...")

            # Process geography validation
            result = await processor.run()

            self.emit_progress("Station 20", 50, "Validating weather continuity...")
            self.emit_progress("Station 20", 70, "Validating temporal consistency...")

            # Store Station 20 output
            state.station_outputs["station_20"] = {
                "validation_status": result['statistics']['validation_status'],
                "geography_score": result['statistics']['geography_score'],
                "transit_realism_score": result['statistics']['transit_realism_score'],
                "location_pairs_analyzed": result['statistics']['location_pairs_analyzed'],
                "outputs": result['outputs'],
                "session_id": state.session_id,
                "created_timestamp": datetime.now().isoformat()
            }

            # Add generated files
            state.generated_files.extend([
                result['outputs']['txt'],
                result['outputs']['json']
            ])

            self.emit_progress("Station 20", 100, f"Station 20 completed! Validation: {result['statistics']['validation_status']}")

            logger.info(f"🗺️  Geography Check Summary:")
            logger.info(f"   Status: {result['statistics']['validation_status']}")
            logger.info(f"   Geography Score: {result['statistics']['geography_score']}/100")
            logger.info(f"   Location Pairs: {result['statistics']['location_pairs_analyzed']}")

            # Display validation suite completion
            print("\n" + "="*70)
            print("✅ VALIDATION SUITE COMPLETE (Stations 16-20)")
            print("="*70)
            print("Canon Consistency: " + ("✅ PASS" if state.station_outputs["station_16"]["validation_status"] == "PASS" else "⚠️  " + state.station_outputs["station_16"]["validation_status"]))
            print("Dialect Planning: " + ("✅ PASS" if state.station_outputs["station_17"]["validation_status"] == "PASS" else "⚠️  " + state.station_outputs["station_17"]["validation_status"]))
            print("Evergreen Content: " + ("✅ PASS" if state.station_outputs["station_18"]["validation_status"] == "PASS" else "⚠️  " + state.station_outputs["station_18"]["validation_status"]))
            print("Procedure Accuracy: " + ("✅ PASS" if state.station_outputs["station_19"]["validation_status"] == "PASS" else "⚠️  " + state.station_outputs["station_19"]["validation_status"]))
            print("Geography & Transit: " + ("✅ PASS" if state.station_outputs["station_20"]["validation_status"] == "PASS" else "⚠️  " + state.station_outputs["station_20"]["validation_status"]))
            print("="*70)
            print("🎬 Ready to proceed to script writing phase!")
            print("="*70)

            state.current_station = 20

            # Save to Redis
            await self._save_station_output_to_redis(state.session_id, "20", state.station_outputs["station_20"])

            return state

        except Exception as e:
            raise Exception(f"Station 20 failed: {str(e)}")


    async def _generate_final_summary(self, state: AudiobookProductionState):
        """Generate final automation summary"""
        
        summary_path = f"outputs/automation_summary_{state.session_id}.json"
        os.makedirs("outputs", exist_ok=True)
        
        # Convert enums to strings in station outputs before serialization
        processed_outputs = state.station_outputs.copy()
        for station_key, station_data in processed_outputs.items():
            if isinstance(station_data, dict):
                processed_outputs[station_key] = self._convert_enums_to_strings(station_data)

        summary = {
            "automation_completed": datetime.now().isoformat(),
            "session_id": state.session_id,
            "story_concept": state.story_concept,
            "chosen_scale": state.chosen_scale,
            "chosen_genre_blend": state.chosen_genre_blend,
            "stations_completed": state.current_station,
            "outputs_summary": {
                "station_1": "Scale evaluation and initial expansion",
                "station_2": "Complete project bible",
                "station_3": "Age guidelines and genre optimization", 
                "station_4": f"Seed bank with {state.station_outputs.get('station_4', {}).get('total_seeds', 0)} story elements",
                "station_4_5": f"Narrator strategy: {state.station_outputs.get('station_4_5', {}).get('recommendation', 'Unknown')}",
                "station_5": f"Season architecture: {state.station_outputs.get('station_5', {}).get('chosen_style', 'Unknown')} style with {state.station_outputs.get('station_5', {}).get('total_episodes', 0)} episodes",
                "station_6": f"Master style guide: {state.station_outputs.get('station_6', {}).get('character_voices_count', 0)} character voices, {state.station_outputs.get('station_6', {}).get('audio_conventions_count', 0)} audio conventions",
                "station_7": f"Reality check: {state.station_outputs.get('station_7', {}).get('pipeline_status', 'Unknown')} - Quality: {state.station_outputs.get('station_7', {}).get('overall_quality_score', 0):.1%}, Passed: {state.station_outputs.get('station_7', {}).get('stations_passed', 0)}/{state.station_outputs.get('station_7', {}).get('stations_passed', 0) + state.station_outputs.get('station_7', {}).get('stations_failed', 0) + state.station_outputs.get('station_7', {}).get('stations_with_warnings', 0)}",
                "station_8": f"Character bible: {state.station_outputs.get('station_8', {}).get('total_characters', 0)} characters ({state.station_outputs.get('station_8', {}).get('tier1_protagonists', 0)} protagonists, {state.station_outputs.get('station_8', {}).get('tier2_supporting', 0)} supporting, {state.station_outputs.get('station_8', {}).get('tier3_recurring', 0)} recurring)",
                "station_9": f"World bible: {state.station_outputs.get('station_9', {}).get('total_locations', 0)} locations, {state.station_outputs.get('station_9', {}).get('tech_magic_systems', 0)} tech/magic systems, {state.station_outputs.get('station_9', {}).get('audio_cues', 0)} audio cues, {state.station_outputs.get('station_9', {}).get('glossary_entries', 0)} glossary entries",
                "station_10": f"Narrative reveal strategy: {state.station_outputs.get('station_10', {}).get('information_items', 0)} information items, {state.station_outputs.get('station_10', {}).get('reveal_methods', 0)} reveal methods, {state.station_outputs.get('station_10', {}).get('plant_proof_payoffs', 0)} plant/proof/payoffs, {state.station_outputs.get('station_10', {}).get('red_herrings', 0)} red herrings",
                "station_11": f"Runtime planning: {state.station_outputs.get('station_11', {}).get('total_episodes', 0)} episodes planned, {state.station_outputs.get('station_11', {}).get('production_timeline', 'Unknown')} timeline, {state.station_outputs.get('station_11', {}).get('budget_estimate', 'Unknown')} budget estimate",
                "station_12": f"Hook & cliffhanger design: {state.station_outputs.get('station_12', {}).get('hooks_designed', 0)} hooks, {state.station_outputs.get('station_12', {}).get('cliffhangers_designed', 0)} cliffhangers, {state.station_outputs.get('station_12', {}).get('bridges_created', 0)} bridges",
                "station_13": f"Multi-world management: {state.station_outputs.get('station_13', {}).get('world_count', 1)} worlds, complexity {state.station_outputs.get('station_13', {}).get('complexity_level', 'simple')}, applicable: {state.station_outputs.get('station_13', {}).get('is_applicable', False)}",
                "station_14": f"Episode blueprints: {state.station_outputs.get('station_14', {}).get('blueprints_generated', 0)} episodes ready for approval",
                "station_15": f"Detailed episode outlining: {state.station_outputs.get('station_15', {}).get('outlines_generated', 0)} production-ready outlines, {state.station_outputs.get('station_15', {}).get('scenes_per_episode', 0)} scenes per episode",
                "station_16": f"Canon check: {state.station_outputs.get('station_16', {}).get('validation_status', 'Unknown')} - Consistency: {state.station_outputs.get('station_16', {}).get('consistency_score', 0)}/100, Issues: {state.station_outputs.get('station_16', {}).get('total_issues', 0)}",
                "station_17": f"Dialect planning: {state.station_outputs.get('station_17', {}).get('validation_status', 'Unknown')} - Voice consistency: {state.station_outputs.get('station_17', {}).get('overall_score', 0)}/100, Characters analyzed: {state.station_outputs.get('station_17', {}).get('characters_analyzed', 0)}",
                "station_18": f"Evergreen check: {state.station_outputs.get('station_18', {}).get('validation_status', 'Unknown')} - Evergreen score: {state.station_outputs.get('station_18', {}).get('evergreen_score', 0)}/100, Dated references: {state.station_outputs.get('station_18', {}).get('dated_references', 0)}",
                "station_19": f"Procedure check: {state.station_outputs.get('station_19', {}).get('validation_status', 'Unknown')} - Realism: {state.station_outputs.get('station_19', {}).get('overall_realism_score', 0)}/100, Procedures validated: {state.station_outputs.get('station_19', {}).get('procedures_validated', 0)}",
                "station_20": f"Geography check: {state.station_outputs.get('station_20', {}).get('validation_status', 'Unknown')} - Geography score: {state.station_outputs.get('station_20', {}).get('geography_score', 0)}/100, Locations analyzed: {state.station_outputs.get('station_20', {}).get('location_pairs_analyzed', 0)}"
            },
            "generated_files": state.generated_files,
            "full_outputs": processed_outputs
        }
        
        # Custom JSON encoder to handle enums
        class EnumEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, 'value'):
                    return obj.value
                return super().default(obj)

        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, cls=EnumEncoder)
            
        state.generated_files.append(summary_path)
        print(f"📄 Final summary saved to: {summary_path}")
    
    async def _save_checkpoint(self, state: AudiobookProductionState):
        """Save automation checkpoint for recovery"""
        
        checkpoint_path = f"outputs/checkpoint_{state.session_id}.json"
        os.makedirs("outputs", exist_ok=True)
        
        # Convert enums to strings in station outputs before serialization
        processed_state = state.to_dict()

        # Process station outputs to convert enums
        if "station_outputs" in processed_state:
            for station_key, station_data in processed_state["station_outputs"].items():
                if isinstance(station_data, dict):
                    # Convert any enum objects to their string values
                    processed_state["station_outputs"][station_key] = self._convert_enums_to_strings(station_data)

        checkpoint_data = {
            "checkpoint_time": datetime.now().isoformat(),
            "state": processed_state
        }
        
        # Custom JSON encoder to handle enums
        class EnumEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, 'value'):
                    return obj.value
                return super().default(obj)

        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, cls=EnumEncoder)
            
        if self.debug_mode:
            print(f"💾 Checkpoint saved: {checkpoint_path}")

    async def _save_station_output_to_redis(self, session_id: str, station_number: str, station_data: dict):
        """Save station output to Redis for next stations to access"""
        try:
            if not self.redis:
                self.redis = RedisClient()
                await self.redis.initialize()

            # Convert station data to JSON string
            json_data = json.dumps(station_data, default=str)

            # Save with the expected key format
            redis_key = f"audiobook:{session_id}:station_{station_number.replace('.', '_')}"

            await self.redis.set(redis_key, json_data, expire=21600)  # Expire after 6 hours

            if self.debug_mode:
                logger.info(f"✅ Saved station {station_number} output to Redis: {redis_key}")

        except Exception as e:
            logger.error(f"❌ Failed to save station {station_number} to Redis: {e}")

    async def _restore_redis_from_checkpoint(self, state: AudiobookProductionState):
        """Restore all station outputs from checkpoint to Redis"""
        try:
            if not self.redis:
                self.redis = RedisClient()
                await self.redis.initialize()

            # Map station keys to Redis format
            station_mapping = {
                "station_1": "01",
                "station_2": "02",
                "station_3": "03",
                "station_4": "04",
                "station_4_5": "04_5",
                "station_5": "05",
                "station_6": "06",
                "station_7": "07",
                "station_8": "08",
                "station_9": "09",
                "station_10": "10",
                "station_11": "11",
                "station_12": "12",
                "station_13": "13",
                "station_14": "14",
                "station_15": "15",
                "station_16": "16",
                "station_17": "17",
                "station_18": "18",
                "station_19": "19",
                "station_20": "20"
            }

            restored_count = 0
            for station_key, station_data in state.station_outputs.items():
                if station_key in station_mapping:
                    redis_number = station_mapping[station_key]
                    await self._save_station_output_to_redis(state.session_id, redis_number, station_data)
                    restored_count += 1

            logger.info(f"✅ Restored {restored_count} station outputs to Redis")

        except Exception as e:
            logger.error(f"❌ Failed to restore Redis data: {e}")
            # Non-fatal - stations can still work with checkpoint data

    def _convert_enums_to_strings(self, data):
        """Recursively convert enum objects to their string values"""
        if isinstance(data, dict):
            return {key: self._convert_enums_to_strings(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._convert_enums_to_strings(item) for item in data]
        elif hasattr(data, 'value'):  # Enum object
            return data.value
        else:
            return data

    @staticmethod
    def list_available_checkpoints():
        """List all available checkpoint files"""
        checkpoint_dir = Path("outputs")
        if not checkpoint_dir.exists():
            return []

        checkpoints = []
        for checkpoint_file in checkpoint_dir.glob("checkpoint_*.json"):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state = data.get('state', {})
                    checkpoints.append({
                        'session_id': state.get('session_id', 'unknown'),
                        'file': str(checkpoint_file),
                        'checkpoint_time': data.get('checkpoint_time', 'unknown'),
                        'current_station': state.get('current_station', 0),
                        'story_concept': state.get('story_concept', '')[:80] + '...'
                    })
            except Exception as e:
                logger.warning(f"Failed to read checkpoint {checkpoint_file}: {e}")

        return sorted(checkpoints, key=lambda x: x['checkpoint_time'], reverse=True)

    async def load_checkpoint(self, session_id: str) -> Optional[AudiobookProductionState]:
        """Load automation checkpoint for recovery"""
        
        checkpoint_path = f"outputs/checkpoint_{session_id}.json"
        
        if not os.path.exists(checkpoint_path):
            return None
            
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)
                
            state_data = checkpoint_data['state']
            
            # Reconstruct state object
            state = AudiobookProductionState(state_data['story_concept'])
            state.session_id = state_data['session_id']
            state.current_station = state_data['current_station']
            state.station_outputs = state_data['station_outputs']
            state.chosen_scale = state_data['chosen_scale']
            state.chosen_genre_blend = state_data['chosen_genre_blend']
            state.generated_files = state_data['generated_files']
            state.errors = state_data['errors']
            
            return state
            
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None
    
    async def resume_automation(self, session_id: str) -> Dict[str, Any]:
        """Resume automation from checkpoint"""

        print(f"🔄 RESUMING AUTOMATION FROM CHECKPOINT")
        print(f"🆔 Session ID: {session_id}")
        print("=" * 50)

        # Load checkpoint
        state = await self.load_checkpoint(session_id)
        if not state:
            return {
                "success": False,
                "error": f"No checkpoint found for session {session_id}"
            }

        print(f"✅ Checkpoint loaded - resuming from Station {state.current_station + 1}")
        self.current_session_id = state.session_id  # Track for interruption handling

        # Restore Redis data from checkpoint
        print(f"🔄 Restoring station outputs to Redis...")
        await self._restore_redis_from_checkpoint(state)
        print(f"✅ Redis data restored for {len(state.station_outputs)} stations")

        try:
            # Resume from where we left off
            if state.current_station < 1:
                state = await self._run_station_1(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 2:
                state = await self._run_station_2(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 3:
                state = await self._run_station_3(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 4:
                state = await self._run_station_4(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 4.5:
                state = await self._run_station_4_5(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 5:
                state = await self._run_station_5(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 6:
                state = await self._run_station_6(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 7:
                state = await self._run_station_7(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 8:
                state = await self._run_station_8(state)
                await self._save_checkpoint(state)
                
            if state.current_station < 9:
                state = await self._run_station_9(state)
                await self._save_checkpoint(state)

            if state.current_station < 10:
                state = await self._run_station_10(state)
                await self._save_checkpoint(state)

            if state.current_station < 11:
                state = await self._run_station_11(state)
                await self._save_checkpoint(state)

            if state.current_station < 12:
                state = await self._run_station_12(state)
                await self._save_checkpoint(state)

            if state.current_station < 13:
                state = await self._run_station_13(state)
                await self._save_checkpoint(state)

            if state.current_station < 14:
                state = await self._run_station_14(state)
                await self._save_checkpoint(state)

            if state.current_station < 15:
                state = await self._run_station_15(state)
                await self._save_checkpoint(state)

            if state.current_station < 16:
                state = await self._run_station_16(state)
                await self._save_checkpoint(state)

            if state.current_station < 17:
                state = await self._run_station_17(state)
                await self._save_checkpoint(state)

            if state.current_station < 18:
                state = await self._run_station_18(state)
                await self._save_checkpoint(state)

            if state.current_station < 19:
                state = await self._run_station_19(state)
                await self._save_checkpoint(state)

            if state.current_station < 20:
                state = await self._run_station_20(state)
                await self._save_checkpoint(state)

            # Generate final summary
            await self._generate_final_summary(state)
            
            print("\n🎉 RESUMED AUTOMATION COMPLETED!")
            
            return {
                "success": True,
                "session_id": state.session_id,
                "outputs": state.station_outputs,
                "files": state.generated_files,
                "summary": "Automation resumed and completed successfully"
            }
            
        except Exception as e:
            logger.error(f"Resume failed: {str(e)}")
            return {
                "success": False,
                "session_id": state.session_id,
                "error": str(e),
                "completed_stations": state.current_station
            }
    
    async def _get_user_scale_choice(self, result) -> str:
        """Get user's scale choice (interactive mode)"""
        print("\n📊 SCALE OPTIONS AVAILABLE:")
        for i, option in enumerate(result.scale_options, 1):
            print(f"  {chr(64+i)}. {option.scale_type.value}: {option.description[:100]}...")
        
        print(f"\n🤖 AI Recommendation: Option {result.recommended_option}")
        
        while True:
            choice = input("\n💡 Choose scale (A/B/C) or press Enter for AI recommendation: ").upper().strip()
            if not choice:
                return result.recommended_option
            if choice in ['A', 'B', 'C']:
                return choice
            print("❌ Invalid choice. Please enter A, B, C, or press Enter.")
    
    async def _get_user_genre_choice(self, result) -> str:
        """Get user's genre blend choice (interactive mode)"""
        print("\n🎭 GENRE BLEND OPTIONS AVAILABLE:")
        for i, option in enumerate(result.genre_options, 1):
            print(f"  {chr(64+i)}. {option.blend_name}: {option.description[:100]}...")
        
        print(f"\n🤖 AI Recommendation: {result.recommended_genre_blend}")
        
        while True:
            choice = input("\n💡 Choose genre blend or press Enter for AI recommendation: ").strip()
            if not choice:
                return result.recommended_genre_blend
            if choice.upper() in ['A', 'B', 'C']:
                return chr(64 + ord(choice.upper()) - 64)
            print("❌ Invalid choice. Please try again or press Enter for recommendation.")


async def main():
    """Main entry point for full automation"""

    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Full Audiobook Production Automation')
    parser.add_argument('--resume', type=str, help='Resume from checkpoint using session ID')
    parser.add_argument('--list-checkpoints', action='store_true', help='List all available checkpoints')
    parser.add_argument('--auto-approve', action='store_true', help='Auto-approve all decisions')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    # List checkpoints if requested
    if args.list_checkpoints:
        print("📋 AVAILABLE CHECKPOINTS")
        print("=" * 80)
        checkpoints = FullAutomationRunner.list_available_checkpoints()
        if not checkpoints:
            print("❌ No checkpoints found")
            print("💡 Run the automation first to create checkpoints")
        else:
            for i, cp in enumerate(checkpoints, 1):
                print(f"\n{i}. Session: {cp['session_id']}")
                print(f"   ⏰ Saved: {cp['checkpoint_time']}")
                print(f"   📊 Progress: Station {cp['current_station']}")
                print(f"   📝 Story: {cp['story_concept']}")
                print(f"   📂 File: {cp['file']}")
            print(f"\n💡 Resume using: python full_automation.py --resume SESSION_ID")
        sys.exit(0)

    print("🎬 FULL AUDIOBOOK PRODUCTION AUTOMATION")
    print("=" * 60)
    print("🤖 Complete Pipeline: Station 1 → 2 → 3 → 4 → 4.5 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15")
    print()

    # Initialize runner
    auto_approve = args.auto_approve
    debug_mode = args.debug

    # Check for resume mode
    if args.resume:
        print(f"🔄 RESUME MODE")
        print(f"🆔 Session ID: {args.resume}")
        print("=" * 60)

        # Interactive config if not provided via CLI
        if not args.auto_approve:
            auto_approve = input("🤖 Auto-approve all decisions? (Y/n): ").lower().strip() != 'n'
        if not args.debug:
            debug_mode = input("🐛 Enable debug mode? (y/N): ").lower().strip() == 'y'

        runner = FullAutomationRunner(auto_approve=auto_approve, debug_mode=debug_mode)

        try:
            results = await runner.resume_automation(args.resume)

            if results["success"]:
                print(f"\n✅ SUCCESS! Session ID: {results['session_id']}")
                print(f"📁 Generated files: {len(results.get('files', []))}")
                for file in results.get('files', []):
                    print(f"   📄 {file}")
            else:
                print(f"\n❌ RESUME FAILED after {results.get('completed_stations', 0)} stations")
                print(f"💥 Error: {results.get('error', 'Unknown error')}")

        except KeyboardInterrupt:
            print("\n\n👋 Resume stopped by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n💥 Fatal error: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        # NEW AUTOMATION RUN
        # Get story concept from file or direct input
        story_concept = None
        
        # Check if test story concept file exists
        test_file = "test_story_concept.txt"
        if os.path.exists(test_file):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    story_concept = f.read().strip()
                print(f"✅ Using test story concept from file: {test_file}")
                print(f"📝 Story: {story_concept}")
            except Exception as e:
                print(f"❌ Error reading test file: {e}")
                story_concept = None
        
        while not story_concept or len(story_concept.strip()) < 10:
            concept_input = input("📝 Enter story concept file path or text (minimum 10 characters): ").strip()

            # Check if it's a file path
            if os.path.exists(concept_input):
                try:
                    with open(concept_input, 'r', encoding='utf-8') as f:
                        story_concept = f.read().strip()
                    print(f"✅ Loaded story concept from file: {concept_input}")
                except Exception as e:
                    print(f"❌ Error reading file: {e}")
                    continue
            else:
                story_concept = concept_input

            if len(story_concept) < 10:
                print("❌ Story concept too short. Please provide more detail.")

        # Configuration options (if not provided via CLI)
        print("\n⚙️  AUTOMATION CONFIGURATION:")
        if args.auto_approve:
            auto_approve = True
            print("🤖 Auto-approve: ✅ ENABLED")
        else:
            auto_approve = input("🤖 Auto-approve all decisions? (Y/n): ").lower().strip() != 'n'
        
        if args.debug:
            debug_mode = True
            print("🐛 Debug mode: ✅ ENABLED")
        elif args.auto_approve:
            # Default to no debug mode when auto-approve is set
            debug_mode = False
            print("🐛 Debug mode: ❌ DISABLED")
        else:
            debug_mode = input("🐛 Enable debug mode? (y/N): ").lower().strip() == 'y'

        # Initialize and run automation
        runner = FullAutomationRunner(auto_approve=auto_approve, debug_mode=debug_mode)

        try:
            results = await runner.run_full_automation(story_concept)

            if results["success"]:
                print(f"\n✅ SUCCESS! Session ID: {results['session_id']}")
                print(f"📁 Generated files: {len(results['files'])}")
                for file in results['files']:
                    print(f"   📄 {file}")
            else:
                print(f"\n❌ FAILED after {results['completed_stations']} stations")
                print(f"💥 Error: {results['error']}")

        except KeyboardInterrupt:
            session_id = getattr(runner, 'current_session_id', 'SESSION_ID')
            print("\n\n👋 Automation stopped by user.")
            print(f"💾 Progress saved to checkpoint")
            print(f"\n💡 TIP: Resume using: python full_automation.py --resume {session_id}")
            sys.exit(0)
        except Exception as e:
            print(f"\n💥 Fatal error: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())