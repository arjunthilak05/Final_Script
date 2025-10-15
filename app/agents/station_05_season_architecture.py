#!/usr/bin/env python3
"""
Station 5: Season Architecture - Complete Implementation
You are the Season Architect using the complete 48-style SCREENPLAY STYLE LIBRARY
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from io import BytesIO

from app.redis_client import RedisClient
from app.agents.json_extractor import extract_json
from app.agents.config_loader import load_station_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScreenplayStyle(Enum):
    """Complete 48-style SCREENPLAY STYLE LIBRARY"""
    THREE_ACT_MICRO = "3-Act Micro"
    FIVE_ACT_MICRO = "5-Act Micro (Freytag Pyramid)"
    EIGHT_SEQUENCE = "8-Sequence Structure"
    KISHOTENKETSU = "Kishōtenketsu"
    BOTTLE_EPISODE = "Bottle Episode Structure"
    REAL_TIME = "Real-Time Structure"
    INVESTIGATION_DUEL = "Investigation Duel"
    CLASSIC_WHODUNIT = "Classic Whodunit"
    HOWCATCHEM = "Howcatchem (Inverted Mystery)"
    HEIST_STRUCTURE = "Heist Structure"
    WRONG_MAN_THRILLER = "Wrong-Man Thriller"
    CHASE_ENGINE = "Chase Engine"
    SURVIVAL_SIEGE = "Survival/Siege Structure"
    HYPERLINK = "Hyperlink Structure"
    NONLINEAR_TIME = "Nonlinear Time Structure"
    FRAME_NARRATIVE = "Frame Narrative"
    ANTHOLOGY_MOSAIC = "Anthology/Mosaic"
    MOCKUMENTARY = "Mockumentary Structure"
    FOUND_FOOTAGE = "Found Footage/Diegetic"
    MUSICAL_ANCHORS = "Musical Anchors Structure"
    COURTROOM_PROCEDURE = "Courtroom/Procedure"
    HEIST_GONE_WRONG = "Heist-Gone-Wrong"
    MYSTERY_BOX = "Mystery-Box Structure"
    ROAD_JOURNEY = "Road/Journey Structure"
    COMPETITION_LADDER = "Competition Ladder"
    COMING_OF_AGE_MICRO = "Coming-of-Age Micro"
    RISE_FALL_REDEMPTION = "Rise→Fall→Redemption Arc"
    TRAGIC_DOWNFALL = "Tragic Downfall Structure"
    CREATURE_FEATURE = "Creature Feature/Attack Cycles"
    DISASTER_COUNTDOWN = "Disaster/Countdown Structure"
    TIME_LOOP = "Time Loop Structure"
    TIME_TRAVEL = "Time Travel/Predestination"
    MULTIVERSE_PARALLEL = "Multiverse/Parallel Structure"
    SOCIAL_PARABLE = "Social Parable/Satire"
    POETIC_ELLIPTICAL = "Poetic/Elliptical Structure"
    ROMANCE_ENGINE = "Romance Engine"
    ACTION_DRIP = "Action Drip Structure"
    BOTTLE_INTERROGATION = "Bottle Interrogation"
    TECH_THRILLER = "Tech-Thriller Pulse"
    CYBER_NOIR = "Cyber-Noir Structure"
    ETHICAL_DILEMMA = "Ethical Dilemma Framework"
    EPISODIC_PUZZLE = "Episodic Puzzle Structure"
    NETWORK_DIVE = "Network Dive Structure"
    BLIND_SPOT_CITY = "Blind-Spot City"
    FAMILY_THREAD = "Family Thread Structure"
    RASHOMON = "Rashomon Structure"
    FIBONACCI = "Fibonacci Structure"
    RING_COMPOSITION = "Ring Composition"

@dataclass
class StyleRecommendation:
    """Individual style recommendation with complete analysis"""
    style_name: str
    fit_reasoning: str
    audio_adaptation: str 
    episode_implications: str
    demo_script: str
    confidence_score: float
    narrator_integration: str = ""

@dataclass
class MacroStructure:
    """Season-level act structure mapping (supports 2/3/4-act structures)"""
    act_1_episodes: List[int]
    act_2a_episodes: List[int] = None
    act_2b_episodes: List[int] = None
    act_3_episodes: List[int] = None
    act_2_episodes: List[int] = None  # For 2-act and 3-act structures
    structure_explanation: str = ""
    total_episodes: int = 0

    def __post_init__(self):
        # Convert None to empty lists for consistency
        if self.act_2a_episodes is None:
            self.act_2a_episodes = []
        if self.act_2b_episodes is None:
            self.act_2b_episodes = []
        if self.act_3_episodes is None:
            self.act_3_episodes = []
        if self.act_2_episodes is None:
            self.act_2_episodes = []

@dataclass
class EpisodeSlot:
    """Individual episode specification"""
    episode_number: int
    primary_function: str
    energy_level: int
    subplot_focus: str
    cliffhanger_type: str
    act_equivalent: str
    special_notes: str

@dataclass
class RhythmMapping:
    """Complete season pacing and rhythm analysis"""
    tension_peaks: List[int]
    breathing_room: List[int]
    format_breaks: List[List[str]]
    revelation_cascade_points: List[List[str]]
    energy_curve: List[int]
    pacing_strategy: Dict[str, str]
    narrator_rhythm_integration: str

@dataclass
class SeasonStructureDocument:
    """Complete Season Architecture output"""
    working_title: str
    session_id: str
    created_timestamp: datetime
    
    # Style Analysis
    style_recommendations: List[StyleRecommendation]
    chosen_style: str
    recommended_choice: str
    
    # Season Structure
    macro_structure: MacroStructure
    episode_grid: List[EpisodeSlot]
    rhythm_mapping: RhythmMapping
    
    # Integration
    narrator_integration: str
    production_considerations: List[str]
    
    # Foundation Context
    project_context: Dict[str, Any]
    comprehensive_profile: Dict[str, str]

class Station05SeasonArchitect:
    """Complete Season Architecture Builder using 48-style SCREENPLAY STYLE LIBRARY"""
    
    def __init__(self):
        self.session_id = None
        self.style_library = self._load_complete_style_library()
        self.openrouter = None
        self.redis = None
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=5)
        
    async def initialize(self):
        """Initialize OpenRouter client and Redis for AI processing"""
        from app.openrouter_agent import OpenRouterAgent
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        await self.redis.initialize()
        logger.info("Station 5: Season Architect initialized with 48-style library")
        
    def _load_complete_style_library(self) -> Dict[str, Dict[str, str]]:
        """Complete 48-style SCREENPLAY STYLE LIBRARY with full definitions"""
        return {
            "3-Act Micro": {
                "definition": "Classic setup/confrontation/resolution compressed for episodes",
                "audio_markers": "Clear act breaks via music/silence, inciting incident at ~3-5 min",
                "best_for": "Traditional story arcs"
            },
            "5-Act Micro (Freytag Pyramid)": {
                "definition": "Exposition→Rising Action→Climax→Falling Action→Denouement",
                "audio_markers": "Sound density increases toward climax",
                "best_for": "Dramatic stories with emotional peaks"
            },
            "8-Sequence Structure": {
                "definition": "8 mini-movements with turns at 25%, 50%, 75%",
                "audio_markers": "Motif returns at quarter-marks",
                "best_for": "Complex narratives"
            },
            "Kishōtenketsu": {
                "definition": "Japanese 4-act Introduction→Development→Twist→Reconciliation",
                "audio_markers": "Reveal through contrast, ambient shift at twist",
                "best_for": "Revelation-focused stories"
            },
            "Bottle Episode Structure": {
                "definition": "Single location, real-time pressure cooker",
                "audio_markers": "Room tone evolves, no location changes",
                "best_for": "Character studies, budget constraints"
            },
            "Real-Time Structure": {
                "definition": "Story time equals listening time exactly",
                "audio_markers": "Clock ticking, real-world time references",
                "best_for": "Thrillers, countdown scenarios"
            },
            "Investigation Duel": {
                "definition": "Two perspectives investigating same truth",
                "audio_markers": "Overlapping VO, alternating POV",
                "best_for": "Multiple detective mysteries"
            },
            "Classic Whodunit": {
                "definition": "Closed-circle mystery, all suspects present",
                "audio_markers": "Fair clues as sound hints",
                "best_for": "Traditional mysteries"
            },
            "Howcatchem (Inverted Mystery)": {
                "definition": "Audience knows culprit",
                "audio_markers": "Procedural sounds, evidence collection",
                "best_for": "Columbo-style cat-and-mouse"
            },
            "Heist Structure": {
                "definition": "Assemble→Plan→Execute→Twist→Consequence",
                "audio_markers": "Planning beats mirror execution SFX",
                "best_for": "Capers, team adventures"
            },
            "Wrong-Man Thriller": {
                "definition": "Innocent accused, must prove innocence",
                "audio_markers": "Pursuit rhythms, paranoid soundscape",
                "best_for": "Hitchcockian suspense"
            },
            "Chase Engine": {
                "definition": "Continuous pursuit drives narrative",
                "audio_markers": "Evolving chase sounds, location shifts",
                "best_for": "Relentless pacing"
            },
            "Survival/Siege Structure": {
                "definition": "Attrition cycles, dwindling resources",
                "audio_markers": "Resource inventory sounds, environmental pressure",
                "best_for": "Horror, disaster stories"
            },
            "Hyperlink Structure": {
                "definition": "Multiple parallel stories, common theme",
                "audio_markers": "Distinct ambience per storyline",
                "best_for": "Ensemble casts"
            },
            "Nonlinear Time Structure": {
                "definition": "Time jumps reframe meaning",
                "audio_markers": "Temporal cue sounds, narrator timestamps",
                "best_for": "Puzzle-driven stories"
            },
            "Frame Narrative": {
                "definition": "Story within story",
                "audio_markers": "Narrator voice shifts between levels",
                "best_for": "Folkloric tales, unreliable narrators"
            },
            "Anthology/Mosaic": {
                "definition": "Connected separate stories",
                "audio_markers": "Reset motif between segments",
                "best_for": "Multi-angle theme exploration"
            },
            "Mockumentary Structure": {
                "definition": "Fake documentary format",
                "audio_markers": "Interview acoustics, archival quality",
                "best_for": "Satire, institutional critique"
            },
            "Found Footage/Diegetic": {
                "definition": "All audio from in-world devices",
                "audio_markers": "Device limitations, recording beeps",
                "best_for": "Horror, authenticity illusion"
            },
            "Musical Anchors Structure": {
                "definition": "Songs drive act breaks",
                "audio_markers": "Leitmotif progression",
                "best_for": "Emotional journeys"
            },
            "Courtroom/Procedure": {
                "definition": "Truth through formal process",
                "audio_markers": "Gavel sounds, formal speech patterns",
                "best_for": "Legal dramas"
            },
            "Heist-Gone-Wrong": {
                "definition": "Plan fails, cascading complications",
                "audio_markers": "Plan motif breaking down",
                "best_for": "Dark comedy"
            },
            "Mystery-Box Structure": {
                "definition": "Questions spawn more questions",
                "audio_markers": "Curiosity cadence, question patterns",
                "best_for": "Long-form mysteries"
            },
            "Road/Journey Structure": {
                "definition": "Physical journey mirrors growth",
                "audio_markers": "Transit ambience, changing acoustics",
                "best_for": "Coming-of-age"
            },
            "Competition Ladder": {
                "definition": "Elimination rounds to final confrontation",
                "audio_markers": "Crowd reactions, tension ratcheting",
                "best_for": "Sports stories"
            },
            "Coming-of-Age Micro": {
                "definition": "Growth through small choices",
                "audio_markers": "Voice maturation, motif evolution",
                "best_for": "Young adult transformation"
            },
            "Rise→Fall→Redemption Arc": {
                "definition": "Success, failure, comeback",
                "audio_markers": "Motif brightens→darkens→transforms",
                "best_for": "Morality tales"
            },
            "Tragic Downfall Structure": {
                "definition": "Fatal flaw leads to destruction",
                "audio_markers": "Motif gradually corrupts",
                "best_for": "Classical tragedy"
            },
            "Creature Feature/Attack Cycles": {
                "definition": "Monster approach→strike→regroup→adapt",
                "audio_markers": "Creature signatures, evolving patterns",
                "best_for": "Horror"
            },
            "Disaster/Countdown Structure": {
                "definition": "Ticking clock to catastrophe",
                "audio_markers": "Countdown beeps, urgency rhythms",
                "best_for": "Prevention missions"
            },
            "Time Loop Structure": {
                "definition": "Repetition with variation",
                "audio_markers": "Loop reset chime, cycle variations",
                "best_for": "Philosophical growth"
            },
            "Time Travel/Predestination": {
                "definition": "Cause-effect paradoxes",
                "audio_markers": "Temporal transitions, era ambience",
                "best_for": "Sci-fi puzzles"
            },
            "Multiverse/Parallel Structure": {
                "definition": "Alternate realities, different choices",
                "audio_markers": "Dimensional shifts, reality signatures",
                "best_for": "What-if scenarios"
            },
            "Social Parable/Satire": {
                "definition": "Story levels expose systemic issues",
                "audio_markers": "Public space ambience",
                "best_for": "Social commentary"
            },
            "Poetic/Elliptical Structure": {
                "definition": "Mood over linear plot",
                "audio_markers": "Sensory details, abstract soundscapes",
                "best_for": "Artistic narratives"
            },
            "Romance Engine": {
                "definition": "Meet→Fun→Apart→Gesture→Resolution",
                "audio_markers": "Intimate acoustics, breathing patterns",
                "best_for": "Love stories"
            },
            "Action Drip Structure": {
                "definition": "Brief action bursts punctuate character moments",
                "audio_markers": "Intense sequences, breathing space",
                "best_for": "Character-driven action"
            },
            "Bottle Interrogation": {
                "definition": "Confined Q&A drives reveals",
                "audio_markers": "Chair creaks, voice proximity changes",
                "best_for": "Psychological pressure"
            },
            "Tech-Thriller Pulse": {
                "definition": "Digital puzzles + physical chase",
                "audio_markers": "UI sounds, system alerts",
                "best_for": "Hacker stories"
            },
            "Cyber-Noir Structure": {
                "definition": "Digital noir, tech replacing shadows",
                "audio_markers": "Electronic hum, quiet dread",
                "best_for": "Future noir"
            },
            "Ethical Dilemma Framework": {
                "definition": "Each choice has moral cost",
                "audio_markers": "Heartbeat, decision pauses",
                "best_for": "Philosophical drama"
            },
            "Episodic Puzzle Structure": {
                "definition": "Scenes unlock through discovered connections",
                "audio_markers": "Discovery sounds, revelation triggers",
                "best_for": "Mystery stories"
            },
            "Network Dive Structure": {
                "definition": "Story unfolds in digital space",
                "audio_markers": "Digital textures, data streams",
                "best_for": "Cyberpunk"
            },
            "Blind-Spot City": {
                "definition": "Hidden world alongside normal",
                "audio_markers": "Phasing ambience at boundaries",
                "best_for": "Urban fantasy"
            },
            "Family Thread Structure": {
                "definition": "Domestic stakes drive drama",
                "audio_markers": "Household sounds, morning routines",
                "best_for": "Family drama"
            },
            "Rashomon Structure": {
                "definition": "Same events, contradicting perspectives",
                "audio_markers": "POV-specific acoustic treatment",
                "best_for": "Truth exploration"
            },
            "Fibonacci Structure": {
                "definition": "Each segment = sum of previous two",
                "audio_markers": "Mathematical scene progression",
                "best_for": "Experimental narratives"
            },
            "Ring Composition": {
                "definition": "Story ends where it began, transformed",
                "audio_markers": "Opening motif returns transformed",
                "best_for": "Circular narratives"
            }
        }
    
    async def process(self, session_id: str) -> SeasonStructureDocument:
        """
        Main processing method: Complete Season Architecture
        Now uses unified JSON approach for simplicity and reliability
        """
        self.session_id = session_id
        logger.info(f"Starting Station 5: Season Architecture for session {session_id}")

        # Gather comprehensive inputs from Stations 1-4.5
        project_inputs = await self._gather_comprehensive_inputs(session_id)

        # Build unified context for single LLM call
        project_context = self._build_project_context(project_inputs)

        # Single unified LLM call using YML config
        logger.info("Requesting complete season architecture from LLM...")
        response = await self.openrouter.process_message(
            project_context,
            model_name=self.config.model,
            max_tokens=self.config.max_tokens
        )

        # Parse comprehensive JSON response
        season_data = await self._parse_complete_response(response, project_inputs, session_id)

        # Save to Redis
        try:
            output_dict = self.export_to_json(season_data)
            key = f"audiobook:{session_id}:station_05"
            json_str = json.dumps(output_dict, default=str)
            await self.redis.set(key, json_str, expire=86400)
            logger.info(f"Station 5 output stored successfully in Redis")
        except Exception as e:
            logger.error(f"Failed to store Station 5 output: {str(e)}")
            raise

        logger.info(f"Station 5 completed: {season_data.chosen_style} architecture")
        return season_data
    
    async def _gather_comprehensive_inputs(self, session_id: str) -> Dict[str, Any]:
        """
        Gather and integrate inputs from ALL previous stations exactly as specified
        """
        logger.info("Gathering comprehensive inputs from Stations 1-4.5")
        
        inputs = {
            "session_id": session_id,
            "working_title": "Untitled Audio Drama",  # Default fallback
            "episode_count": "10",
            "episode_length": "45 minutes",
            "core_premise": "",
            "primary_genre": "Drama",
            "secondary_genres": [],
            "target_age_range": "25-45",
            "content_rating": "PG-13",
            "total_seeds": 0,
            "narrator_strategy": "Limited Omniscient",
            "narrator_presence_level": "Moderate",
            "comprehensive_profile": {}
        }
        
        # Station 1: Scale choice, working titles, core premise
        try:
            station1_data = await self.redis.get(f"audiobook:{session_id}:station_01")
            if station1_data:
                station1 = json.loads(station1_data)
                scale_options = station1.get("scale_options", [])
                recommended_option = station1.get("recommended_option", 1)
                
                try:
                    scale_index = int(recommended_option) - 1
                    scale_data = scale_options[scale_index] if 0 <= scale_index < len(scale_options) else {}
                except (ValueError, TypeError):
                    scale_data = scale_options[0] if scale_options else {}
                
                # Get working title from the first option in working_titles array
                working_titles = station1.get("initial_expansion", {}).get("working_titles", [])
                working_title = working_titles[0] if working_titles else "Untitled Audio Drama"
                
                # Extract main characters from Station 1
                main_characters = station1.get("initial_expansion", {}).get("main_characters", [])
                
                inputs.update({
                    "working_title": working_title,
                    "core_premise": station1.get("initial_expansion", {}).get("core_premise", ""),
                    "original_seed": station1.get("original_seed", ""),
                    "main_characters": main_characters,
                    "episode_count": scale_data.get("episode_count", "10"),
                    "episode_length": scale_data.get("episode_length", "45 minutes"),
                    "scale_rationale": scale_data.get("rationale", ""),
                    "production_complexity": scale_data.get("production_complexity", "Standard")
                })
                logger.info(f"Station 1 data loaded: {inputs['working_title']}")
        except Exception as e:
            logger.warning(f"Failed to load Station 1 data: {e}")
        
        # Station 2: Project Bible (world setting, genre blend, audience profile)
        try:
            station2_data = await self.redis.get(f"audiobook:{session_id}:station_02")
            if station2_data:
                station2 = json.loads(station2_data)
                inputs.update({
                    "primary_genre": station2.get("genre_tone", {}).get("primary_genre", "Drama"),
                    "secondary_genres": station2.get("genre_tone", {}).get("secondary_genres", []),
                    "world_setting": station2.get("world_setting", {}),
                    "audience_profile": station2.get("audience_profile", {}),
                    "format_specifications": station2.get("format_specifications", {}),
                    "production_constraints": station2.get("production_constraints", {})
                })
                logger.info(f"Station 2 data loaded: {inputs['primary_genre']}")
        except Exception as e:
            logger.warning(f"Failed to load Station 2 data: {e}")
        
        # Station 3: Age guidelines, tone calibration
        try:
            station3_data = await self.redis.get(f"audiobook:{session_id}:station_03")
            if station3_data:
                station3 = json.loads(station3_data)
                inputs.update({
                    "target_age_range": station3.get("age_guidelines", {}).get("target_age_range", "25-45"),
                    "content_rating": station3.get("age_guidelines", {}).get("content_rating", "PG-13"),
                    "tone_calibration": station3.get("tone_calibration", {}),
                    "chosen_genre_blend": station3.get("chosen_genre_blend", "")
                })
                logger.info(f"Station 3 data loaded: {inputs['target_age_range']} ({inputs['content_rating']})")
        except Exception as e:
            logger.warning(f"Failed to load Station 3 data: {e}")
        
        # Station 4: Story seed bank
        try:
            station4_data = await self.redis.get(f"audiobook:{session_id}:station_04")
            if station4_data:
                station4 = json.loads(station4_data)
                seed_collection = station4.get("seed_collection", {})
                inputs.update({
                    "total_seeds": station4.get("total_seeds", 0),
                    "micro_moments": seed_collection.get("micro_moments", 0),
                    "episode_beats": seed_collection.get("episode_beats", 0), 
                    "season_arcs": seed_collection.get("season_arcs", 0),
                    "series_defining": seed_collection.get("series_defining", 0),
                    "story_foundation": seed_collection
                })
                logger.info(f"Station 4 data loaded: {inputs['total_seeds']} story seeds")
        except Exception as e:
            logger.warning(f"Failed to load Station 4 data: {e}")
        
        # Station 4.5: Narrator strategy
        try:
            station45_data = await self.redis.get(f"audiobook:{session_id}:station_04_5")
            if station45_data:
                station45 = json.loads(station45_data)
                narrator_strategy = station45.get("narrator_strategy", {})
                inputs.update({
                    "narrator_recommendation": station45.get("recommendation", "LIMITED_OMNISCIENT"),
                    "narrator_strategy": narrator_strategy.get("identity_type", "Limited Omniscient"),
                    "narrator_presence_level": narrator_strategy.get("presence_level", "Moderate"),
                    "narrator_config": {
                        "voice_casting": narrator_strategy.get("voice_casting_notes", "Professional narrator"),
                        "key_functions": narrator_strategy.get("key_functions", []),
                        "sample_lines": narrator_strategy.get("sample_narrator_lines", [])
                    },
                    "sample_scenes": station45.get("sample_scenes", [])
                })
                logger.info(f"Station 4.5 data loaded: {inputs['narrator_strategy']}")
        except Exception as e:
            logger.warning(f"Failed to load Station 4.5 data: {e}")
        
        # Create comprehensive profile
        inputs["comprehensive_profile"] = {
            "scale": f"{inputs['episode_count']} episodes × {inputs['episode_length']}",
            "genre_blend": f"{inputs['primary_genre']}" + (f" + {' + '.join(inputs['secondary_genres'])}" if inputs['secondary_genres'] else ""),
            "audience_target": f"{inputs['target_age_range']} ({inputs['content_rating']})",
            "story_foundation": f"{inputs['total_seeds']} narrative seeds available",
            "narrator_integration": f"{inputs['narrator_strategy']} with {inputs['narrator_presence_level'].lower()} presence",
            "production_readiness": "Complete foundation from Stations 1-4.5"
        }
        
        logger.info(f"Comprehensive inputs gathered for '{inputs['working_title']}' - {inputs['comprehensive_profile']['genre_blend']}")
        return inputs

    def _build_project_context(self, project_inputs: Dict[str, Any]) -> str:
        """Build unified project context string for LLM prompt"""
        return f"""
PROJECT: {project_inputs.get('working_title', 'Untitled')}
GENRE: {project_inputs.get('primary_genre', 'Drama')} + {', '.join(project_inputs.get('secondary_genres', []))}
EPISODES: {project_inputs.get('episode_count', '10')} x {project_inputs.get('episode_length', '45 min')}
TARGET AGE: {project_inputs.get('target_age_range', '25-45')}
PREMISE: {project_inputs.get('core_premise', project_inputs.get('original_seed', 'Story premise'))}
NARRATOR: {project_inputs.get('narrator_strategy', 'Limited')} ({project_inputs.get('narrator_presence_level', 'Moderate')})
"""

    async def _parse_complete_response(self, response: str, project_inputs: Dict[str, Any], session_id: str) -> SeasonStructureDocument:
        """Parse comprehensive JSON response into SeasonStructureDocument"""
        try:
            data = extract_json(response)

            # Parse style recommendations
            style_recommendations = []
            for style_data in data.get("style_recommendations", [])[:3]:
                style_recommendations.append(StyleRecommendation(
                    style_name=style_data.get("style_name", "3-Act Micro"),
                    fit_reasoning=style_data.get("fit_reasoning", "Fits the narrative structure"),
                    audio_adaptation=style_data.get("audio_adaptation", "Clear audio transitions"),
                    episode_implications=style_data.get("episode_implications", "Structured pacing"),
                    demo_script=style_data.get("demo_script", "Demo script placeholder"),
                    confidence_score=float(style_data.get("confidence_score", 0.8)),
                    narrator_integration=style_data.get("narrator_integration", "Moderate narrator presence")
                ))

            # Parse macro structure
            macro_data = data.get("macro_structure", {})
            macro_structure = MacroStructure(
                act_1_episodes=macro_data.get("act_1_episodes", [1, 2, 3]),
                act_2_episodes=macro_data.get("act_2_episodes", [4, 5, 6, 7]),
                act_3_episodes=macro_data.get("act_3_episodes", [8, 9, 10]),
                structure_explanation=macro_data.get("structure_explanation", "Three-act structure"),
                total_episodes=int(project_inputs.get('episode_count', 10))
            )

            # Parse episode grid
            episode_grid = []
            for ep_data in data.get("episode_grid", []):
                episode_grid.append(EpisodeSlot(
                    episode_number=ep_data.get("episode_number", 1),
                    primary_function=ep_data.get("primary_function", "Story progression"),
                    energy_level=ep_data.get("energy_level", 5),
                    subplot_focus=ep_data.get("subplot_focus", "Main plot"),
                    cliffhanger_type=ep_data.get("cliffhanger_type", "Reveal"),
                    act_equivalent=ep_data.get("act_equivalent", "Act 1"),
                    special_notes=ep_data.get("special_notes", "")
                ))

            # Parse rhythm mapping
            rhythm_data = data.get("rhythm_mapping", {})
            rhythm_mapping = RhythmMapping(
                tension_peaks=rhythm_data.get("tension_peaks", [3, 7, 10]),
                breathing_room=rhythm_data.get("breathing_room", [2, 5]),
                format_breaks=[rhythm_data.get("format_breaks", [])],
                revelation_cascade_points=[rhythm_data.get("revelation_cascade_points", [])],
                energy_curve=rhythm_data.get("energy_curve", [5, 6, 7, 8, 7, 8, 9, 8, 9, 10]),
                pacing_strategy=rhythm_data.get("pacing_strategy", {}),
                narrator_rhythm_integration=rhythm_data.get("narrator_rhythm_integration", "Consistent narrator use")
            )

            # Create complete document
            return SeasonStructureDocument(
                working_title=project_inputs.get('working_title', 'Untitled'),
                session_id=session_id,
                created_timestamp=datetime.utcnow(),
                style_recommendations=style_recommendations,
                chosen_style=style_recommendations[0].style_name if style_recommendations else "3-Act Micro",
                recommended_choice=style_recommendations[0].style_name if style_recommendations else "3-Act Micro",
                macro_structure=macro_structure,
                episode_grid=episode_grid,
                rhythm_mapping=rhythm_mapping,
                narrator_integration=style_recommendations[0].narrator_integration if style_recommendations else "Moderate",
                production_considerations=["Audio-optimized structure", "Clear scene transitions"],
                project_context=project_inputs,
                comprehensive_profile=project_inputs.get('comprehensive_profile', {})
            )

        except Exception as e:
            logger.error(f"Failed to parse complete response: {str(e)}")
            raise ValueError(f"Station 5 JSON parsing failed: {str(e)}")

    def export_to_text(self, season_document: SeasonStructureDocument) -> str:
        """
        Export complete Season Structure Document to formatted text matching your specification
        """
        output_lines = []
        
        # Header
        output_lines.extend([
            "STATION 5: SEASON ARCHITECTURE",
            "=" * 80,
            "You are the Season Architect using SCREENPLAY STYLE LIBRARY.",
            "",
            "TASK 1: STYLE SELECTION",
            "Review the 48+ screenplay styles in library.",
            "Recommend top 3 styles for this project:",
            "",
            f"Working Title: {season_document.working_title}",
            f"Session ID: {season_document.session_id}",
            f"Created: {season_document.created_timestamp}",
            "",
            f"CHOSEN SCREENPLAY STYLE:",
            f"{season_document.chosen_style}",
            f"Confidence: {season_document.style_recommendations[0].confidence_score * 100:.1f}%",
            "",
            "TOP 3 STYLE RECOMMENDATIONS:",
            "-" * 50
        ])
        
        # Style Recommendations
        for i, style in enumerate(season_document.style_recommendations, 1):
            output_lines.extend([
                f"{i}. {style.style_name} (Confidence: {style.confidence_score * 100:.1f}%)",
                "",
                "WHY IT FITS OUR STORY:",
                style.fit_reasoning,
                "",
                "HOW IT WORKS IN AUDIO:",
                style.audio_adaptation,
                "",
                "EPISODE STRUCTURE IMPLICATIONS:",
                style.episode_implications,
                "",
                "DEMO SCRIPT (500 words):",
                "-" * 40,
                style.demo_script,
                "-" * 40,
                "",
                "=" * 50,
                ""
            ])
        
        # Task 2: Season Skeleton
        output_lines.extend([
            "TASK 2: SEASON SKELETON",
            "For chosen style, create:",
            "",
            "MACRO STRUCTURE:",
            f"Episodes {'-'.join(map(str, season_document.macro_structure.act_1_episodes))}: Act 1 equivalent (Setup)",
            f"Episodes {'-'.join(map(str, season_document.macro_structure.act_2a_episodes))}: Act 2A equivalent (Rising Action)",
            f"Episodes {'-'.join(map(str, season_document.macro_structure.act_2b_episodes))}: Act 2B equivalent (Complications)",
            f"Episodes {'-'.join(map(str, season_document.macro_structure.act_3_episodes))}: Act 3 equivalent (Resolution)",
            "",
            "MICRO STRUCTURE:",
            "For each episode slot:",
            "- Primary function (setup/complication/revelation/resolution)",
            "- Energy level (1-10)",
            "- Subplot focus",
            "- Cliffhanger type",
            "",
            "COMPLETE EPISODE GRID:",
            "=" * 60
        ])
        
        # Episode Grid
        for episode in season_document.episode_grid:
            special_indicators = []
            
            # Determine episode type
            if episode.episode_number in season_document.rhythm_mapping.tension_peaks:
                special_indicators.append("⚡ TENSION PEAK EPISODE")
            if episode.episode_number in season_document.rhythm_mapping.breathing_room:
                special_indicators.append("💨 BREATHING ROOM EPISODE")
            
            # Check for revelations
            revelations = []
            for cascade_point in season_document.rhythm_mapping.revelation_cascade_points:
                if cascade_point[0] == episode.episode_number:
                    revelations.append(cascade_point[1])
            
            output_lines.append(f"Episode {episode.episode_number}: {episode.primary_function} (Energy: {episode.energy_level}/10, {episode.act_equivalent})")
            output_lines.append(f"  Subplot Focus: {episode.subplot_focus}")
            output_lines.append(f"  Cliffhanger Type: {episode.cliffhanger_type}")
            
            for indicator in special_indicators:
                output_lines.append(f"  {indicator}")
            
            if revelations:
                for revelation in revelations:
                    output_lines.append(f"  Revelations: {revelation}")
            
            output_lines.append("")
        
        # Task 3: Rhythm Mapping
        output_lines.extend([
            "TASK 3: RHYTHM MAPPING",
            "- Tension peaks (which episodes)",
            "- Breathing room (which episodes)", 
            "- Format breaks (special episodes)",
            "- Revelation cascade points",
            "",
            f"TENSION PEAKS: Episodes {season_document.rhythm_mapping.tension_peaks}",
            f"BREATHING ROOM: Episodes {season_document.rhythm_mapping.breathing_room}",
            f"ENERGY CURVE: {season_document.rhythm_mapping.energy_curve}",
            "",
            "FORMAT BREAKS (Special Episodes):"
        ])
        
        if season_document.rhythm_mapping.format_breaks:
            for break_info in season_document.rhythm_mapping.format_breaks:
                output_lines.append(f"Episode {break_info[0]}: {break_info[1]}")
        else:
            output_lines.append("No special format episodes planned")
        
        output_lines.extend([
            "",
            "REVELATION CASCADE POINTS:"
        ])
        
        for cascade_point in season_document.rhythm_mapping.revelation_cascade_points:
            output_lines.append(f"Episode {cascade_point[0]}: {cascade_point[1]}")
        
        # Final sections
        output_lines.extend([
            "",
            "OUTPUT: Season Structure Document with episode grid",
            "=" * 60,
            "",
            "NARRATOR INTEGRATION:",
            season_document.narrator_integration,
            "",
            "IMPLEMENTATION GUIDELINES:",
            "• Follow chosen screenplay style conventions",
            "• Maintain energy curve across episodes", 
            "• Integrate narrator strategy with pacing",
            "• Balance tension peaks with breathing room",
            "",
            "PRODUCTION NOTES:"
        ])
        
        for note in season_document.production_considerations:
            output_lines.append(f"• {note}")
        
        # Complete Style Library
        output_lines.extend([
            "",
            "COMPLETE SCREENPLAY STYLE LIBRARY",
            "Every style explicitly defined - no assumptions",
            "",
            "SCREENPLAY STYLE LIBRARY - COMPLETE LIST WITH DEFINITIONS",
            "(48 styles total - showing first 10 examples)",
            ""
        ])
        
        # Add first 10 styles from library
        library_items = list(self.style_library.items())[:10]
        for i, (style_name, style_data) in enumerate(library_items, 1):
            output_lines.append(f"{i}. {style_name}: {style_data['definition']}")
        
        output_lines.append("")
        output_lines.append("[Plus 38 additional styles in complete library...]")
        
        return "\n".join(output_lines)
    
    def export_to_json(self, season_document: SeasonStructureDocument) -> Dict[str, Any]:
        """
        Export complete Season Structure Document to JSON format
        """
        # Convert episode grid to JSON format
        episode_grid_json = []
        for episode in season_document.episode_grid:
            episode_data = {
                "episode_number": episode.episode_number,
                "primary_function": episode.primary_function,
                "energy_level": episode.energy_level,
                "subplot_focus": episode.subplot_focus,
                "cliffhanger_type": episode.cliffhanger_type,
                "act_equivalent": episode.act_equivalent,
                "tension_peak": episode.episode_number in season_document.rhythm_mapping.tension_peaks,
                "breathing_room": episode.episode_number in season_document.rhythm_mapping.breathing_room,
                "format_break": any(episode.episode_number == fb[0] for fb in season_document.rhythm_mapping.format_breaks),
                "revelation_cascade": [rcp[1] for rcp in season_document.rhythm_mapping.revelation_cascade_points if rcp[0] == episode.episode_number]
            }
            episode_grid_json.append(episode_data)
        
        return {
            "station_id": "station_05",
            "working_title": season_document.working_title,
            "session_id": season_document.session_id,
            "created_timestamp": season_document.created_timestamp.isoformat(),
            "total_episodes": season_document.macro_structure.total_episodes,  # Add for easy access
            "chosen_style": season_document.chosen_style,
            "style_recommendations": [
                {
                    "style": rec.style_name,
                    "fit_reasoning": rec.fit_reasoning,
                    "audio_adaptation": rec.audio_adaptation,
                    "episode_implications": rec.episode_implications,
                    "demo_script": rec.demo_script,
                    "confidence_score": rec.confidence_score
                }
                for rec in season_document.style_recommendations
            ],
            "macro_structure": {
                "act_1_episodes": season_document.macro_structure.act_1_episodes,
                "act_2_episodes": season_document.macro_structure.act_2_episodes or [],  # For 2/3-act structures
                "act_2a_episodes": season_document.macro_structure.act_2a_episodes or [],
                "act_2b_episodes": season_document.macro_structure.act_2b_episodes or [],
                "act_3_episodes": season_document.macro_structure.act_3_episodes or [],
                "total_episodes": season_document.macro_structure.total_episodes
            },
            "episode_grid": episode_grid_json,
            "rhythm_mapping": {
                "tension_peaks": season_document.rhythm_mapping.tension_peaks,
                "breathing_room": season_document.rhythm_mapping.breathing_room,
                "format_breaks": season_document.rhythm_mapping.format_breaks,
                "revelation_cascade_points": season_document.rhythm_mapping.revelation_cascade_points,
                "energy_curve": season_document.rhythm_mapping.energy_curve
            },
            "narrator_integration": season_document.narrator_integration,
            "production_notes": season_document.production_considerations,
            "implementation_guidelines": [
                "Follow chosen screenplay style conventions",
                "Maintain energy curve across episodes",
                "Integrate narrator strategy with pacing",
                "Balance tension peaks with breathing room"
            ]
        }
    
    # PDF export removed - use JSON and TXT formats instead
    # def export_to_pdf(self, season_document: SeasonStructureDocument) -> bytes:
    #     """Export complete Season Structure Document to PDF format - REMOVED"""
    #     pass
