# Quick Start Guide - Station Creator Wizard

## For Your Customers

### What This Does
Your customers can now create custom stations for your audiobook production system **without any coding**. They just answer questions, and the AI creates everything for them.

### How to Use (3 Simple Steps)

#### 1. Run the Wizard
```bash
cd /path/to/script
python run_station_creator.py
```

#### 2. Answer Questions
The AI will ask 6 simple questions:
- What should the station be called?
- What should it do?
- What type of station is it?
- What inputs does it need?
- How complex should the AI be?
- What should it output?

After each answer, the AI shows what it generated and asks "Does this look good?"

**If it looks good:** Type `yes` and press Enter

**If you want changes:** Describe what to change in plain English
- "make it simpler"
- "add emotion detection"
- "use a faster AI model"
- etc.

#### 3. Test Your Station
After the wizard finishes:
```bash
python tools/test_station_XX.py
```
(Replace XX with your station number)

### Example Session

```
$ python run_station_creator.py

Ready to start? yes

Step 1: What would you like to name this station?
> Music Mood Generator

Station created:
  • Station 21: Music Mood Generator
  • File: station_21_music_mood_generator.py

Does this look good? yes

Step 2: What should this station do?
> Suggest background music based on scene emotions

AI generated description:
  "Analyzes scene emotional content and recommends
  appropriate background music selections to enhance
  the listening experience."

Does this look good? yes

[continues through all steps...]

✅ Complete! Files created:
   • app/agents/station_21_music_mood_generator.py
   • app/agents/configs/station_21.yml
   • tools/test_station_21.py

Test now: python tools/test_station_21.py
```

### What Gets Created

For each station, you get:
1. **Complete Python Code** (300-500 lines)
   - Ready to use immediately
   - Professional quality
   - Includes error handling

2. **Configuration File**
   - AI settings
   - Prompts
   - Parameters

3. **Test Script**
   - Easy testing
   - Example usage

### Common Use Cases

#### Create a Quality Checker
```
Name: Dialogue Quality Checker
Does: Check if dialogue sounds natural
Type: Analysis
Inputs: Station 15 (Episode Outlining)
Complexity: Simple
```

#### Create a Music Suggester
```
Name: Music Cue Generator
Does: Suggest background music for scenes
Type: Generation
Inputs: Stations 8, 14, 15
Complexity: Medium
```

#### Create a Content Enhancer
```
Name: Description Enhancer
Does: Make scene descriptions more vivid
Type: Enhancement
Inputs: Station 15
Complexity: Complex
```

### Tips for Success

✅ **Be Specific** - Clearly describe what you want
✅ **Review Carefully** - Check each step before approving
✅ **Request Changes** - If something isn't right, ask for changes
✅ **Test Immediately** - Run the test script right away
✅ **Iterate** - You can always edit the generated code later

### Getting Help

1. **Read the AI's output carefully** - It explains what it created
2. **Use the test script** - Shows if everything works
3. **Check the code comments** - Generated code has explanations
4. **Try it again** - You can create unlimited stations

### Important Notes

⚠️ **This is for testing only** - Generated stations are separate from the main system

⚠️ **Test before using** - Always test your stations first

⚠️ **You can edit** - All generated code can be customized

### Integration Later

When you're ready to add your station to the main pipeline:
1. Test it thoroughly
2. Review and customize the code
3. Follow integration instructions in main README
4. Contact support for help

---

**Ready?** Just run:
```bash
python run_station_creator.py
```

That's it! The AI handles everything else. 🎉
