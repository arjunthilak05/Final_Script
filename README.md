# Audiobook Production System

A sophisticated multi-agent system for automated audiobook production using LangGraph Swarm technology. This system processes story concepts through multiple specialized stations to create comprehensive audiobook production plans.

## 🚀 Features

- **Multi-Station Processing**: 6 specialized stations for different aspects of audiobook production
- **Character Extraction**: Automatically extracts characters from story concepts
- **Project DNA Building**: Creates comprehensive project bibles and documentation
- **Age/Genre Optimization**: Optimizes content for target demographics
- **Reference Mining**: Generates reference materials and seed content
- **Narrator Strategy**: Develops narrator selection and voice strategies
- **Season Architecture**: Plans multi-season content structure
- **Master Style Guide**: Creates comprehensive style guidelines

## 🏗️ Architecture

The system consists of multiple specialized agents (stations) that work together:

- **Station 1**: Seed Processor - Character extraction and scale analysis
- **Station 2**: Project DNA Builder - Creates project bibles and documentation
- **Station 3**: Age/Genre Optimizer - Optimizes for target demographics
- **Station 4**: Reference Miner - Generates reference materials
- **Station 4.5**: Narrator Strategy - Develops narrator selection strategies
- **Station 5**: Season Architecture - Plans multi-season content structure
- **Station 6**: Master Style Guide - Creates comprehensive style guidelines

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

All outputs are saved in the `outputs/` directory with timestamps.

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
- **Station 1 → Station 2**: Automatic progression without manual intervention
- **Error Handling**: Robust error recovery and retry mechanisms
- **State Management**: Persistent state across stations
- **Parallel Processing**: Optimized for performance

---

Built with ❤️ using LangGraph, LangChain, and OpenRouter AI
