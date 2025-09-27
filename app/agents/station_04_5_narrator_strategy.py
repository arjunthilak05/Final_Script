"""
Station 4.5: Narrator Strategy Designer Agent

This agent analyzes story complexity and determines whether the audio series needs
a narrator, and if so, what type. Creates sample scenes demonstrating both approaches.

Dependencies: Stations 1-4 outputs
Outputs: Narrator Strategy Recommendation Document
Human Gate: CRITICAL - Affects all subsequent script development
"""

import json
import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.config import Settings

logger = logging.getLogger(__name__)

class NarratorIdentityType(Enum):
    OMNISCIENT_THIRD_PERSON = "Omniscient third-person"
    CHARACTER_RETROSPECTIVE = "Character narrator (retrospective)"
    CHARACTER_REAL_TIME = "Character narrator (real-time)"
    WITNESS_NARRATOR = "Witness narrator"
    THEMED_NARRATOR = "Themed narrator (conceptual entity)"

class NarratorPresenceLevel(Enum):
    HEAVY = "Heavy (40-50% of runtime)"
    MODERATE = "Moderate (20-30% of runtime)"
    LIGHT = "Light (10-15% of runtime)"
    MINIMAL = "Minimal (5% - transitions only)"

class NarratorRecommendation(Enum):
    WITH_NARRATOR = "WITH_NARRATOR"
    WITHOUT_NARRATOR = "WITHOUT_NARRATOR"
    HYBRID_APPROACH = "HYBRID_APPROACH"

@dataclass
class ComplexityScore:
    """Complexity analysis scoring"""
    complexity_factors: Dict[str, int]
    audio_clarity_factors: Dict[str, int]
    stylistic_factors: Dict[str, int]
    total_score: int
    recommendation_tier: str

@dataclass
class SampleScene:
    """Sample scene demonstration"""
    scene_title: str
    with_narrator: str
    without_narrator: str
    scene_notes: str

@dataclass
class NarratorStrategy:
    """Narrator strategy configuration"""
    identity_type: Optional[NarratorIdentityType]
    presence_level: Optional[NarratorPresenceLevel]
    key_functions: List[str]
    voice_casting_notes: str
    sample_narrator_lines: List[str]

@dataclass
class AlternativeStrategy:
    """No-narrator alternative strategy"""
    character_id_strategy: str
    scene_transition_methods: str
    exposition_tactics: str
    internal_thought_alternatives: str
    timeline_clarification: str

@dataclass
class ProductionImpact:
    """Production impact assessment"""
    budget_implications: str
    schedule_changes: str
    technical_requirements: str
    casting_needs: str

@dataclass
class NarratorRecommendationDocument:
    """Complete Station 4.5 output"""
    working_title: str
    executive_summary: str
    complexity_analysis: ComplexityScore
    sample_scenes: List[SampleScene]
    recommendation: NarratorRecommendation
    narrator_strategy: Optional[NarratorStrategy]
    alternative_strategy: Optional[AlternativeStrategy]
    production_impact: ProductionImpact
    implementation_guidelines: Dict[str, str]
    session_id: str
    created_timestamp: datetime

class Station045NarratorStrategy:
    """
    Station 4.5: Narrator Strategy Designer
    
    Responsibilities:
    1. Analyze story complexity across multiple dimensions
    2. Create demonstration scenes with and without narrator
    3. Recommend narrator strategy or alternative approach
    4. Provide implementation guidelines for subsequent stations
    5. Assess production impact of narrator decision
    """
    
    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.station_id = "station_04_5"
        self.debug_mode = False
        
        # Station-specific prompt templates
        self.complexity_analysis_prompt = self._load_complexity_analysis_prompt()
        self.scene_generation_prompt = self._load_scene_generation_prompt()
        self.recommendation_prompt = self._load_recommendation_prompt()
        
    async def initialize(self):
        """Initialize the Station 4.5 processor"""
        await self.redis.initialize()
        
    def enable_debug_mode(self):
        """Enable detailed logging for debugging"""
        logger.setLevel(logging.DEBUG)
        self.debug_mode = True
        
    def _load_complexity_analysis_prompt(self) -> str:
        """Load complexity analysis prompt template"""
        return """
You are analyzing story complexity for narrator necessity in an audio series.

PROJECT CONTEXT:
{project_context}

STORY ELEMENTS:
{story_elements}

TASK: Score each factor from 0-5 based on the story elements provided.

COMPLEXITY FACTORS (0-35 total):
1. Multiple timelines or locations (0-5)
2. Large cast requiring identification (0-5)  
3. Internal character thoughts crucial (0-5)
4. Exposition that can't be shown (0-5)
5. World-building requirements (0-5)
6. Historical/technical context needed (0-5)
7. Time jumps between scenes (0-5)

AUDIO CLARITY FACTORS (0-25 total):
1. Scene transitions clarity (0-5)
2. Character identification challenges (0-5)
3. Action sequence comprehension (0-5)
4. Emotional subtext needing voice (0-5)
5. Pacing control requirements (0-5)

STYLISTIC FACTORS (0-25 total):
1. Genre conventions expectation (0-5)
2. Intimate vs distant tone desired (0-5)
3. Literary vs cinematic approach (0-5)
4. Poetic/thematic commentary value (0-5)
5. Humor delivery opportunities (0-5)

For each factor, provide:
- SCORE: [0-5]
- REASONING: [2-3 sentences explaining the score]

Format your response as:

COMPLEXITY_FACTORS:
Multiple_timelines_locations: 4 - This story involves time travel and multiple historical periods
Large_cast_identification: 3 - Medium-sized cast with distinct character voices needed
[Continue for all factors...]

AUDIO_CLARITY_FACTORS:
Scene_transitions_clarity: 5 - Complex transitions between time periods require clear guidance
[Continue for all factors...]

STYLISTIC_FACTORS:
Genre_conventions_expectation: 4 - Historical fiction typically uses narrator for context
[Continue for all factors...]

TOTAL_SCORE: [Sum]/75
RECOMMENDATION_TIER: [0-30: No narrator | 31-50: Either way | 51-75: Narrator recommended]
"""

    def _load_scene_generation_prompt(self) -> str:
        """Load scene generation prompt template"""
        return """
You are creating demonstration scenes for narrator strategy analysis.

PROJECT CONTEXT:
{project_context}

STORY ELEMENTS:
{story_elements}

TASK: Create the SAME pivotal scene twice - once with narrator, once without.

Choose a crucial story moment that demonstrates:
- Character emotion/conflict
- Plot advancement
- Setting/atmosphere
- Tension/stakes

Create exactly 500 words for each version.

VERSION A: WITH NARRATOR
Use this structure:
[Scene Setup]
NARRATOR: [Sets scene, provides context, character thoughts]
CHARACTER: [Natural dialogue, can be more subtle]
[SFX: Sound effects]
NARRATOR: [Transitions, internal reactions, time passages]
[Continue showing narrator advantages]

VERSION B: WITHOUT NARRATOR  
Use this structure:
[SFX: Environmental sounds]
CHARACTER: [Natural exposition through dialogue]
[SFX: Story-telling sound effects]
CHARACTER: [Character vocal reactions revealing thoughts]
[All information through dialogue and audio cues only]

Both scenes must:
- Be exactly 500 words each
- Show the same story moment
- Demonstrate the pros/cons of each approach
- Be formatted for audio production
- Include specific SFX cues
- Maintain story authenticity

Format response as:

SCENE_TITLE: [Compelling scene title]

VERSION_A_WITH_NARRATOR:
[500-word scene with narrator]

VERSION_B_WITHOUT_NARRATOR:
[500-word scene without narrator]

SCENE_NOTES:
[Analysis of which version works better and why]
"""

    def _load_recommendation_prompt(self) -> str:
        """Load recommendation generation prompt"""
        return """
You are making the final narrator strategy recommendation.

PROJECT CONTEXT:
{project_context}

COMPLEXITY ANALYSIS:
{complexity_analysis}

SAMPLE SCENES:
{sample_scenes}

TASK: Based on the complexity score and scene demonstrations, make your recommendation.

SCORING GUIDE:
- 0-30: Strong candidate for no narrator
- 31-50: Could work either way (consider production budget/complexity)
- 51-75: Narrator recommended

Consider these factors for your decision:
1. Story complexity requirements
2. Audio clarity needs
3. Production budget constraints
4. Genre expectations
5. Target audience preferences
6. Creative vision alignment

If recommending WITH NARRATOR, specify:
- Identity type (Omniscient third-person, Character retrospective, etc.)
- Presence level (Heavy/Moderate/Light/Minimal)
- Key functions (top 3-5 uses)
- Voice casting requirements
- 5 sample narrator lines

If recommending WITHOUT NARRATOR, specify:
- Character identification strategy
- Scene transition methods
- Exposition delivery tactics
- Internal thought alternatives
- Timeline clarification methods

If recommending HYBRID APPROACH, specify:
- When narrator appears
- Trigger conditions
- How presence/absence is justified

Format response as:

RECOMMENDATION: [WITH_NARRATOR / WITHOUT_NARRATOR / HYBRID_APPROACH]

EXECUTIVE_SUMMARY:
[1 paragraph explaining your recommendation and key reasoning]

[If WITH_NARRATOR:]
NARRATOR_IDENTITY: [Selected type]
PRESENCE_LEVEL: [Heavy/Moderate/Light/Minimal]
KEY_FUNCTIONS: [Function 1, Function 2, Function 3, Function 4, Function 5]
VOICE_CASTING: [Gender, age range, vocal qualities, experience level]
SAMPLE_LINES:
1. [Example narrator line]
2. [Example narrator line]
3. [Example narrator line]
4. [Example narrator line]
5. [Example narrator line]

[If WITHOUT_NARRATOR:]
CHARACTER_ID_STRATEGY: [How to distinguish character voices]
SCENE_TRANSITIONS: [Audio techniques for scene changes]
EXPOSITION_TACTICS: [How to deliver necessary information]
INTERNAL_THOUGHTS: [Alternatives for character psychology]
TIMELINE_CLARIFICATION: [Methods for time/location changes]

[If HYBRID:]
USAGE_TRIGGERS: [When narrator appears]
JUSTIFICATION: [How narrator presence/absence is explained in-story]

PRODUCTION_IMPACT:
Budget: [Cost implications]
Schedule: [Timeline changes]
Technical: [Audio engineering requirements]
Casting: [Additional voice talent needs]

IMPLEMENTATION_GUIDELINES:
Station_5: [How this affects season architecture]
Script_Development: [Writing style requirements]
Audio_Production: [Sound design implications]
Quality_Control: [Testing requirements]
"""

    async def process(self, session_id: str) -> NarratorRecommendationDocument:
        """
        Main processing method for Station 4.5
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            NarratorRecommendationDocument: Complete narrator strategy recommendation
        """
        try:
            logger.info(f"Station 4.5 processing started for session {session_id}")
            
            # Load previous station outputs
            project_data = await self._load_project_data(session_id)
            if not project_data:
                raise ValueError("Could not load required data from previous stations")
            
            # TASK 1: Complexity Analysis
            logger.info("Starting complexity analysis...")
            complexity_score = await self._analyze_complexity(project_data)
            
            # TASK 2: Generate Sample Scenes
            logger.info("Generating demonstration scenes...")
            sample_scenes = await self._generate_sample_scenes(project_data)
            
            # TASK 3: Generate Final Recommendation
            logger.info("Creating final recommendation...")
            recommendation_data = await self._generate_recommendation(
                project_data, complexity_score, sample_scenes
            )
            
            # TASK 4: Create Production Impact Assessment
            production_impact = self._assess_production_impact(recommendation_data)
            
            # TASK 5: Generate Implementation Guidelines
            implementation_guidelines = self._create_implementation_guidelines(
                recommendation_data, project_data
            )
            
            # Compile final document
            narrator_document = NarratorRecommendationDocument(
                working_title=project_data.get("working_title", "Untitled Project"),
                executive_summary=recommendation_data["executive_summary"],
                complexity_analysis=complexity_score,
                sample_scenes=sample_scenes,
                recommendation=NarratorRecommendation(recommendation_data["recommendation"]),
                narrator_strategy=recommendation_data.get("narrator_strategy"),
                alternative_strategy=recommendation_data.get("alternative_strategy"),
                production_impact=production_impact,
                implementation_guidelines=implementation_guidelines,
                session_id=session_id,
                created_timestamp=datetime.utcnow()
            )
            
            # Store in Redis for next station
            await self._store_output(session_id, narrator_document)
            
            logger.info(f"Station 4.5 completed successfully for session {session_id}")
            return narrator_document
            
        except Exception as e:
            logger.error(f"Station 4.5 processing failed for session {session_id}: {str(e)}")
            raise

    async def _load_project_data(self, session_id: str) -> Dict[str, Any]:
        """Load all previous station data for context"""
        try:
            # Load all previous station outputs
            station_keys = [
                f"audiobook:{session_id}:station_01",
                f"audiobook:{session_id}:station_02", 
                f"audiobook:{session_id}:station_03",
                f"audiobook:{session_id}:station_04"
            ]
            
            station_data = {}
            for i, key in enumerate(station_keys, 1):
                data = await self.redis.get(key)
                if data:
                    station_data[f"station_{i}"] = json.loads(data)
            
            if not station_data.get("station_4"):
                logger.error("Station 4 data not found - required for Station 4.5")
                return None
            
            # Combine relevant data for analysis
            project_context = {
                # From Station 1
                "original_seed": station_data.get("station_1", {}).get("original_seed", ""),
                "scale_choice": station_data.get("station_1", {}).get("recommended_option", "B"),
                
                # From Station 2
                "working_title": station_data.get("station_2", {}).get("working_title", "Untitled"),
                "world_setting": station_data.get("station_2", {}).get("world_setting", {}),
                "format_specifications": station_data.get("station_2", {}).get("format_specifications", {}),
                "genre_tone": station_data.get("station_2", {}).get("genre_tone", {}),
                "audience_profile": station_data.get("station_2", {}).get("audience_profile", {}),
                
                # From Station 3
                "age_guidelines": station_data.get("station_3", {}).get("age_guidelines", {}),
                "genre_options": station_data.get("station_3", {}).get("genre_options", []),
                "tone_calibration": station_data.get("station_3", {}).get("tone_calibration", {}),
                
                # From Station 4
                "seed_collection": station_data.get("station_4", {}).get("seed_collection", {}),
                "tactical_extractions": station_data.get("station_4", {}).get("tactical_extractions", []),
                "total_seeds": station_data.get("station_4", {}).get("total_seeds", 0)
            }
            
            return project_context
            
        except Exception as e:
            logger.error(f"Failed to load project data: {str(e)}")
            return None

    async def _analyze_complexity(self, project_data: Dict[str, Any]) -> ComplexityScore:
        """Analyze story complexity for narrator necessity"""
        try:
            # Format context and story elements for LLM
            project_context = self._format_project_context(project_data)
            story_elements = self._format_story_elements(project_data)
            
            prompt = self.complexity_analysis_prompt.format(
                project_context=json.dumps(project_context, indent=2),
                story_elements=story_elements
            )
            
            # Get LLM response
            response = await self.openrouter.generate(
                prompt=prompt,
                model="grok-4",
                max_tokens=2000,
                temperature=0.3  # Lower temperature for consistent scoring
            )
            
            # Parse complexity analysis
            complexity_score = self._parse_complexity_response(response)
            
            logger.info(f"Complexity analysis completed - Total score: {complexity_score.total_score}/75")
            return complexity_score
            
        except Exception as e:
            logger.error(f"Failed to analyze complexity: {str(e)}")
            raise

    async def _generate_sample_scenes(self, project_data: Dict[str, Any]) -> List[SampleScene]:
        """Generate demonstration scenes with and without narrator"""
        try:
            project_context = self._format_project_context(project_data)
            story_elements = self._format_story_elements(project_data)
            
            prompt = self.scene_generation_prompt.format(
                project_context=json.dumps(project_context, indent=2),
                story_elements=story_elements
            )
            
            # Get LLM response
            response = await self.openrouter.generate(
                prompt=prompt,
                model="grok-4", 
                max_tokens=4000,
                temperature=0.7  # Higher creativity for scene writing
            )
            
            # Parse scene response
            sample_scene = self._parse_scene_response(response)
            
            logger.info("Sample scenes generated successfully")
            return [sample_scene]
            
        except Exception as e:
            logger.error(f"Failed to generate sample scenes: {str(e)}")
            raise

    async def _generate_recommendation(self, project_data: Dict[str, Any], 
                                     complexity_score: ComplexityScore,
                                     sample_scenes: List[SampleScene]) -> Dict[str, Any]:
        """Generate final narrator strategy recommendation"""
        try:
            project_context = self._format_project_context(project_data)
            
            prompt = self.recommendation_prompt.format(
                project_context=json.dumps(project_context, indent=2),
                complexity_analysis=asdict(complexity_score),
                sample_scenes=json.dumps([asdict(scene) for scene in sample_scenes], indent=2)
            )
            
            # Get LLM response
            response = await self.openrouter.generate(
                prompt=prompt,
                model="grok-4",
                max_tokens=3000,
                temperature=0.4
            )
            
            # Parse recommendation response
            recommendation_data = self._parse_recommendation_response(response)
            
            logger.info(f"Recommendation generated: {recommendation_data['recommendation']}")
            return recommendation_data
            
        except Exception as e:
            logger.error(f"Failed to generate recommendation: {str(e)}")
            raise

    def _format_project_context(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format project data for LLM consumption"""
        return {
            "working_title": project_data.get("working_title", "Untitled Project"),
            "original_seed": project_data.get("original_seed", ""),
            "scale_choice": project_data.get("scale_choice", "B"),
            "world_setting": project_data.get("world_setting", {}),
            "genre_tone": project_data.get("genre_tone", {}),
            "target_age_range": project_data.get("age_guidelines", {}).get("target_age_range", "Unknown"),
            "content_rating": project_data.get("age_guidelines", {}).get("content_rating", "PG"),
            "episode_specifications": project_data.get("format_specifications", {}),
            "total_story_seeds": project_data.get("total_seeds", 0)
        }

    def _format_story_elements(self, project_data: Dict[str, Any]) -> str:
        """Format story elements for analysis"""
        elements = []
        
        # Add seed collection summary
        seed_collection = project_data.get("seed_collection", {})
        if seed_collection:
            elements.append(f"Story Seeds: {seed_collection.get('micro_moments', 0)} micro-moments, "
                          f"{seed_collection.get('episode_beats', 0)} episode beats, "
                          f"{seed_collection.get('season_arcs', 0)} season arcs, "
                          f"{seed_collection.get('series_defining', 0)} series-defining moments")
        
        # Add world setting details
        world_setting = project_data.get("world_setting", {})
        if world_setting:
            elements.append(f"Setting: {world_setting.get('primary_location', 'Unknown')}")
            elements.append(f"Time Period: {world_setting.get('time_period', 'Unknown')}")
        
        # Add genre information
        genre_tone = project_data.get("genre_tone", {})
        if genre_tone:
            elements.append(f"Primary Genre: {genre_tone.get('primary_genre', 'Unknown')}")
            elements.append(f"Secondary Genres: {genre_tone.get('secondary_genres', [])}")
        
        # Add tactical extractions summary
        tactical_count = len(project_data.get("tactical_extractions", []))
        elements.append(f"Extracted storytelling tactics: {tactical_count}")
        
        return "\n".join(elements)

    def _parse_complexity_response(self, response: str) -> ComplexityScore:
        """Parse complexity analysis response"""
        try:
            # Extract complexity factors
            complexity_factors = {}
            complexity_section = re.search(r'COMPLEXITY_FACTORS:(.*?)AUDIO_CLARITY_FACTORS:', response, re.DOTALL)
            if complexity_section:
                for line in complexity_section.group(1).strip().split('\n'):
                    if ':' in line and any(char.isdigit() for char in line):
                        parts = line.split(':')
                        if len(parts) >= 2:
                            key = parts[0].strip()
                            score_match = re.search(r'(\d+)', parts[1])
                            if score_match:
                                complexity_factors[key] = int(score_match.group(1))
            
            # Extract audio clarity factors
            audio_clarity_factors = {}
            audio_section = re.search(r'AUDIO_CLARITY_FACTORS:(.*?)STYLISTIC_FACTORS:', response, re.DOTALL)
            if audio_section:
                for line in audio_section.group(1).strip().split('\n'):
                    if ':' in line and any(char.isdigit() for char in line):
                        parts = line.split(':')
                        if len(parts) >= 2:
                            key = parts[0].strip()
                            score_match = re.search(r'(\d+)', parts[1])
                            if score_match:
                                audio_clarity_factors[key] = int(score_match.group(1))
            
            # Extract stylistic factors
            stylistic_factors = {}
            stylistic_section = re.search(r'STYLISTIC_FACTORS:(.*?)TOTAL_SCORE:', response, re.DOTALL)
            if stylistic_section:
                for line in stylistic_section.group(1).strip().split('\n'):
                    if ':' in line and any(char.isdigit() for char in line):
                        parts = line.split(':')
                        if len(parts) >= 2:
                            key = parts[0].strip()
                            score_match = re.search(r'(\d+)', parts[1])
                            if score_match:
                                stylistic_factors[key] = int(score_match.group(1))
            
            # Extract total score
            total_match = re.search(r'TOTAL_SCORE:\s*(\d+)', response)
            total_score = int(total_match.group(1)) if total_match else 0
            
            # If total score not found, calculate from individual scores
            if total_score == 0:
                total_score = sum(complexity_factors.values()) + sum(audio_clarity_factors.values()) + sum(stylistic_factors.values())
            
            # Extract recommendation tier
            tier_match = re.search(r'RECOMMENDATION_TIER:\s*([^|\n]+)', response)
            recommendation_tier = tier_match.group(1).strip() if tier_match else "Unknown"
            
            return ComplexityScore(
                complexity_factors=complexity_factors,
                audio_clarity_factors=audio_clarity_factors,
                stylistic_factors=stylistic_factors,
                total_score=total_score,
                recommendation_tier=recommendation_tier
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse complexity response: {str(e)}")
            # Return fallback complexity score
            return ComplexityScore(
                complexity_factors={"fallback": 3},
                audio_clarity_factors={"fallback": 3},
                stylistic_factors={"fallback": 3},
                total_score=45,
                recommendation_tier="Could work either way"
            )

    def _parse_scene_response(self, response: str) -> SampleScene:
        """Parse sample scene response"""
        try:
            # Extract scene title
            title_match = re.search(r'SCENE_TITLE:\s*([^\n]+)', response)
            scene_title = title_match.group(1).strip() if title_match else "Sample Scene"
            
            # Extract with narrator version
            narrator_match = re.search(r'VERSION_A_WITH_NARRATOR:(.*?)VERSION_B_WITHOUT_NARRATOR:', response, re.DOTALL)
            with_narrator = narrator_match.group(1).strip() if narrator_match else "Scene with narrator not found"
            
            # Extract without narrator version
            no_narrator_match = re.search(r'VERSION_B_WITHOUT_NARRATOR:(.*?)SCENE_NOTES:', response, re.DOTALL)
            without_narrator = no_narrator_match.group(1).strip() if no_narrator_match else "Scene without narrator not found"
            
            # Extract scene notes
            notes_match = re.search(r'SCENE_NOTES:(.*?)$', response, re.DOTALL)
            scene_notes = notes_match.group(1).strip() if notes_match else "Analysis not provided"
            
            return SampleScene(
                scene_title=scene_title,
                with_narrator=with_narrator,
                without_narrator=without_narrator,
                scene_notes=scene_notes
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse scene response: {str(e)}")
            return SampleScene(
                scene_title="Sample Scene",
                with_narrator="Scene with narrator could not be generated",
                without_narrator="Scene without narrator could not be generated", 
                scene_notes="Scene analysis unavailable"
            )

    def _parse_recommendation_response(self, response: str) -> Dict[str, Any]:
        """Parse recommendation response"""
        try:
            # Extract recommendation
            rec_match = re.search(r'RECOMMENDATION:\s*([^\n]+)', response)
            raw_recommendation = rec_match.group(1).strip() if rec_match else "WITHOUT_NARRATOR"
            
            # Normalize recommendation format
            if "WITH_NARRATOR" in raw_recommendation or "With Narrator" in raw_recommendation:
                recommendation = "WITH_NARRATOR"
            elif "HYBRID" in raw_recommendation or "Hybrid" in raw_recommendation:
                recommendation = "HYBRID_APPROACH"
            else:
                recommendation = "WITHOUT_NARRATOR"
            
            # Extract executive summary
            summary_match = re.search(r'EXECUTIVE_SUMMARY:(.*?)(?=NARRATOR_IDENTITY:|CHARACTER_ID_STRATEGY:|USAGE_TRIGGERS:|PRODUCTION_IMPACT:)', response, re.DOTALL)
            executive_summary = summary_match.group(1).strip() if summary_match else "No summary provided"
            
            result = {
                "recommendation": recommendation,
                "executive_summary": executive_summary
            }
            
            # Parse based on recommendation type
            if "WITH_NARRATOR" in recommendation:
                result["narrator_strategy"] = self._parse_narrator_strategy(response)
            elif "WITHOUT_NARRATOR" in recommendation:
                result["alternative_strategy"] = self._parse_alternative_strategy(response)
            elif "HYBRID" in recommendation:
                result["narrator_strategy"] = self._parse_narrator_strategy(response)
                result["hybrid_triggers"] = self._parse_hybrid_triggers(response)
            
            return result
            
        except Exception as e:
            logger.warning(f"Failed to parse recommendation response: {str(e)}")
            return {
                "recommendation": "WITHOUT_NARRATOR",
                "executive_summary": "Recommendation could not be parsed - defaulting to no narrator approach"
            }

    def _parse_narrator_strategy(self, response: str) -> NarratorStrategy:
        """Parse narrator strategy from response"""
        try:
            # Extract identity type
            identity_match = re.search(r'NARRATOR_IDENTITY:\s*([^\n]+)', response)
            identity_str = identity_match.group(1).strip() if identity_match else "Omniscient third-person"
            
            # Map to enum
            identity_type = NarratorIdentityType.OMNISCIENT_THIRD_PERSON
            for enum_val in NarratorIdentityType:
                if enum_val.value.lower() in identity_str.lower():
                    identity_type = enum_val
                    break
            
            # Extract presence level
            presence_match = re.search(r'PRESENCE_LEVEL:\s*([^\n]+)', response)
            presence_str = presence_match.group(1).strip() if presence_match else "Moderate"
            
            presence_level = NarratorPresenceLevel.MODERATE
            for enum_val in NarratorPresenceLevel:
                if enum_val.value.lower().startswith(presence_str.lower()):
                    presence_level = enum_val
                    break
            
            # Extract key functions
            functions_match = re.search(r'KEY_FUNCTIONS:\s*\[(.*?)\]', response)
            if functions_match:
                functions_str = functions_match.group(1)
                key_functions = [f.strip().strip('"\'') for f in functions_str.split(',')]
            else:
                key_functions = ["Scene setting", "Character thoughts", "Transitions"]
            
            # Extract voice casting
            casting_match = re.search(r'VOICE_CASTING:\s*([^\n]+)', response)
            voice_casting = casting_match.group(1).strip() if casting_match else "Professional narrator, gender neutral, mature voice"
            
            # Extract sample lines
            lines_section = re.search(r'SAMPLE_LINES:(.*?)(?=\n[A-Z_]+:|$)', response, re.DOTALL)
            sample_lines = []
            if lines_section:
                for line in lines_section.group(1).strip().split('\n'):
                    if line.strip() and (line.strip().startswith(('1.', '2.', '3.', '4.', '5.')) or line.strip().startswith('-')):
                        clean_line = re.sub(r'^\d+\.\s*', '', line.strip())
                        clean_line = re.sub(r'^-\s*', '', clean_line)
                        if clean_line:
                            sample_lines.append(clean_line)
            
            if not sample_lines:
                sample_lines = [
                    "The morning brought unexpected news to the quiet town.",
                    "The protagonist felt their heart racing, though they tried to appear calm.",
                    "Three days later, everything had changed.",
                    "The decision would haunt them for years to come.",
                    "In that moment, the truth became crystal clear."
                ]
            
            return NarratorStrategy(
                identity_type=identity_type,
                presence_level=presence_level,
                key_functions=key_functions[:5],  # Limit to 5
                voice_casting_notes=voice_casting,
                sample_narrator_lines=sample_lines[:5]  # Limit to 5
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse narrator strategy: {str(e)}")
            return NarratorStrategy(
                identity_type=NarratorIdentityType.OMNISCIENT_THIRD_PERSON,
                presence_level=NarratorPresenceLevel.MODERATE,
                key_functions=["Scene setting", "Character thoughts", "Transitions"],
                voice_casting_notes="Professional narrator required",
                sample_narrator_lines=["Sample narrator line unavailable"]
            )

    def _parse_alternative_strategy(self, response: str) -> AlternativeStrategy:
        """Parse alternative strategy for no-narrator approach"""
        try:
            # Extract each strategy component
            char_id_match = re.search(r'CHARACTER_ID_STRATEGY:\s*([^\n]+)', response)
            character_id_strategy = char_id_match.group(1).strip() if char_id_match else "Distinct voice acting and character-specific speech patterns"
            
            transitions_match = re.search(r'SCENE_TRANSITIONS:\s*([^\n]+)', response) 
            scene_transition_methods = transitions_match.group(1).strip() if transitions_match else "Sound effects and musical cues for scene changes"
            
            exposition_match = re.search(r'EXPOSITION_TACTICS:\s*([^\n]+)', response)
            exposition_tactics = exposition_match.group(1).strip() if exposition_match else "Natural dialogue and character conversations"
            
            thoughts_match = re.search(r'INTERNAL_THOUGHTS:\s*([^\n]+)', response)
            internal_thought_alternatives = thoughts_match.group(1).strip() if thoughts_match else "Character monologue and verbal reactions"
            
            timeline_match = re.search(r'TIMELINE_CLARIFICATION:\s*([^\n]+)', response)
            timeline_clarification = timeline_match.group(1).strip() if timeline_match else "Audio cues and character dialogue references"
            
            return AlternativeStrategy(
                character_id_strategy=character_id_strategy,
                scene_transition_methods=scene_transition_methods,
                exposition_tactics=exposition_tactics,
                internal_thought_alternatives=internal_thought_alternatives,
                timeline_clarification=timeline_clarification
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse alternative strategy: {str(e)}")
            return AlternativeStrategy(
                character_id_strategy="Distinct voice acting required",
                scene_transition_methods="Sound effects for transitions",
                exposition_tactics="Natural dialogue exposition",
                internal_thought_alternatives="Character verbal reactions",
                timeline_clarification="Audio cues for time changes"
            )

    def _parse_hybrid_triggers(self, response: str) -> Dict[str, str]:
        """Parse hybrid approach triggers"""
        try:
            triggers_match = re.search(r'USAGE_TRIGGERS:\s*([^\n]+)', response)
            usage_triggers = triggers_match.group(1).strip() if triggers_match else "Complex scenes requiring additional context"
            
            justification_match = re.search(r'JUSTIFICATION:\s*([^\n]+)', response)
            justification = justification_match.group(1).strip() if justification_match else "Narrator appears as story element when needed"
            
            return {
                "usage_triggers": usage_triggers,
                "justification": justification
            }
            
        except Exception as e:
            logger.warning(f"Failed to parse hybrid triggers: {str(e)}")
            return {
                "usage_triggers": "When additional context is needed",
                "justification": "Narrator as story device"
            }

    def _assess_production_impact(self, recommendation_data: Dict[str, Any]) -> ProductionImpact:
        """Assess production impact of narrator decision"""
        
        if recommendation_data["recommendation"] == "WITH_NARRATOR":
            return ProductionImpact(
                budget_implications="Additional narrator casting and recording costs - estimate 15-25% budget increase",
                schedule_changes="Extra recording sessions and editing time - add 2-3 weeks to production",
                technical_requirements="Enhanced audio engineering for narrator mixing and voice treatment",
                casting_needs="Professional narrator casting required - specific voice qualities needed"
            )
        elif recommendation_data["recommendation"] == "HYBRID_APPROACH":
            return ProductionImpact(
                budget_implications="Moderate additional costs for selective narrator use - estimate 8-15% budget increase",
                schedule_changes="Some additional recording and editing - add 1-2 weeks to production",
                technical_requirements="Flexible audio setup for narrator integration in select scenes",
                casting_needs="Narrator casting for specific episodes/scenes only"
            )
        else:  # WITHOUT_NARRATOR
            return ProductionImpact(
                budget_implications="No additional narrator costs - potential savings of 10-20%",
                schedule_changes="Streamlined production without narrator recording sessions",
                technical_requirements="Focus on character voice distinction and sound design clarity",
                casting_needs="Enhanced voice acting requirements for main cast"
            )

    def _create_implementation_guidelines(self, recommendation_data: Dict[str, Any], 
                                        project_data: Dict[str, Any]) -> Dict[str, str]:
        """Create implementation guidelines for subsequent stations"""
        
        guidelines = {}
        
        if recommendation_data["recommendation"] == "WITH_NARRATOR":
            guidelines["Station_5"] = "Design season architecture with narrator consideration - plan narrator intro/outro patterns"
            guidelines["Script_Development"] = "Write dialogue assuming narrator support - can be more subtle and realistic"
            guidelines["Audio_Production"] = "Plan for narrator recording sessions and voice treatment requirements"
            guidelines["Quality_Control"] = "Test narrator/character voice balance and clarity in audio mixes"
            
        elif recommendation_data["recommendation"] == "HYBRID_APPROACH":
            guidelines["Station_5"] = "Identify specific episodes/scenes requiring narrator - plan hybrid structure"
            guidelines["Script_Development"] = "Mark narrator scenes clearly - maintain consistency in narrator voice"
            guidelines["Audio_Production"] = "Prepare flexible recording setup for narrator integration"
            guidelines["Quality_Control"] = "Validate narrator presence/absence transitions feel natural"
            
        else:  # WITHOUT_NARRATOR
            guidelines["Station_5"] = "Design season structure with clear audio-only scene transitions"
            guidelines["Script_Development"] = "Ensure all exposition works through dialogue and action - no narrator dependency"
            guidelines["Audio_Production"] = "Emphasize character voice distinction and environmental audio storytelling"
            guidelines["Quality_Control"] = "Test scene clarity and character identification without narrator assistance"
        
        return guidelines

    async def _store_output(self, session_id: str, narrator_document: NarratorRecommendationDocument) -> None:
        """Store output in Redis for next station"""
        try:
            # Convert to dictionary for JSON serialization
            output_dict = {
                "station_id": self.station_id,
                "working_title": narrator_document.working_title,
                "executive_summary": narrator_document.executive_summary,
                "complexity_analysis": asdict(narrator_document.complexity_analysis),
                "sample_scenes": [asdict(scene) for scene in narrator_document.sample_scenes],
                "recommendation": narrator_document.recommendation.value,
                "narrator_strategy": asdict(narrator_document.narrator_strategy) if narrator_document.narrator_strategy else None,
                "alternative_strategy": asdict(narrator_document.alternative_strategy) if narrator_document.alternative_strategy else None,
                "production_impact": asdict(narrator_document.production_impact),
                "implementation_guidelines": narrator_document.implementation_guidelines,
                "session_id": narrator_document.session_id,
                "created_timestamp": narrator_document.created_timestamp.isoformat()
            }
            
            # Store in Redis with session-based key
            key = f"audiobook:{session_id}:station_04_5"
            json_str = json.dumps(output_dict, default=str)
            await self.redis.set(key, json_str, expire=86400)  # 24 hour expiry
            
            logger.info(f"Station 4.5 output stored successfully for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store Station 4.5 output: {str(e)}")
            raise

    def export_to_pdf(self, narrator_document: NarratorRecommendationDocument, filename: str = None) -> str:
        """
        Export Station 4.5 output to PDF
        
        Args:
            narrator_document: Station 4.5 processing output
            filename: Optional custom filename
            
        Returns:
            str: Path to the generated PDF file
        """
        # from app.pdf_exporter import Station45PDFExporter  # Not implemented
        
        # exporter = Station45PDFExporter()  # Not implemented
        # return exporter.export_station45_output(narrator_document, filename)
        return "PDF export not implemented"
    
    def format_for_human_review(self, narrator_document: NarratorRecommendationDocument) -> Dict:
        """Format output for human review/approval interface"""
        return {
            "station": "Station 4.5: Narrator Strategy Designer",
            "status": "awaiting_human_approval",
            "working_title": narrator_document.working_title,
            "recommendation": narrator_document.recommendation.value,
            "summary": narrator_document.executive_summary,
            "complexity_score": f"{narrator_document.complexity_analysis.total_score}/75",
            "sample_scenes_count": len(narrator_document.sample_scenes),
            "production_impact": {
                "budget": narrator_document.production_impact.budget_implications,
                "schedule": narrator_document.production_impact.schedule_changes,
                "casting": narrator_document.production_impact.casting_needs
            },
            "next_step": "Please review the narrator strategy and approve to proceed to Station 5: Season Architecture Design"
        }


