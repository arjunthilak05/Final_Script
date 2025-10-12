#!/usr/bin/env python3
"""
Full Automation with Dynamic Station Discovery

Automatically discovers and runs all stations in dependency order.
No manual integration needed for new stations!

Usage:
    python full_automation_dynamic.py
"""

import asyncio
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import asdict
from uuid import uuid4

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.append(str(Path(__file__).parent / "app"))

from app.agents.station_registry import get_station_registry, reload_registry
from app.redis_client import RedisClient


class DynamicAutomationRunner:
    """
    Automation runner that automatically discovers and executes stations
    """
    
    def __init__(self, auto_approve: bool = True, debug_mode: bool = False):
        self.auto_approve = auto_approve
        self.debug_mode = debug_mode
        self.registry = get_station_registry()
        self.redis = None
        self.current_session_id = None
    
    def emit_progress(self, station: str, percentage: int, message: str = ""):
        """Emit progress update"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🔄 {station}: {percentage}% - {message}")
    
    async def run_station(self, station_num: float, session_id: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dynamically load and run any station
        
        Args:
            station_num: Station number to run
            session_id: Session ID
            state: Current pipeline state
        
        Returns:
            Updated state with station output
        """
        metadata = self.registry.get_station_metadata(station_num)
        if not metadata:
            raise ValueError(f"Station {station_num} not found")
        
        if not metadata.enabled:
            logger.info(f"⏭️  Station {station_num} is disabled, skipping...")
            return state
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🚀 STATION {station_num}: {metadata.name}")
        logger.info(f"   Type: {metadata.station_type}")
        logger.info(f"   Dependencies: {metadata.dependencies if metadata.dependencies else 'None'}")
        logger.info(f"{'='*70}\n")
        
        self.emit_progress(f"Station {station_num}", 0, f"Initializing {metadata.name}...")
        
        try:
            # Dynamically load the station class
            StationClass = self.registry.load_station_class(station_num)
            
            # Special handling for Station 1 (needs story concept)
            if station_num == 1:
                station = StationClass()
                await station.initialize()
                result = await station.process(state['story_concept'], session_id)
                
                # Store result in a consistent way
                if hasattr(result, '__dict__'):
                    result_dict = asdict(result) if hasattr(result, '__dataclass_fields__') else vars(result)
                else:
                    result_dict = {'result': str(result)}
                
                state['station_outputs'][f'station_{int(station_num)}'] = result_dict
                
            else:
                # Standard station initialization
                # Check if station needs special constructor (like Station 20)
                try:
                    # Try with session_id parameter first
                    station = StationClass(session_id)
                except TypeError:
                    # Fall back to no parameters
                    station = StationClass()
                
                await station.initialize()
                
                self.emit_progress(f"Station {station_num}", 30, "Processing...")
                
                result = await station.process(session_id)
                
                # Store result based on type
                if hasattr(result, '__dict__'):
                    result_dict = asdict(result) if hasattr(result, '__dataclass_fields__') else vars(result)
                else:
                    result_dict = {'result': str(result)}
                
                state['station_outputs'][f'station_{int(station_num) if station_num == int(station_num) else station_num}'] = result_dict
            
            self.emit_progress(f"Station {station_num}", 100, "Complete!")
            
            logger.info(f"✅ Station {station_num} COMPLETE\n")
            
            return state
            
        except Exception as e:
            logger.error(f"❌ Station {station_num} FAILED: {str(e)}")
            logger.exception("Full error details:")
            raise
    
    async def run_full_automation(self, story_concept: str) -> Dict[str, Any]:
        """
        Run the complete automation pipeline with dynamic station discovery
        """
        print("\n" + "="*80)
        print("🚀 DYNAMIC AUDIOBOOK PRODUCTION AUTOMATION")
        print("="*80)
        print(f"📝 Story Concept: {story_concept[:100]}...")
        print(f"🎯 Mode: {'Auto-approve' if self.auto_approve else 'Interactive'}")
        print(f"🐛 Debug: {'Enabled' if self.debug_mode else 'Disabled'}")
        print("="*80)
        
        # Reload registry to pick up any new stations
        logger.info("🔄 Reloading station registry...")
        self.registry = reload_registry()
        
        # Show discovered pipeline
        self.registry.print_pipeline()
        
        # Get execution order
        try:
            execution_order = self.registry.get_execution_order()
        except ValueError as e:
            print(f"\n❌ Pipeline configuration error: {e}")
            print("Please check your station dependencies for circular references.\n")
            return None
        
        # Initialize state
        session_id = str(uuid4())[:8]
        self.current_session_id = session_id
        
        state = {
            'session_id': session_id,
            'story_concept': story_concept,
            'station_outputs': {},
            'start_time': datetime.now(),
            'completed_stations': []
        }
        
        print(f"\n📋 Session ID: {session_id}")
        print(f"📊 Pipeline: {len(execution_order)} stations to execute\n")
        
        # Initialize Redis
        self.redis = RedisClient()
        await self.redis.initialize()
        
        try:
            # Execute stations in dependency order
            total_stations = len(execution_order)
            for idx, station_num in enumerate(execution_order, 1):
                print(f"\n{'─'*70}")
                print(f"Progress: [{idx}/{total_stations}] Station {station_num}")
                print(f"{'─'*70}")
                
                state = await self.run_station(station_num, session_id, state)
                state['completed_stations'].append(station_num)
                
                # Save checkpoint
                await self._save_checkpoint(session_id, state)
            
            # Complete
            state['end_time'] = datetime.now()
            state['status'] = 'completed'
            duration = state['end_time'] - state['start_time']
            
            print("\n" + "="*80)
            print("🎉 PIPELINE COMPLETE!")
            print("="*80)
            print(f"✓ Session ID: {session_id}")
            print(f"✓ Stations completed: {len(state['completed_stations'])}")
            print(f"✓ Duration: {duration}")
            print(f"✓ Status: All stations executed successfully")
            print("="*80 + "\n")
            
            return state
            
        except KeyboardInterrupt:
            logger.warning("\n⚠️  Pipeline interrupted by user")
            state['status'] = 'interrupted'
            state['interrupted_at'] = datetime.now()
            await self._save_checkpoint(session_id, state)
            print(f"\n💾 Progress saved. Resume with: python resume_automation_dynamic.py")
            print(f"   Session ID: {session_id}\n")
            raise
            
        except Exception as e:
            logger.error(f"\n❌ Pipeline failed: {e}")
            state['status'] = 'failed'
            state['error'] = str(e)
            state['failed_at'] = datetime.now()
            await self._save_checkpoint(session_id, state)
            print(f"\n💾 Progress saved. You can attempt to resume with: python resume_automation_dynamic.py")
            print(f"   Session ID: {session_id}\n")
            raise
    
    async def _save_checkpoint(self, session_id: str, state: Dict[str, Any]):
        """Save pipeline checkpoint"""
        try:
            # Convert datetime objects to strings for JSON serialization
            checkpoint = state.copy()
            if 'start_time' in checkpoint:
                checkpoint['start_time'] = checkpoint['start_time'].isoformat()
            if 'end_time' in checkpoint:
                checkpoint['end_time'] = checkpoint['end_time'].isoformat()
            if 'interrupted_at' in checkpoint:
                checkpoint['interrupted_at'] = checkpoint['interrupted_at'].isoformat()
            if 'failed_at' in checkpoint:
                checkpoint['failed_at'] = checkpoint['failed_at'].isoformat()
            
            checkpoint_key = f"audiobook:{session_id}:pipeline_state"
            await self.redis.set(checkpoint_key, json.dumps(checkpoint, default=str), expire=86400)
            logger.debug(f"Checkpoint saved for session {session_id}")
        except Exception as e:
            logger.warning(f"Failed to save checkpoint: {e}")


async def main():
    """Main entry point"""
    print("\n" + "🎬"*40)
    print("   DYNAMIC AUDIOBOOK PRODUCTION SYSTEM")
    print("🎬"*40 + "\n")
    
    # Get story concept
    print("This system automatically discovers and runs all enabled stations.")
    print("New stations created with station_creator_wizard.py are auto-integrated!\n")
    
    story_concept = input("📝 Enter your story concept: ").strip()
    
    if not story_concept:
        print("❌ Story concept required")
        return
    
    print(f"\n🚀 Starting automation with concept: '{story_concept[:80]}...'\n")
    
    # Run automation
    runner = DynamicAutomationRunner(auto_approve=True, debug_mode=False)
    
    try:
        result = await runner.run_full_automation(story_concept)
        
        if result:
            print(f"\n✅ Success! Session ID: {result['session_id']}")
            print(f"\nAll outputs are stored in Redis under session: {result['session_id']}")
            print(f"You can access individual station outputs using the session ID.\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        logger.exception("Full error details:")


if __name__ == "__main__":
    asyncio.run(main())

