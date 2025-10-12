# Station Creator Wizard 🎯

**AI-Powered Tool for Creating Custom Audiobook Production Stations**

This tool allows your customers to create new stations for the audiobook production system without writing any code. The AI wizard guides them through an interactive process with continuous approval loops.

## Overview

The Station Creator Wizard is a **standalone testing tool** that generates production-ready station code based on simple questions and answers. After every step, the AI shows what it generated and waits for customer approval before proceeding.

## Key Features

✅ **No Coding Required** - Answer questions in plain English
✅ **AI-Powered Generation** - Automatically creates complete station code
✅ **Continuous Approval Loops** - Review and approve each step
✅ **Adaptive Changes** - Request modifications anytime
✅ **Production-Ready Code** - Follows existing station patterns
✅ **Standalone Testing** - Separate from main automation

## Quick Start

### Running the Wizard

```bash
# From the script directory
python run_station_creator.py
```

That's it! The wizard will guide you through 8 steps to create your custom station.

## The 8-Step Process

### Step 1: Station Basics
- Name your station
- Assign station number
- Create file names

**Example:**
```
Q: What would you like to name this station?
A: Music Cue Generator

✨ STATION CREATED:
   Station Number: 21
   Station Name: Station 21: Music Cue Generator
   File Name: station_21_music_cue_generator.py

Does this look good? (yes/change)
```

### Step 2: Station Purpose
- Describe what the station should do
- AI generates professional description
- Review and approve or request changes

**Example:**
```
Q: What should this station do?
A: Analyze emotional beats and suggest background music

✨ AI GENERATES:
   "Analyzes the emotional tone and pacing of each scene
   to recommend appropriate background music cues that
   enhance the audio drama experience."

Does this look good? (yes/change)
```

### Step 3: Station Type
Choose from 4 types:
1. **Analysis Station** - Examines data, provides insights
2. **Generation Station** - Creates new content
3. **Enhancement Station** - Improves existing content
4. **Validation Station** - Checks correctness

### Step 4: Input Configuration
- Select which previous stations provide data
- Wizard shows all 20 existing stations
- Choose inputs or select 'none'

**Example:**
```
Select inputs: 8, 14, 15

✨ INPUT CONFIGURATION:
   ✓ Station 8: Character Architecture
   ✓ Station 14: Episode Blueprint
   ✓ Station 15: Detailed Episode Outlining

Does this look good? (yes/change/add more/remove)
```

### Step 5: AI Processing Configuration
Choose complexity level:
1. **Simple** - Fast model, basic analysis
2. **Medium** - Balanced model, detailed work
3. **Complex** - Powerful model, sophisticated analysis

AI generates the prompt template automatically.

### Step 6: Output Format
- AI suggests structured output format
- JSON format with example data
- Review and request modifications

### Step 7: Code Generation
- AI generates complete Python code
- Shows preview with first 50 lines
- Options: accept, view full code, or request changes

### Step 8: File Creation
- Writes files to disk
- Creates test script
- Shows next steps

## What Gets Generated

For each station, the wizard creates:

1. **Station Python Code** (`app/agents/station_XX_name.py`)
   - Complete implementation
   - Retry logic with exponential backoff
   - Redis state management
   - Error handling and logging
   - Input validation
   - Output formatting
   - 300-500 lines of production code

2. **Configuration File** (`app/agents/configs/station_XX.yml`)
   - AI model settings
   - Prompt templates
   - Processing parameters
   - Dependencies list

3. **Test Script** (`tools/test_station_XX.py`)
   - Standalone test file
   - Example usage
   - Easy to run and verify

## Example: Creating an Emotion Analyzer

```bash
$ python run_station_creator.py

🎯 STATION CREATOR WIZARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to start? yes

🔷 STEP 1: STATION BASICS

Q: What would you like to name this station?
> Emotion Analyzer

✨ STATION CREATED:
   Station Number: 21
   File Name: station_21_emotion_analyzer.py

Does this look good? yes

🔷 STEP 2: STATION PURPOSE

Q: What should this station do?
> Analyze the emotional tone of each scene and suggest voice actor direction

🤖 Generating professional description...

✨ STATION PURPOSE:
   Analyzes the emotional tone and intensity of each scene,
   identifying key emotional beats, character feelings, and mood shifts.
   Provides voice actor direction suggestions to enhance audio production quality.

Does this look good? yes

[... continues through all 8 steps ...]

🎉 STATION CREATION COMPLETE!

Files Created:
   ✓ app/agents/station_21_emotion_analyzer.py
   ✓ app/agents/configs/station_21.yml
   ✓ tools/test_station_21.py

Next Steps:
   1. Test: python tools/test_station_21.py
   2. Review code
   3. Customize if needed
   4. Integrate when ready
```

## Testing Your Station

After creation, test your station:

```bash
# Test the station
python tools/test_station_XX.py

# Example output:
🧪 Testing Station 21: Emotion Analyzer
════════════════════════════════════════

📝 Session ID: test_station_21_001
⚙️  Processing...

✅ Station completed successfully!
📤 Output: {...}
```

## Making Changes

### Option 1: Request Changes During Creation
At any approval step, describe what to change:

```
Does this look good? change the output to include intensity scores

🔄 Regenerating with your changes...
```

### Option 2: Edit Generated Code
All generated code is fully editable:

```bash
# Edit the Python code
vim app/agents/station_21_emotion_analyzer.py

# Edit the configuration
vim app/agents/configs/station_21.yml
```

## Advanced Features

### Continuous Approval Loop Pattern

After **every** generation step:
```
AI: "I've created [X]. Here's what it looks like:"
AI: [Shows the output]
AI: "Does this look good? (yes/describe changes)"

Customer options:
- "yes" / "looks good" → Continue
- "change X to Y" → Regenerate
- "make it simpler" → Adjust
- "add more detail" → Enhance
```

### Natural Language Changes

The AI understands requests like:
- "make it simpler"
- "add more details about emotions"
- "change the model to something faster"
- "remove the sarcasm detection"
- "use a different output format"

### Smart Code Generation

Generated code includes:
- Proper error handling
- Retry logic (5 attempts)
- Redis integration
- Logging throughout
- Type hints
- Docstrings
- Input validation
- Output structuring

## File Structure

```
script/
├── run_station_creator.py          # Main runner script
├── tools/
│   ├── station_creator_wizard.py   # Interactive wizard
│   ├── station_generator.py        # Code generation engine
│   ├── station_templates/          # Template library
│   │   ├── analysis_template.py
│   │   ├── generation_template.py
│   │   ├── enhancement_template.py
│   │   └── validation_template.py
│   └── test_station_XX.py          # Generated test files
└── app/
    └── agents/
        ├── station_XX_name.py       # Generated stations
        └── configs/
            └── station_XX.yml       # Generated configs
```

## Integration with Main System

**Important:** This is currently a **standalone testing tool**. Generated stations are not automatically added to the main automation pipeline.

### When Ready to Integrate:

1. **Test thoroughly** using the test script
2. **Review and customize** the generated code
3. **Add to pipeline** by editing `full_automation.py`:

```python
# In full_automation.py
from app.agents.station_21_emotion_analyzer import Station21EmotionAnalyzer

# Add to the pipeline
state = await self._run_station_21(state)
```

4. **Create pipeline method**:

```python
async def _run_station_21(self, state):
    """Run Station 21: Emotion Analyzer"""
    station = Station21EmotionAnalyzer()
    await station.initialize()
    result = await station.process(state.session_id)
    state.station_outputs['station_21'] = result
    return state
```

## Troubleshooting

### Common Issues

**Problem:** Wizard fails to start
```bash
# Solution: Check dependencies
pip install -r requirements.txt
```

**Problem:** AI generation fails
```bash
# Solution: Check OpenRouter API key in .env
echo $OPENROUTER_API_KEY
```

**Problem:** Test script fails
```bash
# Solution: Check Redis is running
redis-cli ping
```

### Getting Help

1. Check the generated code comments
2. Review existing stations (1-20) for examples
3. Test incrementally
4. Review error messages in logs

## Best Practices

### For Station Creation:

1. ✅ **Be Clear** - Describe purpose clearly
2. ✅ **Review Carefully** - Check each step before approving
3. ✅ **Test Early** - Run tests immediately after creation
4. ✅ **Iterate** - Request changes if something isn't right
5. ✅ **Document** - Add comments for custom logic

### For Station Types:

- **Analysis** → Use when examining existing data
- **Generation** → Use when creating new content
- **Enhancement** → Use when improving existing content
- **Validation** → Use when checking correctness

### For AI Complexity:

- **Simple** → Quick checks, basic classifications
- **Medium** → Most content generation tasks
- **Complex** → Creative work, sophisticated analysis

## Examples

### Example 1: Music Cue Generator
```
Type: Generation
Purpose: Suggest background music for scenes
Inputs: Station 8, 14, 15
Complexity: Medium
Output: Music cues with mood, tempo, instruments
```

### Example 2: Dialogue Quality Checker
```
Type: Analysis
Purpose: Check dialogue for naturalness
Inputs: Station 15
Complexity: Simple
Output: Quality scores and improvement suggestions
```

### Example 3: Character Voice Enhancer
```
Type: Enhancement
Purpose: Improve character dialogue distinctiveness
Inputs: Station 8, 15
Complexity: Complex
Output: Enhanced dialogue with character voice notes
```

## FAQ

**Q: Can I create multiple stations at once?**
A: Yes! Run the wizard multiple times. After completion, it asks if you want to create another.

**Q: Can I modify generated code?**
A: Absolutely! All generated code is fully editable.

**Q: What if I make a mistake?**
A: Request changes at any step, or edit the code after generation.

**Q: Do I need to know Python?**
A: No! The wizard handles all coding. However, Python knowledge helps for customization.

**Q: How do I integrate into the main system?**
A: Test thoroughly first, then add to `full_automation.py` following existing patterns.

**Q: Can I use custom AI models?**
A: Yes! Edit the YAML config to use different models.

**Q: What happens to old stations?**
A: Nothing! New stations are added independently.

## Support

For issues or questions:
1. Check this README
2. Review generated code comments
3. Test with the provided test scripts
4. Check logs for error details

## Version

**Current Version:** 1.0.0
**Status:** Standalone Testing Tool
**Created:** 2025
**Last Updated:** 2025-10-12

---

**Ready to create your first custom station?**

```bash
python run_station_creator.py
```

Happy station building! 🚀
