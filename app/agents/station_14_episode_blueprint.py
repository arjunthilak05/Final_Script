"""
Station 14: Simple Episode Blueprint Agent

This is the final blueprint station that creates simple, clear episode summaries 
ready for human review and approval. Synthesizes all previous station outputs
into digestible episode blueprints.

Dependencies: All previous stations (5, 8, 9, 10, 11, 12, 13)
Outputs: Episode blueprints ready for approval (TXT, JSON, PDF)
Human Gate: CRITICAL - Requires stakeholder approval before proceeding
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
class EpisodeBlueprint:
    """Data structure for a single episode blueprint"""
    episode_number: int
    episode_title: str
    simple_summary: str  # 2-3 paragraphs, no dialogue
    why_it_matters: str  # story significance
    character_goals: List[Dict[str, str]]  # character objectives and obstacles
    story_connection: Dict[str, str]  # larger story ties
    production_essentials: Dict[str, Any]  # technical requirements

@dataclass
class SeasonOverview:
    """Data structure for complete season narrative"""
    season_arc_summary: str
    key_story_threads: List[Dict[str, Any]]
    character_journeys: Dict[str, str]
    thematic_cohesion: Dict[str, str]
    audience_experience: Dict[str, str]

@dataclass
class ApprovalChecklist:
    """Data structure for human reviewer checklist"""
    story_coherence: List[str]
    character_consistency: List[str]
    pacing_structure: List[str]
    audio_production: List[str]
    audience_engagement: List[str]
    thematic_depth: List[str]
    concerns: List[str]

class Station14EpisodeBlueprint:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_client = RedisClient()
        self.openrouter = OpenRouterAgent()
        self.station_name = "station_14_episode_blueprint"
        
    async def initialize(self):
        """Initialize connections"""
        await self.redis_client.connect()
        
    async def load_dependencies(self) -> Dict[str, Any]:
        """Load required outputs from all previous stations"""
        dependencies = {}
        
        # Station 5: Season Architecture
        season_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_5")
        if season_raw:
            dependencies['season_architecture'] = json.loads(season_raw)
            
        # Station 8: Character Bible
        character_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_8")
        if character_raw:
            dependencies['character_bible'] = json.loads(character_raw)
            
        # Station 9: World Bible
        world_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_9")
        if world_raw:
            dependencies['world_bible'] = json.loads(world_raw)
            
        # Station 10: Narrative Reveal (if available)
        reveal_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_10")
        if reveal_raw:
            dependencies['narrative_reveal'] = json.loads(reveal_raw)
            
        # Station 11: (if available)
        station11_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_11")
        if station11_raw:
            dependencies['station_11'] = json.loads(station11_raw)
            
        # Station 12: Hook & Cliffhanger
        hook_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_12")
        if hook_raw:
            dependencies['hook_cliffhanger'] = json.loads(hook_raw)
            
        # Station 13: Multi-world (if applicable)
        multiworld_raw = await self.redis_client.get(f"audiobook:{self.session_id}:station_13")
        if multiworld_raw:
            dependencies['multiworld'] = json.loads(multiworld_raw)
            
        return dependencies
        
    async def generate_episode_blueprint(self, episode_num: int, episode_context: Dict, dependencies: Dict) -> Dict[str, Any]:
        """Generate complete blueprint for single episode using LLM"""
        
        # Get relevant character info
        characters_summary = ""
        if dependencies.get('character_bible'):
            char_data = dependencies['character_bible']
            main_chars = char_data.get('tier1_protagonists', [])[:3]  # Top 3 characters
            characters_summary = json.dumps(main_chars, indent=2)[:1500]
        
        # Get relevant world info
        world_summary = ""
        if dependencies.get('world_bible'):
            world_data = dependencies['world_bible']
            locations = world_data.get('geography', {}).get('locations', [])[:3]
            world_summary = json.dumps(locations, indent=2)[:1000]
        
        # Get hook/cliffhanger for this episode
        episode_hooks = {}
        if dependencies.get('hook_cliffhanger'):
            hook_cliff_episodes = dependencies['hook_cliffhanger'].get('episodes', [])
            episode_hooks = next((ep for ep in hook_cliff_episodes if ep.get('episode_number') == episode_num), {})
        
        prompt = f"""
Create a SIMPLE EPISODE BLUEPRINT for Episode {episode_num}.

EPISODE CONTEXT:
{json.dumps(episode_context, indent=2)}

CHARACTERS:
{characters_summary}

WORLD/LOCATIONS:
{world_summary}

HOOK & CLIFFHANGER:
Opening Hook: {episode_hooks.get('opening_hook', {}).get('hook_type', 'N/A')}
Cliffhanger: {episode_hooks.get('cliffhanger', {}).get('type', 'N/A')} (Intensity: {episode_hooks.get('cliffhanger', {}).get('intensity', 'N/A')}/10)

Generate EPISODE BLUEPRINT with:

1. SIMPLE SUMMARY (2-3 paragraphs):
Write a clear, engaging summary in SIMPLE LANGUAGE that explains:
- What happens at the beginning
- What happens in the middle (main action/conflict)
- What happens at the end
- Key turning points
- Character focus

Use storytelling language, NOT technical terms.
Write for someone who doesn't know the production process.
NO dialogue. NO scene numbers. Just the story.

Example style:
"Episode 3 opens with Sarah discovering the mysterious letter in her grandmother's attic. As she reads it, she realizes her family has been keeping a dangerous secret for decades. The middle of the episode follows Sarah as she confronts her mother about the letter, leading to a heated argument that reveals painful truths about their past. By the end, Sarah must decide whether to pursue the truth or protect her family from what she might uncover. The episode ends with Sarah making a phone call that will change everything."

2. WHY IT MATTERS:
- How does this episode advance the overall story?
- What character development occurs?
- What plot threads move forward?
- What does it set up for future episodes?
- Why is this episode necessary?

3. CHARACTER GOALS & OBSTACLES:
For each main character in this episode:
- What do they want?
- What's stopping them?
- What decision do they make?
- How do they change?

4. LARGER STORY CONNECTION:
- Callback to previous episodes (what threads continue?)
- New threads introduced (what questions arise?)
- Story arc progression (where are we in the journey?)
- How hook and cliffhanger connect episodes

5. PRODUCTION ESSENTIALS:
- Estimated episode length (minutes)
- Number of main characters featured
- Number of locations/settings
- Audio complexity (simple/moderate/complex)
- Special audio requirements (if any)

Generate as detailed JSON structure.
Make it CLEAR, SIMPLE, and APPROVAL-READY for stakeholders.

Expected JSON format:
{{
  "simple_summary": "2-3 paragraph story summary with no dialogue",
  "why_it_matters": "story significance and necessity",
  "character_goals": [
    {{
      "character": "Character Name",
      "goal": "what they want",
      "obstacle": "what stops them",
      "decision": "choice they make",
      "change": "how they develop"
    }}
  ],
  "story_connection": {{
    "continues": "what threads from previous episodes",
    "introduces": "new story elements",
    "progression": "where in overall arc",
    "hook_connection": "how opening/ending connect"
  }},
  "production_essentials": {{
    "estimated_length": 30,
    "character_count": 3,
    "location_count": 2,
    "audio_complexity": "moderate",
    "special_requirements": "any unique needs"
  }}
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {
            'simple_summary': 'TBD',
            'why_it_matters': 'TBD',
            'character_goals': [],
            'story_connection': {},
            'production_essentials': {}
        })
        
    async def generate_season_overview(self, all_blueprints: List[Dict], dependencies: Dict) -> Dict[str, Any]:
        """Generate overall season narrative overview"""
        
        episode_summaries = []
        for bp in all_blueprints:
            episode_summaries.append({
                'episode': bp.get('episode_number'),
                'summary': bp.get('simple_summary', '')[:300]
            })
        
        prompt = f"""
Create SEASON NARRATIVE OVERVIEW based on these episode blueprints:

EPISODE SUMMARIES:
{json.dumps(episode_summaries, indent=2)}

Generate SEASON OVERVIEW:

1. SEASON ARC SUMMARY (3-4 paragraphs):
- Overall story journey from beginning to end
- Major turning points across the season
- Character transformation arcs
- Thematic progression
- Resolution/cliffhanger for season

2. KEY STORY THREADS:
- List 5-8 major story threads
- Which episodes each thread appears in
- How each thread resolves (or doesn't)

3. CHARACTER JOURNEYS:
For each main character:
- Starting point (Episode 1)
- Major changes/growth moments
- Ending point (Final episode)
- Transformation summary

4. THEMATIC COHESION:
- Central themes explored
- How themes develop across episodes
- Thematic resolution

5. AUDIENCE EXPERIENCE:
- Emotional journey listeners go through
- Pacing and rhythm across season
- Satisfaction factors
- Hooks for next season (if applicable)

Generate as detailed JSON structure.
This should give stakeholders a clear picture of the complete season.

Expected JSON format:
{{
  "season_arc_summary": "3-4 paragraph overview of complete season",
  "key_story_threads": [
    {{
      "thread": "Thread Name",
      "episodes": [1, 3, 5, 8],
      "resolution": "how it concludes"
    }}
  ],
  "character_journeys": {{
    "Character Name": {{
      "starting_point": "where they begin",
      "growth_moments": ["key changes"],
      "ending_point": "where they end",
      "transformation": "overall change"
    }}
  }},
  "thematic_cohesion": {{
    "central_themes": ["theme1", "theme2"],
    "development": "how themes progress",
    "resolution": "thematic conclusion"
  }},
  "audience_experience": {{
    "emotional_journey": "listener experience",
    "pacing": "rhythm description",
    "satisfaction": "payoff factors"
  }}
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {
            'season_arc_summary': 'TBD',
            'key_story_threads': [],
            'character_journeys': {},
            'thematic_cohesion': {},
            'audience_experience': {}
        })
        
    async def generate_approval_checklist(self, all_blueprints: List[Dict], dependencies: Dict) -> Dict[str, Any]:
        """Generate checklist for human reviewers"""
        
        prompt = f"""
Create APPROVAL CHECKLIST for stakeholders reviewing these episode blueprints.

TOTAL EPISODES: {len(all_blueprints)}

Generate checklist with:

1. STORY COHERENCE:
- Does the overall story make sense?
- Are there any plot holes or logic issues?
- Do character motivations track throughout?
- Are reveals properly set up?

2. CHARACTER CONSISTENCY:
- Do characters behave consistently?
- Are character arcs satisfying?
- Are relationships developed properly?
- Do characters grow/change believably?

3. PACING & STRUCTURE:
- Is pacing appropriate for audio format?
- Are episodes balanced in content/length?
- Do hooks and cliffhangers work effectively?
- Is there variety in episode types?

4. AUDIO PRODUCTION:
- Is audio complexity manageable?
- Are location counts realistic?
- Are character counts per episode reasonable?
- Are there any impossible production requirements?

5. AUDIENCE ENGAGEMENT:
- Will listeners want to continue?
- Are mysteries compelling?
- Are stakes clear and escalating?
- Is payoff satisfying?

6. THEMATIC DEPTH:
- Are themes clear and consistent?
- Does the story have something to say?
- Is there emotional resonance?

7. CONCERNS TO FLAG:
- List any specific concerns or questions
- Note any episodes that need revision
- Identify any missing elements

Generate as JSON checklist with specific items to review.

Expected JSON format:
{{
  "story_coherence": [
    "Does the overall story make sense?",
    "Are there any plot holes?"
  ],
  "character_consistency": [
    "Do characters behave consistently?",
    "Are character arcs satisfying?"
  ],
  "pacing_structure": [
    "Is pacing appropriate for audio?",
    "Are episodes balanced?"
  ],
  "audio_production": [
    "Is audio complexity manageable?",
    "Are location counts realistic?"
  ],
  "audience_engagement": [
    "Will listeners want to continue?",
    "Are mysteries compelling?"
  ],
  "thematic_depth": [
    "Are themes clear and consistent?",
    "Is there emotional resonance?"
  ],
  "concerns_to_flag": [
    "Specific concerns or questions",
    "Episodes needing revision"
  ]
}}
"""
        
        response = await self.openrouter.process_message(prompt, "grok-4")
        return self._parse_json_response(response, {
            'story_coherence': [],
            'character_consistency': [],
            'pacing_structure': [],
            'audio_production': [],
            'audience_engagement': [],
            'thematic_depth': [],
            'concerns_to_flag': []
        })
        
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
            
    def export_txt(self, blueprint_bible: Dict, filepath: str):
        """Export human-readable text report - PRIMARY format for human review"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("EPISODE BLUEPRINT - HUMAN APPROVAL DOCUMENT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Episodes: {len(blueprint_bible.get('episodes', []))}\n\n")
            
            # Season Overview
            f.write("="*70 + "\n")
            f.write("SEASON OVERVIEW\n")
            f.write("="*70 + "\n\n")
            overview = blueprint_bible.get('season_overview', {})
            f.write(overview.get('season_arc_summary', 'N/A') + "\n\n")
            
            # Episode Blueprints
            f.write("\n" + "="*70 + "\n")
            f.write("EPISODE-BY-EPISODE BLUEPRINTS\n")
            f.write("="*70 + "\n\n")
            
            for episode_bp in blueprint_bible.get('episodes', []):
                episode_num = episode_bp.get('episode_number', 'N/A')
                
                f.write("\n" + "="*70 + "\n")
                f.write(f"EPISODE {episode_num}: {episode_bp.get('episode_title', 'Untitled')}\n")
                f.write("="*70 + "\n\n")
                
                # Simple Summary
                f.write("STORY SUMMARY:\n")
                f.write("-"*70 + "\n")
                f.write(episode_bp.get('simple_summary', 'N/A') + "\n\n")
                
                # Why It Matters
                f.write("WHY THIS EPISODE MATTERS:\n")
                f.write("-"*70 + "\n")
                f.write(episode_bp.get('why_it_matters', 'N/A') + "\n\n")
                
                # Character Goals
                f.write("CHARACTER GOALS & OBSTACLES:\n")
                f.write("-"*70 + "\n")
                for char_goal in episode_bp.get('character_goals', []):
                    f.write(f"• {char_goal.get('character', 'N/A')}: ")
                    f.write(f"{char_goal.get('goal', 'N/A')}\n")
                    f.write(f"  Obstacle: {char_goal.get('obstacle', 'N/A')}\n")
                    f.write(f"  Decision: {char_goal.get('decision', 'N/A')}\n\n")
                
                # Story Connection
                f.write("CONNECTION TO LARGER STORY:\n")
                f.write("-"*70 + "\n")
                connection = episode_bp.get('story_connection', {})
                f.write(f"Continues: {connection.get('continues', 'N/A')}\n")
                f.write(f"Introduces: {connection.get('introduces', 'N/A')}\n")
                f.write(f"Progression: {connection.get('progression', 'N/A')}\n\n")
                
                # Production Essentials
                f.write("PRODUCTION ESSENTIALS:\n")
                f.write("-"*70 + "\n")
                prod = episode_bp.get('production_essentials', {})
                f.write(f"Length: {prod.get('estimated_length', 'N/A')} minutes\n")
                f.write(f"Characters: {prod.get('character_count', 'N/A')}\n")
                f.write(f"Locations: {prod.get('location_count', 'N/A')}\n")
                f.write(f"Complexity: {prod.get('audio_complexity', 'N/A')}\n")
                if prod.get('special_requirements'):
                    f.write(f"Special Requirements: {prod.get('special_requirements')}\n")
                f.write("\n")
            
            # Approval Checklist
            f.write("\n" + "="*70 + "\n")
            f.write("APPROVAL CHECKLIST\n")
            f.write("="*70 + "\n\n")
            checklist = blueprint_bible.get('approval_checklist', {})
            
            for category, items in checklist.items():
                if isinstance(items, list) and items:
                    f.write(f"\n{category.replace('_', ' ').upper()}:\n")
                    for item in items:
                        f.write(f"[ ] {item}\n")
            
            f.write("\n\n" + "="*70 + "\n")
            f.write("APPROVAL SIGNATURE\n")
            f.write("="*70 + "\n\n")
            f.write("Approved by: ___________________________  Date: ___________\n\n")
            f.write("Notes/Changes Required:\n")
            f.write("_"*70 + "\n"*5)
            
    def export_json(self, blueprint_bible: Dict, filepath: str):
        """Export structured JSON data"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(blueprint_bible, f, indent=2, ensure_ascii=False)
            
    def export_pdf(self, blueprint_bible: Dict, filepath: str):
        """Export professional PDF report - APPROVAL DOCUMENT"""
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=30,
            alignment=1
        )
        
        # Title Page
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph("EPISODE BLUEPRINT", title_style))
        story.append(Paragraph("Human Approval Document", subtitle_style))
        story.append(Spacer(1, 0.5*inch))
        
        info_data = [
            ['Session ID:', self.session_id],
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Total Episodes:', str(len(blueprint_bible.get('episodes', [])))]
        ]
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(info_table)
        story.append(PageBreak())
        
        # Season Overview
        story.append(Paragraph("Season Overview", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        overview = blueprint_bible.get('season_overview', {})
        story.append(Paragraph(overview.get('season_arc_summary', 'N/A'), styles['Normal']))
        story.append(PageBreak())
        
        # Episode Blueprints
        for episode_bp in blueprint_bible.get('episodes', []):
            episode_num = episode_bp.get('episode_number', 'N/A')
            episode_title = episode_bp.get('episode_title', 'Untitled')
            
            story.append(Paragraph(f"Episode {episode_num}: {episode_title}", styles['Heading1']))
            story.append(Spacer(1, 0.2*inch))
            
            # Story Summary
            story.append(Paragraph("<b>Story Summary</b>", styles['Heading2']))
            story.append(Paragraph(episode_bp.get('simple_summary', 'N/A'), styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Why It Matters
            story.append(Paragraph("<b>Why This Episode Matters</b>", styles['Heading2']))
            story.append(Paragraph(episode_bp.get('why_it_matters', 'N/A'), styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Character Goals
            story.append(Paragraph("<b>Character Goals & Obstacles</b>", styles['Heading2']))
            for char_goal in episode_bp.get('character_goals', []):
                char_text = f"<b>{char_goal.get('character', 'N/A')}:</b> {char_goal.get('goal', 'N/A')}"
                story.append(Paragraph(char_text, styles['Normal']))
                story.append(Paragraph(f"Obstacle: {char_goal.get('obstacle', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Production Essentials Table
            story.append(Paragraph("<b>Production Essentials</b>", styles['Heading2']))
            prod = episode_bp.get('production_essentials', {})
            prod_data = [
                ['Length:', f"{prod.get('estimated_length', 'N/A')} minutes"],
                ['Characters:', str(prod.get('character_count', 'N/A'))],
                ['Locations:', str(prod.get('location_count', 'N/A'))],
                ['Complexity:', prod.get('audio_complexity', 'N/A')]
            ]
            prod_table = Table(prod_data, colWidths=[1.5*inch, 4*inch])
            prod_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(prod_table)
            story.append(PageBreak())
        
        # Approval Checklist
        story.append(Paragraph("Approval Checklist", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        checklist = blueprint_bible.get('approval_checklist', {})
        
        for category, items in checklist.items():
            if isinstance(items, list) and items:
                story.append(Paragraph(f"<b>{category.replace('_', ' ').title()}</b>", styles['Heading2']))
                for item in items:
                    story.append(Paragraph(f"☐ {item}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        story.append(PageBreak())
        
        # Approval Signature Page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("Approval Signature", styles['Heading1']))
        story.append(Spacer(1, 0.5*inch))
        
        sig_data = [
            ['Approved by:', '_'*40],
            ['Date:', '_'*40],
            ['', ''],
            ['Notes/Changes Required:', '']
        ]
        sig_table = Table(sig_data, colWidths=[2*inch, 4.5*inch])
        sig_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 1), 15),
        ]))
        story.append(sig_table)
        
        doc.build(story)
        
    async def run(self) -> Dict[str, Any]:
        """Main execution method"""
        print(f"\n{'='*70}")
        print(f"📋 STATION 14: SIMPLE EPISODE BLUEPRINT")
        print(f"{'='*70}")
        print(f"Session ID: {self.session_id}\n")
        
        try:
            await self.initialize()
            
            # Load dependencies
            print("📥 Loading dependencies from all previous stations...")
            dependencies = await self.load_dependencies()
            
            if not dependencies.get('season_architecture'):
                raise ValueError("Missing season_architecture from Station 5")
            if not dependencies.get('character_bible'):
                raise ValueError("Missing character_bible from Station 8")
                
            print("✅ Dependencies loaded\n")
            
            # Get episode list
            season_data = dependencies.get('season_architecture', {})
            episodes = season_data.get('episodes', [])
            total_episodes = len(episodes)
            
            print(f"📺 Generating blueprints for {total_episodes} episodes...\n")
            
            blueprint_bible = {
                'session_id': self.session_id,
                'generated_at': datetime.now().isoformat(),
                'total_episodes': total_episodes,
                'episodes': []
            }
            
            # Generate blueprint for each episode
            for idx, episode in enumerate(episodes):
                episode_num = idx + 1
                print(f"📝 Episode {episode_num}/{total_episodes}: Generating blueprint...")
                
                episode_blueprint = await self.generate_episode_blueprint(
                    episode_num,
                    episode,
                    dependencies
                )
                
                episode_blueprint['episode_number'] = episode_num
                episode_blueprint['episode_title'] = episode.get('title', f'Episode {episode_num}')
                
                blueprint_bible['episodes'].append(episode_blueprint)
                print(f"✅ Episode {episode_num} blueprint complete\n")
            
            # Generate season overview
            print("🎬 Generating season narrative overview...")
            season_overview = await self.generate_season_overview(
                blueprint_bible['episodes'],
                dependencies
            )
            blueprint_bible['season_overview'] = season_overview
            print("✅ Season overview complete\n")
            
            # Generate approval checklist
            print("✅ Generating approval checklist...")
            approval_checklist = await self.generate_approval_checklist(
                blueprint_bible['episodes'],
                dependencies
            )
            blueprint_bible['approval_checklist'] = approval_checklist
            print("✅ Approval checklist complete\n")
            
            # Export outputs
            print("💾 Exporting blueprint outputs...")
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            base_filename = f"station14_episode_blueprint_{self.session_id}"
            
            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            json_path = os.path.join(output_dir, f"{base_filename}.json")
            pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
            
            self.export_txt(blueprint_bible, txt_path)
            print(f"  ✅ Text (Human Review): {txt_path}")
            
            self.export_json(blueprint_bible, json_path)
            print(f"  ✅ JSON (Data): {json_path}")
            
            self.export_pdf(blueprint_bible, pdf_path)
            print(f"  ✅ PDF (Approval Doc): {pdf_path}")
            
            # Save to Redis
            print("\n💾 Saving to Redis...")
            await self.redis_client.set(
                f"audiobook:{self.session_id}:station_14",
                json.dumps(blueprint_bible)
            )
            print("✅ Saved to Redis\n")
            
            result = {
                'station': 'station_14_episode_blueprint',
                'status': 'complete',
                'outputs': {
                    'txt': txt_path,
                    'json': json_path,
                    'pdf': pdf_path
                },
                'statistics': {
                    'total_episodes': total_episodes,
                    'blueprints_generated': len(blueprint_bible['episodes']),
                    'ready_for_approval': True
                },
                'blueprint_bible': blueprint_bible
            }
            
            print(f"{'='*70}")
            print(f"✅ STATION 14 COMPLETE: Episode Blueprints Ready for Human Approval")
            print(f"{'='*70}\n")
            print(f"📄 Review Document: {pdf_path}")
            print(f"👤 HUMAN GATE: Please review and approve blueprints before proceeding\n")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error in Station 14: {str(e)}")
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
        station = Station14EpisodeBlueprint(session_id)
        result = await station.run()
        print("\n📊 Station 14 Results:")
        print(json.dumps(result['statistics'], indent=2))
    
    asyncio.run(main())