#!/usr/bin/env python3
"""
Station Creator Wizard - Root Level Runner

Run from project root to create new stations that automatically integrate.

Usage:
    python station_creator_wizard.py

This wizard will:
1. Guide you through creating a custom station
2. Generate all necessary files (Python, YAML, test script)
3. Automatically integrate with full_automation.py and resume_automation.py
4. No manual code changes needed!
"""

import sys
import asyncio
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "tools" / "tools"))

# Import the wizard from tools/tools directory
from station_creator_wizard import StationCreatorWizard


async def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("🎯 STATION CREATOR WIZARD")
    print("="*80)
    print("✨ Create custom stations that auto-integrate with the pipeline")
    print("🔄 No manual code changes needed!")
    print("🚀 Stations are automatically discovered and executed")
    print("="*80 + "\n")
    
    # Run the wizard
    wizard = StationCreatorWizard()
    await wizard.run()
    
    print("\n" + "="*80)
    print("✅ STATION CREATED AND AUTO-INTEGRATED!")
    print("="*80)
    print("Your new station will be automatically discovered by:")
    print("  • full_automation_dynamic.py")
    print("  • resume_automation_dynamic.py")
    print("\nNo manual integration needed! The station is ready to use.")
    print("\nNext steps:")
    print("  1. Test your station with the generated test script")
    print("  2. Run full_automation_dynamic.py to see it in action")
    print("  3. Edit the generated files if you need to customize")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

