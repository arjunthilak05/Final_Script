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
        
        # Section-specific prompts
        self.section_prompts = self._load_section_prompts()
        
    async def initialize(self):
        """Initialize Station 2 processor"""
        await self.redis.initialize()
        
    def _load_section_prompts(self) -> Dict[str, str]:
        """Load specialized prompts for each bible section"""
        return {
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
            
            # Use provided Station 1 data
            if not station1_data:
                raise ValueError(f"No Station 1 data provided")
            
            # Prepare context for AI agents
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
                
                # Generate section with AI
                response = await self.openrouter.generate(
                    prompt=prompt,
                    model="grok-4",
                    max_tokens=2000,
                    temperature=0.4
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
            
            integration_response = await self.openrouter.generate(
                prompt=integration_prompt,
                model="grok-4", 
                max_tokens=1500,
                temperature=0.3
            )
            
            logger.info("Integration analysis completed")
            
            # Parse sections into structured data
            bible = self._parse_sections_to_bible(sections, integration_response, station_1_output, session_id)
            
            return bible
            
        except Exception as e:
            logger.error(f"Failed to integrate bible sections: {str(e)}")
            raise

    def _parse_sections_to_bible(self, sections: Dict[str, str], integration: str, station_1_output: Dict, session_id: str) -> ProjectBible:
        """Parse unstructured sections into structured ProjectBible"""
        
        # Extract working title from integration or Station 1
        working_title = self._extract_working_title(integration, station_1_output)
        
        # Parse world setting
        key_locations = self._extract_list(sections["world"], ["location", "key location"], ["Main Location", "Secondary Location"])
        primary_location = key_locations[0] if key_locations else "Urban Setting"
        # Clean up primary location (remove colons, etc.)
        primary_location = primary_location.strip(':').strip()
        
        world_setting = WorldSetting(
            time_period=self._extract_field(sections["world"], ["time period", "when", "year"], "Contemporary"),
            primary_location=primary_location,
            setting_type=self._extract_field(sections["world"], ["setting type", "environment"], "Realistic Contemporary"),
            atmosphere=self._extract_field(sections["world"], ["atmosphere", "mood", "tone"], "Neutral atmosphere"),
            key_locations=[loc.strip(':').strip() for loc in key_locations],  # Clean up all locations
            historical_context=self._extract_field(sections["world"], ["historical", "context"], "Present day context"),
            cultural_elements=self._extract_list(sections["world"], ["cultural", "culture"], ["Modern Western culture"])
        )
        
        # Parse format specifications
        chosen_scale = self._get_chosen_scale(station_1_output)
        format_specs = FormatSpecifications(
            series_type=chosen_scale.get("option_type", "Standard Series"),
            episode_count=chosen_scale.get("episode_count", "8-12"),
            episode_length=chosen_scale.get("episode_length", "35-45 min each"),
            season_structure=self._extract_field(sections["format"], ["season", "structure", "arc"], "Single season arc"),
            pacing_strategy=self._extract_field(sections["format"], ["pacing", "pace"], "Steady build with climactic moments"),
            narrative_structure=self._extract_field(sections["format"], ["narrative", "structure"], "Three-act structure per episode")
        )
        
        # Parse genre and tone
        genre_tone = GenreTone(
            primary_genre=self._extract_field(sections["genre"], ["primary genre", "main genre"], "Drama"),
            secondary_genres=self._extract_list(sections["genre"], ["secondary", "supporting", "element"], ["Contemporary", "Character-driven"]),
            tone_descriptors=self._extract_list(sections["genre"], ["tone", "mood", "feel"], ["Emotional", "Uplifting", "Engaging"]),
            mood_profile=self._extract_field(sections["genre"], ["mood profile", "overall mood"], "Thoughtful and engaging"),
            genre_conventions=self._extract_list(sections["genre"], ["convention", "element", "typical"], ["Character development", "Story progression"])
        )
        
        # Parse creative promises
        creative_promises = CreativePromises(
            core_hooks=self._extract_list(sections.get("creative", ""), ["hook", "compelling", "draw"], ["Character development", "Compelling story"]),
            unique_elements=self._extract_list(sections.get("creative", ""), ["unique", "special", "distinctive"], ["Unique premise", "Audio-optimized storytelling"]),
            emotional_journey=self._extract_field(sections.get("creative", ""), ["emotional", "journey", "arc"], "Character growth and resolution"),
            story_pillars=self._extract_list(sections.get("creative", ""), ["pillar", "foundation", "core"], ["Strong characters", "Engaging plot"])
        )
        
        # Parse audience profile
        audience_profile = AudienceProfile(
            primary_age_range=self._extract_field(sections["audience"], ["age", "range"], "25-45"),
            target_demographics=self._extract_list(sections["audience"], ["demographic", "target"], ["Adults", "Working professionals"]),
            core_interests=self._extract_list(sections["audience"], ["interest", "hobby"], ["Entertainment", "Character development"]),
            listening_context=self._extract_field(sections["audience"], ["context", "listening", "when"], "Commuting and relaxing"),
            content_preferences=self._extract_list(sections["audience"], ["preference", "like"], ["Character-driven stories", "Engaging narratives"])
        )
        
        # Parse production constraints
        production_constraints = ProductionConstraints(
            content_rating=self._extract_content_rating(sections["production"]),
            budget_tier=self._extract_budget_tier(sections["production"]),
            technical_requirements=self._extract_list(sections["production"], ["technical", "requirement"], ["Audio production", "Post-production"]),
            content_restrictions=self._extract_list(sections["production"], ["restriction", "limit"], ["Age-appropriate content"]),
            distribution_channels=self._extract_list(sections["production"], ["distribution", "platform"], ["Podcast platforms", "Streaming services"])
        )
        
        # Parse creative team
        creative_team = CreativeTeam(
            required_roles=self._extract_list(sections["creative"], ["role", "required", "team"], ["Writer", "Director", "Producer"]),
            specialized_skills=self._extract_list(sections["creative"], ["skill", "expertise"], ["Audio production", "Script writing"]),
            team_structure=self._extract_field(sections["creative"], ["structure", "organization"], "Collaborative team approach"),
            collaboration_style=self._extract_field(sections["creative"], ["collaboration", "style"], "Open communication and feedback"),
            key_partnerships=self._extract_list(sections["creative"], ["partnership", "collaboration"], ["Production partners", "Distribution partners"])
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

    def _get_chosen_scale(self, station_1_output: Dict) -> Dict:
        """Get the chosen scale option from Station 1"""
        chosen_option = station_1_output.get("chosen_scale", station_1_output.get("recommended_option", "B"))
        
        # Define default scale options based on choice
        scale_defaults = {
            "A": {"option_type": "Mini Series", "episode_count": "3-6", "episode_length": "15-25 min each"},
            "B": {"option_type": "Standard Series", "episode_count": "8-12", "episode_length": "35-45 min each"}, 
            "C": {"option_type": "Extended Series", "episode_count": "15-20", "episode_length": "35-45 min each"}
        }
        
        return scale_defaults.get(chosen_option, scale_defaults["B"])

    def _extract_working_title(self, integration: str, station_1_output: Dict) -> str:
        """Extract working title from integration feedback or Station 1"""
        
        # First, try to get from Station 1 titles (most reliable)
        titles = station_1_output.get("initial_expansion", {}).get("working_titles", [])
        if titles and titles[0] and len(titles[0].strip()) > 3:
            return titles[0].strip()
        
        # Look for title in integration feedback only if Station 1 titles are empty
        title_patterns = [
            r"(?:working title|title)[:\s]*[\"']([^\"'\n]+)[\"']",  # Quoted titles
            r"(?:working title|title)[:\s]*([A-Z][A-Za-z\s]{3,50})",  # Unquoted proper titles
            r"(?:recommend|suggest)[^:]*title[:\s]*[\"']([^\"'\n]+)[\"']"
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, integration, re.IGNORECASE)
            if match:
                title = match.group(1).strip().strip('"\'')
                # Validate title - should be reasonable length and not contain weird characters
                if 3 < len(title) < 80 and not any(char in title for char in ['*', '(', ')', ':', '**']):
                    return title
        
        # Final fallback
        return "Digital Connection Series"

    def _extract_field(self, text: str, keywords: List[str], default: str) -> str:
        """Extract a single field value from text with robust fallbacks"""
        if not text or not text.strip():
            return default
            
        # Special handling for different content patterns
        for keyword in keywords:
            # Try exact pattern matches first
            if keyword.lower() == "time period":
                # Look for "TIME PERIOD/YEAR:" section
                section_match = re.search(r"TIME PERIOD/YEAR:\s*(.*?)(?=\n[A-Z]|$)", text, re.DOTALL | re.IGNORECASE)
                if section_match:
                    content = section_match.group(1).strip()
                    # Extract first meaningful sentence
                    sentences = re.split(r'[.!?]+', content)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if len(sentence) > 10 and len(sentence) < 200:
                            return sentence
                            
            elif keyword.lower() in ["primary location", "location"]:
                # Look for PRIMARY LOCATIONS section - handle different formats
                patterns = [
                    r"PRIMARY LOCATIONS.*?:(.*?)(?=\n[0-9]\.|TIME PERIOD|$)",
                    r"1\. PRIMARY LOCATIONS.*?:(.*?)(?=\n[0-9]\.|TIME PERIOD|$)",
                    r"(?i)primary locations.*?:(.*?)(?=\n[0-9]\.|time period|$)"
                ]
                
                for pattern in patterns:
                    section_match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                    if section_match:
                        content = section_match.group(1).strip()
                        # Try to extract first location from various formats
                        location_patterns = [
                            r"[A-E]\.\s*([^\n-]+)",  # Letter format (A. Location)
                            r"\d+\.\s*([^\n-]+)",    # Number format (1. Location)
                            r"-\s*([^\n]+)",         # Dash format (- Location)
                            r"•\s*([^\n]+)"          # Bullet format (• Location)
                        ]
                        
                        for loc_pattern in location_patterns:
                            location_match = re.search(loc_pattern, content)
                            if location_match:
                                location = location_match.group(1).strip()
                                if len(location) > 3:
                                    return location
                        
            elif keyword.lower() in ["atmosphere", "mood", "tone"]:
                # Look for ATMOSPHERE/MOOD section
                section_match = re.search(r"ATMOSPHERE/MOOD:\s*(.*?)(?=\n[A-Z]|CULTURAL|$)", text, re.DOTALL | re.IGNORECASE)
                if section_match:
                    content = section_match.group(1).strip()
                    # Extract first meaningful sentence
                    sentences = re.split(r'[.!?]+', content)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if len(sentence) > 10 and len(sentence) < 200:
                            return sentence
                            
            elif keyword.lower() in ["setting type", "environment"]:
                # Look for setting context in time period or atmosphere sections
                for section_name in ["TIME PERIOD", "ATMOSPHERE"]:
                    section_match = re.search(rf"{section_name}.*?:(.*?)(?=\n[A-Z]|$)", text, re.DOTALL | re.IGNORECASE)
                    if section_match:
                        content = section_match.group(1)
                        if "future" in content.lower():
                            return "Near-future setting"
                        elif "contemporary" in content.lower() or "present" in content.lower():
                            return "Contemporary setting"
                        elif "past" in content.lower() or "historical" in content.lower():
                            return "Historical setting"
        
        # Fallback: try basic keyword search
        for keyword in keywords:
            simple_patterns = [
                rf"{re.escape(keyword)}[:\s]*([^\n]+)",
                rf"(?i){re.escape(keyword)}.*?:\s*([^\n.]+)"
            ]
            
            for pattern in simple_patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1).strip().strip('"\'').strip('-').strip()
                    if len(result) > 5 and not result.lower().startswith(('not found', 'unknown', 'n/a')):
                        return result
                
        return default

    def _extract_list(self, text: str, keywords: List[str], default: List[str]) -> List[str]:
        """Extract a list of items from text with improved parsing"""
        if not text or not text.strip():
            return default
            
        for keyword in keywords:
            # Special handling for location lists
            if keyword.lower() in ["location", "key location"]:
                # Look for PRIMARY LOCATIONS section with numbered items
                section_match = re.search(r"PRIMARY LOCATIONS.*?:(.*?)(?=\n[A-Z]|TIME PERIOD|$)", text, re.DOTALL | re.IGNORECASE)
                if section_match:
                    content = section_match.group(1)
                    # Extract numbered locations
                    locations = re.findall(r"\d+\.\s*([^\n]+)", content)
                    if locations:
                        return [loc.strip() for loc in locations[:5]]
            
            # General list extraction patterns
            patterns = [
                rf"{re.escape(keyword)}.*?:(.*?)(?=\n[A-Z][A-Z\s]+:|\n\n|$)",  # Section until next major heading
                rf"(?i){re.escape(keyword)}[^:]*:\s*\n((?:\s*[-•\d\.][^\n]+\n?)+)",  # Bulleted list
                rf"(?i){re.escape(keyword)}[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)"  # Simple content
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    items = []
                    
                    # Try numbered list format first
                    numbered_items = re.findall(r"\d+\.\s*([^\n]+)", content)
                    if numbered_items:
                        items.extend(numbered_items)
                    
                    # Try bulleted list format
                    if not items:
                        bullet_items = re.findall(r"[-•\*]\s*([^\n]+)", content)
                        if bullet_items:
                            items.extend(bullet_items)
                    
                    # Try comma-separated format
                    if not items and ',' in content:
                        comma_items = [item.strip() for item in content.split(',')]
                        items.extend(comma_items)
                    
                    # Try line-separated format
                    if not items:
                        line_items = [line.strip() for line in content.split('\n') if line.strip()]
                        items.extend(line_items)
                    
                    # Clean and filter items
                    cleaned_items = []
                    for item in items:
                        item = item.strip().strip('"\'').strip('-').strip(':').strip()
                        if (len(item) > 3 and len(item) < 200 and 
                            not item.lower().startswith(('not found', 'unknown', 'n/a'))):
                            cleaned_items.append(item)
                    
                    if cleaned_items:
                        return cleaned_items[:5]  # Limit to 5 items
        
        return default

    def _extract_episode_count(self, episode_range: str) -> int:
        """Extract numeric episode count from range string"""
        numbers = re.findall(r'\d+', episode_range)
        if len(numbers) >= 2:
            return int(numbers[1])  # Use upper bound
        elif len(numbers) == 1:
            return int(numbers[0])
        return 10  # Default

    def _extract_content_rating(self, text: str) -> ContentRating:
        """Extract content rating from text"""
        text_lower = text.lower()
        if "pg-13" in text_lower:
            return ContentRating.PG13
        elif "pg" in text_lower and "13" not in text_lower:
            return ContentRating.PG
        elif " r " in text_lower or "r-rated" in text_lower:
            return ContentRating.R
        elif " g " in text_lower or "general" in text_lower:
            return ContentRating.G
        else:
            return ContentRating.PG
    
    def _extract_budget_tier(self, text: str) -> BudgetTier:
        """Extract budget tier from text"""
        text_lower = text.lower()
        if "premium" in text_lower or "high-end" in text_lower:
            return BudgetTier.PREMIUM
        elif "high" in text_lower:
            return BudgetTier.HIGH
        elif "low" in text_lower or "budget" in text_lower and "high" not in text_lower:
            return BudgetTier.LOW
        else:
            return BudgetTier.MEDIUM

    def _extract_cast_size(self, text: str) -> int:
        """Extract maximum cast size from text"""
        # Look for numbers near "cast" or "actor"
        patterns = [
            r"(?:cast|actor)[s]?[^0-9]*(\d+)",
            r"(\d+)[^a-z]*(?:cast|actor)",
            r"maximum[^0-9]*(\d+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                size = int(match.group(1))
                if 1 <= size <= 20:  # Reasonable range
                    return size
        
        return 6  # Default reasonable cast size

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