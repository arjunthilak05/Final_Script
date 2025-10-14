"""
Station 15: Detailed Episode Outlining Agent

This agent expands a simple 2-3 paragraph episode blueprint into a detailed, 
1,000-word scene-by-scene outline. The output is strictly validated against 
Pydantic models to ensure a consistent data contract for downstream production.

Core Function:
- Takes episode blueprint summaries from Station 14
- Expands into detailed scene-by-scene breakdowns
- Enforces strict JSON structure through Pydantic validation
- NO DIALOGUE - only story beats, emotional states, and audio notes
- Formats for audio-only storytelling

Dependencies: Stations 5, 8, 9, 10, 14
Output: Validated scene-by-scene episode outlines (JSON)
"""

import json
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

from app.openrouter_agent import OpenRouterAgent
from app.agents.config_loader import load_station_config
from app.redis_client import RedisClient


# ============================================================================
# PYDANTIC MODELS - Enforce Strict Data Contract
# ============================================================================

class Station15Input(BaseModel):
    """Input model for Station 15 agent"""
    session_id: str = Field(..., description="Unique session identifier")
    episode_number: int = Field(..., description="Episode number to outline", ge=1)
    blueprint_summary: str = Field(..., description="2-3 paragraph summary from Station 14")


class SceneOutline(BaseModel):
    """Structure for each scene in the episode outline"""
    scene_number: int = Field(..., description="Sequential scene number", ge=1)
    location: str = Field(..., description="Where the scene takes place")
    time: str = Field(..., description="Time of day or temporal context")
    characters_present: List[str] = Field(..., description="List of character names in scene")
    goal_obstacle_choice_consequence: str = Field(
        ..., 
        description="Core dramatic loop: what character wants, what stops them, choice made, result"
    )
    reveal: Optional[str] = Field(
        default="None",
        description="Information revealed (Plant/Proof/Payoff from Reveal Matrix or 'None')"
    )
    soundscape_notes: Optional[str] = Field(
        default="Ambient environmental sounds appropriate to location",
        description="Audio storytelling notes: ambient sounds, key SFX, atmosphere"
    )
    transition_to_next_scene: Optional[str] = Field(
        default="Cuts to next scene",
        description="How this scene transitions to the next (or episode end)"
    )
    estimated_runtime: Optional[str] = Field(
        default="2-3 minutes",
        description="Estimated scene duration (e.g., '2 minutes', '3-4 minutes')"
    )


class Station15Output(BaseModel):
    """Main output model containing all scenes for an episode"""
    episode_number: int = Field(..., description="Episode number", ge=1)
    scenes: List[SceneOutline] = Field(..., description="List of scene outlines")


# ============================================================================
# STATION 15 AGENT CLASS
# ============================================================================

class Station15DetailedEpisodeOutlining:
    """
    Episode Outline Builder Agent
    
    Expands episode blueprints into detailed scene-by-scene outlines
    with strict Pydantic validation for consistent data structure.
    """
    
    def __init__(self, session_id: str):
        """
        Initialize Station 15 Agent
        
        Args:
            session_id: Unique session identifier
        """
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.debug_mode = False
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=15)
        self.model_name = self.config.model  # Using configured model
        
        self.station_name = "station_15_detailed_episode_outlining"
        
    async def initialize(self):
        """Initialize Redis connection"""
        await self.redis_client.connect()
    
    def enable_debug_mode(self):
        """Enable debug mode for detailed logging"""
        self.debug_mode = True
        print("🐛 Debug mode enabled for Station 15")
        
    async def load_context_from_redis(self) -> Dict[str, Any]:
        """
        Load full production context from Redis
        
        Loads:
        - Project Bible (Station 2)
        - Character Bible (Station 8)
        - World Bible (Station 9)
        - Reveal Matrix (Station 10)
        
        Returns:
            Dictionary containing all loaded context
        """
        print(f"📥 Loading context from Redis...")
        context = {}
        
        # Load Project Bible (Station 2)
        project_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_02")
        if project_raw:
            context['project_bible'] = json.loads(project_raw)
            print("  ✅ Project Bible loaded")
        else:
            print("  ⚠️ Project Bible not found")
            
        # Load Character Bible (Station 8)
        character_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_08")
        if character_raw:
            context['character_bible'] = json.loads(character_raw)
            print("  ✅ Character Bible loaded")
        else:
            print("  ⚠️ Character Bible not found")
            
        # Load World Bible (Station 9)
        world_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_09")
        if world_raw:
            context['world_bible'] = json.loads(world_raw)
            print("  ✅ World Bible loaded")
        else:
            print("  ⚠️ World Bible not found")
            
        # Load Reveal Matrix (Station 10)
        reveal_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_10")
        if reveal_raw:
            context['reveal_matrix'] = json.loads(reveal_raw)
            print("  ✅ Reveal Matrix loaded")
        else:
            print("  ⚠️ Reveal Matrix not found")
            
        return context
        
    def _construct_llm_prompt(
        self, 
        input_data: Station15Input, 
        context: Dict[str, Any]
    ) -> str:
        """
        Construct detailed prompt for LLM to generate scene-by-scene outline
        
        Args:
            input_data: Station15Input with episode details
            context: Full production context from Redis
            
        Returns:
            Complete prompt string for LLM
        """
        # Extract relevant context summaries (limit size for token efficiency)
        project_summary = json.dumps(
            context.get('project_bible', {}), 
            indent=2
        )[:2000]
        
        character_summary = json.dumps(
            context.get('character_bible', {}), 
            indent=2
        )[:3000]
        
        world_summary = json.dumps(
            context.get('world_bible', {}), 
            indent=2
        )[:3000]
        
        reveal_summary = json.dumps(
            context.get('reveal_matrix', {}), 
            indent=2
        )[:2000]
        
        prompt = f"""You are the EPISODE OUTLINE BUILDER for an AUDIO-ONLY series production system.

Your task: Expand the episode blueprint below into a detailed, 1,000-word scene-by-scene outline.

========================================
PRODUCTION CONTEXT
========================================

PROJECT BIBLE:
{project_summary}

CHARACTER BIBLE:
{character_summary}

WORLD BIBLE:
{world_summary}

REVEAL MATRIX (Plant/Proof/Payoff):
{reveal_summary}

========================================
EPISODE TO OUTLINE
========================================

Episode Number: {input_data.episode_number}

Blueprint Summary:
{input_data.blueprint_summary}

========================================
DETAILED INSTRUCTIONS
========================================

1. BREAK DOWN INTO SCENES:
   - Create a detailed scene-by-scene breakdown (~8-15 scenes)
   - Each scene should be 1-3 minutes of audio runtime
   - Total outline should be approximately 1,000 words
   
2. FOR EACH SCENE, SPECIFY:
   - scene_number: Sequential number (1, 2, 3, etc.)
   - location: Specific place where scene occurs
   - time: Time of day or temporal context
   - characters_present: List of character names in this scene
   - goal_obstacle_choice_consequence: Brief dramatic loop summary
   - reveal: What information is revealed? State if it's "Plant", "Proof", or "Payoff" 
     related to Reveal Matrix, or "None" if no major reveal
   - soundscape_notes: Audio storytelling details (ambient sounds, key SFX, atmosphere)
   - transition_to_next_scene: How scene flows to next (or ends episode)
   - estimated_runtime: Scene duration (e.g., "2 minutes", "3-4 minutes")

3. AUDIO-ONLY STORYTELLING:
   - NO DIALOGUE - only story beats and character emotional states
   - Focus on what listeners HEAR
   - Emphasize soundscape and audio atmosphere
   - Character actions must be audio-perceptible
   
4. DRAMATIC STRUCTURE:
   - Follow goal-obstacle-choice-consequence framework
   - Escalate tension across scenes
   - Integrate reveals from the Reveal Matrix naturally
   - Build to episode climax and ending

5. OUTPUT FORMAT:
   CRITICAL: Your ENTIRE response must be a single, valid, COMPLETE JSON object.
   
   REQUIREMENTS:
   - Start with {{ and end with }}
   - All strings must be properly quoted and escaped
   - All arrays must be properly closed with ]
   - All objects must be properly closed with }}
   - NO conversational text before or after the JSON
   - NO markdown formatting (no ``` blocks)
   - ONLY raw, valid, complete JSON
   - Ensure the JSON is COMPLETE - don't cut off mid-string or mid-object
   
   EXACT STRUCTURE REQUIRED:
   {{
     "episode_number": {input_data.episode_number},
     "scenes": [
       {{
         "scene_number": 1,
         "location": "Example location",
         "time": "Morning/Evening/etc",
         "characters_present": ["Character A", "Character B"],
         "goal_obstacle_choice_consequence": "Character wants X but faces Y, chooses Z, resulting in W",
         "reveal": "Plant: Secret mentioned in passing" OR "Proof: Evidence discovered" OR "Payoff: Truth revealed" OR "None",
         "soundscape_notes": "Ambient sounds, key SFX, atmosphere description",
         "transition_to_next_scene": "How scene flows to next",
         "estimated_runtime": "2 minutes"
       }},
       {{
         "scene_number": 2,
         ...
       }}
     ]
   }}
   
   IMPORTANT: Ensure all strings are complete and properly closed with quotes.
   The JSON must be valid and parseable. Double-check that all braces and brackets match.

========================================
BEGIN GENERATION
========================================

Generate the complete scene-by-scene outline now as a single, valid, COMPLETE JSON object.
Start your response with {{ and end with }}. Include nothing else.
"""
        return prompt
        
    async def run(self) -> Dict[str, Any]:
        """
        Main execution method for Station 15
        
        Process:
        1. Load episode blueprints from Station 14
        2. Generate detailed outlines for each episode
        3. Export all outlines to files
        4. Save to Redis
        5. Return statistics and output paths
        
        Returns:
            Dict with status, statistics, and output file paths
            
        Raises:
            Exception: For errors during processing
        """
        print(f"\n{'='*70}")
        print(f"📝 STATION 15: DETAILED EPISODE OUTLINING")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")
        
        try:
            # Initialize Redis connection
            await self.initialize()
            
            # Load and validate story lock
            print("🔒 Loading story lock...")
            story_lock_key = f"audiobook:{self.session_id}:story_lock"
            story_lock_raw = await self.redis_client.get(story_lock_key)
            if not story_lock_raw:
                print("⚠️  Story lock missing")
                story_lock = {'main_characters': [], 'core_mechanism': '', 'key_plot_points': []}
            else:
                story_lock = json.loads(story_lock_raw)
                print(f"✅ Story lock: {story_lock.get('core_mechanism', 'N/A')[:50]}...")
            
            # Load episode blueprints from Station 14
            print("📥 Loading episode blueprints from Station 14...")
            station_14_data = await self.redis_client.get(f"audiobook:{self.session_id}:station_14")
            
            if not station_14_data:
                raise ValueError("Missing episode blueprints from Station 14. Run Station 14 first.")
            
            blueprint_bible = json.loads(station_14_data)
            episodes = blueprint_bible.get('episodes', [])
            
            if not episodes:
                raise ValueError("No episodes found in Station 14 blueprints")
            
            total_episodes = len(episodes)
            print(f"✅ Loaded {total_episodes} episode blueprints\n")
            
            # Process each episode
            all_outlines = []
            total_scenes = 0
            
            for episode in episodes:
                episode_num = episode.get('episode_number', 0)
                blueprint_summary = episode.get('blueprint_summary', episode.get('summary', ''))
                
                if not blueprint_summary:
                    # Construct summary from available data
                    blueprint_summary = f"Episode {episode_num}:\n"
                    if episode.get('character_goals'):
                        blueprint_summary += f"Character Goals: {episode.get('character_goals')}\n"
                    if episode.get('obstacles'):
                        blueprint_summary += f"Obstacles: {episode.get('obstacles')}\n"
                    if episode.get('emotional_beats'):
                        blueprint_summary += f"Emotional Beats: {episode.get('emotional_beats')}\n"
                
                print(f"📝 Processing Episode {episode_num}/{total_episodes}...")
                
                # Create input for single episode processing
                episode_input = Station15Input(
                    session_id=self.session_id,
                    episode_number=episode_num,
                    blueprint_summary=blueprint_summary
                )
                
                # Process this episode
                outline = await self._process_single_episode(episode_input)
                all_outlines.append(outline)
                total_scenes += len(outline.scenes)
                
                print(f"✅ Episode {episode_num} complete: {len(outline.scenes)} scenes\n")
            
            # Export outputs
            print("💾 Exporting detailed outlines...")
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            base_filename = f"station15_episode_1_{self.session_id}"
            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")
            
            # Export to text file
            self._export_txt(all_outlines, txt_path)
            print(f"  ✅ Text (Production Doc): {txt_path}")
            
            # Export to JSON file
            self._export_json(all_outlines, json_path)
            print(f"  ✅ JSON (Data): {json_path}")
            
            # Save summary to Redis
            print("\n💾 Saving to Redis...")
            outline_summary = {
                'session_id': self.session_id,
                'total_episodes': total_episodes,
                'total_scenes': total_scenes,
                'episodes': [
                    {
                        'episode_number': outline.episode_number,
                        'scene_count': len(outline.scenes)
                    }
                    for outline in all_outlines
                ]
            }
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_15",
                json.dumps(outline_summary)
            )
            print("✅ Saved to Redis\n")
            
            result = {
                'station': 'station_15_detailed_episode_outlining',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path
                },
                'statistics': {
                    'total_episodes': total_episodes,
                    'outlines_generated': len(all_outlines),
                    'scenes_per_episode': total_scenes / total_episodes if total_episodes > 0 else 0,
                    'ready_for_production': True
                }
            }
            
            print(f"{'='*70}")
            print(f"✅ STATION 15 COMPLETE: {total_episodes} Episode Outlines Ready")
            print(f"{'='*70}\n")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error in Station 15: {str(e)}")
            raise
        finally:
            await self.redis_client.disconnect()
    
    def _extract_json_from_response(self, response: str) -> Optional[str]:
        """
        Extract JSON from LLM response using multiple strategies
        
        Args:
            response: Raw LLM response text
            
        Returns:
            Extracted JSON string or None if extraction fails
        """
        import re
        
        try:
            # Strategy 1: Look for complete JSON objects with balanced braces
            json_pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\})*)*\}))*\}'
            matches = re.findall(json_pattern, response, re.DOTALL)
            
            if matches:
                # Try to find the most complete match (largest one)
                for match in sorted(matches, key=len, reverse=True):
                    try:
                        json.loads(match)  # Validate JSON
                        return match
                    except json.JSONDecodeError:
                        continue
            
            # Strategy 2: Look for JSON code blocks
            code_block_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if code_block_match:
                return code_block_match.group(1)
            
            # Strategy 3: Look for the first { and find its matching }
            first_brace = response.find('{')
            if first_brace != -1:
                brace_count = 0
                in_string = False
                escape_next = False
                
                for i, char in enumerate(response[first_brace:], first_brace):
                    if escape_next:
                        escape_next = False
                        continue
                    
                    if char == '\\':
                        escape_next = True
                        continue
                    
                    if char == '"' and not escape_next:
                        in_string = not in_string
                    
                    if not in_string:
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                return response[first_brace:i+1]
            
            return None
            
        except Exception as e:
            print(f"⚠️ JSON extraction failed: {e}")
            return None
    
    async def _process_single_episode(self, data: Station15Input) -> Station15Output:
        """
        Process a single episode outline
        
        Args:
            data: Station15Input with episode details
            
        Returns:
            Validated Station15Output Pydantic object
            
        Raises:
            ValidationError: If LLM response doesn't match expected schema
            Exception: For other errors during processing
        """
        # Load context from Redis (connection already initialized in run())
        context = await self.load_context_from_redis()
        
        if self.debug_mode:
            if not context.get('character_bible'):
                print("⚠️ Warning: Character Bible not found. Outline may lack character details.")
            if not context.get('world_bible'):
                print("⚠️ Warning: World Bible not found. Outline may lack location details.")
            if not context.get('reveal_matrix'):
                print("⚠️ Warning: Reveal Matrix not found. Outline may lack structured reveals.")
        
        # Construct LLM prompt
        prompt = self._construct_llm_prompt(data, context)
        
        # Execute LLM call
        if self.debug_mode:
            print(f"  ⚙️ Generating outline using {self.model_name}...")
        
        llm_response = await self.openrouter.generate(
            prompt=prompt,
            model=self.model_name,
            max_tokens=8000,  # Increased for detailed outline with proper JSON completion
            temperature=0.7
        )
        
        # Parse and validate response
        try:
            # Try to extract JSON using robust extraction
            extracted_json = self._extract_json_from_response(llm_response)
            
            if extracted_json:
                # Parse the extracted JSON
                parsed_json = json.loads(extracted_json)
            else:
                # Fallback to basic cleaning
                cleaned_response = llm_response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response[3:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                # Parse JSON
                parsed_json = json.loads(cleaned_response)
            
            # Validate against Pydantic model
            validated_output = Station15Output(**parsed_json)
            
            if self.debug_mode:
                print(f"  ✅ Validation successful: {len(validated_output.scenes)} scenes")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parsing Error for Episode {data.episode_number}: {str(e)}")
            if self.debug_mode:
                print(f"   Raw LLM response (first 500 chars):")
                print(f"   {llm_response[:500]}")
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
            
        except ValidationError as e:
            print(f"❌ Pydantic Validation Error for Episode {data.episode_number}:")
            print(f"   {str(e)}")
            raise Exception(f"Failed to validate LLM response: {str(e)}")
        
        # Save individual episode outline to Redis
        redis_key = f"audiobook:{self.session_id}:station_15_episode_{data.episode_number}"
        await self.redis_client.set(
            redis_key,
            validated_output.model_dump_json(indent=2)
        )
        
        return validated_output
    
    def _export_txt(self, all_outlines: List[Station15Output], filepath: str):
        """Export all episode outlines to a human-readable text file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 15: DETAILED EPISODE OUTLINES\n")
            f.write("Production-Ready Scene-by-Scene Breakdowns\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Total Episodes: {len(all_outlines)}\n")
            total_scenes = sum(len(outline.scenes) for outline in all_outlines)
            f.write(f"Total Scenes: {total_scenes}\n\n")
            
            # Write each episode outline
            for outline in all_outlines:
                f.write("=" * 70 + "\n")
                f.write(f"EPISODE {outline.episode_number}\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Total Scenes: {len(outline.scenes)}\n\n")
                
                # Write each scene
                for scene in outline.scenes:
                    f.write("-" * 70 + "\n")
                    f.write(f"SCENE {scene.scene_number}\n")
                    f.write("-" * 70 + "\n\n")
                    f.write(f"Location: {scene.location}\n")
                    f.write(f"Time: {scene.time}\n")
                    f.write(f"Characters Present: {', '.join(scene.characters_present)}\n")
                    f.write(f"Estimated Runtime: {scene.estimated_runtime}\n\n")
                    f.write(f"Goal-Obstacle-Choice-Consequence:\n{scene.goal_obstacle_choice_consequence}\n\n")
                    f.write(f"Reveal: {scene.reveal}\n\n")
                    f.write(f"Soundscape Notes:\n{scene.soundscape_notes}\n\n")
                    f.write(f"Transition to Next Scene:\n{scene.transition_to_next_scene}\n\n")
                
                f.write("\n")
    
    def _export_json(self, all_outlines: List[Station15Output], filepath: str):
        """Export all episode outlines to JSON format"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        export_data = {
            'session_id': self.session_id,
            'total_episodes': len(all_outlines),
            'total_scenes': sum(len(outline.scenes) for outline in all_outlines),
            'episodes': [outline.model_dump() for outline in all_outlines]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)


# ============================================================================
# STANDALONE EXECUTION (for testing)
# ============================================================================

if __name__ == "__main__":
    import sys
    import asyncio
    
    async def main():
        """Test Station 15 with sample data"""
        
        # Get session_id and episode_number from command line or use defaults
        if len(sys.argv) >= 3:
            session_id = sys.argv[1]
            episode_number = int(sys.argv[2])
        else:
            print("Usage: python station_15_detailed_episode_outlining.py <session_id> <episode_number>")
            print("Using test data instead...\n")
            session_id = "test_session"
            episode_number = 1
        
        # Sample blueprint summary (normally from Station 14)
        blueprint_summary = """
        Episode 1 opens with Sarah discovering a mysterious letter in her grandmother's attic. 
        The letter contains cryptic references to a family secret that has been hidden for decades. 
        As Sarah reads it, she realizes this could change everything she thought she knew about her family.
        
        The middle of the episode follows Sarah as she confronts her mother about the letter. 
        The conversation becomes increasingly tense as her mother tries to dismiss Sarah's questions, 
        but eventually breaks down and admits there's truth to what the letter suggests. 
        This revelation shakes Sarah's understanding of her own identity.
        
        By the end, Sarah must decide whether to pursue the truth or let sleeping secrets lie. 
        She makes a fateful phone call to an unknown number mentioned in the letter. 
        The episode ends with a voice on the other end that Sarah never expected to hear.
        """
        
        # Create input
        input_data = Station15Input(
            session_id=session_id,
            episode_number=episode_number,
            blueprint_summary=blueprint_summary
        )
        
        # Initialize and run agent
        agent = Station15DetailedEpisodeOutlining(session_id=session_id)
        result = await agent.run(input_data)
        
        # Print results
        print("\n📊 Station 15 Results:")
        print(f"Episode Number: {result.episode_number}")
        print(f"Total Scenes: {len(result.scenes)}")
        print("\nScene Breakdown:")
        for scene in result.scenes:
            print(f"\n  Scene {scene.scene_number}: {scene.location}")
            print(f"    Time: {scene.time}")
            print(f"    Characters: {', '.join(scene.characters_present)}")
            print(f"    Runtime: {scene.estimated_runtime}")
            print(f"    Reveal: {scene.reveal}")
    
    asyncio.run(main())

