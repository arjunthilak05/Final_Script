#!/usr/bin/env python3
"""
Station 11: Runtime Planning for Audio Episodes

This station creates comprehensive runtime planning with 4 major sections:
1. Episode Breakdown - Total runtime targets and segment allocation
2. Word Budgets - Spoken words per minute, dialogue vs narration ratios
3. Pacing Variation - Fast, slow, standard, and special format episodes
4. Series Totals - Total runtime, word count, average pace, variation range

Dependencies: Station 5 (Season Architecture), Station 10 (Narrative Reveal Strategy)
Outputs: Complete Runtime Planning Grid with TXT, JSON, and PDF exports
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EpisodeType(Enum):
    STANDARD = "Standard"
    FAST_PACED = "Fast Paced"
    SLOW_PACED = "Slow Paced"
    SPECIAL_FORMAT = "Special Format"
    PREMIERE = "Premiere"
    FINALE = "Finale"

class SegmentType(Enum):
    TEASER_COLD_OPEN = "Teaser/Cold Open"
    ACT_1 = "Act 1"
    ACT_2 = "Act 2"
    ACT_3 = "Act 3"
    TAG_CREDITS = "Tag/Credits"

@dataclass
class EpisodeSegment:
    """Individual segment within an episode"""
    segment_type: SegmentType
    duration_minutes: float
    word_count: int
    purpose: str
    pacing_notes: str

@dataclass
class EpisodeBreakdown:
    """Complete breakdown for a single episode"""
    episode_number: int
    episode_type: EpisodeType
    total_runtime_minutes: float
    segments: List[EpisodeSegment]
    total_word_count: int
    pacing_style: str
    special_considerations: List[str]

@dataclass
class WordBudget:
    """Word budget specifications"""
    spoken_words_per_minute: int
    total_words_per_episode: int
    dialogue_ratio: float  # 0.0 to 1.0
    narration_ratio: float  # 0.0 to 1.0
    sfx_silence_allowance: float  # percentage
    word_count_variation_range: str

@dataclass
class PacingVariation:
    """Pacing variation specifications"""
    fast_episodes: Dict[str, Any]
    slow_episodes: Dict[str, Any]
    standard_episodes: Dict[str, Any]
    special_format_episodes: Dict[str, Any]
    pacing_rhythm: str
    audience_engagement_strategy: str

@dataclass
class SeriesTotals:
    """Series-wide runtime and word count totals"""
    total_runtime_hours: float
    total_word_count: int
    average_pace_words_per_minute: float
    variation_range_minutes: str
    total_episodes: int
    average_episode_length: float
    production_timeline_estimate: str

@dataclass
class RuntimePlanningGrid:
    """Complete runtime planning strategy"""
    episode_breakdowns: List[EpisodeBreakdown]
    word_budgets: WordBudget
    pacing_variations: PacingVariation
    series_totals: SeriesTotals
    production_guidelines: Dict[str, str]
    audio_specific_considerations: Dict[str, str]
    quality_control_metrics: Dict[str, str]

class Station11RuntimePlanning:
    """Station 11: Runtime Planning Builder"""

    def __init__(self):
        self.openrouter_agent = OpenRouterAgent()
        self.redis_client = RedisClient()
        self.settings = Settings()
        self.debug_mode = False

    def enable_debug_mode(self):
        """Enable debug mode for detailed logging"""
        self.debug_mode = True
        logger.setLevel(logging.DEBUG)
        logger.debug("🐛 Debug mode enabled for Station 11")

    async def initialize(self):
        """Initialize the station (compatibility with other stations)"""
        await self.redis_client.initialize()
        logger.info("✅ Station 11 Runtime Planning initialized")
        
    async def process(self, session_id: str) -> Dict[str, Any]:
        """Main processing function for Station 11"""
        logger.info(f"Starting Station 11: Runtime Planning for session {session_id}")
        
        try:
            # Get dependencies
            dependencies = await self._get_dependencies(session_id)
            
            # Build runtime planning grid
            runtime_grid = await self._build_runtime_planning_grid(dependencies)
            
            # Generate outputs
            outputs = await self._generate_outputs(runtime_grid, session_id)
            
            # Save to Redis
            await self._save_to_redis(runtime_grid, session_id)
            
            logger.info(f"Station 11 completed successfully for session {session_id}")
            return outputs
            
        except Exception as e:
            logger.error(f"Station 11 failed for session {session_id}: {str(e)}")
            raise
    
    async def _get_dependencies(self, session_id: str) -> Dict[str, Any]:
        """Get required dependencies from previous stations"""
        dependencies = {}
        
        # Get Station 5: Season Architecture
        season_architecture_data = await self.redis_client.get(f"audiobook:{session_id}:station_05")
        if season_architecture_data:
            import json
            dependencies['season_architecture'] = json.loads(season_architecture_data)
        else:
            logger.warning("Station 5 output not found, using fallback")
            dependencies['season_architecture'] = {"total_episodes": 10, "chosen_style": "Standard"}
        
        # Get Station 10: Narrative Reveal Strategy
        reveal_strategy_data = await self.redis_client.get(f"audiobook:{session_id}:station_10")
        if reveal_strategy_data:
            import json
            dependencies['reveal_strategy'] = json.loads(reveal_strategy_data)
        else:
            logger.warning("Station 10 output not found, using fallback")
            dependencies['reveal_strategy'] = {"information_taxonomy": [], "reveal_methods": []}
        
        return dependencies
    
    async def _build_runtime_planning_grid(self, dependencies: Dict[str, Any]) -> RuntimePlanningGrid:
        """Build the complete runtime planning strategy"""

        # Extract story information
        # Use episode_grid length as source of truth, not total_episodes field which may be wrong
        episode_grid = dependencies['season_architecture'].get('episodes',
                       dependencies['season_architecture'].get('episode_grid', []))
        total_episodes = len(episode_grid) if episode_grid else dependencies['season_architecture'].get('total_episodes', 10)
        chosen_style = dependencies['season_architecture'].get('chosen_style', 'Standard')
        information_taxonomy = dependencies['reveal_strategy'].get('information_taxonomy', [])
        
        # Build episode breakdowns
        episode_breakdowns = await self._build_episode_breakdowns(
            total_episodes, chosen_style, information_taxonomy
        )
        
        # Build word budgets
        word_budgets = await self._build_word_budgets(
            total_episodes, chosen_style
        )
        
        # Build pacing variations
        pacing_variations = await self._build_pacing_variations(
            total_episodes, chosen_style, information_taxonomy
        )
        
        # Build series totals
        series_totals = await self._build_series_totals(
            episode_breakdowns, word_budgets
        )
        
        # Build production guidelines
        production_guidelines = await self._build_production_guidelines(
            chosen_style, total_episodes
        )
        
        # Build audio-specific considerations
        audio_considerations = await self._build_audio_considerations(
            chosen_style, pacing_variations
        )
        
        # Build quality control metrics
        quality_metrics = await self._build_quality_control_metrics(
            episode_breakdowns, word_budgets
        )
        
        return RuntimePlanningGrid(
            episode_breakdowns=episode_breakdowns,
            word_budgets=word_budgets,
            pacing_variations=pacing_variations,
            series_totals=series_totals,
            production_guidelines=production_guidelines,
            audio_specific_considerations=audio_considerations,
            quality_control_metrics=quality_metrics
        )
    
    async def _build_episode_breakdowns(self, total_episodes: int, chosen_style: str, information_taxonomy: List[Dict]) -> List[EpisodeBreakdown]:
        """Build detailed episode breakdowns"""
        
        prompt = f"""
        You are the Runtime Planner for audio episodes. Create detailed episode breakdowns for this audiobook series:
        
        TOTAL EPISODES: {total_episodes}
        CHOSEN STYLE: {chosen_style}
        STORY COMPLEXITY: {len(information_taxonomy)} information items to reveal
        
        For each episode, create a breakdown with:
        
        1. EPISODE TYPE:
        - Standard: Normal pacing and structure
        - Fast Paced: High word count, rapid reveals
        - Slow Paced: More silence/SFX, contemplative
        - Special Format: Unique structure (flashback, interview, etc.)
        - Premiere: Episode 1 special considerations
        - Finale: Last episode special considerations
        
        2. SEGMENT ALLOCATION:
        - Teaser/Cold Open: 2-5 minutes
        - Act 1: 15-25 minutes
        - Act 2: 20-30 minutes  
        - Act 3: 15-25 minutes
        - Tag/Credits: 1-3 minutes
        
        3. TOTAL RUNTIME TARGET: 45-60 minutes per episode
        
        4. PACING STYLE: How this episode fits the overall rhythm
        
        5. SPECIAL CONSIDERATIONS: Any unique requirements
        
        Create breakdowns for all {total_episodes} episodes. Vary the pacing and structure to create engaging rhythm.
        
        Return as JSON array of episode breakdowns.
        """
        
        response = await self.openrouter_agent.generate(prompt)
        
        try:
            episodes_data = json.loads(response)
            episode_breakdowns = []

            for idx, ep_data in enumerate(episodes_data, start=1):
                # Ensure ep_data is a dictionary
                if not isinstance(ep_data, dict):
                    logger.warning(f"Episode data is not a dict: {type(ep_data)} = {ep_data}")
                    continue

                # Map episode type string to enum
                type_map = {
                    "Standard": EpisodeType.STANDARD,
                    "Fast Paced": EpisodeType.FAST_PACED,
                    "Slow Paced": EpisodeType.SLOW_PACED,
                    "Special Format": EpisodeType.SPECIAL_FORMAT,
                    "Premiere": EpisodeType.PREMIERE,
                    "Finale": EpisodeType.FINALE
                }

                episode_type = type_map.get(ep_data.get('episode_type', 'Standard'), EpisodeType.STANDARD)

                # Build segments
                segments = []
                segments_data = ep_data.get('segments', [])
                if not isinstance(segments_data, list):
                    logger.warning(f"Segments data is not a list: {type(segments_data)} = {segments_data}")
                    segments_data = []

                for seg_data in segments_data:
                    # Ensure seg_data is a dictionary
                    if not isinstance(seg_data, dict):
                        logger.warning(f"Segment data is not a dict: {type(seg_data)} = {seg_data}")
                        continue

                    # Map segment type string to enum
                    seg_type_map = {
                        "Teaser/Cold Open": SegmentType.TEASER_COLD_OPEN,
                        "Act 1": SegmentType.ACT_1,
                        "Act 2": SegmentType.ACT_2,
                        "Act 3": SegmentType.ACT_3,
                        "Tag/Credits": SegmentType.TAG_CREDITS
                    }

                    segment_type = seg_type_map.get(seg_data.get('segment_type', 'Act 1'), SegmentType.ACT_1)

                    segments.append(EpisodeSegment(
                        segment_type=segment_type,
                        duration_minutes=seg_data.get('duration_minutes', 15.0),
                        word_count=seg_data.get('word_count', 2000),
                        purpose=seg_data.get('purpose', ''),
                        pacing_notes=seg_data.get('pacing_notes', '')
                    ))

                # Use enumerated index if episode_number is missing or incorrect
                episode_num = ep_data.get('episode_number', idx)
                if episode_num == 1 and idx > 1:
                    # LLM likely failed to provide correct episode numbers, use index
                    episode_num = idx

                episode_breakdowns.append(EpisodeBreakdown(
                    episode_number=episode_num,
                    episode_type=episode_type,
                    total_runtime_minutes=ep_data.get('total_runtime_minutes', 50.0),
                    segments=segments,
                    total_word_count=ep_data.get('total_word_count', 8000),
                    pacing_style=ep_data.get('pacing_style', ''),
                    special_considerations=ep_data.get('special_considerations', [])
                ))

            return episode_breakdowns
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse episode breakdowns, using fallback")
            return self._create_fallback_episode_breakdowns(total_episodes)
    
    async def _build_word_budgets(self, total_episodes: int, chosen_style: str) -> WordBudget:
        """Build word budget specifications"""
        
        prompt = f"""
        You are the Runtime Planner. Create word budget specifications for this audiobook series:
        
        TOTAL EPISODES: {total_episodes}
        CHOSEN STYLE: {chosen_style}
        
        Calculate optimal word budgets considering:
        
        1. SPOKEN WORDS PER MINUTE: 150-160 words (typical for audiobooks)
        2. TOTAL WORDS PER EPISODE: Based on 45-60 minute episodes
        3. DIALOGUE VS NARRATION RATIO: 
           - Dialogue: 60-70% (character interactions)
           - Narration: 30-40% (description, exposition)
        4. SFX/SILENCE ALLOWANCE: 5-10% of total time
        5. WORD COUNT VARIATION RANGE: ±15% for pacing variety
        
        Consider the chosen style's impact on word density and pacing.
        
        Return as JSON object with word budget specifications.
        """
        
        response = await self.openrouter_agent.generate(prompt)
        
        try:
            budget_data = json.loads(response)
            
            return WordBudget(
                spoken_words_per_minute=budget_data.get('spoken_words_per_minute', 155),
                total_words_per_episode=budget_data.get('total_words_per_episode', 8000),
                dialogue_ratio=budget_data.get('dialogue_ratio', 0.65),
                narration_ratio=budget_data.get('narration_ratio', 0.35),
                sfx_silence_allowance=budget_data.get('sfx_silence_allowance', 0.08),
                word_count_variation_range=budget_data.get('word_count_variation_range', '±15%')
            )
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse word budgets, using fallback")
            return self._create_fallback_word_budget()
    
    async def _build_pacing_variations(self, total_episodes: int, chosen_style: str, information_taxonomy: List[Dict]) -> PacingVariation:
        """Build pacing variation specifications"""
        
        prompt = f"""
        You are the Runtime Planner. Create pacing variation specifications for this audiobook series:
        
        TOTAL EPISODES: {total_episodes}
        CHOSEN STYLE: {chosen_style}
        STORY COMPLEXITY: {len(information_taxonomy)} information items to reveal
        
        Design pacing variations to create engaging rhythm:
        
        1. FAST EPISODES (20-30% of series):
        - High word count (160+ words/minute)
        - Rapid reveals and action
        - Minimal silence/SFX
        - Target episodes: 3, 7, 10 (example)
        
        2. SLOW EPISODES (15-25% of series):
        - Lower word count (140-150 words/minute)
        - More silence and SFX
        - Contemplative moments
        - Character development focus
        
        3. STANDARD EPISODES (50-60% of series):
        - Normal pacing (150-155 words/minute)
        - Balanced dialogue/narration
        - Regular structure
        
        4. SPECIAL FORMAT EPISODES (5-10% of series):
        - Unique structure (flashback, interview, etc.)
        - Custom pacing requirements
        - Experimental audio techniques
        
        5. PACING RHYTHM: How episodes flow together
        6. AUDIENCE ENGAGEMENT STRATEGY: Maintaining interest across series
        
        Return as JSON object with pacing variation specifications.
        """
        
        response = await self.openrouter_agent.generate(prompt)
        
        try:
            pacing_data = json.loads(response)
            
            return PacingVariation(
                fast_episodes=pacing_data.get('fast_episodes', {}),
                slow_episodes=pacing_data.get('slow_episodes', {}),
                standard_episodes=pacing_data.get('standard_episodes', {}),
                special_format_episodes=pacing_data.get('special_format_episodes', {}),
                pacing_rhythm=pacing_data.get('pacing_rhythm', ''),
                audience_engagement_strategy=pacing_data.get('audience_engagement_strategy', '')
            )
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse pacing variations, using fallback")
            return self._create_fallback_pacing_variations(total_episodes)
    
    async def _build_series_totals(self, episode_breakdowns: List[EpisodeBreakdown], word_budgets: WordBudget) -> SeriesTotals:
        """Build series-wide totals and estimates"""
        
        # Calculate totals from episode breakdowns
        total_runtime_minutes = sum(ep.total_runtime_minutes for ep in episode_breakdowns)
        total_runtime_hours = total_runtime_minutes / 60.0
        total_word_count = sum(ep.total_word_count for ep in episode_breakdowns)
        average_pace = total_word_count / total_runtime_minutes if total_runtime_minutes > 0 else 0
        
        # Calculate variation range
        episode_lengths = [ep.total_runtime_minutes for ep in episode_breakdowns]
        min_length = min(episode_lengths)
        max_length = max(episode_lengths)
        variation_range = f"{min_length:.1f} - {max_length:.1f} minutes"
        
        # Estimate production timeline
        total_episodes = len(episode_breakdowns)
        if total_episodes <= 5:
            timeline = "2-3 months"
        elif total_episodes <= 10:
            timeline = "4-6 months"
        elif total_episodes <= 20:
            timeline = "6-9 months"
        else:
            timeline = "9-12 months"
        
        return SeriesTotals(
            total_runtime_hours=total_runtime_hours,
            total_word_count=total_word_count,
            average_pace_words_per_minute=average_pace,
            variation_range_minutes=variation_range,
            total_episodes=total_episodes,
            average_episode_length=total_runtime_minutes / total_episodes if total_episodes > 0 else 0,
            production_timeline_estimate=timeline
        )
    
    async def _build_production_guidelines(self, chosen_style: str, total_episodes: int) -> Dict[str, str]:
        """Build production guidelines for runtime planning"""
        
        guidelines = {
            "overall_approach": f"Audio-first production optimized for {chosen_style} style",
            "recording_schedule": f"Plan for {total_episodes} episodes with flexible pacing",
            "word_count_management": "Monitor word counts per segment to maintain pacing",
            "silence_utilization": "Strategic use of silence and SFX for pacing control",
            "quality_control": "Regular runtime checks during production",
            "audience_retention": "Vary pacing to maintain engagement across series"
        }
        
        return guidelines
    
    async def _build_audio_considerations(self, chosen_style: str, pacing_variations: PacingVariation) -> Dict[str, str]:
        """Build audio-specific considerations"""
        
        considerations = {
            "recording_techniques": "Adapt recording pace to episode type (fast/slow/standard)",
            "sound_design": "Use SFX and music to support pacing variations",
            "voice_acting": "Adjust performance intensity based on episode pacing",
            "post_production": "Fine-tune pacing in post through editing and effects",
            "listening_experience": "Ensure smooth transitions between different pacing styles",
            "accessibility": "Maintain consistent audio quality across all pacing variations"
        }
        
        return considerations
    
    async def _build_quality_control_metrics(self, episode_breakdowns: List[EpisodeBreakdown], word_budgets: WordBudget) -> Dict[str, str]:
        """Build quality control metrics for runtime planning"""
        
        # Calculate actual metrics
        total_episodes = len(episode_breakdowns)
        avg_runtime = sum(ep.total_runtime_minutes for ep in episode_breakdowns) / total_episodes if total_episodes > 0 else 0
        avg_word_count = sum(ep.total_word_count for ep in episode_breakdowns) / total_episodes if total_episodes > 0 else 0
        
        metrics = {
            "target_runtime_range": f"45-60 minutes per episode (avg: {avg_runtime:.1f})",
            "target_word_count_range": f"7,000-9,000 words per episode (avg: {avg_word_count:.0f})",
            "pacing_consistency": "Maintain ±15% variation for engagement",
            "segment_balance": "Ensure proper act structure in each episode",
            "series_rhythm": "Vary pacing to create engaging overall flow",
            "production_efficiency": "Optimize recording schedule based on episode types"
        }
        
        return metrics
    
    async def _generate_outputs(self, runtime_grid: RuntimePlanningGrid, session_id: str) -> Dict[str, Any]:
        """Generate formatted outputs"""
        
        # Create output directory
        output_dir = Path(f"outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate TXT output
        txt_output = self._format_txt_output(runtime_grid)
        txt_path = output_dir / f"station11_runtime_planning_{session_id}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_output)
        
        # Generate JSON output
        json_output = self._format_json_output(runtime_grid)
        json_path = output_dir / f"station11_runtime_planning_{session_id}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=2, ensure_ascii=False)

        # Generate PDF output
        pdf_path = output_dir / f"station11_runtime_planning_{session_id}.pdf"
        try:
            pdf_output = self._format_pdf_output(runtime_grid)
            with open(pdf_path, 'wb') as f:
                f.write(pdf_output)
            has_pdf = True
        except Exception as e:
            logger.warning(f"PDF generation failed: {e}")
            has_pdf = False

        outputs = {
            "txt": str(txt_path),
            "json": str(json_path)
        }
        if has_pdf:
            outputs["pdf"] = str(pdf_path)

        return {
            "status": "success",
            "outputs": outputs,
            "summary": {
                "total_episodes": len(runtime_grid.episode_breakdowns),
                "total_runtime_hours": runtime_grid.series_totals.total_runtime_hours,
                "total_word_count": runtime_grid.series_totals.total_word_count,
                "average_pace": runtime_grid.series_totals.average_pace_words_per_minute
            }
        }
    
    def _format_txt_output(self, runtime_grid: RuntimePlanningGrid) -> str:
        """Format runtime planning grid as readable text"""
        
        output = []
        output.append("=" * 80)
        output.append("RUNTIME PLANNING GRID - COMPLETE STRATEGY")
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 80)
        output.append("")
        
        # Section 1: Episode Breakdowns
        output.append("=== EPISODE BREAKDOWNS ===")
        output.append("")
        for episode in runtime_grid.episode_breakdowns:
            output.append(f"Episode {episode.episode_number}: {episode.episode_type.value}")
            output.append(f"  Total Runtime: {episode.total_runtime_minutes:.1f} minutes")
            output.append(f"  Total Word Count: {episode.total_word_count:,} words")
            output.append(f"  Pacing Style: {episode.pacing_style}")
            output.append("  Segments:")
            for segment in episode.segments:
                output.append(f"    • {segment.segment_type.value}: {segment.duration_minutes:.1f} min, {segment.word_count:,} words")
                output.append(f"      Purpose: {segment.purpose}")
                if segment.pacing_notes:
                    output.append(f"      Pacing: {segment.pacing_notes}")
            if episode.special_considerations:
                output.append("  Special Considerations:")
                for consideration in episode.special_considerations:
                    output.append(f"    - {consideration}")
            output.append("")
        
        # Section 2: Word Budgets
        output.append("=== WORD BUDGETS ===")
        output.append("")
        output.append(f"Spoken Words per Minute: {runtime_grid.word_budgets.spoken_words_per_minute}")
        output.append(f"Total Words per Episode: {runtime_grid.word_budgets.total_words_per_episode:,}")
        output.append(f"Dialogue Ratio: {runtime_grid.word_budgets.dialogue_ratio:.1%}")
        output.append(f"Narration Ratio: {runtime_grid.word_budgets.narration_ratio:.1%}")
        output.append(f"SFX/Silence Allowance: {runtime_grid.word_budgets.sfx_silence_allowance:.1%}")
        output.append(f"Word Count Variation Range: {runtime_grid.word_budgets.word_count_variation_range}")
        output.append("")
        
        # Section 3: Pacing Variations
        output.append("=== PACING VARIATIONS ===")
        output.append("")
        output.append("Fast Episodes:")
        for key, value in runtime_grid.pacing_variations.fast_episodes.items():
            output.append(f"  {key}: {str(value)}")
        output.append("")
        output.append("Slow Episodes:")
        for key, value in runtime_grid.pacing_variations.slow_episodes.items():
            output.append(f"  {key}: {str(value)}")
        output.append("")
        output.append("Standard Episodes:")
        for key, value in runtime_grid.pacing_variations.standard_episodes.items():
            output.append(f"  {key}: {str(value)}")
        output.append("")
        output.append("Special Format Episodes:")
        for key, value in runtime_grid.pacing_variations.special_format_episodes.items():
            output.append(f"  {key}: {str(value)}")
        output.append("")
        output.append(f"Pacing Rhythm: {runtime_grid.pacing_variations.pacing_rhythm}")
        output.append(f"Audience Engagement Strategy: {runtime_grid.pacing_variations.audience_engagement_strategy}")
        output.append("")
        
        # Section 4: Series Totals
        output.append("=== SERIES TOTALS ===")
        output.append("")
        output.append(f"Total Runtime: {runtime_grid.series_totals.total_runtime_hours:.1f} hours")
        output.append(f"Total Word Count: {runtime_grid.series_totals.total_word_count:,} words")
        output.append(f"Average Pace: {runtime_grid.series_totals.average_pace_words_per_minute:.1f} words/minute")
        output.append(f"Variation Range: {runtime_grid.series_totals.variation_range_minutes}")
        output.append(f"Total Episodes: {runtime_grid.series_totals.total_episodes}")
        output.append(f"Average Episode Length: {runtime_grid.series_totals.average_episode_length:.1f} minutes")
        output.append(f"Production Timeline Estimate: {runtime_grid.series_totals.production_timeline_estimate}")
        output.append("")
        
        # Section 5: Production Guidelines
        output.append("=== PRODUCTION GUIDELINES ===")
        output.append("")
        for key, value in runtime_grid.production_guidelines.items():
            output.append(f"{key.replace('_', ' ').title()}: {str(value)}")
            output.append("")

        # Section 6: Audio-Specific Considerations
        output.append("=== AUDIO-SPECIFIC CONSIDERATIONS ===")
        output.append("")
        for key, value in runtime_grid.audio_specific_considerations.items():
            output.append(f"{key.replace('_', ' ').title()}: {str(value)}")
            output.append("")

        # Section 7: Quality Control Metrics
        output.append("=== QUALITY CONTROL METRICS ===")
        output.append("")
        for key, value in runtime_grid.quality_control_metrics.items():
            output.append(f"{key.replace('_', ' ').title()}: {str(value)}")
            output.append("")
        
        output.append("=" * 80)
        output.append("END OF RUNTIME PLANNING GRID")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def _format_json_output(self, runtime_grid: RuntimePlanningGrid) -> Dict[str, Any]:
        """Format runtime planning grid as JSON"""
        
        # Convert enums to strings for JSON serialization
        episode_breakdowns = []
        for episode in runtime_grid.episode_breakdowns:
            episode_dict = asdict(episode)
            episode_dict['episode_type'] = episode.episode_type.value if hasattr(episode.episode_type, 'value') else str(episode.episode_type)
            for segment in episode_dict.get('segments', []):
                if 'segment_type' in segment:
                    segment['segment_type'] = segment['segment_type'].value if hasattr(segment['segment_type'], 'value') else str(segment['segment_type'])
            episode_breakdowns.append(episode_dict)
        
        return {
            "episode_breakdowns": episode_breakdowns,
            "word_budgets": asdict(runtime_grid.word_budgets),
            "pacing_variations": asdict(runtime_grid.pacing_variations),
            "series_totals": asdict(runtime_grid.series_totals),
            "production_guidelines": runtime_grid.production_guidelines,
            "audio_specific_considerations": runtime_grid.audio_specific_considerations,
            "quality_control_metrics": runtime_grid.quality_control_metrics,
            "generated_at": datetime.now().isoformat()
        }
    
    async def _save_to_redis(self, runtime_grid: RuntimePlanningGrid, session_id: str):
        """Save runtime planning grid to Redis"""
        
        key = f"audiobook:{session_id}:station_11"
        data = self._format_json_output(runtime_grid)
        import json
        json_data = json.dumps(data, default=str)
        await self.redis_client.set(key, json_data, expire=86400)  # 24 hour TTL
        logger.info(f"Saved runtime planning grid to Redis: {key}")
    
    # Fallback methods for error handling
    
    def _create_fallback_episode_breakdowns(self, total_episodes: int) -> List[EpisodeBreakdown]:
        """Create fallback episode breakdowns"""
        breakdowns = []
        
        for i in range(1, total_episodes + 1):
            # Determine episode type
            if i == 1:
                episode_type = EpisodeType.PREMIERE
            elif i == total_episodes:
                episode_type = EpisodeType.FINALE
            elif i % 3 == 0:
                episode_type = EpisodeType.FAST_PACED
            elif i % 5 == 0:
                episode_type = EpisodeType.SLOW_PACED
            else:
                episode_type = EpisodeType.STANDARD
            
            # Create segments
            segments = [
                EpisodeSegment(
                    segment_type=SegmentType.TEASER_COLD_OPEN,
                    duration_minutes=3.0,
                    word_count=500,
                    purpose="Hook audience",
                    pacing_notes="Fast-paced opening"
                ),
                EpisodeSegment(
                    segment_type=SegmentType.ACT_1,
                    duration_minutes=20.0,
                    word_count=3000,
                    purpose="Setup and character development",
                    pacing_notes="Steady build"
                ),
                EpisodeSegment(
                    segment_type=SegmentType.ACT_2,
                    duration_minutes=25.0,
                    word_count=3500,
                    purpose="Rising action and conflict",
                    pacing_notes="Increasing tension"
                ),
                EpisodeSegment(
                    segment_type=SegmentType.ACT_3,
                    duration_minutes=20.0,
                    word_count=3000,
                    purpose="Climax and resolution",
                    pacing_notes="Peak intensity"
                ),
                EpisodeSegment(
                    segment_type=SegmentType.TAG_CREDITS,
                    duration_minutes=2.0,
                    word_count=300,
                    purpose="Wrap-up and credits",
                    pacing_notes="Gentle conclusion"
                )
            ]
            
            breakdowns.append(EpisodeBreakdown(
                episode_number=i,
                episode_type=episode_type,
                total_runtime_minutes=70.0,
                segments=segments,
                total_word_count=10300,
                pacing_style="Balanced with variation",
                special_considerations=["Standard structure"]
            ))
        
        return breakdowns
    
    def _create_fallback_word_budget(self) -> WordBudget:
        """Create fallback word budget"""
        return WordBudget(
            spoken_words_per_minute=155,
            total_words_per_episode=8000,
            dialogue_ratio=0.65,
            narration_ratio=0.35,
            sfx_silence_allowance=0.08,
            word_count_variation_range="±15%"
        )
    
    def _create_fallback_pacing_variations(self, total_episodes: int) -> PacingVariation:
        """Create fallback pacing variations"""
        return PacingVariation(
            fast_episodes={
                "target_episodes": "3, 7, 10",
                "word_count": "160+ words/minute",
                "characteristics": "Rapid reveals, minimal silence"
            },
            slow_episodes={
                "target_episodes": "5, 8",
                "word_count": "140-150 words/minute", 
                "characteristics": "Contemplative, more SFX"
            },
            standard_episodes={
                "target_episodes": "1, 2, 4, 6, 9",
                "word_count": "150-155 words/minute",
                "characteristics": "Balanced pacing"
            },
            special_format_episodes={
                "target_episodes": "None planned",
                "characteristics": "Unique structure if needed"
            },
            pacing_rhythm="Alternating fast and slow episodes for engagement",
            audience_engagement_strategy="Vary pacing to maintain interest"
        )

    def _format_pdf_output(self, runtime_grid: RuntimePlanningGrid) -> bytes:
        """Format runtime planning grid as PDF"""
        try:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)

            # Title
            pdf.cell(0, 10, "RUNTIME PLANNING GRID", ln=True, align="C")
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
            pdf.ln(5)

            # Series Totals
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "SERIES TOTALS", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, f"Total Episodes: {runtime_grid.series_totals.total_episodes}", ln=True)
            pdf.cell(0, 6, f"Total Runtime: {runtime_grid.series_totals.total_runtime_hours:.1f} hours", ln=True)
            pdf.cell(0, 6, f"Total Word Count: {runtime_grid.series_totals.total_word_count:,} words", ln=True)
            pdf.cell(0, 6, f"Average Pace: {runtime_grid.series_totals.average_pace_words_per_minute:.1f} words/min", ln=True)
            pdf.ln(5)

            # Episode Breakdowns
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "EPISODE BREAKDOWNS", ln=True)
            pdf.set_font("Arial", "", 9)

            for episode in runtime_grid.episode_breakdowns:
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 6, f"Episode {episode.episode_number}: {episode.episode_type.value}", ln=True)
                pdf.set_font("Arial", "", 9)
                pdf.cell(0, 5, f"  Runtime: {episode.total_runtime_minutes:.1f} min | Words: {episode.total_word_count:,}", ln=True)

                # Truncate pacing style if too long
                pacing = episode.pacing_style[:120] + "..." if len(episode.pacing_style) > 120 else episode.pacing_style
                pdf.multi_cell(0, 5, f"  Pacing: {pacing}")
                pdf.ln(2)

            # Word Budgets
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "WORD BUDGETS", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, f"Spoken Words/Min: {runtime_grid.word_budgets.spoken_words_per_minute}", ln=True)
            pdf.cell(0, 6, f"Total Words/Episode: {runtime_grid.word_budgets.total_words_per_episode:,}", ln=True)
            pdf.cell(0, 6, f"Dialogue Ratio: {runtime_grid.word_budgets.dialogue_ratio:.1%}", ln=True)
            pdf.cell(0, 6, f"Narration Ratio: {runtime_grid.word_budgets.narration_ratio:.1%}", ln=True)
            pdf.ln(5)

            # Production Guidelines
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "PRODUCTION GUIDELINES", ln=True)
            pdf.set_font("Arial", "", 9)
            for key, value in runtime_grid.production_guidelines.items():
                value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                pdf.multi_cell(0, 5, f"{key}: {value_str}")
                pdf.ln(1)

            return pdf.output(dest='S').encode('latin-1')

        except ImportError:
            logger.warning("fpdf not installed, generating text-based PDF")
            # Fallback: return text as bytes
            txt_output = self._format_txt_output(runtime_grid)
            return txt_output.encode('utf-8')

# Main execution
async def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python station_11_runtime_planning.py <session_id>")
        sys.exit(1)
    
    session_id = sys.argv[1]
    
    station = Station11RuntimePlanning()
    result = await station.process(session_id)
    
    print(f"\n{'='*80}")
    print("Station 11: Runtime Planning - COMPLETE")
    print(f"{'='*80}")
    print(f"Status: {result['status']}")
    print(f"Outputs: {json.dumps(result['outputs'], indent=2)}")
    print(f"Summary: {json.dumps(result['summary'], indent=2)}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(main())
