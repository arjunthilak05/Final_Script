# 32-Station Audiobook Production Pipeline

A comprehensive, multi-stage AI-powered system for end-to-end audiobook production. This system transforms story concepts through 32 specialized processing stations into production-ready audiobook scripts with complete quality assurance and voice direction.

## 🎬 Overview

**Complete Pipeline**: Story Concept → Production Scripts → Voice Direction → Quality Certification

- **32 Specialized Stations**: Full production pipeline from concept to final certification
- **100% AI-Driven**: All content generated via Claude 3.5 Sonnet (no hardcoded fallbacks)
- **Interactive Quality Assurance**: Human review points at Stations 31-32
- **Redis-Based State Management**: Seamless data flow across all stations
- **Production-Ready Output**: Scripts, analyses, and voice guidance

## 🎯 Station Overview (32 Total)

### **PHASE 1: Foundation & Strategy (Stations 1-4.5)**
1. **Seed Processor** - Story concept analysis and project scale evaluation
2. **Project DNA Builder** - Comprehensive project bible and metadata
3. **Age/Genre Optimizer** - Target demographic and genre positioning
4. **Reference Miner** - Reference materials and seed content discovery
4.5 **Narrator Strategy** - Narrator selection and voice strategy planning

### **PHASE 2: Architecture & Planning (Stations 5-15)**
5. **Season Architecture** - Multi-season content structure and pacing
6. **Master Style Guide** - Comprehensive brand voice and style standards
7. **Reality Check** - Quality assurance and internal consistency validation
8. **Character Architecture** - 3-tier character system with voice signatures
9. **World Building** - Audio-focused world design with sonic specifications
10. **Narrative Reveal Strategy** - Information reveal planning (45+ methods)
11. **Runtime Planning** - Episode duration analysis and production timeline
12. **Hook & Cliffhanger Designer** - Episode engagement and retention strategies
13. **Multi-World Manager** - Multi-world/timeline management (conditional)
14. **Episode Blueprint** - Simple episode summaries for stakeholder approval
15. **Detailed Episode Outlining** - Production-ready detailed episode outlines

### **PHASE 3: Script Refinement (Stations 16-27)**
16. **Canon Check** - Character and world consistency validation
17. **Dialect Planning** - Voice consistency and character speech patterns
18. **Evergreen Check** - Dated reference detection and content longevity
19. **Procedure Check** - Professional procedure accuracy and authenticity
20. **Geography & Transit** - Location consistency and travel time verification
21. **Narrative Polish** - Dialogue enhancement and pacing refinement
22. **Sensitivity Check** - Cultural sensitivity and inclusive language review
23. **Logic & Plot Coherence** - Plot hole detection and logical consistency
24. **Dialogue Authenticity** - Character voice consistency and speech patterns
25. **Audio Adaptation** - Format conversion to audio-friendly structure
26. **Final Script Lock** - Locked v1.0 production scripts with metadata
27. **Pre-Production Package** - Complete production readiness documentation

### **PHASE 4: Voice Production Prep (Stations 28-30)**
28. **Vocal Range Analysis** - Voice requirements and character casting specs
29. **Acoustic Design** - Sound environment and technical specifications
30. **Narrative Pacing** - Episode timing and audio narrative structure

### **PHASE 5: Quality Assurance & Certification (Stations 31-32)**
31. **Dialogue Naturalness Pass** - Interactive voice acting readiness assessment
   - Speakability Check (tongue twisters, breath points, rhythm)
   - Naturalness Scoring (vocabulary, structure, fillers, interruptions)
   - Identity Clarity Check (speaker recognition test)
   - Subtext Verification (emotional layers and character depth)

32. **Audio-Only Clarity Audit** - Interactive audio comprehension validation
   - Scene Setting Clarity (location/time establishment)
   - Action Comprehension (physical/emotional action tracking)
   - Transition Clarity (time/location/POV transitions)
   - Information Delivery (exposition quality and naturalness)

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Redis (for state management)
- OpenRouter API key (for Claude 3.5 Sonnet access)

### 1. Clone Repository
```bash
git clone https://github.com/arjunthilak05/Final_Script.git
cd Final_Script
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
Create `.env` file in project root:
```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
REDIS_URL=redis://localhost:6379
```

Get your OpenRouter API key from: https://openrouter.ai/keys

### 4. Start Redis (Required)
```bash
# macOS (with Homebrew)
brew install redis
brew services start redis

# macOS (verify it's running)
redis-cli ping  # Should return "PONG"

# Linux
sudo apt-get install redis-server
sudo systemctl start redis-server

# Docker
docker run -d -p 6379:6379 redis:alpine
```

Verify Redis is running:
```bash
redis-cli ping  # Should return "PONG"
```

## 🎯 Quick Start

### Running a Single Episode Through Stations 31-32
```bash
# Station 31: Dialogue Naturalness Pass
python3 -m app.agents.station_31_dialogue_naturalness_pass session_id

# Station 32: Audio-Only Clarity Audit
python3 -m app.agents.station_32_audio_clarity_audit session_id
```

Interactive prompts will guide you through:
1. Episode selection (1, 2, or 'all')
2. Review of quality assessment results
3. Approval to save analysis files

### Querying Results from Redis
```bash
python query_redis.py  # Interactive tool to retrieve station outputs
```

### Pushing Data to Redis
```bash
python push_to_redis.py  # Load station outputs to Redis
```

## 📁 Output Structure

Each phase generates organized output directories:

```
output/
├── station_01/              # Seed Processor outputs
├── station_02/              # Project DNA outputs
├── ...
├── station_26/              # Final Script Lock (locked v1.0 scripts)
│   ├── episode_01.fountain
│   ├── episode_01.json
│   └── episode_01.md
├── station_31/              # Dialogue Naturalness Analysis
│   ├── episode_01_dialogue_analysis.json
│   └── episode_02_dialogue_analysis.json
└── station_32/              # Audio Clarity Audit
    ├── episode_01_clarity_audit.json
    └── episode_02_clarity_audit.json
```

### Station 31 Output Example
```json
{
  "episode": 1,
  "speakability": {
    "breath_issues": 1,
    "rhythm_issues": 2
  },
  "naturalness_scores": {
    "Tom": 4,
    "Sarah": 4
  },
  "identity_clarity": 85,
  "subtext_analysis": {
    "excellent": 1,
    "weak": 1
  }
}
```

### Station 32 Output Example
```json
{
  "episode": 1,
  "scene_setting_clarity": 8,
  "action_comprehension": 7,
  "transition_clarity": 9,
  "information_delivery": 7
}
```

## 📊 Project Structure

```
Final_Script/
├── app/
│   ├── agents/                          # All 32 station modules
│   │   ├── station_01_seed_processor.py
│   │   ├── station_02_project_dna_builder.py
│   │   ├── ... (stations 3-30)
│   │   ├── station_31_dialogue_naturalness_pass.py
│   │   ├── station_32_audio_clarity_audit.py
│   │   └── configs/                     # YAML configs for stations
│   │       ├── station_31.yml
│   │       ├── station_32.yml
│   │       └── ... (other configs)
│   ├── config.py                        # Configuration management
│   ├── config_loader.py                 # YAML config loader
│   ├── openrouter_agent.py              # OpenRouter LLM integration
│   ├── redis_client.py                  # Redis state management
│   └── station_registry.py              # Station management
├── output/                              # Generated station outputs
│   ├── station_01/ ... station_32/      # Individual station folders
│   └── [episode outputs]
├── output2/                             # Legacy output structure
├── tools/                               # Utility tools
├── query_redis.py                       # Query station results
├── push_to_redis.py                     # Push to Redis
├── get_redis_data.py                    # Retrieve Redis data
├── requirements.txt                     # Python dependencies
├── setup.py                             # Package setup
├── REDIS_USAGE.md                       # Redis documentation
├── STATIONS.md                          # Detailed station descriptions
├── STATIONS_31_32_IMPLEMENTATION.md     # Stations 31-32 documentation
└── README.md                            # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here  # Required for Claude 3.5 Sonnet
REDIS_URL=redis://localhost:6379           # Optional (default shown)
```

### Station YAML Configurations
Stations 31-32 (and others) use YAML configuration files:

**Station 31** (`app/agents/configs/station_31.yml`)
- LLM prompts for 4 dialogue checks
- Response parsing configurations
- Temperature and token limits

**Station 32** (`app/agents/configs/station_32.yml`)
- LLM prompts for 4 clarity audits
- Audio-specific evaluation criteria
- Output formatting specifications

## 💡 Key Features

### 1. 100% AI-Driven Content Generation
- All 32 stations use Claude 3.5 Sonnet via OpenRouter
- No hardcoded fallback data or default values
- Dynamic, context-aware processing
- Consistent quality across all stations

### 2. Redis-Based State Management
- Seamless data flow across all 32 stations
- Real-time progress tracking
- Session-based output organization
- Easy data querying and retrieval

### 3. Interactive Quality Assurance (Stations 31-32)
- Human review checkpoints
- 4 dialogue checks in Station 31
- 4 clarity audits in Station 32
- Approval workflow for finalized scripts

### 4. Production-Ready Scripts (Station 26)
- Locked v1.0 scripts with metadata
- Multiple formats: .fountain, .json, .md
- Complete episode coverage
- Audio-optimized formatting

### 5. Comprehensive Output Management
- Episode-level organization
- Multiple output formats (JSON, Markdown, Fountain)
- Detailed analysis files
- Quality metrics and scores

### 6. Modular Station Architecture
- Each station is independent and focused
- Clear input/output contracts
- Easy to extend or modify
- Configurable via YAML

## 🎯 Data Flow

```
Story Concept
    ↓
Station 1-4.5 (Foundation & Strategy)
    ↓
Station 5-15 (Architecture & Planning)
    ↓
Station 16-27 (Script Refinement)
    ↓
Station 28-30 (Voice Production Prep)
    ↓
Station 31 (Dialogue Naturalness Pass) ← Interactive Review
    ↓
Station 32 (Audio-Only Clarity Audit) ← Interactive Review
    ↓
Certified Production-Ready Scripts
```

## 🎬 Stations 31-32: Quality Assurance Pipeline

### Station 31: Dialogue Naturalness Pass
Evaluates dialogue for voice acting readiness through 4 interactive checks:

**1. Speakability Check**
- Detects tongue twisters and difficult consonant combinations
- Identifies breath point issues (sentences that are too long)
- Flags rhythm problems and unnatural word order
- Provides specific line-by-line feedback

**2. Naturalness Scoring (0-5 scale)**
- Vocabulary appropriateness for character age and background
- Sentence structure variety and complexity
- Natural filler words and speech patterns
- Realistic interruptions and overlaps

**3. Identity Clarity Check (0-10 scale)**
- Tests speaker recognition without character names
- Identifies generic lines that could fit any character
- Measures voice distinction effectiveness
- Flags lines requiring stronger vocal markers

**4. Subtext Verification (0-10 scale)**
- Analyzes implied meaning vs. stated meaning
- Identifies emotional layers and character depth
- Detects "tell-don't-show" issues
- Provides suggestions for subtext enhancement

### Station 32: Audio-Only Clarity Audit
Validates scripts for audio-only listening clarity through 4 interactive audits:

**1. Scene Setting Clarity**
- Verifies location/time establishment (within 10 seconds)
- Tracks character presence and entrances
- Analyzes acoustic signature specifications
- Confirms listener orientation

**2. Action Comprehension**
- Tests physical action trackability from audio alone
- Validates character action clarity
- Evaluates emotional action sequences
- Flags unclear or ambiguous actions

**3. Transition Clarity**
- Verifies time transition effectiveness
- Tests location transition smoothness
- Validates POV shift clarity
- Checks acoustic shift appropriateness

**4. Information Delivery**
- Audits exposition integration (natural vs. dumped)
- Detects information overload moments
- Validates audio-friendly language
- Identifies clarity issues

## 📊 Performance Metrics

All stations generate quality metrics:
- **Station 31**: Speakability scores, naturalness ratings (0-5), identity clarity %
- **Station 32**: Clarity scores (0-10) for all 4 audits
- **Output**: JSON files with detailed analysis and recommendations

## 📄 File Formats

### JSON Output
```bash
output/station_31/episode_01_dialogue_analysis.json
output/station_32/episode_01_clarity_audit.json
```

### Script Formats (Station 26)
```bash
output/station_26/episode_01.fountain    # Industry-standard script format
output/station_26/episode_01.json        # Structured script data
output/station_26/episode_01.md          # Markdown script format
```

## 🚨 Important Notes

- **Redis Required**: System requires Redis for state management and data flow
- **OpenRouter API**: Valid API key required for Claude 3.5 Sonnet access
- **Session IDs**: Unique timestamp-based IDs for tracking and organization
- **100% AI-Generated**: All content is generated by Claude 3.5 Sonnet
- **Interactive Review**: Stations 31-32 require human approval before saving
- **Production Ready**: Complete system tested and verified with Episodes 1-2

## 🚀 Example Workflow

### Complete Pipeline (Concept to Certified Scripts)
```bash
# All 32 stations process automatically via scheduled jobs
# Outputs flow through Redis to each subsequent station
# Final output: Production-ready scripts with voice direction
```

### Testing Stations 31-32 with Existing Scripts
```bash
# Run Dialogue Naturalness Pass
python3 -m app.agents.station_31_dialogue_naturalness_pass session_20251023_112749

# When prompted, select:
# - Episode: 1 (or 'all' for multiple)
# - Choice: Press Enter to approve and save

# Run Audio-Only Clarity Audit
python3 -m app.agents.station_32_audio_clarity_audit session_20251023_112749

# Follow same approval workflow
```

### Viewing Results
```bash
# Query Redis for station outputs
python query_redis.py

# Or examine JSON files directly
cat output/station_31/episode_01_dialogue_analysis.json
cat output/station_32/episode_01_clarity_audit.json
```

## 📚 Additional Documentation

- **[REDIS_USAGE.md](REDIS_USAGE.md)** - Detailed Redis integration guide
- **[STATIONS.md](STATIONS.md)** - Complete station descriptions (1-32)
- **[STATIONS_31_32_IMPLEMENTATION.md](STATIONS_31_32_IMPLEMENTATION.md)** - Detailed Stations 31-32 specs

## 🎓 System Requirements

- **Python**: 3.9 or higher
- **Redis**: Latest stable version
- **API Access**: OpenRouter account with Claude 3.5 Sonnet
- **Disk Space**: ~500MB for sample outputs
- **RAM**: 4GB recommended
- **Network**: Internet access for OpenRouter API calls

## ✅ Testing Verification

The system has been tested and verified with:
- ✅ Station 31 (Dialogue Naturalness Pass): Episodes 1-2 fully analyzed
- ✅ Station 32 (Audio-Only Clarity Audit): Episodes 1-2 fully audited
- ✅ All quality metrics generated and validated
- ✅ JSON output files created successfully
- ✅ Redis data persistence confirmed

## 🤝 Contributing

This is a production system. For modifications:
1. Test thoroughly with sample episodes
2. Maintain the station pipeline integrity
3. Update YAML configs for station-specific changes
4. Document all modifications
5. Preserve Redis data flow architecture

## 📄 License

Proprietary - All Rights Reserved

## 🆘 Troubleshooting

### Redis Connection Failed
```bash
# Check if Redis is running
redis-cli ping  # Should return "PONG"

# Verify Redis configuration
echo "PING" | redis-cli
```

### API Key Invalid
```bash
# Check .env file
cat .env

# Verify API key format: sk-or-v1-...
# Get new key from: https://openrouter.ai/keys
```

### Station Errors
```bash
# Check console output for error messages
# Review Redis data for missing dependencies
# Verify previous stations completed successfully
```

### Output Files Not Generated
```bash
# Check permissions on output/ directory
ls -la output/station_31/
ls -la output/station_32/

# Verify episodes loaded correctly
python query_redis.py
```

## 📞 Support

For issues or questions:
1. Review relevant documentation files
2. Check Redis connectivity: `redis-cli ping`
3. Verify API key validity and credits
4. Examine detailed error logs in console output
5. Review JSON output files for data structure

---

## 📊 System Status

| Component | Status | Version |
|-----------|--------|---------|
| Stations (1-32) | ✅ Complete | 32-Station |
| Claude 3.5 Sonnet | ✅ Integrated | Via OpenRouter |
| Redis Integration | ✅ Active | v6.0+ |
| Station 31 | ✅ Production Ready | v1.0 |
| Station 32 | ✅ Production Ready | v1.0 |
| Quality Metrics | ✅ Validated | Full Suite |

---

**Built with**: Python, OpenRouter AI (Claude 3.5 Sonnet), Redis, LangChain
**Architecture**: 32-Station multi-agent pipeline with Redis state management
**Version**: 3.2 (Complete 32-Station Pipeline with Quality Assurance)
**Last Updated**: October 27, 2025
**Status**: ✅ Production Ready
