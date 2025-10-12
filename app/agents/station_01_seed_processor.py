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
        Parse the structured LLM response into data objects
        
        This method handles the new structured text-formatted response from the enhanced prompt.
        """
        try:
            # Save raw response for debugging
            debug_file = f"debug_response_{datetime.now().strftime('%H%M%S')}.txt"
            with open(debug_file, 'w') as f:
                f.write(response)
            logger.info(f"Saved raw LLM response to {debug_file}")
            
            # Use enhanced parsing for the new structured format
            scale_options = self._extract_enhanced_scale_options(response)
            
            # Extract initial expansion elements
            initial_expansion = self._extract_enhanced_initial_expansion(response)
            
            # Determine recommended option based on analysis
            recommended_option = self._determine_enhanced_recommendation(response)
            
            return SeedProcessorOutput(
                original_seed=original_seed,
                scale_options=scale_options,
                recommended_option=recommended_option,
                initial_expansion=initial_expansion,
                processing_timestamp=datetime.utcnow(),
                session_id=session_id
            )
            
        except Exception as e:
            logger.error(f"Failed to parse enhanced response: {str(e)}")
            logger.error(f"Response preview (first 500 chars): {response[:500]}")
            logger.error("CRITICAL: Cannot proceed without valid data from LLM response")
            raise ValueError(f"Station 1 parsing failed - cannot proceed with invalid data: {str(e)}")

    def _extract_enhanced_scale_options(self, response: str) -> List[ScaleOption]:
        """Extract scale options from enhanced structured format"""
        scale_options = []
        
        # Enhanced patterns for the new format - more flexible
        option_patterns = [
            (r"Option A:?\s*(?:MINI SERIES|Mini Series).*?(?=Option B:|TASK 2|$)", "MINI", "A"),
            (r"Option B:?\s*(?:STANDARD SERIES|Standard Series).*?(?=Option C:|TASK 2|$)", "STANDARD", "B"),
            (r"Option C:?\s*(?:EXTENDED SERIES|Extended Series).*?(?=RECOMMENDATION:|TASK 2|$)", "EXTENDED", "C")
        ]
        
        for pattern, option_type, letter in option_patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                option_text = match.group(0)
                
                # Extract specific fields using enhanced parsing - MUST succeed
                try:
                    strengths = self._extract_field_with_prefix(option_text, "STRENGTHS:")
                except ValueError as e:
                    logger.error(f"CRITICAL: Could not extract STRENGTHS for Option {letter}: {e}")
                    raise ValueError(f"Failed to extract STRENGTHS for Option {letter} - LLM must provide this field")
                
                try:
                    limitations = self._extract_field_with_prefix(option_text, "LIMITATIONS:")
                except ValueError as e:
                    logger.error(f"CRITICAL: Could not extract LIMITATIONS for Option {letter}: {e}")
                    raise ValueError(f"Failed to extract LIMITATIONS for Option {letter} - LLM must provide this field")
                
                try:
                    justification = self._extract_field_with_prefix(option_text, "JUSTIFICATION:")
                except ValueError as e:
                    logger.error(f"CRITICAL: Could not extract JUSTIFICATION for Option {letter}: {e}")
                    raise ValueError(f"Failed to extract JUSTIFICATION for Option {letter} - LLM must provide this field")
                
                # Build comprehensive justification
                full_justification = f"**Strengths:** {strengths}. **Limitations:** {limitations}. {justification}"
                
                # Set standard values based on option type
                if option_type == "MINI":
                    scale_option = ScaleOption(
                        option_type="MINI",
                        episode_count="3-6 episodes",
                        episode_length="15-25 min each",
                        word_count="15,000-30,000 total",
                        best_for="contained stories, single mystery, limited cast",
                        justification=full_justification
                    )
                elif option_type == "STANDARD":
                    scale_option = ScaleOption(
                        option_type="STANDARD", 
                        episode_count="8-12 episodes",
                        episode_length="35-45 min each",
                        word_count="60,000-100,000 total",
                        best_for="character journeys, mystery with layers",
                        justification=full_justification
                    )
                else:  # EXTENDED
                    scale_option = ScaleOption(
                        option_type="EXTENDED",
                        episode_count="20-40 episodes", 
                        episode_length="35-45 min each",
                        word_count="150,000-300,000 total",
                        best_for="world-building, ensemble casts, epic scope",
                        justification=full_justification
                    )
                
                scale_options.append(scale_option)
        
        if len(scale_options) != 3:
            logger.error(f"Only extracted {len(scale_options)} scale options, expected 3")
            raise ValueError(f"Failed to extract all 3 scale options from LLM response. Only found {len(scale_options)}")
        
        return scale_options

    def _extract_enhanced_initial_expansion(self, response: str) -> InitialExpansion:
        """Extract initial expansion from enhanced structured format"""
        # Extract working titles - MUST succeed
        try:
            titles = self._extract_numbered_list(response, "WORKING TITLES:")
            if not titles or len(titles) < 3:
                raise ValueError(f"Found {len(titles)} titles, need at least 3")
        except Exception as e:
            logger.error(f"CRITICAL: Could not extract WORKING TITLES: {e}")
            raise ValueError("Failed to extract working titles from LLM response - CRITICAL field missing")
        
        # Extract main characters - MUST succeed
        try:
            main_characters = self._extract_bullet_list(response, "MAIN CHARACTERS:")
            if not main_characters or len(main_characters) < 2:
                raise ValueError(f"Found {len(main_characters)} characters, need at least 2")
        except Exception as e:
            logger.error(f"CRITICAL: Could not extract MAIN CHARACTERS: {e}")
            raise ValueError("Failed to extract main characters from LLM response - CRITICAL field missing")
        
        # Extract core fields - MUST succeed
        try:
            core_premise = self._extract_field_with_prefix(response, "CORE PREMISE:")
        except Exception as e:
            logger.error(f"CRITICAL: Could not extract CORE PREMISE: {e}")
            raise ValueError("Failed to extract core premise from LLM response - CRITICAL field missing")
        
        try:
            central_conflict = self._extract_field_with_prefix(response, "CENTRAL CONFLICT:")
        except Exception as e:
            logger.error(f"CRITICAL: Could not extract CENTRAL CONFLICT: {e}")
            raise ValueError("Failed to extract central conflict from LLM response - CRITICAL field missing")
        
        try:
            episode_rationale = self._extract_field_with_prefix(response, "EPISODE RATIONALE:")
        except Exception as e:
            logger.error(f"CRITICAL: Could not extract EPISODE RATIONALE: {e}")
            raise ValueError("Failed to extract episode rationale from LLM response - CRITICAL field missing")
        
        # Extract breaking points - MUST succeed
        try:
            breaking_points = self._extract_bullet_list(response, "AUDIO BREAKING POINTS:")
            if not breaking_points or len(breaking_points) < 2:
                raise ValueError(f"Found {len(breaking_points)} breaking points, need at least 2")
        except Exception as e:
            logger.error(f"CRITICAL: Could not extract AUDIO BREAKING POINTS: {e}")
            raise ValueError("Failed to extract audio breaking points from LLM response - CRITICAL field missing")
            
        return InitialExpansion(
            working_titles=titles,
            core_premise=core_premise,
            central_conflict=central_conflict,
            episode_rationale=episode_rationale,
            breaking_points=breaking_points,
            main_characters=main_characters
        )

    def _determine_enhanced_recommendation(self, response: str) -> str:
        """Determine recommendation from enhanced format"""
        recommendation_match = re.search(r"RECOMMENDATION:.*?Option ([ABC])", response, re.IGNORECASE | re.DOTALL)
        if recommendation_match:
            return recommendation_match.group(1)
        
        # Fallback patterns
        if "option a" in response.lower() or "recommend.*a" in response.lower():
            return "A"
        elif "option c" in response.lower() or "recommend.*c" in response.lower():
            return "C"
        else:
            return "B"  # Default to Standard

    def _extract_field_with_prefix(self, text: str, prefix: str) -> str:
        """Extract field content after a specific prefix - with flexible matching"""
        
        # Try exact prefix first (case-insensitive)
        # Updated pattern to properly capture content including bullet lists
        pattern = rf"{re.escape(prefix)}\s*((?:.*?\n)?(?:[-•*]\s+.*?\n?)*.*?)(?=\n\n[A-Z]|\n[A-Z][A-Z\s]+:(?:\s|$)|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Clean up common formatting artifacts
            content = re.sub(r'^\[.*?\]\s*', '', content)  # Remove [brackets]
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            if content and len(content) > 10:  # Require more substantial content
                return content
        
        # Try alternative patterns based on field type
        if "CORE PREMISE" in prefix:
            alt_patterns = [
                r"(?:core\s+premise|premise)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)",
                r"(?:story\s+concept|concept)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)",
                r"(?:main\s+story|story)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)"
            ]
        elif "STRENGTHS" in prefix:
            alt_patterns = [
                r"(?:strengths?|advantages?)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)",
                r"(?:pros?|benefits?)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)"
            ]
        elif "LIMITATIONS" in prefix:
            alt_patterns = [
                r"(?:limitations?|constraints?|drawbacks?)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)",
                r"(?:cons?|weaknesses?)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)"
            ]
        elif "JUSTIFICATION" in prefix:
            alt_patterns = [
                r"(?:justification|reasoning|rationale)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)",
                r"(?:explanation|why)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)"
            ]
        elif "CENTRAL CONFLICT" in prefix:
            alt_patterns = [
                r"(?:central\s+conflict|conflict|main\s+conflict)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)",
                r"(?:tension|drama|problem)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)"
            ]
        elif "EPISODE RATIONALE" in prefix:
            alt_patterns = [
                r"(?:episode\s+rationale|rationale|why\s+episodes?)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)",
                r"(?:episode\s+reasoning|reasoning)[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)"
            ]
        else:
            alt_patterns = []
        
        # Try alternative patterns
        for alt_pattern in alt_patterns:
            match = re.search(alt_pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                content = re.sub(r'^\[.*?\]\s*', '', content)  # Remove [brackets]
                content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
                if content and len(content) > 3:
                    return content
        
        # Last resort: look for any meaningful text after similar words
        base_word = prefix.split()[0] if prefix else "content"
        loose_pattern = rf"(?:{re.escape(base_word.lower())})[:\s]*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n-\s|$)"
        match = re.search(loose_pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            content = re.sub(r'^\[.*?\]\s*', '', content)  # Remove [brackets]
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            if content and len(content) > 3:
                return content
        
        raise ValueError(f"Failed to find field with prefix '{prefix}' in LLM response")

    def _extract_numbered_list(self, text: str, prefix: str) -> List[str]:
        """Extract numbered list items after a prefix"""
        # Try with exact prefix first
        pattern = rf"{re.escape(prefix)}\s*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n\n\n|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            list_content = match.group(1)
            # Try different numbering formats
            items = re.findall(r'^\d+[.):]\s*(.+)$', list_content, re.MULTILINE)
            if items:
                return [item.strip() for item in items if item.strip()]
            # Try without anchoring to line start (more flexible)
            items = re.findall(r'\d+[.):]\s*(.+?)(?=\d+[.):|\n\n|$)', list_content, re.DOTALL)
            if items:
                return [item.strip() for item in items if item.strip()]
        return []

    def _extract_bullet_list(self, text: str, prefix: str) -> List[str]:
        """Extract bullet list items after a prefix"""
        # Try with exact prefix first
        pattern = rf"{re.escape(prefix)}\s*(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\n\n\n|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            list_content = match.group(1)
            # Try different bullet formats
            items = re.findall(r'^[-•*]\s*(.+)$', list_content, re.MULTILINE)
            if items:
                return [item.strip() for item in items if item.strip()]
            # Try without anchoring to line start (more flexible)
            items = re.findall(r'[-•*]\s*(.+?)(?=[-•*]|\n\n|$)', list_content, re.DOTALL)
            if items:
                return [item.strip() for item in items if item.strip()]
        return []

    def _extract_scale_options_from_json(self, scale_options_data: dict) -> List[ScaleOption]:
        """Extract scale options from JSON data"""
        scale_options = []
        
        for option_key in ['option_a', 'option_b', 'option_c']:
            if option_key in scale_options_data:
                option = scale_options_data[option_key]
                
                # Build comprehensive justification from all available data
                strengths = "; ".join(option.get('strengths', []))
                limitations = "; ".join(option.get('limitations', []))
                audio_focus = option.get('audio_focus', '')
                justification = option.get('justification', '')
                
                # Combine into detailed justification
                full_justification = f"**Strengths:** {strengths}. **Limitations:** {limitations}. **Audio Focus:** {audio_focus}. {justification}"
                
                scale_option = ScaleOption(
                    option_type=option.get('type', 'UNKNOWN'),
                    episode_count=option.get('episode_count', 'Unknown'),
                    episode_length=option.get('episode_length', 'Unknown'),
                    word_count=option.get('word_count', 'Unknown'),
                    best_for=option.get('best_for', 'Unknown'),
                    justification=full_justification
                )
                
                scale_options.append(scale_option)
        
        return scale_options if scale_options else self._get_default_scale_options()

    def _extract_initial_expansion_from_json(self, expansion_data: dict) -> InitialExpansion:
        """Extract initial expansion from JSON data"""
        return InitialExpansion(
            working_titles=expansion_data.get('working_titles', ['Title 1', 'Title 2', 'Title 3']),
            core_premise=expansion_data.get('core_premise', 'Core premise not available'),
            central_conflict=expansion_data.get('central_conflict', 'Central conflict not available'),
            episode_rationale=expansion_data.get('episode_rationale', 'Episode rationale not available'),
            breaking_points=expansion_data.get('audio_breaking_points', ['Beginning', 'Middle', 'End']),
            main_characters=expansion_data.get('main_characters', ['Main Character', 'Supporting Character', 'Additional Character', 'Background Character'])
        )

    def _fallback_parse_response(self, response: str, original_seed: str, session_id: str) -> SeedProcessorOutput:
        """Fallback parsing for non-JSON responses using the old method"""
        logger.warning("Using fallback parsing - JSON parsing failed")
        try:
            # Use the old extraction methods as fallback
            scale_options = self._extract_scale_options(response)
            initial_expansion = self._extract_initial_expansion(response)
            recommended_option = self._determine_recommendation(response, scale_options)
            
            return SeedProcessorOutput(
                original_seed=original_seed,
                scale_options=scale_options,
                recommended_option=recommended_option,
                initial_expansion=initial_expansion,
                processing_timestamp=datetime.utcnow(),
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Legacy parsing also failed: {str(e)}")
            raise ValueError(f"All parsing methods failed for Station 1: {str(e)}")

    def _extract_scale_options(self, response: str) -> List[ScaleOption]:
        """Extract the three scale options from LLM response"""
        scale_options = []
        
        # Look for Option A, B, C patterns in the response
        
        # Pattern to match each option section
        option_patterns = [
            (r"Option A[:\s]*(.*?)(?=Option B|$)", "MINI"),
            (r"Option B[:\s]*(.*?)(?=Option C|$)", "STANDARD"), 
            (r"Option C[:\s]*(.*?)(?=TASK 2|$)", "EXTENDED")
        ]
        
        for pattern, option_type in option_patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                option_text = match.group(1).strip()
                
                # Extract specific details from option text
                if option_type == "MINI":
                    scale_option = ScaleOption(
                        option_type="MINI",
                        episode_count="3-6 episodes",
                        episode_length="15-25 min each",
                        word_count="15,000-30,000 total",
                        best_for="contained stories, single mystery, limited cast",
                        justification=self._extract_justification(option_text)
                    )
                elif option_type == "STANDARD":
                    scale_option = ScaleOption(
                        option_type="STANDARD", 
                        episode_count="8-12 episodes",
                        episode_length="35-45 min each",
                        word_count="60,000-100,000 total",
                        best_for="character journeys, mystery with layers",
                        justification=self._extract_justification(option_text)
                    )
                else:  # EXTENDED
                    scale_option = ScaleOption(
                        option_type="EXTENDED",
                        episode_count="20-40 episodes", 
                        episode_length="35-45 min each",
                        word_count="150,000-300,000 total",
                        best_for="world-building, ensemble casts, epic scope",
                        justification=self._extract_justification(option_text)
                    )
                
                scale_options.append(scale_option)
        
        # Must have all 3 options - fail if not found
        if len(scale_options) < 3:
            logger.error(f"CRITICAL: Only extracted {len(scale_options)} scale options, expected 3")
            raise ValueError(f"Failed to extract all 3 scale options from LLM response. Only found {len(scale_options)}")
            
        return scale_options

    def _extract_initial_expansion(self, response: str) -> InitialExpansion:
        """Extract initial story expansion from response"""
        
        # Look for TASK 2 section
        task2_match = re.search(r"TASK 2[:\s]*(.*?)$", response, re.DOTALL | re.IGNORECASE)
        if not task2_match:
            logger.error("CRITICAL: Could not find TASK 2 section in LLM response")
            raise ValueError("Failed to find TASK 2 section in LLM response - response format invalid")
        
        task2_text = task2_match.group(1)
        
        # Extract working titles (look for numbered list or bullet points)
        titles = self._extract_working_titles(task2_text)
        
        # Extract core premise, central conflict, etc.
        core_premise = self._extract_field(task2_text, ["core premise", "premise"])
        central_conflict = self._extract_field(task2_text, ["central conflict", "conflict"])
        episode_rationale = self._extract_field(task2_text, ["why this story", "rationale", "episodes"])
        breaking_points = self._extract_breaking_points(task2_text)
        
        return InitialExpansion(
            working_titles=titles,
            core_premise=core_premise,
            central_conflict=central_conflict,
            episode_rationale=episode_rationale,
            breaking_points=breaking_points,
            main_characters=["Main Character", "Supporting Character", "Additional Character", "Background Character"]  # Fallback characters for old method
        )

    def _extract_justification(self, option_text: str) -> str:
        """Extract justification for why this scale fits the story"""
        # Look for explanatory text that isn't the standard template
        lines = option_text.split('\n')
        justification_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip template lines, capture explanatory content
            if (line and 
                not line.startswith('-') and 
                not any(keyword in line.lower() for keyword in ['episodes', 'minutes', 'word count', 'best for'])):
                justification_lines.append(line)
        
        return ' '.join(justification_lines) if justification_lines else "Recommended scale based on story complexity and scope."

    def _extract_working_titles(self, text: str) -> List[str]:
        """Extract 3 working title options"""
        
        # Look for numbered lists or bullet points with titles
        title_patterns = [
            r"(?:Working Title|Title)[s]?[:\s]*\n?(.*?)(?:\n\n|\n(?:[2-9]\.|\d+\.))",
            r"1\.\s*([^\n]+)",
            r"•\s*([^\n]+)",
            r"-\s*([^\n]+)",
            # More flexible patterns for titles in quotes or after colons
            r'"([^"]+)"',
            r"'([^']+)'",
            r":\s*([A-Z][^\n]+)",
            # Try to extract from response even if format varies
            r"([A-Z][a-z\s]+(?:Connection|Messages?|Journey|Call|Text|Sound))"
        ]
        
        titles = []
        for pattern in title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                clean_titles = []
                for match in matches[:5]:  # Look at more matches
                    title = match.strip().strip('"\'').strip()
                    # Filter out very short or clearly non-title text
                    if len(title) > 3 and len(title) < 50 and not title.lower().startswith(('the ', 'this ', 'that ')):
                        clean_titles.append(title)
                if clean_titles:
                    titles.extend(clean_titles)
                    break
        
        # If we found titles, use them; otherwise create meaningful defaults based on content
        if titles:
            # Remove duplicates while preserving order
            seen = set()
            unique_titles = []
            for title in titles:
                if title.lower() not in seen:
                    seen.add(title.lower())
                    unique_titles.append(title)
            titles = unique_titles[:3]
        
        # Ensure we have 3 titles with audio-appropriate names
        audio_defaults = ["The Accidental Connection", "Messages in the Dark", "Wrong Number, Right Person"]
        while len(titles) < 3:
            titles.append(audio_defaults[len(titles)])
            
        return titles[:3]

    def _extract_field(self, text: str, keywords: List[str]) -> str:
        """Extract a specific field based on keywords"""
        
        for keyword in keywords:
            pattern = rf"{keyword}[:\s]*([^\n]+(?:\n(?!\d+\.|\w+:)[^\n]+)*)"
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return f"Field not found in response (keywords: {', '.join(keywords)})"

    def _extract_breaking_points(self, text: str) -> List[str]:
        """Extract natural episode breaking points"""
        
        # Look for breaking points, natural divisions, etc.
        patterns = [
            r"breaking points?[:\s]*\n?(.*?)(?:\n\n|\n(?:\w+:))",
            r"natural divisions?[:\s]*\n?(.*?)(?:\n\n|\n(?:\w+:))",
            r"episode divisions?[:\s]*\n?(.*?)(?:\n\n|\n(?:\w+:))"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                points_text = match.group(1)
                # Split by bullet points, numbers, or newlines
                points = re.split(r'[•\-]|\d+\.|\n', points_text)
                return [point.strip() for point in points if point.strip()]
        
        # Fallback
        return ["Act 1: Setup", "Act 2: Complication", "Act 3: Resolution"]

    def _determine_recommendation(self, response: str, scale_options: List[ScaleOption]) -> str:
        """Determine which option the LLM recommends"""
        # Look for recommendation language in the response
        if "recommend" in response.lower():
            if "option a" in response.lower() or "mini" in response.lower():
                return "A"
            elif "option c" in response.lower() or "extended" in response.lower():
                return "C"
            else:
                return "B"
        
        # Default to Standard series if no clear recommendation
        return "B"

    def _get_default_scale_options(self) -> List[ScaleOption]:
        """Fallback scale options if parsing fails"""
        return [
            ScaleOption("MINI", "3-6 episodes", "15-25 min each", "15,000-30,000 total", 
                       "contained stories, single mystery, limited cast", 
                       "Suitable for focused narrative with limited scope"),
            ScaleOption("STANDARD", "8-12 episodes", "35-45 min each", "60,000-100,000 total",
                       "character journeys, mystery with layers",
                       "Balanced approach for character development and plot complexity"),
            ScaleOption("EXTENDED", "20-40 episodes", "35-45 min each", "150,000-300,000 total",
                       "world-building, ensemble casts, epic scope",
                       "Comprehensive storytelling with multiple storylines")
        ]

    def _get_default_initial_expansion(self) -> InitialExpansion:
        """Fallback initial expansion if parsing fails"""
        return InitialExpansion(
            working_titles=["Working Title 1", "Working Title 2", "Working Title 3"],
            core_premise="Core premise not extracted from response",
            central_conflict="Central conflict not extracted from response", 
            episode_rationale="Episode rationale not extracted from response",
            breaking_points=["Beginning", "Middle", "End"],
            main_characters=["Main Character", "Supporting Character", "Additional Character", "Background Character"]
        )

    def _create_fallback_output(self, original_seed: str, session_id: str) -> SeedProcessorOutput:
        """Create minimal output structure if parsing completely fails"""
        return SeedProcessorOutput(
            original_seed=original_seed,
            scale_options=self._get_default_scale_options(),
            recommended_option="B",
            initial_expansion=self._get_default_initial_expansion(),
            processing_timestamp=datetime.utcnow(),
            session_id=session_id
        )

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
        
        # Fallback: return first 100 characters
        return seed[:100].strip()
    
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


