<!-- 0ec5aff3-ad3e-4ae7-9823-ec67919e8d78 5bd61b3c-5d0b-437b-936d-7df18d9bc1cc -->
# Fix JSON Parsing Failures in Stations 3, 4, and 5

## Root Cause Analysis

### 🔴 CRITICAL ISSUE #1: Model Mismatch

**Configuration vs. Reality:**

- **YML Configs specify:** `model: "z-ai/glm-4.5"` (Stations 3, 4, 5)
- **Code hardcodes:** `model_name="qwen-72b"` throughout agents
- **Result:** YML config is completely ignored, wrong model is used

**Evidence:**

- `station_3.yml:3` → `model: "z-ai/glm-4.5"`
- `station_03_age_genre_optimizer.py:174` → Uses `self.config.model` (correct)
- `station_04_reference_miner.py:442` → Hardcoded `model_name="qwen-72b"` (WRONG)
- `station_05_season_architecture.py:435` → Hardcoded `model_name="qwen-72b"` (WRONG)

### 🔴 CRITICAL ISSUE #2: Token Limits Too Low

**OpenRouter Configuration:**

```python
# openrouter_agent.py:55
"max_tokens": 1000  # ← SEVERELY LIMITS OUTPUT
```

**Station Requirements:**

- Station 3: `max_tokens: 3000` (YML config)
- Station 4: `max_tokens: 8000` (YML config - needs to generate 65 seeds!)
- Station 5: `max_tokens: 3000` (YML config)

**Actual runtime:**

- `openrouter_agent.py:55` forces `max_tokens: 1000` for all `process_message()` calls
- Station 4 truncates at ~4000 characters (incomplete JSON)
- Station 5 can't return full structure

### 🔴 CRITICAL ISSUE #3: Prompt Format Enforcement

**YML prompts correctly specify:**

````yaml
Return ONLY valid JSON:
```json
{
  ...
}
````

```

**But LLM returns:**

- Station 3: Raw JSON without markdown wrapper
- Station 4: Truncated JSON (token limit)
- Station 5: Plain markdown text instead of JSON

## Problems Identified

| Issue | Location | Impact | Priority |

|-------|----------|---------|----------|

| Hardcoded `qwen-72b` ignoring YML config | Station 4 (all 4 calls) | Wrong model used | P0 |

| Hardcoded `qwen-72b` ignoring YML config | Station 5 (1 call) | Wrong model used | P0 |

| `max_tokens: 1000` hardcoded | `openrouter_agent.py:55` | Response truncation | P0 |

| No enforcement of JSON format | All stations | Format violations | P1 |

| Config not used in station calls | Stations 4, 5 | Config ignored | P0 |

## Solution Strategy

### Phase 1: Fix Model Configuration (P0)

1. **Station 4**: Replace all 4 hardcoded `"qwen-72b"` with `self.config.model`

   - Line 442: `_gather_references()`
   - Line 491: `_extract_tactics()`  
   - Line 1250: `_generate_category_seeds()`
   - Line 1331: `_generate_seeds_with_prompt_variation()`

2. **Station 5**: Replace hardcoded `"qwen-72b"` with config

   - Line 435: Main `process()` method

### Phase 2: Fix Token Limits (P0)

1. **`openrouter_agent.py`**: Change `process_message()` to accept `max_tokens` parameter
   ```python
   async def process_message(self, user_input: str, model_name: str = "qwen-72b", 
                            max_tokens: int = 3000) -> str:
   ```

2. **Update station calls** to use config max_tokens:

   - Station 3: Already uses `generate()` with proper max_tokens ✓
   - Station 4: Update 4 calls to pass `max_tokens=self.config.max_tokens`
   - Station 5: Update call to pass `max_tokens` from config

### Phase 3: Enhance JSON Format Enforcement (P1)

1. Add system message forcing JSON output in `openrouter_agent.py`
2. Post-process responses to strip markdown if present
3. Add validation before returning to catch format issues early

## Implementation Checklist

- [ ] Update `openrouter_agent.py:process_message()` to accept `max_tokens` parameter
- [ ] Station 4: Fix 4 model_name references to use `self.config.model`
- [ ] Station 4: Add `max_tokens=self.config.max_tokens` to all 4 LLM calls
- [ ] Station 5: Fix model_name to use config model
- [ ] Station 5: Add `max_tokens` to LLM call
- [ ] Test with actual automation run to verify fixes

## Expected Outcomes

**Before:**

- Station 3: 4/5 failures (raw JSON without wrapper)
- Station 4: 0 references, 0 seeds (truncated JSON)
- Station 5: Complete failure (no JSON)

**After:**

- Station 3: Should succeed on first attempt with correct model
- Station 4: Full JSON responses (8000 tokens), 20-25 references, 65 seeds
- Station 5: Complete season structure with proper JSON

## Files to Modify

1. `/Users/mac/Desktop/script/app/openrouter_agent.py` (lines 32-56)
2. `/Users/mac/Desktop/script/app/agents/station_04_reference_miner.py` (lines 442, 491, 1250, 1331)
3. `/Users/mac/Desktop/script/app/agents/station_05_season_architecture.py` (line 435)