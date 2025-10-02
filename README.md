# Audiobook Production System

A sophisticated multi-agent system for automated audiobook production using LangGraph Swarm technology. This system processes story concepts through multiple specialized stations to create comprehensive audiobook production plans.

## 🚀 Features

- **Multi-Station Processing**: 14 specialized stations for different aspects of audiobook production
- **Character Extraction**: Automatically extracts characters from story concepts
- **Project DNA Building**: Creates comprehensive project bibles and documentation
- **Age/Genre Optimization**: Optimizes content for target demographics
- **Reference Mining**: Generates reference materials and seed content
- **Narrator Strategy**: Develops narrator selection and voice strategies
- **Season Architecture**: Plans multi-season content structure
- **Master Style Guide**: Creates comprehensive style guidelines
- **Reality Check**: Comprehensive quality assurance and validation checkpoint
- **Character Architecture**: Complete 3-tier character development with audio identification
- **World Building**: 5-section world architecture with audio-focused design and sonic signatures
- **Hook & Cliffhanger Design**: Episode engagement strategy with 60-second hooks and cliffhangers
- **Multi-World Management**: Conditional station for multi-world/timeline narratives with audio differentiation
- **Episode Blueprints**: Simple, human-readable episode summaries ready for stakeholder approval

## 🏗️ Architecture

The system consists of multiple specialized agents (stations) that work together:

- **Station 1**: Seed Processor - Character extraction and scale analysis
- **Station 2**: Project DNA Builder - Creates project bibles and documentation
- **Station 3**: Age/Genre Optimizer - Optimizes for target demographics
- **Station 4**: Reference Miner - Generates reference materials
- **Station 4.5**: Narrator Strategy - Develops narrator selection strategies
- **Station 5**: Season Architecture - Plans multi-season content structure
- **Station 6**: Master Style Guide - Creates comprehensive style guidelines
- **Station 7**: Reality Check - Validates all outputs and ensures quality standards
- **Station 8**: Character Architecture - Creates 3-tier character system with voice signatures
- **Station 9**: World Building - Audio-focused world architecture with comprehensive sonic design
- **Station 12**: Hook & Cliffhanger Designer - Episode engagement strategy with opening hooks, act turns, and cliffhangers
- **Station 13**: Multi-World/Timeline Manager - Conditional station for multi-world scenarios with audio differentiation strategies  
- **Station 14**: Simple Episode Blueprint - Human-readable episode summaries ready for stakeholder approval

### New Station Details

**Station 12: Hook & Cliffhanger Designer**
- **Purpose**: Episode engagement strategy with hooks and cliffhangers
- **Input**: Season architecture (Station 5), Character bible (Station 8)
- **Output**: Hook/cliffhanger strategy per episode (TXT, JSON, PDF)
- **Key Features**:
  - 60-second opening hook design
  - Three act turn mapping
  - Cliffhanger type and intensity (1-10 scale)
  - Episode-to-episode bridges
  - Tension curve mapping
  - 10+ cliffhanger types catalog

**Station 13: Multi-World/Timeline Manager**
- **Purpose**: CONDITIONAL station for multi-world/timeline stories
- **Input**: World bible (Station 9), Season architecture (Station 5)
- **Output**: Multi-world management bible (TXT, JSON, PDF)
- **Key Features**:
  - Auto-detection of single vs multi-world scenarios
  - World/timeline inventory (if applicable)
  - Transition rules and audio strategies
  - Sonic differentiation per world
  - Timeline consistency rules
  - Listener orientation strategy
- **Note**: Gracefully skips if single-world story

**Station 14: Simple Episode Blueprint**
- **Purpose**: Final blueprint with simple summaries for human approval
- **Input**: All previous stations (5, 8, 9, 10, 11, 12, 13)
- **Output**: Episode blueprints ready for approval (TXT, JSON, PDF)
- **Key Features**:
  - 2-3 paragraph simple language summaries per episode
  - NO dialogue, just story beats
  - Character goals and obstacles
  - Story connections and significance
  - Production essentials
  - Season narrative overview
  - Approval checklist
- **HUMAN GATE**: Requires stakeholder approval before proceeding

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arjunthilak05/scrpt.git
   cd scrpt
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

4. **Configure OpenRouter API**:
   - Get an API key from [OpenRouter.ai](https://openrouter.ai)
   - Add it to your `.env` file:
     ```
     OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
     ```

5. **Optional: Set up Redis** (for enhanced functionality):
   ```bash
   # macOS
   brew install redis
   brew services start redis
   
   # Or using Docker
   docker run -d -p 6379:6379 redis:alpine
   ```

## 🎯 Usage

### Automated System (Recommended)
Run the complete automated pipeline:
```bash
python full_automation.py
```

### Testing
Test the automation system:
```bash
python test_automated_swarm.py
# or
python demo_automated_system.py
```

### Manual Testing
Test individual stations:
```bash
python test_stations.py
```

### Individual Stations
Run specific stations:
```bash
python station1_cli.py  # Station 1 only
python station2_cli.py  # Station 2 only
```

## 📊 Input Format

When prompted, enter your story concept. Examples:
- "Tom meets Julia through a wrong number text message and they form an unexpected connection"
- "A detective investigates mysterious disappearances in a small town"
- "Two rival chefs are forced to work together to save a restaurant"

## 📁 Project Structure

```
scrpt/
├── app/
│   ├── agents/           # Station agents
│   ├── config.py         # Configuration settings
│   ├── openrouter_agent.py
│   └── redis_client.py
├── outputs/              # Generated files (PDFs, JSON, TXT)
├── requirements.txt      # Python dependencies
├── full_automation.py    # Main automation script
├── resume_automation.py  # Resume automation
└── SETUP_INSTRUCTIONS.md # Detailed setup guide
```

## 🔧 Configuration

The system uses environment variables for configuration. Key settings:

- `OPENROUTER_API_KEY`: Required for AI processing
- `REDIS_URL`: Optional, for caching and state management
- `DATABASE_URL`: Optional, for persistent storage

## 📈 Output

The system generates comprehensive documentation including:
- Character profiles and relationships
- Project bibles and style guides
- Season architecture plans
- Narrator strategies
- Reference materials
- Production timelines
- Hook and cliffhanger strategies
- Multi-world management rules (if applicable)
- Episode blueprints ready for human approval

All outputs are saved in the `outputs/` directory with timestamps.

### Generated Files
Each station produces multiple output formats:
- `station12_hook_cliffhanger_[session].{txt,json,pdf}` - Episode engagement strategies
- `station13_multiworld_[session].{txt,json,pdf}` - World management rules (conditional)
- `station14_episode_blueprint_[session].{txt,json,pdf}` - Human approval documents

### Human Approval Gate
Station 14 produces the **Episode Blueprint** - a human-readable approval document. This is a mandatory review point where stakeholders must:

1. Review all episode summaries
2. Check story coherence and pacing
3. Verify character arcs
4. Approve production requirements
5. Sign off before proceeding to detailed scripting

**Review Files**:
- Primary: `station14_episode_blueprint_[session].pdf` (approval document)
- Reference: `station14_episode_blueprint_[session].txt` (readable format)
- Data: `station14_episode_blueprint_[session].json` (structured data)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) file
2. Review the troubleshooting section
3. Open an issue on GitHub

## 🔄 Automation Features

The system uses LangGraph Swarm technology for seamless execution:
- **Complete Pipeline**: Station 1 → 2 → 3 → 4 → 4.5 → 5 → 6 → 7 → 8 → 9 → 12 → 13 → 14
- **Error Handling**: Robust error recovery and retry mechanisms
- **State Management**: Persistent state across stations
- **Parallel Processing**: Optimized for performance
- **Conditional Stations**: Station 13 gracefully skips for single-world narratives
- **Human Gate**: Station 14 requires stakeholder approval before proceeding

---

Built with ❤️ using LangGraph, LangChain, and OpenRouter AI
