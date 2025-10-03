# Full Automation & Resume Guide

## Overview

The audiobook production system now supports **full automation** through all 14 stations with **robust checkpoint/resume capabilities**. You can start, stop, and resume the automation at any point without losing progress.

## Key Features

✅ **Complete Pipeline**: Runs all 14 stations automatically (1 → 2 → 3 → 4 → 4.5 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14)
✅ **Automatic Checkpoints**: Progress saved after EVERY station
✅ **Resume Capability**: Continue from any checkpoint using session ID
✅ **Graceful Interruption**: Ctrl+C saves progress and shows resume command
✅ **Redis + JSON Storage**: Stations saved in both Redis (for inter-station access) and JSON checkpoints (for resume)
✅ **Interactive & CLI Modes**: Run interactively or with command-line arguments

---

## Quick Start

### 1. Start New Automation

**Interactive mode:**
```bash
python full_automation.py
```

**CLI mode with auto-approve:**
```bash
python full_automation.py --auto-approve --debug
```

**What happens:**
- You'll be prompted for a story concept
- System generates a unique session ID (e.g., `auto_20250103_142531`)
- Runs through all 14 stations automatically
- Saves checkpoint after each station
- Generates final summary and all PDFs

---

### 2. List Available Checkpoints

```bash
python full_automation.py --list-checkpoints
```

**Output:**
```
📋 AVAILABLE CHECKPOINTS
================================================================================

1. Session: auto_20250922_145032
   ⏰ Saved: 2025-09-22T15:00:41.656485
   📊 Progress: Station 7
   📝 Story: For one year, morning motivation coach Tom has been texting daily...
   📂 File: outputs/checkpoint_auto_20250922_145032.json

2. Session: auto_20250921_130832
   ⏰ Saved: 2025-09-21T13:15:22.123456
   📊 Progress: Station 5
   📝 Story: Sarah discovers an ancient journal in her grandmother's attic...
   📂 File: outputs/checkpoint_auto_20250921_130832.json

💡 Resume using: python full_automation.py --resume SESSION_ID
```

---

### 3. Resume from Checkpoint

**Interactive mode:**
```bash
python full_automation.py --resume auto_20250922_145032
```

**CLI mode:**
```bash
python full_automation.py --resume auto_20250922_145032 --auto-approve --debug
```

**What happens:**
- Loads checkpoint JSON
- Restores state (story concept, station outputs, settings)
- Continues from next incomplete station
- Runs remaining stations (e.g., if stopped at Station 7, resumes from Station 8)
- Saves checkpoints as it progresses
- Generates final summary when complete

---

## How Checkpoints Work

### Checkpoint Storage

**Location:** `outputs/checkpoint_<session_id>.json`

**Contents:**
```json
{
  "checkpoint_time": "2025-09-22T15:00:41.656485",
  "state": {
    "story_concept": "For one year, morning motivation coach Tom...",
    "session_id": "auto_20250922_145032",
    "current_station": 7,
    "station_outputs": {
      "station_1": { ... },
      "station_2": { ... },
      ...
      "station_7": { ... }
    },
    "chosen_scale": "B",
    "chosen_genre_blend": "Contemporary Drama",
    "generated_files": [
      "outputs/station4_seedbank_auto_20250922_145032.pdf",
      "outputs/station5_season_architecture_auto_20250922_145032.pdf",
      ...
    ],
    "errors": []
  }
}
```

### When Checkpoints are Saved

✅ **After each station completes** (automatic)
✅ **On graceful exit** (Ctrl+C during run)
✅ **Before final summary generation**

### Resume Logic

The system checks `current_station` and runs only incomplete stations:

```python
if state.current_station < 1:
    run Station 1
if state.current_station < 2:
    run Station 2
...
if state.current_station < 14:
    run Station 14
```

This ensures:
- No duplicate work
- Sequential execution
- All dependencies available (previous stations already complete)

---

## Usage Examples

### Example 1: Full Run Without Interruption

```bash
python full_automation.py --auto-approve
```

**Timeline:**
1. Enter story concept: "A detective solves mysteries with her talking cat..."
2. Session ID created: `auto_20250103_142531`
3. Stations 1-14 run sequentially (takes ~15-30 minutes with API calls)
4. Checkpoints saved: `outputs/checkpoint_auto_20250103_142531.json` (updated after each station)
5. Final summary: `outputs/automation_summary_auto_20250103_142531.json`
6. All PDFs generated in `outputs/`

---

### Example 2: Interrupted Run + Resume

**Initial run:**
```bash
python full_automation.py --auto-approve
```

**During Station 8 (Character Architecture), you press Ctrl+C:**
```
^C
👋 Automation stopped by user.
💾 Progress saved to checkpoint

💡 TIP: Resume using: python full_automation.py --resume auto_20250103_142531
```

**Resume later:**
```bash
python full_automation.py --resume auto_20250103_142531 --auto-approve
```

**Output:**
```
🔄 RESUME MODE
🆔 Session ID: auto_20250103_142531
============================================================
✅ Checkpoint loaded - resuming from Station 8

🎭 TESTING STATION 8: CHARACTER ARCHITECTURE
[runs Station 8]
✅ Station 8 completed!

🌍 TESTING STATION 9: WORLD BUILDING
[runs Station 9]
✅ Station 9 completed!

...continues through Station 14...

🎉 RESUMED AUTOMATION COMPLETED!
```

---

### Example 3: Checking Progress Manually

**List checkpoints:**
```bash
python full_automation.py --list-checkpoints
```

**Examine specific checkpoint:**
```bash
cat outputs/checkpoint_auto_20250103_142531.json | jq '.state.current_station'
# Output: 7
```

**View generated files:**
```bash
cat outputs/checkpoint_auto_20250103_142531.json | jq '.state.generated_files[]'
```

---

## CLI Arguments Reference

| Argument | Description | Example |
|----------|-------------|---------|
| `--resume <session_id>` | Resume from checkpoint | `--resume auto_20250103_142531` |
| `--list-checkpoints` | Show all available checkpoints | `--list-checkpoints` |
| `--auto-approve` | Auto-approve all decisions (no prompts) | `--auto-approve` |
| `--debug` | Enable debug logging | `--debug` |

**Combine arguments:**
```bash
python full_automation.py --resume auto_20250103_142531 --auto-approve --debug
```

---

## Troubleshooting

### "No checkpoint found for session"

**Cause:** Session ID doesn't exist or checkpoint file deleted
**Solution:**
1. Run `--list-checkpoints` to see available sessions
2. Use correct session ID
3. Or start new run without `--resume`

---

### "Station failed" During Resume

**Cause:** Redis data expired (1 hour TTL) or missing dependencies
**Solution:**
1. Check Redis is running: `redis-cli ping` (should return `PONG`)
2. If Redis data expired, checkpoint still has JSON data but station outputs may need regeneration
3. Consider running stations individually via `resume_automation.py`

---

### Resume Skips Stations

**Cause:** `current_station` already marked complete
**Expected:** System only runs incomplete stations (this is correct behavior!)
**Example:** If checkpoint shows `current_station: 7`, resume starts at Station 8

---

## File Structure

```
outputs/
├── checkpoint_auto_20250103_142531.json          # Resume checkpoint
├── automation_summary_auto_20250103_142531.json   # Final summary
├── station4_seedbank_auto_20250103_142531.pdf
├── station5_season_architecture_auto_20250103_142531.pdf
├── station6_master_style_guide_auto_20250103_142531.pdf
├── station7_reality_check_auto_20250103_142531.pdf
├── station8_character_bible_auto_20250103_142531.pdf
├── station9_world_bible_auto_20250103_142531.pdf
├── station10_narrative_reveal_auto_20250103_142531.pdf
├── station11_runtime_planning_auto_20250103_142531.pdf
├── station12_hooks_cliffhangers_auto_20250103_142531.pdf
├── station13_multiworld_timeline_auto_20250103_142531.pdf
└── station14_episode_blueprints_auto_20250103_142531.pdf  # HUMAN APPROVAL GATE
```

---

## Advanced: Manual Station-by-Station Resume

If full automation fails, use the individual station runner:

```bash
python resume_automation.py
```

**Interactive workflow:**
1. Shows available sessions from Redis
2. Select session number
3. Choose station to run (or accept suggested next station)
4. Runs single station
5. Offers to continue to next station

**Use case:** Debugging specific station failures or testing station outputs individually

---

## Best Practices

✅ **Let it run:** Full automation takes 15-30 mins. Let it complete for best results.
✅ **Use auto-approve for batch runs:** Add `--auto-approve` to avoid manual prompts
✅ **Check outputs directory:** Review PDFs after completion
✅ **Keep Redis running:** Stations communicate via Redis (1-hour data persistence)
✅ **Don't delete checkpoints:** They're your recovery mechanism

---

## What's Next After Automation?

After Station 14 completes:

1. **Review Episode Blueprints PDF** (`station14_episode_blueprints_*.pdf`)
2. **Human Approval Gate:** Review and approve/modify blueprint suggestions
3. **Proceed to Script Writing:** Use approved blueprints to write actual episode scripts (future stations 15+)

The system pauses at Station 14 because human creative input is critical for validating episode structure before script generation.

---

## Summary

| Feature | Status |
|---------|--------|
| Run all 14 stations | ✅ Working |
| Save checkpoints automatically | ✅ Working |
| Resume from any checkpoint | ✅ Working |
| List available checkpoints | ✅ Working |
| Graceful Ctrl+C handling | ✅ Working |
| CLI arguments (resume, debug, auto-approve) | ✅ Working |
| Redis + JSON dual storage | ✅ Working |
| PDF generation for all stations | ✅ Working |

**You're ready to automate!** 🚀
