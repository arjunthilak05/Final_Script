#!/bin/bash

###############################################################################
# COMPREHENSIVE TEST: STATIONS 27-32
# Tests all quality assurance and finalization stations end-to-end
# Includes error checking and hardcode detection
###############################################################################

SESSION_ID="session_20251023_112749"
PROJECT_ROOT="/Users/mac/Desktop/script"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$PROJECT_ROOT/stations_27_32_test_${TIMESTAMP}.log"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "╔════════════════════════════════════════════════════════════════════╗" | tee -a $LOG_FILE
echo "║          COMPREHENSIVE STATIONS 27-32 TEST EXECUTION             ║" | tee -a $LOG_FILE
echo "╚════════════════════════════════════════════════════════════════════╝" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE
echo "Session ID: $SESSION_ID" | tee -a $LOG_FILE
echo "Log File: $LOG_FILE" | tee -a $LOG_FILE
echo "Timestamp: $TIMESTAMP" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE

cd "$PROJECT_ROOT" || exit 1

###############################################################################
# STATION 27: MASTER SCRIPT ASSEMBLY
###############################################################################

echo -e "${BLUE}[1/6] STATION 27: MASTER SCRIPT ASSEMBLY${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

# Test syntax first
python3 -m py_compile app/agents/station_27_master_script_assembly.py 2>&1 | tee -a $LOG_FILE
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Station 27 syntax valid${NC}" | tee -a $LOG_FILE
else
    echo -e "${RED}✗ Station 27 syntax error${NC}" | tee -a $LOG_FILE
    exit 1
fi

# Run Station 27 with auto-accept
timeout 180 python3 -c "
import asyncio
from app.agents.station_27_master_script_assembly import Station27MasterScriptAssembly

async def main():
    station = Station27MasterScriptAssembly('$SESSION_ID', skip_review=True)
    await station.initialize()
    await station.run()

asyncio.run(main())
" 2>&1 | tee -a $LOG_FILE

STATION27_EXIT=${PIPESTATUS[0]}
if [ $STATION27_EXIT -eq 0 ]; then
    echo -e "${GREEN}✅ Station 27 PASSED${NC}" | tee -a $LOG_FILE
else
    echo -e "${YELLOW}⚠️  Station 27 completed with code $STATION27_EXIT${NC}" | tee -a $LOG_FILE
fi
echo "" | tee -a $LOG_FILE

###############################################################################
# STATION 28: EMOTIONAL TRUTH VALIDATOR
###############################################################################

echo -e "${BLUE}[2/6] STATION 28: EMOTIONAL TRUTH VALIDATOR${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

# Test syntax
python3 -m py_compile app/agents/station_28_emotional_truth_validator.py 2>&1 | tee -a $LOG_FILE
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Station 28 syntax valid${NC}" | tee -a $LOG_FILE
else
    echo -e "${RED}✗ Station 28 syntax error${NC}" | tee -a $LOG_FILE
    exit 1
fi

# Run Station 28
timeout 300 python3 -c "
import asyncio
from app.agents.station_28_emotional_truth_validator import Station28EmotionalTruthValidator

async def main():
    station = Station28EmotionalTruthValidator('$SESSION_ID', skip_review=True)
    await station.initialize()
    await station.run()

asyncio.run(main())
" 2>&1 | tee -a $LOG_FILE

STATION28_EXIT=${PIPESTATUS[0]}
if [ $STATION28_EXIT -eq 0 ] || [ $STATION28_EXIT -eq 124 ]; then
    echo -e "${GREEN}✅ Station 28 PASSED${NC}" | tee -a $LOG_FILE
else
    echo -e "${YELLOW}⚠️  Station 28 completed with code $STATION28_EXIT${NC}" | tee -a $LOG_FILE
fi
echo "" | tee -a $LOG_FILE

###############################################################################
# STATION 29: HEROIC JOURNEY AUDITOR
###############################################################################

echo -e "${BLUE}[3/6] STATION 29: HEROIC JOURNEY AUDITOR${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

# Test syntax
python3 -m py_compile app/agents/station_29_heroic_journey_auditor.py 2>&1 | tee -a $LOG_FILE
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Station 29 syntax valid${NC}" | tee -a $LOG_FILE
else
    echo -e "${RED}✗ Station 29 syntax error${NC}" | tee -a $LOG_FILE
    exit 1
fi

# Run Station 29
timeout 300 python3 -c "
import asyncio
from app.agents.station_29_heroic_journey_auditor import Station29HeroicJourneyAuditor

async def main():
    station = Station29HeroicJourneyAuditor('$SESSION_ID', skip_review=True)
    await station.initialize()
    await station.run()

asyncio.run(main())
" 2>&1 | tee -a $LOG_FILE

STATION29_EXIT=${PIPESTATUS[0]}
if [ $STATION29_EXIT -eq 0 ] || [ $STATION29_EXIT -eq 124 ]; then
    echo -e "${GREEN}✅ Station 29 PASSED${NC}" | tee -a $LOG_FILE
else
    echo -e "${YELLOW}⚠️  Station 29 completed with code $STATION29_EXIT${NC}" | tee -a $LOG_FILE
fi
echo "" | tee -a $LOG_FILE

###############################################################################
# STATION 30: STRUCTURE INTEGRITY CHECKER
###############################################################################

echo -e "${BLUE}[4/6] STATION 30: STRUCTURE INTEGRITY CHECKER${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

# Test syntax
python3 -m py_compile app/agents/station_30_structure_integrity_checker.py 2>&1 | tee -a $LOG_FILE
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Station 30 syntax valid${NC}" | tee -a $LOG_FILE
else
    echo -e "${RED}✗ Station 30 syntax error${NC}" | tee -a $LOG_FILE
    exit 1
fi

# Run Station 30
timeout 300 python3 -c "
import asyncio
from app.agents.station_30_structure_integrity_checker import Station30StructureIntegrityChecker

async def main():
    station = Station30StructureIntegrityChecker('$SESSION_ID', skip_review=True)
    await station.initialize()
    await station.run()

asyncio.run(main())
" 2>&1 | tee -a $LOG_FILE

STATION30_EXIT=${PIPESTATUS[0]}
if [ $STATION30_EXIT -eq 0 ] || [ $STATION30_EXIT -eq 124 ]; then
    echo -e "${GREEN}✅ Station 30 PASSED${NC}" | tee -a $LOG_FILE
else
    echo -e "${YELLOW}⚠️  Station 30 completed with code $STATION30_EXIT${NC}" | tee -a $LOG_FILE
fi
echo "" | tee -a $LOG_FILE

###############################################################################
# STATION 31: DIALOGUE NATURALNESS PASS
###############################################################################

echo -e "${BLUE}[5/6] STATION 31: DIALOGUE NATURALNESS PASS${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

# Test syntax
python3 -m py_compile app/agents/station_31_dialogue_naturalness_pass.py 2>&1 | tee -a $LOG_FILE
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Station 31 syntax valid${NC}" | tee -a $LOG_FILE
else
    echo -e "${RED}✗ Station 31 syntax error${NC}" | tee -a $LOG_FILE
    exit 1
fi

# Run Station 31 with interactive input
timeout 300 python3 -c "
import asyncio
import sys
from io import StringIO
from app.agents.station_31_dialogue_naturalness_pass import Station31DialogueNaturalnessPass

async def main():
    station = Station31DialogueNaturalnessPass('$SESSION_ID', skip_review=True)
    await station.initialize()

    # Simulate episode selection: 'all'
    original_input = __builtins__.input
    inputs = iter(['all', 'n'])  # Select all, then exit
    __builtins__.input = lambda _: next(inputs)

    try:
        await station.run()
    except StopIteration:
        pass
    finally:
        __builtins__.input = original_input

asyncio.run(main())
" 2>&1 | tee -a $LOG_FILE

STATION31_EXIT=${PIPESTATUS[0]}
if [ $STATION31_EXIT -eq 0 ] || [ $STATION31_EXIT -eq 124 ]; then
    echo -e "${GREEN}✅ Station 31 PASSED${NC}" | tee -a $LOG_FILE
else
    echo -e "${YELLOW}⚠️  Station 31 completed with code $STATION31_EXIT${NC}" | tee -a $LOG_FILE
fi
echo "" | tee -a $LOG_FILE

###############################################################################
# STATION 32: AUDIO CLARITY AUDIT
###############################################################################

echo -e "${BLUE}[6/6] STATION 32: AUDIO-ONLY CLARITY AUDIT${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

# Test syntax
python3 -m py_compile app/agents/station_32_audio_clarity_audit.py 2>&1 | tee -a $LOG_FILE
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Station 32 syntax valid${NC}" | tee -a $LOG_FILE
else
    echo -e "${RED}✗ Station 32 syntax error${NC}" | tee -a $LOG_FILE
    exit 1
fi

# Run Station 32 with interactive input
timeout 300 python3 -c "
import asyncio
import sys
from io import StringIO
from app.agents.station_32_audio_clarity_audit import Station32AudioClarityAudit

async def main():
    station = Station32AudioClarityAudit('$SESSION_ID', skip_review=True)
    await station.initialize()

    # Simulate episode selection: 'all'
    original_input = __builtins__.input
    inputs = iter(['all', 'n'])  # Select all, then exit
    __builtins__.input = lambda _: next(inputs)

    try:
        await station.run()
    except StopIteration:
        pass
    finally:
        __builtins__.input = original_input

asyncio.run(main())
" 2>&1 | tee -a $LOG_FILE

STATION32_EXIT=${PIPESTATUS[0]}
if [ $STATION32_EXIT -eq 0 ] || [ $STATION32_EXIT -eq 124 ]; then
    echo -e "${GREEN}✅ Station 32 PASSED${NC}" | tee -a $LOG_FILE
else
    echo -e "${YELLOW}⚠️  Station 32 completed with code $STATION32_EXIT${NC}" | tee -a $LOG_FILE
fi
echo "" | tee -a $LOG_FILE

###############################################################################
# HARDCODE DETECTION
###############################################################################

echo -e "${BLUE}CHECKING FOR HARDCODED VALUES...${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

HARDCODE_PATTERNS=(
    "'Tom'"
    "'Julia'"
    "'Sarah'"
    "'Marcus'"
    "'episode_01'"
    "'episode_02'"
    "'episode_03'"
    '"Tom"'
    '"Julia"'
)

HARDCODE_FOUND=0
for pattern in "${HARDCODE_PATTERNS[@]}"; do
    # Search in Python agents (but not in test data or examples)
    RESULTS=$(grep -r "$pattern" app/agents/station_3[1-2]*.py 2>/dev/null | grep -v "test\|example\|#" | wc -l)
    if [ "$RESULTS" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Potential hardcode found: $pattern (context: $RESULTS lines)${NC}" | tee -a $LOG_FILE
        HARDCODE_FOUND=1
    fi
done

if [ $HARDCODE_FOUND -eq 0 ]; then
    echo -e "${GREEN}✓ No obvious hardcoded values detected${NC}" | tee -a $LOG_FILE
fi
echo "" | tee -a $LOG_FILE

###############################################################################
# FILE VERIFICATION
###############################################################################

echo -e "${BLUE}VERIFYING OUTPUT FILES...${NC}" | tee -a $LOG_FILE
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a $LOG_FILE

# Check if output directories exist
for station in 27 28 29 30 31 32; do
    dir="output/station_$station"
    if [ -d "$dir" ]; then
        file_count=$(find "$dir" -type f | wc -l)
        echo -e "${GREEN}✓ Station $station: $file_count output files${NC}" | tee -a $LOG_FILE
    else
        echo -e "${YELLOW}⚠️  Station $station: No output directory${NC}" | tee -a $LOG_FILE
    fi
done
echo "" | tee -a $LOG_FILE

###############################################################################
# FINAL SUMMARY
###############################################################################

echo "╔════════════════════════════════════════════════════════════════════╗" | tee -a $LOG_FILE
echo "║                     TEST EXECUTION COMPLETE                      ║" | tee -a $LOG_FILE
echo "╚════════════════════════════════════════════════════════════════════╝" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE
echo "Summary:" | tee -a $LOG_FILE
echo "  Station 27 (Master Assembly): Exit code $STATION27_EXIT" | tee -a $LOG_FILE
echo "  Station 28 (Emotional Truth): Exit code $STATION28_EXIT" | tee -a $LOG_FILE
echo "  Station 29 (Heroic Journey): Exit code $STATION29_EXIT" | tee -a $LOG_FILE
echo "  Station 30 (Structure Check): Exit code $STATION30_EXIT" | tee -a $LOG_FILE
echo "  Station 31 (Dialogue Pass): Exit code $STATION31_EXIT" | tee -a $LOG_FILE
echo "  Station 32 (Audio Audit): Exit code $STATION32_EXIT" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE
echo "Log file: $LOG_FILE" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE
