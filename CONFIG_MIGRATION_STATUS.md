# Station Configuration Migration Status

## Overview
This document tracks the migration of station configurations from hardcoded Python files to external YML configuration files.

## Completed Tasks

### 1. Infrastructure ✅
- Created `app/agents/config_loader.py` - Configuration loader utility
- Created `app/agents/configs/` directory for YML files
- PyYAML dependency verified

### 2. YML Configuration Files ✅
All 16 station YML configuration files have been created:
- ✅ `station_1.yml` - Seed Processor & Scale Evaluator
- ✅ `station_2.yml` - Project DNA Builder  
- ✅ `station_3.yml` - Age & Genre Optimizer
- ✅ `station_4.yml` - Reference Mining & Seed Extraction
- ✅ `station_4_5.yml` - Narrator Strategy Designer
- ✅ `station_5.yml` - Season Architecture
- ✅ `station_6.yml` - Master Style Guide
- ✅ `station_7.yml` - Reality Check
- ✅ `station_8.yml` - Character Architecture
- ✅ `station_9.yml` - World Building
- ✅ `station_10.yml` - Narrative Reveal Strategy
- ✅ `station_11.yml` - Runtime Planning
- ✅ `station_12.yml` - Hook & Cliffhanger Designer
- ✅ `station_13.yml` - Multiworld Timeline
- ✅ `station_14.yml` - Episode Blueprint
- ✅ `station_15.yml` - Detailed Episode Outlining

### 3. Python Files Updated ✅
Completed migrations:
- ✅ `station_01_seed_processor.py` - Updated to use config loader
- ✅ `station_02_project_dna_builder.py` - Updated to use config loader
- ✅ `station_03_age_genre_optimizer.py` - Updated to use config loader (including all sub-agents)

## Remaining Work

### Python Files Requiring Updates
The following stations still need to be updated to use the YML configs:
- ⏳ `station_04_reference_miner.py` - 6 model_name references
- ⏳ `station_04_5_narrator_strategy.py` - 3 model_name references
- ⏳ `station_05_season_architecture.py` - Model references to check
- ⏳ `station_06_master_style_guide.py` - Model references to check
- ⏳ `station_07_reality_check.py` - 1 model_name reference
- ⏳ `station_08_character_architecture.py` - 5 model_name references
- ⏳ `station_09_world_building.py` - 6 model_name references
- ⏳ `station_10_narrative_reveal_strategy.py` - Model references to check
- ⏳ `station_11_runtime_planning.py` - Model references to check
- ⏳ `station_12_hook_cliffhanger.py` - Model references to check
- ⏳ `station_13_multiworld_timeline.py` - Model references to check
- ⏳ `station_14_episode_blueprint.py` - Model references to check
- ⏳ `station_15_detailed_episode_outlining.py` - 1 model reference

## Migration Pattern

For each station file, the following changes are required:

### 1. Add Import
```python
from app.agents.config_loader import load_station_config
```

### 2. Load Config in __init__
```python
def __init__(self):
    # ... existing code ...
    
    # Load station configuration from YML
    self.config = load_station_config(station_number=X)  # or station_suffix="4_5"
    
    # Load prompts from config
    self.prompt_template = self.config.get_prompt('main')
    # or for multiple prompts:
    self.prompts = self.config.get_all_prompts()
```

### 3. Replace Model Name References
Replace all instances of:
```python
model_name="qwen-72b"
```
with:
```python
model_name=self.config.model
```

### 4. Update Prompt Loading
If prompts are loaded in methods like `_load_prompt_template()`, update them to use config:
```python
def _load_prompt_template(self) -> str:
    # This method is deprecated - prompt is now loaded from YML config
    return self.config.get_prompt('main')
```

## Benefits of This Migration

1. **Easy Model Switching** - Change LLM model for any station by editing YML file
2. **Prompt Iteration** - Update prompts without touching Python code
3. **Version Control** - Easier to track prompt changes in git
4. **Team Collaboration** - Non-developers can edit prompts
5. **A/B Testing** - Easier to test different prompts and models
6. **Configuration Management** - Centralized configuration for all stations
7. **Hot Reloading** - Potential to reload configs without restarting

## Next Steps

To complete the migration:

1. Update remaining station files (4-15, 4.5) following the migration pattern above
2. Test each updated station to ensure it still works correctly
3. Update any integration tests that may be affected
4. Document the new configuration system in README
5. Consider adding validation for YML files
6. Consider adding a config management CLI tool

## Configuration Structure

Each YML file follows this structure:

```yaml
# Station X: [Name] Configuration

model: "qwen-72b"  # OpenRouter model to use
temperature: 0.7   # Temperature setting
max_tokens: 3000   # Max tokens for generation

prompts:
  main: |
    [Main prompt text with {placeholders}]
  
  section_name: |
    [Additional prompts if needed]
```

## Testing

After migration, test each station:
1. Verify YML file loads correctly
2. Verify prompts are formatted correctly
3. Verify model is used correctly
4. Run end-to-end test of station
5. Check for any linter errors

## Troubleshooting

Common issues:
- **FileNotFoundError**: YML file not found - check filename matches station number
- **YAMLError**: Invalid YAML syntax - validate YML file
- **KeyError**: Prompt name not found - check prompt key in YML file
- **AttributeError**: Config not loaded - ensure config is loaded in __init__


