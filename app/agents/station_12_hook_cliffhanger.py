"""
Station 12: Hook & Cliffhanger Designer Agent

This agent takes season architecture and character data to create compelling
engagement strategies for each episode including opening hooks, act turns,
and cliffhangers.

Dependencies: Season Architecture (Station 5), Character Bible (Station 8)
Outputs: Hook & cliffhanger strategy per episode
Human Gate: None - feeds into Station 14 for human review
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

@dataclass
class OpeningHook:
    """Data structure for episode opening hook"""
    hook_type: str  # mystery, action, emotion, revelation, conflict, question
    audio_strategy: str  # first sounds, build sequence, voice entry
    character_moment: str  # who speaks first and why
    question_raised: str  # what mystery/problem presented
    tone_setting: str  # emotional temperature and pace
    production_notes: str  # sound design recommendations

@dataclass
class ActTurn:
    """Data structure for act turn point"""
    story_beat: str  # what changes or is revealed
    character_decision: str  # decision point made
    stakes_shift: str  # how tension changes
    audio_signature: str  # distinctive sound marking this moment
    emotional_shift: str  # emotional temperature change

@dataclass
class CliffhangerStrategy:
    """Data structure for episode cliffhanger"""
    cliffhanger_type: str  # from catalog
    intensity_rating: int  # 1-10 scale
    unanswered_question: str  # what question left hanging
    audio_execution: str  # how to cut/end episode
    emotional_state: str  # emotion to leave listener with
    connection_setup: str  # setup for next episode

@dataclass
class EpisodeBridge:
    """Data structure for episode-to-episode bridge"""
    continuity_elements: List[str]  # audio elements that carry forward
    time_gap_handling: str  # how time passage conveyed
    tension_maintenance: str  # how urgency kept across gap
    audio_transition: str  # sound design recommendations

@dataclass
class TensionPoint:
    """Data structure for tension curve point"""
    timestamp: str  # time in episode
    tension_level: int  # 1-10 rating
    reason: str  # why this rating
    emotional_state: str  # audience emotion
    audio_intensity: str  # recommended audio approach

class Station12HookCliffhanger:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_12_hook_cliffhanger"
        
        # Cliffhanger types catalog
        self.cliffhanger_types = [
            "Question", "Danger", "Revelation", "Choice", "Arrival",
            "Betrayal", "Loss", "Discovery", "Transformation", "Time"
        ]
        
    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()
        
    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from previous stations"""
        dependencies = {}
        
        # Load season_architecture (Station 5)
        season_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_5")
        if season_raw:
            dependencies['season_architecture'] = json.loads(season_raw)
            
        # Load character_bible (Station 8)  
        character_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_8")
        if character_raw:
            dependencies['character_bible'] = json.loads(character_raw)
            
        # Load world_bible (Station 9) - optional but helpful
        world_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_9")
        if world_raw:
            dependencies['world_bible'] = json.loads(world_raw)
            
        return dependencies
        
    async def generate_opening_hook(self, episode_num: int, episode_context: Dict, dependencies: Dict) -> Dict[str, Any]:
        """Generate 60-second opening hook for episode using LLM"""
        
        characters_summary = ""
        if dependencies.get('character_bible'):
            char_data = dependencies['character_bible']
            main_chars = char_data.get('tier1_protagonists', [])[:3]  # Top 3 characters
            characters_summary = json.dumps(main_chars, indent=2)[:1000]
        
        world_summary = ""
        if dependencies.get('world_bible'):
            world_data = dependencies['world_bible']
            locations = world_data.get('geography', {}).get('locations', [])[:3]
            world_summary = json.dumps(locations, indent=2)[:1000]
        
        prompt = f"""
You are designing the OPENING HOOK for Episode {episode_num} of an audio drama.

EPISODE CONTEXT:
{json.dumps(episode_context, indent=2)}

CHARACTERS AVAILABLE:
{characters_summary}

WORLD SETTING:
{world_summary}

Design a compelling OPENING HOOK (first 60 seconds) that:

1. HOOK TYPE: Choose from (mystery, action, emotion, revelation, conflict, question)
2. AUDIO STRATEGY:
   - First sound listener hears (within 3 seconds)
   - Sound sequence that builds tension
   - When first voice enters
   - Audio environment setup
3. CHARACTER MOMENT:
   - Who speaks first (and why this character)
   - What they say/do in opening moment
   - Emotional state
4. QUESTION RAISED:
   - What mystery/problem is immediately presented
   - Why listener must keep listening
5. TONE SETTING:
   - Emotional temperature (tense, excited, mysterious, etc.)
   - Pace (fast/slow)
   - Genre signals
6. PRODUCTION NOTES:
   - Sound design recommendations
   - Music/ambience cues
   - Mixing notes for maximum impact

Generate detailed, production-ready opening hook strategy as JSON.
Make it IMMEDIATELY engaging and audio-focused.

Expected JSON format:
{{
  "hook_type": "mystery",
  "audio_strategy": "detailed audio approach",
  "character_moment": "who speaks and what they do",
  "question_raised": "compelling question",
  "tone_setting": "emotional temperature and pace",
  "production_notes": "sound design guidance"
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {
            "hook_type": "mystery",
            "audio_strategy": "TBD",
            "character_moment": "TBD", 
            "question_raised": "TBD",
            "tone_setting": "TBD",
            "production_notes": "TBD"
        })
        
    async def generate_act_turns(self, episode_num: int, episode_context: Dict, dependencies: Dict) -> Dict[str, Any]:
        """Generate three act turn points for episode"""
        
        characters_summary = ""
        if dependencies.get('character_bible'):
            char_data = dependencies['character_bible']
            main_chars = char_data.get('tier1_protagonists', [])[:3]
            characters_summary = json.dumps(main_chars, indent=2)[:1000]
        
        prompt = f"""
You are designing the THREE ACT TURNS for Episode {episode_num} of an audio drama.

EPISODE CONTEXT:
{json.dumps(episode_context, indent=2)}

CHARACTERS:
{characters_summary}

Design THREE ACT TURNS:

ACT 1 TURN (around 25% of episode - approximately minute 7-10 for 30min episode):
1. What changes or is revealed
2. Character decision point (what choice is made)
3. How stakes shift
4. Audio signature (distinctive sound that marks this moment)
5. Emotional shift

ACT 2 TURN / MIDPOINT (around 50% - approximately minute 15 for 30min episode):
1. Major shift or revelation (this should be BIG)
2. Stakes escalation (how tension increases)
3. Point of no return indicator
4. How it sounds different from Act 1
5. Character transformation moment

ACT 3 TURN (around 75% - approximately minute 22-23 for 30min episode):
1. Final point of no return
2. Character commitment (all-in moment)
3. Sound design climax (audio intensity peak)
4. Setup for cliffhanger
5. Emotional peak

For each turn provide:
- Exact story beat
- Character involved
- Audio execution strategy
- Why this moment matters
- Connection to overall arc

Generate as detailed JSON structure.
Make each turn DISTINCTIVE and IMPACTFUL in audio format.

Expected JSON format:
{{
  "act1_turn": {{
    "story_beat": "what changes",
    "character_decision": "choice made",
    "stakes_shift": "how tension changes",
    "audio_signature": "distinctive sound",
    "emotional_shift": "emotional change"
  }},
  "act2_turn": {{ ... }},
  "act3_turn": {{ ... }}
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {
            "act1_turn": {"story_beat": "TBD", "character_decision": "TBD", "stakes_shift": "TBD", "audio_signature": "TBD", "emotional_shift": "TBD"},
            "act2_turn": {"story_beat": "TBD", "character_decision": "TBD", "stakes_shift": "TBD", "audio_signature": "TBD", "emotional_shift": "TBD"},
            "act3_turn": {"story_beat": "TBD", "character_decision": "TBD", "stakes_shift": "TBD", "audio_signature": "TBD", "emotional_shift": "TBD"}
        })
        
    async def generate_cliffhanger(self, episode_num: int, episode_context: Dict, dependencies: Dict, next_episode_hint: str = None) -> Dict[str, Any]:
        """Generate cliffhanger strategy for episode ending"""
        
        prompt = f"""
You are designing the CLIFFHANGER ENDING for Episode {episode_num} of an audio drama.

EPISODE CONTEXT:
{json.dumps(episode_context, indent=2)}

NEXT EPISODE HINT:
{next_episode_hint or "Final episode or continuation TBD"}

CLIFFHANGER TYPES AVAILABLE:
- Question: Pose urgent unanswered question
- Danger: Character in immediate peril
- Revelation: Shocking truth revealed at end
- Choice: Character must make crucial decision (show setup, not resolution)
- Arrival: New character or threat appears
- Betrayal: Trust is shattered
- Loss: Something precious is taken/lost
- Discovery: Find something game-changing
- Transformation: Character fundamentally changed
- Time: Deadline reached or approaching

Design the CLIFFHANGER:

1. CLIFFHANGER TYPE: Choose from list above (pick the MOST effective for this episode)
2. INTENSITY RATING: Rate 1-10 (how urgent/compelling is it)
3. UNANSWERED QUESTION: What specific question is left hanging
4. AUDIO EXECUTION:
   - Last sounds listener hears
   - How to cut the episode (abrupt, fade, sound effect, etc.)
   - Music strategy
   - Silence usage
5. EMOTIONAL STATE: What emotion to leave listener with
6. CONNECTION TO NEXT:
   - Setup for next episode opening
   - Thread that carries forward
   - Audio element that will return
7. PRODUCTION NOTES:
   - Exact timing recommendations
   - Sound design for maximum impact
   - Voice direction for final lines

Generate detailed cliffhanger strategy as JSON.
Make it IMPOSSIBLE to not continue to next episode.

Expected JSON format:
{{
  "type": "Danger",
  "intensity": 8,
  "unanswered_question": "specific question",
  "audio_execution": "how to end",
  "emotional_state": "emotion to leave",
  "connection_setup": "next episode setup",
  "production_notes": "detailed guidance"
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {
            "type": "Question",
            "intensity": 7,
            "unanswered_question": "TBD",
            "audio_execution": "TBD",
            "emotional_state": "TBD", 
            "connection_setup": "TBD",
            "production_notes": "TBD"
        })
        
    async def generate_episode_bridge(self, episode_num: int, this_episode: Dict, next_episode: Dict) -> Dict[str, Any]:
        """Generate bridge strategy between consecutive episodes"""
        
        prompt = f"""
Design the BRIDGE between Episode {episode_num} and Episode {episode_num + 1}.

THIS EPISODE ENDING:
{json.dumps(this_episode.get('cliffhanger', {}), indent=2)}

NEXT EPISODE OPENING:
{json.dumps(next_episode.get('opening_hook', {}), indent=2) if next_episode else "Series finale"}

Create EPISODE BRIDGE strategy:

1. CONTINUITY ELEMENTS:
   - Audio element that carries from end to beginning
   - Character thread continuation
   - Sound motif that repeats
2. TIME GAP HANDLING:
   - How much time passes between episodes
   - How to convey time passage in audio
3. TENSION MAINTENANCE:
   - How to keep urgency across episode gap
   - What question remains central
4. LISTENER EXPERIENCE:
   - Recap strategy (if any)
   - Cold open vs continuation
   - Re-engagement technique
5. AUDIO TRANSITION:
   - Recommended sound design
   - Music continuity
   - Voice-over strategy (if applicable)

Generate as JSON structure with clear production guidance.

Expected JSON format:
{{
  "continuity_elements": ["audio element 1", "element 2"],
  "time_gap_handling": "how time passage shown",
  "tension_maintenance": "how urgency kept",
  "listener_experience": "engagement strategy",
  "audio_transition": "sound design notes"
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {
            "continuity_elements": [],
            "time_gap_handling": "TBD",
            "tension_maintenance": "TBD",
            "listener_experience": "TBD",
            "audio_transition": "TBD"
        })
        
    async def generate_tension_curve(self, episode_data: Dict) -> List[Dict[str, Any]]:
        """Generate tension mapping across episode (1-10 scale at key points)"""
        
        prompt = f"""
Map the TENSION CURVE for this episode at key timestamps.

EPISODE DATA:
- Opening Hook: {episode_data.get('opening_hook', {}).get('hook_type', 'N/A')}
- Act 1 Turn: {str(episode_data.get('act_turns', {}).get('act1_turn', {}).get('story_beat', 'N/A'))[:200]}
- Act 2 Turn: {str(episode_data.get('act_turns', {}).get('act2_turn', {}).get('story_beat', 'N/A'))[:200]}
- Act 3 Turn: {str(episode_data.get('act_turns', {}).get('act3_turn', {}).get('story_beat', 'N/A'))[:200]}
- Cliffhanger: {episode_data.get('cliffhanger', {}).get('type', 'N/A')}

Rate tension level (1-10) at these timestamps:
- 0:00 (Opening) - typically 6-8
- 5:00 (Early Act 1)
- 10:00 (Act 1 Turn)
- 15:00 (Midpoint/Act 2 Turn)
- 20:00 (Act 3 setup)
- 25:00 (Act 3 Turn)
- 30:00 (Cliffhanger) - typically 8-10

For each timestamp provide:
- Tension rating (1-10)
- Why this rating
- Audience emotional state
- Recommended audio intensity

Generate as JSON array of tension points.

Expected JSON format:
[
  {{
    "timestamp": "0:00",
    "tension": 7,
    "reason": "opening hook draws listeners in",
    "emotional_state": "curious and engaged",
    "audio_intensity": "moderate build"
  }},
  ...
]
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        parsed = self._parse_json_response(response, [])
        if not isinstance(parsed, list):
            return [{"timestamp": "0:00", "tension": 7, "reason": "Opening hook", "emotional_state": "engaged", "audio_intensity": "moderate"}]
        return parsed
        
    def _parse_json_response(self, response: str, fallback: Any) -> Any:
        """Parse JSON response with fallback"""
        try:
            return json.loads(response)
        except:
            # Try to extract JSON from response text
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
            return fallback
            
    def export_txt(self, hook_cliffhanger_bible: Dict, filepath: str):
        """Export human-readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("HOOK & CLIFFHANGER STRATEGY BIBLE\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for episode_data in hook_cliffhanger_bible.get('episodes', []):
                episode_num = episode_data.get('episode_number', 'N/A')
                
                f.write("\n" + "="*70 + "\n")
                f.write(f"EPISODE {episode_num}\n")
                f.write("="*70 + "\n\n")
                
                # Opening Hook
                f.write("OPENING HOOK (First 60 Seconds)\n")
                f.write("-"*70 + "\n")
                hook = episode_data.get('opening_hook', {})
                f.write(f"Hook Type: {hook.get('hook_type', 'N/A')}\n")
                f.write(f"Audio Strategy: {hook.get('audio_strategy', 'N/A')}\n")
                f.write(f"Character Moment: {hook.get('character_moment', 'N/A')}\n")
                f.write(f"Question Raised: {hook.get('question_raised', 'N/A')}\n\n")
                
                # Act Turns
                f.write("THREE ACT TURNS\n")
                f.write("-"*70 + "\n")
                turns = episode_data.get('act_turns', {})
                f.write(f"Act 1 Turn (~25%): {turns.get('act1_turn', {}).get('story_beat', 'N/A')}\n")
                f.write(f"Act 2 Turn (~50%): {turns.get('act2_turn', {}).get('story_beat', 'N/A')}\n")
                f.write(f"Act 3 Turn (~75%): {turns.get('act3_turn', {}).get('story_beat', 'N/A')}\n\n")
                
                # Cliffhanger
                f.write("CLIFFHANGER ENDING\n")
                f.write("-"*70 + "\n")
                cliff = episode_data.get('cliffhanger', {})
                f.write(f"Type: {cliff.get('type', 'N/A')}\n")
                f.write(f"Intensity: {cliff.get('intensity', 'N/A')}/10\n")
                f.write(f"Question: {cliff.get('unanswered_question', 'N/A')}\n")
                f.write(f"Audio Execution: {cliff.get('audio_execution', 'N/A')}\n\n")
                
                # Tension Curve
                f.write("TENSION CURVE\n")
                f.write("-"*70 + "\n")
                for point in episode_data.get('tension_curve', []):
                    f.write(f"{point.get('timestamp', 'N/A')}: {point.get('tension', 'N/A')}/10 - {point.get('reason', 'N/A')}\n")
                f.write("\n")
                
    def export_json(self, hook_cliffhanger_bible: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(hook_cliffhanger_bible, f, indent=2, ensure_ascii=False)
            
    def export_pdf(self, hook_cliffhanger_bible: Dict, filepath: str):
        """Export professional PDF report"""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title page
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=1
        )
        
        story.append(Paragraph("HOOK & CLIFFHANGER STRATEGY", title_style))
        story.append(Paragraph("Episode Engagement Bible", styles['Heading2']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Session: {self.session_id}", styles['Normal']))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(PageBreak())
        
        # Episodes
        for episode_data in hook_cliffhanger_bible.get('episodes', []):
            episode_num = episode_data.get('episode_number', 'N/A')
            
            story.append(Paragraph(f"Episode {episode_num}", styles['Heading1']))
            
            # Opening Hook section
            story.append(Paragraph("Opening Hook", styles['Heading2']))
            hook = episode_data.get('opening_hook', {})
            story.append(Paragraph(f"<b>Type:</b> {hook.get('hook_type', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>Strategy:</b> {hook.get('audio_strategy', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Act Turns
            story.append(Paragraph("Act Turns", styles['Heading2']))
            turns = episode_data.get('act_turns', {})
            story.append(Paragraph(f"<b>Act 1:</b> {str(turns.get('act1_turn', {}).get('story_beat', 'N/A'))[:300]}", styles['Normal']))
            story.append(Paragraph(f"<b>Act 2:</b> {str(turns.get('act2_turn', {}).get('story_beat', 'N/A'))[:300]}", styles['Normal']))
            story.append(Paragraph(f"<b>Act 3:</b> {str(turns.get('act3_turn', {}).get('story_beat', 'N/A'))[:300]}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Cliffhanger
            story.append(Paragraph("Cliffhanger", styles['Heading2']))
            cliff = episode_data.get('cliffhanger', {})
            story.append(Paragraph(f"<b>Type:</b> {cliff.get('type', 'N/A')} (Intensity: {cliff.get('intensity', 'N/A')}/10)", styles['Normal']))
            story.append(Paragraph(f"<b>Question:</b> {cliff.get('unanswered_question', 'N/A')}", styles['Normal']))
            story.append(PageBreak())
        
        doc.build(story)
        
    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"⚡ STATION 12: HOOK & CLIFFHANGER DESIGNER")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")
        
        try:
            await self.initialize()
            
            # Load dependencies
            print("📥 Loading dependencies...")
            dependencies = await self.load_dependencies()
            
            if not dependencies.get('season_architecture'):
                raise ValueError("Missing season_architecture from Station 5")
                
            print("✅ Dependencies loaded\n")
            
            # Get episode list from season architecture
            season_data = dependencies.get('season_architecture', {})
            episodes = season_data.get('episodes', [])
            total_episodes = len(episodes)
            
            print(f"📺 Processing {total_episodes} episodes...\n")
            
            hook_cliffhanger_bible = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'total_episodes': total_episodes,
                'episodes': []
            }
            
            # Process each episode
            for idx, episode in enumerate(episodes):
                episode_num = idx + 1
                print(f"⚡ Episode {episode_num}/{total_episodes}...")
                
                # Generate opening hook
                print(f"  🎬 Generating opening hook...")
                opening_hook = await self.generate_opening_hook(episode_num, episode, dependencies)
                
                # Generate act turns
                print(f"  📊 Generating three act turns...")
                act_turns = await self.generate_act_turns(episode_num, episode, dependencies)
                
                # Generate cliffhanger
                next_episode_hint = episodes[idx + 1].get('title', '') if idx + 1 < total_episodes else None
                print(f"  🪝 Generating cliffhanger...")
                cliffhanger = await self.generate_cliffhanger(episode_num, episode, dependencies, next_episode_hint)
                
                # Compile episode data
                episode_engagement = {
                    'episode_number': episode_num,
                    'episode_title': episode.get('title', f'Episode {episode_num}'),
                    'opening_hook': opening_hook,
                    'act_turns': act_turns,
                    'cliffhanger': cliffhanger
                }
                
                # Generate tension curve
                print(f"  📈 Mapping tension curve...")
                tension_curve = await self.generate_tension_curve(episode_engagement)
                episode_engagement['tension_curve'] = tension_curve
                
                hook_cliffhanger_bible['episodes'].append(episode_engagement)
                print(f"✅ Episode {episode_num} complete\n")
            
            # Generate episode bridges
            print("🌉 Generating episode-to-episode bridges...")
            bridges = []
            for idx in range(total_episodes - 1):
                bridge = await self.generate_episode_bridge(
                    idx + 1,
                    hook_cliffhanger_bible['episodes'][idx],
                    hook_cliffhanger_bible['episodes'][idx + 1]
                )
                bridges.append(bridge)
            hook_cliffhanger_bible['episode_bridges'] = bridges
            print("✅ Bridges generated\n")
            
            # Export outputs
            print("💾 Exporting outputs...")
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            base_filename = f"station12_hook_cliffhanger_{self.session_id}"
            
            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")
            pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
            
            self.export_txt(hook_cliffhanger_bible, txt_path)
            print(f"  ✅ Text: {txt_path}")
            
            self.export_json(hook_cliffhanger_bible, json_path)
            print(f"  ✅ JSON: {json_path}")
            
            self.export_pdf(hook_cliffhanger_bible, pdf_path)
            print(f"  ✅ PDF: {pdf_path}")
            
            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_12",
                json.dumps(hook_cliffhanger_bible)
            )
            print("✅ Saved to Redis\n")
            
            result = {
                'station': 'station_12_hook_cliffhanger',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path,
                    'pdf': pdf_path
                },
                'statistics': {
                    'total_episodes': total_episodes,
                    'hooks_designed': total_episodes,
                    'cliffhangers_designed': total_episodes,
                    'bridges_created': len(bridges)
                },
                'hook_cliffhanger_bible': hook_cliffhanger_bible
            }
            
            print(f"{'='*70}")
            print(f"✅ STATION 12 COMPLETE: Hook & Cliffhanger Strategy Generated")
            print(f"{'='*70}\n")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error in Station 12: {str(e)}")
            raise
        finally:
            await self.redis_client.disconnect()


if __name__ == "__main__":
    import sys
    import asyncio
    
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
    else:
        session_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def main():
        station = Station12HookCliffhanger(session_id)
        result = await station.run()
        print("\n📊 Station 12 Results:")
        print(json.dumps(result['statistics'], indent=2))
    
    asyncio.run(main())