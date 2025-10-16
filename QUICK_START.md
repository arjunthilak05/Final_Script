# 🚀 QUICK START GUIDE - STATION 1 & 2

## ⚡ RUN STATION 1

```bash
python -m app.agents.station_01_seed_processor
```

### What happens:

1. **Choose seed type** → Enter 1, 2, 3, or 4
   - 1 = One-liner concept
   - 2 = Synopsis (any length)
   - 3 = Public domain script
   - 4 = Small idea/theme

2. **Enter your content** → Type your story, press Enter twice when done

3. **Choose scale** → See 3 options (A/B/C), choose one
   - A = MINI (3-6 episodes, 15-25 min)
   - B = STANDARD (8-12 episodes, 35-45 min)
   - C = EXTENDED (20-40 episodes, 35-45 min)

4. **Choose title** → See 3 titles, choose 1, 2, or 3

5. **View expansion** → Core premise, conflict, breaking points shown

6. **Get session ID** → Copy this for Station 2!

### Output files:
- `output/station_01/{session_id}_output.json`
- `output/station_01/{session_id}_readable.txt`

---

## ⚡ RUN STATION 2

```bash
python -m app.agents.station_02_project_dna_builder
```

### What happens:

1. **Enter session ID** → Paste the session_id from Station 1

2. **View Station 1 summary** → Quick recap of your choices

3. **Wait for generation** → 7 sections being created (~30-60 seconds)
   - 🌍 World & Setting
   - 📐 Format Specifications
   - 🎭 Genre & Tone
   - ✨ Creative Promises
   - 👥 Audience Profile
   - 🎬 Production Constraints
   - 🎯 Creative Team

4. **Get Project Bible** → Complete bible saved!

### Output files:
- `output/station_02/{session_id}_bible.json`
- `output/station_02/{session_id}_bible.txt`

---

## 📝 EXAMPLE SESSION

```
$ python -m app.agents.station_01_seed_processor

============================================================
🎬 STATION 1: SEED PROCESSOR & SCALE EVALUATOR
============================================================

📝 Welcome! Let's start with your story concept.

You can provide ONE of the following:

  1. A one-liner concept (single sentence)
  2. A synopsis (any length)
  3. A public domain script
  4. A small idea/theme

------------------------------------------------------------

👉 Which type are you providing? (1-4): 1

✅ You selected: one-liner

📝 Now, please enter your content:
(For multi-line input, press Enter twice when done)

A detective investigates mysterious disappearances in a small coastal town.


✅ Received 78 characters

🤖 Analyzing your concept and generating scale options...
⏳ This may take a moment...

✅ Scale options generated successfully

============================================================
📊 SCALE OPTIONS FOR YOUR STORY
============================================================

🔸 OPTION A: MINI SERIES
   Episodes: 3-6 episodes
   Length: 15-25 min each
   Word Count: 15,000-30,000 total
   Best For: contained stories, single mystery, limited cast
   Why: This tight mystery benefits from focused storytelling...

🔸 OPTION B: STANDARD SERIES
   Episodes: 8-12 episodes
   Length: 35-45 min each
   Word Count: 60,000-100,000 total
   Best For: character journeys, mystery with layers
   Why: Allows character development alongside mystery...

🔸 OPTION C: EXTENDED SERIES
   Episodes: 20-40 episodes
   Length: 35-45 min each
   Word Count: 150,000-300,000 total
   Best For: world-building, ensemble casts, epic scope
   Why: Perfect for complex town dynamics and secrets...

------------------------------------------------------------
💡 AI Recommends: Option B
------------------------------------------------------------

👉 Which option do you choose? (A/B/C): B

✅ You selected Option B: STANDARD

============================================================
📝 WORKING TITLE OPTIONS
============================================================

  1. Whispers from the Tide
  2. The Vanishing Shores
  3. Coastal Shadows

------------------------------------------------------------

👉 Which title do you prefer? (1/2/3): 2

✅ You selected: The Vanishing Shores

============================================================
📖 INITIAL EXPANSION GENERATED
============================================================

Core Premise:
A seasoned detective arrives in a fog-shrouded coastal town where locals have been vanishing without a trace. As he digs deeper, he uncovers a conspiracy tied to the town's maritime history.

Central Conflict:
The detective must navigate distrust from tight-lipped townsfolk while racing against time as disappearances accelerate, forcing him to question whether the threat is human or something darker.

Episode Rationale:
8-12 episodes allows layered mystery reveals, character arcs for town residents, and gradual escalation of tension while maintaining audio engagement.

Breaking Points:
  1. First victim's body found, revealing shocking evidence
  2. Detective discovers town's hidden maritime cult
  3. Detective himself becomes target, barely escaping
  4. Final confrontation at lighthouse during storm

Main Characters: Detective Marcus Webb, Sheriff Helen Cross, Lighthouse Keeper Thomas

✅ Output saved to:
   📄 output/station_01/session_20250116_143022_output.json
   📄 output/station_01/session_20250116_143022_readable.txt

============================================================
✅ STATION 1 COMPLETE!
============================================================

Project: The Vanishing Shores
Scale: STANDARD (8-12 episodes)
Session ID: session_20250116_143022

📌 Ready to proceed to Station 2: Project DNA Builder

✅ Success! Session ID: session_20250116_143022
```

---

## 📂 FILE STRUCTURE

After running both stations:

```
output/
├── station_01/
│   ├── session_20250116_143022_output.json
│   └── session_20250116_143022_readable.txt
└── station_02/
    ├── session_20250116_143022_bible.json
    └── session_20250116_143022_bible.txt
```

---

## ✅ CHECKLIST

### Before running:
- [ ] Redis server is running
- [ ] OpenRouter API key is set
- [ ] Config files exist in `app/agents/configs/`

### After Station 1:
- [ ] Session ID received
- [ ] Output files created in `output/station_01/`
- [ ] Readable TXT file looks correct

### After Station 2:
- [ ] Bible generated successfully
- [ ] Output files created in `output/station_02/`
- [ ] All 7 sections present in TXT file

---

## 🐛 COMMON ISSUES

**Issue:** "No such file or directory: output/station_01"
**Fix:** Directories are auto-created, but check permissions

**Issue:** "No Station 1 data found"
**Fix:** Make sure you copy the EXACT session_id from Station 1

**Issue:** "Redis connection failed"
**Fix:** Start Redis: `redis-server`

**Issue:** "OpenRouter API error"
**Fix:** Check your API key in `.env` or environment variables

---

## 🎯 WHAT YOU GET

### Station 1 Outputs:
- ✅ Seed type and content
- ✅ Chosen scale option (A/B/C)
- ✅ Chosen working title
- ✅ Core premise
- ✅ Central conflict
- ✅ Episode rationale
- ✅ Breaking points
- ✅ Main characters

### Station 2 Outputs:
- ✅ World & setting (7 fields)
- ✅ Format specifications (6 fields)
- ✅ Genre & tone (5 fields)
- ✅ Creative promises (3 fields)
- ✅ Audience profile (7 fields)
- ✅ Production constraints (9 fields)
- ✅ Creative team (7 fields)

**Total:** Complete Project Bible ready for production!

---

**Questions?** Check [STATION_1_2_CHANGES.md](./STATION_1_2_CHANGES.md) for detailed documentation.
