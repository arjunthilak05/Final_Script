"""
Station 1: Seed Processor & Scale Evaluator Agent

This agent takes a one-liner concept and evaluates growth potential,
presenting 3 development options (Mini/Standard/Extended series).

Dependencies: None (entry point to the system)
Outputs: Scale options with justification and initial expansion
Human Gate: CRITICAL - Scale decision affects entire pipeline
"""

import asyncio
import json
import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.config import Settings
from app.agents.config_loader import load_station_config
# from app.pdf_exporter import Station1PDFExporter  # Not implemented

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ScaleOption:
    """Data structure for a scale option"""
    option_type: str  # "MINI", "STANDARD", "EXTENDED"
    episode_count: str  # e.g., "3-6 episodes"
    episode_length: str  # e.g., "15-25 min each"
    word_count: str  # e.g., "15,000-30,000 total"
    best_for: str  # What this option is ideal for
    justification: str  # Why this scale fits the seed

@dataclass
class InitialExpansion:
    """Data structure for initial story expansion"""
    working_titles: List[str]  # 3 title options
    core_premise: str  # 2-3 sentences
    central_conflict: str  # Main story tension
    episode_rationale: str  # Why this story needs this many episodes
    breaking_points: List[str]  # Natural episode divisions
    main_characters: List[str]  # Primary character names extracted from story

@dataclass
class SeedProcessorOutput:
    """Complete output from Station 1"""
    original_seed: str
    scale_options: List[ScaleOption]
    recommended_option: str  # "A", "B", or "C"
    initial_expansion: InitialExpansion
    processing_timestamp: datetime
    session_id: str

class Station01SeedProcessor:
    """
    Station 1: Seed Processor & Scale Evaluator
    
    Responsibilities:
    1. Analyze input seed for growth potential
    2. Generate 3 scale options (Mini/Standard/Extended)
    3. Provide initial story expansion
    4. Recommend optimal scale
    5. Prepare for human gate decision
    """
    
    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.station_id = "station_01"
        # self.pdf_exporter = Station1PDFExporter()  # Not implemented
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=1)
        
        # Station-specific prompt template (loaded from config)
        self.prompt_template = self.config.get_prompt('main')
        
    async def initialize(self):
        """Initialize the Station 1 processor"""
        await self.redis.initialize()
        
    def _load_prompt_template(self) -> str:
        """Load the enhanced Station 1 prompt with better structured output"""
        # This method is deprecated - prompt is now loaded from YML config
        # Keeping for backwards compatibility
        return self.prompt_template

    async def process(self, seed_input: str, session_id: str) -> SeedProcessorOutput:
        """
        Main processing method for Station 1
        
        Args:
            seed_input: The one-liner or story concept
            session_id: Unique session identifier
            
        Returns:
            SeedProcessorOutput: Complete analysis and recommendations
        """
        try:
            logger.info(f"Station 1 processing started for session {session_id}")
            
            # Validate input
            if not seed_input or len(seed_input.strip()) < 10:
                raise ValueError("Seed input must be at least 10 characters")
            
            # Format prompt with input
            formatted_prompt = self.prompt_template.format(seed_input=seed_input)
            
            # Get LLM response with retry logic - keep trying until success
            max_retries = 5
            retry_delay = 3  # seconds
            
            for attempt in range(max_retries):
                try:
                    if attempt > 0:
                        logger.info(f"Retry attempt {attempt + 1}/{max_retries} for Station 1")
                        await asyncio.sleep(retry_delay * attempt)
                    
                    response = await self.openrouter.generate(
                        formatted_prompt,
                        model=self.config.model,
                        max_tokens=self.config.max_tokens,
                        temperature=self.config.temperature
                    )
                    
                    # Parse the response into structured data
                    parsed_output = self._parse_llm_response(response, seed_input, session_id)
                    
                    # Success - break out of retry loop
                    logger.info(f"✅ Station 1 succeeded on attempt {attempt + 1}")
                    break
                    
                except Exception as e:
                    logger.warning(f"⚠️ Station 1 attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        logger.error(f"❌ Station 1 FAILED after {max_retries} attempts")
                        raise ValueError(f"Station 1 failed after {max_retries} retries: {str(e)}")
                    # Continue to next retry attempt
            
            # Store in Redis for next station
            await self._store_output(session_id, parsed_output)
            
            # Extract and lock story concept to preserve across stations
            story_lock = {
                'main_characters': self._extract_characters(seed_input),
                'core_mechanism': self._extract_core_mechanism(seed_input),
                'key_plot_points': self._extract_plot_points(seed_input)
            }
            await self.redis.set(
                f"audiobook:{session_id}:story_lock",
                json.dumps(story_lock),
                expire=86400
            )
            logger.info(f"Story lock created: {len(story_lock['main_characters'])} characters preserved")
            
            # Log successful processing
            logger.info(f"Station 1 completed successfully for session {session_id}")
            
            return parsed_output
            
        except Exception as e:
            logger.error(f"Station 1 processing failed for session {session_id}: {str(e)}")
            raise

    def _parse_llm_response(self, response: str, original_seed: str, session_id: str) -> SeedProcessorOutput:
        """
        Parse the structured JSON response from LLM into data objects.
        With high-quality LLMs, we expect properly formatted JSON.
        """
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON object directly
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    raise ValueError("No JSON found in LLM response")

            # Parse JSON
            data = json.loads(json_str)

            # Build scale options from JSON
            scale_options = []
            for option_key in ['option_a', 'option_b', 'option_c']:
                opt = data[option_key]
                scale_options.append(ScaleOption(
                    option_type=opt['type'],
                    episode_count=opt['episode_count'],
                    episode_length=opt['episode_length'],
                    word_count=opt['word_count'],
                    best_for=opt['best_for'],
                    justification=opt['justification']
                ))

            # Build initial expansion
            exp = data['initial_expansion']
            initial_expansion = InitialExpansion(
                working_titles=exp['working_titles'],
                core_premise=exp['core_premise'],
                central_conflict=exp['central_conflict'],
                episode_rationale=exp['episode_rationale'],
                breaking_points=exp['breaking_points'],
                main_characters=exp['main_characters']
            )

            return SeedProcessorOutput(
                original_seed=original_seed,
                scale_options=scale_options,
                recommended_option=data['recommended_option'],
                initial_expansion=initial_expansion,
                processing_timestamp=datetime.utcnow(),
                session_id=session_id
            )

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response preview: {response[:500]}")
            raise ValueError(f"Station 1 requires valid JSON from LLM: {str(e)}")

    # Removed all legacy extraction methods - no longer needed with high-quality LLMs
    # The prompt now enforces JSON output directly

    async def _store_output(self, session_id: str, output: SeedProcessorOutput) -> None:
        """Store output in Redis for next station"""
        try:
            # Convert to dictionary for JSON serialization
            output_dict = {
                "station_id": self.station_id,
                "original_seed": output.original_seed,
                "scale_options": [
                    {
                        "option_type": opt.option_type,
                        "episode_count": opt.episode_count,
                        "episode_length": opt.episode_length,
                        "word_count": opt.word_count,
                        "best_for": opt.best_for,
                        "justification": opt.justification
                    } for opt in output.scale_options
                ],
                "recommended_option": output.recommended_option,
                "initial_expansion": {
                    "working_titles": output.initial_expansion.working_titles,
                    "core_premise": output.initial_expansion.core_premise,
                    "central_conflict": output.initial_expansion.central_conflict,
                    "episode_rationale": output.initial_expansion.episode_rationale,
                    "breaking_points": output.initial_expansion.breaking_points,
                    "main_characters": output.initial_expansion.main_characters
                },
                "processing_timestamp": output.processing_timestamp.isoformat(),
                "session_id": output.session_id
            }
            
            # Store in Redis with session-based key
            key = f"audiobook:{session_id}:station_01"
            await self.redis.set(key, json.dumps(output_dict), expire=86400)  # 24 hour expiry
            
            logger.info(f"Station 1 output stored successfully for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store Station 1 output: {str(e)}")
            raise

    async def get_stored_output(self, session_id: str) -> Optional[SeedProcessorOutput]:
        """Retrieve stored output for a session"""
        try:
            key = f"audiobook:{session_id}:station_01"
            stored_data = await self.redis.get(key)
            
            if not stored_data:
                return None
                
            data = json.loads(stored_data)
            
            # Reconstruct the dataclass objects
            scale_options = [ScaleOption(**opt) for opt in data["scale_options"]]
            initial_expansion = InitialExpansion(**data["initial_expansion"])
            
            return SeedProcessorOutput(
                original_seed=data["original_seed"],
                scale_options=scale_options,
                recommended_option=data["recommended_option"],
                initial_expansion=initial_expansion,
                processing_timestamp=datetime.fromisoformat(data["processing_timestamp"]),
                session_id=data["session_id"]
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve Station 1 output: {str(e)}")
            return None

    def _extract_characters(self, seed: str) -> List[Dict[str, str]]:
        """Extract character names and professions from seed"""
        characters = []
        
        # Pattern 1: "Name is/was a [profession]"
        matches = re.findall(r'(\w+)\s+(?:is|was)\s+(?:a|an|the)\s+([\w\s]+?)(?:,|\.|;|\s+who|\s+has)', seed)
        for match in matches:
            if len(match[0]) > 2:
                characters.append({'name': match[0], 'profession': match[1].strip()})
        
        # Pattern 2: "Name, a [profession]"
        matches = re.findall(r'(\w+),\s+(?:a|an|the)\s+([\w\s]+?)(?:,|\.|;)', seed)
        for match in matches:
            if len(match[0]) > 2 and not any(c['name'] == match[0] for c in characters):
                characters.append({'name': match[0], 'profession': match[1].strip()})
        
        # Pattern 3: Simple capitalized names (likely proper nouns)
        words = seed.split()
        for i, word in enumerate(words):
            if word and word[0].isupper() and len(word) > 2 and word.isalpha():
                # Check if it's not at sentence start and not a common word
                if i > 0 or (i == 0 and not seed[0].isupper()):
                    if not any(c['name'] == word for c in characters):
                        # Try to find profession nearby
                        profession = "character"
                        if i + 2 < len(words) and words[i + 1] in ['is', 'was']:
                            profession = ' '.join(words[i + 2:i + 5]).strip(',.')
                        characters.append({'name': word, 'profession': profession})
        
        return characters[:5]  # Limit to 5 main characters
    
    def _extract_core_mechanism(self, seed: str) -> str:
        """Extract the core story mechanism"""
        # Return the first sentence or main action
        sentences = seed.split('.')
        if sentences and len(sentences[0].strip()) > 10:
            return sentences[0].strip()
        
        # No fallback - raise error if summary extraction fails
        raise ValueError(f"Failed to extract meaningful summary from seed: '{seed[:50]}...'")
    
    def _extract_plot_points(self, seed: str) -> List[str]:
        """Extract key plot points"""
        plot_points = []
        
        # Split by sentence
        sentences = [s.strip() for s in seed.split('.') if len(s.strip()) > 20]
        
        # Take meaningful sentences
        for sentence in sentences[:5]:
            if sentence and len(sentence) > 20:
                plot_points.append(sentence)
        
        return plot_points
    
    def format_for_human_review(self, output: SeedProcessorOutput) -> Dict:
        """Format output for human review/approval interface"""
        return {
            "station": "Station 1: Seed Processor & Scale Evaluator",
            "status": "awaiting_human_approval",
            "original_seed": output.original_seed,
            "analysis": {
                "option_a": {
                    "type": "Mini Series",
                    "specs": f"{output.scale_options[0].episode_count}, {output.scale_options[0].episode_length}",
                    "word_count": output.scale_options[0].word_count,
                    "best_for": output.scale_options[0].best_for,
                    "justification": output.scale_options[0].justification
                },
                "option_b": {
                    "type": "Standard Series", 
                    "specs": f"{output.scale_options[1].episode_count}, {output.scale_options[1].episode_length}",
                    "word_count": output.scale_options[1].word_count,
                    "best_for": output.scale_options[1].best_for,
                    "justification": output.scale_options[1].justification
                },
                "option_c": {
                    "type": "Extended Series",
                    "specs": f"{output.scale_options[2].episode_count}, {output.scale_options[2].episode_length}",
                    "word_count": output.scale_options[2].word_count,
                    "best_for": output.scale_options[2].best_for,
                    "justification": output.scale_options[2].justification
                }
            },
            "recommendation": f"Option {output.recommended_option}",
            "initial_expansion": {
                "working_titles": output.initial_expansion.working_titles,
                "core_premise": output.initial_expansion.core_premise,
                "central_conflict": output.initial_expansion.central_conflict,
                "episode_rationale": output.initial_expansion.episode_rationale,
                "breaking_points": output.initial_expansion.breaking_points
            },
            "next_step": "Please review and select your preferred scale option to proceed to Station 2: Project DNA Builder"
        }

    # def export_to_pdf(self, output: SeedProcessorOutput, filename: str = None) -> str:
    #     """
    #     Export Station 1 output to PDF
    #     
    #     Args:
    #         output: Station 1 processing output
    #         filename: Optional custom filename
    #         
    #     Returns:
    #         str: Path to the generated PDF file
    #     """
    #     return self.pdf_exporter.export_station1_output(output, filename)
    
    # def export_review_to_pdf(self, output: SeedProcessorOutput, filename: str = None) -> str:
    #     """
    #     Export formatted review data to PDF
    #     
    #     Args:
    #         output: Station 1 processing output
    #         filename: Optional custom filename
    #         
    #     Returns:
    #         str: Path to the generated PDF file
    #     """
    #     review_data = self.format_for_human_review(output)
    #     return self.pdf_exporter.export_formatted_review(review_data, filename)


