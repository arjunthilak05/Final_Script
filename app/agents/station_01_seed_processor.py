"""
Station 1: Seed Processor & Scale Evaluator Agent

This agent takes a one-liner concept and evaluates growth potential,
presenting 3 development options (Mini/Standard/Extended series).

Dependencies: None (entry point to the system)
Outputs: Scale options with justification and initial expansion
Human Gate: CRITICAL - Scale decision affects entire pipeline
"""

import json
import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.config import Settings
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
        
        # Station-specific prompt template
        self.prompt_template = self._load_prompt_template()
        
    async def initialize(self):
        """Initialize the Station 1 processor"""
        await self.redis.initialize()
        
    def _load_prompt_template(self) -> str:
        """Load the enhanced Station 1 prompt with better structured output"""
        return """
You are the Seed Processor for an audio-only series production system.

SEED TO ANALYZE: {seed_input}

TASK 1: EVALUATE GROWTH POTENTIAL
Analyze the seed and present 3 development options:

Option A: MINI SERIES (3-6 episodes, 15-25 min each)
- Core story arc focused on single emotional journey
- Estimated word count: 15,000-30,000 total
- Best for: contained stories, single mystery, limited cast
- Audio focus: Intimate character moments, minimal locations
- STRENGTHS: [List 3 specific strengths for this seed]
- LIMITATIONS: [List 2 specific limitations for this seed] 
- JUSTIFICATION: [2-3 sentences explaining why this scale fits this story]

Option B: STANDARD SERIES (8-12 episodes, 35-45 min each)  
- Main arc with 2-3 subplots and character development
- Estimated word count: 60,000-100,000 total
- Best for: character journeys, mystery with layers, relationship dynamics
- Audio focus: Multiple perspectives, rich soundscapes, evolving relationships
- STRENGTHS: [List 3 specific strengths for this seed]
- LIMITATIONS: [List 2 specific limitations for this seed]
- JUSTIFICATION: [2-3 sentences explaining why this scale fits this story]

Option C: EXTENDED SERIES (20-40 episodes, 35-45 min each)
- Complex multi-arc structure with ensemble cast
- Estimated word count: 150,000-300,000 total
- Best for: world-building, ensemble casts, epic scope
- Audio focus: Complex sound design, multiple storylines, deep character exploration
- STRENGTHS: [List 3 specific strengths for this seed]
- LIMITATIONS: [List 2 specific limitations for this seed]
- JUSTIFICATION: [2-3 sentences explaining why this scale fits this story]

RECOMMENDATION: Choose Option A, B, or C and explain why in 2-3 sentences.

TASK 2: INITIAL EXPANSION
For the recommended option, create:

WORKING TITLES:
1. [Audio-friendly title option 1]
2. [Audio-friendly title option 2]
3. [Audio-friendly title option 3]

CORE PREMISE: [2-3 sentences describing the core story, emphasizing audio storytelling elements]

MAIN CHARACTERS:
- [Primary character name 1 - extract from story]
- [Primary character name 2 - extract from story]  
- [Supporting character name 3 - extract from story]
- [Supporting character name 4 - extract from story]

CENTRAL CONFLICT: [The main dramatic tension that drives the audio drama]

EPISODE RATIONALE: [Explanation of why the recommended episode count is perfect for this story]

AUDIO BREAKING POINTS:
- Episode 1 ending: [Natural episode division point]
- Episode 2 ending: [Natural episode division point]
- Episode 3 ending: [Natural episode division point]
- Episode 4 ending: [Natural episode division point]

SIGNATURE SOUNDS:
- [Key audio element 1 that defines this story]
- [Key audio element 2 that defines this story]
- [Key audio element 3 that defines this story]

SPECIAL AUDIO CONSIDERATIONS:
- Focus on dialogue, internal monologue, and sound design
- Consider phone calls, voice messages, ambient sounds
- Think about how story beats translate to audio-only format
- Identify signature sounds that define the story

Be specific, detailed, and tailor every element to the provided seed concept.
"""

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
            
            # Get LLM response - using optimal settings for structured output
            response = await self.openrouter.generate(
                prompt=formatted_prompt,
                model="grok-4",  # Grok-4 Fast model
                max_tokens=3000,  # Increased for detailed response
                temperature=0.4  # Balanced temperature for creativity and consistency
            )
            
            # Parse the response into structured data
            parsed_output = self._parse_llm_response(response, seed_input, session_id)
            
            # Store in Redis for next station
            await self._store_output(session_id, parsed_output)
            
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
            logger.warning("Falling back to legacy parsing methods...")
            # Fallback to old parsing methods
            return self._fallback_parse_response(response, original_seed, session_id)

    def _extract_enhanced_scale_options(self, response: str) -> List[ScaleOption]:
        """Extract scale options from enhanced structured format"""
        scale_options = []
        
        # Enhanced patterns for the new format
        option_patterns = [
            (r"Option A: MINI SERIES.*?(?=Option B:|$)", "MINI", "A"),
            (r"Option B: STANDARD SERIES.*?(?=Option C:|$)", "STANDARD", "B"),
            (r"Option C: EXTENDED SERIES.*?(?=RECOMMENDATION:|$)", "EXTENDED", "C")
        ]
        
        for pattern, option_type, letter in option_patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                option_text = match.group(0)
                
                # Extract specific fields using enhanced parsing
                strengths = self._extract_field_with_prefix(option_text, "STRENGTHS:")
                limitations = self._extract_field_with_prefix(option_text, "LIMITATIONS:")
                justification = self._extract_field_with_prefix(option_text, "JUSTIFICATION:")
                
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
        
        return scale_options if len(scale_options) == 3 else self._get_default_scale_options()

    def _extract_enhanced_initial_expansion(self, response: str) -> InitialExpansion:
        """Extract initial expansion from enhanced structured format"""
        # Extract working titles
        titles = self._extract_numbered_list(response, "WORKING TITLES:")
        
        # Extract main characters
        main_characters = self._extract_bullet_list(response, "MAIN CHARACTERS:")
        
        # Extract other fields
        core_premise = self._extract_field_with_prefix(response, "CORE PREMISE:")
        central_conflict = self._extract_field_with_prefix(response, "CENTRAL CONFLICT:")
        episode_rationale = self._extract_field_with_prefix(response, "EPISODE RATIONALE:")
        
        # Extract breaking points
        breaking_points = self._extract_bullet_list(response, "AUDIO BREAKING POINTS:")
        
        return InitialExpansion(
            working_titles=titles if titles else ["The Accidental Connection", "Messages in the Dark", "Wrong Number, Right Person"],
            core_premise=core_premise if core_premise else "Core premise not found in response",
            central_conflict=central_conflict if central_conflict else "Central conflict not found in response",
            episode_rationale=episode_rationale if episode_rationale else "Episode rationale not found in response",
            breaking_points=breaking_points if breaking_points else ["Act 1: Setup", "Act 2: Complication", "Act 3: Resolution"],
            main_characters=main_characters if main_characters else ["Main Character", "Supporting Character", "Additional Character", "Background Character"]
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
        """Extract field content after a specific prefix"""
        pattern = rf"{re.escape(prefix)}\s*(.*?)(?=\n\n|\n[A-Z]+:|\n-|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Clean up common formatting artifacts
            content = re.sub(r'^\[.*?\]\s*', '', content)  # Remove [brackets]
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            return content
        return "Not found in response"

    def _extract_numbered_list(self, text: str, prefix: str) -> List[str]:
        """Extract numbered list items after a prefix"""
        pattern = rf"{re.escape(prefix)}(.*?)(?=\n\n|\n[A-Z]+:)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            list_content = match.group(1)
            items = re.findall(r'^\d+\.\s*(.+)$', list_content, re.MULTILINE)
            return [item.strip() for item in items if item.strip()]
        return []

    def _extract_bullet_list(self, text: str, prefix: str) -> List[str]:
        """Extract bullet list items after a prefix"""
        pattern = rf"{re.escape(prefix)}(.*?)(?=\n\n|\n[A-Z]+:)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            list_content = match.group(1)
            items = re.findall(r'^-\s*(.+)$', list_content, re.MULTILINE)
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
            logger.error(f"Fallback parsing also failed: {str(e)}")
            return self._create_fallback_output(original_seed, session_id)

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
        
        # Ensure we have all 3 options (fallback if parsing fails)
        if len(scale_options) < 3:
            logger.warning("Failed to extract all scale options, using defaults")
            scale_options = self._get_default_scale_options()
            
        return scale_options

    def _extract_initial_expansion(self, response: str) -> InitialExpansion:
        """Extract initial story expansion from response"""
        
        # Look for TASK 2 section
        task2_match = re.search(r"TASK 2[:\s]*(.*?)$", response, re.DOTALL | re.IGNORECASE)
        if not task2_match:
            logger.warning("Could not find TASK 2 section in response")
            return self._get_default_initial_expansion()
        
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


