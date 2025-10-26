# Station 22 & 23: Quality Control Suite

## Overview

Stations 22 and 23 form the **Quality Control Suite** that validates and enhances first drafts from Station 21. These stations ensure professional pacing, momentum, and mystery/thriller storytelling through automated LLM-driven analysis and fixes.

**Station 22: Momentum Check** - Analyzes and fixes pacing, repetition, and energy flow issues
**Station 23: Twist Integration** - Validates P3 Grid compliance and integrates missing plants/payoffs

---

## Station 22: Momentum Check

### Purpose

Analyzes first drafts for momentum issues and automatically generates corrections to ensure engaging audio storytelling with professional pacing.

### Architecture

```
Station 22 Flow:
┌─────────────────────────────────────────────────────────────┐
│ 1. Load Station 21 First Drafts                            │
│ 2. Display Episode Selection Menu                          │
│ 3. Human Selects Episode                                   │
│ 4. Execute 4 Sequential LLM Analysis Tasks:                │
│    ├─ Task 1: Pacing Analysis                              │
│    ├─ Task 2: Repetition Detection                         │
│    ├─ Task 3: Energy Flow Analysis                         │
│    └─ Task 4: Auto-Fix Momentum (Generate Corrected Script)│
│ 5. Display Detected Issues Report                          │
│ 6. Display Corrected Draft with Changes                    │
│ 7. Human Review (Approve/Regenerate)                       │
│ 8. Save Multiple Formats + Change Report                   │
│ 9. Save to Redis for Station 23                            │
│ 10. Loop for Next Episode                                  │
└─────────────────────────────────────────────────────────────┘
```

### Input Sources

- **Station 21**: First draft scripts (required)
- **Model**: `anthropic/claude-3.5-sonnet`
- **Max Tokens**: 16,384 (for full script rewrites)

### Analysis Tasks

#### Task 1: Pacing Analysis
Detects:
- **Slow sections** - Scenes dragging without progress
- **Rushed transitions** - Important moments glossed over
- **Dead air** - Awkward silences with no tension
- **Rhythm problems** - Monotonous scene lengths

#### Task 2: Repetition Detection
Detects:
- **Word/phrase repetition** - Overused expressions
- **Structural repetition** - Same sentence patterns
- **Character repetition** - Characters repeating same actions
- **Beat repetition** - Story beats feeling redundant

#### Task 3: Energy Flow Analysis
Detects:
- **Energy plateaus** - Scenes at same intensity level
- **Poor tension/release balance** - Too much tension or too relaxed
- **Emotional pacing** - Emotional beats poorly spaced
- **Cliffhanger weakness** - End lacks momentum

#### Task 4: Auto-Fix Momentum
Generates:
- **Corrected script** with all issues fixed
- **Change report** documenting all modifications
- **Maintains**: Character voices, plot points, audio-first formatting
- **Changes**: Pacing, word choices, scene rhythm, transitions

### Output Files

Per episode, generates 4 files:

1. **`episode_XX_momentum_check.json`** - Complete analysis + corrected script
2. **`episode_XX_momentum_corrected.txt`** - Plain text corrected script
3. **`episode_XX_change_report.txt`** - Detailed change documentation
4. **Redis**: `audiobook:{session_id}:station_22:episode_XX` (for Station 23)

### Display Output Example

```
⚡ STATION 22: MOMENTUM CHECK
═══════════════════════════════════════════════════════════════════

📺 EPISODE SELECTION & MOMENTUM CHECK STATUS
═══════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────┐
│ Ep  Title                          Words      Status            │
├────────────────────────────────────────────────────────────────┤
│ 1   The Accidental Lifeline        2847       🟡 NEEDS CHECK    │
│ 2   Shadows in the ER              3012       🟡 NEEDS CHECK    │
└────────────────────────────────────────────────────────────────┘

🔍 DETECTED MOMENTUM ISSUES
═══════════════════════════════════════════════════════════════════

⏱️  PACING ISSUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Slow Sections: 2 found
    • Scene 3: Exposition about hospital procedures drags
    • Scene 7: Dialogue loop without new information

  Rushed Transitions: 1 found
    • Scene 5->6: Critical reveal happens too quickly

🔁 REPETITION ISSUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Repeated Words/Phrases: 4 found
    • 'you know' used 12 times
    • 'I think' used 8 times

⚡ ENERGY FLOW ISSUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Energy Problems: 2 found
    • Scenes 4-6: Three low-energy scenes consecutively
    • Scene 9: Emotional beat underplayed

📊 TOTAL ISSUES DETECTED: 9

✅ EPISODE 1: CORRECTED DRAFT
═══════════════════════════════════════════════════════════════════

CORRECTION STATISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Total Changes: 9
  • Original Word Count: 2847
  • Corrected Word Count: 2891
  • Word Count Change: +44

CHANGES MADE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. [PACING] Scene 3
     Trimmed exposition, added tension through sound design

  2. [REPETITION] Scene 4
     Removed 'you know' filler, tightened dialogue
```

### Usage

```bash
# Run Station 22
python -m app.agents.station_22_momentum_check

# Or programmatically
from app.agents.station_22_momentum_check import Station22MomentumCheck

station = Station22MomentumCheck(
    session_id="session_20251016_235335",
    skip_review=False  # Enable human review
)
await station.initialize()
await station.run()
```

### Configuration

Located at: [`app/agents/configs/station_22.yml`](app/agents/configs/station_22.yml)

Key settings:
- **Model**: `anthropic/claude-3.5-sonnet`
- **Temperature**: 0.7
- **Max Tokens**: 16,384
- **Output Directory**: `output/station_22`

---

## Station 23: Twist Integration

### Purpose

Validates Plant/Proof/Payoff (P3) Grid compliance and automatically integrates missing elements. Ensures mystery/thriller storytelling follows proper reveal strategy with balanced misdirection.

### Architecture

```
Station 23 Flow:
┌─────────────────────────────────────────────────────────────┐
│ 1. Load Scripts from Station 21/22 (prefers 22)            │
│ 2. Load P3 Grid from Station 10                            │
│ 3. Display Episode Selection Menu                          │
│ 4. Human Selects Episode                                   │
│ 5. Execute 4 Sequential LLM Validation Tasks:              │
│    ├─ Task 1: P3 Cross-Reference (Plant Detection)         │
│    ├─ Task 2: Payoff Validation (Premature Reveal Check)   │
│    ├─ Task 3: Misdirection Balance (Red Herring Analysis)  │
│    └─ Task 4: Auto-Integrate Fixes (Rewrite with P3s)      │
│ 6. Display P3 Validation Report                            │
│ 7. Display Enhanced Script with Integrated Elements        │
│ 8. Human Review (Approve/Regenerate)                       │
│ 9. Save Enhanced Script + P3 Compliance Report             │
│ 10. Save to Redis for Station 24+                          │
│ 11. Loop for Next Episode                                  │
└─────────────────────────────────────────────────────────────┘
```

### Input Sources

- **Station 22**: Momentum-corrected scripts (preferred)
- **Station 21**: First drafts (fallback if Station 22 not run)
- **Station 10**: P3 Grid / Reveal Strategy (required)
- **Model**: `anthropic/claude-3.5-sonnet`
- **Max Tokens**: 16,384

### Validation Tasks

#### Task 1: P3 Cross-Reference
Validates:
- **Missing plants** - Required plants not present in script
- **Weak plants** - Plants too subtle for audience to notice
- **Misplaced plants** - Plants appearing in wrong episode
- **Missing proofs** - Evidence not properly shown

**Plant Strength Criteria:**
- **Strong Plant**: Clear, memorable, audience will notice
- **Weak Plant**: Too subtle, audience may miss
- **Missing Plant**: Not present in script at all

#### Task 2: Payoff Validation
Checks for:
- **Premature payoffs** - Reveals scheduled for later episodes
- **Unearned reveals** - Payoffs without sufficient plants/proofs
- **Too explicit** - Should hint, not confirm
- **Missing ambiguity** - Needs room for audience speculation

#### Task 3: Misdirection Balance
Analyzes:
- **Red herring timing** - Introduced at right time?
- **Suspicion distribution** - Is one character TOO suspicious?
- **Fair play** - Are clues present but not obvious?
- **Balance** - Multiple plausible suspects/explanations?

**Ideal Balance:**
- Guilty party: 40% suspicious (hidden in plain sight)
- Red herrings: 30-60% suspicious (plausible alternatives)
- Innocents: 10-20% suspicious (everyone has secrets)

#### Task 4: Auto-Integrate Fixes
Generates enhanced script with:
- **Missing plants added** - Integrated naturally and organically
- **Weak plants strengthened** - Made more memorable
- **Premature payoffs fixed** - Converted to hints
- **Misdirection balanced** - Suspicion levels adjusted
- **Misplaced elements removed** - Wrong-episode content deleted

### P3 Integration Principles

**Adding Plants:**
- Make them feel natural, not forced
- Characters shouldn't draw attention to them
- Plants can be dialogue, action, or sound
- Place in moments of other activity (hide in plain sight)

**Fixing Premature Payoffs:**
- Convert explicit to ambiguous
- Show evidence, don't explain it
- Let audience suspect, don't confirm
- Save "aha moment" for proper episode

**Strengthening Weak Plants:**
- Add emphasis (pause, reaction, repeat)
- Make more distinctive
- Add character attention to it
- Link to emotion or action

**Balancing Misdirection:**
- Give innocent explanations for suspicious behavior
- Add logical reasons for evasion
- Reduce certainty in audience
- Maintain fair play

### Output Files

Per episode, generates 3 files:

1. **`episode_XX_twist_integrated.json`** - Complete validation + enhanced script
2. **`episode_XX_twist_integrated.txt`** - Plain text enhanced script
3. **`episode_XX_p3_validation.txt`** - P3 compliance report
4. **Redis**: `audiobook:{session_id}:station_23:episode_XX` (for Station 24+)

### Display Output Example

```
🎭 STATION 23: TWIST INTEGRATION (P3 VALIDATION)
═══════════════════════════════════════════════════════════════════

📺 EPISODE SELECTION & P3 VALIDATION STATUS
═══════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────┐
│ Ep  Source       Words      P3 Status                          │
├────────────────────────────────────────────────────────────────┤
│ 1   St22✅       2891        🟡 NEEDS P3 VALIDATION             │
│ 2   St21         3012        🟡 NEEDS P3 VALIDATION             │
└────────────────────────────────────────────────────────────────┘

📊 P3 GRID STATISTICS:
  • Major Twists/Reveals: 6
  • Red Herrings: 3
  • Episodes Validated: 0/2
  • Completion: 0%

🎭 P3 VALIDATION REPORT
═══════════════════════════════════════════════════════════════════

🌱 PLANT COMPLIANCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Required Plants: 4
  ✅ Strong Plants: 2
  ⚠️  Weak Plants: 1
  ❌ Missing Plants: 1
  Compliance: 75%

🎯 PAYOFF TIMING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ❌ Premature Reveals: 1
    • Scene 9: Marcus admits guilt explicitly

  ⚠️  Unearned Payoffs: 0

🎭 MISDIRECTION BALANCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Marcus: 40% (target: 40%)
  ⚠️  Sarah: 65% (target: 50%)
  ✅ Rodriguez: 30% (target: 30%)

  Fair Play: ✅
  Balance Rating: needs_adjustment

📊 TOTAL P3 ISSUES: 3

✨ EPISODE 1: P3-ENHANCED SCRIPT
═══════════════════════════════════════════════════════════════════

P3 INTEGRATION STATISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Total P3 Integrations: 3
  • Word Count Change: +47 words
  • P3 Compliance Before: 3/4 plants present
  • P3 Compliance After: 4/4 plants present

P3 INTEGRATIONS MADE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. [PLANT_ADDITION] Scene 4
     P3 Marker: P_MC_002
     Technique: Integrated lighter click during dialogue about stress

  2. [PAYOFF_FIX] Scene 9
     P3 Marker: T_MC_001
     Technique: Changed explicit admission to ambiguous reaction

  3. [MISDIRECTION_BALANCE] Scene 6
     P3 Marker: RH_SAR_001
     Technique: Added innocent explanation for Sarah's evasiveness
```

### Usage

```bash
# Run Station 23
python -m app.agents.station_23_twist_integration

# Or programmatically
from app.agents.station_23_twist_integration import Station23TwistIntegration

station = Station23TwistIntegration(
    session_id="session_20251016_235335",
    skip_review=False  # Enable human review
)
await station.initialize()
await station.run()
```

### Configuration

Located at: [`app/agents/configs/station_23.yml`](app/agents/configs/station_23.yml)

Key settings:
- **Model**: `anthropic/claude-3.5-sonnet`
- **Temperature**: 0.7
- **Max Tokens**: 16,384
- **Output Directory**: `output/station_23`

---

## Integration with Pipeline

### Data Flow

```
Station 21 (First Draft)
    ↓
    ├─→ Station 22 (Momentum Check)
    │       ↓
    │   [Corrected Script]
    │       ↓
    └─→ Station 23 (Twist Integration)
            ↓
        [P3-Enhanced Script]
            ↓
        Station 24+ (Subsequent Stations)
```

### Redis Keys

**Station 22 Output:**
- Key: `audiobook:{session_id}:station_22:episode_{XX}`
- Contains: Momentum-corrected script + analysis

**Station 23 Output:**
- Key: `audiobook:{session_id}:station_23:episode_{XX}`
- Contains: P3-enhanced script + validation

**Station 23 Input Sources:**
- Primary: `audiobook:{session_id}:station_22:episode_{XX}` (if available)
- Fallback: `audiobook:{session_id}:station_21:episode_{XX}`
- P3 Grid: `audiobook:{session_id}:station_10`

---

## Human Interaction Points

### Station 22 Human Review

After generating corrected draft:

**Options:**
- **[Enter]** - Approve and save (recommended)
- **[R]** - Regenerate entire corrected draft
- **[V]** - View complete corrected script
- **[C]** - View detailed change report

### Station 23 Human Review

After integrating P3 elements:

**Options:**
- **[Enter]** - Approve and save (recommended)
- **[R]** - Regenerate P3 integrations
- **[V]** - View complete enhanced script
- **[D]** - View detailed P3 integration report

---

## Design Principles

### 100% LLM-Driven

**NO Hardcoded Fixes:**
- All corrections generated dynamically by LLM
- All P3 integrations crafted by LLM based on context
- No fallback content or templates
- Complete reliance on previous station data

**Dynamic Context Injection:**
- Station 22: Uses first draft from Station 21
- Station 23: Uses Station 10 P3 Grid + Station 21/22 scripts
- All prompts filled with project-specific data

### Audio-First Focus

**Maintains Audio Formatting:**
- All corrections preserve `[SFX: ...]` notation
- Pacing fixes consider audio runtime
- P3 plants can be sound-based (e.g., distinctive click)
- Energy flow considers auditory tension

### Character Voice Consistency

**Preserves Character Identity:**
- Momentum fixes don't change how characters speak
- P3 integrations use character-appropriate language
- Dialogue tightening maintains voice patterns
- Natural integration that fits character behavior

---

## Testing

### Station 22 Test

```python
# Test with real session data
python -m app.agents.station_22_momentum_check
# Enter session ID: session_20251016_235335
# Select episode: 1
# Review changes
# Approve
```

### Station 23 Test

```python
# Test with real session data (requires Station 10)
python -m app.agents.station_23_twist_integration
# Enter session ID: session_20251016_235335
# Select episode: 1
# Review P3 integrations
# Approve
```

### Automated Testing

```python
# Skip human review for automated testing
station_22 = Station22MomentumCheck(session_id, skip_review=True)
await station_22.initialize()
await station_22.run()

station_23 = Station23TwistIntegration(session_id, skip_review=True)
await station_23.initialize()
await station_23.run()
```

---

## File Structure

```
app/agents/
├── configs/
│   ├── station_22.yml          # Momentum check prompts
│   └── station_23.yml          # P3 validation prompts
├── station_22_momentum_check.py    # Main Station 22 class
└── station_23_twist_integration.py # Main Station 23 class

output/
├── station_22/
│   └── episode_01/
│       ├── episode_01_momentum_check.json
│       ├── episode_01_momentum_corrected.txt
│       └── episode_01_change_report.txt
└── station_23/
    └── episode_01/
        ├── episode_01_twist_integrated.json
        ├── episode_01_twist_integrated.txt
        └── episode_01_p3_validation.txt
```

---

## Key Features

### Station 22 Features

✅ **Pacing Analysis** - Detects slow/rushed/dead sections
✅ **Repetition Detection** - Finds overused words/patterns
✅ **Energy Flow Analysis** - Validates tension/release balance
✅ **Auto-Fix Generation** - Creates corrected script automatically
✅ **Change Tracking** - Documents all modifications
✅ **Episode Loop** - Process multiple episodes in one session

### Station 23 Features

✅ **P3 Cross-Reference** - Validates plant placement
✅ **Payoff Validation** - Detects premature reveals
✅ **Misdirection Balance** - Analyzes suspicion distribution
✅ **Auto-Integration** - Adds missing P3 elements naturally
✅ **Fair Play Check** - Ensures mystery is solvable
✅ **Compliance Scoring** - Before/after P3 compliance metrics

---

## Dependencies

### Python Packages

- `asyncio` - Async LLM calls
- `json` - Data serialization
- `yaml` - Configuration loading
- `pathlib` - File path handling

### Internal Dependencies

- `OpenRouterAgent` - LLM communication
- `RedisClient` - Inter-station data storage
- `config_loader` - YAML configuration loading
- `json_extractor` - Robust JSON parsing

### Station Dependencies

**Station 22 Requires:**
- Station 21 (First Draft)

**Station 23 Requires:**
- Station 21 (First Draft) OR Station 22 (Momentum Corrected)
- Station 10 (Reveal Strategy / P3 Grid)

---

## Troubleshooting

### "No first drafts found"
**Solution:** Run Station 21 first to generate episode drafts

### "P3 Grid not available"
**Solution:** Run Station 10 first to generate reveal strategy

### JSON Extraction Errors
**Solution:** Check LLM output format, increase max_tokens if truncated

### Redis Connection Failed
**Solution:** Ensure Redis is running and configured correctly

---

## Future Enhancements

### Potential Additions

1. **Scene-by-Scene Momentum Graph** - Visual pacing representation
2. **Comparative Analysis** - Compare momentum across episodes
3. **Plant Strength Scoring** - Quantitative plant effectiveness metrics
4. **Automated Suspicion Calibration** - Auto-adjust to ideal percentages
5. **Cross-Episode P3 Tracking** - Validate plants pay off later

---

## Credits

**Architecture**: Following Station 21 pattern
**LLM Model**: Anthropic Claude 3.5 Sonnet via OpenRouter
**Created**: 2025-10-20
**Version**: 1.0

---

## Summary

Stations 22 and 23 complete the quality control process for audio drama scripts:

- **Station 22** ensures professional momentum and pacing
- **Station 23** ensures perfect mystery/thriller P3 integration

Both stations are **100% LLM-driven** with no hardcoded content, dynamically generate fixes based on detected issues, and maintain audio-first storytelling principles throughout.
