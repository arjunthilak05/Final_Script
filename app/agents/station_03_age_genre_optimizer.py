"""
Station 3: Age & Genre Optimizer Agent

This agent takes the Project Bible from Station 2 and creates age-appropriate 
content guidelines and optimized genre blending strategies using multi-agent Swarm coordination.

Dependencies: Station 2 Project Bible output
Outputs: Age/Genre Style Guide (3 sections)
Human Gate: IMPORTANT - Style guide affects content production across all episodes
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

logger = logging.getLogger(__name__)

class ViolenceLevel(Enum):
    NONE = "No violence"
    MINIMAL = "Minimal implied violence"
    MILD = "Mild violence without graphic details"
    MODERATE = "Moderate violence with some details"
    STRONG = "Strong violence with graphic elements"

class EmotionalIntensity(Enum):
    LIGHT = "Light emotional content"
    MILD = "Mild emotional situations"
    MODERATE = "Moderate emotional intensity"
    STRONG = "Strong emotional situations"
    INTENSE = "Intense emotional content"

@dataclass
class AgeGuidelines:
    """Age-appropriate content guidelines"""
    target_age_range: str
    content_rating: str
    action_scene_limits: List[str]
    emotional_boundaries: List[str] 
    language_guidelines: Dict[str, str]
    sound_restrictions: List[str]
    theme_complexity: str
    violence_level: ViolenceLevel
    emotional_intensity: EmotionalIntensity
    duration_caps: Dict[str, str]

@dataclass  
class GenreBlend:
    """Genre blending option with audio-specific considerations"""
    primary_genre: str
    complementary_genre: str
    enhancement_analysis: str
    audio_elements: List[str]
    pacing_implications: str
    audience_expectations: str
    signature_sounds: List[str]
    mood_transitions: List[str]

@dataclass
class ToneCalibration:
    """Tone progression and audio conveyance strategies"""
    chosen_blend: str
    episode_progression: List[str]
    tonal_shift_moments: List[str]
    audio_tone_techniques: List[str]
    light_dark_balance: str
    tension_curves: List[str]
    audio_cues: Dict[str, str]

@dataclass
class AgeGenreStyleGuide:
    """Complete Age/Genre Style Guide output"""
    working_title: str
    age_guidelines: AgeGuidelines
    genre_options: List[GenreBlend] 
    tone_calibration: ToneCalibration
    chosen_genre_blend: Optional[str]
    production_notes: List[str]
    session_id: str
    created_timestamp: datetime

class AgeAgent:
    """Specialized agent for age-appropriate content guidelines"""

    def __init__(self, openrouter_agent: OpenRouterAgent, config):
        self.agent = openrouter_agent
        self.config = config
    
    def _parse_violence_level(self, value: str) -> ViolenceLevel:
        """Parse violence level from AI response"""
        value_upper = value.upper().strip()
        for level in ViolenceLevel:
            if level.name in value_upper:
                return level
        # No fallback - raise error if parsing fails
        raise ValueError(f"Failed to parse violence level: '{value}' - no fallback allowed")
    
    def _parse_emotional_intensity(self, value: str) -> EmotionalIntensity:
        """Parse emotional intensity from AI response"""
        value_upper = value.upper().strip()
        for intensity in EmotionalIntensity:
            if intensity.name in value_upper:
                return intensity
        # No fallback - raise error if parsing fails
        raise ValueError(f"Failed to parse emotional intensity: '{value}' - no fallback allowed")
    
    async def analyze_age_requirements(self, project_bible: Dict[str, Any]) -> AgeGuidelines:
        """Create age-appropriate content guidelines"""
        
        audience_profile = project_bible.get('audience_profile', {})
        production_constraints = project_bible.get('production_constraints', {})
        genre_tone = project_bible.get('genre_tone', {})
        
        age_prompt = f"""
        You are an Age-Appropriate Content Specialist for audiobook production.
        
        Based on this Project Bible data:
        - Target Age Range: {audience_profile.get('primary_age_range', 'Unknown')}
        - Content Rating: {production_constraints.get('content_rating', 'Unknown')}
        - Primary Genre: {genre_tone.get('primary_genre', 'Unknown')}
        - Mood Profile: {genre_tone.get('mood_profile', 'Unknown')}
        
        Create comprehensive age-appropriate guidelines in this EXACT JSON format. 
        IMPORTANT: Return ONLY valid, complete JSON - no explanatory text before or after:
        {{
            "target_age_range": "specific age range",
            "content_rating": "rating with justification",
            "action_scene_limits": [
                "specific limit 1",
                "specific limit 2", 
                "specific limit 3"
            ],
            "emotional_boundaries": [
                "boundary 1 with reasoning",
                "boundary 2 with reasoning",
                "boundary 3 with reasoning"
            ],
            "language_guidelines": {{
                "vocabulary_level": "age-appropriate description",
                "forbidden_topics": "topics to avoid",
                "complexity_cap": "sentence/concept complexity limits"
            }},
            "sound_restrictions": [
                "sound type 1 to avoid/limit",
                "sound type 2 to avoid/limit",
                "sound type 3 to avoid/limit"
            ],
            "theme_complexity": "detailed description of appropriate theme depth",
            "violence_level": "NONE/MINIMAL/MILD/MODERATE/STRONG",
            "emotional_intensity": "LIGHT/MILD/MODERATE/STRONG/INTENSE",
            "duration_caps": {{
                "action_scenes": "max duration and reasoning",
                "emotional_scenes": "max duration and reasoning",
                "suspense_buildup": "max duration and reasoning"
            }}
        }}
        
        Focus on AUDIO-SPECIFIC considerations. What sounds, pacing, and content work for this age group?
        """
        
        try:
            response = await self.agent.process_message(
                age_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            # Extract and parse JSON using shared utility
            try:
                data = extract_json(response)
            except ValueError as e:
                logger.warning(f"No JSON found in age analysis response: {response[:200]}...")
                raise ValueError(f"No JSON found in age analysis response: {e}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {str(e)}")
                logger.error(f"Problematic response: {response[:200]}...")
                raise ValueError("Invalid JSON in age analysis response")
            
            return AgeGuidelines(
                target_age_range=data.get('target_age_range', 'Unknown'),
                content_rating=data.get('content_rating', 'Not specified'),
                action_scene_limits=data.get('action_scene_limits', []),
                emotional_boundaries=data.get('emotional_boundaries', []),
                language_guidelines=data.get('language_guidelines', {}),
                sound_restrictions=data.get('sound_restrictions', []),
                theme_complexity=data.get('theme_complexity', 'Not specified'),
                violence_level=self._parse_violence_level(data.get('violence_level', 'NONE')),
                emotional_intensity=self._parse_emotional_intensity(data.get('emotional_intensity', 'LIGHT')),
                duration_caps=data.get('duration_caps', {})
            )
            
        except Exception as e:
            logger.error(f"Age analysis failed: {str(e)}")
            raise ValueError(f"Station 3 age analysis failed - no fallback allowed: {str(e)}")

class GenreAgent:
    """Specialized agent for genre blending and optimization"""

    def __init__(self, openrouter_agent: OpenRouterAgent, config):
        self.agent = openrouter_agent
        self.config = config
    
    async def create_genre_blends(self, project_bible: Dict[str, Any]) -> List[GenreBlend]:
        """Create 3 optimized genre blend options"""
        
        genre_tone = project_bible.get('genre_tone', {})
        format_specs = project_bible.get('format_specifications', {})
        audience_profile = project_bible.get('audience_profile', {})
        
        genre_prompt = f"""
        You are a Genre Blending Specialist for audiobook production.
        
        Based on this Project Bible data:
        - Primary Genre: {genre_tone.get('primary_genre', 'Unknown')}
        - Secondary Genres: {genre_tone.get('secondary_genres', [])}
        - Tone Descriptors: {genre_tone.get('tone_descriptors', [])}
        - Episode Length: {format_specs.get('episode_length', 'Unknown')}
        - Target Age: {audience_profile.get('primary_age_range', 'Unknown')}
        - Listening Context: {audience_profile.get('listening_context', 'Unknown')}
        
        Create 3 distinct genre blend options in this EXACT JSON format.
        IMPORTANT: Return ONLY valid, complete JSON - no explanatory text before or after:
        {{
            "option_a": {{
                "primary_genre": "main genre",
                "complementary_genre": "supporting genre that enhances main",
                "enhancement_analysis": "detailed explanation of how genres work together",
                "audio_elements": [
                    "specific audio element 1",
                    "specific audio element 2",
                    "specific audio element 3"
                ],
                "pacing_implications": "how blend affects episode pacing and rhythm",
                "audience_expectations": "what audiences expect from this combination",
                "signature_sounds": [
                    "unique sound 1 for this blend",
                    "unique sound 2 for this blend"
                ],
                "mood_transitions": [
                    "how mood shifts work in this blend",
                    "transition techniques specific to audio"
                ]
            }},
            "option_b": {{
                "primary_genre": "different main genre approach",
                "complementary_genre": "different supporting genre",
                "enhancement_analysis": "different enhancement strategy",
                "audio_elements": [
                    "different audio element 1",
                    "different audio element 2", 
                    "different audio element 3"
                ],
                "pacing_implications": "different pacing approach",
                "audience_expectations": "different audience appeal",
                "signature_sounds": [
                    "different unique sound 1",
                    "different unique sound 2"
                ],
                "mood_transitions": [
                    "different mood shift approach",
                    "different transition techniques"
                ]
            }},
            "option_c": {{
                "primary_genre": "third main genre approach",
                "complementary_genre": "third supporting genre",
                "enhancement_analysis": "third enhancement strategy",
                "audio_elements": [
                    "third set audio element 1",
                    "third set audio element 2",
                    "third set audio element 3"
                ],
                "pacing_implications": "third pacing strategy",
                "audience_expectations": "third audience approach",
                "signature_sounds": [
                    "third set unique sound 1",
                    "third set unique sound 2"
                ],
                "mood_transitions": [
                    "third mood shift approach",
                    "third transition techniques"
                ]
            }}
        }}
        
        Make each option DISTINCTLY different. Focus on AUDIO-SPECIFIC elements that work without visuals.
        """
        
        try:
            response = await self.agent.process_message(
                genre_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            # Extract and parse JSON using shared utility
            try:
                data = extract_json(response)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {str(e)}")
                logger.error(f"Problematic response: {response[:200]}...")
                raise ValueError("Invalid JSON in genre blend response")
            
            blends = []
            for option_key in ['option_a', 'option_b', 'option_c']:
                if option_key in data:
                    option = data[option_key]
                    blends.append(GenreBlend(
                        primary_genre=option.get('primary_genre', 'Unknown'),
                        complementary_genre=option.get('complementary_genre', 'Unknown'),
                        enhancement_analysis=option.get('enhancement_analysis', 'Not specified'),
                        audio_elements=option.get('audio_elements', []),
                        pacing_implications=option.get('pacing_implications', 'Not specified'),
                        audience_expectations=option.get('audience_expectations', 'Not specified'),
                        signature_sounds=option.get('signature_sounds', []),
                        mood_transitions=option.get('mood_transitions', [])
                    ))
            
            return blends
            
        except Exception as e:
            logger.error(f"Genre blend creation failed: {str(e)}")
            raise ValueError(f"Station 3 genre blend creation failed - no fallback allowed: {str(e)}")

class ToneAgent:
    """Specialized agent for tone calibration and audio conveyance"""

    def __init__(self, openrouter_agent: OpenRouterAgent, config):
        self.agent = openrouter_agent
        self.config = config
    
    async def calibrate_tone(self, project_bible: Dict[str, Any], chosen_blend: GenreBlend) -> ToneCalibration:
        """Create tone progression and audio conveyance strategy"""
        
        format_specs = project_bible.get('format_specifications', {})
        genre_tone = project_bible.get('genre_tone', {})
        
        tone_prompt = f"""
        You are a Tone Calibration Specialist for audiobook production.
        
        Based on this Project Bible and chosen genre blend:
        - Episode Count: {format_specs.get('episode_count', 'Unknown')}
        - Episode Length: {format_specs.get('episode_length', 'Unknown')}
        - Mood Profile: {genre_tone.get('mood_profile', 'Unknown')}
        - Chosen Blend: {chosen_blend.primary_genre} + {chosen_blend.complementary_genre}
        - Enhancement Analysis: {chosen_blend.enhancement_analysis}
        
        Create comprehensive tone calibration in this EXACT JSON format.
        IMPORTANT: Return ONLY valid, complete JSON - no explanatory text before or after:
        {{
            "chosen_blend": "{chosen_blend.primary_genre} + {chosen_blend.complementary_genre}",
            "episode_progression": [
                "Episode 1-3: tone description and purpose",
                "Episode 4-6: tone evolution and changes",
                "Episode 7-9: tone development and intensification",
                "Final episodes: tone resolution and conclusion"
            ],
            "tonal_shift_moments": [
                "Key moment 1: when and how tone shifts",
                "Key moment 2: when and how tone shifts",
                "Key moment 3: when and how tone shifts",
                "Key moment 4: when and how tone shifts"
            ],
            "audio_tone_techniques": [
                "Music technique: how music conveys tone",
                "Voice technique: how narration conveys tone", 
                "Sound design technique: how effects convey tone",
                "Pacing technique: how timing conveys tone",
                "Silence technique: how pauses convey tone"
            ],
            "light_dark_balance": "detailed description of how light and dark moments are balanced throughout",
            "tension_curves": [
                "Episode arc: how tension builds and releases within episodes",
                "Season arc: how tension builds across multiple episodes",
                "Character arc: how emotional tension follows character development"
            ],
            "audio_cues": {{
                "rising_tension": "specific audio technique for building tension",
                "emotional_peak": "specific audio technique for emotional climax",
                "comic_relief": "specific audio technique for lightening mood",
                "resolution": "specific audio technique for satisfying conclusion"
            }}
        }}
        
        Focus on AUDIO-ONLY techniques. How do you convey tone without visuals?
        """
        
        try:
            response = await self.agent.process_message(
                tone_prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            # Extract and parse JSON using shared utility
            try:
                data = extract_json(response)
            except (ValueError, json.JSONDecodeError) as e:
                logger.error(f"Failed to parse JSON from tone calibration: {e}")
                raise ValueError(f"Unable to get valid JSON from tone calibration: {e}")
            
            return ToneCalibration(
                chosen_blend=data.get('chosen_blend', f"{chosen_blend.primary_genre} + {chosen_blend.complementary_genre}"),
                episode_progression=data.get('episode_progression', []),
                tonal_shift_moments=data.get('tonal_shift_moments', []),
                audio_tone_techniques=data.get('audio_tone_techniques', []),
                light_dark_balance=data.get('light_dark_balance', 'Not specified'),
                tension_curves=data.get('tension_curves', []),
                audio_cues=data.get('audio_cues', {})
            )
            
        except Exception as e:
            logger.error(f"❌ CRITICAL: Tone calibration failed: {str(e)}")
            logger.error("Station 3 cannot proceed without valid tone calibration data")
            raise RuntimeError(f"CRITICAL FAILURE in Station 3 tone calibration: {str(e)}")

class Station03AgeGenreOptimizer:
    """Station 3: Age & Genre Optimizer using multi-agent Swarm coordination"""
    
    def __init__(self):
        self.settings = Settings()
        self.openrouter_agent = None
        self.redis_client = None
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=3)
        
        # Initialize specialized agents
        self.age_agent = None
        self.genre_agent = None
        self.tone_agent = None
    
    async def initialize(self):
        """Initialize all agents and connections"""
        self.openrouter_agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        await self.redis_client.initialize()
        
        # Initialize specialized Swarm agents with config
        self.age_agent = AgeAgent(self.openrouter_agent, self.config)
        self.genre_agent = GenreAgent(self.openrouter_agent, self.config)
        self.tone_agent = ToneAgent(self.openrouter_agent, self.config)
        
        logger.info("Station 3: Age & Genre Optimizer initialized with Swarm agents")
    
    async def process(self, project_bible_data: Dict[str, Any], session_id: str) -> AgeGenreStyleGuide:
        """
        Process Station 2 Project Bible and create Age/Genre Style Guide
        using coordinated multi-agent approach
        """
        try:
            logger.info(f"Station 3 processing started for session {session_id}")
            
            # Extract working title
            working_title = project_bible_data.get('working_title', 'Untitled Project')
            
            print(f"🧬 Station 3: Processing Age & Genre Optimization...")
            print(f"📋 Working Title: {working_title}")
            
            # SWARM COORDINATION: All agents work in parallel on their specialties
            print("🤖 Coordinating multi-agent Swarm analysis...")
            
            # Agent 1: Age-appropriate content guidelines with retry logic
            print("   👶 Age Agent: Analyzing age-appropriate content guidelines...")
            max_retries = 5
            retry_delay = 3
            
            for attempt in range(max_retries):
                try:
                    if attempt > 0:
                        print(f"   🔄 Age Agent retry attempt {attempt + 1}/{max_retries}")
                        await asyncio.sleep(retry_delay * attempt)
                    
                    age_guidelines = await self.age_agent.analyze_age_requirements(project_bible_data)
                    print(f"   ✅ Age Agent succeeded on attempt {attempt + 1}")
                    break
                    
                except Exception as e:
                    print(f"   ⚠️ Age Agent attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        print("   ❌ CRITICAL: Age Agent FAILED after all retries")
                        raise ValueError(f"Station 3 age analysis failed after {max_retries} retries: {str(e)}")
            
            # Agent 2: Genre blending options with retry logic
            print("   🎭 Genre Agent: Creating optimized genre blend options...")
            
            for attempt in range(max_retries):
                try:
                    if attempt > 0:
                        print(f"   🔄 Genre Agent retry attempt {attempt + 1}/{max_retries}")
                        await asyncio.sleep(retry_delay * attempt)
                    
                    genre_options = await self.genre_agent.create_genre_blends(project_bible_data)
                    
                    # Validate that we have genre options
                    if not genre_options or len(genre_options) == 0:
                        raise ValueError("No genre options generated by LLM")
                    
                    print(f"   ✅ Genre Agent succeeded on attempt {attempt + 1}")
                    break
                    
                except Exception as e:
                    print(f"   ⚠️ Genre Agent attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        print("   ❌ CRITICAL: Genre Agent FAILED after all retries")
                        raise ValueError(f"Station 3 genre analysis failed after {max_retries} retries: {str(e)}")
            
            # Validate that we have genre options
            if not genre_options or len(genre_options) == 0:
                logger.error("No genre options generated by LLM")
                raise ValueError("Station 3 failed to generate genre options - no fallback allowed")
            
            # Display genre options for user choice
            print(f"\n🎭 GENRE BLEND OPTIONS:")
            print("-" * 40)
            
            for i, option in enumerate(genre_options):
                option_letter = chr(ord('A') + i)
                print(f"\n🔸 OPTION {option_letter}: {option.primary_genre} + {option.complementary_genre}")
                print(f"   Enhancement: {option.enhancement_analysis}")
                print(f"   Audio Elements: {', '.join(option.audio_elements[:2])}...")
                print(f"   Pacing: {option.pacing_implications}")
            
            # Get user's genre choice
            print(f"\n🎯 Choose your preferred genre blend:")
            print("Select Option A, B, or C (or press Enter for Option A):")
            
            chosen_index = 0  # Default to Option A
            while True:
                try:
                    choice = input("> ").strip().upper()
                    if choice == "":
                        choice = "A"
                        print(f"✅ Using default: Option {choice}")
                        break
                    elif choice in ['A', 'B', 'C']:
                        print(f"✅ Selected Option {choice}")
                        chosen_index = ord(choice) - ord('A')
                        break
                    else:
                        print("❌ Please enter A, B, C, or press Enter for default")
                except (EOFError, KeyboardInterrupt):
                    print(f"\n✅ Using default: Option A")
                    choice = "A"
                    break
            
            # Validate chosen_index is within bounds
            if chosen_index >= len(genre_options):
                logger.warning(f"chosen_index {chosen_index} out of bounds for {len(genre_options)} options, using first option")
                chosen_index = 0
            
            chosen_blend = genre_options[chosen_index]
            
            # Agent 3: Tone calibration based on chosen blend with retry logic
            print(f"   🎵 Tone Agent: Calibrating tone for {chosen_blend.primary_genre} + {chosen_blend.complementary_genre}...")
            
            for attempt in range(max_retries):
                try:
                    if attempt > 0:
                        print(f"   🔄 Tone Agent retry attempt {attempt + 1}/{max_retries}")
                        await asyncio.sleep(retry_delay * attempt)
                    
                    tone_calibration = await self.tone_agent.calibrate_tone(project_bible_data, chosen_blend)
                    print(f"   ✅ Tone Agent succeeded on attempt {attempt + 1}")
                    break
                    
                except Exception as e:
                    print(f"   ⚠️ Tone Agent attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        print("   ❌ CRITICAL: Tone Agent FAILED after all retries")
                        raise ValueError(f"Station 3 tone calibration failed after {max_retries} retries: {str(e)}")
            
            # Create comprehensive style guide
            style_guide = AgeGenreStyleGuide(
                working_title=working_title,
                age_guidelines=age_guidelines,
                genre_options=genre_options,
                tone_calibration=tone_calibration,
                chosen_genre_blend=f"Option {choice}: {chosen_blend.primary_genre} + {chosen_blend.complementary_genre}",
                production_notes=[
                    "Age guidelines ensure content appropriateness for target demographic",
                    "Genre blend optimizes audio engagement and audience expectations", 
                    "Tone calibration provides episode-by-episode guidance for consistent mood",
                    "All recommendations are optimized for audio-only production",
                    f"User selected {chosen_blend.primary_genre} + {chosen_blend.complementary_genre} blend"
                ],
                session_id=session_id,
                created_timestamp=datetime.now()
            )
            
            # Store in Redis for Station 4
            await self._store_style_guide(style_guide)
            
            logger.info(f"Station 3 processing completed for session {session_id}")
            return style_guide
            
        except Exception as e:
            logger.error(f"Station 3 processing failed: {str(e)}")
            raise

    async def _store_style_guide(self, style_guide: AgeGenreStyleGuide):
        """Store style guide in Redis for next station"""
        try:
            style_guide_data = {
                'working_title': style_guide.working_title,
                'age_guidelines': asdict(style_guide.age_guidelines),
                'genre_options': [asdict(option) for option in style_guide.genre_options],
                'tone_calibration': asdict(style_guide.tone_calibration),
                'chosen_genre_blend': style_guide.chosen_genre_blend,
                'production_notes': style_guide.production_notes,
                'session_id': style_guide.session_id,
                'created_timestamp': style_guide.created_timestamp.isoformat()
            }
            
            # Convert enums to strings for JSON storage
            age_data = style_guide_data['age_guidelines']
            age_data['violence_level'] = age_data['violence_level'].value
            age_data['emotional_intensity'] = age_data['emotional_intensity'].value
            
            await self.redis_client.set(
                f"audiobook:{style_guide.session_id}:station_03", 
                json.dumps(style_guide_data),
                expire=86400  # 24 hours
            )
            
            logger.info(f"Style guide stored in Redis for session {style_guide.session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store style guide in Redis: {str(e)}")
            # Non-critical error, continue processing

    # PDF export removed - use JSON and TXT formats instead
    # def export_style_guide_to_pdf(self, style_guide: AgeGenreStyleGuide, filename: str = None) -> str:
    #     """Export style guide to PDF format - REMOVED"""
    #     pass

    def display_style_guide_summary(self, style_guide: AgeGenreStyleGuide):
        """Display a formatted summary of the style guide"""
        print(f"\n🎯 AGE & GENRE STYLE GUIDE SUMMARY")
        print("=" * 60)
        print(f"📋 Working Title: {style_guide.working_title}")
        print(f"🎂 Target Age: {style_guide.age_guidelines.target_age_range}")
        print(f"🏷️  Content Rating: {style_guide.age_guidelines.content_rating}")
        print(f"🎭 Chosen Blend: {style_guide.chosen_genre_blend}")
        
        print(f"\n📍 AGE GUIDELINES:")
        print(f"   Violence Level: {style_guide.age_guidelines.violence_level.value}")
        print(f"   Emotional Intensity: {style_guide.age_guidelines.emotional_intensity.value}")
        print(f"   Theme Complexity: {style_guide.age_guidelines.theme_complexity}")
        
        print(f"\n🎵 TONE CALIBRATION:")
        print(f"   Light/Dark Balance: {style_guide.tone_calibration.light_dark_balance}")
        print(f"   Audio Techniques: {len(style_guide.tone_calibration.audio_tone_techniques)} defined")
        print(f"   Tension Curves: {len(style_guide.tone_calibration.tension_curves)} mapped")
        
        print(f"\n📝 PRODUCTION NOTES:")
        for note in style_guide.production_notes:
            print(f"   • {note}")
        
        print(f"\n🔗 Session: {style_guide.session_id}")
        print(f"⏰ Created: {style_guide.created_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")