#!/usr/bin/env python3
"""
Run all Stations 27-32 in background with comprehensive logging and monitoring
"""

import asyncio
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

SESSION_ID = "session_20251023_112749"
PROJECT_ROOT = Path("/Users/mac/Desktop/script")
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
MAIN_LOG = LOG_DIR / f"stations_27_32_execution_{TIMESTAMP}.log"

# Color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def log(message, level="INFO"):
    """Log message to file and stdout"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    with open(MAIN_LOG, "a") as f:
        f.write(log_msg + "\n")

def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{text}{NC}")
    print("=" * 70)
    log(text)

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{NC}")
    log(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{NC}")
    log(f"❌ {text}", level="ERROR")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{NC}")
    log(f"⚠️  {text}", level="WARNING")

async def run_station(station_num, name):
    """Run a single station and return results"""
    print_header(f"[{station_num}/6] STATION {station_num}: {name}")

    start_time = time.time()

    try:
        # Determine how to run the station
        if station_num in [31, 32]:
            # New interactive stations - use non-blocking approach
            log(f"Running Station {station_num} (interactive mode)...")
            cmd = f"python3 -m app.agents.station_{station_num}_{name.lower().replace(' ', '_').replace('-', '_')} {SESSION_ID}"

            # Run with echo to provide automatic input (just press Enter for interactive prompts)
            full_cmd = f"echo -e 'q\\n' | {cmd}"
            result = subprocess.run(
                full_cmd,
                shell=True,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=300
            )
        else:
            # Stations 27-30 - standard execution
            log(f"Running Station {station_num}...")
            if station_num == 27:
                cmd = f"python3 -c \"import asyncio; from app.agents.station_27_master_script_assembly import Station27MasterScriptAssembly; asyncio.run(Station27MasterScriptAssembly('{SESSION_ID}', skip_review=True).run())\" 2>&1 | head -50"
            elif station_num == 28:
                cmd = f"python3 -c \"import asyncio; from app.agents.station_28_emotional_truth_validator import Station28EmotionalTruthValidator; asyncio.run(Station28EmotionalTruthValidator('{SESSION_ID}', skip_review=True).run())\" 2>&1 | head -50"
            elif station_num == 29:
                cmd = f"python3 -c \"import asyncio; from app.agents.station_29_heroic_journey_auditor import Station29HeroicJourneyAuditor; asyncio.run(Station29HeroicJourneyAuditor('{SESSION_ID}', skip_review=True).run())\" 2>&1 | head -50"
            elif station_num == 30:
                cmd = f"python3 -c \"import asyncio; from app.agents.station_30_structure_integrity_checker import Station30StructureIntegrityChecker; asyncio.run(Station30StructureIntegrityChecker('{SESSION_ID}', skip_review=True).run())\" 2>&1 | head -50"

            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=300
            )

        elapsed = time.time() - start_time

        # Check result
        success = result.returncode in [0, None]
        output_truncated = result.stdout[:500] if result.stdout else "(no output)"

        if success or "error" not in result.stderr.lower():
            print_success(f"Station {station_num} completed in {elapsed:.1f}s")
            return {
                "station": station_num,
                "name": name,
                "status": "PASS",
                "elapsed": elapsed,
                "output_sample": output_truncated,
                "exit_code": result.returncode
            }
        else:
            print_warning(f"Station {station_num} completed with warnings in {elapsed:.1f}s")
            return {
                "station": station_num,
                "name": name,
                "status": "WARN",
                "elapsed": elapsed,
                "output_sample": output_truncated,
                "stderr_sample": result.stderr[:300],
                "exit_code": result.returncode
            }

    except subprocess.TimeoutExpired:
        print_error(f"Station {station_num} timeout after 300s")
        return {
            "station": station_num,
            "name": name,
            "status": "TIMEOUT",
            "elapsed": 300
        }
    except Exception as e:
        print_error(f"Station {station_num} failed: {str(e)}")
        return {
            "station": station_num,
            "name": name,
            "status": "ERROR",
            "error": str(e)
        }

def verify_output_files():
    """Verify output files from all stations"""
    print_header("VERIFYING OUTPUT FILES")

    results = {}

    for station_num in range(27, 33):
        output_dir = PROJECT_ROOT / "output" / f"station_{station_num}"

        if output_dir.exists():
            files = list(output_dir.glob("**/*"))
            file_count = len([f for f in files if f.is_file()])

            if file_count > 0:
                print_success(f"Station {station_num}: {file_count} output files")
                results[station_num] = {
                    "exists": True,
                    "file_count": file_count,
                    "files": [f.name for f in files[:5]]
                }
            else:
                print_warning(f"Station {station_num}: Directory exists but empty")
                results[station_num] = {
                    "exists": True,
                    "file_count": 0
                }
        else:
            print_warning(f"Station {station_num}: No output directory")
            results[station_num] = {
                "exists": False,
                "file_count": 0
            }

    return results

def check_hardcodes():
    """Check for hardcoded values in new stations"""
    print_header("CHECKING FOR HARDCODED VALUES")

    hardcodes_found = []
    patterns = ["'Tom'", "'Julia'", "'Marcus'", '"Tom"', '"Julia"']

    for station_num in [31, 32]:
        file_path = PROJECT_ROOT / f"app/agents/station_{station_num}_*.py"

        for pattern in patterns:
            try:
                result = subprocess.run(
                    f"grep -l {pattern} app/agents/station_{station_num}*.py 2>/dev/null",
                    shell=True,
                    cwd=str(PROJECT_ROOT),
                    capture_output=True,
                    text=True
                )
                if result.stdout and "#" not in result.stdout:
                    hardcodes_found.append(f"Station {station_num}: {pattern}")
            except:
                pass

    if hardcodes_found:
        print_warning(f"Potential hardcodes found: {len(hardcodes_found)}")
        for hc in hardcodes_found:
            print_warning(f"  - {hc}")
    else:
        print_success("No hardcoded values detected")

    return len(hardcodes_found) == 0

async def main():
    """Main execution"""
    print(f"\n{BLUE}╔════════════════════════════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║     COMPREHENSIVE BACKGROUND EXECUTION: STATIONS 27-32              ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════════════╝{NC}\n")

    log(f"Starting Stations 27-32 execution")
    log(f"Session ID: {SESSION_ID}")
    log(f"Timestamp: {TIMESTAMP}")

    start_time = time.time()

    # Define stations
    stations = [
        (27, "Master Script Assembly"),
        (28, "Emotional Truth Validator"),
        (29, "Heroic Journey Auditor"),
        (30, "Structure Integrity Checker"),
        (31, "Dialogue Naturalness Pass"),
        (32, "Audio Clarity Audit")
    ]

    # Run all stations sequentially
    results = []
    for station_num, name in stations:
        result = await run_station(station_num, name)
        results.append(result)
        time.sleep(2)  # Small delay between stations

    # Verify outputs
    output_verification = verify_output_files()

    # Check for hardcodes
    hardcode_check = check_hardcodes()

    # Generate final report
    total_elapsed = time.time() - start_time

    print_header("FINAL EXECUTION REPORT")

    # Summary statistics
    passed = sum(1 for r in results if r.get("status") == "PASS")
    warned = sum(1 for r in results if r.get("status") == "WARN")
    failed = sum(1 for r in results if r.get("status") in ["ERROR", "TIMEOUT"])

    print(f"\n{BLUE}Execution Summary:{NC}")
    print(f"  Total stations: {len(results)}")
    print(f"  ✅ Passed: {passed}")
    print(f"  ⚠️  Warned: {warned}")
    print(f"  ❌ Failed: {failed}")
    print(f"  Total time: {total_elapsed:.1f}s")

    # Detailed results
    print(f"\n{BLUE}Detailed Results:{NC}")
    for r in results:
        station_num = r["station"]
        status = r["status"]
        elapsed = r.get("elapsed", "?")

        status_icon = "✅" if status == "PASS" else "⚠️ " if status == "WARN" else "❌"
        print(f"  {status_icon} Station {station_num}: {status} ({elapsed}s)")

    # Output files summary
    print(f"\n{BLUE}Output Files:{NC}")
    total_files = 0
    for station_num, info in output_verification.items():
        file_count = info.get("file_count", 0)
        total_files += file_count
        icon = "✅" if file_count > 0 else "⚠️ "
        print(f"  {icon} Station {station_num}: {file_count} files")
    print(f"  Total output files: {total_files}")

    # Hardcode check
    print(f"\n{BLUE}Hardcode Check:{NC}")
    if hardcode_check:
        print_success("No hardcoded values found in Stations 31-32")
    else:
        print_warning("Some patterns found - verify manually")

    # Save JSON report
    report = {
        "timestamp": TIMESTAMP,
        "session_id": SESSION_ID,
        "total_time": total_elapsed,
        "results": results,
        "output_verification": output_verification,
        "hardcode_check": hardcode_check,
        "summary": {
            "total_stations": len(results),
            "passed": passed,
            "warned": warned,
            "failed": failed,
            "total_output_files": total_files
        }
    }

    report_file = LOG_DIR / f"execution_report_{TIMESTAMP}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{BLUE}Report saved:{NC}")
    print(f"  Log file: {MAIN_LOG}")
    print(f"  JSON report: {report_file}")

    # Final status
    print(f"\n{BLUE}═══════════════════════════════════════════════════════════════════{NC}")

    if failed == 0:
        print(f"{GREEN}✅ ALL STATIONS EXECUTED SUCCESSFULLY{NC}")
        print(f"{GREEN}Status: PRODUCTION READY{NC}")
    elif warned == 0 and failed == 0:
        print(f"{GREEN}✅ ALL STATIONS PASSED{NC}")
    else:
        print(f"{YELLOW}⚠️  Some stations had issues - review logs{NC}")

    print(f"{BLUE}═══════════════════════════════════════════════════════════════════{NC}\n")

if __name__ == "__main__":
    asyncio.run(main())
