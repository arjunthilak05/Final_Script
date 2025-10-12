# 🗑️ Custom Station Removal Guide

## Overview

The `remove_custom_stations.py` script safely removes custom stations created with `station_creator_wizard.py`.

**Key Features:**
- ✅ Lists all custom stations (number > 20)
- ✅ Removes specific stations or all custom stations
- ✅ Deletes Python file, YAML config, and test scripts
- ✅ **Works automatically with dynamic pipeline** - no code updates needed!
- ✅ Protects built-in stations (1-20) from accidental removal

## Why No Manual Updates Needed?

Because you're using the **auto-discovery system**, the dynamic automation scripts (`full_automation_dynamic.py` and `resume_automation_dynamic.py`) automatically detect when stations are removed. They simply won't find them anymore!

The original `full_automation.py` and `resume_automation.py` only use hardcoded stations 1-20, so custom stations don't affect them anyway.

---

## Usage

### 1. List Custom Stations

See what custom stations exist:

```bash
python remove_custom_stations.py --list
```

**Example Output:**
```
📋 CUSTOM STATIONS (Created with station_creator_wizard.py)
================================================================================

🔹 Station 21: Music Cue Generator
   Type: Generation Station
   Dependencies: [8, 14, 15]
   Python: station_21_music_cue_generator.py
   Config: station_21.yml
   Test: test_station_21.py

🔹 Station 22: Emotion Analyzer
   Type: Analysis Station
   Dependencies: [15]
   Python: station_22_emotion_analyzer.py
   Config: station_22.yml
   Test: test_station_22.py

================================================================================
Total custom stations: 2
```

### 2. Remove Specific Station

Remove a single station by number:

```bash
python remove_custom_stations.py --station 21
```

**Interactive confirmation:**
```
⚠️  CONFIRM REMOVAL
================================================================================
Station 21: Music Cue Generator
Type: Generation Station

Files to be deleted:
  • station_21_music_cue_generator.py
  • station_21.yml
  • test_station_21.py
================================================================================

❓ Proceed with removal? (yes/no): yes

🗑️  Removing Station 21...
   ✓ Deleted: station_21_music_cue_generator.py
   ✓ Deleted: station_21.yml
   ✓ Deleted: test_station_21.py

✅ Station 21 removed successfully!

ℹ️  The dynamic automation scripts will automatically detect the removal.
   No manual code updates needed!
```

### 3. Remove All Custom Stations

Remove all custom stations at once:

```bash
python remove_custom_stations.py --all-custom
```

**Confirmation prompt:**
```
⚠️  REMOVE ALL CUSTOM STATIONS
================================================================================
This will remove 2 custom station(s):

  • Station 21: Music Cue Generator
  • Station 22: Emotion Analyzer

================================================================================

❓ Remove ALL custom stations? (yes/no): yes

🗑️  Removing all custom stations...
[... removal process ...]

================================================================================
✅ Removal complete: 2 removed, 0 failed
================================================================================
```

### 4. Interactive Mode

Run without arguments for interactive menu:

```bash
python remove_custom_stations.py
```

**Interactive menu:**
```
📋 CUSTOM STATIONS
[... lists custom stations ...]

Choose an option:
  1. Remove a specific station
  2. Remove all custom stations
  3. Cancel

Enter choice (1-3): 1

Enter station number to remove: 21
[... removal process ...]
```

---

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--list` | List all custom stations without removing |
| `--station N` | Remove station number N (e.g., `--station 21`) |
| `--all-custom` | Remove all custom stations (number > 20) |
| `--help` | Show help message |

---

## What Gets Removed

For each station, the script removes:

1. **Python Implementation**
   - `app/agents/station_XX_name.py`

2. **YAML Configuration**
   - `app/agents/configs/station_XX.yml`

3. **Test Script** (if exists)
   - `tools/test_station_XX.py`

---

## Safety Features

### Protected Stations

Built-in stations (1-20, plus 4.5) **cannot be removed**:

```bash
$ python remove_custom_stations.py --station 8

❌ Cannot remove Station 8: Protected built-in station
   Only custom stations (number > 20) can be removed.
```

### Confirmation Required

Interactive confirmation for all removal operations:
- Single station removal: confirms before deleting
- All custom stations: confirms before batch deletion

### Auto-Discovery Integration

After removal, the dynamic pipeline automatically updates:

```
🔄 Reloading station registry...

🏭 PIPELINE EXECUTION ORDER
======================================================================
   1. Station 1: Seed Processor
   ...
  20. Station 20: Geography Transit
======================================================================
Total stations: 20

ℹ️  All custom stations removed. Only built-in stations remain.
```

---

## Examples

### Example 1: Remove Single Station

```bash
# List custom stations
python remove_custom_stations.py --list

# Remove station 21
python remove_custom_stations.py --station 21

# Verify removal
python remove_custom_stations.py --list
```

### Example 2: Clean Up All Custom Stations

```bash
# Remove all custom stations
python remove_custom_stations.py --all-custom

# Run pipeline (only built-in stations)
python full_automation_dynamic.py
```

### Example 3: Remove Station with Decimal Number

```bash
# Remove station 21.5
python remove_custom_stations.py --station 21.5
```

---

## After Removal

Once you remove a station:

1. **Dynamic scripts auto-update**: `full_automation_dynamic.py` and `resume_automation_dynamic.py` automatically detect the removal

2. **Pipeline recalculates**: Execution order is recalculated without the removed station

3. **No code changes needed**: The auto-discovery system handles everything

4. **Test immediately**:
   ```bash
   python full_automation_dynamic.py
   ```

---

## Troubleshooting

### Station Not Found

```
❌ Station 21 not found
```

**Solution:** The station may already be removed or never existed. Check with `--list`.

### Cannot Remove Protected Station

```
❌ Cannot remove Station 8: Protected built-in station
```

**Solution:** Only custom stations (number > 20) can be removed. Built-in stations are protected.

### Permission Denied

```
❌ Error removing station 21: Permission denied
```

**Solution:** Ensure you have write permissions for the `app/agents/` directory.

### Files Already Deleted

If files were manually deleted, the script will skip them:
```
✓ Deleted: station_21.yml
⚠️  File not found: station_21_music_cue_generator.py (already deleted)
```

---

## Integration with Other Tools

### With Station Creator

```bash
# Create a station
python station_creator_wizard.py

# Test it
python tools/test_station_21.py

# If you don't like it, remove it
python remove_custom_stations.py --station 21
```

### With Dynamic Automation

```bash
# Remove custom stations
python remove_custom_stations.py --all-custom

# Run pipeline (automatically excludes removed stations)
python full_automation_dynamic.py
```

### With Resume Automation

```bash
# Existing session won't break if you remove custom stations
# The resume script will skip removed stations automatically
python resume_automation_dynamic.py
```

---

## Best Practices

1. **Test Before Removing**: Make sure you don't need the station anymore

2. **Check Dependencies**: If other custom stations depend on the one you're removing, they may fail

3. **Backup First**: Consider backing up station files before removal:
   ```bash
   cp app/agents/station_21_*.py ~/backup/
   cp app/agents/configs/station_21.yml ~/backup/
   ```

4. **Remove Unused Stations**: Keep your pipeline clean by removing experimental or unused stations

5. **Use --list First**: Always check what custom stations exist before batch removal

---

## Quick Reference

```bash
# List custom stations
python remove_custom_stations.py --list

# Remove one station
python remove_custom_stations.py --station 21

# Remove all custom stations
python remove_custom_stations.py --all-custom

# Interactive mode
python remove_custom_stations.py

# Get help
python remove_custom_stations.py --help
```

---

## Why This Works Automatically

The removal script works seamlessly because:

1. **Auto-Discovery**: The `station_registry.py` scans `app/agents/` for station files
2. **Dynamic Loading**: Stations are loaded at runtime, not hardcoded
3. **No Static Imports**: Dynamic automation doesn't import stations by name
4. **Dependency Resolution**: Pipeline order is recalculated each time based on available stations

When you delete a station's files, the registry simply doesn't find it anymore. The pipeline automatically adjusts!

---

## Summary

- ✅ Safe removal with confirmation
- ✅ Protects built-in stations
- ✅ Removes all related files
- ✅ **No manual updates needed** (auto-discovery handles it!)
- ✅ Shows updated pipeline
- ✅ Command-line and interactive modes

**Remove stations confidently knowing the system will automatically adjust!** 🎉

