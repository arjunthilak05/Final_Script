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
from app.redis_client import RedisClient
from app.config import Settings

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
            # Load dependencies from previous stations
            dependencies = await self._load_dependencies(session_id)
            
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
                dependencies['working_title'] = dependencies['project_bible'].get('working_title', 'Untitled')
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
            protagonist_names = [char.get('full_name', '') for char in character_bible['tier1_protagonists']]
        
        geography_prompt = f"""
        Create 5-10 KEY LOCATIONS for the audiobook "{working_title}".

        PROJECT CONTEXT:
        Genre: {genre_tone.get('primary_genre', 'Drama')}
        Setting: {world_setting.get('time_period', 'Contemporary')} - {world_setting.get('primary_location', 'Urban')}
        Main Characters: {', '.join(protagonist_names[:3]) if protagonist_names else 'Character-driven story'}

        For EACH location, provide these exact sections:

        **LOCATION [NUMBER]:**
        
        **Name & Type:**
        - Location name
        - Type (residential/commercial/natural/institutional/other)
        
        **Physical Description:**
        - Size and layout
        - Materials and surfaces
        - Lighting and atmosphere
        
        **SONIC SIGNATURE:**
        - Primary ambient sound (constant background)
        - Secondary sounds (frequent but not constant)
        - Unique audio marker (signature sound only here)
        - Acoustic properties (reverb/echo/deadness)
        
        **Travel & Weather:**
        - Travel time to other key locations
        - How weather sounds here
        - Seasonal audio variations
        
        **Emotional & Story Context:**
        - Emotional association (feeling this place evokes)
        - Story significance (why important to plot)
        - Time-of-day sound variations
        
        Generate 6-8 locations that are:
        - AUDIO-DISTINCTIVE (each sounds completely different)
        - STORY-RELEVANT (important to plot and characters)
        - PRODUCTION-READY (clear sound design guidance)
        
        Make each location immediately recognizable by sound alone in an audio drama.
        """
        
        try:
            response = await self.openrouter_agent.generate_response(
                geography_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=3000
            )
            
            locations = await self._parse_geography_response(response)
            
            if self.debug_mode:
                logger.info(f"Generated {len(locations)} locations from LLM response")
                
            return locations
            
        except Exception as e:
            logger.error(f"Failed to generate geography: {e}")
            # Return fallback locations to avoid pipeline failure
            return await self._create_fallback_geography(dependencies)

    async def _parse_geography_response(self, response: str) -> List[LocationProfile]:
        """Parse LLM response into structured LocationProfile objects"""
        
        locations = []
        
        # Split response into location sections
        location_sections = re.split(r'\*\*LOCATION \d+:\*\*', response)
        
        for i, section in enumerate(location_sections[1:], 1):  # Skip first empty section
            try:
                # Extract location name
                name_match = re.search(r'Location name[:\s]*([^\n]+)', section, re.IGNORECASE)
                name = name_match.group(1).strip() if name_match else f"Location {i}"
                
                # Extract type
                type_match = re.search(r'Type[:\s]*\(([^)]+)\)', section, re.IGNORECASE)
                location_type = type_match.group(1).strip() if type_match else "general"
                
                # Extract physical description
                phys_desc = self._extract_section(section, "Physical Description", "Location description")
                
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
                # Create minimal location to avoid failure
                locations.append(await self._create_fallback_location(i))
        
        # Ensure we have at least 5 locations
        while len(locations) < 5:
            locations.append(await self._create_fallback_location(len(locations) + 1))
        
        return locations[:10]  # Max 10 locations

    def _extract_section(self, text: str, keyword: str, fallback: str) -> str:
        """Extract a section from LLM response"""
        # Look for the keyword followed by content
        pattern = rf'{re.escape(keyword)}[:\s]*([^\n]*(?:\n(?![\*\-])[^\n]*)*)'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            content = match.group(1).strip()
            return content if content else fallback
        return fallback

    async def _create_fallback_location(self, index: int) -> LocationProfile:
        """Create fallback location when parsing fails"""
        
        return LocationProfile(
            name=f"Location {index}",
            location_type="general",
            physical_description=f"Important location {index} in the story",
            sonic_signature={
                "primary_ambient": f"Characteristic ambient sound for location {index}",
                "secondary_sounds": f"Secondary audio elements for location {index}",
                "unique_marker": f"Distinctive sound marker for location {index}",
                "acoustic_properties": f"Acoustic characteristics for location {index}"
            },
            travel_times={"other_locations": "Variable travel time"},
            weather_patterns={
                "rain": f"Rain sounds at location {index}",
                "wind": f"Wind patterns at location {index}",
                "clear": f"Clear weather at location {index}"
            },
            acoustic_properties={
                "reverb": "Natural reverb",
                "echo": "Echo characteristics",
                "absorption": "Sound absorption"
            },
            emotional_association=f"Emotional context for location {index}",
            story_significance=f"Narrative importance of location {index}",
            time_variations={
                "morning": f"Morning audio at location {index}",
                "afternoon": f"Afternoon sounds at location {index}",
                "evening": f"Evening atmosphere at location {index}",
                "night": f"Night audio at location {index}"
            }
        )

    async def _create_fallback_geography(self, dependencies: Dict[str, Any]) -> List[LocationProfile]:
        """Create fallback geography when LLM generation fails"""
        
        locations = []
        for i in range(6):  # Create 6 fallback locations
            locations.append(await self._create_fallback_location(i + 1))
        
        return locations

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
            response = await self.openrouter_agent.generate_response(
                social_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=2500
            )
            
            social_system = await self._parse_social_systems_response(response)
            
            if self.debug_mode:
                logger.info("Generated social systems with audio manifestations")
                
            return social_system
            
        except Exception as e:
            logger.error(f"Failed to generate social systems: {e}")
            return await self._create_fallback_social_system()

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
            return await self._create_fallback_social_system()

    def _extract_list(self, text: str, keyword: str, fallback: List[str]) -> List[str]:
        """Extract a list from LLM response"""
        section = self._extract_section(text, keyword, "")
        if section:
            # Look for bullet points or numbered items
            items = re.findall(r'[-•*]\s*([^\n]+)', section)
            if not items:
                items = re.findall(r'\d+\.\s*([^\n]+)', section)
            if not items:
                # Split by commas or semicolons
                items = [item.strip() for item in re.split(r'[,;]', section) if item.strip()]
            return items[:10] if items else fallback
        return fallback

    async def _create_fallback_social_system(self) -> SocialSystem:
        """Create fallback social system"""
        
        return SocialSystem(
            government_structure="Social governance system",
            authority_sounds=["Authority speech patterns", "Official language"],
            economic_system="Economic structure and trade",
            class_divisions=[
                {"level": "Upper", "description": "Upper class characteristics"},
                {"level": "Middle", "description": "Middle class characteristics"},
                {"level": "Lower", "description": "Lower class characteristics"}
            ],
            social_hierarchies={
                "formal_hierarchy": "Official social structure",
                "informal_power": "Unofficial networks",
                "address_patterns": "Speech patterns by rank"
            },
            cultural_norms=["Social customs", "Cultural practices"],
            audio_manifestations={
                "class_accents": ["Upper speech", "Middle speech", "Lower speech"],
                "formality_markers": ["Formal patterns", "Informal speech"],
                "status_indicators": ["Authority cues", "Deference markers"]
            },
            dialogue_formality={
                "superior_to_subordinate": "Formal, direct",
                "subordinate_to_superior": "Respectful, deferential",
                "peer_to_peer": "Casual, familiar",
                "stranger_to_stranger": "Polite, reserved"
            }
        )

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
            response = await self.openrouter_agent.generate_response(
                tech_magic_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=2500
            )
            
            systems = await self._parse_tech_magic_response(response)
            
            if self.debug_mode:
                logger.info(f"Generated {len(systems)} tech/magic systems")
                
            return systems
            
        except Exception as e:
            logger.error(f"Failed to generate tech/magic systems: {e}")
            return await self._create_fallback_tech_magic()

    async def _parse_tech_magic_response(self, response: str) -> List[TechMagicSystem]:
        """Parse tech/magic response into structured systems"""
        
        systems = []
        
        # Split response into system sections
        system_sections = re.split(r'\*\*SYSTEM \d+:\*\*', response)
        
        for i, section in enumerate(system_sections[1:], 1):  # Skip first empty section
            try:
                # Extract system name
                name_match = re.search(r'System name[:\s]*([^\n]+)', section, re.IGNORECASE)
                name = name_match.group(1).strip() if name_match else f"System {i}"
                
                # Extract description
                description = self._extract_section(section, "What it does", f"Technology/magic system {i}")
                
                # Extract access level
                access_match = re.search(r'Access level[:\s]*\(([^)]+)\)', section, re.IGNORECASE)
                access_level = access_match.group(1).strip() if access_match else "common"
                
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
                systems.append(await self._create_fallback_tech_magic_system(i))
        
        # Ensure we have at least 3 systems
        while len(systems) < 3:
            systems.append(await self._create_fallback_tech_magic_system(len(systems) + 1))
        
        return systems[:8]  # Max 8 systems

    async def _create_fallback_tech_magic_system(self, index: int) -> TechMagicSystem:
        """Create fallback tech/magic system"""
        
        return TechMagicSystem(
            name=f"System {index}",
            description=f"Technology or magic system {index}",
            mechanics=f"Mechanics for system {index}",
            access_level="common",
            signature_sounds={
                "activation": f"Activation sound for system {index}",
                "operation": f"Operation sound for system {index}",
                "completion": f"Completion sound for system {index}",
                "malfunction": f"Malfunction sound for system {index}"
            },
            limitations=[f"Limitation for system {index}"],
            narrative_function=f"Narrative purpose of system {index}",
            audio_distinctiveness=f"Unique audio signature for system {index}"
        )

    async def _create_fallback_tech_magic(self) -> List[TechMagicSystem]:
        """Create fallback tech/magic systems"""
        
        systems = []
        for i in range(4):  # Create 4 fallback systems
            systems.append(await self._create_fallback_tech_magic_system(i + 1))
        
        return systems

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
            response = await self.openrouter_agent.generate_response(
                history_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=2500
            )
            
            events, mythology = await self._parse_history_lore_response(response)
            
            if self.debug_mode:
                logger.info(f"Generated {len(events)} historical events and {len(mythology)} mythology entries")
                
            return events, mythology
            
        except Exception as e:
            logger.error(f"Failed to generate history/lore: {e}")
            return await self._create_fallback_history_lore()

    async def _parse_history_lore_response(self, response: str) -> tuple[List[HistoricalEvent], List[Dict[str, str]]]:
        """Parse history/lore response into structured data"""
        
        events = []
        mythology = []
        
        try:
            # Extract historical events
            # Look for patterns like "Event name:"
            event_patterns = re.findall(r'[-•*]\s*([^:\n]+):\s*([^\n]+)', response)
            
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
            
            # Extract mythology
            mythology_section = self._extract_section(response, "MYTHOLOGY", "")
            if mythology_section:
                myth_patterns = re.findall(r'[-•*]\s*([^:\n]+)', mythology_section)
                for myth_name in myth_patterns[:4]:  # Max 4 myths
                    mythology.append({
                        "name": myth_name.strip(),
                        "summary": f"Folklore about {myth_name}",
                        "significance": f"Cultural importance of {myth_name}",
                        "audio_manifestation": f"Audio ritual related to {myth_name}"
                    })
            
            # Ensure minimum content
            if len(events) < 3:
                events.extend(await self._create_fallback_events(3 - len(events)))
            
            if len(mythology) < 2:
                mythology.extend(await self._create_fallback_mythology(2 - len(mythology)))
                
            return events, mythology
            
        except Exception as e:
            logger.error(f"Failed to parse history/lore: {e}")
            return await self._create_fallback_history_lore()

    async def _create_fallback_events(self, count: int) -> List[HistoricalEvent]:
        """Create fallback historical events"""
        
        events = []
        for i in range(count):
            event = HistoricalEvent(
                name=f"Historical Event {i + 1}",
                timeframe=f"Past era {i + 1}",
                description=f"Important historical event {i + 1}",
                consequences=f"Consequences of event {i + 1}",
                public_knowledge=f"Public knowledge of event {i + 1}",
                hidden_truth=f"Hidden truth about event {i + 1}",
                audio_echoes=[f"Audio echo of event {i + 1}"]
            )
            events.append(event)
        
        return events

    async def _create_fallback_mythology(self, count: int) -> List[Dict[str, str]]:
        """Create fallback mythology"""
        
        mythology = []
        for i in range(count):
            mythology.append({
                "name": f"Legend {i + 1}",
                "summary": f"Folklore story {i + 1}",
                "significance": f"Cultural importance {i + 1}",
                "audio_manifestation": f"Audio ritual {i + 1}"
            })
        
        return mythology

    async def _create_fallback_history_lore(self) -> tuple[List[HistoricalEvent], List[Dict[str, str]]]:
        """Create fallback history and lore"""
        
        events = await self._create_fallback_events(4)
        mythology = await self._create_fallback_mythology(3)
        
        return events, mythology

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
                response = await self.openrouter_agent.generate_response(
                    sensory_prompt,
                    model="anthropic/claude-3-sonnet",
                    max_tokens=2000
                )
                
                palette = await self._parse_sensory_palette_response(response, location.name)
                palettes.append(palette)
                
            except Exception as e:
                logger.error(f"Failed to generate sensory palette for {location.name}: {e}")
                palettes.append(await self._create_fallback_sensory_palette(location.name))
        
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
            return await self._create_fallback_sensory_palette(location_name)

    async def _create_fallback_sensory_palette(self, location_name: str) -> SensoryPalette:
        """Create fallback sensory palette"""
        
        return SensoryPalette(
            location_name=location_name,
            ambient_soundscape={
                "base_layer": [f"Base ambience for {location_name}"],
                "mid_layer": [f"Environmental sounds at {location_name}"],
                "top_layer": [f"Occasional sounds at {location_name}"],
                "silence_points": [f"Quiet moments at {location_name}"]
            },
            distinctive_markers=[f"Signature sound of {location_name}"],
            acoustic_properties={
                "reverb": f"Reverb characteristics of {location_name}",
                "echo": f"Echo patterns at {location_name}",
                "absorption": f"Sound absorption at {location_name}"
            },
            time_variations={
                "morning": [f"Morning sounds at {location_name}"],
                "afternoon": [f"Afternoon audio at {location_name}"],
                "evening": [f"Evening atmosphere at {location_name}"],
                "night": [f"Night sounds at {location_name}"]
            },
            emotional_palette={
                "calm": [f"Peaceful sounds of {location_name}"],
                "tense": [f"Tension audio at {location_name}"],
                "mysterious": [f"Mystery elements of {location_name}"],
                "comforting": [f"Comforting sounds at {location_name}"]
            },
            recurring_motifs=[f"Audio leitmotif for {location_name}"],
            production_notes=[f"Production guidance for {location_name}"]
        )

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
            response = await self.openrouter_agent.generate_response(
                glossary_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=2500
            )
            
            glossary = await self._parse_audio_glossary_response(response)
            
            if self.debug_mode:
                logger.info(f"Generated audio glossary with {len(glossary)} entries")
                
            return glossary
            
        except Exception as e:
            logger.error(f"Failed to generate audio glossary: {e}")
            return await self._create_fallback_glossary()

    async def _parse_audio_glossary_response(self, response: str) -> Dict[str, str]:
        """Parse audio glossary response"""
        
        glossary = {}
        
        try:
            # Look for entries in format "**Sound Name**: Description"
            entries = re.findall(r'\*\*([^:]+)\*\*:\s*([^\n]+(?:\n(?!\*\*)[^\n]*)*)', response)
            
            for sound_name, description in entries:
                clean_name = sound_name.strip()
                clean_description = description.strip()
                if clean_name and clean_description:
                    glossary[clean_name] = clean_description
            
            # If not enough entries, add some fallback ones
            if len(glossary) < 10:
                fallback_entries = await self._create_fallback_glossary()
                glossary.update(fallback_entries)
                
            return glossary
            
        except Exception as e:
            logger.error(f"Failed to parse audio glossary: {e}")
            return await self._create_fallback_glossary()

    async def _create_fallback_glossary(self) -> Dict[str, str]:
        """Create fallback audio glossary"""
        
        return {
            "Ambient Base": "Constant background audio layer that establishes location",
            "Signature Sound": "Unique audio marker that identifies specific location",
            "Authority Voice": "Formal speech pattern indicating rank or status",
            "System Activation": "Audio cue when technology or magic engages",
            "Historical Echo": "Sound that references past events",
            "Cultural Marker": "Audio element indicating social customs",
            "Emotional Cue": "Sound that conveys character emotional state",
            "Transition Audio": "Sound indicating movement between locations",
            "Status Indicator": "Audio marker of social or economic position",
            "Mystery Element": "Ambiguous sound that creates intrigue"
        }

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

    def export_to_pdf(self, world_bible: WorldBible) -> bytes:
        """Export world bible to PDF format"""
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from io import BytesIO
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontSize=24,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=30,
                alignment=1  # Center
            )
            
            section_style = ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#34495E'),
                spaceAfter=12
            )
            
            # Title page
            story.append(Paragraph("WORLD BIBLE", title_style))
            story.append(Paragraph("Audio Drama World Building", styles['Heading2']))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Project: {world_bible.working_title}", styles['Normal']))
            story.append(Paragraph(f"Session: {world_bible.session_id}", styles['Normal']))
            story.append(Paragraph(f"Generated: {world_bible.created_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(PageBreak())
            
            # Statistics overview
            story.append(Paragraph("WORLD STATISTICS", section_style))
            stats_data = [
                ['Metric', 'Count'],
                ['Total Locations', str(world_bible.world_statistics['total_locations'])],
                ['Tech/Magic Systems', str(world_bible.world_statistics['tech_magic_systems'])],
                ['Historical Events', str(world_bible.world_statistics['historical_events'])],
                ['Audio Cues', str(world_bible.world_statistics['audio_cues'])],
                ['Glossary Entries', str(world_bible.world_statistics['glossary_entries'])]
            ]
            
            stats_table = Table(stats_data)
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
            story.append(PageBreak())
            
            # Section 1: Geography
            story.append(Paragraph("SECTION 1: GEOGRAPHY & SPACES", section_style))
            for location in world_bible.geography:
                story.append(Paragraph(f"{location.name} ({location.location_type})", styles['Heading3']))
                story.append(Paragraph(f"<b>Description:</b> {location.physical_description}", styles['Normal']))
                story.append(Paragraph(f"<b>Sonic Signature:</b> {location.sonic_signature.get('primary_ambient', 'N/A')}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            story.append(PageBreak())
            
            # Section 2: Social Systems
            story.append(Paragraph("SECTION 2: SOCIAL SYSTEMS", section_style))
            story.append(Paragraph(f"<b>Government:</b> {world_bible.social_systems.government_structure}", styles['Normal']))
            story.append(Paragraph(f"<b>Economy:</b> {world_bible.social_systems.economic_system}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Section 3: Technology/Magic
            story.append(Paragraph("SECTION 3: TECHNOLOGY & MAGIC", section_style))
            for system in world_bible.tech_magic_systems:
                story.append(Paragraph(f"{system.name} ({system.access_level})", styles['Heading3']))
                story.append(Paragraph(f"<b>Description:</b> {system.description}", styles['Normal']))
                story.append(Paragraph(f"<b>Audio Signature:</b> {system.audio_distinctiveness}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            story.append(PageBreak())
            
            # Audio Glossary
            story.append(Paragraph("AUDIO GLOSSARY", section_style))
            glossary_data = [['Sound', 'Description']]
            for sound_name, description in list(world_bible.audio_glossary.items())[:20]:  # Limit for PDF space
                glossary_data.append([sound_name, description[:100] + "..." if len(description) > 100 else description])
            
            glossary_table = Table(glossary_data, colWidths=[2*inch, 4*inch])
            glossary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            story.append(glossary_table)
            
            # Build PDF
            doc.build(story)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return pdf_data
            
        except ImportError:
            logger.warning("ReportLab not available for PDF generation")
            return self.export_to_text(world_bible).encode('utf-8')
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return self.export_to_text(world_bible).encode('utf-8')


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
        
        # PDF export
        try:
            pdf_data = station.export_to_pdf(result)
            pdf_filename = f"outputs/station9_world_bible_{session_id}.pdf"
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_data)
            print(f"📑 PDF Bible: {pdf_filename}")
        except Exception as e:
            print(f"⚠️ PDF export failed: {e}")
        
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