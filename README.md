# Audiobook Production System

A sophisticated multi-agent AI system for automated audiobook production. This system processes story concepts through 20 specialized stations to create comprehensive audiobook production plans with organized output management.

## 🚀 Features

- **20 Specialized Stations**: Complete end-to-end audiobook production pipeline
- **Dynamic LLM Processing**: All stations use real-time AI processing (no fallbacks)
- **Organized Output**: Each run creates a dedicated folder with all outputs
- **Resume Capability**: Built-in checkpoint system for interrupted runs
- **Custom Station Creation**: Wizard tool for creating new stations on-demand
- **Comprehensive Validation**: Multiple quality check stations (16-20)

## 📋 System Stations

### Core Production Stations (1-15)
1. **Seed Processor** - Story concept analysis and scale evaluation
2. **Project DNA Builder** - Comprehensive project bible creation
3. **Age/Genre Optimizer** - Target demographic optimization
4. **Reference Miner** - Reference materials and seed content generation
5. **Narrator Strategy** (4.5) - Narrator selection and voice strategy
6. **Season Architecture** - Multi-season content structure planning
7. **Master Style Guide** - Comprehensive style guidelines
8. **Reality Check** - Quality assurance and validation checkpoint
9. **Character Architecture** - 3-tier character system with voice signatures
10. **World Building** - Audio-focused world architecture with sonic design
11. **Narrative Reveal Strategy** - Information reveal planning with 45+ methods
12. **Runtime Planning** - Production timeline and resource planning
13. **Hook & Cliffhanger Designer** - Episode engagement strategies
14. **Multi-World Manager** - Multi-world/timeline management (conditional)
15. **Simple Episode Blueprint** - Simple episode summaries for stakeholder approval
16. **Detailed Episode Outlining** - Production-ready detailed outlines

### Quality Check Stations (16-20)
16. **Canon Check** - Character and world consistency validation
17. **Dialect Planning** - Voice consistency and character speech patterns
18. **Evergreen Check** - Dated reference detection and longevity analysis
19. **Procedure Check** - Professional procedure accuracy validation
20. **Geography & Transit** - Location consistency and travel time validation

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd script
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
Create `.env` file:
```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
REDIS_URL=redis://localhost:6379
```

### 4. Start Redis (Required)
```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

## 🎯 Usage

### Full Automation (All 20 Stations)
```bash
python full_automation.py
```

Follow prompts to:
1. Enter story concept
2. Review scale options (auto-selected in auto-approve mode)
3. System runs through all 20 stations automatically

### Resume Interrupted Run
```bash
python full_automation.py --resume <session_id>
# Or use auto-resume to pick latest checkpoint
python full_automation.py --resume auto
```

### Create Custom Stations
```bash
python tools/station_creator_wizard.py
```

Interactive wizard creates new stations with:
- Custom prompts and logic
- Proper integration with existing stations
- Automatic file generation

## 📁 Output Structure

Each automation run creates an organized session folder:

```
outputs/
└── auto_20251015_123456/
    ├── station01_seed_processor_auto_20251015_123456.txt
    ├── station02_project_dna_auto_20251015_123456.txt
    ├── station03_age_genre_optimizer_auto_20251015_123456.txt
    ├── station04_reference_miner_auto_20251015_123456.txt
    ├── station45_narrator_strategy_auto_20251015_123456.txt
    ├── station05_season_architecture_auto_20251015_123456.txt
    ├── station05_season_data_auto_20251015_123456.json
    ├── station06_master_style_guide_auto_20251015_123456.txt
    ├── station06_master_style_guide_auto_20251015_123456.json
    ├── station07_reality_check_auto_20251015_123456.txt
    ├── station07_reality_check_auto_20251015_123456.json
    ├── station08_character_bible_auto_20251015_123456.txt
    ├── station08_character_bible_auto_20251015_123456.json
    ├── station09_world_bible_auto_20251015_123456.txt
    ├── station09_world_bible_auto_20251015_123456.json
    ├── station10_reveal_matrix_auto_20251015_123456.txt
    ├── station10_reveal_matrix_auto_20251015_123456.json
    ├── station11_runtime_planning_auto_20251015_123456.txt
    ├── station11_runtime_planning_auto_20251015_123456.json
    ├── station12_hook_cliffhanger_auto_20251015_123456.txt
    ├── station12_hook_cliffhanger_auto_20251015_123456.json
    ├── station13_multiworld_timeline_auto_20251015_123456.txt
    ├── station13_multiworld_timeline_auto_20251015_123456.json
    ├── station14_episode_blueprint_auto_20251015_123456.txt
    ├── station14_episode_blueprint_auto_20251015_123456.json
    ├── station15_detailed_outlines_auto_20251015_123456.txt
    ├── station15_detailed_outlines_auto_20251015_123456.json
    ├── station16_canon_check_auto_20251015_123456.txt
    ├── station16_canon_check_auto_20251015_123456.json
    ├── station17_dialect_planning_auto_20251015_123456.txt
    ├── station17_dialect_planning_auto_20251015_123456.json
    ├── station18_evergreen_check_auto_20251015_123456.txt
    ├── station18_evergreen_check_auto_20251015_123456.json
    ├── station19_procedure_check_auto_20251015_123456.txt
    ├── station19_procedure_check_auto_20251015_123456.json
    ├── station20_geography_check_auto_20251015_123456.txt
    ├── station20_geography_check_auto_20251015_123456.json
    ├── checkpoint_auto_20251015_123456.json
    └── automation_summary_auto_20251015_123456.json
```

## 📊 Project Structure

```
script/
├── app/
│   ├── agents/              # All 20 station modules
│   │   ├── station_01_seed_processor.py
│   │   ├── station_02_project_dna_builder.py
│   │   ├── ...
│   │   └── station_20_geography_transit.py
│   ├── config.py            # Configuration management
│   ├── config_loader.py     # YAML config loader
│   ├── openrouter_agent.py  # OpenRouter LLM integration
│   ├── redis_client.py      # Redis state management
│   ├── state_manager.py     # Automation state tracking
│   ├── output_manager.py    # Output folder organization
│   └── station_registry.py  # Station management
├── tools/
│   ├── station_creator_wizard.py  # Custom station creation
│   ├── station_generator.py       # Station code generator
│   └── station_templates/         # Station templates
├── station_configs/         # YAML configuration files
│   ├── station_16_canon_check.yml
│   ├── station_17_dialect_planning.yml
│   ├── station_18_evergreen_check.yml
│   ├── station_19_procedure_check.yml
│   └── station_20_geography_transit.yml
├── outputs/                 # Generated session folders
├── full_automation.py       # Main automation script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here  # Required
REDIS_URL=redis://localhost:6379           # Optional (default shown)
```

### Station Configurations
Stations 16-20 use YAML configuration files in `station_configs/`:
- Define prompts and validation criteria
- Configure output formats
- Set station-specific parameters

## 💡 Key Features

### 1. Organized Output Management
- Each run creates a unique session folder
- All station outputs (.txt, .json) in one place
- Easy archival and sharing
- Clean outputs directory

### 2. Dynamic LLM Processing
- All stations use real-time AI calls
- No hardcoded fallback data
- Intelligent parsing and validation
- Robust error handling

### 3. Resume Functionality
- Automatic checkpoint saving after each station
- Resume from any point in the pipeline
- Preserves all state and outputs
- Support for both new and legacy checkpoint locations

### 4. Custom Station Creation
- Interactive wizard for new stations
- Automatic code generation
- Integration with existing pipeline
- Template-based creation

### 5. Comprehensive Validation
- 5 quality check stations (16-20)
- Character consistency tracking
- Voice and dialect validation
- Evergreen content checking
- Professional procedure accuracy
- Geographic consistency

## 🎓 Example Story Concepts

```
"A detective discovers a series of impossible murders that defy the laws of physics"

"Two rival food truck owners fall in love while competing for the same street corner"

"A young musician can hear the memories attached to old songs and uses this gift to solve cold cases"

"In a world where dreams are recorded and sold, a dream thief steals the wrong memory"
```

## 🔄 Workflow

1. **Input Story Concept** → System analyzes and recommends scale
2. **Stations 1-4** → Foundation (seed, DNA, optimization, references)
3. **Station 4.5** → Narrator strategy
4. **Stations 5-9** → Core architecture (season, style, validation, characters, world)
5. **Stations 10-15** → Episode development (reveals, runtime, hooks, blueprints, outlines)
6. **Stations 16-20** → Quality validation (canon, dialect, evergreen, procedures, geography)
7. **Output** → Complete production package in organized folder

## 📈 Output Files

### Text Files (.txt)
- Human-readable formatted documents
- Comprehensive station reports
- Easy review and sharing

### JSON Files (.json)
- Structured data for programmatic access
- Complete station outputs
- Integration-ready format

### Checkpoint Files
- Automatic state saving
- Resume capability
- Progress tracking

### Summary Files
- Automation completion report
- All station statistics
- Generated file listings

## 🚨 Important Notes

- **Redis Required**: System requires Redis for state management
- **OpenRouter API**: Valid API key required for LLM processing
- **Session IDs**: Unique timestamp-based IDs for each run
- **No Fallbacks**: All data dynamically generated by AI
- **Organized Outputs**: One folder per run for easy management

## 🤝 Contributing

This is a production system. For modifications:
1. Test thoroughly with sample concepts
2. Maintain the station pipeline integrity
3. Update documentation for new features
4. Preserve organized output structure

## 📄 License

Proprietary - All Rights Reserved

## 🆘 Support

For issues:
1. Check Redis is running: `redis-cli ping`
2. Verify API key is valid
3. Review error logs in console
4. Check checkpoint files for resume

---

**Built with**: Python, OpenRouter AI, Redis, LangChain
**Architecture**: Multi-agent pipeline with organized output management
**Version**: 2.0 (20 Stations + Organized Outputs)
