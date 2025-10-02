"""
Station 13: Multi-World/Timeline Manager Agent

This is a CONDITIONAL station that only activates if the story involves multiple 
worlds, timelines, or realities. Detects scenario complexity and generates 
world transition rules and audio strategies.

Dependencies: World Bible (Station 9), Season Architecture (Station 5), Project Bible (Station 2)
Outputs: Multi-world management bible or "Not Applicable" report
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
class WorldDefinition:
    """Data structure for a world/timeline/reality"""
    name: str
    world_type: str  # physical world, timeline, parallel reality, dream world, etc.
    key_features: Dict[str, Any]
    story_purpose: str
    differentiating_markers: List[str]
    accessibility: Dict[str, Any]

@dataclass
class TransitionRule:
    """Data structure for world transition rules"""
    from_world: str
    to_world: str
    method: str
    trigger_conditions: List[str]
    limitations: Dict[str, Any]
    experience: str

@dataclass
class AudioDifferentiation:
    """Data structure for world audio signatures"""
    world_name: str
    sonic_signature: str
    music_theme: str
    voice_treatment: str
    sound_palette: List[str]
    recognition_cue: str

class Station13MultiworldTimeline:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_13_multiworld_timeline"
        self.is_applicable = False
        
    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()
        
    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from previous stations"""
        dependencies = {}
        
        # Load world_bible (Station 9)
        world_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_9")
        if world_raw:
            dependencies['world_bible'] = json.loads(world_raw)
            
        # Load season_architecture (Station 5)
        season_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_5")
        if season_raw:
            dependencies['season_architecture'] = json.loads(season_raw)
            
        # Load project_bible (Station 2)
        project_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_2")
        if project_raw:
            dependencies['project_bible'] = json.loads(project_raw)
            
        return dependencies
        
    async def detect_multiworld_scenario(self, dependencies: Dict) -> Dict[str, Any]:
        """Detect if story involves multiple worlds/timelines using LLM analysis"""
        
        project_context = json.dumps(dependencies.get('project_bible', {}), indent=2)[:2000]
        world_context = json.dumps(dependencies.get('world_bible', {}), indent=2)[:2000]
        season_context = json.dumps(dependencies.get('season_architecture', {}), indent=2)[:1500]
        
        prompt = f"""
Analyze this audiobook project to determine if it involves MULTIPLE WORLDS, TIMELINES, or REALITIES.

PROJECT CONTEXT:
{project_context}

WORLD BIBLE:
{world_context}

SEASON ARCHITECTURE:
{season_context}

Determine if this story has:
1. Multiple physical worlds/dimensions/realms
2. Time travel or multiple timelines
3. Parallel realities or alternate universes
4. Significant flashback sequences that function as separate timelines
5. Dream worlds or mental landscapes that are substantial

RESPOND WITH JSON:
{{
  "is_multiworld": true/false,
  "type": "multiple_worlds" | "time_travel" | "parallel_timelines" | "flashbacks" | "single_world",
  "world_count": number,
  "timeline_count": number,
  "complexity_level": "simple" | "moderate" | "complex",
  "description": "brief explanation of world/timeline structure",
  "key_differentiators": ["how worlds differ"],
  "transition_frequency": "rare" | "occasional" | "frequent"
}}

If this is a SINGLE WORLD with no significant timeline complexity, set is_multiworld to false.
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        detection_result = self._parse_json_response(response, {
            'is_multiworld': False,
            'type': 'single_world',
            'world_count': 1,
            'timeline_count': 1,
            'complexity_level': 'simple',
            'description': 'Single world narrative',
            'key_differentiators': [],
            'transition_frequency': 'none'
        })
        
        self.is_applicable = detection_result.get('is_multiworld', False)
        return detection_result
        
    async def generate_world_inventory(self, dependencies: Dict) -> List[Dict[str, Any]]:
        """Generate comprehensive inventory of all worlds/timelines"""
        
        world_context = json.dumps(dependencies.get('world_bible', {}), indent=2)[:2000]
        project_context = json.dumps(dependencies.get('project_bible', {}), indent=2)[:1500]
        
        prompt = f"""
Create a comprehensive WORLD/TIMELINE INVENTORY for this multi-world audio drama.

WORLD CONTEXT:
{world_context}

PROJECT CONTEXT:
{project_context}

For EACH world/timeline/reality, provide:

1. NAME/DESIGNATION: What we call this world
2. TYPE: (physical world, timeline, parallel reality, dream world, past, future, etc.)
3. KEY FEATURES:
   - Physical characteristics
   - Time period (if applicable)
   - Technology level
   - Magic/supernatural elements
   - Population/inhabitants
4. STORY PURPOSE:
   - Why this world exists in the narrative
   - What story needs it serves
   - Character connections
5. DIFFERENTIATING MARKERS:
   - Visual/environmental differences
   - Cultural differences
   - Rule differences (physics, magic, etc.)
6. ACCESSIBILITY:
   - Who can access this world
   - Requirements for entry
   - Frequency of visits in story

Generate as JSON array with detailed world objects.
Make each world DISTINCT and purposeful.

Expected JSON format:
[
  {{
    "name": "World Name",
    "type": "physical world",
    "key_features": {{
      "physical_characteristics": "description",
      "time_period": "when it exists",
      "technology_level": "tech description",
      "supernatural_elements": "magic/powers",
      "population": "who lives there"
    }},
    "story_purpose": "why this world exists in narrative",
    "differentiating_markers": ["marker1", "marker2"],
    "accessibility": {{
      "who_can_access": "access requirements",
      "entry_requirements": "how to get in",
      "visit_frequency": "how often visited"
    }}
  }}
]
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, [])
        
    async def generate_transition_rules(self, world_inventory: List[Dict], dependencies: Dict) -> Dict[str, Any]:
        """Generate rules for moving between worlds/timelines"""
        
        world_summary = json.dumps(world_inventory, indent=2)
        
        prompt = f"""
Design TRANSITION RULES for moving between these worlds/timelines:

WORLD INVENTORY:
{world_summary}

Create comprehensive transition system:

1. TRANSITION METHODS:
   For each possible world-to-world connection:
   - How transition occurs (portal, device, ritual, natural, etc.)
   - Trigger conditions
   - Who can initiate
   - Duration of transition process

2. LIMITATIONS & COSTS:
   - Physical limitations (who can travel)
   - Energy/resource costs
   - Time costs (does time pass differently?)
   - Risks and dangers
   - Frequency limits

3. TRANSITION EXPERIENCE:
   - What character experiences during transition
   - Physical sensations
   - Visual/sensory elements
   - Disorientation effects
   - Memory effects

4. CONSISTENCY RULES:
   - What remains constant across worlds
   - What changes
   - Object/equipment behavior
   - Knowledge retention
   - Physical changes to travelers

5. STORY CONSTRAINTS:
   - When transitions can/cannot occur
   - Plot-driven limitations
   - Character-specific rules
   - Emergency exits

Generate as detailed JSON structure with clear rules for audio drama production.

Expected JSON format:
{{
  "transition_methods": [
    {{
      "from_world": "World A",
      "to_world": "World B", 
      "method": "portal",
      "trigger_conditions": ["condition1"],
      "initiator": "who can do it",
      "duration": "how long"
    }}
  ],
  "limitations": {{
    "physical": "who can travel",
    "costs": "what it costs",
    "risks": "dangers involved"
  }},
  "experience": {{
    "sensations": "what traveler feels",
    "effects": "disorientation etc"
  }},
  "consistency_rules": {{
    "constants": "what stays same",
    "variables": "what changes"
  }}
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {})
        
    async def generate_audio_differentiation(self, world_inventory: List[Dict]) -> Dict[str, Any]:
        """Generate audio strategy to differentiate each world/timeline"""
        
        world_summary = json.dumps(world_inventory, indent=2)
        
        prompt = f"""
Design AUDIO DIFFERENTIATION STRATEGY for these worlds/timelines:

WORLDS:
{world_summary}

For EACH world/timeline, create:

1. SONIC SIGNATURE:
   - Primary sound identifier (what makes this world unique)
   - Ambient soundscape (constant background)
   - Distinctive audio elements (recurring sounds)
   - Acoustic properties (reverb, echo, clarity)

2. MUSIC & SCORING:
   - Musical theme or motif for this world
   - Instrumentation choices
   - Tempo and rhythm patterns
   - Emotional tone of music

3. VOICE TREATMENT:
   - How voices sound in this world
   - Processing effects (reverb, filters, pitch)
   - Dialogue pacing differences
   - Acoustic environment for voices

4. SOUND DESIGN PALETTE:
   - Unique sound effects for this world
   - Technology sounds (if applicable)
   - Natural environment sounds
   - Cultural/social sounds

5. LISTENER RECOGNITION:
   - How listener immediately knows which world
   - Audio cue that appears within 3 seconds
   - Recurring audio motif
   - Transition confirmation sound

6. PRODUCTION NOTES:
   - Mixing recommendations
   - Effects chain suggestions
   - Recording environment preferences
   - Post-production guidelines

Generate as detailed JSON with PRODUCTION-READY audio guidance.
Each world must be IMMEDIATELY recognizable by sound alone.

Expected JSON format:
{{
  "World Name": {{
    "sonic_signature": "unique sound identifier",
    "music_theme": "musical approach",
    "voice_treatment": "how voices sound",
    "sound_palette": ["sound1", "sound2"],
    "recognition_cue": "immediate identifier",
    "production_notes": "technical guidance"
  }}
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {})
        
    async def generate_transition_sounds(self, world_inventory: List[Dict], transition_rules: Dict) -> List[Dict[str, Any]]:
        """Generate specific transition sound designs"""
        
        world_summary = json.dumps(world_inventory, indent=2)[:1500]
        transition_summary = json.dumps(transition_rules, indent=2)[:1500]
        
        prompt = f"""
Design TRANSITION SOUNDS for world/timeline shifts:

WORLDS:
{world_summary}

TRANSITION METHODS:
{transition_summary}

For EACH type of transition, design:

1. TRANSITION AUDIO CUE:
   - Initial sound (trigger/activation)
   - Transition process sound (journey)
   - Arrival sound (confirmation)
   - Total duration (seconds)

2. LAYERED SOUND DESIGN:
   - Bottom layer (foundational sound)
   - Mid layer (movement/transformation)
   - Top layer (detail/sparkle)
   - How layers evolve during transition

3. CHARACTER PERSPECTIVE:
   - What character hears during transition
   - Disorientation audio (if applicable)
   - Emotional sound components
   - Voice treatment during transition

4. LISTENER EXPERIENCE:
   - How to signal transition clearly
   - Avoid confusion
   - Build anticipation
   - Payoff on arrival

5. VARIATIONS:
   - Different transition types need different sounds
   - Emergency vs planned transitions
   - First-time vs repeated transitions
   - Success vs failed transitions

6. PRODUCTION SPECS:
   - Exact sound effect descriptions
   - Music cues
   - Mixing notes
   - Timing specifications

Generate detailed transition sound library as JSON array.

Expected JSON format:
[
  {{
    "transition_type": "portal",
    "from_world": "World A",
    "to_world": "World B",
    "audio_cue": "sound description",
    "duration": "3 seconds",
    "layers": {{
      "bottom": "foundational sound",
      "mid": "movement sound",
      "top": "detail sound"
    }},
    "character_experience": "what character hears",
    "production_specs": "technical notes"
  }}
]
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, [])
        
    async def generate_episode_world_mapping(self, world_inventory: List[Dict], dependencies: Dict) -> List[Dict[str, Any]]:
        """Map which worlds appear in which episodes"""
        
        world_summary = json.dumps(world_inventory, indent=2)
        episodes = dependencies.get('season_architecture', {}).get('episodes', [])
        episode_summary = json.dumps(episodes, indent=2)[:2000]
        
        prompt = f"""
Create EPISODE-BY-EPISODE WORLD MAPPING:

WORLDS:
{world_summary}

SEASON ARCHITECTURE:
{episode_summary}

For EACH episode, determine:

1. WORLDS FEATURED:
   - Which worlds appear
   - Primary world (most screen time)
   - Secondary worlds
   - Brief appearances

2. TRANSITION TIMELINE:
   - Approximate timestamps of transitions
   - Number of transitions per episode
   - Transition types used

3. TIME DISTRIBUTION:
   - Percentage of episode in each world
   - Balance across worlds
   - Pacing considerations

4. NARRATIVE PURPOSE:
   - Why these worlds in this episode
   - Story beats per world
   - Character arcs per world

5. AUDIO COMPLEXITY:
   - Number of sonic signatures needed
   - Transition sound count
   - Mixing complexity level

Generate as JSON array (one entry per episode).

Expected JSON format:
[
  {{
    "episode_number": 1,
    "worlds_featured": ["World A", "World B"],
    "primary_world": "World A",
    "transitions": [
      {{
        "timestamp": "15:30",
        "from": "World A",
        "to": "World B",
        "type": "portal"
      }}
    ],
    "time_distribution": {{
      "World A": "70%",
      "World B": "30%"
    }},
    "narrative_purpose": "why these worlds this episode",
    "audio_complexity": "moderate"
  }}
]
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, [])
        
    async def generate_orientation_strategy(self, world_inventory: List[Dict], dependencies: Dict) -> Dict[str, Any]:
        """Generate strategy to keep listeners oriented"""
        
        world_summary = json.dumps(world_inventory, indent=2)[:1500]
        
        prompt = f"""
Design LISTENER ORIENTATION STRATEGY for multi-world audio drama:

WORLDS:
{world_summary}

Create orientation system:

1. VERBAL CUES:
   - Character dialogue markers ("We're in the..." / "Back to...")
   - Natural exposition techniques
   - Location reminders
   - Time period indicators

2. AUDIO CUES:
   - Non-verbal sound reminders
   - Recurring motifs per world
   - Ambient sound signatures
   - Music themes

3. NARRATOR STRATEGY:
   - When to use narrator (if applicable)
   - What narrator says about location
   - Frequency of narrator reminders
   - Narrator voice treatment per world

4. COLD OPEN STRATEGY:
   - How to orient at episode start
   - Recap techniques
   - "Previously on..." approach
   - World identification in first 10 seconds

5. TRANSITION CLARITY:
   - How to make transitions obvious
   - Avoid listener confusion
   - Confirmation techniques
   - Recovery from potential confusion

6. FIRST-TIME LISTENER SUPPORT:
   - How someone jumping in mid-season can orient
   - Essential context delivery
   - World introduction techniques

Generate as detailed JSON strategy document.
Goal: ZERO listener confusion about which world we're in.

Expected JSON format:
{{
  "verbal_cues": {{
    "dialogue_markers": ["example phrases"],
    "exposition_techniques": "natural ways to remind location"
  }},
  "audio_cues": {{
    "sound_reminders": "ambient signatures",
    "music_themes": "recurring motifs"
  }},
  "narrator_strategy": {{
    "when_to_use": "timing guidelines",
    "content": "what to say"
  }},
  "transition_clarity": {{
    "methods": "how to make obvious",
    "confusion_recovery": "if listeners get lost"
  }}
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {})
        
    async def generate_timeline_consistency_rules(self, world_inventory: List[Dict], dependencies: Dict) -> Dict[str, Any]:
        """Generate rules for timeline/reality consistency"""
        
        world_summary = json.dumps(world_inventory, indent=2)
        project_context = json.dumps(dependencies.get('project_bible', {}), indent=2)[:1500]
        
        prompt = f"""
Create TIMELINE CONSISTENCY RULES:

WORLDS/TIMELINES:
{world_summary}

PROJECT CONTEXT:
{project_context}

Define consistency rules:

1. IMMUTABLE ELEMENTS:
   - What cannot change across worlds/timelines
   - Fixed points in time/space
   - Character core traits that remain constant
   - Physical laws that apply everywhere

2. VARIABLE ELEMENTS:
   - What can be different
   - Degree of variation allowed
   - Why variations exist

3. PARADOX PREVENTION:
   - Rules to avoid timeline paradoxes
   - What happens if rules broken
   - Self-correction mechanisms
   - Story constraints to prevent issues

4. CHARACTER KNOWLEDGE:
   - What characters know about multiple worlds
   - Memory rules (what they remember)
   - Information transfer rules
   - Learning across worlds

5. OBJECT CONTINUITY:
   - What happens to objects when traveling
   - Existence in multiple worlds
   - Item changes/adaptations
   - Unique objects per world

6. CAUSE & EFFECT:
   - How actions in one world affect others
   - Time delay effects
   - Ripple rules
   - Isolation vs connection

7. STORY LOGIC:
   - Internal consistency requirements
   - Plot hole prevention
   - Mystery maintenance
   - Revelation planning

Generate as comprehensive JSON rulebook for writers and producers.

Expected JSON format:
{{
  "immutable_elements": {{
    "fixed_points": "what never changes",
    "character_constants": "unchanging traits"
  }},
  "variable_elements": {{
    "allowable_differences": "what can vary",
    "variation_limits": "how much change allowed"
  }},
  "paradox_prevention": {{
    "rules": "how to avoid paradoxes",
    "consequences": "what happens if broken"
  }},
  "character_knowledge": {{
    "awareness_levels": "what characters know",
    "memory_rules": "what they remember"
  }}
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {})
        
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
                # Try array format
                array_match = re.search(r'\[.*\]', response, re.DOTALL)
                if array_match:
                    return json.loads(array_match.group())
            except:
                pass
            return fallback
            
    def export_txt(self, multiworld_bible: Dict, filepath: str):
        """Export human-readable text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("MULTI-WORLD/TIMELINE MANAGEMENT BIBLE\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Applicable: {multiworld_bible.get('is_applicable', False)}\n\n")
            
            if not multiworld_bible.get('is_applicable', False):
                f.write("="*70 + "\n")
                f.write("SINGLE WORLD NARRATIVE\n")
                f.write("="*70 + "\n\n")
                f.write("This story takes place in a single world/timeline.\n")
                f.write("Multi-world management is not required.\n\n")
                detection = multiworld_bible.get('detection_analysis', {})
                f.write(f"Analysis: {detection.get('description', 'N/A')}\n")
                return
                
            # World Inventory
            f.write("="*70 + "\n")
            f.write("SECTION 1: WORLD/TIMELINE INVENTORY\n")
            f.write("="*70 + "\n\n")
            for world in multiworld_bible.get('world_inventory', []):
                f.write(f"WORLD: {world.get('name', 'N/A')}\n")
                f.write("-"*70 + "\n")
                f.write(f"Type: {world.get('type', 'N/A')}\n")
                f.write(f"Purpose: {world.get('story_purpose', 'N/A')}\n")
                f.write(f"Key Features: {world.get('key_features', 'N/A')}\n\n")
                
            # Transition Rules
            f.write("\n" + "="*70 + "\n")
            f.write("SECTION 2: TRANSITION RULES\n")
            f.write("="*70 + "\n\n")
            transition_rules = multiworld_bible.get('transition_rules', {})
            f.write(f"{json.dumps(transition_rules, indent=2)}\n\n")
            
            # Audio Differentiation
            f.write("\n" + "="*70 + "\n")
            f.write("SECTION 3: AUDIO DIFFERENTIATION STRATEGY\n")
            f.write("="*70 + "\n\n")
            audio_diff = multiworld_bible.get('audio_differentiation', {})
            for world_name, audio_spec in audio_diff.items():
                f.write(f"\nWORLD: {world_name}\n")
                f.write("-"*70 + "\n")
                f.write(f"Sonic Signature: {audio_spec.get('sonic_signature', 'N/A')}\n")
                f.write(f"Music Theme: {audio_spec.get('music_theme', 'N/A')}\n\n")
                
            # Transition Sounds
            f.write("\n" + "="*70 + "\n")
            f.write("SECTION 4: TRANSITION SOUND LIBRARY\n")
            f.write("="*70 + "\n\n")
            for trans_sound in multiworld_bible.get('transition_sounds', []):
                f.write(f"Transition: {trans_sound.get('transition_type', 'N/A')}\n")
                f.write(f"Audio Cue: {trans_sound.get('audio_cue', 'N/A')}\n")
                f.write(f"Duration: {trans_sound.get('duration', 'N/A')}\n\n")
                
            # Episode Mapping
            f.write("\n" + "="*70 + "\n")
            f.write("SECTION 5: EPISODE-BY-EPISODE WORLD MAPPING\n")
            f.write("="*70 + "\n\n")
            for ep_map in multiworld_bible.get('episode_mapping', []):
                f.write(f"Episode {ep_map.get('episode_number', 'N/A')}: ")
                f.write(f"{', '.join(ep_map.get('worlds_featured', []))}\n")
                
            # Orientation Strategy
            f.write("\n" + "="*70 + "\n")
            f.write("SECTION 6: LISTENER ORIENTATION STRATEGY\n")
            f.write("="*70 + "\n\n")
            orientation = multiworld_bible.get('orientation_strategy', {})
            f.write(f"{json.dumps(orientation, indent=2)}\n\n")
            
            # Consistency Rules
            f.write("\n" + "="*70 + "\n")
            f.write("SECTION 7: TIMELINE CONSISTENCY RULES\n")
            f.write("="*70 + "\n\n")
            consistency = multiworld_bible.get('consistency_rules', {})
            f.write(f"{json.dumps(consistency, indent=2)}\n\n")
            
    def export_json(self, multiworld_bible: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(multiworld_bible, f, indent=2, ensure_ascii=False)
            
    def export_pdf(self, multiworld_bible: Dict, filepath: str):
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
        
        story.append(Paragraph("MULTI-WORLD/TIMELINE BIBLE", title_style))
        story.append(Paragraph("Audio Drama World Management", styles['Heading2']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Session: {self.session_id}", styles['Normal']))
        story.append(Paragraph(f"Applicable: {multiworld_bible.get('is_applicable', False)}", styles['Normal']))
        story.append(PageBreak())
        
        if not multiworld_bible.get('is_applicable', False):
            story.append(Paragraph("Single World Narrative", styles['Heading1']))
            story.append(Paragraph("This story takes place in a single world/timeline. Multi-world management is not required.", styles['Normal']))
            detection = multiworld_bible.get('detection_analysis', {})
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(f"<b>Analysis:</b> {detection.get('description', 'N/A')}", styles['Normal']))
        else:
            # World Inventory
            story.append(Paragraph("World/Timeline Inventory", styles['Heading1']))
            for world in multiworld_bible.get('world_inventory', []):
                story.append(Paragraph(f"<b>{world.get('name', 'N/A')}</b>", styles['Heading2']))
                story.append(Paragraph(f"Type: {world.get('type', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Purpose: {world.get('story_purpose', 'N/A')}", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            story.append(PageBreak())
            
            # Audio Differentiation
            story.append(Paragraph("Audio Differentiation Strategy", styles['Heading1']))
            audio_diff = multiworld_bible.get('audio_differentiation', {})
            for world_name, audio_spec in audio_diff.items():
                story.append(Paragraph(f"<b>{world_name}</b>", styles['Heading2']))
                story.append(Paragraph(f"Sonic Signature: {audio_spec.get('sonic_signature', 'N/A')}", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            story.append(PageBreak())
            
            # Transition Sounds
            story.append(Paragraph("Transition Sound Library", styles['Heading1']))
            for trans_sound in multiworld_bible.get('transition_sounds', []):
                story.append(Paragraph(f"<b>{trans_sound.get('transition_type', 'N/A')}</b>", styles['Heading2']))
                story.append(Paragraph(f"Audio: {trans_sound.get('audio_cue', 'N/A')}", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
        
    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"🌐 STATION 13: MULTI-WORLD/TIMELINE MANAGER")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")
        
        try:
            await self.initialize()
            
            # Load dependencies
            print("📥 Loading dependencies...")
            dependencies = await self.load_dependencies()
            print("✅ Dependencies loaded\n")
            
            # Detect if multiworld scenario
            print("🔍 Analyzing world/timeline structure...")
            detection_analysis = await self.detect_multiworld_scenario(dependencies)
            print(f"✅ Analysis complete: {detection_analysis.get('type', 'unknown')}\n")
            
            multiworld_bible = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'is_applicable': detection_analysis.get('is_multiworld', False),
                'detection_analysis': detection_analysis
            }
            
            if not detection_analysis.get('is_multiworld', False):
                print("ℹ️  Single world/timeline detected - minimal processing\n")
                
                # Still export files but with minimal content
                output_dir = "outputs"
                os.makedirs(output_dir, exist_ok=True)
                
                base_filename = f"station13_multiworld_{self.session_id}"
                
                txt_path = os.path.join(output_dir, f"{base_filename}.txt")
                json_path = os.path.join(output_dir, f"{base_filename}.json")
                pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
                
                self.export_txt(multiworld_bible, txt_path)
                self.export_json(multiworld_bible, json_path)
                self.export_pdf(multiworld_bible, pdf_path)
                
                print("💾 Outputs generated (Not Applicable status)\n")
                
            else:
                print(f"🌍 Multi-world scenario confirmed - full processing")
                print(f"   Worlds: {detection_analysis.get('world_count', 'N/A')}")
                print(f"   Complexity: {detection_analysis.get('complexity_level', 'N/A')}\n")
                
                # Generate world inventory
                print("📋 Generating world/timeline inventory...")
                world_inventory = await self.generate_world_inventory(dependencies)
                multiworld_bible['world_inventory'] = world_inventory
                print(f"✅ {len(world_inventory)} worlds catalogued\n")
                
                # Generate transition rules
                print("🔄 Generating transition rules...")
                transition_rules = await self.generate_transition_rules(world_inventory, dependencies)
                multiworld_bible['transition_rules'] = transition_rules
                print("✅ Transition rules established\n")
                
                # Generate audio differentiation
                print("🎵 Generating audio differentiation strategy...")
                audio_diff = await self.generate_audio_differentiation(world_inventory)
                multiworld_bible['audio_differentiation'] = audio_diff
                print("✅ Audio signatures defined\n")
                
                # Generate transition sounds
                print("🔊 Generating transition sound library...")
                transition_sounds = await self.generate_transition_sounds(world_inventory, transition_rules)
                multiworld_bible['transition_sounds'] = transition_sounds
                print(f"✅ {len(transition_sounds)} transition sounds designed\n")
                
                # Generate episode mapping
                print("📺 Mapping worlds to episodes...")
                episode_mapping = await self.generate_episode_world_mapping(world_inventory, dependencies)
                multiworld_bible['episode_mapping'] = episode_mapping
                print("✅ Episode world mapping complete\n")
                
                # Generate orientation strategy
                print("🧭 Generating listener orientation strategy...")
                orientation = await self.generate_orientation_strategy(world_inventory, dependencies)
                multiworld_bible['orientation_strategy'] = orientation
                print("✅ Orientation strategy defined\n")
                
                # Generate consistency rules
                print("📜 Generating timeline consistency rules...")
                consistency = await self.generate_timeline_consistency_rules(world_inventory, dependencies)
                multiworld_bible['consistency_rules'] = consistency
                print("✅ Consistency rules established\n")
                
                # Export outputs
                print("💾 Exporting outputs...")
                output_dir = "outputs"
                os.makedirs(output_dir, exist_ok=True)
                
                base_filename = f"station13_multiworld_{self.session_id}"
                
                txt_path = os.path.join(output_dir, f"{base_filename}.txt")
                json_path = os.path.join(output_dir, f"{base_filename}.json")
                pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
                
                self.export_txt(multiworld_bible, txt_path)
                print(f"  ✅ Text: {txt_path}")
                
                self.export_json(multiworld_bible, json_path)
                print(f"  ✅ JSON: {json_path}")
                
                self.export_pdf(multiworld_bible, pdf_path)
                print(f"  ✅ PDF: {pdf_path}")
            
            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_13",
                json.dumps(multiworld_bible)
            )
            print("✅ Saved to Redis\n")
            
            result = {
                'station': 'station_13_multiworld_timeline',
                'status': 'complete',
                'is_applicable': multiworld_bible.get('is_applicable', False),
                'outputs': {
                    'txt': txt_path,
                    'json': json_path,
                    'pdf': pdf_path
                },
                'statistics': {
                    'world_count': len(multiworld_bible.get('world_inventory', [])),
                    'transition_types': len(multiworld_bible.get('transition_sounds', [])),
                    'complexity_level': detection_analysis.get('complexity_level', 'simple')
                },
                'multiworld_bible': multiworld_bible
            }
            
            print(f"{'='*70}")
            print(f"✅ STATION 13 COMPLETE: Multi-World Management Generated")
            print(f"{'='*70}\n")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error in Station 13: {str(e)}")
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
        station = Station13MultiworldTimeline(session_id)
        result = await station.run()
        print("\n📊 Station 13 Results:")
        print(json.dumps(result['statistics'], indent=2))
    
    asyncio.run(main())