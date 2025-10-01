#!/usr/bin/env python3
"""
Station 8: Character Architecture Agent for Audiobook Production

This station creates a comprehensive 3-tier character system for audio drama production.
Generates full character bibles with voice signatures, relationships, and audio identification markers.

Dependencies: Station 2 (Project Bible), Station 4 (Seed Bank), Station 6 (Style Guide)
Outputs: Character Bible with TXT, JSON, and PDF exports
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
class VoiceSignature:
    """Detailed voice signature for audio identification"""
    pitch_range: str  # "Low baritone (80-150 Hz)", "High soprano (250-400 Hz)"
    pace_pattern: str  # "Rapid-fire (180 WPM)", "Deliberate (100 WPM)"
    vocabulary_level: str  # "Graduate education", "Street vernacular"
    accent_details: str  # "Slight Southern drawl", "Brooklyn native"
    verbal_tics: List[str]  # ["clears throat before important points", "says 'listen' frequently"]
    catchphrases: List[str]  # Unique phrases this character uses
    emotional_baseline: str  # "Cautiously optimistic", "Perpetually anxious"

@dataclass
class AudioMarkers:
    """How to identify character in audio-only format"""
    voice_identification: str  # Primary way listeners identify this character
    sound_associations: List[str]  # Background sounds, props, environments
    speech_rhythm: str  # Unique rhythm or cadence
    breathing_pattern: str  # "Deep sighs when frustrated", "Sharp intake when surprised"
    signature_sounds: List[str]  # Non-verbal sounds they make

@dataclass
class CharacterRelationship:
    """Relationship between two characters"""
    character_name: str
    relationship_type: str  # "romantic partner", "bitter rival", "protective mentor"
    dynamic_description: str  # How they interact
    conflict_potential: str  # Sources of tension
    growth_arc: str  # How relationship evolves

@dataclass
class CharacterArc:
    """Character development across episodes"""
    starting_point: str  # Where character begins
    key_transformations: List[str]  # Major character changes
    revelation_timeline: List[Dict[str, str]]  # {"episode": "3", "revelation": "secret identity"}
    ending_point: str  # Where character ends up
    thematic_purpose: str  # Character's role in overall themes

@dataclass
class Tier1Character:
    """Protagonist character with full development"""
    full_name: str
    age: str
    psychological_profile: str
    backstory: str
    core_desires: List[str]
    deepest_fears: List[str]
    secrets: List[Dict[str, str]]  # {"secret": "...", "reveal_timing": "..."}
    voice_signature: VoiceSignature
    audio_markers: AudioMarkers
    character_arc: CharacterArc
    relationships: List[CharacterRelationship]
    sample_dialogue: List[str]  # 3-5 dialogue examples showing voice

@dataclass
class Tier2Character:
    """Major supporting character"""
    full_name: str
    age: str
    role_in_story: str
    personality_summary: str
    relevant_backstory: str
    voice_signature: VoiceSignature
    audio_markers: AudioMarkers
    character_function: str  # Their purpose in the narrative
    episode_appearances: List[str]
    relationships: List[CharacterRelationship]
    sample_dialogue: List[str]

@dataclass
class Tier3Character:
    """Recurring character"""
    name: str
    defining_trait: str
    voice_hook: str  # Quick way to identify in audio
    narrative_function: str
    episode_appearances: List[str]
    memorable_quirk: str
    sample_line: str  # One memorable line showing their voice

@dataclass
class CharacterBible:
    """Complete character architecture output"""
    session_id: str
    working_title: str
    created_timestamp: datetime
    tier1_protagonists: List[Tier1Character]
    tier2_supporting: List[Tier2Character]
    tier3_recurring: List[Tier3Character]
    character_count_summary: Dict[str, int]
    voice_sample_collection: Dict[str, str]
    relationship_matrix: Dict[str, List[str]]
    audio_identification_guide: str
    casting_notes: str

class Station08CharacterArchitecture:
    """Station 8: Character Architecture Generator"""
    
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
            
            logger.info("✅ Station 8 Character Architecture initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Station 8: {e}")
            raise

    def enable_debug_mode(self):
        """Enable debug mode for detailed logging"""
        self.debug_mode = True
        logger.info("🐛 Debug mode enabled for Station 8")

    async def process(self, session_id: str) -> CharacterBible:
        """Main processing function for Station 8"""
        
        logger.info(f"🎭 Station 8: Starting Character Architecture for session {session_id}")
        
        try:
            # Load dependencies from previous stations
            dependencies = await self._load_dependencies(session_id)
            
            logger.info("📚 Loaded project dependencies from previous stations")
            
            # Generate Tier 1 protagonists (1-3 characters)
            tier1_characters = await self._generate_tier1_protagonists(dependencies)
            logger.info(f"✅ Generated {len(tier1_characters)} Tier 1 protagonists")
            
            # Generate Tier 2 supporting characters (3-5 characters)
            tier2_characters = await self._generate_tier2_supporting(dependencies, tier1_characters)
            logger.info(f"✅ Generated {len(tier2_characters)} Tier 2 supporting characters")
            
            # Generate Tier 3 recurring characters (5-10 characters)
            tier3_characters = await self._generate_tier3_recurring(dependencies, tier1_characters)
            logger.info(f"✅ Generated {len(tier3_characters)} Tier 3 recurring characters")
            
            # Generate character relationships
            relationship_matrix = await self._generate_character_relationships(
                tier1_characters, tier2_characters, dependencies
            )
            logger.info("✅ Generated character relationship matrix")
            
            # Generate voice sample collection
            voice_samples = await self._generate_voice_sample_collection(
                tier1_characters, tier2_characters, tier3_characters
            )
            logger.info("✅ Generated voice sample collection")
            
            # Generate audio identification guide
            audio_guide = await self._generate_audio_identification_guide(
                tier1_characters, tier2_characters, tier3_characters
            )
            logger.info("✅ Generated audio identification guide")
            
            # Generate casting notes
            casting_notes = await self._generate_casting_notes(
                tier1_characters, tier2_characters, dependencies
            )
            logger.info("✅ Generated casting and production notes")
            
            # Compile character bible
            character_bible = CharacterBible(
                session_id=session_id,
                working_title=dependencies.get('working_title', 'Untitled Project'),
                created_timestamp=datetime.now(),
                tier1_protagonists=tier1_characters,
                tier2_supporting=tier2_characters,
                tier3_recurring=tier3_characters,
                character_count_summary={
                    "tier1_protagonists": len(tier1_characters),
                    "tier2_supporting": len(tier2_characters),
                    "tier3_recurring": len(tier3_characters),
                    "total_characters": len(tier1_characters) + len(tier2_characters) + len(tier3_characters)
                },
                voice_sample_collection=voice_samples,
                relationship_matrix=relationship_matrix,
                audio_identification_guide=audio_guide,
                casting_notes=casting_notes
            )
            
            logger.info(f"✅ Station 8 completed: {character_bible.character_count_summary['total_characters']} characters created")
            return character_bible
            
        except Exception as e:
            logger.error(f"❌ Station 8 failed: {e}")
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
                
            # Load Station 4: Seed Bank
            seed_bank_key = f"audiobook:{session_id}:station_04"
            seed_bank_data = await self.redis_client.get(seed_bank_key)
            if seed_bank_data:
                dependencies['seed_bank'] = json.loads(seed_bank_data)
                logger.info("✅ Loaded Seed Bank from Station 4")
            else:
                logger.warning("⚠️ No Seed Bank found from Station 4")
                
            # Load Station 6: Style Guide
            style_guide_key = f"audiobook:{session_id}:station_06"
            style_guide_data = await self.redis_client.get(style_guide_key)
            if style_guide_data:
                dependencies['style_guide'] = json.loads(style_guide_data)
                logger.info("✅ Loaded Style Guide from Station 6")
            else:
                logger.warning("⚠️ No Style Guide found from Station 6")
                
            return dependencies
            
        except Exception as e:
            logger.error(f"❌ Failed to load dependencies: {e}")
            raise

    async def _generate_tier1_protagonists(self, dependencies: Dict[str, Any]) -> List[Tier1Character]:
        """Generate 1-3 protagonist characters with full LLM development"""
        
        # Determine number of protagonists based on project scope
        project_bible = dependencies.get('project_bible', {})
        scope_indicators = project_bible.get('format_specifications', {})
        
        # Determine protagonist count based on project complexity
        if isinstance(scope_indicators, dict):
            episode_count = scope_indicators.get('episode_count', '6')
            if isinstance(episode_count, str) and 'episode' in episode_count.lower():
                try:
                    num_episodes = int(re.search(r'\d+', episode_count).group())
                    protagonist_count = 1 if num_episodes <= 6 else 2 if num_episodes <= 12 else 3
                except:
                    protagonist_count = 2
            else:
                protagonist_count = 2
        else:
            protagonist_count = 2
        
        protagonists = []
        
        for i in range(protagonist_count):
            protagonist_prompt = self._build_protagonist_prompt(dependencies, i + 1, protagonist_count)
            
            try:
                response = await self.openrouter_agent.generate_response(
                    protagonist_prompt,
                    model="anthropic/claude-3-sonnet",
                    max_tokens=2000
                )
                
                protagonist = await self._parse_protagonist_response(response, dependencies)
                protagonists.append(protagonist)
                
                if self.debug_mode:
                    logger.info(f"Generated protagonist {i + 1}: {protagonist.full_name}")
                    
            except Exception as e:
                logger.error(f"Failed to generate protagonist {i + 1}: {e}")
                # Create a minimal protagonist to avoid pipeline failure
                protagonists.append(await self._create_fallback_protagonist(dependencies, i + 1))
        
        return protagonists

    def _build_protagonist_prompt(self, dependencies: Dict[str, Any], protagonist_num: int, total_protagonists: int) -> str:
        """Build detailed prompt for protagonist generation"""
        
        project_bible = dependencies.get('project_bible', {})
        style_guide = dependencies.get('style_guide', {})
        seed_bank = dependencies.get('seed_bank', {})
        
        # Extract key context
        working_title = project_bible.get('working_title', 'Untitled Project')
        genre_tone = project_bible.get('genre_tone', {})
        world_setting = project_bible.get('world_setting', {})
        audience_profile = project_bible.get('audience_profile', {})
        
        prompt = f"""
        Create PROTAGONIST {protagonist_num} of {total_protagonists} for the audiobook project "{working_title}".

        PROJECT CONTEXT:
        Genre: {genre_tone.get('primary_genre', 'Drama')}
        Setting: {world_setting.get('time_period', 'Contemporary')} - {world_setting.get('primary_location', 'Urban')}
        Audience: {audience_profile.get('primary_demographic', 'Adult')}
        Tone: {genre_tone.get('emotional_tone', 'Balanced')}

        STYLE REQUIREMENTS:
        Language Level: {style_guide.get('language_rules_complete', 'Accessible')}
        Audio Format: This is for audio-only drama - every detail must work in pure audio

        Generate a complete TIER 1 PROTAGONIST with these exact sections:

        **BASIC INFO:**
        - Full name (first and last)
        - Age (specific number)
        - One-sentence character essence

        **PSYCHOLOGICAL PROFILE:**
        - Core personality traits (3-4 key characteristics)
        - Educational/professional background
        - Major life trauma or defining moment
        - Current life situation and challenges

        **VOICE SIGNATURE:**
        - Pitch range (specific: "Mid-baritone 120-180 Hz" or "High tenor 200-300 Hz")
        - Speaking pace (specific WPM: "Rapid 160 WPM" or "Deliberate 90 WPM")
        - Vocabulary level ("PhD education" or "High school dropout" etc.)
        - Accent/regional details ("Midwest neutral" or "Boston working-class")
        - 3 verbal tics (throat clearing, word repetition, specific phrases)
        - 2 catchphrases unique to this character

        **AUDIO IDENTIFICATION:**
        - Primary voice identifier (how listeners know it's them instantly)
        - 2 sound associations (environments, props, background noise)
        - Breathing/rhythm pattern ("sighs before difficult topics")
        - 2 signature non-verbal sounds they make

        **CHARACTER ARC:**
        - Starting emotional/psychological state
        - 3 major transformation points across the series
        - What they learn/how they change
        - Final state by series end

        **DESIRES & FEARS:**
        - 2 core desires (what drives them)
        - 2 deepest fears (what terrifies them)
        - 1 secret they're hiding (with when it gets revealed)

        **SAMPLE DIALOGUE:**
        Write 3 short dialogue examples (2-3 sentences each) that demonstrate this character's unique voice, vocabulary, and speech patterns. Show their personality through word choice and rhythm.

        Make this character:
        - Unique and memorable for audio identification
        - Complex with realistic psychological depth  
        - Perfectly suited to the project's genre and tone
        - Audio-drama optimized (every detail must work in pure sound)

        NO generic templates. This must be original and specific to this project.
        """
        
        return prompt

    async def _parse_protagonist_response(self, response: str, dependencies: Dict[str, Any]) -> Tier1Character:
        """Parse LLM response into structured Tier1Character"""
        
        # Extract information from response using pattern matching
        # This is a simplified parser - in production, you'd want more robust parsing
        
        try:
            # Extract basic info
            name_match = re.search(r'Full name[:\s]*([^\n]+)', response, re.IGNORECASE)
            full_name = name_match.group(1).strip() if name_match else "Generated Character"
            
            age_match = re.search(r'Age[:\s]*(\d+)', response, re.IGNORECASE)
            age = age_match.group(1) if age_match else "30"
            
            # Extract voice signature components
            pitch_match = re.search(r'Pitch range[:\s]*([^\n]+)', response, re.IGNORECASE)
            pitch_range = pitch_match.group(1).strip() if pitch_match else "Mid-range vocal tone"
            
            pace_match = re.search(r'Speaking pace[:\s]*([^\n]+)', response, re.IGNORECASE)
            pace_pattern = pace_match.group(1).strip() if pace_match else "Moderate speaking pace"
            
            # Extract dialogue samples
            dialogue_matches = re.findall(r'"([^"]*)"', response)
            sample_dialogue = dialogue_matches[:3] if dialogue_matches else [
                "Sample dialogue generated for this character.",
                "Another line showing their speaking style.",
                "A third example of their voice."
            ]
            
            # Create voice signature
            voice_signature = VoiceSignature(
                pitch_range=pitch_range,
                pace_pattern=pace_pattern,
                vocabulary_level=self._extract_section(response, "vocabulary level", "Educated speech patterns"),
                accent_details=self._extract_section(response, "accent", "Neutral accent"),
                verbal_tics=self._extract_list(response, "verbal tics", ["Unique speech pattern", "Characteristic pause"]),
                catchphrases=self._extract_list(response, "catchphrases", ["Signature phrase"]),
                emotional_baseline=self._extract_section(response, "emotional", "Balanced emotional state")
            )
            
            # Create audio markers
            audio_markers = AudioMarkers(
                voice_identification=self._extract_section(response, "voice identifier", "Distinctive vocal quality"),
                sound_associations=self._extract_list(response, "sound associations", ["Associated environment"]),
                speech_rhythm=self._extract_section(response, "rhythm", "Natural speech rhythm"),
                breathing_pattern=self._extract_section(response, "breathing", "Normal breathing pattern"),
                signature_sounds=self._extract_list(response, "signature.*sounds", ["Characteristic sound"])
            )
            
            # Create character arc
            character_arc = CharacterArc(
                starting_point=self._extract_section(response, "starting.*state", "Initial character state"),
                key_transformations=self._extract_list(response, "transformation", ["Character development"]),
                revelation_timeline=[{"episode": "TBD", "revelation": "Character secret"}],
                ending_point=self._extract_section(response, "final.*state", "Character resolution"),
                thematic_purpose="Central character development"
            )
            
            # Create protagonist
            protagonist = Tier1Character(
                full_name=full_name,
                age=age,
                psychological_profile=self._extract_section(response, "psychological", "Complex character psychology"),
                backstory=self._extract_section(response, "background", "Character background"),
                core_desires=self._extract_list(response, "desires", ["Primary motivation"]),
                deepest_fears=self._extract_list(response, "fears", ["Core fear"]),
                secrets=[{"secret": self._extract_section(response, "secret", "Hidden aspect"), "reveal_timing": "Mid-series"}],
                voice_signature=voice_signature,
                audio_markers=audio_markers,
                character_arc=character_arc,
                relationships=[],  # Will be populated later
                sample_dialogue=sample_dialogue
            )
            
            return protagonist
            
        except Exception as e:
            logger.error(f"Failed to parse protagonist response: {e}")
            return await self._create_fallback_protagonist(dependencies, 1)

    def _extract_section(self, text: str, keyword: str, fallback: str) -> str:
        """Extract a section from LLM response"""
        pattern = rf'{keyword}[:\s]*([^\n]*(?:\n(?![\*\-])[^\n]*)*)'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
        return fallback

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
            return items[:5] if items else fallback
        return fallback

    async def _create_fallback_protagonist(self, dependencies: Dict[str, Any], protagonist_num: int) -> Tier1Character:
        """Create minimal protagonist when LLM generation fails"""
        
        working_title = dependencies.get('project_bible', {}).get('working_title', 'Untitled')
        
        return Tier1Character(
            full_name=f"Protagonist {protagonist_num}",
            age="30",
            psychological_profile="Complex character with depth and development needs",
            backstory="Rich background that informs character motivations",
            core_desires=["Character goal needs definition"],
            deepest_fears=["Character fear needs development"],
            secrets=[{"secret": "Character secret to be revealed", "reveal_timing": "Mid-series"}],
            voice_signature=VoiceSignature(
                pitch_range="Mid-range vocal tone",
                pace_pattern="Natural speaking pace",
                vocabulary_level="Educated speech",
                accent_details="Neutral accent",
                verbal_tics=["Needs vocal tic development"],
                catchphrases=["Signature phrase needed"],
                emotional_baseline="Balanced"
            ),
            audio_markers=AudioMarkers(
                voice_identification="Distinctive voice needed",
                sound_associations=["Environment association needed"],
                speech_rhythm="Natural rhythm",
                breathing_pattern="Normal breathing",
                signature_sounds=["Signature sound needed"]
            ),
            character_arc=CharacterArc(
                starting_point="Character starting point",
                key_transformations=["Transformation needed"],
                revelation_timeline=[{"episode": "TBD", "revelation": "Secret reveal"}],
                ending_point="Character resolution",
                thematic_purpose="Thematic role development needed"
            ),
            relationships=[],
            sample_dialogue=["Sample dialogue needed", "Voice demonstration required", "Character speech example"]
        )

    async def _generate_tier2_supporting(self, dependencies: Dict[str, Any], tier1_characters: List[Tier1Character]) -> List[Tier2Character]:
        """Generate 3-5 major supporting characters"""
        
        # Determine supporting character count (3-5 based on project scope)
        project_bible = dependencies.get('project_bible', {})
        protagonist_count = len(tier1_characters)
        supporting_count = min(5, max(3, protagonist_count + 2))
        
        supporting_characters = []
        
        for i in range(supporting_count):
            supporting_prompt = self._build_supporting_prompt(dependencies, tier1_characters, i + 1)
            
            try:
                response = await self.openrouter_agent.generate_response(
                    supporting_prompt,
                    model="anthropic/claude-3-sonnet",
                    max_tokens=1500
                )
                
                supporting_char = await self._parse_supporting_response(response, dependencies)
                supporting_characters.append(supporting_char)
                
                if self.debug_mode:
                    logger.info(f"Generated supporting character {i + 1}: {supporting_char.full_name}")
                    
            except Exception as e:
                logger.error(f"Failed to generate supporting character {i + 1}: {e}")
                supporting_characters.append(await self._create_fallback_supporting(dependencies, i + 1))
        
        return supporting_characters

    def _build_supporting_prompt(self, dependencies: Dict[str, Any], protagonists: List[Tier1Character], char_num: int) -> str:
        """Build prompt for supporting character generation"""
        
        project_bible = dependencies.get('project_bible', {})
        working_title = project_bible.get('working_title', 'Untitled Project')
        
        protagonist_names = [p.full_name for p in protagonists]
        
        prompt = f"""
        Create SUPPORTING CHARACTER {char_num} for the audiobook "{working_title}".

        EXISTING PROTAGONISTS: {', '.join(protagonist_names)}

        This is a TIER 2 MAJOR SUPPORTING character who:
        - Appears in multiple episodes
        - Has significant interactions with protagonists
        - Drives important plot points
        - Has their own character arc

        Generate with these sections:

        **BASIC INFO:**
        - Full name
        - Age
        - Role in the story (how they connect to protagonists)

        **CHARACTER FUNCTION:**
        - Their purpose in the narrative
        - How they challenge or support the protagonists
        - What conflict/growth they create

        **VOICE SIGNATURE:**
        - Pitch and tone description
        - Speaking pace and rhythm
        - Vocabulary/education level
        - Accent or speech patterns
        - 2 verbal tics or speech habits
        - 1 catchphrase

        **AUDIO IDENTIFICATION:**
        - How listeners instantly recognize this character
        - Associated sounds or environments
        - Unique vocal qualities

        **PERSONALITY & BACKSTORY:**
        - Core personality traits
        - Relevant backstory (only what affects the story)
        - What they want from the protagonists
        - Their primary conflict or challenge

        **SAMPLE DIALOGUE:**
        Write 2 dialogue examples showing their voice and relationship dynamics with the protagonists.

        Make this character essential to the story and clearly distinguishable in audio format.
        """
        
        return prompt

    async def _parse_supporting_response(self, response: str, dependencies: Dict[str, Any]) -> Tier2Character:
        """Parse supporting character response"""
        
        try:
            name_match = re.search(r'Full name[:\s]*([^\n]+)', response, re.IGNORECASE)
            full_name = name_match.group(1).strip() if name_match else "Supporting Character"
            
            age_match = re.search(r'Age[:\s]*(\d+)', response, re.IGNORECASE)
            age = age_match.group(1) if age_match else "35"
            
            # Extract dialogue samples
            dialogue_matches = re.findall(r'"([^"]*)"', response)
            sample_dialogue = dialogue_matches[:2] if dialogue_matches else [
                "Supporting character dialogue sample.",
                "Another line showing their relationship dynamic."
            ]
            
            voice_signature = VoiceSignature(
                pitch_range=self._extract_section(response, "pitch", "Supporting character vocal range"),
                pace_pattern=self._extract_section(response, "pace", "Natural speaking rhythm"),
                vocabulary_level=self._extract_section(response, "vocabulary", "Educated speech"),
                accent_details=self._extract_section(response, "accent", "Regional speech pattern"),
                verbal_tics=self._extract_list(response, "tics", ["Speech habit"]),
                catchphrases=self._extract_list(response, "catchphrase", ["Signature phrase"]),
                emotional_baseline=self._extract_section(response, "personality", "Balanced demeanor")
            )
            
            audio_markers = AudioMarkers(
                voice_identification=self._extract_section(response, "recognize", "Distinctive vocal quality"),
                sound_associations=self._extract_list(response, "associated sounds", ["Environmental sound"]),
                speech_rhythm=self._extract_section(response, "rhythm", "Speech pattern"),
                breathing_pattern="Natural breathing pattern",
                signature_sounds=["Character-specific sound"]
            )
            
            supporting_char = Tier2Character(
                full_name=full_name,
                age=age,
                role_in_story=self._extract_section(response, "role", "Supporting role"),
                personality_summary=self._extract_section(response, "personality", "Character personality"),
                relevant_backstory=self._extract_section(response, "backstory", "Character background"),
                voice_signature=voice_signature,
                audio_markers=audio_markers,
                character_function=self._extract_section(response, "function", "Narrative function"),
                episode_appearances=["Multiple episodes"],
                relationships=[],
                sample_dialogue=sample_dialogue
            )
            
            return supporting_char
            
        except Exception as e:
            logger.error(f"Failed to parse supporting character: {e}")
            return await self._create_fallback_supporting(dependencies, 1)

    async def _create_fallback_supporting(self, dependencies: Dict[str, Any], char_num: int) -> Tier2Character:
        """Create fallback supporting character"""
        
        return Tier2Character(
            full_name=f"Supporting Character {char_num}",
            age="35",
            role_in_story="Important supporting role",
            personality_summary="Complex supporting character personality",
            relevant_backstory="Relevant character background",
            voice_signature=VoiceSignature(
                pitch_range="Supporting character vocal range",
                pace_pattern="Natural speaking pace",
                vocabulary_level="Educated speech",
                accent_details="Distinct accent",
                verbal_tics=["Speech characteristic"],
                catchphrases=["Signature phrase"],
                emotional_baseline="Character demeanor"
            ),
            audio_markers=AudioMarkers(
                voice_identification="Distinctive voice",
                sound_associations=["Associated sound"],
                speech_rhythm="Speech pattern",
                breathing_pattern="Breathing pattern",
                signature_sounds=["Character sound"]
            ),
            character_function="Narrative support function",
            episode_appearances=["Multiple episodes"],
            relationships=[],
            sample_dialogue=["Supporting dialogue sample", "Character interaction example"]
        )

    async def _generate_tier3_recurring(self, dependencies: Dict[str, Any], tier1_characters: List[Tier1Character]) -> List[Tier3Character]:
        """Generate 5-10 recurring characters"""
        
        # Generate 5-8 recurring characters based on project scope
        recurring_count = 6
        recurring_characters = []
        
        recurring_prompt = self._build_recurring_prompt(dependencies, tier1_characters)
        
        try:
            response = await self.openrouter_agent.generate_response(
                recurring_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=2000
            )
            
            recurring_characters = await self._parse_recurring_response(response, recurring_count)
            
            if self.debug_mode:
                logger.info(f"Generated {len(recurring_characters)} recurring characters")
                
        except Exception as e:
            logger.error(f"Failed to generate recurring characters: {e}")
            # Create fallback recurring characters
            for i in range(recurring_count):
                recurring_characters.append(await self._create_fallback_recurring(i + 1))
        
        return recurring_characters

    def _build_recurring_prompt(self, dependencies: Dict[str, Any], protagonists: List[Tier1Character]) -> str:
        """Build prompt for recurring characters"""
        
        project_bible = dependencies.get('project_bible', {})
        working_title = project_bible.get('working_title', 'Untitled Project')
        world_setting = project_bible.get('world_setting', {})
        
        prompt = f"""
        Create 6 TIER 3 RECURRING CHARACTERS for "{working_title}".

        SETTING: {world_setting.get('primary_location', 'Urban environment')}

        These are minor but memorable characters who:
        - Appear occasionally throughout the series
        - Have one defining trait or quirk
        - Are instantly recognizable in audio
        - Serve specific narrative functions

        For EACH of the 6 characters, provide:

        **CHARACTER 1:**
        - Name
        - Defining trait
        - Voice hook (how to identify in audio)
        - Narrative function
        - One memorable line

        **CHARACTER 2:**
        [Same format]

        **CHARACTER 3:**
        [Same format]

        **CHARACTER 4:**
        [Same format]

        **CHARACTER 5:**
        [Same format]

        **CHARACTER 6:**
        [Same format]

        Examples of recurring character types:
        - Bartender with catchphrase
        - Nosy neighbor with distinctive accent
        - Coffee shop regular with unique ordering style
        - Security guard with memorable habit
        - Taxi driver with interesting background

        Make each character instantly memorable for audio identification with unique voice hooks.
        """
        
        return prompt

    async def _parse_recurring_response(self, response: str, count: int) -> List[Tier3Character]:
        """Parse recurring characters response"""
        
        recurring_chars = []
        
        # Split response into character sections
        char_sections = re.split(r'\*\*CHARACTER \d+:\*\*', response)
        
        for i, section in enumerate(char_sections[1:], 1):  # Skip first empty section
            if i > count:
                break
                
            try:
                name_match = re.search(r'Name[:\s]*([^\n]+)', section, re.IGNORECASE)
                name = name_match.group(1).strip() if name_match else f"Recurring Character {i}"
                
                trait_match = re.search(r'Defining trait[:\s]*([^\n]+)', section, re.IGNORECASE)
                defining_trait = trait_match.group(1).strip() if trait_match else "Memorable characteristic"
                
                hook_match = re.search(r'Voice hook[:\s]*([^\n]+)', section, re.IGNORECASE)
                voice_hook = hook_match.group(1).strip() if hook_match else "Distinctive voice quality"
                
                function_match = re.search(r'Narrative function[:\s]*([^\n]+)', section, re.IGNORECASE)
                narrative_function = function_match.group(1).strip() if function_match else "Story support function"
                
                line_match = re.search(r'memorable line[:\s]*"([^"]*)"', section, re.IGNORECASE)
                sample_line = line_match.group(1) if line_match else "Memorable character line"
                
                recurring_char = Tier3Character(
                    name=name,
                    defining_trait=defining_trait,
                    voice_hook=voice_hook,
                    narrative_function=narrative_function,
                    episode_appearances=["Various episodes"],
                    memorable_quirk=defining_trait,
                    sample_line=sample_line
                )
                
                recurring_chars.append(recurring_char)
                
            except Exception as e:
                logger.error(f"Failed to parse recurring character {i}: {e}")
                recurring_chars.append(await self._create_fallback_recurring(i))
        
        # Fill to target count if needed
        while len(recurring_chars) < count:
            recurring_chars.append(await self._create_fallback_recurring(len(recurring_chars) + 1))
        
        return recurring_chars[:count]

    async def _create_fallback_recurring(self, char_num: int) -> Tier3Character:
        """Create fallback recurring character"""
        
        return Tier3Character(
            name=f"Recurring Character {char_num}",
            defining_trait="Memorable character trait",
            voice_hook="Distinctive audio identifier",
            narrative_function="Supporting story function",
            episode_appearances=["Various episodes"],
            memorable_quirk="Character quirk",
            sample_line="Memorable character line"
        )

    async def _generate_character_relationships(self, tier1_chars: List[Tier1Character], 
                                             tier2_chars: List[Tier2Character], 
                                             dependencies: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate relationship matrix between characters"""
        
        all_major_chars = [char.full_name for char in tier1_chars] + [char.full_name for char in tier2_chars]
        
        relationship_prompt = f"""
        Create a relationship matrix for these characters in the audiobook project:

        PROTAGONISTS: {[char.full_name for char in tier1_chars]}
        SUPPORTING: {[char.full_name for char in tier2_chars]}

        For each character, define their key relationships with others:
        - Type of relationship (romantic, familial, professional, antagonistic, etc.)
        - Relationship dynamic (how they interact)
        - Conflict potential (sources of tension)

        Format as:
        **[CHARACTER NAME]:**
        - Relationship with [OTHER CHARACTER]: [description]
        - Relationship with [OTHER CHARACTER]: [description]

        Focus on the most important relationships that drive story conflict and character development.
        """
        
        try:
            response = await self.openrouter_agent.generate_response(
                relationship_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=1500
            )
            
            # Parse relationships from response
            relationships = {}
            current_char = None
            
            for line in response.split('\n'):
                char_match = re.match(r'\*\*([^:]+):\*\*', line)
                if char_match:
                    current_char = char_match.group(1).strip()
                    relationships[current_char] = []
                elif current_char and line.strip().startswith('-'):
                    rel_text = line.strip()[1:].strip()
                    relationships[current_char].append(rel_text)
            
            return relationships
            
        except Exception as e:
            logger.error(f"Failed to generate relationships: {e}")
            return {char: ["Relationship development needed"] for char in all_major_chars}

    async def _generate_voice_sample_collection(self, tier1_chars: List[Tier1Character], 
                                               tier2_chars: List[Tier2Character], 
                                               tier3_chars: List[Tier3Character]) -> Dict[str, str]:
        """Generate comprehensive voice sample collection"""
        
        voice_samples = {}
        
        # Compile samples from all characters
        for char in tier1_chars:
            voice_samples[char.full_name] = " | ".join(char.sample_dialogue)
        
        for char in tier2_chars:
            voice_samples[char.full_name] = " | ".join(char.sample_dialogue)
        
        for char in tier3_chars:
            voice_samples[char.name] = char.sample_line
        
        return voice_samples

    async def _generate_audio_identification_guide(self, tier1_chars: List[Tier1Character], 
                                                  tier2_chars: List[Tier2Character], 
                                                  tier3_chars: List[Tier3Character]) -> str:
        """Generate comprehensive audio identification guide"""
        
        guide_sections = []
        
        guide_sections.append("AUDIO IDENTIFICATION GUIDE")
        guide_sections.append("=" * 40)
        guide_sections.append("")
        
        guide_sections.append("TIER 1 PROTAGONISTS:")
        for char in tier1_chars:
            guide_sections.append(f"{char.full_name}:")
            guide_sections.append(f"  Voice ID: {char.audio_markers.voice_identification}")
            guide_sections.append(f"  Key Sounds: {', '.join(char.audio_markers.sound_associations)}")
            guide_sections.append(f"  Speech Pattern: {char.audio_markers.speech_rhythm}")
            guide_sections.append("")
        
        guide_sections.append("TIER 2 SUPPORTING:")
        for char in tier2_chars:
            guide_sections.append(f"{char.full_name}:")
            guide_sections.append(f"  Voice ID: {char.audio_markers.voice_identification}")
            guide_sections.append(f"  Quick ID: {char.voice_signature.catchphrases[0] if char.voice_signature.catchphrases else 'Speech pattern'}")
            guide_sections.append("")
        
        guide_sections.append("TIER 3 RECURRING:")
        for char in tier3_chars:
            guide_sections.append(f"{char.name}: {char.voice_hook}")
        
        return "\n".join(guide_sections)

    async def _generate_casting_notes(self, tier1_chars: List[Tier1Character], 
                                     tier2_chars: List[Tier2Character], 
                                     dependencies: Dict[str, Any]) -> str:
        """Generate casting and production notes"""
        
        casting_prompt = f"""
        Generate professional casting notes for this audiobook project.

        PROTAGONISTS: {len(tier1_chars)} characters
        SUPPORTING: {len(tier2_chars)} characters

        KEY VOICE REQUIREMENTS:
        {[f"{char.full_name}: {char.voice_signature.pitch_range}, {char.voice_signature.accent_details}" for char in tier1_chars]}

        Create casting guidance covering:
        1. Overall voice casting strategy
        2. Key voice type requirements
        3. Accent/dialect needs
        4. Age range considerations
        5. Production complexity notes
        6. Special audio requirements

        Focus on practical casting and recording guidance for audio drama production.
        """
        
        try:
            response = await self.openrouter_agent.generate_response(
                casting_prompt,
                model="anthropic/claude-3-sonnet",
                max_tokens=1000
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate casting notes: {e}")
            return "Casting notes require development based on character voice specifications."

    def export_to_text(self, character_bible: CharacterBible) -> str:
        """Export character bible to text format"""
        
        sections = []
        
        # Header
        sections.append("CHARACTER BIBLE")
        sections.append("=" * 60)
        sections.append(f"Project: {character_bible.working_title}")
        sections.append(f"Session: {character_bible.session_id}")
        sections.append(f"Generated: {character_bible.created_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        sections.append(f"Total Characters: {character_bible.character_count_summary['total_characters']}")
        sections.append("")
        
        # Character count summary
        sections.append("CHARACTER COUNT SUMMARY")
        sections.append("-" * 30)
        sections.append(f"Tier 1 Protagonists: {character_bible.character_count_summary['tier1_protagonists']}")
        sections.append(f"Tier 2 Supporting: {character_bible.character_count_summary['tier2_supporting']}")
        sections.append(f"Tier 3 Recurring: {character_bible.character_count_summary['tier3_recurring']}")
        sections.append("")
        
        # Tier 1 characters
        sections.append("TIER 1: PROTAGONISTS")
        sections.append("=" * 30)
        for char in character_bible.tier1_protagonists:
            sections.append(f"\n{char.full_name} (Age {char.age})")
            sections.append("-" * len(char.full_name))
            sections.append(f"Psychology: {char.psychological_profile}")
            sections.append(f"Voice: {char.voice_signature.pitch_range}, {char.voice_signature.pace_pattern}")
            sections.append(f"Accent: {char.voice_signature.accent_details}")
            sections.append(f"Audio ID: {char.audio_markers.voice_identification}")
            sections.append(f"Desires: {', '.join(char.core_desires)}")
            sections.append(f"Fears: {', '.join(char.deepest_fears)}")
            sections.append("Sample Dialogue:")
            for dialogue in char.sample_dialogue:
                sections.append(f"  \"{dialogue}\"")
            sections.append("")
        
        # Tier 2 characters
        sections.append("\nTIER 2: MAJOR SUPPORTING")
        sections.append("=" * 30)
        for char in character_bible.tier2_supporting:
            sections.append(f"\n{char.full_name} (Age {char.age})")
            sections.append("-" * len(char.full_name))
            sections.append(f"Role: {char.role_in_story}")
            sections.append(f"Function: {char.character_function}")
            sections.append(f"Voice: {char.voice_signature.pitch_range}")
            sections.append(f"Audio ID: {char.audio_markers.voice_identification}")
            sections.append("Sample Dialogue:")
            for dialogue in char.sample_dialogue:
                sections.append(f"  \"{dialogue}\"")
            sections.append("")
        
        # Tier 3 characters
        sections.append("\nTIER 3: RECURRING CHARACTERS")
        sections.append("=" * 30)
        for char in character_bible.tier3_recurring:
            sections.append(f"{char.name}: {char.defining_trait}")
            sections.append(f"  Voice Hook: {char.voice_hook}")
            sections.append(f"  Function: {char.narrative_function}")
            sections.append(f"  Sample Line: \"{char.sample_line}\"")
            sections.append("")
        
        # Audio identification guide
        sections.append("\nAUDIO IDENTIFICATION GUIDE")
        sections.append("=" * 30)
        sections.append(character_bible.audio_identification_guide)
        sections.append("")
        
        # Relationship matrix
        sections.append("\nCHARACTER RELATIONSHIPS")
        sections.append("=" * 30)
        for character, relationships in character_bible.relationship_matrix.items():
            sections.append(f"{character}:")
            for relationship in relationships:
                sections.append(f"  • {relationship}")
            sections.append("")
        
        # Casting notes
        sections.append("\nCASTING & PRODUCTION NOTES")
        sections.append("=" * 30)
        sections.append(character_bible.casting_notes)
        sections.append("")
        
        return "\n".join(sections)

    def export_to_json(self, character_bible: CharacterBible) -> Dict[str, Any]:
        """Export character bible to JSON format"""
        
        return {
            "session_id": character_bible.session_id,
            "working_title": character_bible.working_title,
            "created_timestamp": character_bible.created_timestamp.isoformat(),
            "character_count_summary": character_bible.character_count_summary,
            "tier1_protagonists": [asdict(char) for char in character_bible.tier1_protagonists],
            "tier2_supporting": [asdict(char) for char in character_bible.tier2_supporting],
            "tier3_recurring": [asdict(char) for char in character_bible.tier3_recurring],
            "voice_sample_collection": character_bible.voice_sample_collection,
            "relationship_matrix": character_bible.relationship_matrix,
            "audio_identification_guide": character_bible.audio_identification_guide,
            "casting_notes": character_bible.casting_notes
        }

    def export_to_pdf(self, character_bible: CharacterBible) -> bytes:
        """Export character bible to PDF format"""
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
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
                textColor='darkblue',
                spaceAfter=30
            )
            
            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading1'],
                fontSize=16,
                textColor='darkred',
                spaceAfter=12
            )
            
            # Title page
            story.append(Paragraph("CHARACTER BIBLE", title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Project: {character_bible.working_title}", styles['Heading2']))
            story.append(Paragraph(f"Total Characters: {character_bible.character_count_summary['total_characters']}", styles['Normal']))
            story.append(Paragraph(f"Generated: {character_bible.created_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(PageBreak())
            
            # Character summary
            story.append(Paragraph("CHARACTER OVERVIEW", header_style))
            story.append(Paragraph(f"Tier 1 Protagonists: {character_bible.character_count_summary['tier1_protagonists']}", styles['Normal']))
            story.append(Paragraph(f"Tier 2 Supporting: {character_bible.character_count_summary['tier2_supporting']}", styles['Normal']))
            story.append(Paragraph(f"Tier 3 Recurring: {character_bible.character_count_summary['tier3_recurring']}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Tier 1 characters
            story.append(Paragraph("TIER 1: PROTAGONISTS", header_style))
            for char in character_bible.tier1_protagonists:
                story.append(Paragraph(f"{char.full_name} (Age {char.age})", styles['Heading3']))
                story.append(Paragraph(f"<b>Psychology:</b> {char.psychological_profile}", styles['Normal']))
                story.append(Paragraph(f"<b>Voice:</b> {char.voice_signature.pitch_range}, {char.voice_signature.pace_pattern}", styles['Normal']))
                story.append(Paragraph(f"<b>Audio ID:</b> {char.audio_markers.voice_identification}", styles['Normal']))
                
                story.append(Paragraph("<b>Sample Dialogue:</b>", styles['Normal']))
                for dialogue in char.sample_dialogue[:2]:  # Limit for PDF space
                    story.append(Paragraph(f"• \"{dialogue}\"", styles['Normal']))
                story.append(Spacer(1, 12))
            
            story.append(PageBreak())
            
            # Tier 2 characters
            story.append(Paragraph("TIER 2: MAJOR SUPPORTING", header_style))
            for char in character_bible.tier2_supporting:
                story.append(Paragraph(f"{char.full_name} (Age {char.age})", styles['Heading3']))
                story.append(Paragraph(f"<b>Role:</b> {char.role_in_story}", styles['Normal']))
                story.append(Paragraph(f"<b>Voice:</b> {char.voice_signature.pitch_range}", styles['Normal']))
                story.append(Paragraph(f"<b>Audio ID:</b> {char.audio_markers.voice_identification}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Tier 3 characters
            story.append(Paragraph("TIER 3: RECURRING CHARACTERS", header_style))
            for char in character_bible.tier3_recurring:
                story.append(Paragraph(f"<b>{char.name}:</b> {char.defining_trait}", styles['Normal']))
                story.append(Paragraph(f"Voice Hook: {char.voice_hook}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            story.append(PageBreak())
            
            # Audio guide
            story.append(Paragraph("AUDIO IDENTIFICATION GUIDE", header_style))
            audio_guide_lines = character_bible.audio_identification_guide.split('\n')
            for line in audio_guide_lines:
                if line.strip():
                    story.append(Paragraph(line, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return pdf_data
            
        except ImportError:
            logger.warning("ReportLab not available for PDF generation")
            return self.export_to_text(character_bible).encode('utf-8')
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return self.export_to_text(character_bible).encode('utf-8')


# CLI interface for testing
async def main():
    """Main CLI interface for Station 8"""
    
    print("🎭 STATION 8: CHARACTER ARCHITECTURE")
    print("=" * 50)
    
    session_id = input("Enter session ID for character generation: ").strip()
    if not session_id:
        print("❌ Session ID required")
        return
    
    try:
        station = Station08CharacterArchitecture()
        await station.initialize()
        
        debug = input("Enable debug mode? (y/N): ").lower().strip() == 'y'
        if debug:
            station.enable_debug_mode()
        
        print(f"\n🎭 Starting character architecture for session: {session_id}")
        
        result = await station.process(session_id)
        
        print(f"\n✅ CHARACTER BIBLE COMPLETED")
        print("=" * 50)
        print(f"Total Characters: {result.character_count_summary['total_characters']}")
        print(f"Protagonists: {result.character_count_summary['tier1_protagonists']}")
        print(f"Supporting: {result.character_count_summary['tier2_supporting']}")
        print(f"Recurring: {result.character_count_summary['tier3_recurring']}")
        
        # Export results
        os.makedirs("outputs", exist_ok=True)
        
        # Text export
        text_filename = f"outputs/station8_character_bible_{session_id}.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(station.export_to_text(result))
        print(f"📄 Text Bible: {text_filename}")
        
        # JSON export
        json_filename = f"outputs/station8_character_bible_{session_id}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(station.export_to_json(result), f, indent=2, default=str)
        print(f"📊 JSON Data: {json_filename}")
        
        # PDF export
        try:
            pdf_data = station.export_to_pdf(result)
            pdf_filename = f"outputs/station8_character_bible_{session_id}.pdf"
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_data)
            print(f"📑 PDF Bible: {pdf_filename}")
        except Exception as e:
            print(f"⚠️ PDF export failed: {e}")
        
        # Show character summary
        print(f"\n🎭 PROTAGONISTS:")
        for char in result.tier1_protagonists:
            print(f"   • {char.full_name} (Age {char.age})")
        
        print(f"\n🎭 SUPPORTING CHARACTERS:")
        for char in result.tier2_supporting:
            print(f"   • {char.full_name} - {char.role_in_story}")
        
        print(f"\n🎭 RECURRING CHARACTERS:")
        for char in result.tier3_recurring:
            print(f"   • {char.name} - {char.defining_trait}")
        
    except Exception as e:
        print(f"❌ Character generation failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())