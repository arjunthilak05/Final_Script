# Remaining Stations 5-10 Optimization Guide

## Quick Reference

We've successfully optimized **Stations 1-4**, removing **1,127 lines** (26% reduction).

Remaining work for **Stations 5-10**:

---

## Station 5: Season Architecture (1,829 lines)

**Complexity:** HIGH - 11 parsing/extraction methods

**Current Issues:**
- Complex screenplay style library parsing
- Multiple extraction methods for episode grids
- Rhythm mapping parsing

**Optimization Strategy:**
1. Update `/app/agents/configs/station_5.yml` to request JSON
2. Add JSON extractor import
3. Replace parsing methods:
   - `_parse_style_recommendations()`
   - `_parse_macro_structure()`
   - `_parse_episode_grid()`
   - `_parse_rhythm_mapping()`
   - And 7 more

**Expected Savings:** ~400-500 lines (22-27%)

---

## Station 6: Master Style Guide

**Complexity:** MEDIUM

**Files to check:**
```bash
wc -l /Users/mac/Desktop/script/app/agents/station_06*
```

**Pattern to Apply:**
1. Check for extraction methods
2. Update YML to JSON format
3. Use `extract_json()` utility
4. Remove old parsers

---

## Station 7: Reality Check System

**Complexity:** MEDIUM

**Pattern:** Same as above

---

## Station 8: Character Architecture

**Complexity:** HIGH - Likely has complex character parsing

**Expected Issues:**
- Character tier parsing
- Voice signature extraction
- Relationship mapping

**Solution:** Request JSON with structured character data

---

## Station 9: World Building System

**Complexity:** HIGH - Geographic and cultural data

**Expected Issues:**
- Location parsing
- Sonic signature extraction
- Social system parsing

**Solution:** JSON with nested structures for locations, systems, etc.

---

## Station 10: Narrative Reveal Strategy

**Complexity:** VERY HIGH - 45+ reveal styles

**Expected Issues:**
- Reveal taxonomy parsing
- Plant/Proof/Payoff grid extraction
- Method catalog parsing

**Solution:** Large JSON with arrays of reveals and methods

---

## Quick Optimization Checklist

For each station (5-10):

### Step 1: Analyze
```bash
# Count lines
wc -l station_XX_*.py

# Find extraction methods
grep -n "def _.*parse\|def _.*extract" station_XX_*.py
```

### Step 2: Update YML
```yaml
prompts:
  main: |
    Return ONLY valid JSON:

    ```json
    {
      "field1": "value",
      "field2": ["array"],
      "field3": {
        "nested": "object"
      }
    }
    ```

    CRITICAL: Return ONLY valid JSON.
```

### Step 3: Update Python
```python
# Add import
from app.agents.json_extractor import extract_json

# Replace parsing method
def _parse_response(self, response: str) -> Output:
    data = extract_json(response)
    return OutputClass(**data)

# Delete old extraction methods
# (Everything starting with _extract_ or _parse_)
```

### Step 4: Test
```bash
python test_station_XX.py
```

---

## Estimated Total Savings

| Station | Est. Lines | Est. Extraction Methods | Est. Reduction |
|---------|-----------|-------------------------|----------------|
| Station 5 | 1,829 | 11 methods | ~450 lines (25%) |
| Station 6 | ~800 | ~5 methods | ~150 lines (19%) |
| Station 7 | ~700 | ~4 methods | ~120 lines (17%) |
| Station 8 | ~1,200 | ~8 methods | ~250 lines (21%) |
| Station 9 | ~1,100 | ~7 methods | ~220 lines (20%) |
| Station 10 | ~1,500 | ~10 methods | ~350 lines (23%) |
| **TOTAL** | **~7,129** | **~45 methods** | **~1,540 lines (22%)** |

---

## Combined Total (Stations 1-10)

| Metric | Value |
|--------|-------|
| **Already Optimized (1-4)** | 1,127 lines removed |
| **Remaining (5-10)** | ~1,540 lines to remove |
| **TOTAL EXPECTED** | **~2,667 lines removed** |
| **Original Total** | ~11,478 lines |
| **Final Total** | **~8,811 lines** |
| **Reduction Percentage** | **~23% reduction** |

---

## Priority Order

1. **Station 5** - Largest, most complex
2. **Station 10** - Reveal strategy complexity
3. **Station 8** - Character architecture
4. **Station 9** - World building
5. **Station 6** - Style guide (smaller)
6. **Station 7** - Reality check (smallest)

---

## Common Pitfalls to Avoid

### 1. Don't Keep Fallbacks
```python
# ❌ BAD
data = extract_json(response)
if not data:
    return self._fallback_parsing(response)

# ✅ GOOD
data = extract_json(response)  # Let it fail if no JSON
return OutputClass(**data)
```

### 2. Don't Validate Too Much
```python
# ❌ BAD - Defensive programming for low-quality LLMs
if "field1" not in data:
    data["field1"] = "default"
if not isinstance(data["field2"], list):
    data["field2"] = []

# ✅ GOOD - Trust the LLM
return OutputClass(**data)
```

### 3. Don't Parse Text
```python
# ❌ BAD
if "Option A:" in response:
    option_a = self._extract_option(response, "A")

# ✅ GOOD
data = extract_json(response)
option_a = data["option_a"]
```

---

## Testing Strategy

After optimizing each station:

1. **Unit Test JSON Parsing**
```python
def test_station_X_parsing():
    sample_json = '''{"field": "value"}'''
    result = station.parse(sample_json)
    assert result.field == "value"
```

2. **Integration Test with Real LLM**
```bash
python full_automation.py --test-mode --stations X
```

3. **Verify Redis Output**
```bash
redis-cli GET "audiobook:test_session:station_0X"
```

---

## Success Criteria

For each station:
- ✅ YML updated to request JSON
- ✅ Python uses `extract_json()`
- ✅ All `_extract_*` and `_parse_*` methods removed
- ✅ Tests pass
- ✅ 15-25% line reduction achieved

---

## Time Estimate

Per station: ~30-45 minutes
- 10 min: Analyze current code
- 15 min: Update YML and Python
- 10 min: Test and debug
- 5 min: Document changes

**Total for 6 stations:** ~3-4.5 hours

---

## Final Notes

You've already done the hard part (Stations 1-4, especially Station 4 which was most complex).

Stations 5-10 follow the exact same pattern:
1. JSON in YML
2. `extract_json()` in Python
3. Delete old methods
4. Test

The pattern is proven and repeatable. Just apply it systematically to each remaining station.

**You're 40% done. Keep going!** 🚀
