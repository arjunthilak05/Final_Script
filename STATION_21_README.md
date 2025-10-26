# 🎬 STATION 21: FIRST DRAFT (SCENE-BY-SCENE)

## ✅ IMPLEMENTATION COMPLETE

Station 21 has been successfully implemented with full LLM-driven scene-by-scene script generation integrating all 20 previous stations.

---

## 📋 OVERVIEW

**Station 21: First Draft (Scene-by-Scene)** generates complete audio drama scripts with dialogue, audio cues, and stage directions. This is the first station to create actual production-ready dialogue.

### **Core Capabilities:**
1. **Scene-by-Scene Script Writing** - Complete dialogue and action
2. **Multi-Episode Management** - Draft episodes in any order
3. **Complete Context Integration** - Uses all 20 previous stations
4. **Audio-First Storytelling** - Every element designed for audio production
5. **Multi-Format Output** - Fountain, JSON, TXT, PDF-ready
6. **Human Review Gates** - Quality control at critical points
7. **Loop Capability** - Draft multiple episodes in sequence

---

## 🏗️ ARCHITECTURE

### **Files Created:**
- [app/agents/configs/station_21.yml](app/agents/configs/station_21.yml) - Configuration with comprehensive prompts
- [app/agents/station_21_first_draft.py](app/agents/station_21_first_draft.py) - Main implementation (~800 lines)

### **Dependencies (All 20 Previous Stations):**
**Foundation (1-9):**
- Station 1: Seed & Scale
- Station 2: Project Bible
- Station 3: Genre & Age
- Station 4: References
- Station 5: Season Architecture
- Station 6: Master Style Guide ⭐ (Character voices)
- Station 7: Character Bible
- Station 8: World Builder
- Station 9: World Building System ⭐ (Audio cue library)

**Planning (10-15):**
- Station 10: Reveal Strategy ⭐ (P3 Grid)
- Station 11: Runtime Planning ⭐ (Word budgets)
- Station 12: Hook & Cliffhanger ⭐
- Station 13: Timeline Manager
- Station 14: Simple Blueprints ⭐
- Station 15: Detailed Outlines ⭐

**Validation (16-20):**
- Station 16: Canon Check
- Station 17: Dialect Planning
- Station 18: Evergreen Check
- Station 19: Procedure Check
- Station 20: Geography/Transit

⭐ = Critical for script generation

### **Integration Points:**
- **Reads from:** Redis keys for all 20 stations
- **Writes to:**
  - `output/station_21/episode_XX/` (multiple formats)
  - `audiobook:{session_id}:station_21:episode_XX` (Redis)

---

## 🎯 FEATURES IMPLEMENTED

### **1. Episode Selection & Management**
- ✅ Interactive episode selection menu
- ✅ Validation status display for all episodes
- ✅ Draft status tracking
- ✅ Series completion percentage
- ✅ Can draft episodes in any order
- ✅ Resume capability (tracks what's been drafted)

### **2. Complete Context Loading**
- ✅ Loads all 20 previous stations from Redis
- ✅ Extracts episode-specific data (blueprints, outlines, runtime)
- ✅ Retrieves P3 plants from Station 10
- ✅ Gets audio cue library from Station 9
- ✅ Loads character voices from Station 6
- ✅ Accesses runtime/word budgets from Station 11
- ✅ Integrates hook strategies from Station 12

### **3. LLM-Driven Script Generation**
- ✅ 100% LLM-generated dialogue and action
- ✅ No hardcoded dialogue or scenes
- ✅ Dynamic prompt building from all context
- ✅ Scene-by-scene structure following outline
- ✅ Audio-first formatting with [SFX: ...] notation
- ✅ Character voice consistency
- ✅ P3 plant integration
- ✅ Information reveal control

### **4. Four Output Formats**
1. **Fountain** (`.fountain`) - Industry-standard screenplay format
2. **JSON** (`.json`) - Structured data for pipeline
3. **Plain Text** (`.txt`) - Human-readable backup
4. **Statistics** (`.txt`) - Analysis report

### **5. Human Interaction Points**
- **3 Required Human Interactions:**
  1. Episode Selection (start of process)
  2. Draft Review (after generation)
  3. Continue Loop (after saving)

- **Review Options:**
  - [Enter] - Approve and save
  - [R] - Regenerate entire draft
  - [E] - Edit specific scene
  - [V] - View complete script

### **6. Quality Features**
- ✅ Word count tracking vs target budget
- ✅ Scene breakdown with individual word counts
- ✅ Audio cue integration verification
- ✅ P3 plant tracking
- ✅ Character voice samples extracted
- ✅ Generation time monitoring
- ✅ Comprehensive statistics reporting

---

## 🚀 USAGE

### **Interactive Mode:**
```bash
python -m app.agents.station_21_first_draft
# Enter session ID when prompted
# Select episode to draft
# Review and approve draft
# Choose to continue or finish
```

### **Automated Mode (Testing):**
```python
from app.agents.station_21_first_draft import Station21FirstDraft

station = Station21FirstDraft(session_id, skip_review=True)
await station.initialize()
await station.run()
```

### **Example Flow:**
```
1. User runs Station 21
2. System loads all 20 previous stations
3. Displays episode selection menu
4. User selects Episode 1
5. System loads Episode 1 context (blueprint, outline, runtime, etc.)
6. System displays Episode 1 summary
7. LLM generates 2000-3500 word first draft (~5-10 minutes)
8. System displays draft with statistics
9. User reviews and approves
10. System saves 4 file formats + Redis
11. User chooses to draft Episode 2 or finish
```

---

## 📊 KEY TECHNICAL DETAILS

### **LLM Prompt Architecture:**
Station 21 builds a massive context-rich prompt that includes:

```
PROMPT SECTIONS (Dynamically Injected):
├─ Project Context (title, genre, episode info)
├─ Episode Blueprint (from Station 14)
├─ Detailed Outline (from Station 15 - scene-by-scene)
├─ Runtime Allocation (from Station 11 - word budgets)
├─ Reveal Strategy (from Station 10 - P3 plants)
├─ Hook Strategy (from Station 12)
├─ Character Voices (from Station 6)
├─ Audio Cue Library (from Station 9)
├─ World Context (from Stations 7-9)
├─ Validation Notes (from Stations 16-20)
└─ Comprehensive Writing Guidelines
```

### **Prompt Engineering:**
- **~3000 tokens of context** (project-specific data)
- **~2000 tokens of instructions** (writing guidelines)
- **~16K token output** (script generation)
- **Total: ~21K tokens per episode draft**

### **Word Count Philosophy:**
- **First drafts target 67-75% of final word count**
- Example: 4,883 word target → 3,287 word first draft (67%)
- Intentionally under-target to leave expansion room for:
  - Station 22: Polish Pass (add depth)
  - Station 23: Dialogue Polish (sharpen lines)
  - Station 24: Audio Cue Optimization

---

## 📄 OUTPUT FILE STRUCTURE

### **Directory Structure:**
```
output/station_21/
├── episode_01/
│   ├── episode_01_draft_data.json       (47 KB - Complete data)
│   ├── episode_01_first_draft.fountain  (12 KB - Industry format)
│   ├── episode_01_first_draft.txt       (11 KB - Plain text)
│   └── episode_01_draft_stats.txt       (8 KB - Statistics)
├── episode_02/
│   ├── ...
```

### **JSON Structure:**
```json
{
  "session_id": "session_20251019_160045",
  "episode_number": 1,
  "episode_title": "The Lighter",
  "generated_at": "2025-10-19T16:15:30Z",
  "draft_data": {
    "first_draft_script": {
      "episode_number": 1,
      "episode_title": "The Lighter",
      "total_word_count": 3287,
      "scenes": [
        {
          "scene_number": 1,
          "heading": "INT. POLICE EVIDENCE ROOM - NIGHT",
          "estimated_runtime": "4 minutes",
          "script_content": "[Complete formatted script with dialogue and SFX]",
          "word_count": 385,
          "characters_present": ["DETECTIVE CHEN", "CAPTAIN RODRIGUEZ"],
          "audio_cues_used": ["fluorescent_buzz", "box_scrape", "lighter_click"],
          "p3_plants_included": ["P_VI_001"],
          "reveals": ["New evidence discovered"],
          "emotional_beats": ["Detective's surprise", "Captain's resistance"]
        }
      ],
      "structural_elements": {
        "cold_open": "Scene 1",
        "act_1": "Scenes 2-4",
        "act_2": "Scenes 5-6",
        "act_3": "Scenes 7-8",
        "tag": "Scene 9"
      },
      "audio_summary": {
        "total_audio_cues": 47,
        "recurring_motifs": ["lighter_click", "rain"],
        "location_signatures": ["marcus_apartment", "police_station", "evidence_room"]
      },
      "character_summary": {
        "marcus_cole": {
          "lines_of_dialogue": 15,
          "key_moments": ["Lighter click habit", "Guilt over past", "Tag revelation"]
        },
        "sarah_chen": {
          "lines_of_dialogue": 18,
          "key_moments": ["Research obsession", "Calendar marking", "Breakthrough"]
        }
      },
      "hook_and_cliffhanger": {
        "opening_hook_effectiveness": "Mystery established in 60 seconds with evidence discovery",
        "cliffhanger_setup": "Marcus revealed as witness - lighter match confirmed"
      }
    },
    "generation_time": 512.3,
    "generated_at": "2025-10-19T16:15:30Z"
  },
  "context": {
    "word_budget": 4883,
    "runtime": "45 minutes"
  }
}
```

### **Fountain Format Sample:**
```fountain
Title: The Last Detective
Episode: 1 - The Lighter
Credit: First Draft
Draft date: 10/19/2025
Contact: [Production Contact]

===

INT. POLICE EVIDENCE ROOM - NIGHT (PRESENT DAY)

[SFX: Fluorescent buzz, footsteps on concrete, metal shelves]

The evidence room is quiet except for the hum of fluorescent
lights. DETECTIVE CHEN (30s, methodical) moves between shelves
of boxes, searching.

[SFX: Cardboard box scraping on metal shelf]

DETECTIVE CHEN
(muttering to self)
Box 847... 847... there.

[... script continues ...]
```

---

## 🎵 AUDIO-FIRST FORMATTING

### **SFX Notation:**
```
[SFX: Description of sound effect]
[SFX: Fluorescent buzz, footsteps on concrete]
[SFX: Lighter CLICK - distinctive metallic sound]
```

### **Voice Filters:**
```
CHARACTER NAME
(filtered through phone)
Dialogue here.

CHARACTER NAME
(V.O. - voice over)
Internal thought or narration.

CHARACTER NAME
(O.S. - off screen/off mic)
Character speaking from another room.

CHARACTER NAME
(whispered)
Quiet, intimate dialogue.
```

### **Stage Directions:**
```
Present tense, describe what we HEAR:
❌ "John walks to the window" (visual)
✅ "[SFX: Footsteps approach window, rain tapping on glass]" (audio)
```

---

## 🎯 INTEGRATION WITH PIPELINE

### **Upstream Dependencies:**
```
Stations 1-9 (Foundation) → Complete world and characters
    ↓
Stations 10-13 (Planning) → Reveal strategy, runtime, hooks
    ↓
Stations 14-15 (Blueprints) → Episode structure and outlines
    ↓
Stations 16-20 (Validation) → Quality checks passed
    ↓
STATION 21 (First Draft) → Scene-by-scene scripts generated
```

### **Downstream Usage:**
```
STATION 21 Output
    ↓
Station 22 (Polish Pass) → Expand and deepen
    ↓
Station 23 (Dialogue Polish) → Sharpen lines
    ↓
Station 24 (Audio Optimization) → Perfect sound design
    ↓
Station 25 (Final Script) → Production-ready
    ↓
Station 26 (Export) → Multiple format final delivery
```

---

## ✅ IMPLEMENTATION CHECKLIST

- [x] Station 21 YAML configuration with comprehensive prompt
- [x] Main Python implementation with episode management
- [x] Context loading from all 20 previous stations
- [x] Episode selection interface with validation display
- [x] LLM-driven scene-by-scene draft generation
- [x] Dynamic prompt building (no hardcoded values)
- [x] Audio-first formatting with [SFX: ...] notation
- [x] Character voice consistency enforcement
- [x] P3 plant integration tracking
- [x] Multi-format output generation (Fountain, JSON, TXT, Stats)
- [x] Human review interface with options
- [x] Regeneration capability
- [x] Loop capability for multiple episodes
- [x] Redis storage for Station 22
- [x] Statistics and analysis reporting
- [x] Complete error handling
- [x] Comprehensive documentation

---

## 🎉 SUCCESS METRICS

✅ **Code Quality:**
- 800+ lines of production-ready Python
- Full type hints and error handling
- Modular design with helper methods
- Follows established station patterns
- No hardcoded dialogue or scenes

✅ **LLM Integration:**
- 100% dynamic content generation
- Comprehensive context injection
- No fallback/hardcoded values
- JSON extraction and validation
- Error recovery with detailed logging

✅ **Output Quality:**
- Production-ready script formats
- Industry-standard Fountain format
- Complete audio cue integration
- Character voice consistency
- Proper scene structure

✅ **User Experience:**
- Clear episode selection interface
- Validation status visibility
- Progress tracking
- Quality review gates
- Multi-episode workflow

---

## 🚀 READY FOR PRODUCTION

Station 21 is fully implemented and ready to generate scene-by-scene first drafts for any audio drama project in the pipeline.

**What You Get:**
1. ✅ Complete dialogue-driven scripts
2. ✅ Audio-first formatting
3. ✅ Multi-format outputs
4. ✅ Full context integration
5. ✅ Quality control gates
6. ✅ Production-ready structure

**No hardcoded content - everything is LLM-generated from your project's unique context!**

---

**Implementation Date:** October 19, 2025
**Status:** ✅ Complete and Production-Ready
**LLM-Driven:** 100% Dynamic Content Generation
