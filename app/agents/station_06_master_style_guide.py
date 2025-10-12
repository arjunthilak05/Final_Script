#!/usr/bin/env python3
"""
Station 6: Master Style Guide - Complete Implementation
You are the Master Style Guide Builder for audio-only drama production

REFACTORED: NO FALLBACK CONTENT. FAIL LOUDLY. RETRY WITH VALIDATION.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from io import BytesIO

from app.redis_client import RedisClient
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
class LanguageRules:
    """Complete language framework for audio drama"""
    vocabulary_ceiling: str
    forbidden_words: List[str]
    preferred_alternatives: Dict[str, str]
    max_sentence_length: int
    complexity_ratios: Dict[str, float]
    technical_term_protocols: List[str]
    narrator_voice_traits: List[str]
    tense_consistency_rules: List[str]
    transition_phrases: List[str]

@dataclass
class CharacterVoice:
    """Individual character voice specification"""
    character_name: str
    voice_signature: str
    accent_traits: List[str]
    vocabulary_level: str
    speech_patterns: List[str]
    emotional_range: str
    code_switching_triggers: List[str]

@dataclass
class DialectAccentMap:
    """Complete character voice distinction framework"""
    character_voices: List[CharacterVoice]
    regional_markers: Dict[str, List[str]]
    pronunciation_guide: Dict[str, str]
    voice_evolution_rules: List[str]
    cultural_speech_patterns: Dict[str, List[str]]

@dataclass
class AudioConvention:
    """Individual audio convention specification"""
    convention_type: str
    audio_signature: str
    usage_rules: List[str]
    timing_guidelines: str
    integration_notes: str

@dataclass
class AudioConventionsFramework:
    """Complete sonic storytelling language"""
    scene_transitions: List[AudioConvention]
    temporal_markers: List[AudioConvention]
    environmental_signatures: Dict[str, str]
    silence_protocols: List[str]
    perspective_shift_cues: List[str]

@dataclass
class DialoguePrinciples:
    """Natural conversation framework for audio"""
    naturalism_balance: str
    character_id_frequency: str
    subtext_conversion_ratio: str
    interruption_protocols: List[str]
    exposition_integration_methods: List[str]
    emotional_expression_guidelines: List[str]
    multi_character_management: List[str]

@dataclass
class NarrationStyle:
    """Complete narration framework"""
    narrator_personality: str
    activation_triggers: List[str]
    knowledge_scope: str
    emotional_involvement_level: str
    reliability_level: str
    voice_characteristics: List[str]
    screenplay_integration: List[str]

@dataclass
class SonicSignature:
    """Unique audio identity system"""
    main_theme_variations: List[str]
    character_musical_signatures: Dict[str, str]
    emotional_audio_palette: Dict[str, str]
    environmental_soundscapes: Dict[str, str]
    recurring_audio_elements: List[str]
    motif_applications: List[str]

@dataclass
class MasterStyleGuide:
    """Complete Master Style Guide document"""
    working_title: str
    session_id: str
    created_timestamp: datetime

    # Project context integration
    project_context: Dict[str, Any]
    comprehensive_profile: Dict[str, str]

    # Six main sections
    language_rules: LanguageRules
    dialect_accent_map: DialectAccentMap
    audio_conventions: AudioConventionsFramework
    dialogue_principles: DialoguePrinciples
    narration_style: Optional[NarrationStyle]
    sonic_signature: SonicSignature

    # Implementation guidance
    implementation_guidelines: List[str]
    quality_control_checklist: List[str]
    executive_summary: str

class Station06MasterStyleGuideBuilder:
    """Complete Master Style Guide Builder with comprehensive creative framework"""

    def __init__(self):
        self.session_id = None
        self.openrouter = None
        self.redis = None

    async def initialize(self):
        """Initialize OpenRouter client and Redis for AI processing"""
        from app.openrouter_agent import OpenRouterAgent
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        await self.redis.initialize()
        logger.info("Station 6: Master Style Guide Builder initialized")

    async def process(self, session_id: str) -> MasterStyleGuide:
        """
        Main processing method: Complete Master Style Guide Creation
        Follows your exact specification for Station 6
        """
        self.session_id = session_id
        logger.info(f"Starting Station 6: Master Style Guide for session {session_id}")

        # Gather comprehensive inputs from ALL previous stations (1-5)
        project_inputs = await self._gather_comprehensive_inputs(session_id)

        # SECTION 1: Language Rules System
        language_rules = await self._create_language_rules_system(project_inputs)

        # SECTION 2: Dialect & Accent Map
        dialect_accent_map = await self._create_dialect_accent_map(project_inputs)

        # SECTION 3: Audio Conventions Framework
        audio_conventions = await self._create_audio_conventions_framework(project_inputs)

        # SECTION 4: Dialogue Principles System
        dialogue_principles = await self._create_dialogue_principles_system(project_inputs)

        # SECTION 5: Narration Style System (if applicable)
        narration_style = await self._create_narration_style_system(project_inputs)

        # SECTION 6: Sonic Signature System
        sonic_signature = await self._create_sonic_signature_system(project_inputs)

        # Package complete Master Style Guide
        style_guide = self._create_complete_style_guide(
            project_inputs, language_rules, dialect_accent_map, audio_conventions,
            dialogue_principles, narration_style, sonic_signature, session_id
        )

        # Save to Redis before returning
        try:
            output_dict = self.export_to_json(style_guide)
            key = f"audiobook:{session_id}:station_06"
            json_str = json.dumps(output_dict, default=str)
            await self.redis.set(key, json_str, expire=86400)  # 24 hour expiry
            logger.info(f"Station 6 output stored successfully in Redis at key: {key}")
        except Exception as e:
            logger.error(f"Failed to store Station 6 output to Redis: {str(e)}")
            raise

        logger.info(f"Station 6 completed: Master Style Guide for {style_guide.working_title}")
        return style_guide

    async def _gather_comprehensive_inputs(self, session_id: str) -> Dict[str, Any]:
        """
        Gather and integrate inputs from ALL previous stations exactly as specified
        NO HARDCODED DEFAULTS - Validate that data exists from previous stations
        """
        logger.info("Gathering comprehensive inputs from ALL Stations 1-5")

        # Initialize with None - NO DEFAULTS
        inputs = {
            "session_id": session_id,
            "working_title": None,
            "episode_count": None,
            "episode_length": None,
            "core_premise": None,
            "primary_genre": None,
            "secondary_genres": [],
            "target_age_range": None,
            "content_rating": None,
            "total_seeds": 0,
            "narrator_strategy": None,
            "narrator_presence_level": None,
            "chosen_screenplay_style": None,
            "total_episodes": None,
            "main_characters": [],
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
                working_title = working_titles[0] if working_titles else None

                # Extract main characters from Station 1
                main_characters_raw = station1.get("initial_expansion", {}).get("main_characters", [])
                # Clean character names - extract just the name from "**Name:** description" format
                main_characters = self._extract_character_names(main_characters_raw)

                inputs.update({
                    "working_title": working_title,
                    "core_premise": station1.get("initial_expansion", {}).get("core_premise") or None,
                    "original_seed": station1.get("original_seed") or None,
                    "main_characters": main_characters,
                    "episode_count": scale_data.get("episode_count") or None,
                    "episode_length": scale_data.get("episode_length") or None,
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
                    "primary_genre": station2.get("genre_tone", {}).get("primary_genre") or None,
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
                    "target_age_range": station3.get("age_guidelines", {}).get("target_age_range") or None,
                    "content_rating": station3.get("age_guidelines", {}).get("content_rating") or None,
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
                    "narrator_strategy": narrator_strategy.get("identity_type") or None,
                    "narrator_presence_level": narrator_strategy.get("presence_level") or None,
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

        # Station 5: Season architecture
        try:
            station5_data = await self.redis.get(f"audiobook:{session_id}:station_05")
            if station5_data:
                station5 = json.loads(station5_data)
                inputs.update({
                    "chosen_screenplay_style": station5.get("chosen_style") or None,
                    "total_episodes": station5.get("total_episodes") or None,
                    "confidence_score": station5.get("confidence_score", 0.85),
                    "tension_peaks": station5.get("tension_peaks", [2, 5, 7, 10]),
                    "breathing_room": station5.get("breathing_room", [1, 4, 6]),
                    "narrator_integration": station5.get("narrator_integration", ""),
                    "style_recommendations_count": station5.get("style_recommendations", 3)
                })
                logger.info(f"Station 5 data loaded: {inputs['chosen_screenplay_style']}")
        except Exception as e:
            logger.warning(f"Failed to load Station 5 data: {e}")

        # VALIDATE CRITICAL INPUTS - Fail loudly if missing
        required_inputs = ['working_title', 'core_premise', 'primary_genre', 'target_age_range', 'content_rating']
        missing = [k for k in required_inputs if not inputs.get(k)]
        if missing:
            raise ValueError(
                f"Station 6 cannot proceed: Missing required inputs from previous stations: {missing}\n"
                f"Ensure Stations 1-5 have run successfully."
            )

        # Validate main_characters specifically
        if inputs.get('main_characters'):
            validation = ContentValidator.validate_character_names(inputs['main_characters'])
            validate_and_raise(validation, "Main Characters from Station 1")

        # Create comprehensive profile integrating ALL station data
        inputs["comprehensive_profile"] = {
            "scale": f"{inputs['episode_count']} episodes × {inputs['episode_length']}",
            "genre_blend": f"{inputs['primary_genre']}" + (f" + {' + '.join(inputs['secondary_genres'])}" if inputs['secondary_genres'] else ""),
            "audience_target": f"{inputs['target_age_range']} ({inputs['content_rating']})",
            "story_foundation": f"{inputs['total_seeds']} narrative seeds available",
            "narrator_integration": f"{inputs['narrator_strategy']} with {inputs['narrator_presence_level'].lower()} presence" if inputs['narrator_strategy'] and inputs['narrator_presence_level'] else "No narrator",
            "screenplay_style": f"{inputs['chosen_screenplay_style']} structure" if inputs['chosen_screenplay_style'] else "Structure TBD",
            "production_readiness": "Complete foundation from Stations 1-5"
        }

        logger.info(f"Comprehensive inputs gathered for '{inputs['working_title']}' - {inputs['comprehensive_profile']['genre_blend']}")
        return inputs

    def _extract_json_from_response(self, response: str) -> str:
        """
        Extract JSON from LLM response that might include markdown formatting.
        Handles cases like:
        - Plain JSON
        - ```json ... ```
        - Text before/after JSON
        """
        import re
        
        # Try to find JSON in markdown code fences
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find JSON object directly
        json_match = re.search(r'(\{.*\})', response, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Return as-is if no patterns match
        return response.strip()
    
    def _extract_character_names(self, character_descriptions: List[str]) -> List[str]:
        """
        Extract clean character names from bullet point descriptions.
        
        Handles formats like:
        - "**Tom:** The morning motivation coach..."
        - "**Julia:** The depressed ER doctor..."
        - "Tom: description"
        - "Tom - description"
        
        Returns just the names: ["Tom", "Julia"]
        """
        import re
        clean_names = []
        
        for desc in character_descriptions:
            if not desc or not desc.strip():
                continue
            
            # Remove leading/trailing whitespace
            desc = desc.strip()
            
            # Try to extract name from various formats
            # Pattern 1: **Name:** or **Name** or Name:
            match = re.match(r'^\*\*([^*:]+)\*\*:?', desc)
            if match:
                clean_names.append(match.group(1).strip())
                continue
            
            # Pattern 2: Name: description or Name - description
            match = re.match(r'^([^:*\-]+)[:\-]', desc)
            if match:
                name = match.group(1).strip()
                # Make sure it's not empty and doesn't contain markdown or bullet characters
                if name and len(name) >= 2 and not any(c in name for c in ['*', '-', '•']):
                    clean_names.append(name)
                    continue
            
            # Pattern 3: Just take the first word if it looks like a name (starts with capital)
            words = desc.split()
            if words and words[0] and words[0][0].isupper() and words[0].isalpha():
                clean_names.append(words[0])
        
        return clean_names

    async def _create_language_rules_system(self, project_inputs: Dict[str, Any]) -> LanguageRules:
        """
        SECTION 1: LANGUAGE RULES SYSTEM
        Create authoritative language framework integrating age rating and narrator strategy
        NO FALLBACKS - Retry with validation until success
        """
        logger.info("Creating comprehensive language rules system")

        # Create validator for language rules
        def validate_language_rules(result: Dict[str, Any]) -> ValidationResult:
            validation = ContentValidator.validate_required_fields(result, [
                'vocabulary_ceiling', 'forbidden_words', 'max_sentence_length',
                'technical_term_protocols', 'narrator_voice_traits'
            ])
            return validation

        # Build prompt for LLM
        prompt = self._build_language_rules_prompt(project_inputs)

        # Use retry mechanism
        async def generate_with_retry():
            response = await self.openrouter.generate(
                prompt=prompt,
                max_tokens=4000
            )
            # Extract JSON from response (handles markdown formatting)
            json_str = self._extract_json_from_response(response)
            return json.loads(json_str)

        try:
            result = await retry_with_validation(
                generate_with_retry,
                validate_language_rules,
                RetryConfig(max_attempts=5),
                context_name="Language Rules Generation"
            )

            # Convert to LanguageRules dataclass
            return LanguageRules(
                vocabulary_ceiling=result['vocabulary_ceiling'],
                forbidden_words=result['forbidden_words'],
                preferred_alternatives=result.get('preferred_alternatives', {}),
                max_sentence_length=result['max_sentence_length'],
                complexity_ratios=result.get('complexity_ratios', {"simple": 0.5, "compound": 0.3, "complex": 0.2}),
                technical_term_protocols=result['technical_term_protocols'],
                narrator_voice_traits=result['narrator_voice_traits'],
                tense_consistency_rules=result.get('tense_consistency_rules', []),
                transition_phrases=result.get('transition_phrases', [])
            )

        except ValueError as e:
            logger.error(f"Failed to generate valid language rules after retries: {e}")
            raise ValueError(
                f"Station 6 cannot proceed: LLM failed to generate valid language rules.\n"
                f"Error: {e}\n"
                f"NO FALLBACK CONTENT AVAILABLE. Check previous station outputs and retry."
            )

    def _build_language_rules_prompt(self, project_inputs: Dict[str, Any]) -> str:
        """Build detailed prompt for language rules generation"""
        return f"""
Create comprehensive language rules for the audio drama "{project_inputs['working_title']}".

PROJECT CONTEXT:
- Genre: {project_inputs['primary_genre']}
- Target Age: {project_inputs['target_age_range']}
- Content Rating: {project_inputs['content_rating']}
- Premise: {project_inputs['core_premise']}

CRITICAL: Return ONLY a valid JSON object with no additional text, explanations, or markdown formatting.

Required JSON structure:
{{
  "vocabulary_ceiling": "Detailed description of appropriate vocabulary level for this age group",
  "forbidden_words": ["word1", "word2", "word3"],
  "preferred_alternatives": {{"avoid_this": "use_this_instead"}},
  "max_sentence_length": 25,
  "complexity_ratios": {{"simple": 0.6, "compound": 0.3, "complex": 0.1}},
  "technical_term_protocols": ["Rule 1", "Rule 2", "Rule 3"],
  "narrator_voice_traits": ["Trait 1", "Trait 2", "Trait 3"],
  "tense_consistency_rules": ["Rule 1", "Rule 2", "Rule 3"],
  "transition_phrases": ["Phrase 1", "Phrase 2", "Phrase 3"]
}}

Be specific to this story's genre, age group, and themes. No generic placeholders.
Return ONLY the JSON object.
"""

    async def _create_dialect_accent_map(self, project_inputs: Dict[str, Any]) -> DialectAccentMap:
        """
        SECTION 2: DIALECT & ACCENT MAP
        Develop complete character voice distinction framework
        NO FALLBACKS - Retry with validation until success
        """
        logger.info("Creating comprehensive dialect and accent mapping")

        # Create validator for dialect map
        def validate_dialect_map(result: Dict[str, Any]) -> ValidationResult:
            # Validate required fields
            validation = ContentValidator.validate_required_fields(result, [
                'character_voices', 'regional_markers', 'voice_evolution_rules'
            ])
            if not validation.is_valid:
                return validation

            # Validate character names are not generic
            character_names = [cv['character_name'] for cv in result['character_voices']]
            name_validation = ContentValidator.validate_character_names(character_names)
            return name_validation

        # Build prompt for LLM
        prompt = self._build_dialect_map_prompt(project_inputs)

        # Use retry mechanism
        async def generate_with_retry():
            response = await self.openrouter.generate(
                prompt=prompt,
                max_tokens=4000
            )
            # Extract JSON from response (handles markdown formatting)
            json_str = self._extract_json_from_response(response)
            return json.loads(json_str)

        try:
            result = await retry_with_validation(
                generate_with_retry,
                validate_dialect_map,
                RetryConfig(max_attempts=5),
                context_name="Dialect & Accent Map Generation"
            )

            # Convert to DialectAccentMap dataclass
            character_voices = [
                CharacterVoice(
                    character_name=cv['character_name'],
                    voice_signature=cv['voice_signature'],
                    accent_traits=cv['accent_traits'],
                    vocabulary_level=cv['vocabulary_level'],
                    speech_patterns=cv['speech_patterns'],
                    emotional_range=cv['emotional_range'],
                    code_switching_triggers=cv.get('code_switching_triggers', [])
                )
                for cv in result['character_voices']
            ]

            return DialectAccentMap(
                character_voices=character_voices,
                regional_markers=result['regional_markers'],
                pronunciation_guide=result.get('pronunciation_guide', {}),
                voice_evolution_rules=result['voice_evolution_rules'],
                cultural_speech_patterns=result.get('cultural_speech_patterns', {})
            )

        except ValueError as e:
            logger.error(f"Failed to generate valid dialect map after retries: {e}")
            raise ValueError(
                f"Station 6 cannot proceed: LLM failed to generate valid dialect/accent map.\n"
                f"Error: {e}\n"
                f"NO FALLBACK CONTENT AVAILABLE. Check character data from Station 1 and retry."
            )

    def _build_dialect_map_prompt(self, project_inputs: Dict[str, Any]) -> str:
        """Build detailed prompt for dialect map generation"""
        characters = project_inputs.get('main_characters', [])
        return f"""
Create dialect and accent mapping for the audio drama "{project_inputs['working_title']}".

PROJECT CONTEXT:
- Genre: {project_inputs['primary_genre']}
- Main Characters: {', '.join(characters)}
- Premise: {project_inputs['core_premise']}

Generate a JSON object with:
- character_voices: Array of character voice objects with fields:
  - character_name: MUST use actual character names from the story, NOT generic names
  - voice_signature: Distinctive voice description
  - accent_traits: List of accent characteristics
  - vocabulary_level: Education/background level
  - speech_patterns: List of speaking patterns
  - emotional_range: Emotional expression style
  - code_switching_triggers: When character changes speech style
- regional_markers: Dictionary of location-specific speech patterns
- pronunciation_guide: Dictionary of term pronunciations
- voice_evolution_rules: List of how voices change through story
- cultural_speech_patterns: Dictionary of cultural/professional speech patterns

Use actual character names: {', '.join(characters)}
NO generic names like "Main Character" or "Character 1".
"""

    async def _create_audio_conventions_framework(self, project_inputs: Dict[str, Any]) -> AudioConventionsFramework:
        """
        SECTION 3: AUDIO CONVENTIONS FRAMEWORK
        Establish complete sonic storytelling language
        NO FALLBACKS - Retry with validation until success
        """
        logger.info("Creating comprehensive audio conventions framework")

        # Create validator
        def validate_audio_conventions(result: Dict[str, Any]) -> ValidationResult:
            validation = ContentValidator.validate_required_fields(result, [
                'scene_transitions', 'temporal_markers', 'silence_protocols'
            ])
            return validation

        # Build prompt
        prompt = self._build_audio_conventions_prompt(project_inputs)

        # Use retry mechanism
        async def generate_with_retry():
            response = await self.openrouter.generate(
                prompt=prompt,
                max_tokens=4000
            )
            # Extract JSON from response (handles markdown formatting)
            json_str = self._extract_json_from_response(response)
            return json.loads(json_str)

        try:
            result = await retry_with_validation(
                generate_with_retry,
                validate_audio_conventions,
                RetryConfig(max_attempts=5),
                context_name="Audio Conventions Framework Generation"
            )

            # Convert to AudioConventionsFramework dataclass
            scene_transitions = [
                AudioConvention(
                    convention_type=st['convention_type'],
                    audio_signature=st['audio_signature'],
                    usage_rules=st['usage_rules'],
                    timing_guidelines=st['timing_guidelines'],
                    integration_notes=st['integration_notes']
                )
                for st in result['scene_transitions']
            ]

            temporal_markers = [
                AudioConvention(
                    convention_type=tm['convention_type'],
                    audio_signature=tm['audio_signature'],
                    usage_rules=tm['usage_rules'],
                    timing_guidelines=tm['timing_guidelines'],
                    integration_notes=tm['integration_notes']
                )
                for tm in result['temporal_markers']
            ]

            return AudioConventionsFramework(
                scene_transitions=scene_transitions,
                temporal_markers=temporal_markers,
                environmental_signatures=result.get('environmental_signatures', {}),
                silence_protocols=result['silence_protocols'],
                perspective_shift_cues=result.get('perspective_shift_cues', [])
            )

        except ValueError as e:
            logger.error(f"Failed to generate valid audio conventions after retries: {e}")
            raise ValueError(
                f"Station 6 cannot proceed: LLM failed to generate valid audio conventions.\n"
                f"Error: {e}\n"
                f"NO FALLBACK CONTENT AVAILABLE. Check project context and retry."
            )

    def _build_audio_conventions_prompt(self, project_inputs: Dict[str, Any]) -> str:
        """Build detailed prompt for audio conventions generation"""
        return f"""
Create audio conventions framework for "{project_inputs['working_title']}".

PROJECT CONTEXT:
- Genre: {project_inputs['primary_genre']}
- Screenplay Style: {project_inputs.get('chosen_screenplay_style', 'TBD')}
- Premise: {project_inputs['core_premise']}

Generate JSON with:
- scene_transitions: Array of transition objects (convention_type, audio_signature, usage_rules, timing_guidelines, integration_notes)
- temporal_markers: Array of temporal marker objects (same fields)
- environmental_signatures: Dictionary of location audio signatures
- silence_protocols: List of silence usage rules
- perspective_shift_cues: List of POV shift indicators

Be story-specific. No generic content.
"""

    async def _create_dialogue_principles_system(self, project_inputs: Dict[str, Any]) -> DialoguePrinciples:
        """
        SECTION 4: DIALOGUE PRINCIPLES SYSTEM
        Create natural conversation framework for audio
        NO FALLBACKS - Retry with validation until success
        """
        logger.info("Creating comprehensive dialogue principles system")

        # Create validator
        def validate_dialogue_principles(result: Dict[str, Any]) -> ValidationResult:
            validation = ContentValidator.validate_required_fields(result, [
                'naturalism_balance', 'interruption_protocols', 'exposition_integration_methods'
            ])
            return validation

        # Build prompt
        prompt = self._build_dialogue_principles_prompt(project_inputs)

        # Use retry mechanism
        async def generate_with_retry():
            response = await self.openrouter.generate(
                prompt=prompt,
                max_tokens=4000
            )
            # Extract JSON from response (handles markdown formatting)
            json_str = self._extract_json_from_response(response)
            return json.loads(json_str)

        try:
            result = await retry_with_validation(
                generate_with_retry,
                validate_dialogue_principles,
                RetryConfig(max_attempts=5),
                context_name="Dialogue Principles Generation"
            )

            return DialoguePrinciples(
                naturalism_balance=result['naturalism_balance'],
                character_id_frequency=result.get('character_id_frequency', ''),
                subtext_conversion_ratio=result.get('subtext_conversion_ratio', ''),
                interruption_protocols=result['interruption_protocols'],
                exposition_integration_methods=result['exposition_integration_methods'],
                emotional_expression_guidelines=result.get('emotional_expression_guidelines', []),
                multi_character_management=result.get('multi_character_management', [])
            )

        except ValueError as e:
            logger.error(f"Failed to generate valid dialogue principles after retries: {e}")
            raise ValueError(
                f"Station 6 cannot proceed: LLM failed to generate valid dialogue principles.\n"
                f"Error: {e}\n"
                f"NO FALLBACK CONTENT AVAILABLE. Check project context and retry."
            )

    def _build_dialogue_principles_prompt(self, project_inputs: Dict[str, Any]) -> str:
        """Build detailed prompt for dialogue principles generation"""
        return f"""
Create dialogue principles for "{project_inputs['working_title']}".

PROJECT CONTEXT:
- Genre: {project_inputs['primary_genre']}
- Target Age: {project_inputs['target_age_range']}
- Premise: {project_inputs['core_premise']}

Generate JSON with:
- naturalism_balance: Balance between realistic and enhanced dialogue
- character_id_frequency: How often to use character names
- subtext_conversion_ratio: How much subtext to make explicit for audio
- interruption_protocols: List of rules for dialogue interruptions
- exposition_integration_methods: List of natural exposition techniques
- emotional_expression_guidelines: List of emotional delivery rules
- multi_character_management: List of group scene rules

Be story-specific. Consider the genre and age rating.
"""

    async def _create_narration_style_system(self, project_inputs: Dict[str, Any]) -> Optional[NarrationStyle]:
        """
        SECTION 5: NARRATION STYLE SYSTEM (if applicable)
        Based on narrator_strategy from Station 4.5, define complete narration framework
        NO FALLBACKS - Retry with validation until success
        """
        logger.info("Creating comprehensive narration style system")

        narrator_strategy = project_inputs.get("narrator_strategy")

        if not narrator_strategy or narrator_strategy == "Without Narrator":
            logger.info("No narrator strategy selected - skipping narration style")
            return None

        # Create validator
        def validate_narration_style(result: Dict[str, Any]) -> ValidationResult:
            validation = ContentValidator.validate_required_fields(result, [
                'narrator_personality', 'activation_triggers', 'knowledge_scope'
            ])
            return validation

        # Build prompt
        prompt = self._build_narration_style_prompt(project_inputs)

        # Use retry mechanism
        async def generate_with_retry():
            response = await self.openrouter.generate(
                prompt=prompt,
                max_tokens=4000
            )
            # Extract JSON from response (handles markdown formatting)
            json_str = self._extract_json_from_response(response)
            return json.loads(json_str)

        try:
            result = await retry_with_validation(
                generate_with_retry,
                validate_narration_style,
                RetryConfig(max_attempts=5),
                context_name="Narration Style Generation"
            )

            return NarrationStyle(
                narrator_personality=result['narrator_personality'],
                activation_triggers=result['activation_triggers'],
                knowledge_scope=result['knowledge_scope'],
                emotional_involvement_level=result.get('emotional_involvement_level', ''),
                reliability_level=result.get('reliability_level', ''),
                voice_characteristics=result.get('voice_characteristics', []),
                screenplay_integration=result.get('screenplay_integration', [])
            )

        except ValueError as e:
            logger.error(f"Failed to generate valid narration style after retries: {e}")
            raise ValueError(
                f"Station 6 cannot proceed: LLM failed to generate valid narration style.\n"
                f"Error: {e}\n"
                f"NO FALLBACK CONTENT AVAILABLE. Check narrator strategy from Station 4.5 and retry."
            )

    def _build_narration_style_prompt(self, project_inputs: Dict[str, Any]) -> str:
        """Build detailed prompt for narration style generation"""
        return f"""
Create narration style for "{project_inputs['working_title']}".

PROJECT CONTEXT:
- Genre: {project_inputs['primary_genre']}
- Narrator Strategy: {project_inputs['narrator_strategy']}
- Narrator Presence: {project_inputs.get('narrator_presence_level', 'Moderate')}
- Premise: {project_inputs['core_premise']}

Generate JSON with:
- narrator_personality: Detailed personality description
- activation_triggers: List of when narrator speaks
- knowledge_scope: What narrator knows/doesn't know
- emotional_involvement_level: Narrator's emotional engagement
- reliability_level: How reliable/trustworthy the narrator is
- voice_characteristics: List of vocal delivery traits
- screenplay_integration: How narrator supports story structure

Be story-specific. Match the narrator strategy from Station 4.5.
"""

    async def _create_sonic_signature_system(self, project_inputs: Dict[str, Any]) -> SonicSignature:
        """
        SECTION 6: SONIC SIGNATURE SYSTEM
        Create unique audio identity integrating all story elements
        NO FALLBACKS - Retry with validation until success
        """
        logger.info("Creating comprehensive sonic signature system")

        # Create validator
        def validate_sonic_signature(result: Dict[str, Any]) -> ValidationResult:
            validation = ContentValidator.validate_required_fields(result, [
                'main_theme_variations', 'character_musical_signatures', 'emotional_audio_palette'
            ])
            if not validation.is_valid:
                return validation

            # Validate character names in musical signatures
            character_names = list(result['character_musical_signatures'].keys())
            name_validation = ContentValidator.validate_character_names(character_names)
            return name_validation

        # Build prompt
        prompt = self._build_sonic_signature_prompt(project_inputs)

        # Use retry mechanism
        async def generate_with_retry():
            response = await self.openrouter.generate(
                prompt=prompt,
                max_tokens=4000
            )
            # Extract JSON from response (handles markdown formatting)
            json_str = self._extract_json_from_response(response)
            return json.loads(json_str)

        try:
            result = await retry_with_validation(
                generate_with_retry,
                validate_sonic_signature,
                RetryConfig(max_attempts=5),
                context_name="Sonic Signature Generation"
            )

            return SonicSignature(
                main_theme_variations=result['main_theme_variations'],
                character_musical_signatures=result['character_musical_signatures'],
                emotional_audio_palette=result['emotional_audio_palette'],
                environmental_soundscapes=result.get('environmental_soundscapes', {}),
                recurring_audio_elements=result.get('recurring_audio_elements', []),
                motif_applications=result.get('motif_applications', [])
            )

        except ValueError as e:
            logger.error(f"Failed to generate valid sonic signature after retries: {e}")
            raise ValueError(
                f"Station 6 cannot proceed: LLM failed to generate valid sonic signature.\n"
                f"Error: {e}\n"
                f"NO FALLBACK CONTENT AVAILABLE. Check character and story data and retry."
            )

    def _build_sonic_signature_prompt(self, project_inputs: Dict[str, Any]) -> str:
        """Build detailed prompt for sonic signature generation"""
        characters = project_inputs.get('main_characters', [])
        return f"""
Create sonic signature for "{project_inputs['working_title']}".

PROJECT CONTEXT:
- Genre: {project_inputs['primary_genre']}
- Main Characters: {', '.join(characters)}
- Premise: {project_inputs['core_premise']}

Generate JSON with:
- main_theme_variations: List of theme variations
- character_musical_signatures: Dictionary mapping character names to musical descriptions
  - Use actual character names: {', '.join(characters)}
  - NO generic names like "Main Character"
- emotional_audio_palette: Dictionary of emotion-to-audio mappings
- environmental_soundscapes: Dictionary of location soundscapes
- recurring_audio_elements: List of recurring audio motifs
- motif_applications: List of how motifs are used

Be story-specific. Use actual character names from the story.
"""

    def _create_complete_style_guide(self, project_inputs: Dict[str, Any], language_rules: LanguageRules,
                                   dialect_accent_map: DialectAccentMap, audio_conventions: AudioConventionsFramework,
                                   dialogue_principles: DialoguePrinciples, narration_style: Optional[NarrationStyle],
                                   sonic_signature: SonicSignature, session_id: str) -> MasterStyleGuide:
        """Package complete Master Style Guide document"""

        # Create executive summary
        narrator_desc = f"{project_inputs.get('narrator_strategy', 'No')} narration" if project_inputs.get('narrator_strategy') else "No narration"
        executive_summary = f"""
        The Master Style Guide for '{project_inputs.get('working_title', 'this audio drama')}' establishes a comprehensive creative framework for audio-only drama production targeting {project_inputs.get('target_age_range', 'adult')} audiences with {project_inputs.get('content_rating', 'TBD')} content rating.

        This {project_inputs.get('primary_genre', 'drama')} series employs {narrator_desc} within a {project_inputs.get('chosen_screenplay_style', 'TBD')} structure across {project_inputs.get('total_episodes', 'TBD')} episodes. The style guide integrates sophisticated language rules appropriate for the target audience, distinct character voice signatures for audio-only identification, comprehensive audio conventions for temporal and spatial navigation, natural dialogue principles optimized for audio comprehension, and a unique sonic signature that supports both the story's themes and emotional depth.

        All elements work together to create an immersive audio experience that respects audience intelligence while ensuring accessibility and emotional engagement throughout the {project_inputs.get('episode_count', 'TBD')} × {project_inputs.get('episode_length', 'TBD')} season structure.
        """

        return MasterStyleGuide(
            working_title=project_inputs.get("working_title", "Untitled Audio Drama"),
            session_id=session_id,
            created_timestamp=datetime.now(),
            project_context=project_inputs,
            comprehensive_profile=project_inputs.get("comprehensive_profile", {}),
            language_rules=language_rules,
            dialect_accent_map=dialect_accent_map,
            audio_conventions=audio_conventions,
            dialogue_principles=dialogue_principles,
            narration_style=narration_style,
            sonic_signature=sonic_signature,
            implementation_guidelines=[
                "Review character voice signatures before script development to ensure consistency",
                "Apply audio conventions systematically across all episodes for audience orientation",
                "Balance naturalistic dialogue with audio-only comprehension requirements",
                "Integrate sonic signature elements throughout production for unified audio identity",
                "Maintain age-appropriate language while respecting audience sophistication",
                "Use narrator activation triggers consistently to support pacing and comprehension",
                "Test all audio conventions in early episodes to establish audience expectations",
                "Coordinate music and sound design with dialogue pacing for optimal audio experience"
            ],
            quality_control_checklist=[
                "Verify all dialogue follows age-appropriate vocabulary guidelines",
                "Confirm character voice distinctions are clear in audio-only format",
                "Check that technical terms are properly introduced and explained",
                "Ensure audio transitions serve narrative function and maintain clarity",
                "Validate that exposition integration feels natural within dialogue",
                "Test narrator voice consistency across episodes and scenes",
                "Confirm sonic signature elements support rather than distract from story",
                "Verify emotional expression is sufficient for audio-only comprehension",
                "Check that silence protocols are applied consistently for dramatic effect",
                "Ensure all pronunciation guides are followed for character and technical terms"
            ],
            executive_summary=executive_summary.strip()
        )

    def export_to_text(self, style_guide: MasterStyleGuide) -> str:
        """
        Export complete Master Style Guide to formatted text
        """
        output_lines = []

        # Header
        output_lines.extend([
            "STATION 6: MASTER STYLE GUIDE",
            "=" * 80,
            "Complete Creative Framework for Audio-Only Drama Production",
            "",
            f"Working Title: {style_guide.working_title}",
            f"Session ID: {style_guide.session_id}",
            f"Created: {style_guide.created_timestamp}",
            "",
            "EXECUTIVE SUMMARY:"
        ])

        # Wrap long executive summary text
        wrapped_summary = self._wrap_text(style_guide.executive_summary, 80)
        output_lines.extend(wrapped_summary)

        output_lines.extend([
            "",
            "=" * 80,
            ""
        ])

        # SECTION 1: Language Rules
        output_lines.extend([
            "SECTION 1: LANGUAGE RULES SYSTEM",
            "-" * 50,
            "",
            "VOCABULARY ARCHITECTURE:",
            style_guide.language_rules.vocabulary_ceiling,
            "",
            "FORBIDDEN WORDS:"
        ])

        # Format forbidden words with proper line breaks
        forbidden_words = style_guide.language_rules.forbidden_words
        if forbidden_words:
            # Split long lists into multiple lines
            words_per_line = 4
            for i in range(0, len(forbidden_words), words_per_line):
                line_words = forbidden_words[i:i+words_per_line]
                output_lines.append(", ".join(line_words))

        output_lines.extend([
            "",
            "PREFERRED ALTERNATIVES:"
        ])

        for term, alternative in style_guide.language_rules.preferred_alternatives.items():
            output_lines.append(f"  {term} → {alternative}")

        output_lines.extend([
            "",
            f"MAXIMUM SENTENCE LENGTH: {style_guide.language_rules.max_sentence_length} words",
            "",
            "COMPLEXITY RATIOS:"
        ])

        for complexity, ratio in style_guide.language_rules.complexity_ratios.items():
            output_lines.append(f"  {complexity.title()}: {ratio:.1%}")

        output_lines.extend([
            "",
            "TECHNICAL TERM PROTOCOLS:"
        ])
        for protocol in style_guide.language_rules.technical_term_protocols:
            output_lines.append(f"• {protocol}")

        output_lines.extend([
            "",
            "NARRATOR VOICE TRAITS:"
        ])
        for trait in style_guide.language_rules.narrator_voice_traits:
            output_lines.append(f"• {trait}")

        output_lines.extend([
            "",
            "TENSE CONSISTENCY RULES:"
        ])
        for rule in style_guide.language_rules.tense_consistency_rules:
            output_lines.append(f"• {rule}")

        output_lines.extend([
            "",
            "TRANSITION PHRASES:"
        ])

        # Format transition phrases with proper line breaks
        transition_phrases = style_guide.language_rules.transition_phrases
        if transition_phrases:
            # Split long lists into multiple lines
            phrases_per_line = 3
            for i in range(0, len(transition_phrases), phrases_per_line):
                line_phrases = transition_phrases[i:i+phrases_per_line]
                output_lines.append(", ".join(line_phrases))

        output_lines.extend([
            "",
            "=" * 80,
            ""
        ])

        # SECTION 2: Dialect & Accent Map
        output_lines.extend([
            "SECTION 2: DIALECT & ACCENT MAP",
            "-" * 50,
            "",
            "CHARACTER VOICE ARCHITECTURE:"
        ])

        for voice in style_guide.dialect_accent_map.character_voices:
            output_lines.extend([
                "",
                f"CHARACTER: {voice.character_name}",
                f"Voice Signature: {voice.voice_signature}",
                f"Accent Traits: {', '.join(voice.accent_traits)}",
                f"Vocabulary Level: {voice.vocabulary_level}",
                f"Speech Patterns: {', '.join(voice.speech_patterns)}",
                f"Emotional Range: {voice.emotional_range}",
                f"Code-Switching Triggers: {', '.join(voice.code_switching_triggers)}"
            ])

        output_lines.extend([
            "",
            "REGIONAL MARKERS:"
        ])
        for region, markers in style_guide.dialect_accent_map.regional_markers.items():
            output_lines.append(f"  {region}: {', '.join(markers)}")

        output_lines.extend([
            "",
            "PRONUNCIATION GUIDE:"
        ])
        for term, pronunciation in style_guide.dialect_accent_map.pronunciation_guide.items():
            output_lines.append(f"  {term}: {pronunciation}")

        output_lines.extend([
            "",
            "VOICE EVOLUTION RULES:"
        ])
        for rule in style_guide.dialect_accent_map.voice_evolution_rules:
            output_lines.append(f"• {rule}")

        output_lines.extend([
            "",
            "=" * 80,
            ""
        ])

        # SECTION 3: Audio Conventions
        output_lines.extend([
            "SECTION 3: AUDIO CONVENTIONS FRAMEWORK",
            "-" * 50,
            "",
            "SCENE TRANSITIONS:"
        ])

        for convention in style_guide.audio_conventions.scene_transitions:
            output_lines.extend([
                "",
                f"TYPE: {convention.convention_type}",
                f"Audio Signature: {convention.audio_signature}",
                f"Usage Rules: {', '.join(convention.usage_rules)}",
                f"Timing: {convention.timing_guidelines}",
                f"Integration: {convention.integration_notes}"
            ])

        output_lines.extend([
            "",
            "TEMPORAL MARKERS:"
        ])

        for marker in style_guide.audio_conventions.temporal_markers:
            output_lines.extend([
                "",
                f"TYPE: {marker.convention_type}",
                f"Audio Signature: {marker.audio_signature}",
                f"Usage Rules: {', '.join(marker.usage_rules)}",
                f"Timing: {marker.timing_guidelines}",
                f"Integration: {marker.integration_notes}"
            ])

        output_lines.extend([
            "",
            "ENVIRONMENTAL SIGNATURES:"
        ])
        for location, signature in style_guide.audio_conventions.environmental_signatures.items():
            output_lines.append(f"  {location}: {signature}")

        output_lines.extend([
            "",
            "SILENCE PROTOCOLS:"
        ])
        for protocol in style_guide.audio_conventions.silence_protocols:
            output_lines.append(f"• {protocol}")

        output_lines.extend([
            "",
            "=" * 80,
            ""
        ])

        # SECTION 4: Dialogue Principles
        output_lines.extend([
            "SECTION 4: DIALOGUE PRINCIPLES SYSTEM",
            "-" * 50,
            "",
            f"NATURALISM BALANCE: {style_guide.dialogue_principles.naturalism_balance}",
            "",
            f"CHARACTER ID FREQUENCY: {style_guide.dialogue_principles.character_id_frequency}",
            "",
            f"SUBTEXT CONVERSION RATIO: {style_guide.dialogue_principles.subtext_conversion_ratio}",
            "",
            "INTERRUPTION PROTOCOLS:"
        ])

        for protocol in style_guide.dialogue_principles.interruption_protocols:
            output_lines.append(f"• {protocol}")

        output_lines.extend([
            "",
            "EXPOSITION INTEGRATION METHODS:"
        ])
        for method in style_guide.dialogue_principles.exposition_integration_methods:
            output_lines.append(f"• {method}")

        output_lines.extend([
            "",
            "EMOTIONAL EXPRESSION GUIDELINES:"
        ])
        for guideline in style_guide.dialogue_principles.emotional_expression_guidelines:
            output_lines.append(f"• {guideline}")

        output_lines.extend([
            "",
            "=" * 80,
            ""
        ])

        # SECTION 5: Narration Style
        output_lines.extend([
            "SECTION 5: NARRATION STYLE SYSTEM",
            "-" * 50,
            ""
        ])

        if style_guide.narration_style:
            output_lines.extend([
                f"NARRATOR PERSONALITY: {style_guide.narration_style.narrator_personality}",
                "",
                "ACTIVATION TRIGGERS:"
            ])
            for trigger in style_guide.narration_style.activation_triggers:
                output_lines.append(f"• {trigger}")

            output_lines.extend([
                "",
                f"KNOWLEDGE SCOPE: {style_guide.narration_style.knowledge_scope}",
                "",
                f"EMOTIONAL INVOLVEMENT: {style_guide.narration_style.emotional_involvement_level}",
                "",
                f"RELIABILITY LEVEL: {style_guide.narration_style.reliability_level}",
                "",
                "VOICE CHARACTERISTICS:"
            ])
            for characteristic in style_guide.narration_style.voice_characteristics:
                output_lines.append(f"• {characteristic}")

            output_lines.extend([
                "",
                "SCREENPLAY INTEGRATION:"
            ])
            for integration in style_guide.narration_style.screenplay_integration:
                output_lines.append(f"• {integration}")
        else:
            output_lines.append("No narrator strategy selected for this production.")

        output_lines.extend([
            "",
            "=" * 80,
            ""
        ])

        # SECTION 6: Sonic Signature
        output_lines.extend([
            "SECTION 6: SONIC SIGNATURE SYSTEM",
            "-" * 50,
            "",
            "MAIN THEME VARIATIONS:"
        ])

        for variation in style_guide.sonic_signature.main_theme_variations:
            output_lines.append(f"• {variation}")

        output_lines.extend([
            "",
            "CHARACTER MUSICAL SIGNATURES:"
        ])
        for character, signature in style_guide.sonic_signature.character_musical_signatures.items():
            output_lines.append(f"  {character}: {signature}")

        output_lines.extend([
            "",
            "EMOTIONAL AUDIO PALETTE:"
        ])
        for emotion, audio in style_guide.sonic_signature.emotional_audio_palette.items():
            output_lines.append(f"  {emotion}: {audio}")

        output_lines.extend([
            "",
            "ENVIRONMENTAL SOUNDSCAPES:"
        ])
        for environment, soundscape in style_guide.sonic_signature.environmental_soundscapes.items():
            output_lines.append(f"  {environment}: {soundscape}")

        output_lines.extend([
            "",
            "RECURRING AUDIO ELEMENTS:"
        ])
        for element in style_guide.sonic_signature.recurring_audio_elements:
            output_lines.append(f"• {element}")

        output_lines.extend([
            "",
            "=" * 80,
            "",
            "IMPLEMENTATION GUIDELINES:",
            "-" * 30
        ])

        for guideline in style_guide.implementation_guidelines:
            output_lines.append(f"• {guideline}")

        output_lines.extend([
            "",
            "QUALITY CONTROL CHECKLIST:",
            "-" * 30
        ])

        for item in style_guide.quality_control_checklist:
            output_lines.append(f"□ {item}")

        output_lines.extend([
            "",
            "=" * 80,
            "END OF MASTER STYLE GUIDE"
        ])

        return "\n".join(output_lines)

    def export_to_json(self, style_guide: MasterStyleGuide) -> Dict[str, Any]:
        """
        Export complete Master Style Guide to JSON format
        """
        return {
            "station_id": "station_06",
            "working_title": style_guide.working_title,
            "session_id": style_guide.session_id,
            "created_timestamp": style_guide.created_timestamp.isoformat(),
            "executive_summary": style_guide.executive_summary,
            "project_context": style_guide.project_context,
            "comprehensive_profile": style_guide.comprehensive_profile,
            "language_rules": asdict(style_guide.language_rules),
            "dialect_accent_map": asdict(style_guide.dialect_accent_map),
            "audio_conventions": asdict(style_guide.audio_conventions),
            "dialogue_principles": asdict(style_guide.dialogue_principles),
            "narration_style": asdict(style_guide.narration_style) if style_guide.narration_style else None,
            "sonic_signature": asdict(style_guide.sonic_signature),
            "implementation_guidelines": style_guide.implementation_guidelines,
            "quality_control_checklist": style_guide.quality_control_checklist
        }

    def _wrap_text(self, text: str, width: int = 80) -> List[str]:
        """Wrap long text into multiple lines for better formatting"""
        if not text:
            return []

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            # Check if adding this word would exceed the width
            if current_length + len(word) + (1 if current_line else 0) > width:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_length = len(word)
                else:
                    # Single word is longer than width, add it anyway
                    lines.append(word)
                    current_length = 0
            else:
                current_line.append(word)
                current_length += len(word) + (1 if current_line else 0)

        # Add the last line if it has content
        if current_line:
            lines.append(" ".join(current_line))

        return lines
