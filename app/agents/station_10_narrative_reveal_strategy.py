#!/usr/bin/env python3
"""
Station 10: Narrative Reveal Strategy for Audiobook Production

This station creates comprehensive narrative reveal architecture with 5 major sections:
1. Reveal Taxonomy - Categorize all story information
2. Reveal Methods - Choose from 45+ methods with audio execution
3. Plant/Proof/Payoff Grid - For each revelation
4. Misdirection Strategy - Red herrings and believability
5. Fairness Check - Audience engagement and relisten value

Dependencies: Station 2 (Project Bible), Station 5 (Season Architecture), Station 8 (Character Bible)
Outputs: Complete Reveal Matrix with TXT, JSON, and PDF exports
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
from enum import Enum

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InformationPriority(Enum):
    MUST_KNOW = "Must know by Episode X"
    SHOULD_SUSPECT = "Should suspect by Episode Y"
    CAN_DISCOVER = "Can discover in Episode Z"
    NEVER_STATED = "Never explicitly stated"

class RevealMethod(Enum):
    BREADCRUMB_DRIP = "Breadcrumb Drip"
    MINI_TWIST_RHYTHM = "Mini-Twist Rhythm"
    QUESTION_LADDER = "Question Ladder"
    PROCEDURAL_REVEAL = "Procedural Reveal"
    MYSTERY_BOX_REVEAL = "Mystery-Box Reveal"
    INVESTIGATION_DUEL_REVEAL = "Investigation Duel Reveal"
    FORENSIC_REBUILD = "Forensic Rebuild"
    EFFECT_CAUSE_REVEAL = "Effect→Cause (Backwards Reveal)"
    NONLINEAR_MOSAIC_REVEAL = "Nonlinear Mosaic Reveal"
    FLASHBACK_WINDOWS = "Flashback Windows"
    PARALLEL_POV_RELAY = "Parallel POV Relay"
    RASHOMON_CONTRADICTION = "Rashomon Contradiction"
    FRAME_NARRATIVE_REVEAL = "Frame Narrative Reveal"
    CASE_FILE_EPISTOLARY_REVEAL = "Case-File/Epistolary Reveal"
    MONTAGE_REVEAL = "Montage Reveal"
    PLANT_PAYOFF_LATTICE = "Plant-Payoff Lattice"
    MOTIF_SIGNAL_REVEAL = "Motif Signal Reveal"
    RED_HERRING_BALANCE = "Red-Herring Balance"
    SLOW_BURN_REVEAL = "Slow Burn Reveal"
    ACCELERANT_REVEAL = "Accelerant Reveal"
    REAL_TIME_COUNTDOWN_REVEAL = "Real-Time Countdown Reveal"
    BOTTLE_INTERROGATION_REVEAL = "Bottle Interrogation Reveal"
    HEIST_EXPLAIN_EXECUTE_REFRAME = "Heist Explain→Execute→Reframe"
    LONG_CON_REVEAL = "Long Con Reveal"
    FAIR_PLAY_MYSTERY = "Fair-Play Mystery (Knox Rules)"
    CHEKHOV_ECONOMY_REVEAL = "Chekhov Economy Reveal"
    DRAMATIC_IRONY_REVEAL = "Dramatic Irony Reveal"
    LOSS_DISCOVERY_REVEAL = "Loss→Discovery Reveal"
    SOCIETY_WALL_REVEAL = "Society Wall Reveal"
    DREAM_MEMORY_DIVE_REVEAL = "Dream/Memory Dive Reveal"
    SIMULATION_NETWORK_POV_REVEAL = "Simulation/Network POV Reveal"
    COLD_OPEN_CLUE_REVEAL = "Cold Open Clue Reveal"
    B_STORY_ECHO_REVEAL = "B-Story Echo Reveal"
    CALENDAR_CLOCK_REVEAL = "Calendar Clock Reveal"
    CLUE_RECAP_BEAT = "Clue Recap Beat"
    EMOTIONAL_REVEAL = "Emotional Reveal"
    EXPOSITION_VIA_CONFLICT = "Exposition via Conflict"
    COMIC_MISDIRECTION_REVEAL = "Comic Misdirection Reveal"
    DATA_TRAIL_REVEAL = "Data Trail Reveal"
    ENVIRONMENTAL_STORY_REVEAL = "Environmental Story Reveal"
    TICKING_TRUTH_REVEAL = "Ticking Truth Reveal"
    SETUP_PROMISE_DELIVERY = "Setup→Promise Delivery"
    TEASER_TAG_REVEAL = "Teaser→Tag Reveal"
    MIRROR_REVEAL = "Mirror Reveal"
    ACCUMULATION_REVEAL = "Accumulation Reveal"

@dataclass
class InformationItem:
    """Individual piece of story information"""
    name: str
    description: str
    priority: InformationPriority
    target_episode: str
    category: str  # "character", "plot", "world", "theme"
    importance_level: int  # 1-10 scale
    emotional_impact: str
    audience_expectation: str

@dataclass
class RevealExecution:
    """How a specific reveal will be executed"""
    method: RevealMethod
    reasoning: str
    audio_execution: str
    audience_positioning: str
    timing: str
    emotional_arc: str
    production_notes: str

@dataclass
class PlantProofPayoff:
    """Plant/Proof/Payoff structure for a revelation"""
    revelation_name: str
    plant: Dict[str, str]  # episode, scene, line
    proof: Dict[str, str]  # episode, scene, evidence
    payoff: Dict[str, str]  # episode, scene, impact
    connection_strength: int  # 1-10 scale
    audience_satisfaction: str

@dataclass
class RedHerring:
    """Misdirection element"""
    name: str
    description: str
    introduction_episode: str
    debunk_episode: str
    believability_factors: List[str]
    purpose: str
    audio_signature: str

@dataclass
class FairnessCheck:
    """Audience engagement and fairness assessment"""
    theoretical_solvability: str
    clue_visibility: str
    relisten_value: str
    hidden_vs_visible_balance: str
    audience_agency: str
    satisfaction_guarantee: str

@dataclass
class RevealMatrix:
    """Complete narrative reveal strategy"""
    information_taxonomy: List[InformationItem]
    reveal_methods: List[RevealExecution]
    plant_proof_payoff_grid: List[PlantProofPayoff]
    misdirection_strategy: List[RedHerring]
    fairness_assessment: FairnessCheck
    reveal_timeline: Dict[str, List[str]]
    audio_cue_library: Dict[str, List[str]]
    production_guidelines: Dict[str, str]

class Station10NarrativeRevealStrategy:
    """Station 10: Narrative Reveal Strategy Builder"""
    
    def __init__(self):
        self.openrouter_agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.settings = Settings()
    
    async def initialize(self):
        """Initialize the station - MUST be called before process()"""
        await self.redis_client.initialize()
        logger.info("✅ Station 10 Redis client initialized")
    
    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON from LLM response, handling markdown code blocks"""
        # Remove markdown code blocks if present
        if response.strip().startswith('```json'):
            # Find the start and end of JSON block
            start_marker = '```json'
            end_marker = '```'
            start_idx = response.find(start_marker)
            end_idx = response.find(end_marker, start_idx + len(start_marker))
            
            if start_idx != -1 and end_idx != -1:
                json_content = response[start_idx + len(start_marker):end_idx].strip()
                logger.info("Extracted JSON from markdown code block")
                return json_content
        elif response.strip().startswith('```'):
            # Generic code block
            start_marker = '```'
            end_marker = '```'
            start_idx = response.find(start_marker)
            end_idx = response.find(end_marker, start_idx + len(start_marker))
            
            if start_idx != -1 and end_idx != -1:
                json_content = response[start_idx + len(start_marker):end_idx].strip()
                logger.info("Extracted JSON from generic code block")
                return json_content
        
        # Return original response if no code blocks found
        return response.strip()
        
    async def process(self, session_id: str) -> Dict[str, Any]:
        """Main processing function for Station 10"""
        logger.info(f"Starting Station 10: Narrative Reveal Strategy for session {session_id}")
        
        try:
            # Get dependencies
            dependencies = await self._get_dependencies(session_id)
            
            # Build reveal strategy
            reveal_matrix = await self._build_reveal_matrix(dependencies)
            
            # Generate outputs
            outputs = await self._generate_outputs(reveal_matrix, session_id)
            
            # Save to Redis
            await self._save_to_redis(reveal_matrix, session_id)
            
            logger.info(f"Station 10 completed successfully for session {session_id}")
            return outputs
            
        except Exception as e:
            logger.error(f"Station 10 failed for session {session_id}: {str(e)}")
            raise
    
    async def _get_dependencies(self, session_id: str) -> Dict[str, Any]:
        """Get required dependencies from previous stations"""
        dependencies = {}
        
        # Get Station 2: Project Bible
        project_bible_key = f"audiobook:{session_id}:station_02"
        project_bible_data = await self.redis_client.get(project_bible_key)
        if not project_bible_data:
            logger.error(f"❌ CRITICAL: Station 2 output not found in Redis at key {project_bible_key}")
            raise ValueError("CRITICAL: Station 2 (Project Bible) output is required for Station 10")
        project_bible = json.loads(project_bible_data)
        dependencies['project_bible'] = project_bible
        logger.info(f"✅ Loaded Station 2 output")
        
        # Get Station 5: Season Architecture  
        season_architecture_key = f"audiobook:{session_id}:station_05"
        season_architecture_data = await self.redis_client.get(season_architecture_key)
        if not season_architecture_data:
            logger.error(f"❌ CRITICAL: Station 5 output not found in Redis at key {season_architecture_key}")
            raise ValueError("CRITICAL: Station 5 (Season Architecture) output is required for Station 10")
        season_architecture = json.loads(season_architecture_data)
        dependencies['season_architecture'] = season_architecture
        logger.info(f"✅ Loaded Station 5 output")
        
        # Get Station 8: Character Bible
        character_bible_key = f"audiobook:{session_id}:station_08"
        character_bible_data = await self.redis_client.get(character_bible_key)
        if not character_bible_data:
            logger.error(f"❌ CRITICAL: Station 8 output not found in Redis at key {character_bible_key}")
            raise ValueError("CRITICAL: Station 8 (Character Bible) output is required for Station 10")
        character_bible = json.loads(character_bible_data)
        dependencies['character_bible'] = character_bible
        logger.info(f"✅ Loaded Station 8 output")
        
        return dependencies
    
    async def _build_reveal_matrix(self, dependencies: Dict[str, Any]) -> RevealMatrix:
        """Build the complete narrative reveal strategy"""
        
        # Extract story information
        # Defensive checks: ensure all dependencies are dicts
        project_bible = dependencies.get('project_bible', {})
        if not isinstance(project_bible, dict):
            project_bible = {}
            
        season_arch = dependencies.get('season_architecture', {})
        if not isinstance(season_arch, dict):
            season_arch = {}
            
        char_bible = dependencies.get('character_bible', {})
        if not isinstance(char_bible, dict):
            char_bible = {}
        
        story_concept = project_bible.get('story_concept', 'Unknown story')
        # Try total_episodes first (new format), fallback to episode_count (old format)
        episode_count = season_arch.get('total_episodes') or season_arch.get('episode_count', 10)
        characters = char_bible.get('characters', [])
        
        # Build information taxonomy
        information_taxonomy = await self._build_information_taxonomy(
            story_concept, episode_count, characters
        )
        
        # Build reveal methods
        reveal_methods = await self._build_reveal_methods(
            story_concept, information_taxonomy
        )
        
        # Build plant/proof/payoff grid
        plant_proof_payoff_grid = await self._build_plant_proof_payoff_grid(
            information_taxonomy, episode_count
        )
        
        # Build misdirection strategy
        misdirection_strategy = await self._build_misdirection_strategy(
            story_concept, characters
        )
        
        # Build fairness assessment
        fairness_assessment = await self._build_fairness_assessment(
            information_taxonomy, reveal_methods
        )
        
        # Build reveal timeline
        reveal_timeline = await self._build_reveal_timeline(
            information_taxonomy, episode_count
        )
        
        # Build audio cue library
        audio_cue_library = await self._build_audio_cue_library(
            reveal_methods, story_concept
        )
        
        # Build production guidelines
        production_guidelines = await self._build_production_guidelines(
            reveal_methods, fairness_assessment
        )
        
        return RevealMatrix(
            information_taxonomy=information_taxonomy,
            reveal_methods=reveal_methods,
            plant_proof_payoff_grid=plant_proof_payoff_grid,
            misdirection_strategy=misdirection_strategy,
            fairness_assessment=fairness_assessment,
            reveal_timeline=reveal_timeline,
            audio_cue_library=audio_cue_library,
            production_guidelines=production_guidelines
        )
    
    async def _build_information_taxonomy(self, story_concept: str, episode_count: int, characters: List[Dict]) -> List[InformationItem]:
        """Build comprehensive information taxonomy"""
        
        prompt = f"""
        You are the Narrative Reveal Architect. Create a comprehensive information taxonomy for this audiobook story:
        
        STORY CONCEPT: {story_concept}
        EPISODE COUNT: {episode_count}
        CHARACTERS: {json.dumps(characters, indent=2)}
        
        Create 15-25 information items across these categories:
        - Character secrets and motivations
        - Plot twists and revelations
        - World-building mysteries
        - Thematic discoveries
        - Relationship dynamics
        - Historical events
        - Future implications
        
        For each information item, specify:
        1. Name (clear, descriptive)
        2. Description (what this information is)
        3. Priority (Must know by Episode X, Should suspect by Episode Y, Can discover in Episode Z, Never explicitly stated)
        4. Target episode (when audience should know/suspect/discover this)
        5. Category (character, plot, world, theme)
        6. Importance level (1-10 scale)
        7. Emotional impact (how this affects audience)
        8. Audience expectation (what audience might expect vs reality)
        
        Return as JSON array of information items.
        """
        
        response = await self.openrouter_agent.generate(prompt)
        
        try:
            # Parse the response to extract information items
            json_text = self._extract_json_from_response(response)
            items_data = json.loads(json_text)
            information_items = []
            
            for item_data in items_data:
                # Map priority string to enum
                priority_map = {
                    "Must know by Episode X": InformationPriority.MUST_KNOW,
                    "Should suspect by Episode Y": InformationPriority.SHOULD_SUSPECT,
                    "Can discover in Episode Z": InformationPriority.CAN_DISCOVER,
                    "Never explicitly stated": InformationPriority.NEVER_STATED
                }
                
                priority = priority_map.get(item_data.get('priority', 'Can discover in Episode Z'), InformationPriority.CAN_DISCOVER)
                
                information_items.append(InformationItem(
                    name=item_data.get('name', 'Unknown'),
                    description=item_data.get('description', ''),
                    priority=priority,
                    target_episode=str(item_data.get('target_episode', 'Episode 5')),
                    category=item_data.get('category', 'plot'),
                    importance_level=item_data.get('importance_level', 5),
                    emotional_impact=item_data.get('emotional_impact', ''),
                    audience_expectation=item_data.get('audience_expectation', '')
                ))
            
            return information_items
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ CRITICAL: Failed to parse information taxonomy JSON: {str(e)}")
            logger.error(f"Response was: {response[:500]}...")
            raise ValueError(f"CRITICAL: Unable to parse information taxonomy from LLM response: {str(e)}")
    
    async def _build_reveal_methods(self, story_concept: str, information_taxonomy: List[InformationItem]) -> List[RevealExecution]:
        """Build reveal methods for each major revelation"""
        
        # Select key revelations for detailed method planning
        key_revelations = [item for item in information_taxonomy if item.importance_level >= 7]
        
        reveal_executions = []
        
        for revelation in key_revelations:
            prompt = f"""
            You are the Narrative Reveal Architect. Design the reveal method for this key revelation:
            
            REVELATION: {revelation.name}
            DESCRIPTION: {revelation.description}
            TARGET EPISODE: {revelation.target_episode}
            IMPORTANCE LEVEL: {revelation.importance_level}/10
            EMOTIONAL IMPACT: {revelation.emotional_impact}
            
            Choose the BEST reveal method from this catalog of 45+ methods:
            
            1. Breadcrumb Drip - Information revealed in tiny fragments
            2. Mini-Twist Rhythm - Frequent small reversals
            3. Question Ladder - Each answer spawns deeper question
            4. Procedural Reveal - Information unfolds like documented process
            5. Mystery-Box Reveal - Central puzzle sustains tension
            6. Investigation Duel Reveal - Two investigators with opposing methods
            7. Forensic Rebuild - Reconstructing past through evidence
            8. Effect→Cause (Backwards Reveal) - Start with consequences, work back
            9. Nonlinear Mosaic Reveal - Multiple timelines converge
            10. Flashback Windows - Strategic past scenes illuminate present
            11. Parallel POV Relay - Alternating perspectives converge
            12. Rashomon Contradiction - Conflicting accounts force doubt
            13. Frame Narrative Reveal - Outer story controls inner truth
            14. Case-File/Epistolary Reveal - Documents/recordings reveal truth
            15. Montage Reveal - Rapid information in compressed sequence
            16. Plant-Payoff Lattice - Early details bloom into revelations
            17. Motif Signal Reveal - Recurring element changes meaning
            18. Red-Herring Balance - Misdirections balanced with real clues
            19. Slow Burn Reveal - Gradual build to major revelation
            20. Accelerant Reveal - Sudden flood of revelations
            21. Real-Time Countdown Reveal - Truth emerges against ticking clock
            22. Bottle Interrogation Reveal - Confined Q&A extracts truth
            23. Heist Explain→Execute→Reframe - Plan shown, executed, reinterpreted
            24. Long Con Reveal - Audience misled until deep revelation
            25. Fair-Play Mystery (Knox Rules) - All clues available to audience
            26. Chekhov Economy Reveal - Every detail must pay off
            27. Dramatic Irony Reveal - Audience knows before characters
            28. Loss→Discovery Reveal - Revelation tied to emotional loss
            29. Society Wall Reveal - Individual vs collective truth
            30. Dream/Memory Dive Reveal - Surreal sequences provide truth
            31. Simulation/Network POV Reveal - System perspective reveals pattern
            32. Cold Open Clue Reveal - Opening scene gains meaning later
            33. B-Story Echo Reveal - Subplot mirrors and reveals main plot
            34. Calendar Clock Reveal - Date-specific revelations
            35. Clue Recap Beat - Periodic summary ensures tracking
            36. Emotional Reveal - Truth through emotional confrontation
            37. Exposition via Conflict - Arguments reveal information
            38. Comic Misdirection Reveal - Comedy hides truth delivery
            39. Data Trail Reveal - Digital breadcrumbs to truth
            40. Environmental Story Reveal - Setting reveals truth
            41. Ticking Truth Reveal - Revelation impact grows over time
            42. Setup→Promise Delivery - Early setup pays off clearly
            43. Teaser→Tag Reveal - Hook at start, surprise at end
            44. Mirror Reveal - Parallel situations reveal truth
            45. Accumulation Reveal - Small details accumulate to truth
            
            For this revelation, specify:
            1. Method selected (choose the most effective one)
            2. Why this method (reasoning for this choice)
            3. Audio execution (how this sounds in audiobook format)
            4. Audience positioning (how audience experiences this)
            5. Timing (when and how this unfolds)
            6. Emotional arc (emotional journey for audience)
            7. Production notes (specific audio production considerations)
            
            Return as JSON object.
            """
            
            response = await self.openrouter_agent.generate(prompt)
            
            try:
                json_text = self._extract_json_from_response(response)
                method_data = json.loads(json_text)
                
                # Map method string to enum
                method_map = {
                    "Breadcrumb Drip": RevealMethod.BREADCRUMB_DRIP,
                    "Mini-Twist Rhythm": RevealMethod.MINI_TWIST_RHYTHM,
                    "Question Ladder": RevealMethod.QUESTION_LADDER,
                    "Procedural Reveal": RevealMethod.PROCEDURAL_REVEAL,
                    "Mystery-Box Reveal": RevealMethod.MYSTERY_BOX_REVEAL,
                    "Investigation Duel Reveal": RevealMethod.INVESTIGATION_DUEL_REVEAL,
                    "Forensic Rebuild": RevealMethod.FORENSIC_REBUILD,
                    "Effect→Cause (Backwards Reveal)": RevealMethod.EFFECT_CAUSE_REVEAL,
                    "Nonlinear Mosaic Reveal": RevealMethod.NONLINEAR_MOSAIC_REVEAL,
                    "Flashback Windows": RevealMethod.FLASHBACK_WINDOWS,
                    "Parallel POV Relay": RevealMethod.PARALLEL_POV_RELAY,
                    "Rashomon Contradiction": RevealMethod.RASHOMON_CONTRADICTION,
                    "Frame Narrative Reveal": RevealMethod.FRAME_NARRATIVE_REVEAL,
                    "Case-File/Epistolary Reveal": RevealMethod.CASE_FILE_EPISTOLARY_REVEAL,
                    "Montage Reveal": RevealMethod.MONTAGE_REVEAL,
                    "Plant-Payoff Lattice": RevealMethod.PLANT_PAYOFF_LATTICE,
                    "Motif Signal Reveal": RevealMethod.MOTIF_SIGNAL_REVEAL,
                    "Red-Herring Balance": RevealMethod.RED_HERRING_BALANCE,
                    "Slow Burn Reveal": RevealMethod.SLOW_BURN_REVEAL,
                    "Accelerant Reveal": RevealMethod.ACCELERANT_REVEAL,
                    "Real-Time Countdown Reveal": RevealMethod.REAL_TIME_COUNTDOWN_REVEAL,
                    "Bottle Interrogation Reveal": RevealMethod.BOTTLE_INTERROGATION_REVEAL,
                    "Heist Explain→Execute→Reframe": RevealMethod.HEIST_EXPLAIN_EXECUTE_REFRAME,
                    "Long Con Reveal": RevealMethod.LONG_CON_REVEAL,
                    "Fair-Play Mystery (Knox Rules)": RevealMethod.FAIR_PLAY_MYSTERY,
                    "Chekhov Economy Reveal": RevealMethod.CHEKHOV_ECONOMY_REVEAL,
                    "Dramatic Irony Reveal": RevealMethod.DRAMATIC_IRONY_REVEAL,
                    "Loss→Discovery Reveal": RevealMethod.LOSS_DISCOVERY_REVEAL,
                    "Society Wall Reveal": RevealMethod.SOCIETY_WALL_REVEAL,
                    "Dream/Memory Dive Reveal": RevealMethod.DREAM_MEMORY_DIVE_REVEAL,
                    "Simulation/Network POV Reveal": RevealMethod.SIMULATION_NETWORK_POV_REVEAL,
                    "Cold Open Clue Reveal": RevealMethod.COLD_OPEN_CLUE_REVEAL,
                    "B-Story Echo Reveal": RevealMethod.B_STORY_ECHO_REVEAL,
                    "Calendar Clock Reveal": RevealMethod.CALENDAR_CLOCK_REVEAL,
                    "Clue Recap Beat": RevealMethod.CLUE_RECAP_BEAT,
                    "Emotional Reveal": RevealMethod.EMOTIONAL_REVEAL,
                    "Exposition via Conflict": RevealMethod.EXPOSITION_VIA_CONFLICT,
                    "Comic Misdirection Reveal": RevealMethod.COMIC_MISDIRECTION_REVEAL,
                    "Data Trail Reveal": RevealMethod.DATA_TRAIL_REVEAL,
                    "Environmental Story Reveal": RevealMethod.ENVIRONMENTAL_STORY_REVEAL,
                    "Ticking Truth Reveal": RevealMethod.TICKING_TRUTH_REVEAL,
                    "Setup→Promise Delivery": RevealMethod.SETUP_PROMISE_DELIVERY,
                    "Teaser→Tag Reveal": RevealMethod.TEASER_TAG_REVEAL,
                    "Mirror Reveal": RevealMethod.MIRROR_REVEAL,
                    "Accumulation Reveal": RevealMethod.ACCUMULATION_REVEAL
                }
                
                method = method_map.get(method_data.get('method_selected', 'Slow Burn Reveal'), RevealMethod.SLOW_BURN_REVEAL)
                
                reveal_executions.append(RevealExecution(
                    method=method,
                    reasoning=method_data.get('why_this_method', ''),
                    audio_execution=method_data.get('audio_execution', ''),
                    audience_positioning=method_data.get('audience_positioning', ''),
                    timing=method_data.get('timing', ''),
                    emotional_arc=method_data.get('emotional_arc', ''),
                    production_notes=method_data.get('production_notes', '')
                ))
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ CRITICAL: Failed to parse reveal method for {revelation.name}: {str(e)}")
                raise ValueError(f"CRITICAL: Unable to parse reveal method from LLM response: {str(e)}")
        
        return reveal_executions
    
    async def _build_plant_proof_payoff_grid(self, information_taxonomy: List[InformationItem], episode_count: int) -> List[PlantProofPayoff]:
        """Build plant/proof/payoff grid for each revelation"""

        # Focus on high-importance revelations
        key_revelations = [item for item in information_taxonomy if item.importance_level >= 6]

        plant_proof_payoff_items = []

        for revelation in key_revelations:
            prompt = f"""
            You are the Narrative Reveal Architect. Create a Plant/Proof/Payoff structure for this revelation:

            REVELATION: {revelation.name}
            DESCRIPTION: {revelation.description}
            TARGET EPISODE: {revelation.target_episode}
            IMPORTANCE LEVEL: {revelation.importance_level}/10
            TOTAL EPISODES: {episode_count}

            Design the three-act structure:

            PLANT (Episode/Scene/Line):
            - When and where is the first hint dropped?
            - What specific line, action, or detail plants this revelation?
            - How subtle or obvious should this be?

            PROOF (Episode/Scene/Evidence):
            - When does the evidence become clear?
            - What concrete proof supports this revelation?
            - How does the audience connect the plant to the proof?

            PAYOFF (Episode/Scene/Impact):
            - When does the full revelation occur?
            - What is the emotional and narrative impact?
            - How does this change the story going forward?

            Also specify:
            - Connection strength (1-10 scale)
            - Audience satisfaction (how satisfying is this reveal)

            Return as JSON object.
            """

            # Retry logic with exponential backoff
            max_retries = 3
            retry_delay = 2  # Start with 2 seconds

            for attempt in range(max_retries):
                try:
                    # Add delay between API calls to prevent rate limiting
                    if attempt > 0:
                        await asyncio.sleep(retry_delay * attempt)

                    response = await self.openrouter_agent.generate(prompt)

                    # Validate response is not empty
                    if not response or not response.strip():
                        logger.warning(f"⚠️ Empty response for {revelation.name}, attempt {attempt + 1}/{max_retries}")
                        if attempt < max_retries - 1:
                            continue
                        else:
                            logger.error(f"❌ All retries exhausted for {revelation.name}, skipping...")
                            break

                    json_text = self._extract_json_from_response(response)

                    # Validate JSON text is not empty
                    if not json_text or not json_text.strip():
                        logger.warning(f"⚠️ Empty JSON text for {revelation.name}, attempt {attempt + 1}/{max_retries}")
                        if attempt < max_retries - 1:
                            continue
                        else:
                            logger.error(f"❌ All retries exhausted for {revelation.name}, skipping...")
                            break

                    ppp_data = json.loads(json_text)

                    plant_proof_payoff_items.append(PlantProofPayoff(
                        revelation_name=revelation.name,
                        plant=ppp_data.get('plant', {}),
                        proof=ppp_data.get('proof', {}),
                        payoff=ppp_data.get('payoff', {}),
                        connection_strength=ppp_data.get('connection_strength', 7),
                        audience_satisfaction=ppp_data.get('audience_satisfaction', '')
                    ))

                    logger.info(f"✅ Successfully processed {revelation.name}")
                    break  # Success - exit retry loop

                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ JSON parse error for {revelation.name}, attempt {attempt + 1}/{max_retries}: {str(e)}")
                    if attempt < max_retries - 1:
                        continue  # Retry
                    else:
                        logger.error(f"❌ Failed to parse {revelation.name} after {max_retries} attempts, skipping...")

                except Exception as e:
                    logger.warning(f"⚠️ Unexpected error for {revelation.name}, attempt {attempt + 1}/{max_retries}: {str(e)}")
                    if attempt < max_retries - 1:
                        continue  # Retry
                    else:
                        logger.error(f"❌ Failed to process {revelation.name} after {max_retries} attempts, skipping...")

            # Add delay between revelations to prevent rate limiting
            await asyncio.sleep(1.5)

        return plant_proof_payoff_items
    
    async def _build_misdirection_strategy(self, story_concept: str, characters: List[Dict]) -> List[RedHerring]:
        """Build misdirection strategy with red herrings"""
        
        prompt = f"""
        You are the Narrative Reveal Architect. Create a misdirection strategy with 3-5 red herrings for this story:
        
        STORY CONCEPT: {story_concept}
        CHARACTERS: {json.dumps(characters, indent=2)}
        
        Design red herrings that:
        1. Are believable and compelling
        2. Lead audience down wrong paths
        3. Are satisfyingly debunked
        4. Serve the overall narrative
        
        For each red herring, specify:
        1. Name (descriptive title)
        2. Description (what this misdirection is)
        3. Introduction episode (when it's introduced)
        4. Debunk episode (when it's revealed as false)
        5. Believability factors (why audience believes this)
        6. Purpose (how this serves the story)
        7. Audio signature (how this sounds in audiobook)
        
        Return as JSON array of red herrings.
        """
        
        response = await self.openrouter_agent.generate(prompt)
        
        try:
            json_text = self._extract_json_from_response(response)
            red_herrings_data = json.loads(json_text)
            red_herrings = []
            
            for herring_data in red_herrings_data:
                red_herrings.append(RedHerring(
                    name=herring_data.get('name', 'Unknown Red Herring'),
                    description=herring_data.get('description', ''),
                    introduction_episode=herring_data.get('introduction_episode', 'Episode 2'),
                    debunk_episode=herring_data.get('debunk_episode', 'Episode 8'),
                    believability_factors=herring_data.get('believability_factors', []),
                    purpose=herring_data.get('purpose', ''),
                    audio_signature=herring_data.get('audio_signature', '')
                ))
            
            return red_herrings
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ CRITICAL: Failed to parse misdirection strategy: {str(e)}")
            raise ValueError(f"CRITICAL: Unable to parse misdirection strategy from LLM response: {str(e)}")
    
    async def _build_fairness_assessment(self, information_taxonomy: List[InformationItem], reveal_methods: List[RevealExecution]) -> FairnessCheck:
        """Build fairness assessment for audience engagement"""
        
        prompt = f"""
        You are the Narrative Reveal Architect. Assess the fairness and audience engagement of this reveal strategy:
        
        INFORMATION TAXONOMY: {len(information_taxonomy)} items
        REVEAL METHODS: {len(reveal_methods)} methods
        
        Evaluate these aspects:
        
        1. THEORETICAL SOLVABILITY:
        - Could a sharp audience member theoretically figure out the major reveals?
        - Are the clues logically connected?
        - Is the mystery solvable with available information?
        
        2. CLUE VISIBILITY:
        - Are important clues findable on first listen?
        - Are they hidden in plain sight or buried too deep?
        - Balance between obvious and subtle clues
        
        3. RELISTEN VALUE:
        - What new details emerge on second listen?
        - How do early scenes gain new meaning?
        - Are there hidden layers for dedicated fans?
        
        4. HIDDEN VS VISIBLE BALANCE:
        - Right mix of obvious and hidden information?
        - Audience feels smart without being confused?
        - Satisfying discovery without frustration?
        
        5. AUDIENCE AGENCY:
        - Does audience feel like active participant?
        - Can they make predictions and feel rewarded?        
        - Do they get opportunities to theorize and discuss?
        
        6. SATISFACTION GUARANTEE:
        - Are reveals emotionally satisfying?
        - Do they pay off setup appropriately?
        - Balance between expected and surprising?
        
        Return as JSON object with these 6 assessments.
        """
        
        response = await self.openrouter_agent.generate(prompt)
        
        try:
            json_text = self._extract_json_from_response(response)
            fairness_data = json.loads(json_text)
            
            return FairnessCheck(
                theoretical_solvability=fairness_data.get('theoretical_solvability', ''),
                clue_visibility=fairness_data.get('clue_visibility', ''),
                relisten_value=fairness_data.get('relisten_value', ''),
                hidden_vs_visible_balance=fairness_data.get('hidden_vs_visible_balance', ''),
                audience_agency=fairness_data.get('audience_agency', ''),
                satisfaction_guarantee=fairness_data.get('satisfaction_guarantee', '')
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ CRITICAL: Failed to parse fairness assessment: {str(e)}")
            raise ValueError(f"CRITICAL: Unable to parse fairness assessment from LLM response: {str(e)}")
    
    async def _build_reveal_timeline(self, information_taxonomy: List[InformationItem], episode_count: int) -> Dict[str, List[str]]:
        """Build episode-by-episode reveal timeline"""
        
        timeline = {}
        
        for episode_num in range(1, episode_count + 1):
            episode_key = f"Episode {episode_num}"
            episode_reveals = []
            
            for item in information_taxonomy:
                # Check if this item reveals in this episode
                # Handle both string and integer target_episode values
                target_episode_str = str(item.target_episode)
                if episode_key in target_episode_str or str(episode_num) in target_episode_str:
                    episode_reveals.append(f"{item.name} ({item.priority.value})")
            
            if episode_reveals:
                timeline[episode_key] = episode_reveals
        
        return timeline
    
    async def _build_audio_cue_library(self, reveal_methods: List[RevealExecution], story_concept: str) -> Dict[str, List[str]]:
        """Build audio cue library for reveals"""
        
        prompt = f"""
        You are the Audio Design Specialist. Create an audio cue library for these reveal methods:
        
        STORY CONCEPT: {story_concept}
        REVEAL METHODS: {len(reveal_methods)} methods
        
        Create audio signatures for:
        1. Revelation moments (major reveals)
        2. Plant moments (subtle hints)
        3. Proof moments (evidence building)
        4. Misdirection moments (red herrings)
        5. Connection moments (when pieces click together)
        
        For each category, suggest:
        - Specific sound effects
        - Music cues
        - Voice treatment
        - Silence/pause usage
        - Layering techniques
        
        Return as JSON object with categories as keys and lists of audio cues as values.
        """
        
        response = await self.openrouter_agent.generate(prompt)
        
        try:
            json_text = self._extract_json_from_response(response)
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.error(f"❌ CRITICAL: Failed to parse audio cue library: {str(e)}")
            raise ValueError(f"CRITICAL: Unable to parse audio cue library from LLM response: {str(e)}")
    
    async def _build_production_guidelines(self, reveal_methods: List[RevealExecution], fairness_assessment: FairnessCheck) -> Dict[str, str]:
        """Build production guidelines for reveal strategy"""
        
        guidelines = {
            "overall_approach": "Audio-first storytelling with layered reveals",
            "clue_delivery": "Balance between subtle and obvious, ensuring fair play",
            "pacing": "Vary reveal intensity across episodes for sustained engagement",
            "audio_treatment": "Use sound design to enhance reveal moments without overwhelming",
            "relistenability": "Layer information for discovery on multiple listens",
            "audience_respect": "Trust audience intelligence while providing necessary guidance"
        }
        
        # Add method-specific guidelines
        for i, method in enumerate(reveal_methods[:5]):  # Top 5 methods
            guidelines[f"method_{i+1}_{method.method.value}"] = method.production_notes
        
        return guidelines
    
    async def _generate_outputs(self, reveal_matrix: RevealMatrix, session_id: str) -> Dict[str, Any]:
        """Generate formatted outputs"""
        
        # Create output directory
        output_dir = Path(f"outputs/{session_id}/station_10")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate TXT output
        txt_output = self._format_txt_output(reveal_matrix)
        txt_path = output_dir / "reveal_matrix.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_output)
        
        # Generate JSON output
        json_output = self._format_json_output(reveal_matrix)
        json_path = output_dir / "reveal_matrix.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            # Custom JSON encoder to handle enums
            class EnumEncoder(json.JSONEncoder):
                def default(self, obj):
                    if hasattr(obj, 'value'):
                        return obj.value
                    return super().default(obj)
            json.dump(json_output, f, indent=2, ensure_ascii=False, cls=EnumEncoder)
        
        return {
            "status": "success",
            "outputs": {
                "txt": str(txt_path),
                "json": str(json_path)
            },
            "summary": {
                "information_items": len(reveal_matrix.information_taxonomy),
                "reveal_methods": len(reveal_matrix.reveal_methods),
                "plant_proof_payoffs": len(reveal_matrix.plant_proof_payoff_grid),
                "red_herrings": len(reveal_matrix.misdirection_strategy)
            }
        }
    
    def _format_txt_output(self, reveal_matrix: RevealMatrix) -> str:
        """Format reveal matrix as readable text"""
        
        output = []
        output.append("=" * 80)
        output.append("NARRATIVE REVEAL STRATEGY - COMPLETE MATRIX")
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 80)
        output.append("")
        
        # Section 1: Information Taxonomy
        output.append("=== INFORMATION TAXONOMY ===")
        output.append("")
        for item in reveal_matrix.information_taxonomy:
            output.append(f"▪ {item.name}")
            output.append(f"  Description: {item.description}")
            output.append(f"  Priority: {item.priority.value}")
            output.append(f"  Target: {item.target_episode}")
            output.append(f"  Category: {item.category} | Importance: {item.importance_level}/10")
            output.append(f"  Emotional Impact: {item.emotional_impact}")
            output.append("")
        
        # Section 2: Reveal Methods
        output.append("=== REVEAL METHODS SELECTED ===")
        output.append("")
        for method in reveal_matrix.reveal_methods:
            output.append(f"▪ Method: {method.method.value}")
            output.append(f"  Reasoning: {method.reasoning}")
            output.append(f"  Audio Execution: {method.audio_execution}")
            output.append(f"  Audience Positioning: {method.audience_positioning}")
            output.append(f"  Timing: {method.timing}")
            output.append(f"  Emotional Arc: {method.emotional_arc}")
            output.append(f"  Production Notes: {method.production_notes}")
            output.append("")
        
        # Section 3: Plant/Proof/Payoff Grid
        output.append("=== PLANT/PROOF/PAYOFF GRID ===")
        output.append("")
        for ppp in reveal_matrix.plant_proof_payoff_grid:
            output.append(f"▪ Revelation: {ppp.revelation_name}")
            output.append(f"  PLANT:")
            output.append(f"    Episode: {ppp.plant.get('episode', 'N/A')}")
            output.append(f"    Scene: {ppp.plant.get('scene', 'N/A')}")
            output.append(f"    Line: {ppp.plant.get('line', 'N/A')}")
            output.append(f"  PROOF:")
            output.append(f"    Episode: {ppp.proof.get('episode', 'N/A')}")
            output.append(f"    Scene: {ppp.proof.get('scene', 'N/A')}")
            output.append(f"    Evidence: {ppp.proof.get('evidence', 'N/A')}")
            output.append(f"  PAYOFF:")
            output.append(f"    Episode: {ppp.payoff.get('episode', 'N/A')}")
            output.append(f"    Scene: {ppp.payoff.get('scene', 'N/A')}")
            output.append(f"    Impact: {ppp.payoff.get('impact', 'N/A')}")
            output.append(f"  Connection Strength: {ppp.connection_strength}/10")
            output.append(f"  Audience Satisfaction: {ppp.audience_satisfaction}")
            output.append("")
        
        # Section 4: Misdirection Strategy
        output.append("=== MISDIRECTION STRATEGY ===")
        output.append("")
        for herring in reveal_matrix.misdirection_strategy:
            output.append(f"▪ {herring.name}")
            output.append(f"  Description: {herring.description}")
            output.append(f"  Introduced: {herring.introduction_episode}")
            output.append(f"  Debunked: {herring.debunk_episode}")
            output.append(f"  Believability: {', '.join(herring.believability_factors)}")
            output.append(f"  Purpose: {herring.purpose}")
            output.append(f"  Audio Signature: {herring.audio_signature}")
            output.append("")
        
        # Section 5: Fairness Assessment
        output.append("=== FAIRNESS CHECK ===")
        output.append("")
        output.append(f"Theoretical Solvability: {reveal_matrix.fairness_assessment.theoretical_solvability}")
        output.append(f"Clue Visibility: {reveal_matrix.fairness_assessment.clue_visibility}")
        output.append(f"Relisten Value: {reveal_matrix.fairness_assessment.relisten_value}")
        output.append(f"Hidden vs Visible Balance: {reveal_matrix.fairness_assessment.hidden_vs_visible_balance}")
        output.append(f"Audience Agency: {reveal_matrix.fairness_assessment.audience_agency}")
        output.append(f"Satisfaction Guarantee: {reveal_matrix.fairness_assessment.satisfaction_guarantee}")
        output.append("")
        
        # Section 6: Reveal Timeline
        output.append("=== REVEAL TIMELINE ===")
        output.append("")
        for episode, reveals in reveal_matrix.reveal_timeline.items():
            output.append(f"{episode}:")
            for reveal in reveals:
                output.append(f"  - {reveal}")
            output.append("")
        
        # Section 7: Audio Cue Library
        output.append("=== AUDIO CUE LIBRARY ===")
        output.append("")
        for category, cues in reveal_matrix.audio_cue_library.items():
            output.append(f"{category.replace('_', ' ').title()}:")
            for cue in cues:
                output.append(f"  - {cue}")
            output.append("")
        
        # Section 8: Production Guidelines
        output.append("=== PRODUCTION GUIDELINES ===")
        output.append("")
        for key, value in reveal_matrix.production_guidelines.items():
            output.append(f"{key.replace('_', ' ').title()}: {value}")
            output.append("")
        
        output.append("=" * 80)
        output.append("END OF REVEAL MATRIX")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def _format_json_output(self, reveal_matrix: RevealMatrix) -> Dict[str, Any]:
        """Format reveal matrix as JSON"""
        
        return {
            "information_taxonomy": [asdict(item) for item in reveal_matrix.information_taxonomy],
            "reveal_methods": [asdict(method) for method in reveal_matrix.reveal_methods],
            "plant_proof_payoff_grid": [asdict(ppp) for ppp in reveal_matrix.plant_proof_payoff_grid],
            "misdirection_strategy": [asdict(herring) for herring in reveal_matrix.misdirection_strategy],
            "fairness_assessment": asdict(reveal_matrix.fairness_assessment),
            "reveal_timeline": reveal_matrix.reveal_timeline,
            "audio_cue_library": reveal_matrix.audio_cue_library,
            "production_guidelines": reveal_matrix.production_guidelines,
            "generated_at": datetime.now().isoformat()
        }
    
    async def _save_to_redis(self, reveal_matrix: RevealMatrix, session_id: str):
        """Save reveal matrix to Redis"""
        
        key = f"audiobook:{session_id}:station_10"
        data = json.dumps(self._format_json_output(reveal_matrix), default=str)
        await self.redis_client.set(key, data, expire=86400)  # 24 hour TTL
        logger.info(f"Saved reveal matrix to Redis: {key}")
    
    # Fallback methods for error handling
    
    def _create_fallback_information_taxonomy(self, story_concept: str, episode_count: int) -> List[InformationItem]:
        """Create fallback information taxonomy"""
        return [
            InformationItem(
                name="Core Mystery",
                description=f"Central question of {story_concept}",
                priority=InformationPriority.MUST_KNOW,
                target_episode=f"Episode {episode_count}",
                category="plot",
                importance_level=10,
                emotional_impact="High stakes revelation",
                audience_expectation="Expected but satisfying"
            )
        ]
    
    def _create_fallback_reveal_execution(self, revelation: InformationItem) -> RevealExecution:
        """Create fallback reveal execution"""
        return RevealExecution(
            method=RevealMethod.SLOW_BURN_REVEAL,
            reasoning="Gradual build appropriate for audio format",
            audio_execution="Layer clues across episodes with increasing clarity",
            audience_positioning="Audience suspects alongside characters",
            timing=f"Build from Episode 1 to {revelation.target_episode}",
            emotional_arc="Curiosity → Suspicion → Recognition → Satisfaction",
            production_notes="Use recurring audio motif to signal related clues"
        )
    
    def _create_fallback_plant_proof_payoff(self, revelation: InformationItem, episode_count: int) -> PlantProofPayoff:
        """Create fallback plant/proof/payoff"""
        plant_episode = max(1, int(episode_count * 0.2))
        proof_episode = max(1, int(episode_count * 0.6))
        payoff_episode = str(revelation.target_episode)
        
        return PlantProofPayoff(
            revelation_name=revelation.name,
            plant={
                "episode": f"Episode {plant_episode}",
                "scene": "Early establishing scene",
                "line": "Subtle reference or detail"
            },
            proof={
                "episode": f"Episode {proof_episode}",
                "scene": "Mid-point discovery scene",
                "evidence": "Concrete evidence emerges"
            },
            payoff={
                "episode": payoff_episode,
                "scene": "Climactic revelation scene",
                "impact": "Major story shift and emotional impact"
            },
            connection_strength=7,
            audience_satisfaction="Satisfying if executed well"
        )
    
    def _create_fallback_red_herrings(self, story_concept: str) -> List[RedHerring]:
        """Create fallback red herrings"""
        return [
            RedHerring(
                name="False Suspect",
                description="Character appears guilty but is innocent",
                introduction_episode="Episode 2",
                debunk_episode="Episode 7",
                believability_factors=["Suspicious behavior", "Means and opportunity", "Prior conflict"],
                purpose="Misdirect audience attention from real culprit",
                audio_signature="Ominous music when this character appears"
            )
        ]
    
    def _create_fallback_fairness_check(self) -> FairnessCheck:
        """Create fallback fairness check"""
        return FairnessCheck(
            theoretical_solvability="Mystery is solvable with careful attention to details",
            clue_visibility="Clues are present but require active listening",
            relisten_value="Second listen reveals hidden connections and foreshadowing",
            hidden_vs_visible_balance="Good balance between obvious and subtle information",
            audience_agency="Audience can form theories and feel rewarded",
            satisfaction_guarantee="Reveals pay off setup appropriately"
        )

# Main execution
async def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python station_10_narrative_reveal_strategy.py <session_id>")
        sys.exit(1)
    
    session_id = sys.argv[1]
    
    station = Station10NarrativeRevealStrategy()
    result = await station.process(session_id)
    
    print(f"\n{'='*80}")
    print("Station 10: Narrative Reveal Strategy - COMPLETE")
    print(f"{'='*80}")
    print(f"Status: {result['status']}")
    print(f"Outputs: {json.dumps(result['outputs'], indent=2)}")
    print(f"Summary: {json.dumps(result['summary'], indent=2)}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(main())
