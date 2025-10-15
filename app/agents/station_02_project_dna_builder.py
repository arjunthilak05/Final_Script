"""
Station 2: Project DNA Builder Agent

This agent takes the scale choice from Station 1 and creates a comprehensive 
Project Bible that establishes the core identity of the audiobook series.

Dependencies: Station 1 output (scale choice and initial expansion)
Outputs: Complete Project Bible (8 sections)
Human Gate: CRITICAL - Bible approval affects entire production pipeline
"""

import json
import re
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.config import Settings
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

logger = logging.getLogger(__name__)

class ContentRating(Enum):
    G = "G"
    PG = "PG" 
    PG13 = "PG-13"
    R = "R"

class BudgetTier(Enum):
    LOW = "Low Budget"
    MEDIUM = "Medium Budget"
    HIGH = "High Budget"
    PREMIUM = "Premium Budget"

@dataclass
class WorldSetting:
    """World and setting information"""
    time_period: str
    primary_location: str
    setting_type: str
    atmosphere: str
    key_locations: List[str]
    historical_context: str
    cultural_elements: List[str]

@dataclass
class FormatSpecifications:
    """Technical format specifications"""
    series_type: str
    episode_count: str
    episode_length: str
    season_structure: str
    pacing_strategy: str
    narrative_structure: str

@dataclass
class GenreTone:
    """Genre and tone definition"""
    primary_genre: str
    secondary_genres: List[str]
    tone_descriptors: List[str]
    mood_profile: str
    genre_conventions: List[str]

@dataclass
class CreativePromises:
    """Creative commitments for the series"""
    core_hooks: List[str]
    unique_elements: List[str]
    emotional_journey: str
    story_pillars: List[str]

@dataclass
class AudienceProfile:
    """Target audience definition"""
    primary_age_range: str
    target_demographics: List[str]
    core_interests: List[str]
    listening_context: str
    content_preferences: List[str]

@dataclass
class ProductionConstraints:
    """Production and technical constraints"""
    content_rating: ContentRating
    budget_tier: BudgetTier
    technical_requirements: List[str]
    content_restrictions: List[str]
    distribution_channels: List[str]

@dataclass
class CreativeTeam:
    """Team and decision-making structure"""
    required_roles: List[str]
    specialized_skills: List[str]
    team_structure: str
    collaboration_style: str
    key_partnerships: List[str]

@dataclass
class ProjectBible:
    """Complete Project Bible output from Station 2"""
    working_title: str
    world_setting: WorldSetting
    format_specifications: FormatSpecifications
    genre_tone: GenreTone
    creative_promises: CreativePromises
    audience_profile: AudienceProfile
    production_constraints: ProductionConstraints
    creative_team: CreativeTeam
    session_id: str
    created_timestamp: datetime
    station_1_reference: Dict[str, Any]

class Station02ProjectDNABuilder:
    """
    Station 2: Project DNA Builder
    
    Creates comprehensive Project Bible using multi-step AI analysis.
    Each section is generated with specialized prompts for consistent quality.
    """
    
    def __init__(self):
        self.settings = Settings()
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.station_id = "station_02"
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=2)
        
        # Section-specific prompts (loaded from config)
        self.section_prompts = self.config.get_all_prompts()
        
    async def initialize(self):
        """Initialize Station 2 processor"""
        await self.redis.initialize()
        
    def _load_section_prompts(self) -> Dict[str, str]:
        """Load specialized prompts for each bible section"""
        # This method is deprecated - prompts are now loaded from YML config
        # Keeping for backwards compatibility
        return self.section_prompts if hasattr(self, 'section_prompts') else {
            "world": """
You are the World Building Specialist for audiobook production.

Based on the story concept and scale choice, create detailed world and setting information:

REQUIREMENTS:
1. PRIMARY LOCATIONS (3-5 key places):
   - Where most scenes take place
   - Consider audio storytelling needs
   - Each location needs distinct acoustic signature
   - Think about how each place SOUNDS different

2. TIME PERIOD/YEAR:
   - When story takes place
   - Historical context if relevant
   - Technology level considerations

3. ATMOSPHERE/MOOD:
   - Overall emotional tone of the world
   - How environment affects characters
   - Audio mood descriptors

4. CULTURAL CONTEXT:
   - Social environment
   - Rules and norms that matter to the story
   - Background that affects character behavior

Focus on audio-specific considerations. How will each location SOUND different?
Keep practical for audio-only production.

STORY CONTEXT: {context}

Provide detailed world building analysis.
""",

            "format": """
You are the Format Specification Expert for audiobook production.

Based on the scale choice from Station 1, define technical format specifications:

REQUIREMENTS:
1. AUDIO-ONLY CONSTRAINTS:
   - What visual elements must be converted to audio
   - Dialogue vs narration balance
   - Sound effect requirements

2. EPISODE COUNT: Use exact count from Station 1 scale choice
3. EPISODE LENGTH TARGET: Use exact length from Station 1
4. RELEASE CADENCE: 
   - Weekly, bi-weekly, or all-at-once
   - Consider audience engagement patterns

5. SEASON STRUCTURE:
   - How episodes group together
   - Natural story arcs within season
   - Cliffhanger and pacing strategy

Be specific and practical for production planning.

STORY CONTEXT: {context}

Provide detailed format specifications.
""",

            "genre": """
You are the Genre and Tone Expert for audiobook production.

Analyze the story concept and define genre/tone framework:

REQUIREMENTS:
1. PRIMARY GENRE: Single main genre that best fits the story
2. SECONDARY GENRE ELEMENTS (2-3):
   - Supporting genres that add complexity
   - How they blend with primary genre

3. TONE DESCRIPTORS (3-5 adjectives):
   - Emotional tone words
   - How story should FEEL to listeners
   - Audio-specific tone considerations

4. SIMILAR SUCCESSFUL SHOWS (3-5 references):
   - Existing audio content for comparison
   - What elements to emulate
   - What to differentiate from

Consider audio storytelling conventions for each genre.

STORY CONTEXT: {context}

Provide detailed genre and tone analysis.
""",

            "audience": """
You are the Audience Profiling Expert for audiobook production.

Define the target audience based on story content and genre:

REQUIREMENTS:
1. PRIMARY AGE RANGE: Be specific (e.g., "25-45", "18-35")
2. CONTENT RATING: Choose appropriate rating:
   - G: General audiences, no mature content
   - PG: Mild language/themes, suitable for most
   - PG-13: Some mature themes, strong language occasional
   - R: Mature themes, strong language, adult situations

3. EMOTIONAL GOALS FOR LISTENERS (3-4):
   - What emotions should audience feel?
   - What experience are we creating?
   - Why will they keep listening?

4. EXPECTED LISTENING CONTEXT:
   - Commuting, exercising, relaxing?
   - Attention level required
   - Binge vs episodic listening preference

Be realistic about audience expectations and market positioning.

STORY CONTEXT: {context}

Provide detailed audience profile analysis.
""",

            "production": """
You are the Production Constraints Expert for audiobook production.

Set realistic production parameters:

REQUIREMENTS:
1. MAXIMUM CAST SIZE:
   - How many voice actors needed?
   - Main characters vs supporting roles
   - Budget-conscious recommendations

2. SFX COMPLEXITY LEVEL:
   - Minimal: Basic sound effects only
   - Moderate: Enhanced ambience and effects
   - Rich: Complex soundscapes and production

3. MUSIC REQUIREMENTS:
   - Theme music, transitions, emotional scoring
   - Production complexity level
   - Budget considerations

4. LANGUAGES: Primary language, any secondary needs
5. LOCALIZATION NEEDS: International distribution plans

Balance creative vision with production realities.

STORY CONTEXT: {context}

Provide detailed production constraint analysis.
""",

            "creative": """
You are the Creative Team Structure Expert.

Define the creative decision-making structure:

REQUIREMENTS:
1. SHOWRUNNER/CREATOR: Who has final creative authority?
2. KEY DECISION MAKERS (2-4 roles):
   - Who approves major creative choices?
   - Writing, directing, production roles
   - Clear hierarchy

3. APPROVAL GATES:
   - What decisions need approval?
   - Script approval, casting, music choices
   - Quality control checkpoints

Keep structure simple but clear for decision-making.

STORY CONTEXT: {context}

Provide detailed creative team structure.
""",

            "integration": """
You are the Project Bible Integration Expert.

Review all sections and ensure:
1. CONSISTENCY: All sections align and support each other
2. COMPLETENESS: No missing information or contradictions  
3. FEASIBILITY: Everything is realistic for production
4. COHERENCE: The bible tells a unified story about the project

Suggest a compelling working title that captures the essence.
Flag any inconsistencies or gaps.

ALL SECTIONS: {all_sections}

Provide integration analysis and title recommendation.
"""
        }

    async def process(self, station1_data: Dict[str, Any], session_id: str) -> ProjectBible:
        """
        Main processing method for Station 2
        
        Args:
            station1_data: Station 1 output data dictionary
            session_id: Session ID for tracking
            
        Returns:
            ProjectBible: Complete project bible
        """
        try:
            logger.info(f"Station 2 processing started for session {session_id}")
            
            # Load and validate story lock
            story_lock_key = f"audiobook:{session_id}:story_lock"
            story_lock_raw = await self.redis.get(story_lock_key)
            if not story_lock_raw:
                logger.warning("Story lock missing - cannot fully preserve story concept")
                story_lock = {'main_characters': [], 'core_mechanism': '', 'key_plot_points': []}
            else:
                story_lock = json.loads(story_lock_raw)
                logger.info(f"Story lock loaded: {[c['name'] for c in story_lock.get('main_characters', [])]}")
            
            # Use provided Station 1 data
            if not station1_data:
                raise ValueError(f"No Station 1 data provided")
            
            # Prepare context for AI agents (story lock already loaded and logged)
            context = self._prepare_context(station1_data)
            
            # Generate each bible section
            bible_sections = await self._generate_bible_sections(context)
            
            # Integrate all sections into final bible
            final_bible = await self._integrate_bible_sections(bible_sections, station1_data, session_id)
            
            # Store output for next station
            await self._store_output(session_id, final_bible)
            
            logger.info(f"Station 2 completed successfully for session {session_id}")
            return final_bible
            
        except Exception as e:
            logger.error(f"Station 2 processing failed for session {session_id}: {str(e)}")
            raise

    async def _get_station_1_output(self, session_id: str) -> Optional[Dict]:
        """Retrieve Station 1 output from Redis"""
        try:
            key = f"audiobook:{session_id}:station_01"
            stored_data = await self.redis.get(key)
            
            if not stored_data:
                logger.warning(f"No Station 1 data found for session {session_id}")
                return None
                
            return json.loads(stored_data)
            
        except Exception as e:
            logger.error(f"Failed to retrieve Station 1 output: {str(e)}")
            return None

    def _prepare_context(self, station_1_output: Dict) -> str:
        """Prepare context string for AI agents"""
        # Extract chosen scale option
        chosen_option = station_1_output.get("recommended_option", "B")
        scale_options = station_1_output.get("scale_options", [])
        
        # Find the chosen scale details
        chosen_scale = None
        option_index = ord(chosen_option) - ord('A')
        if 0 <= option_index < len(scale_options):
            chosen_scale = scale_options[option_index]
        else:
            chosen_scale = scale_options[1] if len(scale_options) > 1 else {}
        
        # Extract main characters from Station 1
        main_characters = station_1_output.get("initial_expansion", {}).get("main_characters", [])
        characters_text = ', '.join(main_characters) if main_characters else "Character names to be determined"
        
        context = f"""
ORIGINAL STORY CONCEPT: {station_1_output.get("original_seed", "")}

CHOSEN SCALE: {chosen_scale.get('option_type', 'STANDARD')} SERIES
- Episodes: {chosen_scale.get('episode_count', '8-12')}
- Length: {chosen_scale.get('episode_length', '35-45 min each')}
- Word Count: {chosen_scale.get('word_count', '60,000-100,000 total')}
- Best For: {chosen_scale.get('best_for', 'character journeys, mystery with layers')}

INITIAL EXPANSION FROM STATION 1:
- Working Titles: {', '.join(station_1_output.get("initial_expansion", {}).get("working_titles", []))}
- Main Characters: {characters_text}
- Core Premise: {station_1_output.get("initial_expansion", {}).get("core_premise", "")}
- Central Conflict: {station_1_output.get("initial_expansion", {}).get("central_conflict", "")}
- Episode Rationale: {station_1_output.get("initial_expansion", {}).get("episode_rationale", "")}
- Breaking Points: {', '.join(station_1_output.get("initial_expansion", {}).get("breaking_points", []))}
"""
        return context

    async def _generate_bible_sections(self, context: str) -> Dict[str, str]:
        """Generate each section of the Project Bible"""
        sections = {}
        
        # Generate each section using specialized prompts
        section_order = ["world", "format", "genre", "audience", "production", "creative"]
        
        for section_name in section_order:
            try:
                logger.info(f"Generating {section_name} section")
                
                # Format prompt with context
                prompt = self.section_prompts[section_name].format(context=context)
                
                # Generate section with AI using config model
                response = await self.openrouter.process_message(
                    prompt,
                    model_name=self.config.model
                )
                
                sections[section_name] = response.strip()
                logger.info(f"Generated {section_name} section ({len(response)} chars)")
                
            except Exception as e:
                logger.error(f"Failed to generate {section_name} section: {str(e)}")
                sections[section_name] = f"Error generating {section_name} section: {str(e)}"
        
        return sections

    async def _integrate_bible_sections(self, sections: Dict[str, str], station_1_output: Dict, session_id: str) -> ProjectBible:
        """Integrate all bible sections into final structured output"""
        try:
            # Use integration prompt to review consistency
            all_sections_text = "\n\n".join([f"{key.upper()} SECTION:\n{content}" for key, content in sections.items()])
            
            integration_prompt = self.section_prompts["integration"].format(all_sections=all_sections_text)
            
            integration_response = await self.openrouter.process_message(
                integration_prompt,
                model_name=self.config.model
            )
            
            logger.info("Integration analysis completed")
            
            # Parse sections into structured data
            bible = self._parse_sections_to_bible(sections, integration_response, station_1_output, session_id)
            
            return bible
            
        except Exception as e:
            logger.error(f"Failed to integrate bible sections: {str(e)}")
            raise

    def _parse_sections_to_bible(self, sections: Dict[str, str], integration: str, station_1_output: Dict, session_id: str) -> ProjectBible:
        """Parse JSON sections into structured ProjectBible"""

        # Extract working title from Station 1
        titles = station_1_output.get("initial_expansion", {}).get("working_titles", [])
        working_title = titles[0] if titles and titles[0] else "Untitled Project"

        # Parse world setting from JSON
        world_data = extract_json(sections["world"])
        world_setting = WorldSetting(
            time_period=world_data["time_period"],
            primary_location=world_data["primary_location"],
            setting_type=world_data["setting_type"],
            atmosphere=world_data["atmosphere"],
            key_locations=world_data["key_locations"],
            historical_context=world_data["historical_context"],
            cultural_elements=world_data["cultural_elements"]
        )

        # Parse format specifications from JSON
        format_data = extract_json(sections["format"])
        format_specs = FormatSpecifications(
            series_type=format_data["series_type"],
            episode_count=format_data["episode_count"],
            episode_length=format_data["episode_length"],
            season_structure=format_data["season_structure"],
            pacing_strategy=format_data["pacing_strategy"],
            narrative_structure=format_data["narrative_structure"]
        )

        # Parse genre and tone from JSON
        genre_data = extract_json(sections["genre"])
        genre_tone = GenreTone(
            primary_genre=genre_data["primary_genre"],
            secondary_genres=genre_data["secondary_genres"],
            tone_descriptors=genre_data["tone_descriptors"],
            mood_profile=genre_data["mood_profile"],
            genre_conventions=genre_data["genre_conventions"]
        )

        # Parse audience profile from JSON
        audience_data = extract_json(sections["audience"])
        audience_profile = AudienceProfile(
            primary_age_range=audience_data["primary_age_range"],
            target_demographics=audience_data["target_demographics"],
            core_interests=audience_data["core_interests"],
            listening_context=audience_data["listening_context"],
            content_preferences=audience_data["content_preferences"]
        )

        # Parse production constraints from JSON
        production_data = extract_json(sections["production"])
        production_constraints = ProductionConstraints(
            content_rating=ContentRating(production_data["content_rating"]),
            budget_tier=BudgetTier(production_data["budget_tier"]),
            technical_requirements=production_data["technical_requirements"],
            content_restrictions=production_data["content_restrictions"],
            distribution_channels=production_data["distribution_channels"]
        )

        # Parse creative team from JSON
        creative_data = extract_json(sections["creative"])
        creative_team = CreativeTeam(
            required_roles=creative_data["required_roles"],
            specialized_skills=creative_data["specialized_skills"],
            team_structure=creative_data["team_structure"],
            collaboration_style=creative_data["collaboration_style"],
            key_partnerships=creative_data["key_partnerships"]
        )

        # Creative promises from creative section
        creative_promises = CreativePromises(
            core_hooks=creative_data.get("core_hooks", ["Story engagement", "Character development"]),
            unique_elements=creative_data.get("unique_elements", ["Audio-optimized storytelling"]),
            emotional_journey=creative_data.get("emotional_journey", "Character growth"),
            story_pillars=creative_data.get("story_pillars", ["Strong narrative", "Engaging characters"])
        )

        return ProjectBible(
            working_title=working_title,
            world_setting=world_setting,
            format_specifications=format_specs,
            genre_tone=genre_tone,
            creative_promises=creative_promises,
            audience_profile=audience_profile,
            production_constraints=production_constraints,
            creative_team=creative_team,
            session_id=session_id,
            created_timestamp=datetime.utcnow(),
            station_1_reference=station_1_output
        )

    # Removed all extraction methods - using JSON directly from high-quality LLMs

    async def _store_output(self, session_id: str, bible: ProjectBible) -> None:
        """Store Project Bible in Redis"""
        try:
            # Convert to dictionary for JSON serialization
            bible_dict = asdict(bible)
            bible_dict["created_timestamp"] = bible.created_timestamp.isoformat()
            bible_dict["production_constraints"]["content_rating"] = bible.production_constraints.content_rating.value
            bible_dict["production_constraints"]["budget_tier"] = bible.production_constraints.budget_tier.value
            
            # Store in Redis
            key = f"audiobook:{session_id}:station_02"
            await self.redis.set(key, json.dumps(bible_dict), expire=86400)  # 24 hour expiry
            
            logger.info(f"Station 2 output stored successfully for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store Station 2 output: {str(e)}")
            raise

    async def get_stored_output(self, session_id: str) -> Optional[ProjectBible]:
        """Retrieve stored Project Bible for a session"""
        try:
            key = f"audiobook:{session_id}:station_02"
            stored_data = await self.redis.get(key)
            
            if not stored_data:
                return None
                
            data = json.loads(stored_data)
            
            # Reconstruct the dataclass objects
            world_setting = WorldSetting(**data["world_setting"])
            format_specifications = FormatSpecifications(**data["format_specifications"])
            genre_tone = GenreTone(**data["genre_tone"])
            creative_promises = CreativePromises(**data["creative_promises"])
            
            # Handle content rating enum
            content_rating = ContentRating(data["audience_profile"]["content_rating"])
            audience_data = data["audience_profile"].copy()
            audience_data["content_rating"] = content_rating
            audience_profile = AudienceProfile(**audience_data)
            
            production_constraints = ProductionConstraints(**data["production_constraints"])
            creative_team = CreativeTeam(**data["creative_team"])
            
            return ProjectBible(
                working_title=data["working_title"],
                world_setting=world_setting,
                format_specifications=format_specifications,
                genre_tone=genre_tone,
                creative_promises=creative_promises,
                audience_profile=audience_profile,
                production_constraints=production_constraints,
                creative_team=creative_team,
                session_id=data["session_id"],
                created_timestamp=datetime.fromisoformat(data["created_timestamp"]),
                station_1_reference=data["station_1_reference"]
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve Station 2 output: {str(e)}")
            return None

    def format_for_human_review(self, bible: ProjectBible) -> Dict:
        """Format Project Bible for human review/approval"""
        return {
            "station": "Station 2: Project DNA Builder",
            "status": "awaiting_human_approval",
            "working_title": bible.working_title,
            "project_bible": {
                "world_setting": {
                    "primary_locations": bible.world_setting.primary_locations,
                    "time_period": bible.world_setting.time_period,
                    "atmosphere": bible.world_setting.atmosphere_mood,
                    "cultural_context": bible.world_setting.cultural_context
                },
                "format_specifications": {
                    "episode_count": bible.format_specifications.episode_count,
                    "episode_length": bible.format_specifications.episode_length_target,
                    "release_cadence": bible.format_specifications.release_cadence,
                    "audio_constraints": bible.format_specifications.audio_only_constraints,
                    "season_structure": bible.format_specifications.season_structure
                },
                "genre_tone": {
                    "primary_genre": bible.genre_tone.primary_genre,
                    "secondary_elements": bible.genre_tone.secondary_genre_elements,
                    "tone": bible.genre_tone.tone_descriptors,
                    "similar_shows": bible.genre_tone.similar_successful_shows
                },
                "audience_profile": {
                    "age_range": bible.audience_profile.primary_age_range,
                    "content_rating": bible.audience_profile.content_rating.value,
                    "emotional_goals": bible.audience_profile.emotional_goals,
                    "listening_context": bible.audience_profile.expected_listening_context
                },
                "production_constraints": {
                    "max_cast_size": bible.production_constraints.maximum_cast_size,
                    "sfx_complexity": bible.production_constraints.sfx_complexity_level,
                    "music_needs": bible.production_constraints.music_requirements,
                    "languages": bible.production_constraints.languages,
                    "localization": bible.production_constraints.localization_needs
                },
                "creative_promises": {
                    "must_have": bible.creative_promises.must_have_elements,
                    "must_avoid": bible.creative_promises.must_avoid_elements,
                    "unique_points": bible.creative_promises.unique_selling_points
                },
                "creative_team": {
                    "showrunner": bible.creative_team.showrunner_creator,
                    "key_decision_makers": bible.creative_team.key_decision_makers,
                    "approval_gates": bible.creative_team.approval_gates
                }
            },
            "next_step": "Please review and approve the Project Bible to proceed to Station 3: Age & Genre Optimizer"
        }