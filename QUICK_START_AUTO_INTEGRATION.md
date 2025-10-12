# 🚀 Quick Start: Auto-Integration System

## What's New?

Your station creation system now **automatically integrates** new stations into the pipeline!

## Create a New Station (3 Steps)

### Step 1: Run the Wizard

```bash
python station_creator_wizard.py
```

### Step 2: Answer Questions

The AI wizard asks you:
1. Station name
2. What it does
3. Station type (Analysis/Generation/Enhancement/Validation)
4. Which stations it needs data from
5. AI complexity (Simple/Medium/Complex)
6. Output format

**After each question, you approve or request changes.**

### Step 3: Done!

The wizard creates:
- ✅ `app/agents/station_XX_name.py` - Complete Python code
- ✅ `app/agents/configs/station_XX.yml` - Configuration
- ✅ `tools/test_station_XX.py` - Test script

**The station is automatically integrated!** No manual code changes needed.

## Run Your Pipeline

### Option 1: Full Pipeline (New Dynamic Version)

```bash
python full_automation_dynamic.py
```

**This automatically:**
- Discovers all stations (including any new ones you created)
- Resolves dependencies
- Runs them in correct order

### Option 2: Resume from Checkpoint

```bash
python resume_automation_dynamic.py
```

**This lets you:**
- List existing sessions
- Resume from where you left off
- Automatically runs remaining stations

## Example Session

```bash
$ python station_creator_wizard.py

# Answer the questions...
# Wizard generates files...

✅ STATION CREATED!
   Station 21: Music Cue Generator
   Auto-integrated into pipeline!

$ python full_automation_dynamic.py

🏭 PIPELINE EXECUTION ORDER
======================================================================
1. Station 1: Seed Processor
2. Station 2: Project DNA Builder
...
21. Station 20: Geography Transit
22. Station 21: Music Cue Generator    ← YOUR NEW STATION!
======================================================================

Enter story concept: A detective in a cyberpunk city...

[Pipeline runs automatically with your new station included!]
```

## Remove Custom Stations

Don't need a custom station anymore? Remove it easily:

```bash
# List custom stations
python remove_custom_stations.py --list

# Remove specific station
python remove_custom_stations.py --station 21

# Remove all custom stations
python remove_custom_stations.py --all-custom
```

**The pipeline automatically updates!** No code changes needed.

See `REMOVE_STATIONS_GUIDE.md` for details.

## Key Features

✅ **Zero Manual Integration** - Stations auto-integrate
✅ **Smart Dependencies** - Execution order automatically calculated
✅ **Enable/Disable** - Control stations via YAML config
✅ **Easy Removal** - Remove custom stations safely
✅ **No Code Edits** - Never touch automation scripts again

## That's It!

Create stations → They auto-integrate → Run pipeline → Remove if needed → Profit!

See `AUTO_INTEGRATION_GUIDE.md` for detailed documentation.

