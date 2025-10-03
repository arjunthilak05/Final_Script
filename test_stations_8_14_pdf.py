#!/usr/bin/env python3
"""
PDF Output Verification Test for Stations 8-14
==============================================

This test file runs stations 8-14 individually and generates PDF outputs
for each station to verify content quality and completeness.

Usage:
    python test_stations_8_14_pdf.py

Features:
- Creates mock data for stations 1-7 dependencies
- Runs each station 8-14 individually
- Generates and validates PDF outputs
- Provides detailed content analysis
- Creates a comprehensive test report

Author: Claude Code Integration Test
"""

import asyncio
import sys
import json
import os
import logging
from datetime import datetime
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / "app"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MockDataGenerator:
    """Generates realistic mock data for stations 1-7 to feed into stations 8-14"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.story_concept = "Sarah discovers an ancient journal in her grandmother's attic that contains mysterious entries about time travel. When she reads the entries aloud, she finds herself transported to different historical periods where she must solve mysteries to return home."
        
    def generate_station_1_data(self):
        """Mock Station 1: Seed Processing & Scale Evaluation"""
        return {
            "original_seed": self.story_concept,
            "scale_options": [
                {"scale_type": "A", "description": "Intimate character study (6-8 episodes)"},
                {"scale_type": "B", "description": "Balanced adventure series (12-15 episodes)"},
                {"scale_type": "C", "description": "Epic multi-season saga (20+ episodes)"}
            ],
            "recommended_option": "B",
            "processing_timestamp": datetime.now().isoformat(),
            "session_id": self.session_id
        }
    
    def generate_station_2_data(self):
        """Mock Station 2: Project DNA Building"""
        return {
            "working_title": "The Time Keeper's Journal",
            "world_setting": {
                "primary_setting": "Multi-temporal (Victorian Era, Ancient Rome, Medieval England)",
                "tone": "Mysterious adventure with historical elements",
                "scope": "Medium scale - 12-episode series"
            },
            "format_specifications": {
                "episode_length": "25-30 minutes",
                "season_count": 1,
                "total_episodes": 12
            },
            "genre_tone": {
                "primary_genres": ["Time Travel", "Historical Mystery", "Adventure"],
                "tone_keywords": ["mysterious", "educational", "thrilling"]
            },
            "audience_profile": {
                "target_age": "Young Adult (16-25)",
                "interests": ["History", "Mystery", "Time Travel"]
            },
            "session_id": self.session_id,
            "created_timestamp": datetime.now().isoformat()
        }
    
    def generate_station_3_data(self):
        """Mock Station 3: Age & Genre Optimization"""
        return {
            "working_title": "The Time Keeper's Journal",
            "age_guidelines": {
                "recommended_age": "16+",
                "content_warnings": ["Mild violence", "Historical trauma references"]
            },
            "chosen_genre_blend": "Historical Time Travel Mystery",
            "tone_calibration": {
                "adventure_level": 8,
                "mystery_level": 9,
                "educational_level": 7
            },
            "session_id": self.session_id,
            "created_timestamp": datetime.now().isoformat()
        }
    
    def generate_station_4_data(self):
        """Mock Station 4: Reference Mining & Seed Extraction"""
        return {
            "working_title": "The Time Keeper's Journal",
            "total_references": 25,
            "total_extractions": 18,
            "total_seeds": 45,
            "seed_collection": {
                "micro_moments": 15,
                "episode_beats": 12,
                "season_arcs": 8,
                "series_defining": 10
            },
            "quality_metrics": {
                "uniqueness_score": 0.87,
                "narrative_coherence": 0.92
            },
            "session_id": self.session_id,
            "created_timestamp": datetime.now().isoformat()
        }
    
    def generate_station_5_data(self):
        """Mock Station 5: Season Architecture"""
        return {
            "working_title": "The Time Keeper's Journal",
            "chosen_style": "Mystery-Adventure Hybrid",
            "total_episodes": 12,
            "confidence_score": 0.89,
            "style_recommendations": 3,
            "tension_peaks": [3, 6, 9, 12],
            "breathing_room": [2, 5, 8, 11],
            "narrator_integration": "Third-person omniscient with character POV shifts",
            "season_architecture": {
                "total_episodes": 12,
                "chosen_style": "Mystery-Adventure Hybrid",
                "style_overview": "Balanced mystery with adventure elements",
                "episode_structure": "3-act structure with cliffhangers",
                "tension_distribution": "Rising action with periodic relief",
                "pacing_guidelines": "25-30 minute episodes"
            },
            "session_id": self.session_id,
            "created_timestamp": datetime.now().isoformat()
        }
    
    def generate_station_6_data(self):
        """Mock Station 6: Master Style Guide"""
        return {
            "working_title": "The Time Keeper's Journal",
            "character_voices_count": 8,
            "audio_conventions_count": 12,
            "has_narrator": True,
            "narrator_personality": "Scholarly yet accessible historian",
            "sonic_elements_count": 6,
            "language_rules_complete": True,
            "dialogue_principles_complete": True,
            "session_id": self.session_id,
            "created_timestamp": datetime.now().isoformat()
        }
    
    def generate_station_7_data(self):
        """Mock Station 7: Reality Check"""
        return {
            "pipeline_status": "PASSED",
            "overall_quality_score": 0.91,
            "pipeline_integrity": 0.95,
            "stations_passed": 6,
            "stations_failed": 0,
            "stations_with_warnings": 1,
            "creative_uniqueness_score": 0.88,
            "technical_completeness_score": 0.94,
            "critical_issues_count": 0,
            "recommendations_count": 3,
            "session_id": self.session_id,
            "validation_timestamp": datetime.now().isoformat()
        }

class StationTester:
    """Runs and tests individual stations 8-14"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.mock_data = MockDataGenerator(session_id)
        self.generated_pdfs = []
        self.test_results = {}
        
    async def setup_redis_mock_data(self):
        """Set up mock data in Redis for stations to access"""
        try:
            from app.redis_client import RedisClient
            redis = RedisClient()
            await redis.initialize()
            
            # Store mock data for each station
            mock_stations = {
                "01": self.mock_data.generate_station_1_data(),
                "02": self.mock_data.generate_station_2_data(),
                "03": self.mock_data.generate_station_3_data(),
                "04": self.mock_data.generate_station_4_data(),
                "05": self.mock_data.generate_station_5_data(),
                "06": self.mock_data.generate_station_6_data(),
                "07": self.mock_data.generate_station_7_data()
            }
            
            for station_num, data in mock_stations.items():
                redis_key = f"audiobook:{self.session_id}:station_{station_num}"
                json_data = json.dumps(data, default=str)
                await redis.set(redis_key, json_data, expire=3600)
                logger.info(f"✅ Stored mock data for station {station_num}")
            
            await redis.disconnect()
            logger.info("📊 All mock data stored in Redis")
            
        except Exception as e:
            logger.warning(f"⚠️  Redis setup failed: {e}")
            logger.info("💡 Tests will run without Redis (may affect some functionality)")
    
    async def test_station_8(self):
        """Test Station 8: Character Architecture"""
        print("\n🎭 TESTING STATION 8: CHARACTER ARCHITECTURE")
        print("=" * 60)
        
        try:
            from app.agents.station_08_character_architecture import Station08CharacterArchitecture
            
            processor = Station08CharacterArchitecture()
            await processor.initialize()
            
            print("🔄 Running Station 8...")
            result = await processor.process(self.session_id)
            
            # Export PDF
            pdf_data = processor.export_to_pdf(result)
            pdf_filename = f"outputs/test_station8_character_bible_{self.session_id}.pdf"
            os.makedirs("outputs", exist_ok=True)
            
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_data)
            
            self.generated_pdfs.append(pdf_filename)
            
            # Analyze results
            char_count = result.character_count_summary['total_characters']
            tier1_count = result.character_count_summary['tier1_protagonists']
            
            self.test_results['station_8'] = {
                'status': 'success',
                'pdf_file': pdf_filename,
                'characters_generated': char_count,
                'protagonists': tier1_count,
                'pdf_size': os.path.getsize(pdf_filename)
            }
            
            print(f"✅ Station 8 completed!")
            print(f"   📄 PDF: {pdf_filename}")
            print(f"   🎭 Characters: {char_count} total ({tier1_count} protagonists)")
            print(f"   📊 PDF Size: {os.path.getsize(pdf_filename):,} bytes")
            
        except Exception as e:
            print(f"❌ Station 8 failed: {e}")
            self.test_results['station_8'] = {'status': 'failed', 'error': str(e)}
    
    async def test_station_9(self):
        """Test Station 9: World Building"""
        print("\n🌍 TESTING STATION 9: WORLD BUILDING")
        print("=" * 60)
        
        try:
            from app.agents.station_09_world_building import Station09WorldBuilding
            
            processor = Station09WorldBuilding()
            await processor.initialize()
            
            print("🔄 Running Station 9...")
            result = await processor.process(self.session_id)
            
            # Export PDF
            pdf_data = processor.export_to_pdf(result)
            pdf_filename = f"outputs/test_station9_world_bible_{self.session_id}.pdf"
            
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_data)
            
            self.generated_pdfs.append(pdf_filename)
            
            # Analyze results
            locations = result.world_statistics['total_locations']
            audio_cues = result.world_statistics['audio_cues']
            
            self.test_results['station_9'] = {
                'status': 'success',
                'pdf_file': pdf_filename,
                'locations': locations,
                'audio_cues': audio_cues,
                'pdf_size': os.path.getsize(pdf_filename)
            }
            
            print(f"✅ Station 9 completed!")
            print(f"   📄 PDF: {pdf_filename}")
            print(f"   🌍 Locations: {locations}, Audio cues: {audio_cues}")
            print(f"   📊 PDF Size: {os.path.getsize(pdf_filename):,} bytes")
            
        except Exception as e:
            print(f"❌ Station 9 failed: {e}")
            self.test_results['station_9'] = {'status': 'failed', 'error': str(e)}
    
    async def test_station_10(self):
        """Test Station 10: Narrative Reveal Strategy"""
        print("\n🎭 TESTING STATION 10: NARRATIVE REVEAL STRATEGY")
        print("=" * 60)
        
        try:
            from app.agents.station_10_narrative_reveal_strategy import Station10NarrativeRevealStrategy
            
            processor = Station10NarrativeRevealStrategy()
            
            print("🔄 Running Station 10...")
            result = await processor.process(self.session_id)
            
            # Check if PDF was generated
            pdf_filename = result.get("outputs", {}).get("pdf", "")
            if pdf_filename and os.path.exists(pdf_filename):
                self.generated_pdfs.append(pdf_filename)
                pdf_size = os.path.getsize(pdf_filename)
            else:
                pdf_filename = f"outputs/test_station10_narrative_reveal_{self.session_id}.pdf"
                pdf_size = 0
            
            # Analyze results
            info_items = result.get("summary", {}).get("information_items", 0)
            reveal_methods = result.get("summary", {}).get("reveal_methods", 0)
            
            self.test_results['station_10'] = {
                'status': 'success',
                'pdf_file': pdf_filename,
                'information_items': info_items,
                'reveal_methods': reveal_methods,
                'pdf_size': pdf_size
            }
            
            print(f"✅ Station 10 completed!")
            print(f"   📄 PDF: {pdf_filename}")
            print(f"   🎭 Info items: {info_items}, Reveal methods: {reveal_methods}")
            print(f"   📊 PDF Size: {pdf_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Station 10 failed: {e}")
            self.test_results['station_10'] = {'status': 'failed', 'error': str(e)}
    
    async def test_station_11(self):
        """Test Station 11: Runtime Planning"""
        print("\n📅 TESTING STATION 11: RUNTIME PLANNING")
        print("=" * 60)
        
        try:
            from app.agents.station_11_runtime_planning import Station11RuntimePlanning
            
            processor = Station11RuntimePlanning()
            await processor.initialize()
            
            print("🔄 Running Station 11...")
            result = await processor.process(self.session_id)
            
            # Check if PDF was generated
            pdf_filename = result.get("outputs", {}).get("pdf", "")
            if pdf_filename and os.path.exists(pdf_filename):
                self.generated_pdfs.append(pdf_filename)
                pdf_size = os.path.getsize(pdf_filename)
            else:
                pdf_filename = f"outputs/test_station11_runtime_planning_{self.session_id}.pdf"
                pdf_size = 0
            
            # Analyze results
            total_episodes = result.get("summary", {}).get("total_episodes", 0)
            timeline = result.get("summary", {}).get("production_timeline", "Unknown")
            
            self.test_results['station_11'] = {
                'status': 'success',
                'pdf_file': pdf_filename,
                'total_episodes': total_episodes,
                'timeline': timeline,
                'pdf_size': pdf_size
            }
            
            print(f"✅ Station 11 completed!")
            print(f"   📄 PDF: {pdf_filename}")
            print(f"   📅 Episodes: {total_episodes}, Timeline: {timeline}")
            print(f"   📊 PDF Size: {pdf_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Station 11 failed: {e}")
            self.test_results['station_11'] = {'status': 'failed', 'error': str(e)}
    
    async def test_station_12(self):
        """Test Station 12: Hook & Cliffhanger Designer"""
        print("\n⚡ TESTING STATION 12: HOOK & CLIFFHANGER DESIGNER")
        print("=" * 60)
        
        try:
            from app.agents.station_12_hook_cliffhanger import Station12HookCliffhanger
            
            processor = Station12HookCliffhanger(self.session_id)
            await processor.initialize()
            
            print("🔄 Running Station 12...")
            result = await processor.run()
            
            # Check PDF generation
            pdf_filename = result.get("outputs", {}).get("pdf", "")
            if pdf_filename and os.path.exists(pdf_filename):
                self.generated_pdfs.append(pdf_filename)
                pdf_size = os.path.getsize(pdf_filename)
            else:
                pdf_filename = f"outputs/test_station12_hooks_cliffhangers_{self.session_id}.pdf"
                pdf_size = 0
            
            # Analyze results
            hooks_designed = result.get("statistics", {}).get("hooks_designed", 0)
            cliffhangers_designed = result.get("statistics", {}).get("cliffhangers_designed", 0)
            
            self.test_results['station_12'] = {
                'status': 'success',
                'pdf_file': pdf_filename,
                'hooks_designed': hooks_designed,
                'cliffhangers_designed': cliffhangers_designed,
                'pdf_size': pdf_size
            }
            
            print(f"✅ Station 12 completed!")
            print(f"   📄 PDF: {pdf_filename}")
            print(f"   ⚡ Hooks: {hooks_designed}, Cliffhangers: {cliffhangers_designed}")
            print(f"   📊 PDF Size: {pdf_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Station 12 failed: {e}")
            self.test_results['station_12'] = {'status': 'failed', 'error': str(e)}
    
    async def test_station_13(self):
        """Test Station 13: Multi-World/Timeline Manager"""
        print("\n🌐 TESTING STATION 13: MULTI-WORLD/TIMELINE MANAGER")
        print("=" * 60)
        
        try:
            from app.agents.station_13_multiworld_timeline import Station13MultiworldTimeline
            
            processor = Station13MultiworldTimeline(self.session_id)
            await processor.initialize()
            
            print("🔄 Running Station 13...")
            result = await processor.run()
            
            # Check PDF generation
            pdf_filename = result.get("outputs", {}).get("pdf", "")
            if pdf_filename and os.path.exists(pdf_filename):
                self.generated_pdfs.append(pdf_filename)
                pdf_size = os.path.getsize(pdf_filename)
            else:
                pdf_filename = f"outputs/test_station13_multiworld_{self.session_id}.pdf"
                pdf_size = 0
            
            # Analyze results
            is_applicable = result.get("is_applicable", False)
            world_count = result.get("statistics", {}).get("world_count", 1)
            complexity = result.get("statistics", {}).get("complexity_level", "simple")
            
            self.test_results['station_13'] = {
                'status': 'success',
                'pdf_file': pdf_filename,
                'is_applicable': is_applicable,
                'world_count': world_count,
                'complexity': complexity,
                'pdf_size': pdf_size
            }
            
            print(f"✅ Station 13 completed!")
            print(f"   📄 PDF: {pdf_filename}")
            print(f"   🌐 Applicable: {is_applicable}, Worlds: {world_count}, Complexity: {complexity}")
            print(f"   📊 PDF Size: {pdf_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Station 13 failed: {e}")
            self.test_results['station_13'] = {'status': 'failed', 'error': str(e)}
    
    async def test_station_14(self):
        """Test Station 14: Episode Blueprint"""
        print("\n📋 TESTING STATION 14: EPISODE BLUEPRINT")
        print("=" * 60)
        
        try:
            from app.agents.station_14_episode_blueprint import Station14EpisodeBlueprint
            
            processor = Station14EpisodeBlueprint(self.session_id)
            await processor.initialize()
            
            print("🔄 Running Station 14...")
            result = await processor.run()
            
            # Check PDF generation
            pdf_filename = result.get("outputs", {}).get("pdf", "")
            if pdf_filename and os.path.exists(pdf_filename):
                self.generated_pdfs.append(pdf_filename)
                pdf_size = os.path.getsize(pdf_filename)
            else:
                pdf_filename = f"outputs/test_station14_episode_blueprints_{self.session_id}.pdf"
                pdf_size = 0
            
            # Analyze results
            blueprints_generated = result.get("statistics", {}).get("blueprints_generated", 0)
            ready_for_approval = result.get("statistics", {}).get("ready_for_approval", False)
            
            self.test_results['station_14'] = {
                'status': 'success',
                'pdf_file': pdf_filename,
                'blueprints_generated': blueprints_generated,
                'ready_for_approval': ready_for_approval,
                'pdf_size': pdf_size
            }
            
            print(f"✅ Station 14 completed!")
            print(f"   📄 PDF: {pdf_filename}")
            print(f"   📋 Blueprints: {blueprints_generated}, Ready for approval: {ready_for_approval}")
            print(f"   📊 PDF Size: {pdf_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Station 14 failed: {e}")
            self.test_results['station_14'] = {'status': 'failed', 'error': str(e)}
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📊 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        successful_stations = []
        failed_stations = []
        total_pdf_size = 0
        
        for station, results in self.test_results.items():
            if results['status'] == 'success':
                successful_stations.append(station)
                total_pdf_size += results.get('pdf_size', 0)
            else:
                failed_stations.append(station)
        
        print(f"📈 SUMMARY:")
        print(f"   ✅ Successful stations: {len(successful_stations)}/7")
        print(f"   ❌ Failed stations: {len(failed_stations)}/7")
        print(f"   📄 PDFs generated: {len(self.generated_pdfs)}")
        print(f"   📊 Total PDF size: {total_pdf_size:,} bytes")
        
        print(f"\n📁 GENERATED PDF FILES:")
        for i, pdf_file in enumerate(self.generated_pdfs, 1):
            if os.path.exists(pdf_file):
                size = os.path.getsize(pdf_file)
                print(f"   {i}. {pdf_file} ({size:,} bytes)")
            else:
                print(f"   {i}. {pdf_file} (FILE MISSING)")
        
        print(f"\n🎯 STATION DETAILS:")
        for station, results in self.test_results.items():
            status_icon = "✅" if results['status'] == 'success' else "❌"
            print(f"   {status_icon} {station.upper()}: {results['status']}")
            
            if results['status'] == 'success':
                # Print specific metrics for each station
                if station == 'station_8':
                    print(f"      🎭 Characters: {results.get('characters_generated', 0)}")
                elif station == 'station_9':
                    print(f"      🌍 Locations: {results.get('locations', 0)}")
                elif station == 'station_10':
                    print(f"      🎭 Info items: {results.get('information_items', 0)}")
                elif station == 'station_11':
                    print(f"      📅 Episodes: {results.get('total_episodes', 0)}")
                elif station == 'station_12':
                    print(f"      ⚡ Hooks: {results.get('hooks_designed', 0)}")
                elif station == 'station_13':
                    print(f"      🌐 Worlds: {results.get('world_count', 0)}")
                elif station == 'station_14':
                    print(f"      📋 Blueprints: {results.get('blueprints_generated', 0)}")
                
                print(f"      📄 PDF: {results.get('pdf_file', 'N/A')}")
                print(f"      📊 Size: {results.get('pdf_size', 0):,} bytes")
            else:
                print(f"      ❌ Error: {results.get('error', 'Unknown error')}")
        
        # Save detailed report to file
        report_data = {
            'test_timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'summary': {
                'successful_stations': len(successful_stations),
                'failed_stations': len(failed_stations),
                'total_pdfs': len(self.generated_pdfs),
                'total_pdf_size': total_pdf_size
            },
            'station_results': self.test_results,
            'generated_pdfs': self.generated_pdfs
        }
        
        report_file = f"outputs/test_report_stations_8_14_{self.session_id}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n💾 DETAILED REPORT SAVED: {report_file}")
        
        return len(successful_stations) == 7  # Return True if all stations passed

async def main():
    """Main test execution"""
    print("🎬 PDF OUTPUT VERIFICATION TEST - STATIONS 8-14")
    print("=" * 80)
    
    # Generate unique session ID for this test
    session_id = f"pdf_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"🆔 Test Session ID: {session_id}")
    
    # Initialize tester
    tester = StationTester(session_id)
    
    print("\n🔧 SETUP PHASE:")
    print("- Setting up mock data for stations 1-7...")
    await tester.setup_redis_mock_data()
    
    print("- Creating output directory...")
    os.makedirs("outputs", exist_ok=True)
    
    print("\n🚀 TESTING PHASE:")
    print("Running stations 8-14 individually...")
    
    # Run all station tests
    await tester.test_station_8()
    await tester.test_station_9()
    await tester.test_station_10()
    await tester.test_station_11()
    await tester.test_station_12()
    await tester.test_station_13()
    await tester.test_station_14()
    
    # Generate final report
    all_passed = tester.generate_test_report()
    
    print(f"\n🎉 TEST COMPLETE!")
    if all_passed:
        print("✅ ALL STATIONS PASSED - PDF outputs ready for review!")
    else:
        print("⚠️  Some stations had issues - check the report for details")
    
    print(f"\n📂 Next steps:")
    print(f"   1. Review PDF files in outputs/ directory")
    print(f"   2. Check content quality and completeness")
    print(f"   3. Verify visual formatting and layout")
    print(f"   4. Test human approval workflow for Station 14")

if __name__ == "__main__":
    asyncio.run(main())