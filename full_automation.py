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
        print(f"🏭 Pipeline: Station 1 → 2 → 3 → 4 → 4.5 → 5 → 6")
        print()
        
        # Initialize state
        state = AudiobookProductionState(story_concept)
        
        try:
            # Station 1: Seed Processing & Scale Evaluation
            state = await self._run_station_1(state)
            
            # Station 2: Project DNA Building
            state = await self._run_station_2(state)
            
            # Station 3: Age & Genre Optimization  
            state = await self._run_station_3(state)
            
            # Station 4: Reference Mining & Seed Extraction
            state = await self._run_station_4(state)
            
            # Station 4.5: Narrator Strategy Designer
            state = await self._run_station_4_5(state)
            
            # Station 5: Season Architecture
            state = await self._run_station_5(state)
            
            # Station 6: Master Style Guide
            state = await self._run_station_6(state)
            
            # Save checkpoint after each station
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
                "summary": "All 6 stations completed successfully"
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
            
            # Export to PDF
            try:
                pdf_path = processor.export_to_pdf(result, 
                    filename=f"station4_seedbank_{state.session_id}.pdf")
                state.generated_files.append(pdf_path)
                self.emit_progress("Station 4", 95, f"Exported seed bank to {pdf_path}")
            except Exception as e:
                logger.warning(f"PDF export failed: {e}")
            
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
            
            # Export to PDF
            try:
                pdf_path = processor.export_to_pdf(result, 
                    filename=f"station45_narrator_strategy_{state.session_id}.pdf")
                state.generated_files.append(pdf_path)
                self.emit_progress("Station 4.5", 95, f"Exported narrator strategy to {pdf_path}")
                logger.info(f"✅ Station 4.5 PDF exported: {pdf_path}")
            except Exception as e:
                logger.error(f"❌ PDF export failed: {e}")
                self.emit_progress("Station 4.5", 95, f"PDF export failed: {e}")
                
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
            
            # Store Station 5 output
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
                "created_timestamp": result.created_timestamp.isoformat()
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
                
            # Export PDF
            try:
                pdf_data = processor.export_to_pdf(result)
                pdf_filename = f"outputs/station5_season_architecture_{state.session_id}.pdf"
                os.makedirs(os.path.dirname(pdf_filename), exist_ok=True)
                with open(pdf_filename, 'wb') as f:
                    f.write(pdf_data)
                state.generated_files.append(pdf_filename)
                self.emit_progress("Station 5", 95, f"Exported PDF to {pdf_filename}")
            except Exception as e:
                logger.warning(f"PDF export failed: {e}")
            
            self.emit_progress("Station 5", 100, f"Station 5 completed! Chosen style: {result.chosen_style}")
            state.current_station = 5
            
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
                
            # Export PDF
            try:
                pdf_data = processor.export_to_pdf(result)
                pdf_filename = f"outputs/station6_master_style_guide_{state.session_id}.pdf"
                os.makedirs(os.path.dirname(pdf_filename), exist_ok=True)
                with open(pdf_filename, 'wb') as f:
                    f.write(pdf_data)
                state.generated_files.append(pdf_filename)
                self.emit_progress("Station 6", 95, f"Exported PDF to {pdf_filename}")
            except Exception as e:
                logger.warning(f"PDF export failed: {e}")
            
            self.emit_progress("Station 6", 100, f"Station 6 completed! Master Style Guide for {result.working_title}")
            state.current_station = 6
            
            return state
            
        except Exception as e:
            raise Exception(f"Station 6 failed: {str(e)}")
    
    
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
                "station_6": f"Master style guide: {state.station_outputs.get('station_6', {}).get('character_voices_count', 0)} character voices, {state.station_outputs.get('station_6', {}).get('audio_conventions_count', 0)} audio conventions"
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
            
            await self.redis.set(redis_key, json_data, expire=3600)  # Expire after 1 hour
            
            if self.debug_mode:
                logger.info(f"✅ Saved station {station_number} output to Redis: {redis_key}")
                
        except Exception as e:
            logger.error(f"❌ Failed to save station {station_number} to Redis: {e}")

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
    
    print("🎬 FULL AUDIOBOOK PRODUCTION AUTOMATION")
    print("=" * 60)
    print("🤖 Complete Pipeline: Station 1 → 2 → 3 → 4 → 4.5 → 5 → 6")
    print()
    
    # Get story concept
    story_concept = None
    while not story_concept or len(story_concept.strip()) < 10:
        story_concept = input("📝 Enter your story concept (minimum 10 characters): ").strip()
        if len(story_concept) < 10:
            print("❌ Story concept too short. Please provide more detail.")
    
    # Configuration options
    print("\n⚙️  AUTOMATION CONFIGURATION:")
    auto_approve = input("🤖 Auto-approve all decisions? (Y/n): ").lower().strip() != 'n'
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
        print("\n\n👋 Automation stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())