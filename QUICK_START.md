# Quick Start - Full Automation with Resume

## 🚀 Start New Run

```bash
python full_automation.py --auto-approve
```
Enter story concept → automation runs → saves checkpoints → generates all PDFs

---

## 🔄 Resume from Checkpoint

**List available sessions:**
```bash
python full_automation.py --list-checkpoints
```

**Resume specific session:**
```bash
python full_automation.py --resume auto_20250922_145032 --auto-approve
```

---

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `python full_automation.py` | Start new automation (interactive) |
| `python full_automation.py --auto-approve` | Start with auto-approve |
| `python full_automation.py --list-checkpoints` | Show all checkpoints |
| `python full_automation.py --resume SESSION_ID` | Resume from checkpoint |
| `python full_automation.py --help` | Show help |

---

## 🎯 What Gets Generated

After completion, check `outputs/` directory:

```
✅ automation_summary_SESSION_ID.json     - Complete run summary
✅ checkpoint_SESSION_ID.json             - Resume checkpoint
✅ station4_seedbank_SESSION_ID.pdf       - Story seeds
✅ station5_season_architecture_SESSION_ID.pdf
✅ station6_master_style_guide_SESSION_ID.pdf
✅ station7_reality_check_SESSION_ID.pdf
✅ station8_character_bible_SESSION_ID.pdf
✅ station9_world_bible_SESSION_ID.pdf
✅ station10_narrative_reveal_SESSION_ID.pdf
✅ station11_runtime_planning_SESSION_ID.pdf
✅ station12_hooks_cliffhangers_SESSION_ID.pdf
✅ station13_multiworld_timeline_SESSION_ID.pdf
✅ station14_episode_blueprints_SESSION_ID.pdf   ← Human review needed!
```

---

## 🛑 Interruption Handling

**Press Ctrl+C during run:**
```
^C
👋 Automation stopped by user.
💾 Progress saved to checkpoint

💡 TIP: Resume using: python full_automation.py --resume auto_20250103_142531
```

**Then resume later:**
```bash
python full_automation.py --resume auto_20250103_142531 --auto-approve
```

✅ Continues exactly where you left off!

---

## ⚡ Quick Reference

**New run:**
```bash
python full_automation.py --auto-approve --debug
```

**Check progress:**
```bash
python full_automation.py --list-checkpoints
```

**Resume:**
```bash
python full_automation.py --resume SESSION_ID --auto-approve
```

**Manual station testing:**
```bash
python resume_automation.py  # Interactive station-by-station
```

---

## 📖 Full Documentation

See [AUTOMATION_GUIDE.md](./AUTOMATION_GUIDE.md) for complete details, troubleshooting, and advanced usage.
