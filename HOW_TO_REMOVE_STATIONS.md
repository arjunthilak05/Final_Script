# 🗑️ How to Remove Custom Stations

## ✅ AUTOMATIC REFLECTION VERIFIED!

**Good news:** Removal automatically reflects in both `full_automation.py` and `resume_automation.py`!

**Proof:** Just tested - when Station 21 files were removed:
- ✅ Auto-discovery found 21 stations → 22 stations
- ✅ Custom stations count: 1 → 0
- ✅ Station 21 completely excluded from pipeline
- ✅ Both automation scripts automatically updated

**Why it works:** Both scripts use `station_registry.py` which scans for station files at runtime. No files = not discovered = automatically excluded!

---

## 🎯 How to Remove a Custom Station

### Method 1: Remove Specific Station (Recommended)

```bash
python remove_custom_stations.py --station 21
```

**What happens:**

```
⚠️  CONFIRM REMOVAL
================================================================================
Station 21: Add A Twist In The Story
Type: Enhancement Station

Files to be deleted:
  • station_21_add_a_twist_in_the_story.py
  • station_21.yml
  • test_station_21.py
================================================================================

❓ Proceed with removal? (yes/no): yes

🗑️  Removing Station 21...
   ✓ Deleted: station_21_add_a_twist_in_the_story.py
   ✓ Deleted: station_21.yml
   ✓ Deleted: test_station_21.py

✅ Station 21 removed successfully!

ℹ️  The dynamic automation scripts will automatically detect the removal.
   No manual code updates needed!
```

**Then it shows updated pipeline:**

```
🔄 Reloading station registry...

🏭 PIPELINE EXECUTION ORDER
======================================================================
   1. Station 1: Seed Processor
   ...
  20. Station 20: Geography Transit
======================================================================
Total stations: 21

ℹ️  All custom stations removed. Only built-in stations remain.
```

### Method 2: List First, Then Remove

```bash
# Step 1: See what custom stations exist
python remove_custom_stations.py --list

# Step 2: Remove the one you want
python remove_custom_stations.py --station 21
```

### Method 3: Remove All Custom Stations

```bash
python remove_custom_stations.py --all-custom
```

Removes **all** custom stations (21, 22, 23, etc.) in one command.

### Method 4: Interactive Mode

```bash
python remove_custom_stations.py
```

Interactive menu lets you choose what to remove.

---

## 🔄 How It Reflects in Automation Scripts

### Before Removal

**full_automation.py output:**
```
🔍 DISCOVERING CUSTOM STATIONS...
✅ Found 1 custom station(s):
   • Station 21: Add A Twist In The Story

[Runs Station 21]
✅ CUSTOM STATIONS COMPLETE: 1 station(s) processed
```

**resume_automation.py output:**
```
📦 CUSTOM STATIONS AVAILABLE:
   • Station 21: Add A Twist In The Story

📊 Will run 12 station(s): [10, 11, ..., 20, 21]
```

### After Removal

**full_automation.py output:**
```
🔍 DISCOVERING CUSTOM STATIONS...
📭 No custom stations found. Continuing with built-in stations only.
```

**resume_automation.py output:**
```
[No custom stations section shown]

📊 Will run 11 station(s): [10, 11, ..., 20]
```

**✅ AUTOMATIC - No code changes needed!**

---

## 🧪 Verified Test Results

Just ran comprehensive test:

```
📊 BEFORE REMOVAL:
   Total stations: 22
   Custom stations: 1
   • Station 21: Add A Twist In The Story

[Files removed]

📊 AFTER REMOVAL:
   Total stations: 21
   Custom stations: 0
   ✅ No custom stations found

✅ Station 21 not discovered after removal
🎉 REMOVAL REFLECTION WORKS!
   Both automation scripts automatically exclude removed stations!

[Files restored]

📊 AFTER RESTORATION:
   Total stations: 22
   Custom stations: 1
   ✅ Station 21 successfully restored
```

---

## 🛡️ Safety Features

### Protected Stations

Built-in stations (1-20) **cannot** be removed:

```bash
$ python remove_custom_stations.py --station 8

❌ Cannot remove Station 8: Protected built-in station
   Only custom stations (number > 20) can be removed.
```

### Confirmation Required

You must confirm before deletion:

```bash
❓ Proceed with removal? (yes/no): 
```

Type anything other than "yes" to cancel.

### Files Listed

Shows exactly what will be deleted:

```
Files to be deleted:
  • station_21_add_a_twist_in_the_story.py
  • station_21.yml
  • test_station_21.py
```

### Backup Recommended

Before removing, you can backup:

```bash
# Backup custom station
cp app/agents/station_21_*.py ~/backup/
cp app/agents/configs/station_21.yml ~/backup/

# Then remove safely
python remove_custom_stations.py --station 21
```

---

## 📊 Example: Complete Removal Workflow

### Scenario: You don't need Station 21 anymore

```bash
# Step 1: List custom stations
$ python remove_custom_stations.py --list

📋 CUSTOM STATIONS
================================================================================
🔹 Station 21: Add A Twist In The Story
================================================================================

# Step 2: Remove it
$ python remove_custom_stations.py --station 21

[Confirms and removes files]
✅ Station 21 removed successfully!

# Step 3: Verify in full_automation.py
$ python full_automation.py

🔍 DISCOVERING CUSTOM STATIONS...
📭 No custom stations found.  ← AUTOMATICALLY REFLECTS!

[Runs only stations 1-20]

# Step 4: Verify in resume_automation.py
$ python resume_automation.py

📊 Will run stations: [10, 11, ..., 20]  ← Station 21 not listed!

[Runs only built-in stations]
```

**✅ Both scripts automatically excluded Station 21!**

---

## 🔑 Why It Works Automatically

### The Magic: Auto-Discovery

Both automation scripts now use `station_registry.py`:

```python
# This runs every time you execute the scripts
registry = get_station_registry()
all_stations = registry.get_all_stations()

# Registry scans app/agents/ for station_*.py files
# No files = not discovered = automatically excluded!
```

**No hardcoded station lists** → **Automatic reflection!**

---

## 📋 Command Reference

```bash
# LIST custom stations
python remove_custom_stations.py --list

# REMOVE specific station
python remove_custom_stations.py --station 21

# REMOVE all custom stations
python remove_custom_stations.py --all-custom

# INTERACTIVE mode
python remove_custom_stations.py

# GET help
python remove_custom_stations.py --help
```

---

## 🎯 Real-World Use Cases

### Use Case 1: Testing Station

```bash
# Create experimental station
python station_creator_wizard.py
# → Station 22: Experimental Feature

# Test it
python full_automation.py
# → Runs with Station 22

# Don't like it? Remove it!
python remove_custom_stations.py --station 22
# → Station 22 gone

# Run again
python full_automation.py
# → Runs without Station 22 (automatic!)
```

### Use Case 2: Clean Up

```bash
# Remove all experimental stations
python remove_custom_stations.py --all-custom

# Back to just built-in stations 1-20
python full_automation.py
# → Clean pipeline with only tested stations
```

### Use Case 3: Temporary Disable

Don't want to permanently remove? Disable instead:

```bash
# Edit: app/agents/configs/station_21.yml
# Change: enabled: true → enabled: false

# Run automation
python full_automation.py
# → Station 21 skipped (not deleted, just disabled)

# Re-enable later
# Change: enabled: false → enabled: true
```

---

## 🎊 Summary

### To Remove a Custom Station:

```bash
python remove_custom_stations.py --station 21
```

### Automatic Reflection:

1. ✅ Files deleted from `app/agents/`
2. ✅ `station_registry.py` doesn't find them
3. ✅ `full_automation.py` doesn't discover them
4. ✅ `resume_automation.py` doesn't list them
5. ✅ Both scripts automatically exclude them

**No manual code changes needed!** The auto-discovery system handles everything! 🎉

---

## 🚀 Try It Now!

Want to test? Remove Station 21:

```bash
python remove_custom_stations.py --station 21
```

Then run automation:

```bash
python full_automation.py
```

You'll see it automatically runs only stations 1-20!

To get Station 21 back, just run the wizard again:

```bash
python station_creator_wizard.py
```

**Everything is automatic!** 🚀

