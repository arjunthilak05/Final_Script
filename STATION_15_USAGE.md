# Station 15: Detailed Episode Outlining - Usage Guide

## Overview

Station 15 expands simple episode blueprints (from Station 14) into detailed, scene-by-scene outlines formatted for audio production. It uses strict Pydantic validation to ensure consistent data structure.

## Key Features

- **Pydantic Validation**: Strict type checking and data validation
- **Scene-by-Scene Breakdown**: Converts 2-3 paragraph summaries into ~8-15 detailed scenes
- **Audio-First Design**: No dialogue, focus on soundscape and audio storytelling
- **Reveal Integration**: Maps scenes to Plant/Proof/Payoff from Reveal Matrix
- **Production Ready**: Includes runtime estimates, character lists, and technical notes

## Models

### Input Model (Station15Input)
```python
class Station15Input(BaseModel):
    session_id: str
    episode_number: int
    blueprint_summary: str  # From Station 14
```

### Scene Model (SceneOutline)
```python
class SceneOutline(BaseModel):
    scene_number: int
    location: str
    time: str
    characters_present: List[str]
    goal_obstacle_choice_consequence: str
    reveal: str  # Plant/Proof/Payoff/None
    soundscape_notes: str
    transition_to_next_scene: str
    estimated_runtime: str
```

### Output Model (Station15Output)
```python
class Station15Output(BaseModel):
    episode_number: int
    scenes: List[SceneOutline]
```

## Usage Examples

### Basic Usage

```python
import asyncio
from app.agents.station_15_detailed_episode_outlining import (
    Station15DetailedEpisodeOutlining,
    Station15Input
)

async def outline_episode():
    # Create input
    input_data = Station15Input(
        session_id="auto_20251007_123810",
        episode_number=1,
        blueprint_summary="""
        Episode 1 opens with Sarah discovering a mysterious letter...
        (2-3 paragraph summary from Station 14)
        """
    )
    
    # Initialize agent
    agent = Station15DetailedEpisodeOutlining(session_id=input_data.session_id)
    
    # Run and get validated output
    result = await agent.run(input_data)
    
    # Access validated data
    print(f"Episode {result.episode_number} has {len(result.scenes)} scenes")
    for scene in result.scenes:
        print(f"Scene {scene.scene_number}: {scene.location}")
        print(f"  Characters: {', '.join(scene.characters_present)}")
        print(f"  Runtime: {scene.estimated_runtime}")

asyncio.run(outline_episode())
```

### Standalone Execution

```bash
# Test with sample data
python app/agents/station_15_detailed_episode_outlining.py

# Use specific session and episode
python app/agents/station_15_detailed_episode_outlining.py auto_20251007_123810 1
```

### Integration with Station 14

```python
import asyncio
import json
from app.agents.station_14_episode_blueprint import Station14EpisodeBlueprint
from app.agents.station_15_detailed_episode_outlining import (
    Station15DetailedEpisodeOutlining,
    Station15Input
)

async def blueprint_to_outline():
    session_id = "auto_20251007_123810"
    
    # Step 1: Generate blueprints (Station 14)
    station14 = Station14EpisodeBlueprint(session_id)
    blueprint_result = await station14.run()
    
    # Step 2: Expand each episode into detailed outline (Station 15)
    station15 = Station15DetailedEpisodeOutlining(session_id)
    
    for episode in blueprint_result['blueprint_bible']['episodes']:
        episode_num = episode['episode_number']
        blueprint_summary = episode['simple_summary']
        
        # Create input
        input_data = Station15Input(
            session_id=session_id,
            episode_number=episode_num,
            blueprint_summary=blueprint_summary
        )
        
        # Generate detailed outline
        outline = await station15.run(input_data)
        print(f"✅ Episode {episode_num}: {len(outline.scenes)} scenes outlined")

asyncio.run(blueprint_to_outline())
```

## Redis Storage

Station 15 saves validated outlines to Redis with the following key pattern:

```
audiobook:{session_id}:station_15_output_episode_{episode_number}
```

Example:
```
audiobook:auto_20251007_123810:station_15_output_episode_1
```

The value is a JSON-serialized `Station15Output` object.

## Context Dependencies

Station 15 loads the following from Redis:

1. **Project Bible** (Station 2): `audiobook:{session_id}:station_02`
2. **Character Bible** (Station 8): `audiobook:{session_id}:station_08`
3. **World Bible** (Station 9): `audiobook:{session_id}:station_09`
4. **Reveal Matrix** (Station 10): `audiobook:{session_id}:station_10`

These provide the LLM with full production context for generating accurate, consistent outlines.

## LLM Configuration

- **Model**: `qwen-72b` (qwen/qwen-2.5-72b-instruct:free)
- **Max Tokens**: 4000 (to accommodate detailed outlines)
- **Temperature**: 0.7 (balanced creativity and consistency)

## Validation Flow

1. **LLM Generation**: Prompt instructs model to output raw JSON
2. **Cleaning**: Removes markdown code blocks if present
3. **JSON Parsing**: Converts string to Python dict
4. **Pydantic Validation**: Validates against `Station15Output` schema
5. **Error Handling**: Raises detailed exceptions if validation fails

## Output Structure Example

```json
{
  "episode_number": 1,
  "scenes": [
    {
      "scene_number": 1,
      "location": "Sarah's grandmother's attic",
      "time": "Late afternoon",
      "characters_present": ["Sarah"],
      "goal_obstacle_choice_consequence": "Sarah wants to explore the attic but fears disturbing family history, chooses to open the old trunk, discovers mysterious letter",
      "reveal": "Plant: Family secret mentioned cryptically",
      "soundscape_notes": "Creaking floorboards, dust particles settling, rustling of old papers, distant sounds of traffic below",
      "transition_to_next_scene": "Sarah's breathing quickens as she reads the first line",
      "estimated_runtime": "2 minutes"
    },
    {
      "scene_number": 2,
      "location": "Sarah's kitchen",
      "time": "Evening",
      "characters_present": ["Sarah", "Mother"],
      "goal_obstacle_choice_consequence": "Sarah wants answers but mother deflects, chooses to press harder, mother finally breaks down",
      "reveal": "Proof: Mother confirms the letter's authenticity",
      "soundscape_notes": "Clinking dishes, tense silence, chair scraping, voice trembling",
      "transition_to_next_scene": "Mother leaves abruptly, door closes",
      "estimated_runtime": "3 minutes"
    }
  ]
}
```

## Error Handling

### Common Errors

1. **JSON Parse Error**: LLM didn't return valid JSON
   - Check raw LLM response
   - Verify prompt instructions

2. **Validation Error**: JSON structure doesn't match schema
   - Review Pydantic error details
   - Ensure all required fields present

3. **Missing Context**: Required bibles not in Redis
   - Verify previous stations completed
   - Check Redis keys

### Debug Tips

```python
try:
    result = await agent.run(input_data)
except Exception as e:
    print(f"Error: {str(e)}")
    # Check detailed error information
```

## Integration with Full Automation

To integrate Station 15 into the full automation pipeline, add it after Station 14 in `full_automation.py`:

```python
# After Station 14 completes
station14_result = await run_station_14()

# For each episode, generate detailed outline
for episode in station14_result['blueprint_bible']['episodes']:
    input_data = Station15Input(
        session_id=session_id,
        episode_number=episode['episode_number'],
        blueprint_summary=episode['simple_summary']
    )
    
    station15 = Station15DetailedEpisodeOutlining(session_id)
    outline = await station15.run(input_data)
    
    # Save or process outline as needed
```

## Benefits of Pydantic Validation

1. **Type Safety**: Ensures all fields have correct types
2. **Required Fields**: Automatically validates required fields present
3. **Data Consistency**: Guarantees uniform structure across episodes
4. **Automatic Serialization**: Easy JSON export with `model_dump_json()`
5. **IDE Support**: Type hints and autocomplete in development
6. **Error Messages**: Clear validation error messages for debugging

## Next Steps

After Station 15, the detailed scene-by-scene outlines are ready for:

- **Script Writing**: Convert scenes into full dialogue scripts
- **Production Planning**: Use runtime estimates for scheduling
- **Audio Direction**: Use soundscape notes for sound design
- **Voice Acting**: Use character emotional states for performance direction
- **Post-Production**: Use transitions for editing guidance

## Testing

Run the built-in test:

```bash
cd /home/arya/scrpt
python app/agents/station_15_detailed_episode_outlining.py
```

This will test with sample data and display the generated outline structure.

