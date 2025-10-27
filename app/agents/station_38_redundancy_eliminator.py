"""
Station 38: Redundancy Eliminator

This station identifies and eliminates redundancy across dialogue, sound effects, scenes, and overall word count,
streamlining scripts for production-readiness while maintaining story integrity.

Flow:
1. Load Station 27 master scripts
2. Execute 4-task redundancy elimination:
   - Task 1: Dialogue Redundancy (repeated info, phrases, conflicts, reactions)
   - Task 2: Sound Redundancy (narrator/sound overlap, overused SFX/music)
   - Task 3: Scene Redundancy (similar scenes, beats, transitions)
   - Task 4: Word Count Optimization (trimming, combining, efficiency)
3. Generate comprehensive redundancy report with cut lists
4. Save JSON + Markdown outputs
5. Require user approval before applying changes

Critical Implementation Rules:
- Identify repeated information without loss of clarity
- Cut weakest instances, keep strongest
- Vary repeated phrases while preserving character voice
- Combine similar scenes for efficiency
- Trim unnecessary words without losing meaning
"""

import asyncio
import json
import logging
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Station38RedundancyEliminator:
    """Station 38: Redundancy Eliminator"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=38)
        
        # Load additional config from YAML
        self._load_additional_config()
        
        self.output_dir = Path("output/station_38")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_additional_config(self):
        """Load additional configuration from YAML file"""
        config_dir = Path(__file__).parent / 'configs'
        config_path = config_dir / 'station_38.yml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = yaml.safe_load(f)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 38 initialized")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("✂️  STATION 38: REDUNDANCY ELIMINATOR")
        print("=" * 70)
        print()

        try:
            # Step 1: Load required inputs
            print("📥 Loading required inputs...")
            station27_data = await self.load_station27_data()
            
            print("✅ All inputs loaded successfully")
            episodes = station27_data.get('episodes', {})
            print(f"   ✓ Station 27: {len(episodes)} master scripts")
            print()

            # Step 2: Display project summary
            self.display_project_summary(station27_data)

            # Step 3: Process all episodes
            if not episodes:
                raise ValueError("❌ No episodes found in Station 27 data. Cannot proceed.")

            print(f"📊 Processing {len(episodes)} episodes for redundancy elimination...")
            print()

            all_episode_results = []

            # Task 1: Dialogue Redundancy
            print("\n" + "=" * 70)
            print("💬 TASK 1: DIALOGUE REDUNDANCY")
            print("=" * 70)
            print("Identifying repeated information, phrases, conflicts, and reactions...")
            
            dialogue_redundancy = await self.execute_task1_dialogue_redundancy(station27_data)
            
            repeated_info = dialogue_redundancy.get('repeated_information', [])
            repeated_phrases = dialogue_redundancy.get('repeated_phrases', [])
            repeated_conflicts = dialogue_redundancy.get('repeated_conflicts', [])
            repeated_reactions = dialogue_redundancy.get('repeated_reactions', [])
            
            print(f"✅ Found {len(repeated_info)} instances of repeated information")
            print(f"   Found {len(repeated_phrases)} overused phrases")
            print(f"   Found {len(repeated_conflicts)} repetitive conflicts")
            print(f"   Found {len(repeated_reactions)} repeated reactions")

            # Task 2: Sound Redundancy
            print("\n" + "=" * 70)
            print("🔊 TASK 2: SOUND REDUNDANCY")
            print("=" * 70)
            print("Identifying narrator/description overlap and overused sounds...")
            
            sound_redundancy = await self.execute_task2_sound_redundancy(station27_data)
            
            narrator_overlap = sound_redundancy.get('narrator_overlap', [])
            dialogue_sound_overlap = sound_redundancy.get('dialogue_sound_overlap', [])
            overused_sfx = sound_redundancy.get('overused_sfx', [])
            overused_music = sound_redundancy.get('overused_music', [])
            
            print(f"✅ Found {len(narrator_overlap)} narrator/description overlaps")
            print(f"   Found {len(dialogue_sound_overlap)} dialogue/sound overlaps")
            print(f"   Found {len(overused_sfx)} overused sound effects")
            print(f"   Found {len(overused_music)} overused music cues")

            # Task 3: Scene Redundancy
            print("\n" + "=" * 70)
            print("🎬 TASK 3: SCENE REDUNDANCY")
            print("=" * 70)
            print("Identifying similar scenes, beats, and transitions...")
            
            scene_redundancy = await self.execute_task3_scene_redundancy(station27_data)
            
            similar_scenes = scene_redundancy.get('similar_scenes', [])
            similar_beats = scene_redundancy.get('similar_beats', [])
            similar_transitions = scene_redundancy.get('similar_transitions', [])
            
            print(f"✅ Found {len(similar_scenes)} similar scenes to combine/cut")
            print(f"   Found {len(similar_beats)} repetitive story beats")
            print(f"   Found {len(similar_transitions)} repetitive transitions")

            # Task 4: Word Count Optimization
            print("\n" + "=" * 70)
            print("✍️  TASK 4: WORD COUNT OPTIMIZATION")
            print("=" * 70)
            print("Generating optimization recommendations...")
            
            optimization = await self.execute_task4_word_count_optimization(
                station27_data, dialogue_redundancy, sound_redundancy, scene_redundancy
            )
            
            print(f"✅ Optimization complete")
            current_count = optimization.get('current_word_count', 0)
            target_count = optimization.get('target_word_count', 0)
            savings = optimization.get('estimated_savings', 0)
            
            print(f"   Current word count: {current_count:,}")
            print(f"   Target word count: {target_count:,}")
            print(f"   Estimated savings: {savings:,} words")

            # Compile complete redundancy data
            redundancy_data = {
                'session_id': self.session_id,
                'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
                'dialogue_redundancy': dialogue_redundancy,
                'sound_redundancy': sound_redundancy,
                'scene_redundancy': scene_redundancy,
                'optimization': optimization,
                'overall_assessment': await self.generate_overall_assessment(
                    dialogue_redundancy, sound_redundancy, scene_redundancy, optimization
                )
            }

            # Step 4: Generate output files
            print("\n" + "=" * 70)
            print("💾 GENERATING OUTPUT FILES")
            print("=" * 70)
            
            await self.generate_output_files(redundancy_data, station27_data)
            print(f"✅ All output files generated in: {self.output_dir}/")

            # Step 5: Display critical issues
            self.display_critical_issues(redundancy_data)

            # Step 6: User validation prompt
            print("\n" + "=" * 70)
            print("🔍 USER VALIDATION REQUIRED")
            print("=" * 70)
            
            total_redundancies = (
                len(repeated_info) + len(repeated_phrases) + len(repeated_conflicts) + len(repeated_reactions) +
                len(narrator_overlap) + len(dialogue_sound_overlap) + len(overused_sfx) + len(overused_music) +
                len(similar_scenes) + len(similar_beats) + len(similar_transitions)
            )
            
            if total_redundancies > 0:
                print(f"⚠️  Found {total_redundancies} redundancies to eliminate")
                print("   Review detailed report and approve changes before proceeding.")
            else:
                print("✅ No redundancies found! Script is streamlined.")
            
            print(f"\n📁 Output files saved to: {self.output_dir}")
            print("✅ Station 38 complete!")

        except Exception as e:
            logger.error(f"Error in Station 38: {str(e)}", exc_info=True)
            raise

    async def load_station27_data(self) -> Dict[str, Any]:
        """Load Station 27 master scripts"""
        try:
            station_27_dir = Path("output/station_27")
            episodes = {}
            
            if not station_27_dir.exists():
                raise ValueError(f"Station 27 output directory not found")
            
            episode_dirs = sorted([d for d in station_27_dir.iterdir() 
                                  if d.is_dir() and d.name.startswith("episode_")])
            
            if not episode_dirs:
                raise ValueError(f"No episode data found in Station 27 output")
            
            for episode_dir in episode_dirs:
                episode_num = episode_dir.name.replace("episode_", "")
                master_file = episode_dir / f"{episode_dir.name}_MASTER.json"
                
                if master_file.exists():
                    with open(master_file, 'r', encoding='utf-8') as f:
                        episode_data = json.load(f)
                        
                        if episode_data.get('session_id') == self.session_id:
                            episodes[f"episode_{episode_num}"] = episode_data
            
            if not episodes:
                raise ValueError(f"""
❌ No Station 27 data found for session: '{self.session_id}'

REQUIRED: Station 38 depends on Station 27 (Master Script Assembly)

SOLUTIONS:
1. Run Station 27 first to generate script data
2. Check that session_id matches in the output files
""")
            
            return {
                'working_title': episodes.get('episode_01', {}).get('production_package', {}).get('title', 'Unknown'),
                'episodes': episodes
            }
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error loading Station 27 data: {str(e)}")
            raise

    def display_project_summary(self, station27_data: Dict[str, Any]):
        """Display project summary"""
        print("📊 PROJECT SUMMARY")
        print("-" * 60)
        
        working_title = station27_data.get('working_title', 'Unknown Project')
        episodes = station27_data.get('episodes', {})
        
        print(f"   Project: {working_title}")
        print(f"   Episodes: {len(episodes)}")
        print()

    async def execute_task1_dialogue_redundancy(self, station27_data: Dict[str, Any]) -> Dict[str, Any]:
        """Task 1: Identify dialogue redundancy"""
        
        episodes = station27_data.get('episodes', {})
        
        # Collect all episode scripts
        episodes_content = {}
        for episode_id, episode_data in episodes.items():
            master_assembly = episode_data.get('master_script_assembly', {})
            script_content = master_assembly.get('master_script_text', '')
            
            if not script_content:
                script_content = episode_data.get('script', episode_data.get('master_script_text', ''))
            
            episodes_content[episode_id] = script_content
        
        prompt = self.config_data['prompts']['dialogue_redundancy'].format(
            episodes_content=json.dumps(episodes_content, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('dialogue_redundancy', {})

    async def execute_task2_sound_redundancy(self, station27_data: Dict[str, Any]) -> Dict[str, Any]:
        """Task 2: Identify sound redundancy"""
        
        episodes = station27_data.get('episodes', {})
        episodes_content = {}
        
        for episode_id, episode_data in episodes.items():
            master_assembly = episode_data.get('master_script_assembly', {})
            script_content = master_assembly.get('master_script_text', '')
            
            if not script_content:
                script_content = episode_data.get('script', episode_data.get('master_script_text', ''))
            
            episodes_content[episode_id] = script_content
        
        prompt = self.config_data['prompts']['sound_redundancy'].format(
            episodes_content=json.dumps(episodes_content, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('sound_redundancy', {})

    async def execute_task3_scene_redundancy(self, station27_data: Dict[str, Any]) -> Dict[str, Any]:
        """Task 3: Identify scene redundancy"""
        
        episodes = station27_data.get('episodes', {})
        episodes_content = {}
        
        for episode_id, episode_data in episodes.items():
            master_assembly = episode_data.get('master_script_assembly', {})
            script_content = master_assembly.get('master_script_text', '')
            
            if not script_content:
                script_content = episode_data.get('script', episode_data.get('master_script_text', ''))
            
            episodes_content[episode_id] = script_content
        
        prompt = self.config_data['prompts']['scene_redundancy'].format(
            episodes_content=json.dumps(episodes_content, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('scene_redundancy', {})

    async def execute_task4_word_count_optimization(self, station27_data: Dict[str, Any],
                                                     dialogue_redundancy: Dict[str, Any],
                                                     sound_redundancy: Dict[str, Any],
                                                     scene_redundancy: Dict[str, Any]) -> Dict[str, Any]:
        """Task 4: Word count optimization"""
        
        prompt = self.config_data['prompts']['word_count_optimization'].format(
            dialogue_redundancy=json.dumps(dialogue_redundancy, indent=2),
            sound_redundancy=json.dumps(sound_redundancy, indent=2),
            scene_redundancy=json.dumps(scene_redundancy, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('optimization', {})

    async def generate_overall_assessment(self, dialogue_redundancy: Dict[str, Any],
                                         sound_redundancy: Dict[str, Any],
                                         scene_redundancy: Dict[str, Any],
                                         optimization: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall assessment"""
        
        prompt = self.config_data['prompts']['overall_assessment'].format(
            dialogue_redundancy=json.dumps(dialogue_redundancy, indent=2),
            sound_redundancy=json.dumps(sound_redundancy, indent=2),
            scene_redundancy=json.dumps(scene_redundancy, indent=2),
            optimization=json.dumps(optimization, indent=2)
        )
        
        response = await self.openrouter.generate(
            prompt,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        result = extract_json(response)
        return result.get('overall_assessment', {})

    async def generate_output_files(self, redundancy_data: Dict[str, Any], 
                                   station27_data: Dict[str, Any]):
        """Generate all output files"""
        
        output_basename = f"session_{self.session_id}_redundancy"
        
        # Save complete redundancy JSON
        redundancy_file = self.output_dir / f"{output_basename}_full.json"
        with open(redundancy_file, 'w', encoding='utf-8') as f:
            json.dump(redundancy_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ {redundancy_file}")
        
        # Save cut list
        cut_list = {
            'dialogue_cuts': redundancy_data.get('dialogue_redundancy', {}),
            'sound_cuts': redundancy_data.get('sound_redundancy', {}),
            'scene_cuts': redundancy_data.get('scene_redundancy', {}),
            'optimization': redundancy_data.get('optimization', {})
        }
        cut_list_file = self.output_dir / f"{output_basename}_cut_list.json"
        with open(cut_list_file, 'w', encoding='utf-8') as f:
            json.dump(cut_list, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ {cut_list_file}")
        
        # Save markdown summary
        summary_file = self.output_dir / f"{output_basename}_summary.md"
        self.save_summary_markdown(summary_file, redundancy_data)
        
        print(f"   ✓ {summary_file}")

    def save_summary_markdown(self, filepath: Path, redundancy_data: Dict[str, Any]):
        """Save summary report as markdown"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Redundancy Elimination Report\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall assessment
            overall = redundancy_data.get('overall_assessment', {})
            if overall:
                f.write("## Overall Assessment\n\n")
                f.write(overall.get('summary_text', 'No summary available') + "\n\n")
                
                scores = overall.get('scores', {})
                if scores:
                    f.write("### Redundancy Scores\n\n")
                    f.write(f"- Dialogue Redundancy: {scores.get('dialogue_score', 'N/A')}/100\n")
                    f.write(f"- Sound Redundancy: {scores.get('sound_score', 'N/A')}/100\n")
                    f.write(f"- Scene Redundancy: {scores.get('scene_score', 'N/A')}/100\n")
                    f.write(f"- Word Count Efficiency: {scores.get('efficiency_score', 'N/A')}/100\n\n")
            
            # Dialogue redundancy summary
            dialogue = redundancy_data.get('dialogue_redundancy', {})
            if dialogue:
                f.write("## Dialogue Redundancy\n\n")
                f.write(f"- Repeated information: {len(dialogue.get('repeated_information', []))}\n")
                f.write(f"- Repeated phrases: {len(dialogue.get('repeated_phrases', []))}\n")
                f.write(f"- Repeated conflicts: {len(dialogue.get('repeated_conflicts', []))}\n")
                f.write(f"- Repeated reactions: {len(dialogue.get('repeated_reactions', []))}\n\n")
            
            # Sound redundancy summary
            sound = redundancy_data.get('sound_redundancy', {})
            if sound:
                f.write("## Sound Redundancy\n\n")
                f.write(f"- Narrator/sound overlaps: {len(sound.get('narrator_overlap', []))}\n")
                f.write(f"- Dialogue/sound overlaps: {len(sound.get('dialogue_sound_overlap', []))}\n")
                f.write(f"- Overused SFX: {len(sound.get('overused_sfx', []))}\n")
                f.write(f"- Overused music: {len(sound.get('overused_music', []))}\n\n")
            
            # Scene redundancy summary
            scene = redundancy_data.get('scene_redundancy', {})
            if scene:
                f.write("## Scene Redundancy\n\n")
                f.write(f"- Similar scenes to combine: {len(scene.get('similar_scenes', []))}\n")
                f.write(f"- Repetitive beats: {len(scene.get('similar_beats', []))}\n")
                f.write(f"- Repetitive transitions: {len(scene.get('similar_transitions', []))}\n\n")
            
            # Optimization summary
            optimization = redundancy_data.get('optimization', {})
            if optimization:
                f.write("## Word Count Optimization\n\n")
                current = optimization.get('current_word_count', 0)
                target = optimization.get('target_word_count', 0)
                savings = optimization.get('estimated_savings', 0)
                
                f.write(f"- Current word count: {current:,}\n")
                f.write(f"- Target word count: {target:,}\n")
                f.write(f"- Estimated savings: {savings:,} words\n\n")
            
            f.write("---\n\n")
            f.write("*Generated by Station 38: Redundancy Eliminator*\n")

    def display_critical_issues(self, redundancy_data: Dict[str, Any]):
        """Display critical issues"""
        dialogue = redundancy_data.get('dialogue_redundancy', {})
        sound = redundancy_data.get('sound_redundancy', {})
        scene = redundancy_data.get('scene_redundancy', {})
        optimization = redundancy_data.get('optimization', {})
        
        total_cuts = (
            len(dialogue.get('repeated_information', [])) +
            len(dialogue.get('repeated_phrases', [])) +
            len(sound.get('narrator_overlap', [])) +
            len(scene.get('similar_scenes', []))
        )
        
        print("\n" + "=" * 70)
        print("📊 REDUNDANCY SUMMARY")
        print("=" * 70)
        
        if total_cuts > 0:
            print(f"\n⚠️  Found {total_cuts} redundancies to eliminate")
            print("\nTop recommendations:")
            
            # Show top 5 from each category
            if dialogue.get('repeated_information'):
                for item in dialogue.get('repeated_information', [])[:3]:
                    print(f"   - Repeated info: {item.get('description', 'N/A')[:50]}...")
            
            if dialogue.get('repeated_phrases'):
                for item in dialogue.get('repeated_phrases', [])[:3]:
                    print(f"   - Overused phrase: {item.get('phrase', 'N/A')[:50]}...")
            
            if sound.get('narrator_overlap'):
                for item in sound.get('narrator_overlap', [])[:3]:
                    print(f"   - Narrator/sound overlap: {item.get('issue', 'N/A')[:50]}...")
            
            if scene.get('similar_scenes'):
                for item in scene.get('similar_scenes', [])[:3]:
                    print(f"   - Similar scenes: {item.get('description', 'N/A')[:50]}...")
        else:
            print("\n✅ No redundancies found! Script is clean.")
        
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
    else:
        print("\n" + "="*70)
        print("✂️  STATION 38: REDUNDANCY ELIMINATOR")
        print("="*70)
        print()
        print("Please enter the session ID to process:")
        print("(Default: session_20251023_112749)")
        session_input = input("Session ID: ").strip()
        session_id = session_input if session_input else "session_20251023_112749"
        print()
    
    async def main():
        station = Station38RedundancyEliminator(session_id=session_id)
        await station.initialize()
        await station.run()
    
    asyncio.run(main())

