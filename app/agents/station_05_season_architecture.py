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
        Follows your exact specification for Station 5
        """
        self.session_id = session_id
        logger.info(f"Starting Station 5: Season Architecture for session {session_id}")
        
        # Gather comprehensive inputs from Stations 1-4.5
        project_inputs = await self._gather_comprehensive_inputs(session_id)
        
        # TASK 1: STYLE SELECTION - Review 48 styles, recommend TOP 3
        style_recommendations = await self._analyze_48_styles(project_inputs)
        
        # TASK 2: SEASON SKELETON - Create complete season architecture
        season_structure = await self._create_season_skeleton(project_inputs, style_recommendations)
        
        # TASK 3: RHYTHM MAPPING - Design sophisticated pacing
        rhythm_mapping = await self._design_rhythm_mapping(project_inputs, season_structure)
        
        # Package complete Season Structure Document
        season_document = self._create_complete_document(
            project_inputs, style_recommendations, season_structure, rhythm_mapping, session_id
        )
        
        # Save to Redis before returning
        try:
            output_dict = self.export_to_json(season_document)
            key = f"audiobook:{session_id}:station_05"
            json_str = json.dumps(output_dict, default=str)
            await self.redis.set(key, json_str, expire=86400)  # 24 hour expiry
            logger.info(f"Station 5 output stored successfully in Redis at key: {key}")
        except Exception as e:
            logger.error(f"Failed to store Station 5 output to Redis: {str(e)}")
            raise
        
        logger.info(f"Station 5 completed: {season_document.chosen_style} architecture")
        return season_document
    
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
    
    async def _analyze_48_styles(self, project_inputs: Dict[str, Any]) -> List[StyleRecommendation]:
        """
        TASK 1: STYLE SELECTION
        Review the 48 screenplay styles, recommend TOP 3 with comprehensive analysis
        """
        logger.info("Analyzing 48 screenplay styles for optimal selection")
        
        # Style analysis with retry logic
        max_retries = 5
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    logger.info(f"🔄 Style analysis retry attempt {attempt + 1}/{max_retries}")
                    await asyncio.sleep(retry_delay * attempt)
                
                # Generate style recommendations using LLM analysis
                style_prompt = self._build_style_analysis_prompt(project_inputs)
                response = await self.openrouter.process_message(
                    style_prompt,
                    model_name="qwen-72b"
                )
                
                # Parse LLM response into style recommendations
                result = await self._parse_style_recommendations(response, project_inputs)
                logger.info(f"✅ Style analysis succeeded on attempt {attempt + 1}")
                return result
                
            except Exception as e:
                logger.warning(f"⚠️ Style analysis attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"❌ Style analysis FAILED after {max_retries} attempts")
                    raise ValueError(f"Station 5 style analysis failed after {max_retries} retries: {str(e)}")
    
    def _build_style_analysis_prompt(self, project_inputs: Dict[str, Any]) -> str:
        """Build prompt for LLM style analysis"""
        
        title = project_inputs.get('working_title', 'Untitled Audio Drama')
        genre = project_inputs.get('primary_genre', 'Drama')
        premise = project_inputs.get('core_premise', project_inputs.get('original_seed', ''))
        episodes = project_inputs.get('episode_count', '10')
        length = project_inputs.get('episode_length', '45 minutes')
        age_range = project_inputs.get('target_age_range', '25-45')
        narrator_strategy = project_inputs.get('narrator_strategy', 'Limited Omniscient')
        
        return f"""
        Analyze and recommend the TOP 3 screenplay styles for this audiobook project:

        PROJECT DETAILS:
        Title: {title}
        Genre: {genre}
        Premise: {premise}
        Episodes: {episodes} at {length} each
        Target Age: {age_range}
        Narrator: {narrator_strategy}

        From the 48 standard screenplay styles, recommend the 3 BEST options for this audio drama.

        For EACH of the 3 recommendations, provide:

        **STYLE 1: [Style Name]**
        - Fit Reasoning: Why this style suits this specific project
        - Audio Adaptation: How this works in pure audio format
        - Episode Implications: How this affects the {episodes}-episode structure
        - Confidence Score: 0.0-1.0 rating
        - Narrator Integration: How {narrator_strategy} works with this style

        **STYLE 2: [Style Name]**
        [Same format]

        **STYLE 3: [Style Name]**
        [Same format]

        Focus on styles that excel in audio format and suit the {genre} genre for {age_range} audiences.
        """
    
    async def _parse_style_recommendations(self, response: str, project_inputs: Dict[str, Any]) -> List[StyleRecommendation]:
        """Parse LLM response into style recommendations"""
        
        try:
            recommendations = []
            
            # Split response into style sections
            style_sections = re.split(r'\*\*STYLE \d+:', response)
            
            for i, section in enumerate(style_sections[1:], 1):  # Skip first empty section
                if i > 3:  # Only process first 3 styles
                    break
                
                # Extract style name
                name_match = re.search(r'^([^\*\n]+)', section.strip())
                style_name = name_match.group(1).strip() if name_match else f"Audio Drama Style {i}"
                
                # Extract sections
                fit_reasoning = self._extract_section_content(section, "Fit Reasoning")
                audio_adaptation = self._extract_section_content(section, "Audio Adaptation")
                episode_implications = self._extract_section_content(section, "Episode Implications")
                narrator_integration = self._extract_section_content(section, "Narrator Integration")
                
                # Extract confidence score
                confidence_match = re.search(r'Confidence Score[:\s]*([\d.]+)', section)
                confidence_score = float(confidence_match.group(1)) if confidence_match else 0.8
                
                recommendation = StyleRecommendation(
                    style_name=style_name,
                    fit_reasoning=fit_reasoning,
                    audio_adaptation=audio_adaptation,
                    episode_implications=episode_implications,
                    demo_script=self._generate_demo_script(style_name, project_inputs.get('working_title', 'Project'), 
                                                         project_inputs.get('core_premise', ''), 
                                                         project_inputs.get('primary_genre', 'Drama'),
                                                         project_inputs.get('narrator_strategy', 'Limited Omniscient'),
                                                         project_inputs),
                    confidence_score=confidence_score,
                    narrator_integration=narrator_integration
                )
                
                recommendations.append(recommendation)
            
            # Ensure we have at least 1 recommendation
            if not recommendations:
                raise ValueError("No style recommendations found in LLM response")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to parse style recommendations: {e}")
            raise ValueError(f"Could not parse style recommendations from LLM response: {str(e)}")
    
    def _extract_section_content(self, text: str, section_name: str) -> str:
        """Extract content from a named section"""
        pattern = rf'{section_name}[:\s]*([^\n]+(?:\n(?![\*\-])[^\n]*)*)'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
        return f"{section_name} details needed"

    def _create_fallback_style_recommendations(self, project_inputs: Dict[str, Any]) -> List[StyleRecommendation]:
        """Create style recommendations using actual project data"""
        
        # Extract real project data
        title = project_inputs.get('working_title', 'Untitled Audio Drama')
        genre = project_inputs.get('primary_genre', 'Drama')
        premise = project_inputs.get('core_premise', project_inputs.get('original_seed', ''))
        episodes = project_inputs.get('episode_count', '10')
        length = project_inputs.get('episode_length', '45 minutes')
        age_range = project_inputs.get('target_age_range', '25-45')
        narrator_strategy = project_inputs.get('narrator_strategy', 'Limited Omniscient')
        
        # Determine appropriate style based on actual genre and content
        if 'Contemporary Drama' in genre or 'Drama' in genre:
            style_name = "Character-Driven Drama"
            fit_reasoning = f"The Character-Driven Drama structure is perfect for '{title}' because it focuses on deep emotional relationships and personal growth, which aligns with the story's core themes. The {genre} genre emphasizes character development and intimate storytelling, making it ideal for the {age_range} target demographic who appreciates nuanced, relationship-focused narratives. The audio medium excels with this structure because it relies on compelling dialogue, internal monologues, and emotional voice acting to drive the story forward. With {episodes} episodes at {length} each, there's ample time to develop the character arcs and explore the emotional depth that this story demands."
        else:
            style_name = "Episodic Character Study"  
            fit_reasoning = f"The Episodic Character Study structure works well for '{title}' as a {genre} story, allowing each episode to explore different aspects of the characters while building toward the overall narrative resolution. This approach suits the {age_range} demographic and provides flexibility for the {episodes}-episode structure."

        return [
            StyleRecommendation(
                style_name=style_name,
                fit_reasoning=fit_reasoning,
                audio_adaptation=f"This structure excels in audio format because it emphasizes dialogue-driven scenes, character interactions, and emotional moments that translate beautifully to voice acting. The story '{title}' benefits from audio's ability to convey internal thoughts through narration and subtle emotional cues through vocal performance. Sound design can enhance the intimate, character-focused moments while supporting the {genre} atmosphere.",
                episode_implications=f"Each of the {episodes} episodes can focus on key character moments and relationship developments, building emotional investment while advancing the central storyline. The {length} episode length provides sufficient time for character exploration while maintaining narrative momentum throughout the series.",
                demo_script=self._generate_demo_script(style_name, title, premise, genre, narrator_strategy, project_inputs),
                confidence_score=0.85,
                narrator_integration=f"The {narrator_strategy} narrator strategy enhances this structure by providing character insights and emotional context, helping guide the audience through the character development journey that defines this story."
            ),
            # Add second and third style recommendations based on project data
            StyleRecommendation(
                style_name="Episodic Drama",
                fit_reasoning=f"Episodic Drama works well for '{title}' by allowing each episode to explore different emotional beats while building toward the overall resolution. This structure suits the {genre} genre and provides flexibility for character development across the {episodes}-episode arc.",
                audio_adaptation=f"This structure emphasizes character dialogue and emotional moments that work perfectly in audio format, allowing the voice acting to drive the narrative forward.",
                episode_implications=f"Each episode can focus on key relationship moments while advancing the central storyline over {episodes} episodes.",
                demo_script=self._generate_demo_script("Episodic Drama", title, premise, genre, narrator_strategy, project_inputs),
                confidence_score=0.78,
                narrator_integration=f"The {narrator_strategy} narrator provides emotional context and character insights throughout the episodic structure."
            ),
            StyleRecommendation(
                style_name="Contemporary Series",
                fit_reasoning=f"Contemporary Series structure suits '{title}' as a modern {genre} story, allowing for realistic character development and relationship exploration that resonates with the {age_range} demographic.",
                audio_adaptation="This structure relies on realistic dialogue and character interactions that translate excellently to audio format.",
                episode_implications=f"The {episodes}-episode structure provides ample time for character growth and story development.",
                demo_script=self._generate_demo_script("Contemporary Series", title, premise, genre, narrator_strategy, project_inputs),
                confidence_score=0.72,
                narrator_integration=f"The {narrator_strategy} narrator enhances the contemporary feel by providing modern, relatable commentary."
            )
        ]
    
    def _generate_demo_script(self, style_name: str, title: str, premise: str, genre: str, narrator_strategy: str, project_inputs: Dict[str, Any] = None) -> str:
        """Generate a 500-word demo script based on the actual story premise and style"""
        
        # Use actual project data if available, otherwise extract from premise
        if project_inputs:
            # Get real character names and setting from project data
            world_setting = project_inputs.get('world_setting', {})
            setting = world_setting.get('primary_location', 'the main location')
            
            # Use main characters extracted from Station 1
            main_characters = project_inputs.get('main_characters', [])
            if main_characters and len(main_characters) >= 2:
                char1_name = main_characters[0]
                char2_name = main_characters[1]
            elif main_characters and len(main_characters) == 1:
                char1_name = main_characters[0]
                char2_name = "Supporting Character"  # Fallback second character
            else:
                # Fallback to extraction from premise if no characters found
                char1_name, char2_name = self._extract_character_names_from_premise(premise, genre)
        else:
            # Fallback to premise analysis
            char1_name, char2_name = self._extract_character_names_from_premise(premise, genre)
            setting = self._extract_setting_from_premise(premise, genre)
        
        # Clean character names (remove descriptions if present)
        char1_name = self._clean_character_name(char1_name)
        char2_name = self._clean_character_name(char2_name)
        
        # Generate story-specific demo script based on actual premise
        return self._create_premise_specific_demo_script(style_name, title, premise, genre, narrator_strategy, char1_name, char2_name, setting)
    
    def _clean_character_name(self, char_name: str) -> str:
        """Clean character name by extracting just the name part"""
        if not char_name:
            return "Character"
        
        # Remove descriptions (everything after colon, dash, or parentheses)
        import re
        name = re.split(r'[:\-\(]', char_name)[0].strip()
        
        # Take first name only if it's a full name
        name_parts = name.split()
        return name_parts[0] if name_parts else "Character"
    
    def _create_premise_specific_demo_script(self, style_name: str, title: str, premise: str, genre: str, narrator_strategy: str, char1_name: str, char2_name: str, setting: str) -> str:
        """Create a demo script that reflects the actual story premise"""
        
        # Analyze the premise to create appropriate content
        premise_lower = premise.lower() if premise else ""
        
        # Detect story elements from premise
        if "text" in premise_lower and "message" in premise_lower:
            # Text message story
            return self._create_text_message_demo_script(style_name, title, premise, genre, narrator_strategy, char1_name, char2_name, setting)
        elif "hospital" in premise_lower or "doctor" in premise_lower or "medical" in premise_lower:
            # Medical setting story
            return self._create_medical_demo_script(style_name, title, premise, genre, narrator_strategy, char1_name, char2_name, setting)
        elif "coach" in premise_lower and "motivation" in premise_lower:
            # Coaching/motivation story
            return self._create_coaching_demo_script(style_name, title, premise, genre, narrator_strategy, char1_name, char2_name, setting)
        else:
            # Generic story-based script
            return self._create_generic_story_demo_script(style_name, title, premise, genre, narrator_strategy, char1_name, char2_name, setting)
    
    def _create_text_message_demo_script(self, style_name: str, title: str, premise: str, genre: str, narrator_strategy: str, char1_name: str, char2_name: str, setting: str) -> str:
        """Create demo script for text message based stories"""
        return f"""FADE IN:

INT. {setting.upper()} - DAY

NARRATOR ({narrator_strategy})
'{title}' begins with a simple mistake that will change two lives forever.

SFX: Phone notification sound

{char1_name.upper()}
(looking at phone)
Another message to send. Hope this helps someone today.

NARRATOR
{char1_name} types carefully, believing the message will reach its intended recipient.

{char1_name.upper()}
(typing, speaking aloud)
"Remember - every morning is a fresh start. You have the strength to face whatever comes today."

SFX: Message sent sound

NARRATOR
Miles away, a phone buzzes in {char2_name}'s pocket.

INT. {setting.upper()} - CONTINUOUS

{char2_name.upper()}
(exhausted, checking phone)
Wrong number again? Wait... this is different.

NARRATOR
{char2_name} reads the message, and for the first time in months, feels something shift.

{char2_name.upper()}
(quietly, to phone)
"You have the strength..." Maybe I do.

NARRATOR
Neither knows it yet, but this accidental connection will become the foundation for something extraordinary. In '{title}', the wrong number becomes exactly the right message.

SFX: Phone being put away gently

FADE OUT.

[This demo showcases how '{title}' uses the {style_name} approach to explore {genre.lower()} themes through the unique medium of text message communication.]"""
    
    def _create_medical_demo_script(self, style_name: str, title: str, premise: str, genre: str, narrator_strategy: str, char1_name: str, char2_name: str, setting: str) -> str:
        """Create demo script for medical setting stories"""
        return f"""FADE IN:

INT. {setting.upper()} - DAY

SFX: Hospital ambience, distant monitors

NARRATOR ({narrator_strategy})
In '{title}', healing comes in unexpected forms.

{char2_name.upper()}
(tired, checking phone during break)
Another twelve hour shift. How do I keep going?

SFX: Phone notification

{char2_name.upper()}
(reading message, surprised)
"You have the strength to face whatever comes today." Who is this?

NARRATOR
{char2_name} doesn't know that these messages come from {char1_name}, sent to the wrong number for months.

INT. {char1_name.upper()}'S OFFICE - SAME TIME

{char1_name.upper()}
(to computer, typing)
Day 247. Sending today's motivation to my client. Hope it helps.

NARRATOR
What {char1_name} doesn't know is that these messages have been saving a life - just not the life intended.

BACK TO HOSPITAL

{char2_name.upper()}
(to colleague)
These messages... they come every morning. Right when I need them most.

NARRATOR
The {genre.lower()} of '{title}' lies in these unintended connections - how strangers can heal each other without ever knowing it.

FADE OUT.

[This demo demonstrates how '{title}' explores {genre.lower()} themes through the {style_name} structure.]"""
    
    def _create_coaching_demo_script(self, style_name: str, title: str, premise: str, genre: str, narrator_strategy: str, char1_name: str, char2_name: str, setting: str) -> str:
        """Create demo script for coaching/motivation stories"""
        return f"""FADE IN:

INT. {setting.upper()} - MORNING

NARRATOR ({narrator_strategy})
Every morning, {char1_name} begins the same routine that will unknowingly change someone's life.

{char1_name.upper()}
(reviewing notes, speaking to phone)
"Good morning! Today is full of possibilities. Remember, you're stronger than you think."

SFX: Message sent

NARRATOR
For a year, these messages have been going to the wrong number. But to {char2_name}, they've become a lifeline.

INT. DIFFERENT LOCATION - SAME TIME

{char2_name.upper()}
(reading message, smiling slightly)
There it is. My daily reminder that someone believes in me.

NARRATOR
What started as a simple mistake has become something profound. In '{title}', the wrong number becomes the right message at exactly the right time.

{char2_name.upper()}
(to phone)
Whoever you are, thank you. You'll never know what these mean to me.

NARRATOR
But one day, {char1_name} will find out. And when that happens, both their worlds will change forever.

FADE OUT.

[This demo script showcases the {style_name} approach to '{title}', highlighting the {genre.lower()} elements that drive this unique story forward.]"""
    
    def _create_generic_story_demo_script(self, style_name: str, title: str, premise: str, genre: str, narrator_strategy: str, char1_name: str, char2_name: str, setting: str) -> str:
        """Create a generic demo script based on the premise"""
        return f"""FADE IN:

INT. {setting.upper()} - DAY

NARRATOR ({narrator_strategy})
In '{title}', two lives are about to intersect in ways neither could imagine.

{char1_name.upper()}
(focused on their task)
Every action has consequences. I just hope this one leads somewhere good.

NARRATOR
{char1_name} doesn't know that their simple action will ripple outward, touching {char2_name}'s life in profound ways.

{char2_name.upper()}
(dealing with their situation)
I've been waiting for something to change. Some sign that things can get better.

NARRATOR
The {genre.lower()} of '{title}' unfolds in these moments of possibility - when ordinary actions create extraordinary connections.

{char1_name.upper()}
If I can help even one person today, it will all be worth it.

{char2_name.upper()}
(experiencing the effect)
Something's different. Something's changing.

NARRATOR
And in that moment of recognition, '{title}' begins its exploration of how we find each other in an interconnected world.

FADE OUT.

[This demo script demonstrates the {style_name} structure for '{title}', emphasizing the {genre.lower()} themes that will drive the narrative forward.]"""
    
    def _extract_character_names_from_premise(self, premise: str, genre: str) -> tuple:
        """Extract character names from premise or generate appropriate ones based on genre"""
        premise_lower = premise.lower() if premise else ""
        
        # Try to extract names from premise
        import re
        name_patterns = [
            r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b',  # First Last names
            r'\b([A-Z][a-z]+)\b',  # Single names
        ]
        
        names = []
        for pattern in name_patterns:
            matches = re.findall(pattern, premise)
            if matches:
                if isinstance(matches[0], tuple):
                    names.extend(matches[0])
                else:
                    names.extend(matches)
                break
        
        # Generate appropriate names based on genre if none found
        if len(names) < 2:
            # Generate appropriate generic names based on genre
            if 'romance' in genre.lower() or 'contemporary' in genre.lower():
                char1_name = names[0] if names else "the protagonist"
                char2_name = names[1] if len(names) > 1 else "the love interest"
            elif 'mystery' in genre.lower() or 'thriller' in genre.lower():
                char1_name = names[0] if names else "the detective"
                char2_name = names[1] if len(names) > 1 else "the investigator"
            elif 'drama' in genre.lower():
                char1_name = names[0] if names else "the main character"
                char2_name = names[1] if len(names) > 1 else "the supporting character"
            else:
                char1_name = names[0] if names else "Main Character"
                char2_name = names[1] if len(names) > 1 else "Supporting Character"
        else:
            char1_name = names[0]
            char2_name = names[1]
            
        return char1_name, char2_name
    
    def _extract_setting_from_premise(self, premise: str, genre: str) -> str:
        """Extract setting from premise or generate appropriate one based on genre"""
        premise_lower = premise.lower() if premise else ""
        
        # Common setting keywords
        setting_keywords = {
            'hospital': 'the healthcare setting',
            'medical': 'the professional facility',
            'coffee': 'a busy coffee shop',
            'office': 'the corporate office',
            'school': 'the school campus',
            'university': 'the university campus',
            'restaurant': 'the local restaurant',
            'park': 'the city park',
            'home': 'the family home',
            'apartment': 'the apartment building',
            'street': 'the city street',
            'beach': 'the beachfront',
            'mountain': 'the mountain trail',
            'forest': 'the forest path',
            'library': 'the public library',
            'museum': 'the art museum',
            'theater': 'the theater district',
            'airport': 'the airport terminal',
            'train': 'the train station',
            'hotel': 'the hotel lobby'
        }
        
        # Check for setting keywords in premise
        for keyword, setting in setting_keywords.items():
            if keyword in premise_lower:
                return setting
        
        # Generate setting based on genre
        if 'romance' in genre.lower():
            return 'a cozy café'
        elif 'mystery' in genre.lower():
            return 'the investigation room'
        elif 'drama' in genre.lower():
            return 'the main location'
        elif 'contemporary' in genre.lower():
            return 'the modern city center'
        else:
            return 'the main location'
    
    async def _create_season_skeleton(self, project_inputs: Dict[str, Any], style_recommendations: List[StyleRecommendation]) -> Dict[str, Any]:
        """
        TASK 2: SEASON SKELETON
        Create complete season architecture with macro and micro structure
        """
        logger.info("Creating complete season skeleton with 4-act mapping")
        
        # Generate season skeleton using LLM with retry logic
        max_retries = 5
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    logger.info(f"🔄 Season skeleton retry attempt {attempt + 1}/{max_retries}")
                    await asyncio.sleep(retry_delay * attempt)
                
                skeleton_prompt = self._build_season_skeleton_prompt(project_inputs, style_recommendations)
                response = await self.openrouter.process_message(
                    skeleton_prompt,
                    model_name="qwen-72b"
                )
                
                result = await self._parse_season_skeleton(response, project_inputs, style_recommendations)
                logger.info(f"✅ Season skeleton succeeded on attempt {attempt + 1}")
                return result
                
            except Exception as e:
                logger.warning(f"⚠️ Season skeleton attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"❌ Season skeleton FAILED after {max_retries} attempts")
                    raise ValueError(f"Station 5 season skeleton generation failed after {max_retries} retries: {str(e)}")
    
    def _build_season_skeleton_prompt(self, project_inputs: Dict[str, Any], style_recommendations: List[StyleRecommendation]) -> str:
        """Build prompt for LLM season skeleton generation"""
        
        title = project_inputs.get('working_title', 'Untitled Audio Drama')
        genre = project_inputs.get('primary_genre', 'Drama')
        premise = project_inputs.get('core_premise', project_inputs.get('original_seed', ''))
        episodes = project_inputs.get('episode_count', '10')
        length = project_inputs.get('episode_length', '45 minutes')
        chosen_style = style_recommendations[0] if style_recommendations else None
        style_name = chosen_style.style_name if chosen_style else "Character-Driven Drama"
        
        return f"""
        Create a complete season skeleton for this audiobook project using the {style_name} structure:

        PROJECT DETAILS:
        Title: {title}
        Genre: {genre}
        Premise: {premise}
        Episodes: {episodes} at {length} each
        Chosen Style: {style_name}

        Create a complete season architecture with:

        **MACRO STRUCTURE:**
        - Act 1 (Setup): Episodes 1-2
        - Act 2A (Rising Action): Episodes 3-4
        - Act 2B (Midpoint): Episodes 5-6
        - Act 3 (Resolution): Episodes 7+

        **EPISODE BREAKDOWN:**
        For each episode, provide:
        - Episode Number: [1-{episodes}]
        - Episode Title: [Descriptive title]
        - Act Position: [Which act this belongs to]
        - Story Function: [What this episode accomplishes]
        - Key Beats: [3-4 major story moments]
        - Character Focus: [Which characters are featured]
        - Emotional Arc: [The emotional journey]
        - Cliffhanger: [How it ends to hook the next episode]

        Focus on the {genre} genre and ensure each episode builds toward the overall story resolution.
        Use the {style_name} structure to guide pacing and character development.
        """
    
    async def _parse_season_skeleton(self, response: str, project_inputs: Dict[str, Any], style_recommendations: List[StyleRecommendation]) -> Dict[str, Any]:
        """Parse LLM response into season skeleton structure"""
        
        try:
            # Extract macro structure
            macro_structure = self._extract_macro_structure(response)
            
            # Extract episode breakdown
            episodes = self._extract_episode_breakdown(response, project_inputs)
            
            # Create comprehensive skeleton
            skeleton = {
                "macro_structure": macro_structure,
                "episodes": episodes,
                "total_episodes": len(episodes),
                "chosen_style": style_recommendations[0].style_name if style_recommendations else "Character-Driven Drama",
                "genre_integration": self._extract_genre_integration(response),
                "audio_considerations": self._extract_audio_considerations(response)
            }
            
            return skeleton
            
        except Exception as e:
            logger.error(f"Failed to parse season skeleton: {e}")
            raise ValueError(f"Could not parse season skeleton from LLM response: {str(e)}")
    
    def _extract_macro_structure(self, response: str) -> Dict[str, Any]:
        """Extract macro structure from LLM response"""
        try:
            # Look for act structure
            acts = {}
            act_pattern = r'Act (\d+[AB]?)[:\s]*([^\n]+(?:\n(?![A-Z\*])[^\n]*)*)'
            act_matches = re.findall(act_pattern, response, re.MULTILINE)
            
            for act_num, act_desc in act_matches:
                acts[f"act_{act_num.lower()}"] = act_desc.strip()
            
            return {
                "four_act_structure": acts,
                "pacing_notes": "Character-driven pacing with emotional beats",
                "narrative_arc": "Setup → Development → Crisis → Resolution"
            }
        except:
            return {
                "four_act_structure": {
                    "act_1": "Setup and character introduction",
                    "act_2a": "Rising action and development", 
                    "act_2b": "Midpoint and complications",
                    "act_3": "Climax and resolution"
                },
                "pacing_notes": "Character-driven pacing with emotional beats",
                "narrative_arc": "Setup → Development → Crisis → Resolution"
            }
    
    def _extract_episode_breakdown(self, response: str, project_inputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract episode breakdown from LLM response"""
        try:
            episodes = []
            episode_sections = re.split(r'Episode (\d+)', response)[1:]  # Skip first empty section
            
            for i in range(0, len(episode_sections), 2):
                if i + 1 < len(episode_sections):
                    episode_num = episode_sections[i]
                    episode_content = episode_sections[i + 1]
                    
                    episode = {
                        "episode_number": int(episode_num),
                        "episode_title": self._extract_episode_field(episode_content, "Title", f"Episode {episode_num}"),
                        "act_position": self._extract_episode_field(episode_content, "Act Position", "Act 1"),
                        "story_function": self._extract_episode_field(episode_content, "Story Function", "Story development"),
                        "key_beats": self._extract_episode_list(episode_content, "Key Beats"),
                        "character_focus": self._extract_episode_field(episode_content, "Character Focus", "Main characters"),
                        "emotional_arc": self._extract_episode_field(episode_content, "Emotional Arc", "Character growth"),
                        "cliffhanger": self._extract_episode_field(episode_content, "Cliffhanger", "Story continuation")
                    }
                    
                    episodes.append(episode)
            
            # Ensure we have the right number of episodes
            target_count = int(str(project_inputs.get('episode_count', '6')).split('-')[0])
            while len(episodes) < target_count:
                episodes.append({
                    "episode_number": len(episodes) + 1,
                    "episode_title": f"Episode {len(episodes) + 1}",
                    "act_position": "Act 1" if len(episodes) < 2 else "Act 2A",
                    "story_function": "Story development",
                    "key_beats": ["Character development", "Plot advancement", "Emotional beats"],
                    "character_focus": "Main characters",
                    "emotional_arc": "Character growth",
                    "cliffhanger": "Story continuation"
                })
            
            return episodes[:target_count]
            
        except Exception as e:
            logger.warning(f"Failed to parse episodes from LLM response: {e}")
            # Return basic episode structure
            target_count = int(str(project_inputs.get('episode_count', '6')).split('-')[0])
            return [
                {
                    "episode_number": i + 1,
                    "episode_title": f"Episode {i + 1}",
                    "act_position": "Act 1" if i < 2 else "Act 2A" if i < 4 else "Act 3",
                    "story_function": "Story development",
                    "key_beats": ["Character development", "Plot advancement", "Emotional beats"],
                    "character_focus": "Main characters", 
                    "emotional_arc": "Character growth",
                    "cliffhanger": "Story continuation"
                }
                for i in range(target_count)
            ]
    
    def _extract_episode_field(self, text: str, field_name: str, default: str) -> str:
        """Extract a specific field from episode text"""
        pattern = rf'{field_name}[:\s]*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else default
    
    def _extract_episode_list(self, text: str, field_name: str) -> List[str]:
        """Extract a list field from episode text"""
        pattern = rf'{field_name}[:\s]*([^\n]+(?:\n\s*[-•][^\n]*)*)'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            content = match.group(1)
            items = re.findall(r'[-•]\s*([^\n]+)', content)
            if items:
                return [item.strip() for item in items]
            return [content.strip()]
        return ["Character development", "Plot advancement", "Emotional beats"]
    
    def _extract_genre_integration(self, response: str) -> str:
        """Extract genre integration notes"""
        pattern = r'genre integration[:\s]*([^\n]+(?:\n(?![A-Z\*])[^\n]*)*)'
        match = re.search(pattern, response, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else "Genre elements integrated throughout"
    
    def _extract_audio_considerations(self, response: str) -> str:
        """Extract audio considerations"""
        pattern = r'audio[:\s]*([^\n]+(?:\n(?![A-Z\*])[^\n]*)*)'
        match = re.search(pattern, response, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else "Optimized for audio presentation"

    def _create_comprehensive_season_skeleton(self, project_inputs: Dict[str, Any], chosen_style) -> Dict[str, Any]:
        """Create comprehensive season skeleton with all episodes detailed"""

        # Determine total episodes from project inputs, default to 10
        episode_count_str = str(project_inputs.get('episode_count', '10'))
        if '-' in episode_count_str:
            # For ranges like "3-6", use the maximum value
            parts = episode_count_str.split('-')
            total_episodes = int(''.join(filter(str.isdigit, parts[1]))) if len(parts) > 1 else 10
        else:
            digits = ''.join(filter(str.isdigit, episode_count_str))
            total_episodes = int(digits) if digits else 10

        # Create macro structure based on total episodes
        if total_episodes <= 4:
            # Simple 2-act structure for very short series
            act_1 = list(range(1, (total_episodes // 2) + 1))
            act_2 = list(range(len(act_1) + 1, total_episodes + 1))
            macro = {
                "act_1_episodes": act_1,
                "act_2_episodes": act_2,
            }
        elif total_episodes <= 6:
            # 3-act structure for short series
            act_size = total_episodes // 3
            macro = {
                "act_1_episodes": list(range(1, act_size + 1)),
                "act_2_episodes": list(range(act_size + 1, act_size * 2 + 1)),
                "act_3_episodes": list(range(act_size * 2 + 1, total_episodes + 1)),
            }
        else:
            # 4-act structure for standard/long series (8+ episodes)
            # Act 1: ~20%, Act 2A: ~30%, Act 2B: ~20%, Act 3: ~30%
            act1_end = max(2, int(total_episodes * 0.2))
            act2a_end = act1_end + int(total_episodes * 0.3)
            act2b_end = act2a_end + int(total_episodes * 0.2)

            macro = {
                "act_1_episodes": list(range(1, act1_end + 1)),
                "act_2a_episodes": list(range(act1_end + 1, act2a_end + 1)),
                "act_2b_episodes": list(range(act2a_end + 1, act2b_end + 1)),
                "act_3_episodes": list(range(act2b_end + 1, total_episodes + 1)),
            }

        macro["structure_explanation"] = f"The {chosen_style.style_name if chosen_style else 'Character-Driven Drama'} structure maps perfectly to this season flow for '{project_inputs.get('working_title', 'this story')}' with {total_episodes} episodes, allowing for natural character development and emotional progression."

        return {
            "macro_structure": macro,
            "episode_grid": self._generate_generic_episode_grid(project_inputs, chosen_style, total_episodes)
        }
    
    def _generate_generic_episode_grid(self, project_inputs: Dict[str, Any], chosen_style, total_episodes: int = None) -> List[Dict[str, Any]]:
        """Generate generic episode grid based on project inputs"""
        title = project_inputs.get('working_title', 'this story')
        genre = project_inputs.get('primary_genre', 'Drama')

        # Use provided total_episodes or parse from project inputs
        if total_episodes is None:
            episode_count_str = str(project_inputs.get('episode_count', '10'))
            if '-' in episode_count_str:
                parts = episode_count_str.split('-')
                total_episodes = int(''.join(filter(str.isdigit, parts[1]))) if len(parts) > 1 else 10
            else:
                digits = ''.join(filter(str.isdigit, episode_count_str))
                total_episodes = int(digits) if digits else 10

        episodes = []
        for i in range(1, total_episodes + 1):
            # Determine act and function based on episode number
            if i <= 2:
                act = "Act 1"
                function = "Setup" if i == 1 else "Development"
                energy = 7 if i == 1 else 8
            elif i <= 6:
                act = "Act 2A"
                function = "Complication" if i % 2 == 1 else "Development"
                energy = 6 + (i % 3)
            elif i <= 8:
                act = "Act 2B"
                function = "Climax" if i == 7 else "Revelation" 
                energy = 9 if i == 7 else 8
            else:
                act = "Act 3"
                function = "Climax" if i == 9 else "Resolution"
                energy = 10 if i == 9 else 6
            
            episodes.append({
                "episode_number": i,
                "primary_function": function,
                "energy_level": energy,
                "subplot_focus": f"Episode {i} develops the {genre.lower()} elements of '{title}', focusing on character relationships and story progression appropriate for this part of the narrative arc.",
                "cliffhanger_type": "Character Development" if i == total_episodes else "Story Progression",
                "act_equivalent": act,
                "special_notes": f"Episode {i} serves the {function.lower()} function in the {act} structure, maintaining audience engagement through character development and narrative progression suitable for the {genre} genre."
            })
        
        return episodes
    
    async def _design_rhythm_mapping(self, project_inputs: Dict[str, Any], season_structure: Dict[str, Any]) -> RhythmMapping:
        """
        TASK 3: RHYTHM MAPPING
        Design sophisticated pacing across the complete season
        """
        logger.info("Designing sophisticated rhythm and pacing mapping")

        # Get total episodes from macro structure
        macro_data = season_structure.get("macro_structure", {})
        all_episodes = []
        for key in macro_data:
            if key.endswith('_episodes') and isinstance(macro_data[key], list):
                all_episodes.extend(macro_data[key])
        total_eps = max(all_episodes) if all_episodes else 10

        # Calculate dynamic tension peaks and breathing room based on total episodes
        # Tension peaks at: ~20%, ~50%, ~70%, ~90% of series
        tension_peaks = [
            max(1, int(total_eps * 0.2)),
            max(2, int(total_eps * 0.5)),
            max(3, int(total_eps * 0.7)),
            max(total_eps - 1, int(total_eps * 0.9))
        ]

        # Breathing room at: start, ~30%, ~60%, end
        breathing_room = [
            1,
            max(2, int(total_eps * 0.3)),
            max(3, int(total_eps * 0.6)),
            total_eps
        ]

        # Format breaks at: ~40% and ~80% of series
        format_breaks = [
            [max(2, int(total_eps * 0.4)), f"Character development special - focused episode exploring key relationships in '{project_inputs.get('working_title', 'the story')}'"],
            [max(3, int(total_eps * 0.8)), f"Revelation special - major story developments and character revelations for the {project_inputs.get('primary_genre', 'drama')} storyline"]
        ]

        # Revelation cascade points at key story moments
        revelation_points = [
            [tension_peaks[0], f"Major character or plot development that advances '{project_inputs.get('working_title', 'the story')}' narrative"],
            [tension_peaks[1], f"Significant relationship or conflict development appropriate for the {project_inputs.get('primary_genre', 'drama')} genre"],
            [tension_peaks[2], f"Escalating stakes and character development as the story reaches its turning point"],
            [max(total_eps - 2, int(total_eps * 0.8)), f"Major revelations and plot developments that set up the final act"],
            [tension_peaks[3], f"Climactic revelations and character resolutions for '{project_inputs.get('working_title', 'the story')}'"]
        ]

        # Generate dynamic energy curve based on total episodes
        energy_curve = []
        for i in range(1, total_eps + 1):
            # Start moderate, peak in middle and near end, end calm
            if i == 1:
                energy_curve.append(7)
            elif i in tension_peaks:
                energy_curve.append(9 if i < total_eps - 1 else 10)
            elif i in breathing_room:
                energy_curve.append(6)
            else:
                energy_curve.append(7 + (i % 3))

        # Create comprehensive rhythm mapping
        return RhythmMapping(
            tension_peaks=tension_peaks,
            breathing_room=breathing_room,
            format_breaks=format_breaks,
            revelation_cascade_points=revelation_points,
            energy_curve=energy_curve,
            pacing_strategy={
                "overall_approach": f"The pacing strategy for '{project_inputs.get('working_title', 'this story')}' builds through character development and emotional progression appropriate for the {project_inputs.get('primary_genre', 'drama')} genre. The rhythm balances character moments with story progression, maintaining audience engagement through the {total_eps}-episode structure.",
                "climax_episodes": f"Episodes {', '.join(map(str, tension_peaks))} serve as major tension peaks with character development, relationship progression, emotional escalation, and final resolution respectively",
                "recovery_episodes": f"Episodes {', '.join(map(str, breathing_room))} provide breathing room through character exploration, relationship building, and emotional processing while maintaining story momentum",
                "momentum_maintenance": "Episodes maintain engagement through character development, relationship dynamics, and steady story progression without overwhelming the audience"
            },
            narrator_rhythm_integration=f"The {project_inputs.get('narrator_strategy', 'Limited Omniscient')} narrator enhances pacing by providing smooth transitions between story beats, offering character insights during development moments, and building emotional connection during key scenes throughout the series"
        )
    
    def _create_complete_document(self, project_inputs: Dict[str, Any], style_recommendations: List[StyleRecommendation], 
                                 season_structure: Dict[str, Any], rhythm_mapping: RhythmMapping, session_id: str) -> SeasonStructureDocument:
        """Package complete Season Structure Document"""
        
        # Create macro structure
        macro_data = season_structure.get("macro_structure", {})

        # Calculate total_episodes from episode_grid (source of truth)
        episode_grid_data = season_structure.get("episode_grid", [])
        total_eps = len(episode_grid_data) if episode_grid_data else 10

        # Use macro_data acts if they exist and are valid, otherwise empty lists
        # The acts should have been created correctly in _create_comprehensive_season_skeleton
        macro_structure = MacroStructure(
            act_1_episodes=macro_data.get("act_1_episodes", []),
            act_2a_episodes=macro_data.get("act_2a_episodes", []),
            act_2b_episodes=macro_data.get("act_2b_episodes", []),
            act_3_episodes=macro_data.get("act_3_episodes", []),
            act_2_episodes=macro_data.get("act_2_episodes", []),  # For 3-act structure
            structure_explanation=macro_data.get("structure_explanation", ""),
            total_episodes=total_eps
        )
        
        # Create episode grid
        episode_grid = []
        for ep_data in season_structure.get("episode_grid", []):
            episode_slot = EpisodeSlot(
                episode_number=ep_data.get("episode_number", 1),
                primary_function=ep_data.get("primary_function", "Setup"),
                energy_level=ep_data.get("energy_level", 5),
                subplot_focus=ep_data.get("subplot_focus", ""),
                cliffhanger_type=ep_data.get("cliffhanger_type", "None"),
                act_equivalent=ep_data.get("act_equivalent", "Act 1"),
                special_notes=ep_data.get("special_notes", "")
            )
            episode_grid.append(episode_slot)
        
        return SeasonStructureDocument(
            working_title=project_inputs.get("working_title", "Untitled Audio Drama"),
            session_id=session_id,
            created_timestamp=datetime.now(),
            style_recommendations=style_recommendations,
            chosen_style=style_recommendations[0].style_name if style_recommendations else "Character-Driven Drama",
            recommended_choice=f"{style_recommendations[0].style_name if style_recommendations else 'Character-Driven Drama'} is the optimal choice for '{project_inputs.get('working_title', 'this story')}' because it aligns with the {project_inputs.get('primary_genre', 'Drama')} genre and provides the right structure for character development and emotional storytelling. This approach suits the {project_inputs.get('target_age_range', '25-45')} target audience and works well with the {project_inputs.get('narrator_strategy', 'Limited Omniscient')} narrator strategy to create engaging audio drama content over {project_inputs.get('episode_count', '10')} episodes.",
            macro_structure=macro_structure,
            episode_grid=episode_grid,
            rhythm_mapping=rhythm_mapping,
            narrator_integration=f"{project_inputs.get('narrator_strategy', 'Limited Omniscient')} narrator strategy perfectly complements the {style_recommendations[0].style_name if style_recommendations else 'Character-Driven Drama'} structure by providing character insights and emotional context. The narrator enhances character development, guides listeners through important story moments, and helps build emotional connection with the characters throughout the series.",
            production_considerations=[
                f"Audio production should focus on character voice differentiation for the {project_inputs.get('primary_genre', 'drama')} genre",
                f"Sound design should support the emotional tone appropriate for '{project_inputs.get('working_title', 'this story')}'",
                f"Narrator integration requires careful balance with dialogue for the {project_inputs.get('narrator_strategy', 'Limited Omniscient')} approach",
                f"Episode pacing should maintain audience engagement across the {project_inputs.get('episode_count', '10')}-episode structure",
                f"Audio atmosphere should complement the {project_inputs.get('target_age_range', '25-45')} target demographic preferences"
            ],
            project_context=project_inputs,
            comprehensive_profile=project_inputs.get("comprehensive_profile", {})
        )
    
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
