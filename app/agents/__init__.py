"""
Agents module for the Audiobook Production Automation System

This module contains all the station agents that form the 45-station
production pipeline for automated audiobook script creation.
"""

from .station_01_seed_processor import Station01SeedProcessor
from .station_02_project_dna_builder import Station02ProjectDNABuilder
from .station_03_age_genre_optimizer import Station03AgeGenreOptimizer
from .station_04_reference_mining import Station04ReferenceMining
from .station_045_narrator_strategy_designer import Station045NarratorStrategyDesigner
from .station_05_season_architect import Station05SeasonArchitect
from .station_06_master_style_guide_builder import Station06MasterStyleGuideBuilder
from .station_07_character_architect import Station07CharacterArchitect
from .station_08_world_builder import Station08WorldBuilder
from .station_09_world_building_system import Station09WorldBuildingSystem
from .station_10_narrative_reveal_strategy import Station10NarrativeRevealStrategy
from .station_11_runtime_planner import Station11RuntimePlanner
from .station_12_hook_cliffhanger_designer import Station12HookCliffhangerDesigner
from .station_13_multi_world_timeline_manager import Station13MultiWorldTimelineManager
from .station_14_simple_episode_blueprint import Station14SimpleEpisodeBlueprint
from .station_15_detailed_episode_outlining import Station15DetailedEpisodeOutlining
from .station_16_canon_check import Station16CanonCheck
from .station_17_dialect_planning import Station17DialectPlanning
from .station_18_evergreen_check import Station18EvergreenCheck
from .station_19_procedure_check import Station19ProcedureCheck
from .station_20_geography_transit import Station20GeographyTransit
from .station_21_first_draft import Station21FirstDraft
from .station_22_momentum_check import Station22MomentumCheck
from .station_23_twist_integration import Station23TwistIntegration
from .station_24_dialogue_polish import Station24DialoguePolish
from .station_25_audio_optimization import Station25AudioOptimization
from .station_26_final_script_lock import Station26FinalScriptLock
from .station_27_master_script_assembly import Station27MasterScriptAssembly
from .station_28_emotional_truth_validator import Station28EmotionalTruthValidator
from .station_29_heroic_journey_auditor import Station29HeroicJourneyAuditor
from .station_30_structure_integrity_checker import Station30StructureIntegrityChecker
from .station_31_dialogue_naturalness import Station31DialogueNaturalness
from .station_32_audio_clarity_auditor import Station32AudioClarityAuditor
from .station_33_pacing_energy_analyzer import Station33PacingEnergyAnalyzer
from .station_34_world_consistency_validator import Station34WorldConsistencyValidator
from .station_35_character_voice_distinction import Station35CharacterVoiceDistinction
from .station_36_music_sfx_hygiene import Station36MusicSfxHygiene
from .station_37_plant_payoff_tracker import Station37PlantPayoffTracker
from .station_38_redundancy_eliminator import Station38RedundancyEliminator

__all__ = [
    'Station01SeedProcessor',
    'Station02ProjectDNABuilder',
    'Station03AgeGenreOptimizer',
    'Station04ReferenceMining',
    'Station045NarratorStrategyDesigner',
    'Station05SeasonArchitect',
    'Station06MasterStyleGuideBuilder',
    'Station07CharacterArchitect',
    'Station08WorldBuilder',
    'Station09WorldBuildingSystem',
    'Station10NarrativeRevealStrategy',
    'Station11RuntimePlanner',
    'Station12HookCliffhangerDesigner',
    'Station13MultiWorldTimelineManager',
    'Station14SimpleEpisodeBlueprint',
    'Station15DetailedEpisodeOutlining',
    'Station16CanonCheck',
    'Station17DialectPlanning',
    'Station18EvergreenCheck',
    'Station19ProcedureCheck',
    'Station20GeographyTransit',
    'Station21FirstDraft',
    'Station22MomentumCheck',
    'Station23TwistIntegration',
    'Station24DialoguePolish',
    'Station25AudioOptimization',
    'Station26FinalScriptLock',
    'Station27MasterScriptAssembly',
    'Station28EmotionalTruthValidator',
    'Station29HeroicJourneyAuditor',
    'Station30StructureIntegrityChecker',
    'Station31DialogueNaturalness',
    'Station32AudioClarityAuditor',
    'Station33PacingEnergyAnalyzer',
    'Station34WorldConsistencyValidator',
    'Station35CharacterVoiceDistinction',
    'Station36MusicSfxHygiene',
    'Station37PlantPayoffTracker',
    'Station38RedundancyEliminator',
]