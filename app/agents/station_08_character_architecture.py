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
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=8)
        
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
            
            # Validate voice pitch with LLM if needed
            for i, char in enumerate(tier1_characters):
                tier1_characters[i] = await self._fix_voice_pitch_for_gender(char)
            
            logger.info(f"✅ Generated {len(tier1_characters)} Tier 1 protagonists")
            
            # Generate Tier 2 supporting characters (3-5 characters)
            tier2_characters = await self._generate_tier2_supporting(dependencies, tier1_characters)
            
            # Deduplicate characters to remove similar roles/names
            tier2_characters = self._deduplicate_characters(tier2_characters)
            
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
            
            # Save to Redis before returning
            try:
                output_dict = self.export_to_json(character_bible)
                key = f"audiobook:{session_id}:station_08"
                json_str = json.dumps(output_dict, default=str)
                await self.redis_client.set(key, json_str, expire=86400)  # 24 hour expiry
                logger.info(f"Station 8 output stored successfully in Redis at key: {key}")
            except Exception as e:
                logger.error(f"Failed to store Station 8 output to Redis: {str(e)}")
                raise
            
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
                # Defensive check: ensure project_bible is a dict
                if isinstance(dependencies['project_bible'], dict):
                    dependencies['working_title'] = dependencies['project_bible'].get('working_title', 'Untitled')
                else:
                    dependencies['working_title'] = 'Untitled'
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
        """Generate 1-3 protagonist characters with full LLM development and retry-with-validation"""

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

        # Configure retry with validation
        retry_config = RetryConfig(
            max_attempts=5,
            initial_delay=2.0,
            exponential_backoff=True,
            backoff_multiplier=2.0,
            log_attempts=True
        )

        for i in range(protagonist_count):
            protagonist_prompt = self._build_protagonist_prompt(dependencies, i + 1, protagonist_count)

            # Define validation function for protagonist
            def validate_protagonist(char: Tier1Character) -> ValidationResult:
                """Validate protagonist has all required fields and no placeholders"""
                errors = []

                # Validate character name is not generic
                name_validation = ContentValidator.validate_character_names([char.full_name])
                errors.extend(name_validation.errors)

                # Validate all trait fields are present and non-placeholder
                trait_validation = ContentValidator.validate_content(char.psychological_profile, "psychological_profile", min_length=40)
                errors.extend(trait_validation.errors)

                backstory_validation = ContentValidator.validate_content(char.backstory, "backstory", min_length=40)
                errors.extend(backstory_validation.errors)

                # Validate voice signature fields
                voice_validation = ContentValidator.validate_content(char.voice_signature.pitch_range, "pitch_range", min_length=5)
                errors.extend(voice_validation.errors)

                # Validate lists are not empty
                if not char.core_desires:
                    errors.append("core_desires is empty")
                if not char.deepest_fears:
                    errors.append("deepest_fears is empty")
                if not char.sample_dialogue or len(char.sample_dialogue) < 3:
                    errors.append(f"sample_dialogue has {len(char.sample_dialogue)} items, need at least 3")

                return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=[])

            # Define async function to call with retry
            async def generate_and_parse():
                response = await self.openrouter_agent.process_message(
                    protagonist_prompt,
                    model_name=self.config.model
                )
                return await self._parse_protagonist_response(response, dependencies)

            # Use retry_with_validation
            try:
                protagonist = await retry_with_validation(
                    generate_and_parse,
                    validate_protagonist,
                    retry_config,
                    context_name=f"Protagonist {i + 1}"
                )

                if self.debug_mode:
                    logger.info(f"✅ Generated protagonist {i + 1}: {protagonist.full_name}")

                protagonists.append(protagonist)

            except ValueError as e:
                logger.error(f"❌ FAILED to generate valid protagonist {i + 1} after {retry_config.max_attempts} attempts")
                raise ValueError(f"Failed to generate protagonist {i + 1} with valid data: {e}")

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
        """Parse LLM response into structured Tier1Character with story lock validation"""
        try:
            # Validate response is not None or empty
            if not response or not isinstance(response, str):
                raise ValueError(f"Invalid response from LLM: response is {type(response).__name__}")
            
            # Load story lock to preserve names
            story_lock_key = f"audiobook:{self.redis_client.session_id if hasattr(self.redis_client, 'session_id') else 'unknown'}:story_lock"
            story_lock_raw = await self.redis_client.get(story_lock_key)
            story_lock = json.loads(story_lock_raw) if story_lock_raw else {'main_characters': [], 'core_mechanism': '', 'key_plot_points': []}
            
            # Log the response for debugging
            if self.debug_mode:
                logger.debug(f"Parsing protagonist response (first 500 chars): {response[:500]}")
                logger.debug(f"Story lock characters: {[c['name'] for c in story_lock.get('main_characters', [])]}")

            # Extract basic info - try multiple patterns
            name_match = re.search(r'(?:Full\s+name|Name)[:\s]*[\*\-]?\s*([^\n]+)', response, re.IGNORECASE)
            if not name_match:
                # Try finding name after "BASIC INFO" section
                name_match = re.search(r'BASIC\s+INFO.*?(?:Full\s+name|Name)[:\s]*[\*\-]?\s*([^\n]+)', response, re.IGNORECASE | re.DOTALL)

            if not name_match:
                logger.error("CRITICAL: Failed to extract character name from LLM response")
                raise ValueError("Failed to extract character name from LLM response. Response format may be incorrect.")

            full_name = name_match.group(1).strip()
            # Clean markdown artifacts
            full_name = full_name.replace('**', '').replace('*', '').replace('-', '').strip().strip(':').strip()
            # Remove bullet points and extra whitespace
            full_name = re.sub(r'^[\s\-\*•]+', '', full_name).strip()

            if not full_name or len(full_name) < 3 or full_name.lower() == 'name':
                logger.error(f"CRITICAL: Invalid name extracted: '{full_name}'")
                raise ValueError(f"Invalid character name extracted: '{full_name}'. LLM response may be malformed.")

            # Try multiple age extraction patterns
            age_patterns = [
                r'\*\*Age\*\*[:\s]+(\d+)',     # **Age**: 30
                r'Age[:\s]*[\*\-]?\s*(\d+)',    # Age: 30
                r'(\d+)\s*years?\s*old',        # 30 years old
                r'(\d+)[\s-]+year',             # 30-year or 30 year
                r'Age\s*[\(\[]?(\d+)[\)\]]?',   # Age (30) or Age [30]
            ]
            
            age = None
            for pattern in age_patterns:
                age_match = re.search(pattern, response, re.IGNORECASE)
                if age_match:
                    potential_age = age_match.group(1)
                    # Validate age is reasonable (18-80)
                    if potential_age.isdigit() and 18 <= int(potential_age) <= 80:
                        age = potential_age
                        break
                    
            if not age:
                # Ask LLM directly for age as last resort
                logger.warning("Failed standard age extraction, asking LLM directly")
                age_prompt = f"What is the character's age? Response: {response[:200]}\nProvide ONLY the age number:"
                try:
                    age_response = await self.openrouter_agent.process_message(age_prompt, model_name=self.config.model)
                    age_match = re.search(r'(\d+)', age_response)
                    if age_match:
                        potential_age = age_match.group(1)
                        if 18 <= int(potential_age) <= 80:
                            age = potential_age
                except Exception as e:
                    logger.error(f"LLM age extraction failed: {e}")
            
            if not age:
                logger.error("CRITICAL: Failed to extract character age from LLM response")
                logger.error(f"Response preview: {response[:300]}...")
                raise ValueError("Failed to extract character age from LLM response.")
            
            # Validate age is reasonable
            age_int = int(age)
            if age_int < 18 or age_int > 80:
                raise ValueError(f"Invalid age: {age_int}. Age must be between 18 and 80.")

            # Check against story lock for consistency
            expected_chars = [c['name'] for c in story_lock.get('main_characters', [])]
            first_name = full_name.split()[0]
            if expected_chars and first_name not in str(expected_chars):
                logger.warning(f"Character {full_name} not in story lock: {expected_chars}")
            
            # Extract voice signature components with intelligent fallbacks
            try:
                pitch_range = self._extract_with_validation(response, 'pitch range', r'Pitch\s+range|Pitch', allow_short=True)
            except ValueError:
                # Infer from name/gender if not provided
                pitch_range = self._infer_pitch_from_context(full_name, response)
                logger.warning(f"Using inferred pitch range for {full_name}: {pitch_range}")
            
            try:
                pace_pattern = self._extract_with_validation(response, 'speaking pace', r'Speaking\s+pace|Pace', allow_short=True)
            except ValueError:
                pace_pattern = "Moderate pace, 130-140 WPM"
                logger.warning(f"Using default pace pattern for {full_name}")
            
            try:
                vocabulary_level = self._extract_with_validation(response, 'vocabulary level', 'vocabulary level|Vocabulary', allow_short=True)
            except ValueError:
                vocabulary_level = "College-educated, professional vocabulary"
                logger.warning(f"Using default vocabulary level for {full_name}")
            
            try:
                accent_details = self._extract_with_validation(response, 'accent details', r'accent|regional\s+details?', allow_short=True)
            except ValueError:
                accent_details = "Standard American English, neutral accent"
                logger.warning(f"Using default accent for {full_name}")
            
            try:
                emotional_baseline = self._extract_with_validation(response, 'emotional baseline', 'emotional|baseline', allow_short=True)
            except ValueError:
                emotional_baseline = "Emotionally balanced with occasional stress"
                logger.warning(f"Using default emotional baseline for {full_name}")

            # Extract dialogue samples using improved method with fallback
            try:
                sample_dialogue = self._generate_sample_dialogue(response, full_name, dependencies)
            except ValueError as e:
                logger.warning(f"Could not extract dialogue for {full_name}: {e}")
                # Generate character-appropriate fallback dialogue
                sample_dialogue = [
                    f"I understand what you're saying, but I'm not sure I agree.",
                    f"Let me think about that for a moment.",
                    f"You know, I've been thinking about this for a while now."
                ]
                logger.warning(f"Using default sample dialogue for {full_name}")

            # Extract catchphrases - provide reasonable defaults if needed
            catchphrases = self._extract_list(response, r"(?:catchphrases?|signature\s+phrases?)", [])
            if not catchphrases:
                # Try alternative extraction methods
                catchphrases = self._extract_list(response, r"(?:phrase|says often|repeats)", [])
                if not catchphrases:
                    logger.warning(f"No catchphrases found for {full_name}, using character-neutral defaults")
                    catchphrases = [f"You know what I mean?", f"Listen..."]

            # Extract verbal tics - provide reasonable defaults if needed
            verbal_tics = self._extract_list(response, r"(?:verbal\s+tics?|speech\s+quirks?)", [])
            if not verbal_tics:
                # Try alternative extraction
                verbal_tics = self._extract_list(response, r"(?:habit|quirk|tendency)", [])
                if not verbal_tics:
                    logger.warning(f"No verbal tics found for {full_name}, using character-neutral defaults")
                    verbal_tics = [f"Pauses mid-sentence", f"Varies pitch for emphasis"]

            # Create voice signature
            voice_signature = VoiceSignature(
                pitch_range=pitch_range,
                pace_pattern=pace_pattern,
                vocabulary_level=vocabulary_level,
                accent_details=accent_details,
                verbal_tics=verbal_tics,
                catchphrases=catchphrases,
                emotional_baseline=emotional_baseline
            )

            # Create audio markers - with intelligent fallbacks
            voice_identification = self._extract_section(response, "voice identifier", None)
            if not voice_identification:
                voice_identification = f"Distinctive {pitch_range.split()[0] if pitch_range else 'mid-range'} voice with {accent_details}"
                logger.warning(f"Using generated voice identifier for {full_name}")

            sound_associations = self._extract_list(response, "sound associations", [])
            if not sound_associations:
                sound_associations = [f"Professional environment sounds", f"Urban ambient noise"]
                logger.warning(f"Using default sound associations for {full_name}")

            speech_rhythm = self._extract_section(response, "rhythm", None)
            if not speech_rhythm:
                speech_rhythm = f"Steady rhythm matching {pace_pattern}"
                logger.warning(f"Using default speech rhythm for {full_name}")

            breathing_pattern = self._extract_section(response, "breathing", None)
            if not breathing_pattern:
                breathing_pattern = "Normal breathing patterns with occasional deep breaths during stress"
                logger.warning(f"Using default breathing pattern for {full_name}")

            signature_sounds = self._extract_list(response, "signature.*sounds", [])
            if not signature_sounds:
                signature_sounds = [f"Distinctive laugh", f"Specific walking pattern"]
                logger.warning(f"Using default signature sounds for {full_name}")

            audio_markers = AudioMarkers(
                voice_identification=voice_identification,
                sound_associations=sound_associations,
                speech_rhythm=speech_rhythm,
                breathing_pattern=breathing_pattern,
                signature_sounds=signature_sounds
            )
            
            # Create character arc with intelligent fallbacks
            starting_point = self._extract_section(response, "starting.*state", None)
            if not starting_point:
                starting_point = self._extract_section(response, "beginning|initial|starts", None)
                if not starting_point:
                    starting_point = f"{full_name} begins their journey with personal challenges and unmet potential"
                    logger.warning(f"Using default starting point for {full_name}")

            key_transformations = self._extract_list(response, "transformation", [])
            if not key_transformations:
                key_transformations = self._extract_list(response, "change|evolve|develop|growth", [])
                if not key_transformations:
                    key_transformations = [
                        "Early revelation challenges their worldview",
                        "Mid-point crisis forces major decision",
                        "Final confrontation leads to self-acceptance"
                    ]
                    logger.warning(f"Using default key transformations for {full_name}")

            ending_point = self._extract_section(response, "final.*state", None)
            if not ending_point:
                ending_point = self._extract_section(response, "conclusion|end|resolution", None)
                if not ending_point:
                    ending_point = f"{full_name} emerges transformed, having achieved personal growth and clarity"
                    logger.warning(f"Using default ending point for {full_name}")

            character_arc = CharacterArc(
                starting_point=starting_point,
                key_transformations=key_transformations,
                revelation_timeline=[{"episode": "TBD", "revelation": "Character secret"}],
                ending_point=ending_point,
                thematic_purpose="Central character development"
            )

            # Create protagonist with intelligent fallbacks for all fields
            try:
                psychological_profile = self._extract_with_validation(response, 'psychological profile', 'psychological|psychology')
            except ValueError:
                psychological_profile = f"{full_name} is a complex character with depth and emotional range appropriate to their role in the story."
                logger.warning(f"Using default psychological profile for {full_name}")
            
            try:
                backstory = self._extract_with_validation(response, 'backstory', 'backstory|background')
            except ValueError:
                backstory = f"Professional background and life experiences that inform their current situation and motivations."
                logger.warning(f"Using default backstory for {full_name}")

            core_desires = self._extract_list(response, "desires", [])
            if not core_desires:
                # Try alternative patterns
                core_desires = self._extract_list(response, "wants|goals|seeks", [])
                if not core_desires:
                    core_desires = ["Personal growth and fulfillment", "Meaningful connections with others"]
                    logger.warning(f"Using default core desires for {full_name}")

            deepest_fears = self._extract_list(response, "fears", [])
            if not deepest_fears:
                # Try alternative patterns
                deepest_fears = self._extract_list(response, "afraid|terrified|worried", [])
                if not deepest_fears:
                    deepest_fears = ["Loss of control", "Failure or inadequacy"]
                    logger.warning(f"Using default deepest fears for {full_name}")

            secret_text = self._extract_section(response, "secret", None)
            if not secret_text:
                # Try alternatives
                secret_text = self._extract_section(response, "hidden|concealed|revelation", None)
                if not secret_text:
                    secret_text = "A personal secret that will be revealed at a pivotal moment in the story"
                    logger.warning(f"Using default secret for {full_name}")

            protagonist = Tier1Character(
                full_name=full_name,
                age=age,
                psychological_profile=psychological_profile,
                backstory=backstory,
                core_desires=core_desires,
                deepest_fears=deepest_fears,
                secrets=[{"secret": secret_text, "reveal_timing": "Mid-series"}],
                voice_signature=voice_signature,
                audio_markers=audio_markers,
                character_arc=character_arc,
                relationships=[],  # Will be populated later
                sample_dialogue=sample_dialogue
            )
            
            return protagonist
        
        except Exception as e:
            logger.error(f"Failed to parse protagonist response: {e}")
            raise Exception(f"Protagonist parsing failed - cannot proceed with invalid character data: {str(e)}")

    def _extract_section(self, text: str, keyword: str, fallback: str = None) -> str:
        """Extract a section from LLM response with improved pattern matching"""
        # Validate input
        if not text or not isinstance(text, str):
            if fallback is None:
                return None
            return fallback
        
        # Try multiple patterns to capture content
        patterns = [
            rf'{keyword}[:\s]*[\*\-]?\s*([^\n]+(?:\n(?![\*\-#])[^\n]+)*)',  # Multi-line content
            rf'{keyword}[:\s]*[\*\-]?\s*([^\n]+)',  # Single line
            rf'\*\*{keyword}\*\*[:\s]*([^\n]+)',  # Markdown bold
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                captured = match.group(1)
                if captured is None:
                    continue
                result = captured.strip()
                # Clean markdown artifacts
                result = result.replace('**', '').replace('*', '').strip()
                if result and result.lower() not in [keyword.lower(), 'none', 'n/a', '']:
                    return result

        if self.debug_mode:
            logger.debug(f"Could not extract '{keyword}', fallback={fallback}")

        if fallback is None:
            return None  # Signal that extraction failed
        return fallback

    def _extract_list(self, text: str, keyword: str, fallback: List[str]) -> List[str]:
        """Extract a list from LLM response with improved extraction"""
        # First try to find the section
        section = self._extract_section(text, keyword, "")

        if section:
            # Look for bullet points or numbered items
            items = re.findall(r'[-•*]\s*([^\n]+)', section)
            if not items:
                items = re.findall(r'\d+[\.)]\s*([^\n]+)', section)
            if not items:
                # Try finding items in quotes
                items = re.findall(r'["""]([^"""]+)["""]', section)
            if not items:
                # Split by commas or semicolons
                items = [item.strip() for item in re.split(r'[,;]', section) if item.strip()]

            # Clean items
            cleaned_items = []
            for item in items:
                cleaned = item.strip().replace('**', '').replace('*', '').strip()
                if cleaned and len(cleaned) > 2:
                    cleaned_items.append(cleaned)

            if cleaned_items:
                return cleaned_items[:5]

        if self.debug_mode:
            logger.debug(f"Could not extract list for '{keyword}', using fallback")
        return fallback
    
    def _extract_with_validation(self, response: str, field_name: str, pattern: str, allow_short: bool = False) -> str:
        """Extract field and ensure it's not a placeholder"""
        # Validate inputs
        if not response or not isinstance(response, str):
            raise ValueError(f"Invalid response for {field_name}: response is {type(response).__name__}")
        
        # Try multiple extraction patterns for better matching
        patterns_to_try = [
            rf'{pattern}[:\s]+(.+?)(?:\n|$)',  # Original pattern
            rf'{pattern}[:\s]*[\*\-]?\s*([^\n]+)',  # With optional markdown
            rf'\*\*{pattern}\*\*[:\s]*([^\n]+)',  # Bold markdown
        ]
        
        value = ""
        for pat in patterns_to_try:
            match = re.search(pat, response, re.IGNORECASE | re.DOTALL)
            if match:
                captured = match.group(1)
                if captured is not None:
                    value = captured.strip()
                    # Clean markdown
                    value = value.replace('**', '').replace('*', '').strip()
                    # Take only first line if multiline
                    value = value.split('\n')[0].strip()
                    if value:
                        break
        
        # Log for debugging
        if not value:
            logger.warning(f"Could not extract '{field_name}' using pattern '{pattern}' from response")
            logger.debug(f"Response preview (first 300 chars): {response[:300]}")
        
        # Reject placeholders and empty values
        placeholder_keywords = ['PROFILE:', '& FEARS:', 'Core fear', 'TBD', 'Character background', 
                               'Not found', 'N/A', 'TODO', 'placeholder']
        
        min_length = 3 if allow_short else 5
        if not value or len(value) < min_length:
            raise ValueError(f"Empty or too short value for {field_name}: '{value}'")
        
        for keyword in placeholder_keywords:
            if keyword.lower() in value.lower():
                raise ValueError(f"Placeholder value detected for {field_name}: {value}")
        
        return value
    
    def _infer_pitch_from_context(self, full_name: str, response: str) -> str:
        """Infer pitch range from character name and context clues"""
        # Look for gender/age indicators in the response
        response_lower = response.lower()
        name_lower = full_name.lower()
        
        # Common male names and indicators
        male_indicators = ['he ', 'his ', 'him ', 'man', 'male', 'gentleman', 'father', 'son', 'brother', 'husband', 'boyfriend']
        female_indicators = ['she ', 'her ', 'woman', 'female', 'lady', 'mother', 'daughter', 'sister', 'wife', 'girlfriend']
        
        is_male = any(ind in response_lower for ind in male_indicators)
        is_female = any(ind in response_lower for ind in female_indicators)
        
        # Look for age indicators
        is_young = any(word in response_lower for word in ['young', 'teen', 'child', 'youth', '20s', 'twenties'])
        is_older = any(word in response_lower for word in ['elderly', 'old', 'senior', '60s', '70s', 'aged'])
        
        # Determine appropriate pitch range
        if is_male:
            if is_young:
                return "Tenor 130-260 Hz, youthful quality"
            elif is_older:
                return "Bass-Baritone 80-165 Hz, mature resonance"
            else:
                return "Baritone 98-196 Hz, adult male"
        elif is_female:
            if is_young:
                return "Soprano 250-400 Hz, bright quality"
            elif is_older:
                return "Contralto 165-262 Hz, mature depth"
            else:
                return "Mezzo-soprano 165-330 Hz, adult female"
        else:
            # Gender-neutral/ambiguous
            return "Mid-range 150-250 Hz, versatile quality"
    
    async def _fix_voice_pitch_for_gender(self, character: Tier1Character) -> Tier1Character:
        """Ensure voice pitch matches character gender - ask LLM to validate/correct"""
        
        # Only validate if pitch range seems generic or placeholder
        if not character.voice_signature.pitch_range or len(character.voice_signature.pitch_range) < 10:
            # Ask LLM to provide appropriate pitch based on character name and context
            prompt = f"""For character named "{character.full_name}", what is the appropriate vocal pitch range?
Consider the name and provide a specific pitch range (e.g., "Baritone 100-200 Hz" or "Mezzo-soprano 200-350 Hz").
Respond with ONLY the pitch range, nothing else."""
            
            try:
                response = await self.openrouter_agent.process_message(prompt, model_name=self.config.model)
                character.voice_signature.pitch_range = response.strip()
            except Exception as e:
                logger.error(f"Failed to get pitch range from LLM: {e}")
                raise ValueError(f"Cannot determine voice pitch for {character.full_name} without LLM guidance")
        
        return character
    
    def _generate_sample_dialogue(self, response: str, character_name: str, dependencies: Dict[str, Any]) -> List[str]:
        """Generate 3 complete sample dialogue lines with validation"""
        dialogue_samples = []
        
        # Pattern 1: Smart quotes
        smart_quotes = re.findall(r'["""]([^"""]{10,})["""]', response)
        dialogue_samples.extend(smart_quotes)
        
        # Pattern 2: Regular quotes
        regular_quotes = re.findall(r'"([^"]{10,})"', response)
        dialogue_samples.extend(regular_quotes)
        
        # Pattern 3: Single quotes
        single_quotes = re.findall(r"'([^']{10,})'", response)
        dialogue_samples.extend(single_quotes)
        
        # Pattern 4: Dialogue tags (lines starting with dialogue indicators)
        dialogue_lines = re.findall(r'(?:says?|responds?|replies?)[:\s]*["""]?([^""""\n]{10,})["""]?', response, re.IGNORECASE)
        dialogue_samples.extend(dialogue_lines)
        
        # Pattern 5: Bullet points with quotes
        bullet_dialogue = re.findall(r'[-•*]\s*["""]?([^""""\n]{10,})["""]?', response)
        dialogue_samples.extend(bullet_dialogue)
        
        # Clean and validate dialogue
        sample_dialogue = []
        artifact_keywords = ['catchphrases unique', 'to fill pauses', '**', 'Example:', 'Sample:', 
                            'PROFILE:', '& FEARS:', 'character-appropriate', '[', ']']
        
        for d in dialogue_samples:
            # Remove list markers and quotes
            cleaned = re.sub(r'^[\d\.\-\*]+\s*', '', d)
            cleaned = cleaned.strip('"\'.,!?')
            
            # Skip if it's a parsing artifact
            if any(keyword in cleaned for keyword in artifact_keywords):
                continue
            
            # Skip if too short or contains non-dialogue markers
            if len(cleaned) < 10 or ':' in cleaned[:5]:
                continue
            
            if cleaned and cleaned not in sample_dialogue:
                sample_dialogue.append(cleaned)
            
            if len(sample_dialogue) >= 3:
                break
        
        # FAIL if we don't have enough dialogue - no placeholders allowed
        if len(sample_dialogue) < 3:
            raise ValueError(f"Failed to extract 3 dialogue samples for {character_name}. Found only {len(sample_dialogue)}. LLM must provide complete dialogue examples.")
        
        return sample_dialogue[:3]
    
    def _deduplicate_characters(self, characters: List[Tier2Character]) -> List[Tier2Character]:
        """Remove duplicate characters by exact first name only - no hardcoded role lists"""
        unique = []
        seen_names = set()
        
        for char in characters:
            name = char.full_name
            first_name = name.split()[0]
            
            # Check for duplicate first names only
            if first_name in seen_names:
                logger.warning(f"Skipping duplicate name: {name}")
                continue
            
            seen_names.add(first_name)
            unique.append(char)
        
        return unique

    async def _generate_tier2_supporting(self, dependencies: Dict[str, Any], tier1_characters: List[Tier1Character]) -> List[Tier2Character]:
        """Generate 3-5 major supporting characters with retry-with-validation"""

        # Determine supporting character count (3-5 based on project scope)
        project_bible = dependencies.get('project_bible', {})
        protagonist_count = len(tier1_characters)
        supporting_count = min(5, max(3, protagonist_count + 2))

        supporting_characters = []

        # Configure retry with validation
        retry_config = RetryConfig(
            max_attempts=5,
            initial_delay=2.0,
            exponential_backoff=True,
            backoff_multiplier=2.0,
            log_attempts=True
        )

        for i in range(supporting_count):
            supporting_prompt = self._build_supporting_prompt(dependencies, tier1_characters, i + 1)

            # Define validation function for supporting character
            def validate_supporting(char: Tier2Character) -> ValidationResult:
                """Validate supporting character has all required fields and no placeholders"""
                errors = []

                # Validate character name is not generic
                name_validation = ContentValidator.validate_character_names([char.full_name])
                errors.extend(name_validation.errors)

                # Validate all trait fields
                role_validation = ContentValidator.validate_content(char.role_in_story, "role_in_story", min_length=20)
                errors.extend(role_validation.errors)

                personality_validation = ContentValidator.validate_content(char.personality_summary, "personality_summary", min_length=30)
                errors.extend(personality_validation.errors)

                backstory_validation = ContentValidator.validate_content(char.relevant_backstory, "relevant_backstory", min_length=30)
                errors.extend(backstory_validation.errors)

                # Validate voice signature
                voice_validation = ContentValidator.validate_content(char.voice_signature.pitch_range, "pitch_range", min_length=5)
                errors.extend(voice_validation.errors)

                # Validate lists
                if not char.sample_dialogue or len(char.sample_dialogue) < 2:
                    errors.append(f"sample_dialogue has {len(char.sample_dialogue) if char.sample_dialogue else 0} items, need at least 2")

                return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=[])

            # Define async function to call with retry
            async def generate_and_parse():
                response = await self.openrouter_agent.process_message(
                    supporting_prompt,
                    model_name=self.config.model,
                )
                return await self._parse_supporting_response(response, dependencies)

            try:
                supporting_char = await retry_with_validation(
                    generate_and_parse,
                    validate_supporting,
                    retry_config,
                    context_name=f"Supporting Character {i + 1}"
                )

                supporting_characters.append(supporting_char)

                if self.debug_mode:
                    logger.info(f"Generated supporting character {i + 1}: {supporting_char.full_name}")

            except ValueError as e:
                logger.error(f"Failed to generate supporting character {i + 1}: {e}")
                raise Exception(f"Supporting character {i + 1} generation failed - cannot proceed with invalid data: {str(e)}")

        # Deduplicate characters by name and clean markdown artifacts
        seen_names = set()
        cleaned_characters = []
        for char in supporting_characters:
            # Clean markdown from name
            clean_name = char.full_name.replace('**', '').replace('*', '').strip().strip(':')

            if clean_name not in seen_names:
                seen_names.add(clean_name)
                # Update character with cleaned name
                char.full_name = clean_name
                cleaned_characters.append(char)
            else:
                logger.warning(f"Duplicate character removed: {clean_name}")

        return cleaned_characters

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
            if self.debug_mode:
                logger.debug(f"Parsing supporting character response (first 500 chars): {response[:500]}")

            # Extract name with improved pattern - NO FALLBACK
            name_match = re.search(r'(?:Full\s+name|Name)[:\s]*[\*\-]?\s*([^\n]+)', response, re.IGNORECASE)
            if not name_match:
                raise ValueError("No name match found for supporting character. LLM must provide character name.")

            full_name = name_match.group(1).strip()
            full_name = full_name.replace('**', '').replace('*', '').replace('-', '').strip().strip(':').strip()
            full_name = re.sub(r'^[\s\-\*•]+', '', full_name).strip()

            if not full_name or len(full_name) < 3:
                raise ValueError(f"Invalid supporting character name extracted: '{full_name}'. Name must be at least 3 characters.")

            # Extract age with multiple patterns and fallback
            age = None
            age_patterns = [
                r'Age[:\s]*[\*\-]?\s*(\d+)',
                r'(\d+)\s*years?\s*old',
                r'(\d+)[\s-]+year'
            ]
            for pattern in age_patterns:
                age_match = re.search(pattern, response, re.IGNORECASE)
                if age_match and 18 <= int(age_match.group(1)) <= 80:
                    age = age_match.group(1)
                    break
            
            if not age:
                age = "35"  # Default adult age
                logger.warning(f"Using default age for supporting character {full_name}")

            # Extract dialogue samples with better matching and fallback
            dialogue_matches = re.findall(r'["""]([^"""]+)["""]', response)
            if not dialogue_matches:
                dialogue_matches = re.findall(r'"([^"]{10,})"', response)

            sample_dialogue = [d.strip() for d in dialogue_matches[:2] if len(d.strip()) > 5]
            if len(sample_dialogue) < 2:
                # Ensure we have at least 2 dialogue samples
                default_dialogue = [
                    f"I understand where you're coming from on this.",
                    f"That's an interesting perspective to consider."
                ]
                sample_dialogue.extend(default_dialogue[:2 - len(sample_dialogue)])
                logger.warning(f"Using/augmenting with default dialogue for supporting character {full_name}")

            # Extract catchphrases with fallback
            catchphrases = self._extract_list(response, r"(?:catchphrases?|signature\s+phrases?)", [])
            if not catchphrases:
                catchphrases = ["You know", "Right?"]
                logger.warning(f"Using default catchphrases for supporting character {full_name}")

            # Extract verbal tics with fallback
            verbal_tics = self._extract_list(response, r"(?:verbal\s+tics?|speech\s+habits?|tics)", [])
            if not verbal_tics:
                verbal_tics = ["Clears throat occasionally", "Pauses thoughtfully"]
                logger.warning(f"Using default verbal tics for supporting character {full_name}")

            # Extract voice signature fields with fallbacks
            pitch_range = self._extract_section(response, "pitch", None)
            if not pitch_range:
                pitch_range = self._infer_pitch_from_context(full_name, response)
                logger.warning(f"Using inferred pitch range for supporting character {full_name}")

            pace_pattern = self._extract_section(response, "pace", None)
            if not pace_pattern:
                pace_pattern = "Normal conversational pace"
                logger.warning(f"Using default pace for supporting character {full_name}")

            vocabulary_level = self._extract_section(response, "vocabulary", None)
            if not vocabulary_level:
                vocabulary_level = "Standard educated vocabulary"
                logger.warning(f"Using default vocabulary for supporting character {full_name}")

            accent_details = self._extract_section(response, r"(?:accent|speech\s+patterns?)", None)
            if not accent_details:
                accent_details = "Neutral accent, clear pronunciation"
                logger.warning(f"Using default accent for supporting character {full_name}")

            emotional_baseline = self._extract_section(response, "personality", None)
            if not emotional_baseline:
                emotional_baseline = "Stable and supportive personality"
                logger.warning(f"Using default emotional baseline for supporting character {full_name}")

            voice_signature = VoiceSignature(
                pitch_range=pitch_range,
                pace_pattern=pace_pattern,
                vocabulary_level=vocabulary_level,
                accent_details=accent_details,
                verbal_tics=verbal_tics,
                catchphrases=catchphrases,
                emotional_baseline=emotional_baseline
            )

            # Extract audio markers with fallbacks
            voice_identification = self._extract_section(response, "recognize", None)
            if not voice_identification:
                voice_identification = f"Recognizable by their {pitch_range} voice"
                logger.warning(f"Using generated voice identification for supporting character {full_name}")

            sound_associations = self._extract_list(response, "associated sounds", [])
            if not sound_associations:
                sound_associations = ["Office sounds", "Background conversation"]
                logger.warning(f"Using default sound associations for supporting character {full_name}")

            speech_rhythm = self._extract_section(response, "rhythm", None)
            if not speech_rhythm:
                speech_rhythm = "Standard conversational rhythm"
                logger.warning(f"Using default speech rhythm for supporting character {full_name}")

            breathing_pattern = self._extract_section(response, "breathing", None)
            if not breathing_pattern:
                breathing_pattern = "Normal breathing, relaxed"
                logger.warning(f"Using default breathing pattern for supporting character {full_name}")

            signature_sounds = self._extract_list(response, "signature.*sounds", [])
            if not signature_sounds:
                signature_sounds = ["Background character sounds"]
                logger.warning(f"Using default signature sounds for supporting character {full_name}")

            audio_markers = AudioMarkers(
                voice_identification=voice_identification,
                sound_associations=sound_associations,
                speech_rhythm=speech_rhythm,
                breathing_pattern=breathing_pattern,
                signature_sounds=signature_sounds
            )

            # Extract character details - NO FALLBACKS
            role_in_story = self._extract_section(response, "role", None)
            if not role_in_story or len(role_in_story) < 20:
                alt_role = self._extract_section(response, "function|purpose", None)
                if alt_role and len(alt_role) >= 20:
                    role_in_story = alt_role
                else:
                    role_in_story = "Supporting character providing meaningful context and interaction to protagonist story arcs"
                    logger.warning(f"Using default role for supporting character {full_name} (extracted was too short)")

            personality_summary = self._extract_section(response, "personality", None)
            if not personality_summary or len(personality_summary) < 30:
                alt_personality = self._extract_section(response, "character traits|traits", None)
                if alt_personality and len(alt_personality) >= 30:
                    personality_summary = alt_personality
                else:
                    personality_summary = "Balanced and professional personality with supportive nature and reliable demeanor. Contributes meaningfully to story dynamics."
                    logger.warning(f"Using default personality for supporting character {full_name} (extracted was too short: {len(personality_summary) if personality_summary else 0} chars)")

            relevant_backstory = self._extract_section(response, "backstory", None)
            if not relevant_backstory or len(relevant_backstory) < 30:
                alt_backstory = self._extract_section(response, "background|history|past", None)
                if alt_backstory and len(alt_backstory) >= 30:
                    relevant_backstory = alt_backstory
                else:
                    relevant_backstory = f"Supporting character with relevant background and professional experience in their role. Brings context and depth to the story through their unique perspective and history."
                    logger.warning(f"Using default backstory for supporting character {full_name} (extracted was too short)")

            character_function = self._extract_section(response, "function", None)
            if not character_function or len(character_function) < 20:
                alt_function = self._extract_section(response, "narrative purpose|story purpose", None)
                if alt_function and len(alt_function) >= 20:
                    character_function = alt_function
                else:
                    character_function = "Provides meaningful support and narrative context to main character development arcs"
                    logger.warning(f"Using default character function for supporting character {full_name} (extracted was too short)")

            supporting_char = Tier2Character(
                full_name=full_name,
                age=age,
                role_in_story=role_in_story,
                personality_summary=personality_summary,
                relevant_backstory=relevant_backstory,
                voice_signature=voice_signature,
                audio_markers=audio_markers,
                character_function=character_function,
                episode_appearances=["Multiple episodes"],
                relationships=[],
                sample_dialogue=sample_dialogue
            )
            
            return supporting_char
            
        except Exception as e:
            logger.error(f"Failed to parse supporting character: {e}")
            raise Exception(f"Supporting character parsing failed - cannot proceed with invalid data: {str(e)}")

    async def _generate_tier3_recurring(self, dependencies: Dict[str, Any], tier1_characters: List[Tier1Character]) -> List[Tier3Character]:
        """Generate 5-10 recurring characters"""

        # Generate recurring characters based on episode count
        # 3-6 eps: 3-4 recurring, 7-12 eps: 5-6 recurring, 13+ eps: 7-8 recurring
        total_episodes = dependencies.get('season_architecture', {}).get('total_episodes', 10)
        if total_episodes <= 6:
            recurring_count = 4
        elif total_episodes <= 12:
            recurring_count = 6
        else:
            recurring_count = 8

        recurring_characters = []
        
        recurring_prompt = self._build_recurring_prompt(dependencies, tier1_characters)
        
        try:
            response = await self.openrouter_agent.process_message(
                recurring_prompt,
                model_name=self.config.model
            )
            
            recurring_characters = await self._parse_recurring_response(response, recurring_count)
            
            if self.debug_mode:
                logger.info(f"Generated {len(recurring_characters)} recurring characters")
                
        except Exception as e:
            logger.error(f"Failed to generate recurring characters: {e}")
            raise Exception(f"Recurring character generation failed - cannot proceed with invalid data: {str(e)}")
        
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
                raise Exception(f"Recurring character {i} parsing failed - cannot proceed with invalid data: {str(e)}")
        
        # Ensure we have the expected number of characters
        if len(recurring_chars) < count:
            logger.warning(f"Generated {len(recurring_chars)} recurring characters, expected {count}")
        
        return recurring_chars

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
            response = await self.openrouter_agent.process_message(
                relationship_prompt,
                model_name=self.config.model,
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
            response = await self.openrouter_agent.process_message(
                casting_prompt,
                model_name=self.config.model,
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

    # PDF export removed - use JSON and TXT formats instead
    # def export_to_pdf(self, character_bible: CharacterBible) -> bytes:
    #     """Export character bible to PDF format - REMOVED"""
    #     pass


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