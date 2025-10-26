# 🚀 HOW TO RUN EACH STATION INDIVIDUALLY

## Prerequisites
1. **Redis server running**: `redis-cli ping` should return PONG
2. **Environment variables set**: `OPENROUTER_API_KEY` and `REDIS_URL`
3. **Dependencies installed**: `pip install -r requirements.txt`

## Station Execution Order & Commands

### **Station 1: Seed Processor** (Interactive - requires user input)
```bash
python -m app.agents.station_01_seed_processor
```
**What it does:**
- Asks for story concept type (1-4)
- Takes your story input
- Generates 3 scale options (A/B/C)
- You choose scale
- Generates 3 titles
- You choose title
- Creates session ID

**Output:** `output/station_01/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 2: Project DNA Builder** (Needs Station 1 session ID)
```bash
python -m app.agents.station_02_project_dna_builder
```
**What it does:**
- Asks for session ID from Station 1
- Loads Station 1 data
- Generates Project Bible with 7 sections
- Saves comprehensive bible

**Output:** `output/station_02/session_YYYYMMDD_HHMMSS_bible.json`

---

### **Station 3: Age/Genre Optimizer** (Needs Station 2 session ID)
```bash
python -m app.agents.station_03_age_genre_optimizer
```
**What it does:**
- Asks for session ID from Station 2
- Loads previous station data
- Optimizes age targeting and genre blending
- Creates style guide

**Output:** `output/station_03/session_YYYYMMDD_HHMMSS_style_guide.json`

---

### **Station 4: Reference Mining** (Needs Station 3 session ID)
```bash
python -m app.agents.station_04_reference_mining
```
**What it does:**
- Asks for session ID from Station 3
- Loads previous station data
- Mines reference materials
- Generates seed content

**Output:** `output/station_04/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 4.5: Narrator Strategy Designer** (Needs Station 4 session ID)
```bash
python -m app.agents.station_045_narrator_strategy_designer
```
**What it does:**
- Asks for session ID from Station 4
- Loads previous station data
- Analyzes narrator necessity
- Creates narrator strategy

**Output:** `output/station_045/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 5: Season Architect** (Needs Station 4.5 session ID)
```bash
python -m app.agents.station_05_season_architect
```
**What it does:**
- Asks for session ID from Station 4.5
- Loads previous station data
- Designs season architecture
- Creates multi-season structure

**Output:** `output/station_05/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 6: Master Style Guide Builder** (Needs Station 5 session ID)
```bash
python -m app.agents.station_06_master_style_guide_builder
```
**What it does:**
- Asks for session ID from Station 5
- Loads previous station data
- Builds comprehensive style guide
- Creates master guidelines

**Output:** `output/station_06/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 7: Character Architect** (Needs Station 6 session ID)
```bash
python -m app.agents.station_07_character_architect
```
**What it does:**
- Asks for session ID from Station 6
- Loads previous station data
- Creates character bible
- Designs 3-tier character system

**Output:** `output/station_07/session_YYYYMMDD_HHMMSS_character_bible.json`

---

### **Station 8: World Builder** (Needs Station 7 session ID)
```bash
python -m app.agents.station_08_world_builder
```
**What it does:**
- Asks for session ID from Station 7
- Loads previous station data
- Builds world bible
- Creates audio-focused world architecture

**Output:** `output/station_08/session_YYYYMMDD_HHMMSS_world_bible.json`

---

### **Station 11: Runtime Planner** (Needs Station 8 session ID)
```bash
python -m app.agents.station_11_runtime_planner
```
**What it does:**
- Asks for session ID from Station 8
- Loads previous station data
- Plans production timeline
- Creates runtime planning

**Output:** `output/station_11/session_YYYYMMDD_HHMMSS_runtime_planning.json`

---

### **Station 12: Hook & Cliffhanger Designer** (Needs Station 11 session ID)
```bash
python -m app.agents.station_12_hook_cliffhanger_designer
```
**What it does:**
- Asks for session ID from Station 11
- Loads previous station data
- Designs hooks and cliffhangers
- Creates engagement strategies

**Output:** `output/station_12/session_YYYYMMDD_HHMMSS_hook_cliffhanger_design.json`

---

### **Station 13: Multi-World Timeline Manager** (Needs Station 12 session ID)
```bash
python -m app.agents.station_13_multi_world_timeline_manager
```
**What it does:**
- Asks for session ID from Station 12
- Loads previous station data
- Manages multi-world timelines
- Creates timeline management

**Output:** `output/station_13/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 14: Simple Episode Blueprint** (Needs Station 13 session ID)
```bash
python -m app.agents.station_14_simple_episode_blueprint
```
**What it does:**
- Asks for session ID from Station 13
- Loads previous station data
- Creates simple episode blueprints
- Generates stakeholder-ready summaries

**Output:** `output/station_14/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 15: Detailed Episode Outlining** (Needs Station 14 session ID)
```bash
python -m app.agents.station_15_detailed_episode_outlining
```
**What it does:**
- Asks for session ID from Station 14
- Loads previous station data
- Creates detailed episode outlines
- Generates production-ready outlines

**Output:** `output/station_15/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 16: Canon Check** (Needs Station 15 session ID)
```bash
python -m app.agents.station_16_canon_check
```
**What it does:**
- Asks for session ID from Station 15
- Loads previous station data
- Checks character and world consistency
- Validates canon

**Output:** `output/station_16/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 17: Dialect Planning** (Needs Station 16 session ID)
```bash
python -m app.agents.station_17_dialect_planning
```
**What it does:**
- Asks for session ID from Station 16
- Loads previous station data
- Plans voice consistency
- Creates dialect planning

**Output:** `output/station_17/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 18: Evergreen Check** (Needs Station 17 session ID)
```bash
python -m app.agents.station_18_evergreen_check
```
**What it does:**
- Asks for session ID from Station 17
- Loads previous station data
- Checks for dated references
- Ensures evergreen content

**Output:** `output/station_18/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 19: Procedure Check** (Needs Station 18 session ID)
```bash
python -m app.agents.station_19_procedure_check
```
**What it does:**
- Asks for session ID from Station 18
- Loads previous station data
- Validates professional procedures
- Checks procedure accuracy

**Output:** `output/station_19/session_YYYYMMDD_HHMMSS_output.json`

---

### **Station 20: Geography & Transit** (Needs Station 19 session ID)
```bash
python -m app.agents.station_20_geography_transit
```
**What it does:**
- Asks for session ID from Station 19
- Loads previous station data
- Validates location consistency
- Checks travel times

**Output:** `output/station_20/session_YYYYMMDD_HHMMSS_output.json`

---

## 📋 **Complete Workflow Example**

```bash
# 1. Start with Station 1 (interactive)
python -m app.agents.station_01_seed_processor
# Copy the session ID from output

# 2. Run Station 2
python -m app.agents.station_02_project_dna_builder
# Enter the session ID when prompted

# 3. Run Station 3
python -m app.agents.station_03_age_genre_optimizer
# Enter the session ID when prompted

# 4. Run Station 4
python -m app.agents.station_04_reference_mining
# Enter the session ID when prompted

# 5. Run Station 4.5
python -m app.agents.station_045_narrator_strategy_designer
# Enter the session ID when prompted

# Continue with remaining stations...
python -m app.agents.station_05_season_architect
python -m app.agents.station_06_master_style_guide_builder
python -m app.agents.station_07_character_architect
python -m app.agents.station_08_world_builder
python -m app.agents.station_11_runtime_planner
python -m app.agents.station_12_hook_cliffhanger_designer
python -m app.agents.station_13_multi_world_timeline_manager
python -m app.agents.station_14_simple_episode_blueprint
python -m app.agents.station_15_detailed_episode_outlining
python -m app.agents.station_16_canon_check
python -m app.agents.station_17_dialect_planning
python -m app.agents.station_18_evergreen_check
python -m app.agents.station_19_procedure_check
python -m app.agents.station_20_geography_transit
```

## 🔧 **Troubleshooting**

**Issue**: "No Station X data found"
**Solution**: Make sure you're using the correct session ID from the previous station

**Issue**: "Redis connection failed"
**Solution**: Start Redis server: `redis-server`

**Issue**: "OpenRouter API error"
**Solution**: Check your API key: `echo $OPENROUTER_API_KEY`

**Issue**: "No such module named 'app'"
**Solution**: Run from project root directory: `cd /path/to/Final_Script`

## 📁 **Output Structure**

Each station creates files in its respective folder:
```
output/
├── station_01/session_YYYYMMDD_HHMMSS_output.json
├── station_02/session_YYYYMMDD_HHMMSS_bible.json
├── station_03/session_YYYYMMDD_HHMMSS_style_guide.json
├── station_04/session_YYYYMMDD_HHMMSS_output.json
├── station_045/session_YYYYMMDD_HHMMSS_output.json
├── station_05/session_YYYYMMDD_HHMMSS_output.json
├── station_06/session_YYYYMMDD_HHMMSS_output.json
├── station_07/session_YYYYMMDD_HHMMSS_character_bible.json
├── station_08/session_YYYYMMDD_HHMMSS_world_bible.json
├── station_11/session_YYYYMMDD_HHMMSS_runtime_planning.json
├── station_12/session_YYYYMMDD_HHMMSS_hook_cliffhanger_design.json
├── station_13/session_YYYYMMDD_HHMMSS_output.json
├── station_14/session_YYYYMMDD_HHMMSS_output.json
├── station_15/session_YYYYMMDD_HHMMSS_output.json
├── station_16/session_YYYYMMDD_HHMMSS_output.json
├── station_17/session_YYYYMMDD_HHMMSS_output.json
├── station_18/session_YYYYMMDD_HHMMSS_output.json
├── station_19/session_YYYYMMDD_HHMMSS_output.json
└── station_20/session_YYYYMMDD_HHMMSS_output.json
```

## ⚡ **Quick Start**

1. **Start Redis**: `redis-server`
2. **Set API key**: `export OPENROUTER_API_KEY=your-key-here`
3. **Run Station 1**: `python -m app.agents.station_01_seed_processor`
4. **Copy session ID** from Station 1 output
5. **Run Station 2**: `python -m app.agents.station_02_project_dna_builder`
6. **Enter session ID** when prompted
7. **Continue with remaining stations** in order

---

**That's it! Each station runs independently and you can run them in sequence manually.**

