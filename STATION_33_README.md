# Station 33: Pacing & Energy Analyzer

## Overview

Station 33 is a comprehensive pacing and energy analysis tool that evaluates audio drama scripts at both micro (within episodes) and macro (across episodes) levels. It identifies problem zones, analyzes rhythm patterns, and generates actionable pacing fixes.

## Purpose

- **Micro-Pacing Analysis**: Scene-level pacing within individual episodes
- **Macro-Pacing Analysis**: Series-wide pacing patterns and energy trends
- **Attention Management**: Flag dead zones, overload zones, and repetition fatigue
- **Rhythm Solutions**: Generate specific, actionable fixes for pacing problems

## Prerequisites

- Must have completed Station 27 (Master Script Assembly)
- All episode scripts must be available in `output/station_27/`
- Redis connection (for optional data retrieval)

## Input

- **Episode Scripts**: Loaded from Station 27 output files
  - Format: JSON files in `output/station_27/episode_XX/`
  - Required fields: `format_conversion.fountain_script` or `master_script_assembly.master_script_text`

## Output Files

### 1. `pacing_chart.json`
Per-episode pacing metrics including:
- Scene length distribution
- Dialogue density analysis
- Sound density categorization
- Emotional pacing sequences
- Episode energy ratings

### 2. `energy_curve_data.json`
Series-wide energy analysis:
- Energy ratings per episode (1-10 scale)
- Energy trend (building/declining/stable)
- Visualization data for energy curve charts

### 3. `problem_zones.json`
Flagged issues with episode and scene IDs:
- **Dead Zones**: Scenes with no plot advancement
- **Overload Zones**: Scenes with too many events
- **Repetition Fatigue**: Repeated patterns across episodes
- **Audio Fatigue**: Monotonous audio patterns

### 4. `pacing_fixes.json`
Actionable solutions for each flagged problem:
- Specific fixes with before/after durations
- Scene IDs for modifications
- Implementation steps
- Priority rankings

### 5. `pacing_analysis_report.md`
Human-readable summary report including:
- Executive summary
- Energy trend analysis
- Problem zones overview
- Recommended fixes
- Error log (if any)

### 6. `error_log.txt` (if errors found)
Log of any processing errors or malformed data issues

## Usage

```bash
# Run Station 33
cd app/agents
python station_33_pacing_energy_analyzer.py <session_id>

# Example
python station_33_pacing_energy_analyzer.py auto_20251024_102126
```

## Workflow

1. **Load All Episodes**: Station 33 requires a complete dataset for macro analysis
2. **Task 1: Micro-Pacing** (per episode)
   - Analyze scene lengths, dialogue density, sound density, emotional pacing
   - Rate episode energy 1-10
3. **Task 2: Macro-Pacing** (all episodes)
   - Analyze energy trends across series
   - Check momentum and cliffhanger intensity
   - Track revelation pacing
4. **Task 3: Attention Management**
   - Flag dead zones, overload zones
   - Detect repetition and audio fatigue
5. **Task 4: Rhythm Solutions**
   - Generate specific fixes for each problem
   - Include before/after estimates
6. **Generate Output Files**: All JSON, markdown, and error logs
7. **User Validation Prompt**: Review fixes before applying

## Configuration

All thresholds are configurable in `app/agents/configs/station_33.yml`:

```yaml
thresholds:
  scene_length:
    short_max: 120  # seconds
    medium_max: 300  # seconds
  
  dialogue:
    fast_wpm: 160  # words per minute
    slow_wpm: 100  # words per minute
  
  energy:
    high_min: 7  # rating 1-10
    low_max: 3   # rating 1-10
  
  attention_risks:
    consecutive_high_intensity: 3  # scenes
    info_dump_reveals: 3  # per scene
    speaker_uninterrupted_max: 300  # seconds
```

## Key Features

### No Hardcoding
All thresholds and values are loaded from the config file. No hardcoded magic numbers.

### Robust Error Handling
- Missing timestamps: Logged, scene skipped with warning
- Malformed dialogue: Gracefully handled, reported in error log
- Missing episodes: Fails immediately with clear message (no silent skips)

### User Validation
After generating fixes, requires explicit user approval:
```
🔍 USER VALIDATION REQUIRED
Review pacing_fixes.json before applying solutions.
Apply pacing fixes? [y/n]:
```

### Context Requirements
Must load ALL episode scripts before processing. Fails if dataset is incomplete.

## Example Output

### `pacing_fixes.json` Excerpt
```json
{
  "fixes": [
    {
      "problem": "Episode 2, Scene 4: Dead zone - no plot advancement",
      "solution": "Add reveal: character discovers clue about mystery",
      "implementation": "Insert 2-minute scene section where character finds hidden message",
      "before_duration": "4 minutes",
      "after_duration": "6 minutes",
      "target_scene_id": "Scene 4A",
      "priority": "high"
    }
  ]
}
```

### `energy_curve_data.json` Excerpt
```json
{
  "energy_ratings": [
    {"episode_id": 1, "energy_rating": 7},
    {"episode_id": 2, "energy_rating": 5},
    {"episode_id": 3, "energy_rating": 8}
  ],
  "energy_trend": "building"
}
```

## Analysis Types

### Micro-Pacing
- **Scene Length Distribution**: Short/medium/long scenes, monotonous patterns
- **Dialogue Density**: WPM rates, fast/slow sections, silence gaps
- **Sound Density**: Audio activity levels, simultaneous sound overload
- **Emotional Pacing**: Intensity sequences, exhaustion/flatness risks

### Macro-Pacing
- **Episode Energy Ratings**: 1-10 scores across series
- **Momentum Analysis**: Building toward climaxes, rest episodes
- **Cliffhanger Intensity**: Variation and building trend
- **Revelation Pacing**: Info dump detection, gradual distribution

### Attention Management
- **Dead Zones**: No plot advancement, conflict, or reveals
- **Overload Zones**: Too many events or fast dialogue
- **Repetition Fatigue**: Repeated patterns
- **Audio Fatigue**: Monotonous audio patterns

### Rhythm Solutions
- **Slow Sections**: Urgency additions, dialogue trims, tension injections
- **Rushed Sections**: Scene splits, transition beats, pacing buffers
- **Monotonous Sections**: Sentence variation, sound texture, emotional shifts
- **Dead Zones**: Plot advancement, conflict, reveals
- **Overload Zones**: Prioritization, cuts, scene splits

## Testing

Test with incomplete/malformed data to verify error handling:
- Missing scene timestamps
- Malformed dialogue data
- Missing episode files

## Integration

- Uses utility functions from `app/utils/` for file I/O
- Logs to standard output (no separate log file)
- Progress tracking via existing logging framework
- No external API calls required (uses OpenRouterAgent for LLM analysis)

## Next Steps

After Station 33 analysis:
1. Review `pacing_analysis_report.md` for overview
2. Check `pacing_fixes.json` for specific solutions
3. Apply approved fixes to episode scripts
4. Re-run Station 27+ to regenerate updated scripts

## Troubleshooting

**Error: "No Station 27 data found"**
- Ensure Station 27 has been run successfully
- Check that `output/station_27/` directory exists with episode files

**Error: "No content available for analysis"**
- Verify episode files contain `format_conversion.fountain_script` or `master_script_assembly.master_script_text`
- Check file encoding (should be UTF-8)

**Warning: "Could not load episode from..."**
- Check file permissions
- Verify JSON files are valid

## Dependencies

- Station 27: Master Script Assembly (provides episode scripts)
- Python packages: asyncio, json, logging, pathlib, datetime, typing
- No external API dependencies (optional Redis connection)
