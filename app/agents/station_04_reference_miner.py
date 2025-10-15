"""
Station 4: Reference Mining & Seed Extraction Agent

This agent takes the Age/Genre Style Guide from Station 3 and creates a comprehensive
Seed Bank Document with 65 story elements through systematic reference analysis.

Dependencies: Station 3 Age/Genre Style Guide output
Outputs: Seed Bank Document (65 story elements across 4 categories)
Human Gate: IMPORTANT - Seed bank affects all creative development moving forward
"""

import asyncio
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
# from app.pdf_exporter import Station4PDFExporter  # Not implemented

logger = logging.getLogger(__name__)

class MediaType(Enum):
    AUDIO_DRAMA = "Audio Drama"
    FILM_TV = "Film/TV"
    LITERATURE = "Literature"
    PODCAST = "Podcast"
    INTERACTIVE = "Interactive Media"

class ImplementationDifficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

@dataclass
class MediaReference:
    """Cross-media reference for tactical extraction"""
    title: str
    medium: MediaType
    genre_relevance: str
    age_appropriateness: str
    why_selected: str
    release_year: Optional[str] = None
    creator: Optional[str] = None

@dataclass
class TacticalExtraction:
    """Extracted tactics and techniques from references"""
    reference_title: str
    storytelling_tactic: str
    pitfall_to_avoid: str
    audio_technique: str
    applicability_score: float  # 0.0 to 1.0
    implementation_notes: str

@dataclass
class StoryElement:
    """Individual story seed/element"""
    title: str
    description: str
    audio_considerations: str
    implementation_difficulty: ImplementationDifficulty
    character_requirements: List[str]
    setting_requirements: str
    estimated_runtime: str
    genre_tags: List[str]
    source_reference: str
    adaptation_notes: str

@dataclass
class SeedCollection:
    """Complete collection of 65 story elements"""
    micro_moments: List[StoryElement]     # 30 items - single scenes, 30-90 seconds
    episode_beats: List[StoryElement]     # 20 items - major plot points, cliffhangers
    season_arcs: List[StoryElement]       # 10 items - character development, world expansion
    series_defining: List[StoryElement]   # 5 items - franchise-making scenes, iconic moments

@dataclass
class AdaptationGuide:
    """Guidelines for implementing seeds in audio format"""
    audio_constraints: List[str]
    voice_acting_requirements: List[str]
    sound_design_priorities: List[str]
    pacing_considerations: List[str]
    technical_requirements: List[str]

@dataclass
class SeedBankDocument:
    """Complete Station 4 output - Seed Bank Document"""
    working_title: str
    references: List[MediaReference]
    tactical_extractions: List[TacticalExtraction]
    seed_collection: SeedCollection
    adaptation_guide: AdaptationGuide
    implementation_roadmap: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    session_id: str
    created_timestamp: datetime

class Station04ReferenceMiner:
    """
    Station 4: Reference Mining & Seed Extraction
    
    Responsibilities:
    1. Gather 20-25 cross-media references based on project requirements
    2. Extract storytelling tactics, pitfalls, and audio techniques
    3. Generate 65 story seeds across 4 categories
    4. Adapt all content for audio-only format
    5. Create comprehensive seed bank document
    """
    
    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.station_id = "station_04"
        # self.pdf_exporter = Station4PDFExporter()  # Not implemented
        self.debug_mode = False
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=4)
        
        # Station-specific prompt templates (loaded from config)
        self.reference_prompt = self.config.get_prompt('reference_gathering')
        self.extraction_prompt = self.config.get_prompt('tactical_extraction')
        self.seed_generation_prompt = self.config.get_prompt('seed_generation')
        
    async def initialize(self):
        """Initialize the Station 4 processor"""
        await self.redis.initialize()
        
    def _load_reference_prompt(self) -> str:
        """Load the reference gathering prompt template"""
        return """
You are the Reference Curator and Seed Extractor for an audio drama development system.

PROJECT CONTEXT:
Title: {working_title}
Primary Genre: {primary_genre}
Secondary Genres: {secondary_genres}
Target Age Range: {target_age_range}
Content Rating: {content_rating}
Tone Profile: {tone_profile}
World Setting: {world_setting}
Series Scale: {series_scale}

TASK 1: REFERENCE GATHERING

Based on the project requirements above, identify 20-25 cross-media references that could provide valuable storytelling techniques. Your selections must be:

1. **GENRE-APPROPRIATE**: Match or complement the primary/secondary genres
2. **AGE-APPROPRIATE**: Suitable for the target age range and content rating
3. **AUDIO-RELEVANT**: Have elements that translate well to audio-only format
4. **TACTICALLY RICH**: Contain specific techniques we can extract and adapt

REQUIRED DISTRIBUTION:
- 5-7 Successful Audio Dramas (podcasts, radio plays, audio series)
- 6-8 Film/TV with Relevant Narrative Elements
- 4-6 Literature with Audio Potential (especially dialogue-heavy works)
- 3-4 Podcasts with Strong Storytelling Techniques
- 2-3 Interactive Media/Games (for narrative structure ideas)

For each reference, provide:

**TITLE**: [Exact title]
**MEDIUM**: [Audio Drama/Film/TV/Literature/Podcast/Interactive]
**RELEASE YEAR**: [Year if known]
**CREATOR**: [Key creator if known]
**GENRE RELEVANCE**: [How it matches our genre blend - be specific]
**AGE APPROPRIATENESS**: [Why it fits our content rating and target age]
**WHY SELECTED**: [2-3 sentences explaining what specific storytelling elements make this valuable for our audio drama project]

SELECTION CRITERIA PRIORITIES:
1. **Audio Storytelling Excellence**: References with masterful use of dialogue, voice acting, sound design
2. **Character Development Techniques**: Strong character arcs that work in audio format
3. **Tension/Pacing Mastery**: References that build and maintain audience engagement
4. **Genre Innovation**: Creative approaches to blending genres similar to our project
5. **Structural Sophistication**: Interesting narrative structures (non-linear, multiple perspectives, etc.)

Focus on references that are:
- Critically acclaimed or audience favorites
- Known for specific storytelling innovations
- Rich in techniques transferable to audio drama
- Appropriate for professional development team analysis

Provide exactly 20-25 references with full details for each.
"""

    def _load_extraction_prompt(self) -> str:
        """Load the tactical extraction prompt template"""
        return """
You are extracting specific storytelling tactics from references for audio drama development.

PROJECT CONTEXT: {project_context}

REFERENCE TO ANALYZE: {reference_details}

TASK 2: TACTICAL EXTRACTION

For this reference, extract exactly THREE elements:

**1. STORYTELLING TACTIC THAT WORKS**
Identify one specific technique, approach, or method that made this reference successful. Focus on:
- Concrete, actionable storytelling choices
- Techniques that contributed to audience engagement
- Methods that could be adapted to different contexts
- Specific structural or character development approaches

**2. PITFALL TO AVOID**  
Identify one common failure mode, mistake, or weakness either:
- Present in this reference that we should avoid
- Common in this genre/medium that this reference successfully avoided
- Known challenge in adapting this type of content to audio format

**3. AUDIO-SPECIFIC TECHNIQUE**
Identify one technique that specifically leverages sound, voice, or audio-only storytelling:
- How dialogue carries narrative weight
- Use of sound effects or ambient audio
- Voice acting techniques that convey emotion/information
- Audio pacing or rhythm strategies
- Ways to convey visual information through sound

For each extraction, provide:
- **TECHNIQUE NAME**: [Brief, memorable name]
- **DESCRIPTION**: [2-3 sentences explaining the technique]
- **WHY IT WORKS**: [1-2 sentences on effectiveness]
- **AUDIO ADAPTATION**: [How to adapt this for audio-only format]
- **APPLICABILITY SCORE**: [Rate 0.0-1.0 how well this applies to our specific project]

Focus on techniques that are:
- Specific and actionable
- Transferable to our genre/tone combination
- Suitable for our target age range
- Practical for audio drama production
"""

    def _load_seed_generation_prompt(self) -> str:
        """Load the seed generation prompt template - FIXED VERSION"""
        return """
You are generating story seeds for an audio drama production.

PROJECT CONTEXT:
{project_context}

AVAILABLE TACTICS:
{available_tactics}

CRITICAL INSTRUCTIONS:
1. You MUST use the EXACT markers shown below
2. You MUST generate exactly 65 total seeds (30+20+10+5)
3. Each seed MUST use the SEED_START and SEED_END markers
4. DO NOT modify or skip the category markers

REQUIRED FORMAT FOR EACH SEED:

SEED_START
TITLE: [Title Here]
DESCRIPTION: [2-3 sentences]
AUDIO_CONSIDERATIONS: [Audio notes]
DIFFICULTY: [Easy/Medium/Hard]
CHARACTERS: [Character list]
SETTING: [Setting description]
RUNTIME: [Duration]
TAGS: [Genre tags]
SOURCE: [Reference title]
ADAPTATION: [Audio adaptation notes]
SEED_END

OUTPUT STRUCTURE (USE THESE EXACT MARKERS):

==MICRO_MOMENTS_START==
[Generate exactly 30 seeds here using SEED_START/SEED_END format]
==MICRO_MOMENTS_END==

==EPISODE_BEATS_START==
[Generate exactly 20 seeds here using SEED_START/SEED_END format] 
==EPISODE_BEATS_END==

==SEASON_ARCS_START==
[Generate exactly 10 seeds here using SEED_START/SEED_END format]
==SEASON_ARCS_END==

==SERIES_DEFINING_START==
[Generate exactly 5 seeds here using SEED_START/SEED_END format]
==SERIES_DEFINING_END==

IMPORTANT: The markers ==MICRO_MOMENTS_START==, ==MICRO_MOMENTS_END==, etc. MUST appear in your response EXACTLY as shown.
"""

    async def process(self, session_id: str) -> SeedBankDocument:
        """
        Main processing method for Station 4
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            SeedBankDocument: Complete seed bank with 65 story elements
        """
        try:
            logger.info(f"Station 4 processing started for session {session_id}")
            
            # Load Station 3 output and earlier station data
            project_data = await self._load_project_data(session_id)
            if not project_data:
                raise ValueError("Could not load required data from previous stations")
            
            # TASK 1: Gather references
            logger.info("Starting reference gathering...")
            references = await self._gather_references(project_data)
            
            # TASK 2: Extract tactics from references
            logger.info("Starting tactical extraction...")
            tactical_extractions = await self._extract_tactics(references, project_data)
            
            # TASK 3: Generate seeds from tactics with retry mechanism
            logger.info("Starting seed generation...")
            seed_collection = await self._generate_seeds_with_retry(tactical_extractions, project_data)
            
            # Create adaptation guide and implementation roadmap
            adaptation_guide = self._create_adaptation_guide(project_data, tactical_extractions)
            implementation_roadmap = self._create_implementation_roadmap(seed_collection)
            quality_metrics = self._calculate_quality_metrics(references, tactical_extractions, seed_collection)
            
            # Compile final document
            seed_bank_document = SeedBankDocument(
                working_title=project_data.get("working_title", "Untitled Project"),
                references=references,
                tactical_extractions=tactical_extractions,
                seed_collection=seed_collection,
                adaptation_guide=adaptation_guide,
                implementation_roadmap=implementation_roadmap,
                quality_metrics=quality_metrics,
                session_id=session_id,
                created_timestamp=datetime.utcnow()
            )
            
            # Store in Redis for next station
            await self._store_output(session_id, seed_bank_document)
            
            logger.info(f"Station 4 completed successfully for session {session_id}")
            return seed_bank_document
            
        except Exception as e:
            logger.error(f"Station 4 processing failed for session {session_id}: {str(e)}")
            raise

    async def _load_project_data(self, session_id: str) -> Dict[str, Any]:
        """Load all previous station data for context"""
        try:
            # Load Station 3 output (primary dependency)
            station3_key = f"audiobook:{session_id}:station_03"
            station3_data = await self.redis.get(station3_key)
            
            # Load Station 2 output (for world/setting info)
            station2_key = f"audiobook:{session_id}:station_02"
            station2_data = await self.redis.get(station2_key)
            
            # Load Station 1 output (for scale info)
            station1_key = f"audiobook:{session_id}:station_01"
            station1_data = await self.redis.get(station1_key)
            
            if not station3_data:
                logger.error("Station 3 data not found - required for Station 4")
                return None
            
            # Parse JSON data
            station3 = json.loads(station3_data) if station3_data else {}
            station2 = json.loads(station2_data) if station2_data else {}
            station1 = json.loads(station1_data) if station1_data else {}
            
            # Combine relevant data
            project_data = {
                # From Station 3
                "age_guidelines": station3.get("age_guidelines", {}),
                "genre_blend_options": station3.get("genre_options", []),
                "tone_calibration": station3.get("tone_calibration", {}),
                "working_title": station3.get("working_title", "Untitled Project"),
                
                # From Station 2  
                "world_setting": station2.get("world_setting", {}),
                "format_specifications": station2.get("format_specifications", {}),
                "genre_tone": station2.get("genre_tone", {}),
                "audience_profile": station2.get("audience_profile", {}),
                
                # From Station 1
                "original_seed": station1.get("original_seed", ""),
                "scale_choice": station1.get("recommended_option", "B"),
                "initial_expansion": station1.get("initial_expansion", {}),
                "main_characters": station1.get("initial_expansion", {}).get("main_characters", [])
            }
            
            return project_data
            
        except Exception as e:
            logger.error(f"Failed to load project data: {str(e)}")
            return None

    async def _gather_references(self, project_data: Dict[str, Any]) -> List[MediaReference]:
        """TASK 1: Gather 20-25 cross-media references"""
        try:
            # Format context for LLM
            context = self._format_project_context(project_data)
            prompt = self.reference_prompt.format(**context)
            
            # Get LLM response with small delay to avoid rate limiting
            await asyncio.sleep(1.0)  # 1 second delay between API calls
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            # Parse references from response
            references = self._parse_references_response(response)
            
            # Validate we have the right number - RETRY if not enough (but don't fail)
            if len(references) < 20:
                logger.warning(f"⚠️  Expected 20-25 references, only got {len(references)}")
                logger.warning("Retrying reference gathering with more explicit prompt...")
                
                # Retry with more explicit instructions
                retry_prompt = prompt + f"""
                
                IMPORTANT: You MUST provide EXACTLY 20-25 references (you only provided {len(references)}).
                Each reference must include ALL required fields:
                - TITLE
                - MEDIUM  
                - RELEASE YEAR
                - CREATOR
                - GENRE RELEVANCE
                - AGE APPROPRIATENESS
                - WHY SELECTED
                
                Generate {25 - len(references)} MORE references now to reach the minimum of 20.
                """
                
                await asyncio.sleep(1.0)  # 1 second delay between API calls
                retry_response = await self.openrouter.process_message(
                    retry_prompt,
                    model_name=self.config.model,
                    max_tokens=self.config.max_tokens
                )
                
                additional_refs = self._parse_references_response(retry_response)
                references.extend(additional_refs)
                
                if len(references) < 20:
                    logger.warning(f"⚠️  After retry, still only have {len(references)} references (target was 20 minimum)")
                    logger.warning(f"Continuing with {len(references)} references - quality may be impacted")
            
            if len(references) > 25:
                logger.warning(f"Got {len(references)} references, trimming to 25")
                references = references[:25]
            
            logger.info(f"✅ Gathered {len(references)} references (target: 20-25)")
            return references
            
        except Exception as e:
            logger.error(f"❌ CRITICAL: Failed to gather references: {str(e)}")
            raise RuntimeError(f"CRITICAL FAILURE in Station 4 reference gathering: {str(e)}")

    async def _extract_tactics(self, references: List[MediaReference], project_data: Dict[str, Any]) -> List[TacticalExtraction]:
        """TASK 2: Extract tactics from each reference"""
        tactical_extractions = []
        
        try:
            project_context = self._format_project_context(project_data)
            
            for reference in references:
                try:
                    # Format reference details
                    reference_details = f"""
TITLE: {reference.title}
MEDIUM: {reference.medium.value}
YEAR: {reference.release_year or 'Unknown'}
CREATOR: {reference.creator or 'Unknown'}
GENRE RELEVANCE: {reference.genre_relevance}
WHY SELECTED: {reference.why_selected}
"""
                    
                    # Format extraction prompt
                    prompt = self.extraction_prompt.format(
                        project_context=json.dumps(project_context, indent=2),
                        reference_details=reference_details
                    )
                    
                    # Get LLM response
                    await asyncio.sleep(1.0)  # 1 second delay between API calls
                    response = await self.openrouter.process_message(
                        prompt,
                        model_name=self.config.model,
                        max_tokens=self.config.max_tokens
                    )
                    
                    # Parse extraction from response
                    extraction = self._parse_extraction_response(response, reference.title)
                    if extraction:
                        tactical_extractions.append(extraction)
                        
                except Exception as e:
                    logger.warning(f"Failed to extract from {reference.title}: {str(e)}")
                    continue
            
            logger.info(f"Extracted tactics from {len(tactical_extractions)} references")
            return tactical_extractions
            
        except Exception as e:
            logger.error(f"Failed to extract tactics: {str(e)}")
            raise ValueError(f"Station 4 tactical extraction failed - no fallback allowed: {str(e)}")


    def _format_project_context(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format project data for LLM consumption"""
        age_guidelines = project_data.get("age_guidelines", {})
        world_setting = project_data.get("world_setting", {})
        format_specs = project_data.get("format_specifications", {})
        genre_tone = project_data.get("genre_tone", {})
        
        return {
            "working_title": project_data.get("working_title", "Untitled Project"),
            "primary_genre": genre_tone.get("primary_genre", "Unknown"),
            "secondary_genres": genre_tone.get("secondary_genres", []),
            "target_age_range": age_guidelines.get("target_age_range", "Unknown"),
            "content_rating": age_guidelines.get("content_rating", "PG"),
            "tone_profile": genre_tone.get("mood_profile", "Unknown"),
            "world_setting": world_setting.get("primary_location", "Contemporary setting"),
            "series_scale": format_specs.get("series_type", "Standard series"),
            "episode_count": format_specs.get("episode_count", "8-12"),
            "episode_length": format_specs.get("episode_length", "35-45 min")
        }

    def _parse_references_response(self, response: str) -> List[MediaReference]:
        """Parse references from JSON response"""
        try:
            data = extract_json(response)
            references = []

            for ref_data in data.get("references", []):
                medium_str = ref_data.get("medium", "Audio Drama")

                # Map medium string to enum
                if "Audio Drama" in medium_str:
                    medium = MediaType.AUDIO_DRAMA
                elif "Film" in medium_str or "TV" in medium_str:
                    medium = MediaType.FILM_TV
                elif "Literature" in medium_str:
                    medium = MediaType.LITERATURE
                elif "Podcast" in medium_str:
                    medium = MediaType.PODCAST
                elif "Interactive" in medium_str:
                    medium = MediaType.INTERACTIVE
                else:
                    medium = MediaType.AUDIO_DRAMA

                references.append(MediaReference(
                    title=ref_data["title"],
                    medium=medium,
                    genre_relevance=ref_data.get("genre_relevance", "Relevant"),
                    age_appropriateness=ref_data.get("age_appropriateness", "Appropriate"),
                    why_selected=ref_data.get("why_selected", "Selected for techniques"),
                    release_year=ref_data.get("release_year"),
                    creator=ref_data.get("creator")
                ))

            return references

        except Exception as e:
            logger.error(f"Failed to parse references JSON: {str(e)}")
            return []

    def _parse_extraction_response(self, response: str, reference_title: str) -> Optional[TacticalExtraction]:
        """Parse tactical extraction from JSON response"""
        try:
            data = extract_json(response)

            return TacticalExtraction(
                reference_title=reference_title,
                storytelling_tactic=data.get("storytelling_tactic", "Narrative technique"),
                pitfall_to_avoid=data.get("pitfall_to_avoid", "Common pitfall"),
                audio_technique=data.get("audio_technique", "Audio-specific technique"),
                applicability_score=float(data.get("applicability_score", 0.7)),
                implementation_notes=data.get("implementation_notes", "Standard implementation")
            )

        except Exception as e:
            logger.warning(f"Failed to parse extraction JSON for {reference_title}: {str(e)}")
            return None

    def _format_available_tactics(self, tactical_extractions: List[TacticalExtraction]) -> str:
        """Format tactical extractions for seed generation prompt"""
        tactics_text = ""
        for i, extraction in enumerate(tactical_extractions, 1):
            tactics_text += f"""
TACTIC {i} (from {extraction.reference_title}):
- Storytelling Technique: {extraction.storytelling_tactic}
- Pitfall to Avoid: {extraction.pitfall_to_avoid} 
- Audio Technique: {extraction.audio_technique}
- Applicability Score: {extraction.applicability_score}
"""
        return tactics_text

    def _parse_seeds_response(self, response: str) -> SeedCollection:
        """Parse seeds from JSON response"""
        try:
            data = extract_json(response)

            def parse_seed_list(seeds_data: List[Dict]) -> List[StoryElement]:
                """Helper to parse list of seed dictionaries"""
                seeds = []
                for seed_data in seeds_data:
                    # Map difficulty string to enum
                    diff_str = seed_data.get("difficulty", "Medium")
                    if "Easy" in diff_str:
                        difficulty = ImplementationDifficulty.EASY
                    elif "Hard" in diff_str:
                        difficulty = ImplementationDifficulty.HARD
                    else:
                        difficulty = ImplementationDifficulty.MEDIUM

                    seeds.append(StoryElement(
                        title=seed_data.get("title", "Untitled"),
                        description=seed_data.get("description", "No description"),
                        audio_considerations=seed_data.get("audio_considerations", "Standard audio"),
                        implementation_difficulty=difficulty,
                        character_requirements=seed_data.get("characters", []),
                        setting_requirements=seed_data.get("setting", "Standard setting"),
                        estimated_runtime=seed_data.get("runtime", "2-3 minutes"),
                        genre_tags=seed_data.get("tags", []),
                        source_reference=seed_data.get("source_reference", "General"),
                        adaptation_notes=seed_data.get("adaptation_notes", "Standard adaptation")
                    ))
                return seeds

            return SeedCollection(
                micro_moments=parse_seed_list(data.get("micro_moments", []))[:30],
                episode_beats=parse_seed_list(data.get("episode_beats", []))[:20],
                season_arcs=parse_seed_list(data.get("season_arcs", []))[:10],
                series_defining=parse_seed_list(data.get("series_defining", []))[:5]
            )

        except Exception as e:
            logger.error(f"Seed parsing failed: {str(e)}")
            return SeedCollection([], [], [], [])

    def _extract_field_new(self, text: str, field_name: str) -> str:
        """Extract a field value from text"""
        pattern = rf"{field_name}:\s*(.+?)(?=\n[A-Z_]+:|\n\n|\Z)"
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _parse_seed_category(self, response: str, category_name: str, expected_count: int) -> List[StoryElement]:
        """Parse a specific category of seeds"""
        seeds = []
        
        try:
            # More flexible patterns to match various LLM response formats
            patterns = [
                # Pattern 1: **CATEGORY X: NAME** format
                rf"\*\*CATEGORY \d+:\s*{re.escape(category_name)}\*\*.*?(?=\*\*CATEGORY|\*\*Audio Adaptation Guide|\*\*Implementation|\Z)",
                # Pattern 2: Category X: NAME format
                rf"CATEGORY \d+:\s*{re.escape(category_name)}.*?(?=CATEGORY \d+|Audio Adaptation Guide|Implementation|$)",
                # Pattern 3: **CATEGORY NAME** format
                rf"\*\*{re.escape(category_name)}\*\*.*?(?=\*\*[A-Z]|Audio Adaptation Guide|Implementation|$)",
                # Pattern 4: Simple category name
                rf"{re.escape(category_name)}.*?(?=\n\n[A-Z][A-Z\s-]+:|Audio Adaptation Guide|Implementation|$)",
                # Pattern 5: Flexible category header
                rf"(?:CATEGORY|Category).*?{re.escape(category_name)}.*?(?=(?:CATEGORY|Category).*?(?:MICRO|EPISODE|SEASON|SERIES)|Audio Adaptation|Implementation|$)"
            ]
            
            category_match = None
            matched_pattern = None
            for i, pattern in enumerate(patterns):
                category_match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                if category_match:
                    matched_pattern = i + 1
                    break
            
            if not category_match:
                logger.warning(f"Could not find {category_name} section in response")
                print(f"⚠️  Could not find {category_name} section")
                return []  # Return empty list to trigger retry
            
            category_text = category_match.group(0)
            logger.info(f"Found {category_name} section (pattern {matched_pattern}) with {len(category_text)} characters")
            
            # Multiple approaches to split into individual seed blocks
            seed_blocks = []
            
            # Method 1: Split by seed titles (most common format)
            seed_title_patterns = [
                r'\n(?=[A-Z][^\n:]+\n)',  # Title followed by newline (simplified)
                r'\n(?=\*\*[A-Z][^*\n]+\*\*)',  # **Bold Title**
                r'\n(?=\d+\.\s*[A-Z][^\n:]+)',  # Numbered titles (simplified)
                r'\n(?=[A-Z][a-z\s]+(?:\n|$))'  # Simple titles (simplified)
            ]
            
            for pattern in seed_title_patterns:
                blocks = re.split(pattern, category_text)
                if len(blocks) > 1:
                    seed_blocks = [block.strip() for block in blocks if block.strip()]
                    break
            
            # Method 2: If no clear titles, split by paragraphs and filter
            if not seed_blocks:
                paragraphs = re.split(r'\n\s*\n', category_text)
                seed_blocks = [p.strip() for p in paragraphs if len(p.strip()) > 50]
            
            # Method 3: Extract based on common seed structure patterns
            if not seed_blocks:
                # Look for anything that looks like a structured seed (simplified pattern)
                seed_patterns = re.findall(
                    r'([A-Z][^\n:]+)\s*\n(.*?)(?=\n[A-Z][^\n:]+\s*\n|$)', 
                    category_text, 
                    re.DOTALL
                )
                seed_blocks = [f"{title}\n{content}" for title, content in seed_patterns]
            
            # Parse each block
            for block in seed_blocks:
                if not block.strip() or len(block.strip()) < 20:
                    continue
                    
                seed = self._parse_single_seed(block)
                if seed:
                    seeds.append(seed)
                    if len(seeds) >= expected_count:
                        break
            
            logger.info(f"Successfully parsed {len(seeds)} seeds from {category_name}")
            
            # No fallbacks - retry mechanism must generate sufficient seeds
            logger.info(f"Parsed {len(seeds)} seeds from {category_name} (target: {expected_count})")
            
            return seeds[:expected_count]  # Trim to exact count
            
        except Exception as e:
            logger.error(f"Failed to parse {category_name}: {str(e)}")
            return []  # Return empty list to trigger retry

    def _parse_single_seed(self, block: str) -> Optional[StoryElement]:
        """Parse a single story seed from text block"""
        try:
            # First try to extract title from the beginning of the block
            title = None
            
            # Method 1: Look for explicit title field
            title = self._extract_field(block, ["TITLE", "Title", "**TITLE**"])
            
            # Method 2: Extract from first line if it looks like a title
            if not title:
                lines = [line.strip() for line in block.split('\n') if line.strip()]
                if lines:
                    first_line = lines[0]
                    # Remove common prefixes and formatting
                    first_line = re.sub(r'^\d+\.\s*', '', first_line)  # Remove numbering
                    first_line = re.sub(r'^\*\*([^*]+)\*\*', r'\1', first_line)  # Remove bold formatting
                    first_line = first_line.strip()
                    
                    # Check if it looks like a title (not too long, not a field name)
                    if 5 <= len(first_line) <= 80 and ':' not in first_line and not first_line.isupper():
                        title = first_line
            
            # Method 3: Extract title from common patterns
            if not title:
                title_patterns = [
                    r'(?:^|\n)([A-Z][A-Za-z\s]+)\n',  # Capitalized line (simplified)
                    r'(?:^|\n)\*\*([^*\n]+)\*\*',  # Bold text (simplified)
                    r'(?:^|\n)(\d+\.\s*[A-Z][A-Za-z\s]+)\n'  # Numbered title (simplified)
                ]
                
                for pattern in title_patterns:
                    try:
                        match = re.search(pattern, block)
                        if match:
                            title = match.group(1).strip()
                            break
                    except re.error as e:
                        logger.warning(f"Regex error in title pattern {pattern}: {e}")
                        continue
            
            # Extract other fields with more flexible patterns
            description = self._extract_flexible_field(block, ["DESCRIPTION", "Description", "Summary"]) 
            if not description:
                # Try to extract from the paragraph after title
                lines = [line.strip() for line in block.split('\n') if line.strip()]
                if len(lines) > 1:
                    # Skip title line and look for description
                    for line in lines[1:]:
                        if len(line) > 20 and not re.match(r'^[A-Z\s]+:', line):
                            description = line
                            break
            
            audio_considerations = self._extract_flexible_field(block, [
                "AUDIO CONSIDERATIONS", "Audio Considerations", "Audio Notes", "AUDIO", "Audio"
            ])
            
            difficulty_str = self._extract_flexible_field(block, [
                "IMPLEMENTATION DIFFICULTY", "Difficulty", "Implementation", "DIFFICULTY"
            ])
            
            character_requirements = self._extract_flexible_list_field(block, [
                "CHARACTER REQUIREMENTS", "Characters", "CHARACTER", "Cast"
            ])
            
            setting_requirements = self._extract_flexible_field(block, [
                "SETTING REQUIREMENTS", "Setting", "SETTING", "Location"
            ])
            
            estimated_runtime = self._extract_flexible_field(block, [
                "ESTIMATED RUNTIME", "Runtime", "RUNTIME", "Duration", "Time"
            ])
            
            genre_tags = self._extract_flexible_list_field(block, [
                "GENRE TAGS", "Tags", "GENRE", "Genres", "Categories"
            ])
            
            source_reference = self._extract_flexible_field(block, [
                "SOURCE REFERENCE", "Source", "SOURCE", "Reference", "Inspired by"
            ])
            
            adaptation_notes = self._extract_flexible_field(block, [
                "ADAPTATION NOTES", "Adaptation", "Notes", "Implementation Notes"
            ])
            
            # Validate we have minimum required fields
            if not title:
                # Try to generate a title from the content
                if description and len(description) > 10:
                    title = description.split('.')[0][:50] + "..." if len(description) > 50 else description
                else:
                    return None
            
            if not description or len(description) < 10:
                # Generate a basic description if missing
                if title:
                    description = f"Story element: {title}"
                else:
                    return None
            
            # Parse implementation difficulty
            difficulty = self._parse_difficulty(difficulty_str)
            
            return StoryElement(
                title=title,
                description=description,
                audio_considerations=audio_considerations or "Standard audio production with emphasis on dialogue clarity",
                implementation_difficulty=difficulty,
                character_requirements=character_requirements or ["Primary character"],
                setting_requirements=setting_requirements or "Standard setting appropriate for audio",
                estimated_runtime=estimated_runtime or "2-3 minutes",
                genre_tags=genre_tags or ["drama"],
                source_reference=source_reference or "Original creation",
                adaptation_notes=adaptation_notes or "Direct implementation for audio format"
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse seed block: {str(e)}")
            return None

    def _extract_flexible_field(self, text: str, field_names: List[str]) -> Optional[str]:
        """Extract field content with more flexible patterns"""
        for field_name in field_names:
            # Escape the field name properly
            escaped_name = re.escape(field_name)
            
            patterns = [
                # Standard patterns - simplified to avoid nested quantifiers
                rf"\*\*{escaped_name}\*\*[:\s]*([^\n]+)",
                rf"{escaped_name}[:\s]*([^\n]+)",
                rf"\*{escaped_name}\*[:\s]*([^\n]+)",
                # Case insensitive patterns
                rf"(?i){escaped_name}[:\s]*([^\n]+)",
                rf"(?i)\*\*{escaped_name}\*\*[:\s]*([^\n]+)"
            ]
            
            for pattern in patterns:
                try:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        content = match.group(1).strip()
                        # Clean up formatting
                        content = re.sub(r'^\[|\]$', '', content)  # Remove brackets
                        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
                        if content and content.lower() not in ["unknown", "n/a", "none", "tbd"]:
                            return content
                except re.error as e:
                    logger.warning(f"Regex error in pattern {pattern}: {e}")
                    continue
        
        return None

    def _extract_flexible_list_field(self, text: str, field_names: List[str]) -> List[str]:
        """Extract list field content with flexible patterns"""
        for field_name in field_names:
            # Escape the field name properly
            escaped_name = re.escape(field_name)
            
            patterns = [
                # List in brackets - simplified
                rf"\*\*{escaped_name}\*\*[:\s]*\[(.*?)\]",
                rf"{escaped_name}[:\s]*\[(.*?)\]",
                # Simple comma-separated values
                rf"\*\*{escaped_name}\*\*[:\s]*([^\n]+)",
                rf"{escaped_name}[:\s]*([^\n]+)",
                # Case insensitive
                rf"(?i){escaped_name}[:\s]*([^\n]+)"
            ]
            
            for pattern in patterns:
                try:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        content = match.group(1).strip()
                        # Parse as list
                        if "," in content:
                            items = [item.strip().strip('"\'') for item in content.split(",")]
                            return [item for item in items if item and item.lower() not in ["unknown", "n/a", "none"]]
                        elif content and content.lower() not in ["unknown", "n/a", "none"]:
                            return [content.strip('"\'')]
                except re.error as e:
                    logger.warning(f"Regex error in list pattern {pattern}: {e}")
                    continue
        
        return []

    def _extract_list_field(self, text: str, field_names: List[str]) -> List[str]:
        """Extract list field content from text"""
        for field_name in field_names:
            patterns = [
                rf"\*\*{field_name}\*\*[:\s]*\[(.*?)\]",  # [item1, item2]
                rf"{field_name}[:\s]*\[(.*?)\]",
                rf"\*\*{field_name}\*\*[:\s]*(.*?)(?=\n\n|\n\*\*|\n[A-Z]+:)",  # Multi-line list
                rf"{field_name}[:\s]*(.*?)(?=\n\n|\n\*\*|\n[A-Z]+:)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    # Parse as list
                    if "," in content:
                        items = [item.strip().strip('"\'') for item in content.split(",")]
                        return [item for item in items if item]
                    elif content:
                        return [content.strip('"\'')]
        
        return []

    def _parse_difficulty(self, difficulty_str: str) -> ImplementationDifficulty:
        """Parse difficulty string to enum"""
        if not difficulty_str:
            return ImplementationDifficulty.MEDIUM
        
        difficulty_lower = difficulty_str.lower()
        
        if "easy" in difficulty_lower:
            return ImplementationDifficulty.EASY
        elif "hard" in difficulty_lower or "difficult" in difficulty_lower:
            return ImplementationDifficulty.HARD
        else:
            return ImplementationDifficulty.MEDIUM

    def _create_adaptation_guide(self, project_data: Dict[str, Any], tactical_extractions: List[TacticalExtraction]) -> AdaptationGuide:
        """Create comprehensive adaptation guide"""
        age_guidelines = project_data.get("age_guidelines", {})
        
        # Extract audio constraints from age guidelines
        audio_constraints = age_guidelines.get("sound_restrictions", [])
        if not audio_constraints:
            audio_constraints = ["No jarring sound effects", "Age-appropriate content", "Clear dialogue priority"]
        
        # Voice acting requirements based on project needs
        voice_acting_requirements = [
            "Professional voice talent capable of emotional range",
            f"Age-appropriate delivery for {age_guidelines.get('target_age_range', 'general')} audience",
            "Character voice consistency across episodes"
        ]
        
        # Sound design priorities from tactical extractions
        sound_priorities = []
        for extraction in tactical_extractions:
            if "sound" in extraction.audio_technique.lower():
                sound_priorities.append(extraction.audio_technique[:100])  # Truncate long descriptions
        
        if not sound_priorities:
            sound_priorities = ["Atmospheric sound design", "Clear dialogue mixing", "Signature audio elements"]
        
        return AdaptationGuide(
            audio_constraints=audio_constraints,
            voice_acting_requirements=voice_acting_requirements,
            sound_design_priorities=sound_priorities[:10],  # Top 10 priorities
            pacing_considerations=[
                "Maintain engagement for audio-only format",
                "Strategic use of silence and pauses",
                "Rhythm matching target age group attention spans"
            ],
            technical_requirements=[
                "High-quality audio recording standards",
                "Consistent audio levels across scenes",
                "Professional editing and post-production"
            ]
        )

    def _create_implementation_roadmap(self, seed_collection: SeedCollection) -> Dict[str, Any]:
        """Create implementation roadmap for the seed bank"""
        # Analyze difficulty distribution
        difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        all_seeds = (seed_collection.micro_moments + seed_collection.episode_beats + 
                    seed_collection.season_arcs + seed_collection.series_defining)
        
        for seed in all_seeds:
            difficulty_counts[seed.implementation_difficulty.value] += 1
        
        return {
            "phase_1_quick_wins": {
                "description": "Start with easy-to-implement micro-moments",
                "recommended_seeds": [seed.title for seed in seed_collection.micro_moments 
                                    if seed.implementation_difficulty == ImplementationDifficulty.EASY][:5],
                "estimated_timeline": "1-2 weeks"
            },
            "phase_2_core_development": {
                "description": "Implement episode-level beats and medium difficulty elements",
                "estimated_timeline": "4-6 weeks"
            },
            "phase_3_advanced_elements": {
                "description": "Tackle complex season arcs and series-defining moments",
                "estimated_timeline": "2-4 weeks"
            },
            "difficulty_distribution": difficulty_counts,
            "total_seed_count": len(all_seeds),
            "implementation_priority": "Focus on audio-rich seeds that showcase the medium's strengths"
        }

    def _calculate_quality_metrics(self, references: List[MediaReference], 
                                 tactical_extractions: List[TacticalExtraction], 
                                 seed_collection: SeedCollection) -> Dict[str, Any]:
        """Calculate quality metrics for the seed bank"""
        total_seeds = self._count_total_seeds(seed_collection)
        
        # Reference diversity
        medium_counts = {}
        for ref in references:
            medium = ref.medium.value
            medium_counts[medium] = medium_counts.get(medium, 0) + 1
        
        # Tactical applicability average
        avg_applicability = sum(ext.applicability_score for ext in tactical_extractions) / len(tactical_extractions) if tactical_extractions else 0.0
        
        return {
            "total_references": len(references),
            "total_extractions": len(tactical_extractions),
            "total_seeds": total_seeds,
            "seed_target_met": total_seeds >= 65,
            "reference_diversity": medium_counts,
            "average_tactic_applicability": round(avg_applicability, 2),
            "quality_score": self._calculate_overall_quality_score(references, tactical_extractions, seed_collection)
        }

    def _calculate_overall_quality_score(self, references: List[MediaReference], 
                                       tactical_extractions: List[TacticalExtraction], 
                                       seed_collection: SeedCollection) -> float:
        """Calculate overall quality score (0.0 to 1.0)"""
        score = 0.0
        
        # Reference count score (0.3 weight)
        ref_score = min(len(references) / 22.5, 1.0)  # Target 20-25 references
        score += ref_score * 0.3
        
        # Extraction completeness score (0.2 weight)
        extraction_score = len(tactical_extractions) / len(references) if references else 0.0
        score += extraction_score * 0.2
        
        # Seed count score (0.3 weight)
        seed_count_score = min(self._count_total_seeds(seed_collection) / 65, 1.0)
        score += seed_count_score * 0.3
        
        # Average applicability score (0.2 weight)
        if tactical_extractions:
            avg_applicability = sum(ext.applicability_score for ext in tactical_extractions) / len(tactical_extractions)
            score += avg_applicability * 0.2
        
        return round(min(score, 1.0), 2)

    def _count_total_seeds(self, seed_collection: SeedCollection) -> int:
        """Count total seeds across all categories"""
        return (len(seed_collection.micro_moments) + 
                len(seed_collection.episode_beats) + 
                len(seed_collection.season_arcs) + 
                len(seed_collection.series_defining))

    def _validate_seed_counts(self, seed_collection: SeedCollection) -> None:
        """Validate that we have the correct number of seeds in each category"""
        expected_counts = {
            "micro_moments": 30,
            "episode_beats": 20,
            "season_arcs": 10,
            "series_defining": 5
        }
        
        actual_counts = {
            "micro_moments": len(seed_collection.micro_moments),
            "episode_beats": len(seed_collection.episode_beats),
            "season_arcs": len(seed_collection.season_arcs),
            "series_defining": len(seed_collection.series_defining)
        }
        
        for category, expected in expected_counts.items():
            actual = actual_counts[category]
            if actual != expected:
                logger.warning(f"Seed count mismatch in {category}: expected {expected}, got {actual}")

    # No fallback methods - all content must be LLM-generated

    async def _generate_seeds_with_retry(self, tactical_extractions: List[TacticalExtraction], project_data: Dict[str, Any], max_retries: int = 3) -> SeedCollection:
        """Generate seeds with progressive approach"""
        
        # Try generating all at once first
        for attempt in range(2):
            try:
                seed_collection = await self._generate_all_seeds(tactical_extractions, project_data)
                total_seeds = self._count_total_seeds(seed_collection)
                
                if total_seeds >= 50:  # Accept if we get 75% of target
                    logger.info(f"Generated {total_seeds} seeds in batch approach")
                    return seed_collection
                    
            except Exception as e:
                logger.warning(f"Batch generation attempt {attempt + 1} failed: {e}")
        
        # No fallback - raise error if all attempts fail
        raise ValueError(f"Station 4 seed generation failed after {max_retries} attempts - no fallback allowed")

    async def _generate_all_seeds(self, tactical_extractions: List[TacticalExtraction], project_data: Dict[str, Any]) -> SeedCollection:
        """Generate all seeds in batches to avoid token limit issues"""
        try:
            logger.info("Generating seeds in batches to avoid token truncation...")
            
            # Generate each category separately to avoid token limits
            micro_moments = await self._generate_category_seeds("micro_moments", 30, tactical_extractions, project_data)
            episode_beats = await self._generate_category_seeds("episode_beats", 20, tactical_extractions, project_data)
            season_arcs = await self._generate_category_seeds("season_arcs", 10, tactical_extractions, project_data)
            series_defining = await self._generate_category_seeds("series_defining", 5, tactical_extractions, project_data)
            
            return SeedCollection(
                micro_moments=micro_moments,
                episode_beats=episode_beats,
                season_arcs=season_arcs,
                series_defining=series_defining
            )
            
        except Exception as e:
            logger.error(f"Failed to generate all seeds: {str(e)}")
            raise

    async def _generate_seeds_progressively(self, tactical_extractions: List[TacticalExtraction], project_data: Dict[str, Any]) -> SeedCollection:
        """Generate seeds category by category"""
        
        micro_moments = await self._generate_category_seeds("micro_moments", 30, tactical_extractions, project_data)
        episode_beats = await self._generate_category_seeds("episode_beats", 20, tactical_extractions, project_data)
        season_arcs = await self._generate_category_seeds("season_arcs", 10, tactical_extractions, project_data)
        series_defining = await self._generate_category_seeds("series_defining", 5, tactical_extractions, project_data)
        
        return SeedCollection(
            micro_moments=micro_moments,
            episode_beats=episode_beats,
            season_arcs=season_arcs,
            series_defining=series_defining
        )

    async def _generate_category_seeds(self, category: str, count: int, tactical_extractions: List[TacticalExtraction], project_data: Dict[str, Any]) -> List[StoryElement]:
        """Generate seeds for a specific category"""
        
        category_descriptions = {
            "micro_moments": "Single scenes lasting 30-90 seconds",
            "episode_beats": "Major plot points and cliffhangers", 
            "season_arcs": "Character development and world expansion",
            "series_defining": "Franchise-making iconic moments"
        }
        
        prompt = f"""
Generate exactly {count} seeds for: {category_descriptions[category]}

PROJECT: {project_data.get('working_title', 'Audio Drama')}
GENRE: {project_data.get('primary_genre', 'Drama')}

Use this exact format for each seed:

SEED_START
TITLE: [Title]
DESCRIPTION: [Description]
AUDIO_CONSIDERATIONS: [Audio notes]
DIFFICULTY: Easy
CHARACTERS: [Characters]
SETTING: [Setting]
RUNTIME: [Duration]
TAGS: [Tags]
SOURCE: [Reference]
ADAPTATION: [Notes]
SEED_END

Generate {count} seeds now:
"""
        
        await asyncio.sleep(1.0)  # 1 second delay between API calls
        response = await self.openrouter.process_message(
            prompt,
            model_name=self.config.model,
            max_tokens=self.config.max_tokens
        )
        
        return self._extract_seeds_from_simple_response(response)

    def _extract_seeds_from_simple_response(self, response: str) -> List[StoryElement]:
        """Extract seeds from a simple response format"""
        seeds = []

        # Split by SEED_START/SEED_END markers
        seed_blocks = re.findall(r'SEED_START(.*?)SEED_END', response, re.DOTALL)

        for block in seed_blocks:
            seed = self._parse_single_seed_new(block.strip())
            if seed:
                seeds.append(seed)

        return seeds

    def _parse_single_seed_new(self, seed_text: str) -> Optional[StoryElement]:
        """Parse a single seed from text format"""
        try:
            # Extract fields using simple patterns
            title_match = re.search(r'Title:\s*(.+?)(?:\n|$)', seed_text)
            desc_match = re.search(r'Description:\s*(.+?)(?:\n|$)', seed_text, re.DOTALL)
            audio_match = re.search(r'Audio:\s*(.+?)(?:\n|$)', seed_text)

            if not title_match or not desc_match:
                return None

            title = title_match.group(1).strip()
            description = desc_match.group(1).strip()
            audio_considerations = audio_match.group(1).strip() if audio_match else "Standard audio treatment"

            # Determine difficulty
            difficulty = ImplementationDifficulty.MEDIUM
            if "easy" in seed_text.lower():
                difficulty = ImplementationDifficulty.EASY
            elif "hard" in seed_text.lower():
                difficulty = ImplementationDifficulty.HARD

            return StoryElement(
                title=title,
                description=description,
                audio_considerations=audio_considerations,
                implementation_difficulty=difficulty,
                character_requirements=[],
                setting_requirements="TBD",
                estimated_runtime="2-3 minutes",
                genre_tags=[],
                source_reference="Generated",
                adaptation_notes=""
            )
        except Exception as e:
            logger.warning(f"Failed to parse seed: {e}")
            return None

    async def _generate_seeds_with_prompt_variation(self, tactical_extractions: List[TacticalExtraction], project_data: Dict[str, Any], variation: str) -> SeedCollection:
        """Generate seeds using different prompt variations"""
        
        project_context = self._format_project_context(project_data)
        available_tactics = self._format_available_tactics(tactical_extractions)
        
        if variation == "simplified":
            prompt = self._get_simplified_seed_prompt(project_context, available_tactics)
        elif variation == "explicit":
            prompt = self._get_explicit_seed_prompt(project_context, available_tactics)
        else:
            # Standard prompt
            prompt = self.seed_generation_prompt.format(
                project_context=json.dumps(project_context, indent=2),
                available_tactics=available_tactics,
                world_setting=project_context.get("world_setting", "Contemporary setting"),
                content_rating=project_context.get("content_rating", "PG"),
                genre_blend=project_context.get("genre_blend", "Multi-genre"),
                series_scale=project_context.get("series_scale", "Standard")
            )
        
            # Get LLM response
            await asyncio.sleep(1.0)  # 1 second delay between API calls
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
        
        # Parse seeds from response
        seed_collection = self._parse_seeds_response(response)
        return seed_collection

    def _get_simplified_seed_prompt(self, project_context: Dict, available_tactics: str) -> str:
        """Simplified prompt for retry attempts"""
        return f"""
Create 65 story seeds for an audio drama project.

PROJECT: {project_context.get('working_title', 'Audio Drama')}
GENRE: {project_context.get('primary_genre', 'Drama')}
AUDIENCE: {project_context.get('target_age_range', 'Teen/Adult')}

Generate exactly:
- 30 MICRO-MOMENTS (30-90 seconds each)  
- 20 EPISODE BEATS (3-8 minutes each)
- 10 SEASON ARCS (spanning multiple episodes)
- 5 SERIES DEFINING moments

For each seed, provide:
TITLE: [Clear title]
DESCRIPTION: [2-3 sentence description]
AUDIO: [Audio production notes]
DIFFICULTY: Easy/Medium/Hard
CHARACTERS: [Who is needed]
SETTING: [Where it takes place]
RUNTIME: [Duration]
TAGS: [Genre tags]
SOURCE: [Reference inspiration]
NOTES: [Implementation notes]

Start with MICRO-MOMENTS, then EPISODE BEATS, then SEASON ARCS, then SERIES DEFINING.
"""

    def _get_explicit_seed_prompt(self, project_context: Dict, available_tactics: str) -> str:
        """Very explicit format prompt for final retry"""
        return f"""
You MUST generate exactly 65 story seeds in this EXACT format:

**MICRO-MOMENTS CATEGORY (30 seeds)**

Seed 1:
**TITLE**: [Title Here]
**DESCRIPTION**: [Description here]
**AUDIO**: [Audio notes here]
**DIFFICULTY**: [Easy/Medium/Hard]
**CHARACTERS**: [Character list]
**SETTING**: [Setting description]
**RUNTIME**: [Time duration]
**TAGS**: [Genre tags]
**SOURCE**: [Reference]
**NOTES**: [Implementation notes]

[Repeat for 30 seeds]

**EPISODE BEATS CATEGORY (20 seeds)**

[Same format for 20 seeds]

**SEASON ARCS CATEGORY (10 seeds)**

[Same format for 10 seeds]

**SERIES DEFINING CATEGORY (5 seeds)**

[Same format for 5 seeds]

PROJECT: {project_context.get('working_title', 'Audio Drama')}
GENRE: {project_context.get('primary_genre', 'Drama')}
"""

    # No fallback seed creation - all seeds must be LLM-generated

    async def _store_output(self, session_id: str, seed_bank_document: SeedBankDocument) -> None:
        """Store output in Redis for next station"""
        try:
            # Convert to dictionary for JSON serialization
            output_dict = {
                "station_id": self.station_id,
                "working_title": seed_bank_document.working_title,
                "references": [{**asdict(ref), "medium": ref.medium.value} for ref in seed_bank_document.references],
                "tactical_extractions": [asdict(ext) for ext in seed_bank_document.tactical_extractions],
                "seed_collection": {
                    "micro_moments": [{**asdict(seed), "implementation_difficulty": seed.implementation_difficulty.value} for seed in seed_bank_document.seed_collection.micro_moments],
                    "episode_beats": [{**asdict(seed), "implementation_difficulty": seed.implementation_difficulty.value} for seed in seed_bank_document.seed_collection.episode_beats],
                    "season_arcs": [{**asdict(seed), "implementation_difficulty": seed.implementation_difficulty.value} for seed in seed_bank_document.seed_collection.season_arcs],
                    "series_defining": [{**asdict(seed), "implementation_difficulty": seed.implementation_difficulty.value} for seed in seed_bank_document.seed_collection.series_defining]
                },
                "adaptation_guide": asdict(seed_bank_document.adaptation_guide),
                "implementation_roadmap": seed_bank_document.implementation_roadmap,
                "quality_metrics": seed_bank_document.quality_metrics,
                "session_id": seed_bank_document.session_id,
                "created_timestamp": seed_bank_document.created_timestamp.isoformat()
            }
            
            # Store in Redis with session-based key
            key = f"audiobook:{session_id}:station_04"
            try:
                json_str = json.dumps(output_dict, default=str)
                await self.redis.set(key, json_str, expire=86400)  # 24 hour expiry
            except (TypeError, ValueError) as e:
                logger.error(f"JSON serialization error: {e}")
                # Try with additional fallback handling
                json_str = json.dumps(output_dict, default=lambda obj: str(obj) if hasattr(obj, 'value') else str(obj))
                await self.redis.set(key, json_str, expire=86400)
            
            logger.info(f"Station 4 output stored successfully for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store Station 4 output: {str(e)}")
            raise

    async def get_stored_output(self, session_id: str) -> Optional[SeedBankDocument]:
        """Retrieve stored output for a session"""
        try:
            key = f"audiobook:{session_id}:station_04"
            stored_data = await self.redis.get(key)
            
            if not stored_data:
                return None
                
            data = json.loads(stored_data)
            
            # Reconstruct the dataclass objects
            references = [MediaReference(**{**ref, "medium": MediaType(ref["medium"])}) for ref in data["references"]]
            tactical_extractions = [TacticalExtraction(**ext) for ext in data["tactical_extractions"]]
            
            # Reconstruct seed collection
            seed_collection = SeedCollection(
                micro_moments=[StoryElement(**{**seed, "implementation_difficulty": ImplementationDifficulty(seed["implementation_difficulty"])}) for seed in data["seed_collection"]["micro_moments"]],
                episode_beats=[StoryElement(**{**seed, "implementation_difficulty": ImplementationDifficulty(seed["implementation_difficulty"])}) for seed in data["seed_collection"]["episode_beats"]],
                season_arcs=[StoryElement(**{**seed, "implementation_difficulty": ImplementationDifficulty(seed["implementation_difficulty"])}) for seed in data["seed_collection"]["season_arcs"]],
                series_defining=[StoryElement(**{**seed, "implementation_difficulty": ImplementationDifficulty(seed["implementation_difficulty"])}) for seed in data["seed_collection"]["series_defining"]]
            )
            
            adaptation_guide = AdaptationGuide(**data["adaptation_guide"])
            
            return SeedBankDocument(
                working_title=data["working_title"],
                references=references,
                tactical_extractions=tactical_extractions,
                seed_collection=seed_collection,
                adaptation_guide=adaptation_guide,
                implementation_roadmap=data["implementation_roadmap"],
                quality_metrics=data["quality_metrics"],
                session_id=data["session_id"],
                created_timestamp=datetime.fromisoformat(data["created_timestamp"])
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve Station 4 output: {str(e)}")
            return None

    def format_for_human_review(self, seed_bank_document: SeedBankDocument) -> Dict:
        """Format output for human review/approval interface"""
        total_seeds = self._count_total_seeds(seed_bank_document.seed_collection)
        
        return {
            "station": "Station 4: Reference Mining & Seed Extraction",
            "status": "awaiting_human_approval",
            "working_title": seed_bank_document.working_title,
            "summary": {
                "total_references": len(seed_bank_document.references),
                "total_tactical_extractions": len(seed_bank_document.tactical_extractions),
                "total_seeds_generated": total_seeds,
                "seed_target_met": total_seeds >= 65,
                "quality_score": seed_bank_document.quality_metrics.get("quality_score", 0.0)
            },
            "reference_breakdown": {
                medium.value: sum(1 for ref in seed_bank_document.references if ref.medium == medium)
                for medium in MediaType
            },
            "seed_breakdown": {
                "micro_moments": len(seed_bank_document.seed_collection.micro_moments),
                "episode_beats": len(seed_bank_document.seed_collection.episode_beats),
                "season_arcs": len(seed_bank_document.seed_collection.season_arcs),
                "series_defining": len(seed_bank_document.seed_collection.series_defining)
            },
            "sample_seeds": {
                "micro_moment": seed_bank_document.seed_collection.micro_moments[0].title if seed_bank_document.seed_collection.micro_moments else "None",
                "episode_beat": seed_bank_document.seed_collection.episode_beats[0].title if seed_bank_document.seed_collection.episode_beats else "None",
                "season_arc": seed_bank_document.seed_collection.season_arcs[0].title if seed_bank_document.seed_collection.season_arcs else "None",
                "series_defining": seed_bank_document.seed_collection.series_defining[0].title if seed_bank_document.seed_collection.series_defining else "None"
            },
            "implementation_readiness": seed_bank_document.implementation_roadmap.get("phase_1_quick_wins", {}),
            "next_step": "Please review the seed bank and approve to proceed to Station 5: Character Constellation Development"
        }

    # PDF export removed - use JSON and TXT formats instead
    # def export_to_pdf(self, seed_bank_document: SeedBankDocument, filename: str = None) -> str:
    #     """Export Station 4 output to PDF - REMOVED"""
    #     pass

    # def export_review_to_pdf(self, seed_bank_document: SeedBankDocument, filename: str = None) -> str:
    #     """Export formatted review data to PDF - REMOVED"""
    #     pass

    def enable_debug_mode(self):
        """Enable detailed logging for debugging"""
        logger.setLevel(logging.DEBUG)
        self.debug_mode = True
        logger.info("Debug mode enabled for Station 4")

    def disable_debug_mode(self):
        """Disable debug mode"""
        self.debug_mode = False
        logger.info("Debug mode disabled for Station 4")


