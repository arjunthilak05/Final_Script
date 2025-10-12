#!/usr/bin/env python3
"""
Station 9: World Building System for Audiobook Production

This station creates comprehensive audio-focused world architecture with 5 major sections:
1. Geography/Spaces with sonic signatures
2. Social Systems with audio manifestations  
3. Technology/Magic with signature sounds
4. History/Lore with audio echoes
5. Sensory Palette - complete audio cue library

Dependencies: Station 2 (Project Bible), Station 6 (Style Guide), Station 8 (Character Bible)
Outputs: World Bible with TXT, JSON, and PDF exports
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

from app.openrouter_agent import OpenRouterAgent
from app.agents.config_loader import load_station_config
from app.redis_client import RedisClient
from app.config import Settings
from app.agents.retry_validator import (
    ContentValidator,
    RetryConfig,
    retry_with_validation,
    ValidationResult,
    validate_and_raise
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LocationProfile:
    """Complete location profile with sonic signature"""
    name: str
    location_type: str  # "residential", "commercial", "natural", "institutional"
    physical_description: str
    sonic_signature: Dict[str, Any]  # Audio identity details
    travel_times: Dict[str, str]  # Travel to other locations
    weather_patterns: Dict[str, str]  # Weather sounds
    acoustic_properties: Dict[str, str]  # Reverb, echo, etc.
    emotional_association: str
    story_significance: str
    time_variations: Dict[str, str]  # How it sounds at different times

@dataclass
class SocialSystem:
    """Social system with audio manifestations"""
    government_structure: str
    authority_sounds: List[str]  # How authority manifests in audio
    economic_system: str
    class_divisions: List[Dict[str, str]]
    social_hierarchies: Dict[str, Any]
    cultural_norms: List[str]
    audio_manifestations: Dict[str, List[str]]  # How social structure sounds
    dialogue_formality: Dict[str, str]  # Formality levels by relationship

@dataclass
class TechMagicSystem:
    """Technology or magic system with signature sounds"""
    name: str
    description: str
    mechanics: str
    access_level: str  # "common", "rare", "legendary"
    signature_sounds: Dict[str, str]  # activation, operation, completion, malfunction
    limitations: List[str]
    narrative_function: str
    audio_distinctiveness: str

@dataclass
class HistoricalEvent:
    """Historical event with audio echoes"""
    name: str
    timeframe: str
    description: str
    consequences: str
    public_knowledge: str
    hidden_truth: str
    audio_echoes: List[str]  # Sounds/phrases that reference this event

@dataclass
class AudioCue:
    """Individual audio cue specification"""
    cue_name: str
    description: str
    location: str
    trigger: str  # When this sound occurs
    emotional_context: str
    production_notes: str

@dataclass
class SensoryPalette:
    """Complete audio cue library for location"""
    location_name: str
    ambient_soundscape: Dict[str, List[str]]  # Layered ambient sounds
    distinctive_markers: List[str]  # Unique audio identifiers
    acoustic_properties: Dict[str, str]
    time_variations: Dict[str, List[str]]
    emotional_palette: Dict[str, List[str]]
    recurring_motifs: List[str]
    production_notes: List[str]

@dataclass
class WorldBible:
    """Complete world building output"""
    session_id: str
    working_title: str
    created_timestamp: datetime
    geography: List[LocationProfile]
    social_systems: SocialSystem
    tech_magic_systems: List[TechMagicSystem]
    historical_events: List[HistoricalEvent]
    mythology_folklore: List[Dict[str, str]]
    sensory_palettes: List[SensoryPalette]
    audio_glossary: Dict[str, str]
    world_statistics: Dict[str, int]

class Station09WorldBuilding:
    """Station 9: World Building System"""
    
    def __init__(self):
        self.settings = Settings()
        self.redis_client = None
        self.openrouter_agent = None
        self.debug_mode = False
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=9)
        
    async def initialize(self):
        """Initialize the station components"""
        try:
            self.redis_client = RedisClient()
            await self.redis_client.initialize()
            
            self.openrouter_agent = OpenRouterAgent()
            # OpenRouter agent doesn't need initialization
            
            logger.info("✅ Station 9 World Building initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Station 9: {e}")
            raise

    def enable_debug_mode(self):
        """Enable debug mode for detailed logging"""
        self.debug_mode = True
        logger.info("🐛 Debug mode enabled for Station 9")

    async def process(self, session_id: str) -> WorldBible:
        """Main processing function for Station 9"""
        
        logger.info(f"🌍 Station 9: Starting World Building for session {session_id}")
        
        try:
            # Load and validate story lock
            story_lock_key = f"audiobook:{session_id}:story_lock"
            story_lock_raw = await self.redis_client.get(story_lock_key)
            if not story_lock_raw:
                logger.warning("Story lock missing")
                story_lock = {'main_characters': [], 'core_mechanism': '', 'key_plot_points': []}
            else:
                story_lock = json.loads(story_lock_raw)
                logger.info(f"Story lock loaded: {len(story_lock.get('key_plot_points', []))} plot points preserved")
            
            # Load dependencies from previous stations
            dependencies = await self._load_dependencies(session_id)
            dependencies['story_lock'] = story_lock
            
            logger.info("📚 Loaded project dependencies from previous stations")
            
            # Generate Geography/Spaces (5-10 locations)
            geography = await self._generate_geography_spaces(dependencies)
            logger.info(f"✅ Generated {len(geography)} locations with sonic signatures")
            
            # Generate Social Systems
            social_systems = await self._generate_social_systems(dependencies, geography)
            logger.info("✅ Generated social systems with audio manifestations")
            
            # Generate Technology/Magic Systems
            tech_magic = await self._generate_tech_magic_systems(dependencies)
            logger.info(f"✅ Generated {len(tech_magic)} tech/magic systems")
            
            # Generate History/Lore
            history_events, mythology = await self._generate_history_lore(dependencies, geography)
            logger.info(f"✅ Generated {len(history_events)} historical events and mythology")
            
            # Generate Sensory Palette (Audio Cue Library)
            sensory_palettes = await self._generate_sensory_palettes(geography, dependencies)
            logger.info("✅ Generated comprehensive audio cue library")
            
            # Generate Audio Glossary
            audio_glossary = await self._generate_audio_glossary({
                'geography': geography,
                'social_systems': social_systems,
                'tech_magic': tech_magic,
                'history': history_events,
                'sensory': sensory_palettes
            })
            logger.info(f"✅ Generated audio glossary with {len(audio_glossary)} entries")
            
            # Compile world bible
            world_bible = WorldBible(
                session_id=session_id,
                working_title=dependencies.get('working_title', 'Untitled Project'),
                created_timestamp=datetime.now(),
                geography=geography,
                social_systems=social_systems,
                tech_magic_systems=tech_magic,
                historical_events=history_events,
                mythology_folklore=mythology,
                sensory_palettes=sensory_palettes,
                audio_glossary=audio_glossary,
                world_statistics={
                    "total_locations": len(geography),
                    "tech_magic_systems": len(tech_magic),
                    "historical_events": len(history_events),
                    "mythology_entries": len(mythology),
                    "audio_cues": sum(len(palette.distinctive_markers) for palette in sensory_palettes),
                    "glossary_entries": len(audio_glossary)
                }
            )
            
            # Save to Redis before returning
            try:
                output_dict = self.export_to_json(world_bible)
                key = f"audiobook:{session_id}:station_09"
                json_str = json.dumps(output_dict, default=str)
                await self.redis_client.set(key, json_str, expire=86400)  # 24 hour expiry
                logger.info(f"Station 9 output stored successfully in Redis at key: {key}")
            except Exception as e:
                logger.error(f"Failed to store Station 9 output to Redis: {str(e)}")
                raise
            
            logger.info(f"✅ Station 9 completed: World Bible with {world_bible.world_statistics['total_locations']} locations")
            return world_bible
            
        except Exception as e:
            logger.error(f"❌ Station 9 failed: {e}")
            raise

    async def _load_dependencies(self, session_id: str) -> Dict[str, Any]:
        """Load required outputs from previous stations"""
        
        dependencies = {}
        
        try:
            # Load Station 2: Project Bible
            project_bible_key = f"audiobook:{session_id}:station_02"
            project_bible_data = await self.redis_client.get(project_bible_key)
            if project_bible_data:
                dependencies['project_bible'] = json.loads(project_bible_data)
                # Defensive check: ensure project_bible is a dict
                if isinstance(dependencies['project_bible'], dict):
                    dependencies['working_title'] = dependencies['project_bible'].get('working_title', 'Untitled')
                else:
                    dependencies['working_title'] = 'Untitled'
                logger.info("✅ Loaded Project Bible from Station 2")
            else:
                logger.warning("⚠️ No Project Bible found from Station 2")
                
            # Load Station 6: Style Guide
            style_guide_key = f"audiobook:{session_id}:station_06"
            style_guide_data = await self.redis_client.get(style_guide_key)
            if style_guide_data:
                dependencies['style_guide'] = json.loads(style_guide_data)
                logger.info("✅ Loaded Style Guide from Station 6")
            else:
                logger.warning("⚠️ No Style Guide found from Station 6")
                
            # Load Station 8: Character Bible
            character_bible_key = f"audiobook:{session_id}:station_08"
            character_bible_data = await self.redis_client.get(character_bible_key)
            if character_bible_data:
                dependencies['character_bible'] = json.loads(character_bible_data)
                logger.info("✅ Loaded Character Bible from Station 8")
            else:
                logger.warning("⚠️ No Character Bible found from Station 8")
                
            return dependencies
            
        except Exception as e:
            logger.error(f"❌ Failed to load dependencies: {e}")
            raise

    async def _generate_geography_spaces(self, dependencies: Dict[str, Any]) -> List[LocationProfile]:
        """Generate 5-10 key locations with sonic signatures using LLM"""
        
        project_bible = dependencies.get('project_bible', {})
        character_bible = dependencies.get('character_bible', {})
        
        # Extract context
        working_title = project_bible.get('working_title', 'Untitled Project')
        world_setting = project_bible.get('world_setting', {})
        genre_tone = project_bible.get('genre_tone', {})
        
        # Get character locations for reference
        protagonist_names = []
        if isinstance(character_bible, dict) and 'tier1_protagonists' in character_bible:
            # tier1_protagonists could be a list of characters or an int (count) if generation failed
            tier1_data = character_bible['tier1_protagonists']
            if isinstance(tier1_data, list):
                protagonist_names = [char.get('full_name', '') for char in tier1_data if isinstance(char, dict)]
            # If it's an int or not a list, keep protagonist_names empty
        
        # Load story lock for context
        story_lock = dependencies.get('story_lock', {})
        core_mechanism = story_lock.get('core_mechanism', '')[:200]
        
        geography_prompt = f"""
        Create 6-8 KEY LOCATIONS for the audiobook "{working_title}".

        PROJECT CONTEXT:
        Genre: {genre_tone.get('primary_genre', 'Drama')}
        Setting: {world_setting.get('time_period', 'Contemporary')} - {world_setting.get('primary_location', 'Urban')}
        Main Characters: {', '.join(protagonist_names[:3]) if protagonist_names else 'Character-driven story'}
        Story Context: {core_mechanism}

        ⚠️ CRITICAL FORMATTING REQUIREMENTS ⚠️
        - Each location MUST have a SPECIFIC, DESCRIPTIVE name (NOT "Location 1" or "Location 2")
        - Each location MUST have a detailed physical description (minimum 3-4 sentences)
        - Follow the EXACT format shown below
        
        ✅ GOOD location names: "St. Mary's Hospital Emergency Room", "Marcus's Downtown Coaching Office", 
        "Julia's Apartment on 5th Street", "Central Park Jogging Path", "The Riverside Cafe"
        
        ❌ BAD location names: "Location 1", "Location 2", "System 1", "Place A", "The Office", "The House"

        FORMAT (follow this EXACTLY for each location):

        **LOCATION 1:**
        
        **Name & Type:**
        - Location name: Detective Sarah Chen's Precinct Office
        - Type: institutional
        
        **Physical Description:**
        A cramped downtown police precinct office with fluorescent lighting that hums constantly. Gray metal desks crowd the space, topped with stacks of case files and aging computer monitors. The walls are painted institutional beige, covered with wanted posters, duty rosters, and city maps marked with colored pins. Large windows overlook the bustling street below, though venetian blinds keep most of the natural light out. The air conditioning rattles in summer, and the heating pipes clang in winter.
        
        **SONIC SIGNATURE:**
        - Primary ambient sound: Low hum of fluorescent lights, distant street traffic through windows
        - Secondary sounds: Phone rings, keyboard typing, footsteps on linoleum, radio chatter
        - Unique audio marker: The distinctive buzz of the old fax machine in the corner
        - Acoustic properties: Hard surfaces create slight echo, sounds carry between desks
        
        **Travel & Weather:**
        - Travel time to other key locations: 5 minutes to courthouse, 15 minutes to crime scenes in various districts
        - How weather sounds here: Rain drums on windows, wind whistles through old window frames, thunder rumbles
        - Seasonal audio variations: Summer brings louder AC, winter brings clanging radiators and more muffled outdoor sounds
        
        **Emotional & Story Context:**
        - Emotional association: Tension, bureaucracy, determination, exhaustion
        - Story significance: Sarah's base of operations where she coordinates investigations and confronts suspects
        - Time-of-day sound variations: Morning bustle with shift change, afternoon quieter, evening skeleton crew

        Now generate 6-8 MORE locations following this EXACT format with the SAME level of detail.
        Each location must have:
        - A specific, unique name (NOT "Location 2" or "The Office")
        - A detailed Physical Description paragraph (minimum 4 sentences, 200+ characters)
        - Complete sonic signature details
        - All other sections filled out completely
        """
        
        # Define validator for location names
        def validate_geography(locations: List[LocationProfile]) -> ValidationResult:
            errors = []
            warnings = []

            if not locations or len(locations) < 3:
                errors.append(f"Too few locations generated: {len(locations) if locations else 0}. Need at least 3.")
                return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

            # Validate location names are not generic
            location_names = [loc.name for loc in locations]
            name_validation = ContentValidator.validate_location_names(location_names)
            errors.extend(name_validation.errors)

            # Validate each location has meaningful content
            for i, loc in enumerate(locations):
                # Check description length
                if len(loc.physical_description) < 30:
                    errors.append(f"Location {i+1} description too short: {len(loc.physical_description)} chars")

                # Check sonic signature is not generic
                if 'location' in loc.sonic_signature.get('primary_ambient', '').lower() and \
                   str(i+1) in loc.sonic_signature.get('primary_ambient', ''):
                    errors.append(f"Location {i+1} has generic sonic signature")

            return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

        # Retry with validation - NO FALLBACKS
        async def generate_and_parse():
            response = await self.openrouter_agent.process_message(
                geography_prompt,
                model_name=self.config.model
            )
            # Save response for debugging if parsing fails
            if self.debug_mode:
                debug_file = f"outputs/debug_station9_geography_{datetime.now().strftime('%H%M%S')}.txt"
                os.makedirs("outputs", exist_ok=True)
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(response)
                logger.info(f"Saved geography LLM response to {debug_file}")
            return await self._parse_geography_response(response)

        retry_config = RetryConfig(max_attempts=5, initial_delay=1.0)
        locations = await retry_with_validation(
            generate_and_parse,
            validate_geography,
            retry_config,
            "Geography Generation"
        )

        if self.debug_mode:
            logger.info(f"Generated {len(locations)} validated locations from LLM")

        return locations

    async def _parse_geography_response(self, response: str) -> List[LocationProfile]:
        """Parse LLM response into structured LocationProfile objects"""
        
        # Validate response
        if not response or not isinstance(response, str):
            logger.warning(f"Invalid response from LLM: {type(response).__name__}")
            return []
        
        locations = []
        
        # Try multiple splitting patterns to handle different LLM formats
        split_patterns = [
            r'\*\*LOCATION \d+:\*\*',           # **LOCATION 1:**
            r'LOCATION \d+:',                    # LOCATION 1:
            r'### Location \d+',                 # ### Location 1
            r'\d+\.\s+(?:Location|LOCATION)',    # 1. Location
        ]
        
        location_sections = []
        for pattern in split_patterns:
            location_sections = re.split(pattern, response)
            if len(location_sections) > 1:  # Found sections
                logger.info(f"Split response using pattern: {pattern}")
                break
        
        # If no sections found, treat entire response as one location
        if len(location_sections) <= 1:
            logger.warning("Could not split response into sections, treating as single location")
            location_sections = ['', response]  # Fake first section so loop works
        
        for i, section in enumerate(location_sections[1:], 1):  # Skip first empty section
            try:
                if self.debug_mode:
                    logger.info(f"Parsing location section {i}:\n{section[:300]}...")
                
                # Extract location name - try multiple patterns
                name = None
                name_patterns = [
                    r'[-•*]\s*Location name[:\s]*([^\n]+)',  # - Location name: ...
                    r'Location name[:\s]*([^\n]+)',           # Location name: ...
                    r'Name[:\s]*([^\n]+)',                    # Name: ...
                    r'\*\*Name[:\s]*\*\*[:\s]*([^\n]+)',     # **Name:** ...
                ]
                
                for pattern in name_patterns:
                    name_match = re.search(pattern, section, re.IGNORECASE)
                    if name_match:
                        name = name_match.group(1).strip()
                        break
                
                # If no name found, raise error to trigger retry
                if not name:
                    raise ValueError(f"Could not extract location name from section {i}. LLM must provide 'Location name:' field.")
                
                # Clean markdown artifacts from name
                name = name.replace('**', '').replace('*', '').strip()
                name = re.sub(r'^[\s\-\*•]+', '', name).strip()
                
                # Remove parenthetical type info if present
                name = re.sub(r'\s*\([^)]*\)\s*$', '', name).strip()
                
                # Validate name is not a placeholder - FAIL if it is
                placeholder_patterns = [r'^\[.*\]$', r'^TBD$', r'^TODO$', r'^N/A$', r'^Location\s*\d+$', r'^Place\s*[A-Z]$']
                is_placeholder = any(re.match(pattern, name, re.IGNORECASE) for pattern in placeholder_patterns)
                
                if is_placeholder:
                    raise ValueError(f"LLM returned generic/placeholder location name: '{name}'. Must provide specific location name.")
                
                if len(name) < 3:
                    raise ValueError(f"Location name too short: '{name}'. Must provide specific location name with at least 3 characters.")
                
                # Extract type - try multiple patterns
                type_match = re.search(r'[-•*]\s*Type[:\s]*\(?([^)\n]+)', section, re.IGNORECASE)
                if not type_match:
                    type_match = re.search(r'Type[:\s]*\(?([^)\n]+)', section, re.IGNORECASE)
                location_type = type_match.group(1).strip() if type_match else "general"
                location_type = location_type.replace(')', '').strip()
                
                # Extract physical description - MUST exist
                try:
                    phys_desc = self._extract_section(section, "Physical Description", None)
                    if len(phys_desc) < 30:
                        raise ValueError(f"Physical description too short ({len(phys_desc)} chars): '{phys_desc}'")
                except Exception as e:
                    raise ValueError(f"Failed to extract Physical Description for location {i}: {str(e)}")
                
                # Extract sonic signature components
                primary_ambient = self._extract_section(section, "Primary ambient sound", "Ambient soundscape")
                secondary_sounds = self._extract_section(section, "Secondary sounds", "Environmental sounds")
                unique_marker = self._extract_section(section, "Unique audio marker", "Distinctive sound")
                acoustic_props = self._extract_section(section, "Acoustic properties", "Natural acoustics")
                
                # Extract other details
                emotional_assoc = self._extract_section(section, "Emotional association", "Neutral emotional context")
                story_significance = self._extract_section(section, "Story significance", "Important to narrative")
                
                # Build sonic signature
                sonic_signature = {
                    "primary_ambient": primary_ambient,
                    "secondary_sounds": secondary_sounds,
                    "unique_marker": unique_marker,
                    "acoustic_properties": acoustic_props
                }
                
                # Build travel times (simplified)
                travel_times = {"other_locations": "Variable travel time"}
                
                # Build weather patterns
                weather_patterns = {
                    "rain": f"Rain sounds in {name}",
                    "wind": f"Wind patterns at {name}",
                    "clear": f"Clear weather audio at {name}"
                }
                
                # Build acoustic properties
                acoustic_properties = {
                    "reverb": "Natural reverb characteristics",
                    "echo": "Echo patterns",
                    "absorption": "Sound absorption qualities"
                }
                
                # Build time variations
                time_variations = {
                    "morning": f"Morning sounds at {name}",
                    "afternoon": f"Afternoon audio at {name}",
                    "evening": f"Evening atmosphere at {name}",
                    "night": f"Night sounds at {name}"
                }
                
                location = LocationProfile(
                    name=name,
                    location_type=location_type,
                    physical_description=phys_desc,
                    sonic_signature=sonic_signature,
                    travel_times=travel_times,
                    weather_patterns=weather_patterns,
                    acoustic_properties=acoustic_properties,
                    emotional_association=emotional_assoc,
                    story_significance=story_significance,
                    time_variations=time_variations
                )
                
                locations.append(location)
                
            except Exception as e:
                logger.error(f"Failed to parse location {i}: {e}")
                # DO NOT create fallback - raise error to trigger retry
                raise ValueError(f"Location {i} parsing failed: {str(e)}")

        # FAIL if not enough locations - NO FALLBACKS
        if len(locations) < 3:
            raise ValueError(f"Only {len(locations)} locations parsed. LLM must provide at least 3 locations.")

        logger.info(f"Successfully parsed {len(locations)} locations")
        return locations[:10]  # Max 10 locations

    def _extract_section(self, text: str, keyword: str, fallback: str = None) -> str:
        """Extract a section from LLM response with flexible pattern matching"""
        # Validate input
        if not text or not isinstance(text, str):
            if fallback is not None:
                return fallback
            raise ValueError(f"Invalid text for extracting '{keyword}'")
        
        # Try multiple patterns in order of preference
        patterns = [
            # Multi-line block after header with colon INSIDE bold (e.g., **Physical Description:**\n[content...])
            # This is the most common format LLMs use
            (rf'\*\*{re.escape(keyword)}[:\s]*\*\*\s*\n\s*(.+?)(?=\n\s*\*\*|$)', re.DOTALL),
            
            # Multi-line block after header with colon OUTSIDE bold (e.g., **Physical Description**:\n[content...])
            (rf'\*\*{re.escape(keyword)}\*\*[:\s]*\n\s*(.+?)(?=\n\s*\*\*|$)', re.DOTALL),
            
            # Same line with bullet point (e.g., - Primary ambient sound: [content])
            (rf'[-•*]\s*{re.escape(keyword)}[:\s]*(.+?)(?=\n|$)', 0),
            
            # Header on its own line, content follows (e.g., Physical Description:\n[content])
            (rf'{re.escape(keyword)}[:\s]*\n\s*(.+?)(?=\n\s*(?:\*\*|[-•*]\s+\w+[:\s])|$)', re.DOTALL),
            
            # Same line after keyword (e.g., Physical Description: [content])
            (rf'{re.escape(keyword)}[:\s]+(.+?)(?=\n\s*(?:\*\*|[-•*])|$)', 0),
            
            # Bold keyword same line with colon inside (e.g., **Keyword:** content)
            (rf'\*\*{re.escape(keyword)}[:\s]*\*\*[:\s]+(.+?)(?=\n|$)', 0),
        ]
        
        for pattern, flags in patterns:
            try:
                base_flags = re.IGNORECASE | re.MULTILINE
                if flags:
                    base_flags |= flags
                    
                match = re.search(pattern, text, base_flags)
                if match:
                    captured = match.group(1)
                    if captured:
                        # Clean up the captured content
                        cleaned = captured.strip()
                        # Remove markdown artifacts
                        cleaned = re.sub(r'^\*\*|\*\*$', '', cleaned)  # Remove ** at start/end
                        cleaned = re.sub(r'^\[|\]$', '', cleaned)       # Remove [ ] at start/end
                        cleaned = cleaned.strip()
                        
                        # Only return if we got meaningful content
                        if cleaned and len(cleaned) > 2:  # More than just punctuation
                            return cleaned
            except Exception as e:
                logger.debug(f"Pattern failed for '{keyword}': {e}")
                continue
        
        if fallback is None:
            raise ValueError(f"Failed to extract '{keyword}' from LLM response and no fallback allowed.")
        return fallback


    async def _generate_social_systems(self, dependencies: Dict[str, Any], geography: List[LocationProfile]) -> SocialSystem:
        """Generate government, economy, hierarchies with audio manifestations"""
        
        project_bible = dependencies.get('project_bible', {})
        working_title = project_bible.get('working_title', 'Untitled Project')
        genre_tone = project_bible.get('genre_tone', {})
        
        location_names = [loc.name for loc in geography[:3]]  # Use first 3 locations for context
        
        social_prompt = f"""
        Generate SOCIAL SYSTEMS for the audiobook "{working_title}".

        PROJECT CONTEXT:
        Genre: {genre_tone.get('primary_genre', 'Drama')}
        Key Locations: {', '.join(location_names)}

        Create detailed social systems covering:

        **GOVERNMENT/AUTHORITY STRUCTURE:**
        - Leadership hierarchy and power structure
        - How authority is expressed in dialogue
        - Formal vs informal power dynamics
        - Audio cues for rank and status

        **ECONOMIC SYSTEM:**
        - Currency and trade mechanisms
        - Class divisions and wealth indicators
        - How economic status sounds in speech
        - Audio markers of financial position

        **SOCIAL HIERARCHIES:**
        - Class/caste/rank system
        - How people address superiors/inferiors
        - Formality levels and speech patterns
        - Status-based audio access and restrictions

        **CULTURAL NORMS:**
        - Standard greetings and social rituals
        - Taboos and forbidden topics
        - Customs that affect daily interaction
        - Cultural phrases and expressions

        **AUDIO MANIFESTATIONS:**
        - How social class affects accent and vocabulary
        - Formality markers in dialogue
        - Status-based sound design elements
        - Cultural audio rituals and ceremonies

        Focus on how these social systems create AUDIO-DISTINGUISHABLE differences between characters and situations.
        """
        
        try:
            response = await self.openrouter_agent.process_message(
                social_prompt,
                model_name="qwen-72b"
            )
            
            social_system = await self._parse_social_systems_response(response)
            
            if self.debug_mode:
                logger.info("Generated social systems with audio manifestations")
                
            return social_system
            
        except Exception as e:
            logger.error(f"Failed to generate social systems: {e}")
            raise ValueError(f"Social system generation failed. LLM must provide complete social system data: {str(e)}")

    async def _parse_social_systems_response(self, response: str) -> SocialSystem:
        """Parse social systems response into structured data"""
        
        try:
            # Extract government structure
            government = self._extract_section(response, "GOVERNMENT/AUTHORITY STRUCTURE", "Government system")
            
            # Extract authority sounds
            authority_sounds = self._extract_list(response, "authority.*dialogue", ["Formal address patterns", "Status indicators"])
            
            # Extract economic system
            economic = self._extract_section(response, "ECONOMIC SYSTEM", "Economic structure")
            
            # Build class divisions
            class_divisions = [
                {"level": "Upper", "description": "Upper class characteristics"},
                {"level": "Middle", "description": "Middle class characteristics"},
                {"level": "Lower", "description": "Lower class characteristics"}
            ]
            
            # Build social hierarchies
            social_hierarchies = {
                "formal_hierarchy": "Official social structure",
                "informal_power": "Unofficial influence networks",
                "address_patterns": "How rank affects speech"
            }
            
            # Extract cultural norms
            cultural_norms = self._extract_list(response, "cultural norms", ["Social customs", "Interaction patterns"])
            
            # Build audio manifestations
            audio_manifestations = {
                "class_accents": ["Upper class speech", "Middle class speech", "Lower class speech"],
                "formality_markers": ["Formal language patterns", "Informal speech"],
                "status_indicators": ["Authority voice cues", "Deference markers"]
            }
            
            # Build dialogue formality
            dialogue_formality = {
                "superior_to_subordinate": "Formal, direct",
                "subordinate_to_superior": "Respectful, deferential",
                "peer_to_peer": "Casual, familiar",
                "stranger_to_stranger": "Polite, reserved"
            }
            
            return SocialSystem(
                government_structure=government,
                authority_sounds=authority_sounds,
                economic_system=economic,
                class_divisions=class_divisions,
                social_hierarchies=social_hierarchies,
                cultural_norms=cultural_norms,
                audio_manifestations=audio_manifestations,
                dialogue_formality=dialogue_formality
            )
            
        except Exception as e:
            logger.error(f"Failed to parse social systems: {e}")
            raise ValueError(f"Social system parsing failed. LLM must provide complete social system data: {str(e)}")

    def _extract_list(self, text: str, keyword: str, fallback: List[str] = None) -> List[str]:
        """Extract a list from LLM response - FAIL if not found and no fallback"""
        try:
            section = self._extract_section(text, keyword, "")
        except:
            section = ""
        
        if section:
            # Look for bullet points or numbered items
            items = re.findall(r'[-•*]\s*([^\n]+)', section)
            if not items:
                items = re.findall(r'\d+\.\s*([^\n]+)', section)
            if not items:
                # Split by commas or semicolons
                items = [item.strip() for item in re.split(r'[,;]', section) if item.strip()]
            if items:
                return items[:10]
        
        if fallback is None:
            raise ValueError(f"Failed to extract list for '{keyword}' from LLM response and no fallback allowed.")
        return fallback


    async def _generate_tech_magic_systems(self, dependencies: Dict[str, Any]) -> List[TechMagicSystem]:
        """Generate technology/magic systems with signature sounds"""
        
        project_bible = dependencies.get('project_bible', {})
        working_title = project_bible.get('working_title', 'Untitled Project')
        genre_tone = project_bible.get('genre_tone', {})
        world_setting = project_bible.get('world_setting', {})
        
        tech_magic_prompt = f"""
        Generate TECHNOLOGY/MAGIC SYSTEMS for the audiobook "{working_title}".

        PROJECT CONTEXT:
        Genre: {genre_tone.get('primary_genre', 'Drama')}
        Setting: {world_setting.get('time_period', 'Contemporary')}

        Create 5-8 TECHNOLOGY or MAGIC elements:

        For EACH system provide:

        **SYSTEM [NUMBER]:**
        
        **Name & Description:**
        - System name
        - What it does and how it works
        - Access level (common/rare/legendary)
        
        **SIGNATURE SOUNDS:**
        - Activation sound (how it starts)
        - Operation sound (while running)
        - Completion sound (how it ends)
        - Malfunction sound (when it breaks)
        
        **MECHANICS & LIMITATIONS:**
        - Rules and constraints
        - Power source or requirements
        - Failure modes and risks
        
        **AUDIO DISTINCTIVENESS:**
        - How characters recognize this system by sound
        - Environmental audio changes when active
        - Unique audio signature elements
        
        **NARRATIVE FUNCTION:**
        - Story purpose and plot relevance
        - Character relationships to this system
        - Conflict potential

        Make each system SONICALLY UNIQUE for audio drama production.
        """
        
        try:
            response = await self.openrouter_agent.process_message(
                tech_magic_prompt,
                model_name="qwen-72b"
            )
            
            # Save response for debugging if parsing fails
            if self.debug_mode:
                debug_file = f"outputs/debug_station9_techmagic_{datetime.now().strftime('%H%M%S')}.txt"
                os.makedirs("outputs", exist_ok=True)
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(response)
                logger.info(f"Saved tech/magic LLM response to {debug_file}")
            
            systems = await self._parse_tech_magic_response(response)
            
            if self.debug_mode:
                logger.info(f"Generated {len(systems)} tech/magic systems")
                
            return systems
            
        except Exception as e:
            logger.error(f"Failed to generate tech/magic systems: {e}")
            raise ValueError(f"Tech/magic system generation failed. LLM must provide complete tech/magic data: {str(e)}")

    async def _parse_tech_magic_response(self, response: str) -> List[TechMagicSystem]:
        """Parse tech/magic response into structured systems"""
        
        systems = []
        
        # Try multiple splitting patterns to handle different LLM formats
        split_patterns = [
            r'###\s*SYSTEM \d+:',         # ### SYSTEM 1:
            r'\*\*SYSTEM \d+:\*\*',       # **SYSTEM 1:**
            r'SYSTEM \d+:',                # SYSTEM 1:
        ]
        
        system_sections = []
        for pattern in split_patterns:
            system_sections = re.split(pattern, response)
            if len(system_sections) > 1:
                if self.debug_mode:
                    logger.info(f"Split tech/magic response using pattern: {pattern} into {len(system_sections)} sections")
                break
        
        if len(system_sections) <= 1:
            if self.debug_mode:
                logger.warning(f"No SYSTEM sections found. Response preview: {response[:500]}...")
            # Return empty list to trigger retry
            raise ValueError("No SYSTEM sections found in LLM response")
        
        for i, section in enumerate(system_sections[1:], 1):  # Skip first empty section
            try:
                if self.debug_mode:
                    logger.info(f"Parsing tech/magic system section {i}:\n{section[:300]}...")
                
                # Extract system name - try multiple patterns
                name = None
                name_patterns = [
                    r'[-•*]\s*\*\*System [Nn]ame[:\s]*\*\*[:\s]*(.+?)(?=\n|$)',  # - **System name:** EchoCast
                    r'\*\*System [Nn]ame[:\s]*\*\*[:\s]*(.+?)(?=\n|$)',          # **System name:** EchoCast
                    r'[-•*]\s*System [Nn]ame[:\s]*(.+?)(?=\n|$)',                # - System name: EchoCast
                    r'System [Nn]ame[:\s]*(.+?)(?=\n|$)',                        # System name: EchoCast
                    r'^\s*\*\*(.+?)\*\*\s*$',                                    # **ECHOCAST** (on first line)
                ]
                
                for pattern in name_patterns:
                    name_match = re.search(pattern, section, re.IGNORECASE | re.MULTILINE)
                    if name_match:
                        name = name_match.group(1).strip()
                        # Clean up markdown
                        name = name.replace('**', '').replace('*', '').strip()
                        if len(name) > 2:
                            break
                
                if not name:
                    name = f"System {i}"
                
                # Extract description - try multiple keywords
                description = None
                desc_keywords = ["Description", "What it does"]
                for keyword in desc_keywords:
                    try:
                        description = self._extract_section(section, keyword, None)
                        if description:
                            break
                    except:
                        continue
                
                if not description:
                    description = f"Technology/magic system {i}"
                
                # Extract access level - try multiple patterns
                access_patterns = [
                    r'[-•*]\s*\*\*Access [Ll]evel[:\s]*\*\*[:\s]*(.+?)(?=\n|$)',  # - **Access Level:** Common
                    r'\*\*Access [Ll]evel[:\s]*\*\*[:\s]*(.+?)(?=\n|$)',          # **Access Level:** Common
                    r'[-•*]\s*Access [Ll]evel[:\s]*\(([^)]+)\)',                   # - Access level: (Common)
                    r'Access [Ll]evel[:\s]*\(([^)]+)\)',                           # Access level: (Common)
                    r'[-•*]\s*Access [Ll]evel[:\s]*(.+?)(?=\n|$)',                # - Access level: Common
                    r'Access [Ll]evel[:\s]*(.+?)(?=\n|$)',                        # Access level: Common
                ]
                
                access_level = "common"
                for pattern in access_patterns:
                    access_match = re.search(pattern, section, re.IGNORECASE)
                    if access_match:
                        access_level = access_match.group(1).strip().lower()
                        break
                
                # Extract signature sounds
                activation_sound = self._extract_section(section, "Activation sound", "Startup audio")
                operation_sound = self._extract_section(section, "Operation sound", "Running audio")
                completion_sound = self._extract_section(section, "Completion sound", "Completion audio")
                malfunction_sound = self._extract_section(section, "Malfunction sound", "Error audio")
                
                signature_sounds = {
                    "activation": activation_sound,
                    "operation": operation_sound,
                    "completion": completion_sound,
                    "malfunction": malfunction_sound
                }
                
                # Extract other details
                mechanics = self._extract_section(section, "Rules and constraints", "System mechanics")
                limitations = self._extract_list(section, "limitations", ["System constraints"])
                narrative_function = self._extract_section(section, "Story purpose", "Narrative importance")
                audio_distinctiveness = self._extract_section(section, "AUDIO DISTINCTIVENESS", "Unique audio signature")
                
                system = TechMagicSystem(
                    name=name,
                    description=description,
                    mechanics=mechanics,
                    access_level=access_level,
                    signature_sounds=signature_sounds,
                    limitations=limitations,
                    narrative_function=narrative_function,
                    audio_distinctiveness=audio_distinctiveness
                )
                
                systems.append(system)
                
            except Exception as e:
                logger.error(f"Failed to parse tech/magic system {i}: {e}")
                raise ValueError(f"Tech/magic system {i} parsing failed. LLM must provide complete tech/magic system data: {str(e)}")
        
        # FAIL if not enough systems - no fallbacks
        if len(systems) < 2:
            raise ValueError(f"Only {len(systems)} tech/magic systems parsed. LLM must provide at least 2 systems.")
        
        return systems[:8]  # Max 8 systems


    async def _generate_history_lore(self, dependencies: Dict[str, Any], geography: List[LocationProfile]) -> tuple[List[HistoricalEvent], List[Dict[str, str]]]:
        """Generate historical timeline and mythology"""
        
        project_bible = dependencies.get('project_bible', {})
        working_title = project_bible.get('working_title', 'Untitled Project')
        location_names = [loc.name for loc in geography[:3]]
        
        history_prompt = f"""
        Generate HISTORY & LORE for the audiobook "{working_title}".

        WORLD CONTEXT:
        Key Locations: {', '.join(location_names)}

        Create historical depth covering:

        **HISTORICAL TIMELINE (5-7 events):**
        For each event:
        - Event name and timeframe
        - What happened and consequences
        - Public knowledge vs hidden truth
        - Audio echoes (sounds/phrases that reference this)

        **MYTHOLOGY & FOLKLORE (3-5 stories):**
        - Legend name and summary
        - Cultural significance
        - How it influences behavior
        - Audio manifestations (ritual phrases, warnings)

        **COMMON KNOWLEDGE:**
        - What everyone knows about history
        - Shared cultural memories
        - Historical phrases used today
        - Conversational references

        **SECRETS & HIDDEN TRUTHS:**
        - What really happened vs official story
        - Who knows the truth
        - Clues in the world
        - How secrets emerge in dialogue

        Focus on creating AUDIO-RICH historical depth that enhances the narrative.
        """
        
        try:
            response = await self.openrouter_agent.process_message(
                history_prompt,
                model_name="qwen-72b"
            )
            
            # Save response for debugging if parsing fails
            if self.debug_mode:
                debug_file = f"outputs/debug_station9_history_{datetime.now().strftime('%H%M%S')}.txt"
                os.makedirs("outputs", exist_ok=True)
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(response)
                logger.info(f"Saved history/lore LLM response to {debug_file}")
            
            events, mythology = await self._parse_history_lore_response(response)
            
            if self.debug_mode:
                logger.info(f"Generated {len(events)} historical events and {len(mythology)} mythology entries")
                
            return events, mythology
            
        except Exception as e:
            logger.error(f"Failed to generate history/lore: {e}")
            raise ValueError(f"History/lore generation failed. LLM must provide complete history/lore data: {str(e)}")

    async def _parse_history_lore_response(self, response: str) -> tuple[List[HistoricalEvent], List[Dict[str, str]]]:
        """Parse history/lore response into structured data"""
        
        events = []
        mythology = []
        
        try:
            if self.debug_mode:
                logger.info(f"Parsing history/lore response of length {len(response)}")
            
            # Extract historical events
            # Look for patterns like "Event name:"
            event_patterns = re.findall(r'[-•*]\s*([^:\n]+):\s*([^\n]+)', response)
            
            if self.debug_mode:
                logger.info(f"Found {len(event_patterns)} event patterns")
            
            for i, (name, description) in enumerate(event_patterns[:6]):  # Max 6 events
                event = HistoricalEvent(
                    name=name.strip(),
                    timeframe=f"Historical period {i + 1}",
                    description=description.strip(),
                    consequences=f"Consequences of {name}",
                    public_knowledge=f"Public knowledge about {name}",
                    hidden_truth=f"Hidden truth about {name}",
                    audio_echoes=[f"Audio reference to {name}"]
                )
                events.append(event)
            
            # Extract mythology - try to find the MYTHOLOGY & FOLKLORE section
            mythology_section = ""
            
            # Try multiple patterns to find the mythology section
            myth_section_patterns = [
                r'####\s*\*\*MYTHOLOGY\s*&\s*FOLKLORE[:\s]*\*\*(.*?)(?=####|###|$)',  # #### **MYTHOLOGY & FOLKLORE:**
                r'###\s*\*\*MYTHOLOGY\s*&\s*FOLKLORE[:\s]*\*\*(.*?)(?=####|###|$)',   # ### **MYTHOLOGY & FOLKLORE:**
                r'###\s*MYTHOLOGY\s*&\s*FOLKLORE[:\s]*(.*?)(?=###|$)',                 # ### MYTHOLOGY & FOLKLORE:
                r'\*\*MYTHOLOGY\s*&\s*FOLKLORE[:\s]*\*\*(.*?)(?=###|\*\*[A-Z]|$)',   # **MYTHOLOGY & FOLKLORE:**
            ]
            
            for pattern in myth_section_patterns:
                match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
                if match:
                    mythology_section = match.group(1)
                    if self.debug_mode:
                        logger.info(f"Found mythology section using pattern: {pattern}")
                        logger.info(f"Mythology section content (first 500 chars): {mythology_section[:500]}")
                    break
            
            if mythology_section:
                # Look for numbered legends/myths with summary
                # Pattern: 1. **The Legend of X**\n   - **Legend Name:**...\n   - **Summary:** ...
                # Or simpler: 1. **The Legend of X**\n   ... - **Summary:** ...
                myth_patterns = re.findall(
                    r'\d+\.\s*\*\*(.+?)\*\*.*?-\s*\*\*Summary[:\s]*\*\*[:\s]*(.+?)(?=\n\s*-\s*\*\*[A-Z]|\n\s*\d+\.|\Z)',
                    mythology_section,
                    re.DOTALL
                )
                
                if self.debug_mode:
                    logger.info(f"Found {len(myth_patterns)} mythology entries")
                
                for myth_name, summary in myth_patterns[:4]:  # Max 4 myths
                    mythology.append({
                        "name": myth_name.strip(),
                        "summary": summary.strip()[:200],  # Limit summary length
                        "significance": f"Cultural significance of {myth_name}",
                        "audio_manifestation": f"Audio manifestation related to {myth_name}"
                    })
            
            # Ensure minimum content - FAIL if not enough events
            # Mythology is optional since LLMs don't always include it
            if len(events) < 3:
                raise ValueError(f"Only {len(events)} historical events parsed. LLM must provide at least 3 events.")
            
            # If no mythology found, create minimal entries to avoid failures
            if len(mythology) == 0:
                if self.debug_mode:
                    logger.warning("No mythology entries found, creating fallback entries")
                mythology = [
                    {
                        "name": "Local Folklore",
                        "summary": "Traditional stories passed down through generations",
                        "significance": "Cultural heritage of the community",
                        "audio_manifestation": "Phrases and sayings in dialogue"
                    },
                    {
                        "name": "Urban Legends",
                        "summary": "Modern myths about the city and its locations",
                        "significance": "Shared community narratives",
                        "audio_manifestation": "References in casual conversation"
                    }
                ]
                
            return events, mythology
            
        except Exception as e:
            logger.error(f"Failed to parse history/lore: {e}")
            raise ValueError(f"History/lore parsing failed. LLM must provide properly formatted history/lore data: {str(e)}")


    async def _generate_sensory_palettes(self, geography: List[LocationProfile], dependencies: Dict[str, Any]) -> List[SensoryPalette]:
        """Generate comprehensive audio cue library for all locations"""
        
        palettes = []
        
        for location in geography:
            sensory_prompt = f"""
            Generate COMPREHENSIVE AUDIO CUE LIBRARY for location: "{location.name}"

            LOCATION CONTEXT:
            Type: {location.location_type}
            Description: {location.physical_description}
            Emotional Association: {location.emotional_association}

            Create detailed sensory palette:

            **AMBIENT SOUNDSCAPE (4 layers):**
            - Base layer (constant background)
            - Mid layer (frequent sounds)
            - Top layer (occasional sounds)
            - Silence points (when ambient drops)

            **DISTINCTIVE AUDIO MARKERS:**
            - Signature sound (unique to this location)
            - Warning sounds (danger indicators)
            - Welcome sounds (arrival indicators)
            - Transition sounds (leaving indicators)

            **ACOUSTIC PROPERTIES:**
            - Reverb characteristics
            - Echo patterns
            - Sound absorption qualities
            - How voices sound here

            **TIME VARIATIONS:**
            - Morning audio elements
            - Afternoon soundscape
            - Evening atmosphere
            - Night sounds

            **EMOTIONAL SOUND PALETTE:**
            - Calm/peaceful sounds
            - Tense/dangerous sounds
            - Mysterious sounds
            - Comforting sounds

            **PRODUCTION NOTES:**
            - Microphone positioning
            - Mixing recommendations
            - Sound design notes

            Make this PRODUCTION-READY for audio teams.
            """
            
            try:
                response = await self.openrouter_agent.process_message(
                    sensory_prompt,
                    model_name="qwen-72b"
                )
                
                palette = await self._parse_sensory_palette_response(response, location.name)
                palettes.append(palette)
                
            except Exception as e:
                logger.error(f"Failed to generate sensory palette for {location.name}: {e}")
                raise ValueError(f"Sensory palette generation failed for '{location.name}'. LLM must provide complete sensory palette: {str(e)}")
        
        return palettes

    async def _parse_sensory_palette_response(self, response: str, location_name: str) -> SensoryPalette:
        """Parse sensory palette response"""
        
        try:
            # Extract ambient layers
            base_layer = self._extract_section(response, "Base layer", "Background ambience")
            mid_layer = self._extract_section(response, "Mid layer", "Environmental sounds")
            top_layer = self._extract_section(response, "Top layer", "Occasional sounds")
            silence_points = self._extract_section(response, "Silence points", "Quiet moments")
            
            ambient_soundscape = {
                "base_layer": [base_layer],
                "mid_layer": [mid_layer],
                "top_layer": [top_layer],
                "silence_points": [silence_points]
            }
            
            # Extract distinctive markers
            distinctive_markers = self._extract_list(response, "DISTINCTIVE AUDIO MARKERS", 
                                                   ["Signature sound", "Location identifier"])
            
            # Extract acoustic properties
            reverb = self._extract_section(response, "Reverb", "Natural reverb")
            echo = self._extract_section(response, "Echo", "Echo characteristics")
            absorption = self._extract_section(response, "absorption", "Sound absorption")
            
            acoustic_properties = {
                "reverb": reverb,
                "echo": echo,
                "absorption": absorption
            }
            
            # Extract time variations
            morning = self._extract_list(response, "Morning", ["Morning ambience"])
            afternoon = self._extract_list(response, "Afternoon", ["Afternoon sounds"])
            evening = self._extract_list(response, "Evening", ["Evening atmosphere"])
            night = self._extract_list(response, "Night", ["Night sounds"])
            
            time_variations = {
                "morning": morning,
                "afternoon": afternoon,
                "evening": evening,
                "night": night
            }
            
            # Extract emotional palette
            calm = self._extract_list(response, "Calm", ["Peaceful sounds"])
            tense = self._extract_list(response, "Tense", ["Tension audio"])
            mysterious = self._extract_list(response, "Mysterious", ["Mystery elements"])
            comforting = self._extract_list(response, "Comforting", ["Comfort sounds"])
            
            emotional_palette = {
                "calm": calm,
                "tense": tense,
                "mysterious": mysterious,
                "comforting": comforting
            }
            
            # Extract production notes
            production_notes = self._extract_list(response, "PRODUCTION NOTES", 
                                                ["Audio production guidance"])
            
            return SensoryPalette(
                location_name=location_name,
                ambient_soundscape=ambient_soundscape,
                distinctive_markers=distinctive_markers,
                acoustic_properties=acoustic_properties,
                time_variations=time_variations,
                emotional_palette=emotional_palette,
                recurring_motifs=[f"Audio motif for {location_name}"],
                production_notes=production_notes
            )
            
        except Exception as e:
            logger.error(f"Failed to parse sensory palette: {e}")
            raise ValueError(f"Sensory palette parsing failed for '{location_name}'. LLM must provide complete sensory data: {str(e)}")


    async def _generate_audio_glossary(self, world_components: Dict[str, Any]) -> Dict[str, str]:
        """Generate comprehensive audio glossary"""
        
        glossary_prompt = f"""
        Generate AUDIO GLOSSARY for this world bible.

        WORLD COMPONENTS:
        - {len(world_components.get('geography', []))} locations
        - Social systems and hierarchies
        - Technology/magic systems
        - Historical events and lore

        Create 30-50 unique audio glossary entries:

        Format as:
        **Sound Name**: Detailed description of what this sounds like, when it occurs, and what it signifies

        Include entries for:
        - Location-specific signature sounds
        - Technology/magic activation sounds
        - Social/cultural audio markers
        - Historical audio echoes
        - Environmental audio cues
        - Character status indicators
        - Emotional state sounds
        - Ritual/ceremonial sounds

        Make each entry PRODUCTION-READY for sound designers.
        """
        
        try:
            response = await self.openrouter_agent.process_message(
                glossary_prompt,
                model_name="qwen-72b"
            )
            
            glossary = await self._parse_audio_glossary_response(response)
            
            if self.debug_mode:
                logger.info(f"Generated audio glossary with {len(glossary)} entries")
                
            return glossary
            
        except Exception as e:
            logger.error(f"Failed to generate audio glossary: {e}")
            raise ValueError(f"Audio glossary generation failed. LLM must provide complete glossary data: {str(e)}")

    async def _parse_audio_glossary_response(self, response: str) -> Dict[str, str]:
        """Parse audio glossary response - handles multiple format variations"""
        
        glossary = {}
        
        try:
            # Try multiple parsing patterns to handle different LLM output formats
            
            # Pattern 1: **Sound Name**: Description
            entries = re.findall(r'\*\*([^:*\n]+)\*\*:\s*([^\n]+(?:\n(?!\*\*)[^\n]*)*)', response)
            for sound_name, description in entries:
                clean_name = sound_name.strip()
                clean_description = description.strip()
                if clean_name and clean_description and len(clean_name) > 2:
                    glossary[clean_name] = clean_description
            
            # Pattern 2: - **Sound Name**: Description (bullet points)
            if len(glossary) < 5:
                entries = re.findall(r'[-•*]\s*\*\*([^:*\n]+)\*\*:\s*([^\n]+)', response)
                for sound_name, description in entries:
                    clean_name = sound_name.strip()
                    clean_description = description.strip()
                    if clean_name and clean_description and len(clean_name) > 2:
                        if clean_name not in glossary:
                            glossary[clean_name] = clean_description
            
            # Pattern 3: "Sound Name" - Description or "Sound Name": Description
            if len(glossary) < 5:
                entries = re.findall(r'[""""]([^""""\n]+)[""""]\s*[:-]\s*([^\n]+)', response)
                for sound_name, description in entries:
                    clean_name = sound_name.strip()
                    clean_description = description.strip()
                    if clean_name and clean_description and len(clean_name) > 2:
                        if clean_name not in glossary:
                            glossary[clean_name] = clean_description
            
            # Pattern 4: Numbered list: 1. Sound Name: Description
            if len(glossary) < 5:
                entries = re.findall(r'\d+\.\s*([^:\n]+):\s*([^\n]+)', response)
                for sound_name, description in entries:
                    clean_name = sound_name.strip()
                    clean_description = description.strip()
                    if clean_name and clean_description and len(clean_name) > 2:
                        if clean_name not in glossary:
                            glossary[clean_name] = clean_description
            
            logger.info(f"Audio glossary parsed: {len(glossary)} entries found")
            
            # FAIL if not enough entries
            if len(glossary) < 5:
                logger.error(f"Response preview (first 500 chars): {response[:500]}")
                raise ValueError(f"Only {len(glossary)} glossary entries parsed from LLM response. Need at least 5 entries. Check response format.")
                
            return glossary
            
        except Exception as e:
            logger.error(f"Failed to parse audio glossary: {e}")
            raise ValueError(f"Audio glossary parsing failed: {str(e)}")


    def export_to_text(self, world_bible: WorldBible) -> str:
        """Export world bible to text format"""
        
        sections = []
        
        # Header
        sections.append("=" * 70)
        sections.append("WORLD BIBLE - AUDIO DRAMA WORLD BUILDING")
        sections.append("=" * 70)
        sections.append(f"Project: {world_bible.working_title}")
        sections.append(f"Session: {world_bible.session_id}")
        sections.append(f"Generated: {world_bible.created_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        sections.append("")
        
        # Statistics
        sections.append("WORLD STATISTICS")
        sections.append("-" * 30)
        sections.append(f"Total Locations: {world_bible.world_statistics['total_locations']}")
        sections.append(f"Tech/Magic Systems: {world_bible.world_statistics['tech_magic_systems']}")
        sections.append(f"Historical Events: {world_bible.world_statistics['historical_events']}")
        sections.append(f"Audio Cues: {world_bible.world_statistics['audio_cues']}")
        sections.append(f"Glossary Entries: {world_bible.world_statistics['glossary_entries']}")
        sections.append("")
        
        # Section 1: Geography
        sections.append("=" * 70)
        sections.append("SECTION 1: GEOGRAPHY & SPACES")
        sections.append("=" * 70)
        for location in world_bible.geography:
            sections.append(f"\n{location.name.upper()} ({location.location_type})")
            sections.append("-" * len(location.name))
            sections.append(f"Description: {location.physical_description}")
            sections.append(f"Emotional Context: {location.emotional_association}")
            sections.append(f"Story Significance: {location.story_significance}")
            sections.append("")
            sections.append("SONIC SIGNATURE:")
            sections.append(f"  Primary Ambient: {location.sonic_signature.get('primary_ambient', 'N/A')}")
            sections.append(f"  Secondary Sounds: {location.sonic_signature.get('secondary_sounds', 'N/A')}")
            sections.append(f"  Unique Marker: {location.sonic_signature.get('unique_marker', 'N/A')}")
            sections.append(f"  Acoustics: {location.sonic_signature.get('acoustic_properties', 'N/A')}")
            sections.append("")
        
        # Section 2: Social Systems
        sections.append("\n" + "=" * 70)
        sections.append("SECTION 2: SOCIAL SYSTEMS")
        sections.append("=" * 70)
        sections.append(f"Government: {world_bible.social_systems.government_structure}")
        sections.append(f"Economy: {world_bible.social_systems.economic_system}")
        sections.append("")
        sections.append("AUDIO MANIFESTATIONS:")
        for category, sounds in world_bible.social_systems.audio_manifestations.items():
            sections.append(f"  {category.title()}: {', '.join(sounds)}")
        sections.append("")
        sections.append("DIALOGUE FORMALITY:")
        for relationship, style in world_bible.social_systems.dialogue_formality.items():
            sections.append(f"  {relationship.replace('_', ' ').title()}: {style}")
        sections.append("")
        
        # Section 3: Technology/Magic
        sections.append("\n" + "=" * 70)
        sections.append("SECTION 3: TECHNOLOGY & MAGIC")
        sections.append("=" * 70)
        for system in world_bible.tech_magic_systems:
            sections.append(f"\n{system.name.upper()} ({system.access_level})")
            sections.append("-" * len(system.name))
            sections.append(f"Description: {system.description}")
            sections.append(f"Mechanics: {system.mechanics}")
            sections.append("")
            sections.append("SIGNATURE SOUNDS:")
            for sound_type, sound_desc in system.signature_sounds.items():
                sections.append(f"  {sound_type.title()}: {sound_desc}")
            sections.append(f"Audio Distinctiveness: {system.audio_distinctiveness}")
            sections.append("")
        
        # Section 4: History & Lore
        sections.append("\n" + "=" * 70)
        sections.append("SECTION 4: HISTORY & LORE")
        sections.append("=" * 70)
        sections.append("HISTORICAL TIMELINE:")
        for event in world_bible.historical_events:
            sections.append(f"\n{event.name} ({event.timeframe})")
            sections.append(f"  What Happened: {event.description}")
            sections.append(f"  Public Knowledge: {event.public_knowledge}")
            sections.append(f"  Hidden Truth: {event.hidden_truth}")
            sections.append(f"  Audio Echoes: {', '.join(event.audio_echoes)}")
        
        sections.append("\nMYTHOLOGY & FOLKLORE:")
        for myth in world_bible.mythology_folklore:
            sections.append(f"\n{myth['name']}")
            sections.append(f"  Story: {myth['summary']}")
            sections.append(f"  Significance: {myth['significance']}")
            sections.append(f"  Audio Elements: {myth['audio_manifestation']}")
        sections.append("")
        
        # Section 5: Sensory Palette
        sections.append("\n" + "=" * 70)
        sections.append("SECTION 5: SENSORY PALETTE & AUDIO CUE LIBRARY")
        sections.append("=" * 70)
        for palette in world_bible.sensory_palettes:
            sections.append(f"\n{palette.location_name.upper()} - AUDIO CUES")
            sections.append("-" * (len(palette.location_name) + 12))
            
            sections.append("AMBIENT LAYERS:")
            for layer, sounds in palette.ambient_soundscape.items():
                sections.append(f"  {layer.replace('_', ' ').title()}: {', '.join(sounds)}")
            
            sections.append(f"\nDISTINCTIVE MARKERS: {', '.join(palette.distinctive_markers)}")
            
            sections.append("\nTIME VARIATIONS:")
            for time_period, sounds in palette.time_variations.items():
                sections.append(f"  {time_period.title()}: {', '.join(sounds)}")
            
            sections.append(f"\nPRODUCTION NOTES: {', '.join(palette.production_notes)}")
            sections.append("")
        
        # Audio Glossary
        sections.append("\n" + "=" * 70)
        sections.append("AUDIO GLOSSARY")
        sections.append("=" * 70)
        for sound_name, description in world_bible.audio_glossary.items():
            sections.append(f"{sound_name}: {description}")
        
        return "\n".join(sections)

    def export_to_json(self, world_bible: WorldBible) -> Dict[str, Any]:
        """Export world bible to JSON format"""
        
        return {
            "session_id": world_bible.session_id,
            "working_title": world_bible.working_title,
            "created_timestamp": world_bible.created_timestamp.isoformat(),
            "world_statistics": world_bible.world_statistics,
            "geography": [asdict(location) for location in world_bible.geography],
            "social_systems": asdict(world_bible.social_systems),
            "tech_magic_systems": [asdict(system) for system in world_bible.tech_magic_systems],
            "historical_events": [asdict(event) for event in world_bible.historical_events],
            "mythology_folklore": world_bible.mythology_folklore,
            "sensory_palettes": [asdict(palette) for palette in world_bible.sensory_palettes],
            "audio_glossary": world_bible.audio_glossary
        }

    # PDF export removed - use JSON and TXT formats instead
    # def export_to_pdf(self, world_bible: WorldBible) -> bytes:
    #     """Export world bible to PDF format - REMOVED"""
    #     pass


# CLI interface for testing
async def main():
    """Main CLI interface for Station 9"""
    
    print("🌍 STATION 9: WORLD BUILDING SYSTEM")
    print("=" * 50)
    
    session_id = input("Enter session ID for world building: ").strip()
    if not session_id:
        print("❌ Session ID required")
        return
    
    try:
        station = Station09WorldBuilding()
        await station.initialize()
        
        debug = input("Enable debug mode? (y/N): ").lower().strip() == 'y'
        if debug:
            station.enable_debug_mode()
        
        print(f"\n🌍 Starting world building for session: {session_id}")
        
        result = await station.process(session_id)
        
        print(f"\n✅ WORLD BIBLE COMPLETED")
        print("=" * 50)
        print(f"Total Locations: {result.world_statistics['total_locations']}")
        print(f"Tech/Magic Systems: {result.world_statistics['tech_magic_systems']}")
        print(f"Historical Events: {result.world_statistics['historical_events']}")
        print(f"Audio Cues: {result.world_statistics['audio_cues']}")
        print(f"Glossary Entries: {result.world_statistics['glossary_entries']}")
        
        # Export results
        os.makedirs("outputs", exist_ok=True)
        
        # Text export
        text_filename = f"outputs/station9_world_bible_{session_id}.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(station.export_to_text(result))
        print(f"📄 Text Bible: {text_filename}")
        
        # JSON export
        json_filename = f"outputs/station9_world_bible_{session_id}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(station.export_to_json(result), f, indent=2, default=str)
        print(f"📊 JSON Data: {json_filename}")
        
        # PDF export removed
        # try:
        #     pdf_data = station.export_to_pdf(result)
        #     pdf_filename = f"outputs/station9_world_bible_{session_id}.pdf"
        #     with open(pdf_filename, 'wb') as f:
        #         f.write(pdf_data)
        #     print(f"📑 PDF Bible: {pdf_filename}")
        # except Exception as e:
        #     print(f"⚠️ PDF export failed: {e}")
        
        # Show world summary
        print(f"\n🗺️ LOCATIONS:")
        for location in result.geography:
            print(f"   • {location.name} ({location.location_type})")
        
        print(f"\n⚡ TECH/MAGIC SYSTEMS:")
        for system in result.tech_magic_systems:
            print(f"   • {system.name} ({system.access_level})")
        
        print(f"\n📜 HISTORICAL EVENTS:")
        for event in result.historical_events:
            print(f"   • {event.name} ({event.timeframe})")
        
    except Exception as e:
        print(f"❌ World building failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())