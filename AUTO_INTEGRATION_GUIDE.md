# 🎯 Automatic Station Integration System

## Overview

Your audiobook production system now features **fully automatic station discovery and integration**. When you create a new station, it's automatically discovered and added to the pipeline - **no manual code changes needed!**

## What Was Implemented

### ✅ Core Components

1. **`app/agents/station_registry.py`** - Auto-discovery engine
   - Scans `app/agents/` for all station files
   - Reads YAML configs for dependencies and metadata
   - Resolves dependency order using topological sort
   - Dynamically loads station classes at runtime

2. **`station_creator_wizard.py`** (root level) - Station creation wizard
   - Interactive wizard to create custom stations
   - Generates Python code, YAML config, and test scripts
   - Stations are auto-integrated immediately

3. **`full_automation_dynamic.py`** - Dynamic automation runner
   - Automatically discovers all stations
   - Runs them in correct dependency order
   - No hardcoded station list!

4. **`resume_automation_dynamic.py`** - Dynamic resume script
   - Lists existing sessions
   - Resumes from any point
   - Auto-discovers remaining stations to run

5. **Updated YAML Configs** - All station configs now include:
   - `dependencies:` section listing required input stations
   - `enabled: true/false` flag to control pipeline inclusion

## How to Use

### 🚀 Creating a New Station

Simply run the wizard from the project root:

```bash
python station_creator_wizard.py
```

The wizard will:
1. ✅ Guide you through 8 interactive steps
2. ✅ Generate all necessary files
3. ✅ Place them in the correct directories
4. ✅ Station is **automatically integrated** - no manual edits needed!

### 🏭 Running Full Automation

Use the new dynamic automation runner:

```bash
python full_automation_dynamic.py
```

This will:
- 🔍 Auto-discover all enabled stations
- 📊 Show the complete pipeline with dependencies
- ⚡ Execute stations in correct dependency order
- 💾 Save checkpoints automatically

### 🔄 Resuming Automation

If a pipeline is interrupted:

```bash
python resume_automation_dynamic.py
```

This will:
- 📋 Show all existing sessions
- ✅ Let you choose which session to resume
- 🎯 Auto-resume from where it left off
- 📦 Run remaining stations automatically

## Pipeline Execution Order

The system automatically determines execution order based on dependencies. Current pipeline:

```
1. Station 1: Seed Processor (no dependencies)
2. Station 2: Project DNA Builder (depends on: 1)
3. Station 3: Age Genre Optimizer (depends on: 2)
4. Station 4: Reference Miner (depends on: 1, 2, 3)
5. Station 4.5: Narrator Strategy (depends on: 2, 3)
6. Station 5: Season Architecture (depends on: 2, 3, 4)
7. Station 6: Master Style Guide (depends on: 2, 3)
8. Station 7: Reality Check (depends on: 2, 3, 4, 5)
9. Station 8: Character Architecture (depends on: 2, 3, 4, 5)
10. Station 9: World Building (depends on: 2, 3, 8)
11. Station 10: Narrative Reveal Strategy (depends on: 2, 3, 8, 9)
12. Station 11: Runtime Planning (depends on: 5)
13. Station 12: Hook Cliffhanger (depends on: 5, 8)
14. Station 13: Multiworld Timeline (depends on: 5, 8, 9)
15. Station 14: Episode Blueprint (depends on: 5, 8, 9, 10, 11)
16. Station 15: Detailed Episode Outlining (depends on: 14)
17. Station 16: Canon Check (depends on: 8, 9, 15)
18. Station 17: Dialect Planning (depends on: 8, 15)
19. Station 18: Evergreen Check (depends on: 2, 15)
20. Station 19: Procedure Check (depends on: 15)
21. Station 20: Geography Transit (depends on: 9, 15)
```

**New stations you create will be automatically added to this pipeline in the correct position!**

## Example: Creating a Custom Station

Let's say you want to create a "Music Cue Generator" station:

```bash
$ python station_creator_wizard.py

🎯 STATION CREATOR WIZARD
============================================================

Step 1: Station Basics
📝 What would you like to name this station?
> Music Cue Generator

✨ STATION CREATED:
   Station Number: 21
   File: station_21_music_cue_generator.py
   
Does this look good? yes

Step 2: Station Purpose
📝 What should this station do?
> Analyze emotional beats and suggest background music cues

🤖 Generating professional description...

✨ STATION PURPOSE:
   "Analyzes the emotional tone and pacing of scenes to recommend
   appropriate background music cues that enhance the audio drama..."
   
Does this look good? yes

Step 3: Station Type
📋 Select: 1. Analysis  2. Generation  3. Enhancement  4. Validation
> 2

Step 4: Input Configuration
📥 Which stations provide data? (comma-separated)
> 8, 14, 15

✨ Will receive inputs from:
   - Station 8: Character Architecture
   - Station 14: Episode Blueprint
   - Station 15: Detailed Episode Outlining
   
Does this look good? yes

[... continues through remaining steps ...]

✅ STATION CREATED AND AUTO-INTEGRATED!

Files created:
  ✓ app/agents/station_21_music_cue_generator.py
  ✓ app/agents/configs/station_21.yml
  ✓ tools/test_station_21.py

Your station is now part of the pipeline!
Run: python full_automation_dynamic.py
```

## How It Works

### Auto-Discovery Process

1. **Scan** - Registry scans `app/agents/` for `station_*.py` files
2. **Parse** - Extracts station number from filename (handles `station_08`, `station_4_5`, etc.)
3. **Load Metadata** - Reads corresponding YAML config from `app/agents/configs/`
4. **Extract Dependencies** - Parses dependency list from YAML
5. **Topological Sort** - Determines correct execution order
6. **Dynamic Loading** - Imports station classes at runtime

### Dependency Resolution

The system uses a topological sort algorithm to determine execution order:

```python
# Automatic dependency resolution
Station 21 depends on [8, 14, 15]
→ Ensures 8, 14, and 15 run before 21
→ Detects circular dependencies
→ Optimizes execution order
```

### Station Configuration Format

Each station config (YAML) must include:

```yaml
# Station X: Name Configuration

model: "qwen-72b"
temperature: 0.7
max_tokens: 4000

prompts:
  main: |
    Your AI prompt here...

# Input dependencies (IMPORTANT for auto-discovery)
dependencies:
  - station: 8
    name: "Character Architecture"
  - station: 14
    name: "Episode Blueprint"
  - station: 15
    name: "Detailed Episode Outlining"

# Or if no dependencies:
# dependencies:
#   none: true

# Enable/disable in pipeline
enabled: true
```

## Managing Stations

### Enabling/Disabling Stations

Edit the station's YAML config:

```yaml
# To disable a station:
enabled: false

# To re-enable:
enabled: true
```

The system automatically skips disabled stations.

### Modifying Dependencies

Edit the `dependencies` section in the YAML config:

```yaml
dependencies:
  - station: 5
    name: "Season Architecture"
  - station: 8
    name: "Character Architecture"
  # Add more as needed
```

### Testing Individual Stations

Each created station gets its own test script:

```bash
python tools/test_station_21.py
```

## Backward Compatibility

The original automation scripts still work:

- ✅ `full_automation.py` - Original hardcoded version
- ✅ `resume_automation.py` - Original resume script

**Recommendation:** Use the new dynamic versions (`*_dynamic.py`) for automatic station integration.

## Advanced Features

### Custom Station Types

The wizard supports 4 station types:

1. **Analysis** - Examines data, provides insights
2. **Generation** - Creates new content
3. **Enhancement** - Improves existing content
4. **Validation** - Checks correctness

### AI Model Selection

Choose complexity level:

- **Simple** - Fast model (Claude Haiku) for basic tasks
- **Medium** - Balanced model (Qwen-72B) for most tasks
- **Complex** - Powerful model (Claude Sonnet 4) for sophisticated work

### Metadata in Configs

Station configs include metadata for tracking:

```yaml
metadata:
  station_number: 21
  station_name: "Music Cue Generator"
  station_type: "Generation"
  purpose: "Analyzes emotional beats..."
  created: "2025-10-12T..."
  created_by: "Station Creator Wizard"
```

## Troubleshooting

### Station Not Discovered

**Problem:** Created a station but it doesn't appear in the pipeline

**Solutions:**
1. Check filename follows pattern: `station_XX_name.py`
2. Ensure YAML config exists: `station_XX.yml`
3. Verify `enabled: true` in YAML
4. Check for syntax errors in Python file

### Circular Dependency Error

**Problem:** "Circular dependency detected involving station X"

**Solution:** Review dependencies in YAML configs. A station cannot depend on itself or create a dependency loop.

Example of circular dependency (BAD):
```
Station 21 → depends on 22
Station 22 → depends on 21  ❌ Circular!
```

### Wrong Execution Order

**Problem:** Station runs before its dependencies

**Solution:** Check the `dependencies` section in the station's YAML config. Add missing dependencies.

### Station Class Not Found

**Problem:** "Station X not found in registry"

**Solution:**
1. Verify the Python file exists in `app/agents/`
2. Check the class name matches the pattern: `Station##ClassName`
3. Ensure no syntax errors in the Python file

## File Structure

```
/home/arya/scrpt/
├── station_creator_wizard.py          # 🆕 Root-level wizard runner
├── full_automation_dynamic.py         # 🆕 Dynamic automation
├── resume_automation_dynamic.py       # 🆕 Dynamic resume
│
├── app/
│   └── agents/
│       ├── station_registry.py        # 🆕 Auto-discovery engine
│       ├── station_01_seed_processor.py
│       ├── station_02_project_dna_builder.py
│       ├── ...
│       ├── station_20_geography_transit.py
│       └── configs/
│           ├── station_1.yml          # ✏️ Updated with dependencies
│           ├── station_2.yml
│           └── ...
│
└── tools/
    └── tools/
        ├── station_creator_wizard.py  # Wizard implementation
        ├── station_generator.py       # ✏️ Updated code generator
        └── station_templates/
            ├── analysis_template.py
            ├── generation_template.py
            ├── enhancement_template.py
            └── validation_template.py
```

## Key Benefits

✅ **Zero Manual Integration** - Create stations and they just work
✅ **Automatic Dependency Resolution** - Correct execution order guaranteed
✅ **No Code Changes Needed** - No editing automation scripts
✅ **Flexible Pipeline** - Enable/disable stations with config flag
✅ **Dependency Validation** - Detects circular dependencies
✅ **Easy Testing** - Each station gets its own test script
✅ **Backward Compatible** - Old automation scripts still work

## Summary

Your audiobook production system is now **fully modular and self-extending**. When you create a new station using the wizard:

1. ✨ Files are generated automatically
2. 🔍 Station is immediately discovered
3. 📊 Dependencies are resolved
4. ⚡ Pipeline includes it automatically
5. 🚀 Ready to run!

**No manual code changes ever needed again!**

---

## Quick Reference

### Create a Station
```bash
python station_creator_wizard.py
```

### Run Full Pipeline
```bash
python full_automation_dynamic.py
```

### Resume a Session
```bash
python resume_automation_dynamic.py
```

### Test a Station
```bash
python tools/test_station_XX.py
```

### Disable a Station
Edit `app/agents/configs/station_XX.yml`:
```yaml
enabled: false
```

---

**🎉 Enjoy your fully automated, self-extending audiobook production system!**

