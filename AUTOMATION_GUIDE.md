# 🚀 FULL AUTOMATION GUIDE

## ✅ **WORKING AUTOMATION SCRIPT**

The `full_automation.py` script is now **fully functional** and will:

1. **Run Station 1 automatically** with a default story concept (no user input required)
2. **Handle all station dependencies** correctly
3. **Save checkpoints** after each station for resume capability
4. **Provide progress tracking** and error recovery
5. **Create organized output** directories

### **Key Features:**

✅ **Fully Automated** - No user interaction required  
✅ **Dependency Management** - Stations run in correct order  
✅ **Error Recovery** - Checkpoint saving and resume capability  
✅ **Progress Tracking** - Real-time updates and success rates  
✅ **Session Management** - Unique IDs and organized outputs  

### **Default Story Concept:**

The automation uses this default story for Station 1:
> "A detective investigates mysterious disappearances in a small coastal town where the locals seem to know more than they're telling."

This ensures consistent, automated operation without requiring user input.

## Prerequisites

1. **Redis Server Running**
   ```bash
   redis-cli ping  # Should return PONG
   ```

2. **Environment Variables Set**
   ```bash
   export OPENROUTER_API_KEY=sk-or-v1-your-key-here
   export REDIS_URL=redis://localhost:6379
   ```

3. **Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🆕 Run All Stations (New Session)

```bash
python full_automation.py
```

**What happens:**
1. Creates new session ID (auto_YYYYMMDD_HHMMSS)
2. Runs all 20 stations in dependency order
3. Saves checkpoint after each station
4. Creates organized output folder
5. Generates final summary

### 🔄 Resume Interrupted Session

```bash
# Resume specific session
python full_automation.py --resume auto_20250116_143022

# Auto-resume latest session
python full_automation.py --resume auto
```

**What happens:**
1. Loads checkpoint data
2. Skips already completed stations
3. Continues from where it left off
4. Updates progress tracking

## Station Execution Order

The script automatically determines the correct order based on dependencies:

1. **Station 1**: Seed Processor (no dependencies)
2. **Station 2**: Project DNA Builder (depends on 1)
3. **Station 3**: Age/Genre Optimizer (depends on 1, 2)
4. **Station 4**: Reference Mining (depends on 1, 2, 3)
5. **Station 4.5**: Narrator Strategy Designer (depends on 1, 2, 3, 4)
6. **Station 5**: Season Architect (depends on 1, 2, 3, 4, 4.5)
7. **Station 6**: Master Style Guide Builder (depends on 1, 2, 3, 4, 4.5, 5)
8. **Station 7**: Character Architect (depends on 1, 2, 3, 4, 4.5, 5, 6)
9. **Station 8**: World Builder (depends on 1, 2, 3, 4, 4.5, 5, 6, 7)
10. **Station 11**: Runtime Planner (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8)
11. **Station 12**: Hook & Cliffhanger Designer (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11)
12. **Station 13**: Multi-World Timeline Manager (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12)
13. **Station 14**: Simple Episode Blueprint (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12, 13)
14. **Station 15**: Detailed Episode Outlining (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12, 13, 14)
15. **Station 16**: Canon Check (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12, 13, 14, 15)
16. **Station 17**: Dialect Planning (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16)
17. **Station 18**: Evergreen Check (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17)
18. **Station 19**: Procedure Check (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18)
19. **Station 20**: Geography & Transit (depends on 1, 2, 3, 4, 4.5, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19)

## Output Structure

Each automation run creates an organized session folder:

```
output/
└── auto_20250116_143022/
    ├── checkpoint_auto_20250116_143022.json
    ├── automation_summary_auto_20250116_143022.json
    └── automation.log
```

**Note**: Individual station outputs are saved in their respective station folders (e.g., `output/station_01/`, `output/station_02/`, etc.)

## Features

### ✅ Automatic Dependency Management
- Stations run in correct order based on dependencies
- No manual intervention required

### ✅ Progress Tracking
- Real-time progress updates
- Success/failure tracking per station
- Overall success rate calculation

### ✅ Error Recovery
- Checkpoint saving after each station
- Resume capability from any point
- Failed stations don't stop the pipeline

### ✅ Session Management
- Unique session IDs for each run
- Organized output directories
- Comprehensive logging

### ✅ Resume Capability
- Resume from specific session ID
- Auto-resume latest session
- Skip already completed stations

## Example Session

```bash
$ python full_automation.py

================================================================================
🚀 AUDIOBOOK PRODUCTION SYSTEM - FULL AUTOMATION
================================================================================

🆕 Starting new session: auto_20250116_143022

📁 Created output directory: output/auto_20250116_143022

📋 Station Execution Order:
    1. ⏳ Station 1: Seed Processor
    2. ⏳ Station 2: Project DNA Builder
    3. ⏳ Station 3: Age/Genre Optimizer
    ...
   20. ⏳ Station 20: Geography & Transit

🎯 Progress: 1/20 stations
📊 Success Rate: Starting...

🚀 Starting Station 1: Seed Processor
============================================================
🎬 STATION 1: SEED PROCESSOR & SCALE EVALUATOR
============================================================
...
✅ Station 1: Seed Processor completed successfully
💾 Checkpoint saved: output/auto_20250116_143022/checkpoint_auto_20250116_143022.json

🎯 Progress: 2/20 stations
📊 Success Rate: 1/1 (100.0%)

🚀 Starting Station 2: Project DNA Builder
...
```

## Troubleshooting

### Common Issues

**Issue**: "Redis connection failed"
**Solution**: Start Redis server
```bash
redis-server
# or
sudo systemctl start redis
```

**Issue**: "OpenRouter API error"
**Solution**: Check API key
```bash
echo $OPENROUTER_API_KEY
```

**Issue**: "No such module named 'app'"
**Solution**: Run from project root directory
```bash
cd /path/to/Final_Script
python full_automation.py
```

**Issue**: "Station X failed"
**Solution**: Check logs and resume
```bash
tail -f automation.log
python full_automation.py --resume auto
```

### Log Files

- **automation.log**: Complete automation log
- **checkpoint_*.json**: Progress checkpoints
- **automation_summary_*.json**: Final summary

## Tips

1. **Monitor Progress**: Watch the console output for real-time updates
2. **Check Logs**: Use `tail -f automation.log` to monitor detailed logs
3. **Resume Often**: The script saves checkpoints after each station
4. **Handle Failures**: Failed stations don't stop the pipeline - you can resume
5. **Review Outputs**: Check individual station outputs in their respective folders

## Advanced Usage

### Custom Session ID
```bash
# The script generates auto_YYYYMMDD_HHMMSS by default
# You can resume any previous session
python full_automation.py --resume session_20250116_143022
```

### Monitoring
```bash
# Monitor logs in real-time
tail -f automation.log

# Check Redis data
python query_redis.py
```

### Cleanup
```bash
# Remove old sessions (optional)
rm -rf output/auto_*
```

---

**Ready to automate your audiobook production? Run `python full_automation.py` and let the system handle everything!**
