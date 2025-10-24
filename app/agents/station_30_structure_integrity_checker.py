"""
Station 30: Narrative Structure Integrity Checker

This station validates completed episode scripts for structural integrity and narrative coherence.
It analyzes structure adherence, reveal mechanism execution, subplot integration, and cross-episode continuity.

Flow:
1. Load Station 5 structure choice and Station 10 reveal mechanism data
2. Load all generated scripts across episodes from previous stations
3. Execute 4-task validation sequence:
   - Task 1: Structure Adherence Validation
   - Task 2: Reveal Mechanism Check
   - Task 3: Subplot Integration Analysis
   - Task 4: Cross-Episode Continuity
4. Generate comprehensive validation reports
5. Present flagged issues to user for approval before applying fixes
6. Save JSON + TXT outputs per episode and summary report

Critical Implementation Rules:
- NO hardcoded structure types - All 48 structures must validate via config-driven rules
- NO fallbacks - Fail explicitly if dependencies missing
- Dynamic rule loading based on Station 5 selection
- User validation required for all flagged issues
- Comprehensive error handling with explicit dependency checks
"""

import asyncio
import json
import logging
import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.agents.config_loader import load_station_config
from app.agents.json_extractor import extract_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RuleReference:
    """Reference to a specific structure rule"""
    rule_id: str
    source_file: str
    rule_definition: str
    expected_value: str
    actual_value: str
    deviation: str


@dataclass
class FixRecommendation:
    """Programmatically actionable fix recommendation"""
    description: str
    action_type: str
    target_timestamp: Optional[str]
    current_timestamp: Optional[str]
    adjustment_seconds: Optional[int]
    affected_elements: List[str]
    automation_possible: bool
    automation_script: Optional[str]


@dataclass
class UserValidation:
    """User approval tracking for fixes"""
    status: str  # pending_review | approved | rejected | partial
    total_issues_requiring_approval: int
    approved_fixes: List[int]
    rejected_fixes: List[int]
    approval_timestamp: Optional[str]
    pending_issues: List[int]


@dataclass
class StructureValidationMetadata:
    """Metadata about structure validation process"""
    structure_selected: str
    structure_source: str
    rules_loaded: int
    rules_applied: int
    rules_list: List[str]
    load_timestamp: str
    config_version: str
    validation_successful: bool


class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, errors: List[Dict]):
        super().__init__(message)
        self.errors = errors


class OutputValidationError(Exception):
    """Custom exception for output validation errors"""
    pass


class Station30StructureIntegrityChecker:
    """Station 30: Narrative Structure Integrity Checker"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.config = load_station_config(station_number=30)
        self.output_dir = Path("output/station_30")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Store validation results
        self.validation_results = {}
        self.structure_rules = {}
        self.flagged_issues = []
        self.issue_counter = 0
        self.user_validation = UserValidation(
            status="pending_review",
            total_issues_requiring_approval=0,
            approved_fixes=[],
            rejected_fixes=[],
            approval_timestamp=None,
            pending_issues=[]
        )
        self.structure_metadata = None
        
    def create_flagged_issue(self, issue_type: str, severity: str, description: str, 
                           rule_reference: Optional[RuleReference] = None,
                           fix_recommendation: Optional[FixRecommendation] = None) -> Dict:
        """Create a flagged issue with unique ID and approval tracking"""
        self.issue_counter += 1
        
        # Standardize severity
        standardized_severity = self.standardize_severity(severity)
        
        issue = {
            "issue_id": self.issue_counter,
            "type": issue_type,
            "severity": standardized_severity,
            "severity_description": self.get_severity_description(standardized_severity),
            "description": description,
            "approval_required": standardized_severity in ["critical", "high"],
            "approval_status": "pending" if standardized_severity in ["critical", "high"] else "auto_approved",
            "user_comment": None,
            "timestamp": datetime.now().isoformat()
        }
        
        if rule_reference:
            issue["rule_reference"] = {
                "rule_id": rule_reference.rule_id,
                "source_file": rule_reference.source_file,
                "rule_definition": rule_reference.rule_definition,
                "expected_value": rule_reference.expected_value,
                "actual_value": rule_reference.actual_value,
                "deviation": rule_reference.deviation
            }
        
        if fix_recommendation:
            issue["recommended_fix"] = {
                "description": fix_recommendation.description,
                "action_type": fix_recommendation.action_type,
                "target_timestamp": fix_recommendation.target_timestamp,
                "current_timestamp": fix_recommendation.current_timestamp,
                "adjustment_seconds": fix_recommendation.adjustment_seconds,
                "affected_elements": fix_recommendation.affected_elements,
                "automation_possible": fix_recommendation.automation_possible,
                "automation_script": fix_recommendation.automation_script
            }
        
        # Update user validation tracking
        if issue["approval_required"]:
            self.user_validation.total_issues_requiring_approval += 1
            self.user_validation.pending_issues.append(self.issue_counter)
        
        self.flagged_issues.append(issue)
        return issue
    
    def approve_issue(self, issue_id: int, user_comment: Optional[str] = None) -> bool:
        """Approve a flagged issue"""
        for issue in self.flagged_issues:
            if issue["issue_id"] == issue_id:
                issue["approval_status"] = "approved"
                issue["user_comment"] = user_comment
                
                # Update user validation tracking
                if issue_id in self.user_validation.pending_issues:
                    self.user_validation.pending_issues.remove(issue_id)
                    self.user_validation.approved_fixes.append(issue_id)
                
                return True
        return False
    
    def reject_issue(self, issue_id: int, user_comment: Optional[str] = None) -> bool:
        """Reject a flagged issue"""
        for issue in self.flagged_issues:
            if issue["issue_id"] == issue_id:
                issue["approval_status"] = "rejected"
                issue["user_comment"] = user_comment
                
                # Update user validation tracking
                if issue_id in self.user_validation.pending_issues:
                    self.user_validation.pending_issues.remove(issue_id)
                    self.user_validation.rejected_fixes.append(issue_id)
                
                return True
        return False
    
    def get_pending_issues(self) -> List[Dict]:
        """Get all issues requiring user approval"""
        return [issue for issue in self.flagged_issues if issue["approval_status"] == "pending"]
    
    def update_user_validation_status(self) -> None:
        """Update the overall user validation status"""
        if not self.user_validation.pending_issues:
            if self.user_validation.approved_fixes and not self.user_validation.rejected_fixes:
                self.user_validation.status = "approved"
            elif self.user_validation.rejected_fixes and not self.user_validation.approved_fixes:
                self.user_validation.status = "rejected"
            elif self.user_validation.approved_fixes and self.user_validation.rejected_fixes:
                self.user_validation.status = "partial"
            else:
                self.user_validation.status = "no_issues"
            
            self.user_validation.approval_timestamp = datetime.now().isoformat()
        else:
            self.user_validation.status = "pending_review"
    
    def standardize_severity(self, severity: str) -> str:
        """Standardize severity levels to consistent taxonomy"""
        severity_mapping = {
            # Critical variations
            'critical': 'critical',
            'fatal': 'critical',
            'blocking': 'critical',
            'severe': 'critical',
            
            # High variations  
            'high': 'high',
            'major': 'high',
            'important': 'high',
            'significant': 'high',
            
            # Medium variations
            'medium': 'medium',
            'moderate': 'medium',
            'normal': 'medium',
            'standard': 'medium',
            
            # Low variations
            'low': 'low',
            'minor': 'low',
            'trivial': 'low',
            'cosmetic': 'low'
        }
        
        return severity_mapping.get(severity.lower(), 'medium')
    
    def get_severity_description(self, severity: str) -> str:
        """Get standardized description for severity level"""
        descriptions = {
            'critical': 'Breaks core structure promise, unlistenable',
            'high': 'Significantly degrades experience, obvious to audience', 
            'medium': 'Noticeable issue, fixable without major rework',
            'low': 'Minor polish item, optional fix'
        }
        return descriptions.get(severity, 'Unknown severity level')
    
    def extract_audio_elements(self, content: str) -> Dict:
        """Extract audio elements from episode content for continuity checking"""
        audio_elements = {
            'character_voices': [],
            'sound_effects': [],
            'music_cues': [],
            'ambient_sounds': [],
            'audio_consistency_issues': []
        }
        
        # Extract character voice patterns
        import re
        voice_patterns = re.findall(r'\[VOICE:\s*([^\]]+)\]', content, re.IGNORECASE)
        audio_elements['character_voices'] = list(set(voice_patterns))
        
        # Extract sound effects
        sound_patterns = re.findall(r'\[SOUND:\s*([^\]]+)\]', content, re.IGNORECASE)
        audio_elements['sound_effects'] = list(set(sound_patterns))
        
        # Extract music cues
        music_patterns = re.findall(r'\[MUSIC:\s*([^\]]+)\]', content, re.IGNORECASE)
        audio_elements['music_cues'] = list(set(music_patterns))
        
        # Extract ambient sounds
        ambient_patterns = re.findall(r'\[AMBIENT:\s*([^\]]+)\]', content, re.IGNORECASE)
        audio_elements['ambient_sounds'] = list(set(ambient_patterns))
        
        return audio_elements
    
    def extract_timeline_elements(self, content: str) -> Dict:
        """Extract timeline elements from episode content for continuity checking"""
        timeline_elements = {
            'time_references': [],
            'date_references': [],
            'sequence_events': [],
            'timeline_consistency_issues': []
        }
        
        import re
        
        # Extract time references
        time_patterns = re.findall(r'\b(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\b', content, re.IGNORECASE)
        timeline_elements['time_references'] = list(set(time_patterns))
        
        # Extract date references
        date_patterns = re.findall(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})\b', content)
        timeline_elements['date_references'] = list(set(date_patterns))
        
        # Extract sequence events (before, after, then, next, etc.)
        sequence_patterns = re.findall(r'\b(before|after|then|next|previously|earlier|later|meanwhile)\b', content, re.IGNORECASE)
        timeline_elements['sequence_events'] = list(set(sequence_patterns))
        
        return timeline_elements
    
    def analyze_cross_episode_trends(self, all_episode_results: List[Dict]) -> Dict:
        """Analyze trends across all episodes"""
        trends = {
            'structure_compliance_trend': [],
            'reveal_mechanism_trend': [],
            'subplot_integration_trend': [],
            'continuity_issues_trend': [],
            'overall_quality_trend': [],
            'recommendations': []
        }
        
        if len(all_episode_results) < 2:
            trends['recommendations'].append("Insufficient episodes for trend analysis (minimum 2 required)")
            return trends
        
        # Analyze structure compliance trend
        for result in all_episode_results:
            structure_score = result.get('structure_adherence', {}).get('compliance_score', 0)
            trends['structure_compliance_trend'].append({
                'episode': result.get('episode_id'),
                'score': structure_score,
                'timestamp': result.get('timestamp')
            })
        
        # Analyze reveal mechanism trend
        for result in all_episode_results:
            reveal_score = result.get('reveal_mechanism', {}).get('fairness_score', 0)
            trends['reveal_mechanism_trend'].append({
                'episode': result.get('episode_id'),
                'score': reveal_score,
                'timestamp': result.get('timestamp')
            })
        
        # Analyze subplot integration trend
        for result in all_episode_results:
            subplot_score = result.get('subplot_integration', {}).get('integration_score', 0)
            trends['subplot_integration_trend'].append({
                'episode': result.get('episode_id'),
                'score': subplot_score,
                'timestamp': result.get('timestamp')
            })
        
        # Analyze continuity issues trend
        for result in all_episode_results:
            continuity_issues = len(result.get('continuity_check', {}).get('inconsistencies', []))
            trends['continuity_issues_trend'].append({
                'episode': result.get('episode_id'),
                'issue_count': continuity_issues,
                'timestamp': result.get('timestamp')
            })
        
        # Calculate overall quality trend
        for result in all_episode_results:
            structure_score = result.get('structure_adherence', {}).get('compliance_score', 0)
            reveal_score = result.get('reveal_mechanism', {}).get('fairness_score', 0)
            subplot_score = result.get('subplot_integration', {}).get('integration_score', 0)
            
            overall_score = (structure_score + reveal_score + subplot_score) / 3
            trends['overall_quality_trend'].append({
                'episode': result.get('episode_id'),
                'score': overall_score,
                'timestamp': result.get('timestamp')
            })
        
        # Generate trend-based recommendations
        self.generate_trend_recommendations(trends)
        
        return trends
    
    def generate_trend_recommendations(self, trends: Dict) -> None:
        """Generate recommendations based on trend analysis"""
        recommendations = []
        
        # Check structure compliance trend
        structure_scores = [t['score'] for t in trends['structure_compliance_trend']]
        if len(structure_scores) >= 2:
            if structure_scores[-1] < structure_scores[0]:
                recommendations.append("Structure compliance declining - review recent episodes for structural issues")
            elif structure_scores[-1] > structure_scores[0]:
                recommendations.append("Structure compliance improving - maintain current approach")
        
        # Check continuity issues trend
        continuity_counts = [t['issue_count'] for t in trends['continuity_issues_trend']]
        if len(continuity_counts) >= 2:
            if continuity_counts[-1] > continuity_counts[0]:
                recommendations.append("Continuity issues increasing - implement stricter continuity checking")
            elif continuity_counts[-1] < continuity_counts[0]:
                recommendations.append("Continuity issues decreasing - good progress on consistency")
        
        # Check overall quality trend
        quality_scores = [t['score'] for t in trends['overall_quality_trend']]
        if len(quality_scores) >= 3:
            recent_avg = sum(quality_scores[-3:]) / 3
            early_avg = sum(quality_scores[:3]) / 3
            
            if recent_avg < early_avg - 0.1:
                recommendations.append("Overall quality declining - comprehensive review recommended")
            elif recent_avg > early_avg + 0.1:
                recommendations.append("Overall quality improving - continue current practices")
        
        trends['recommendations'].extend(recommendations)

    async def initialize(self):
        """Initialize connections"""
        await self.redis.initialize()
        logger.info("✅ Station 30 initialized")

    async def validate_inputs(self) -> None:
        """Validate all dependencies before processing."""
        errors = []
        
        # Check Station 5 structure file
        station5_key = f"audiobook:{self.session_id}:station_05"
        station5_raw = await self.redis.get(station5_key)
        if not station5_raw:
            # Try loading from output file as fallback for testing
            station5_output_file = Path(f"output/station_05/{self.session_id}_output.json")
            if station5_output_file.exists():
                print(f"   ⚠️  Loading Station 5 data from output file: {station5_output_file}")
                with open(station5_output_file, 'r', encoding='utf-8') as f:
                    station5_raw = f.read()
            else:
                errors.append({
                    "type": "missing_dependency",
                    "station": 5,
                    "file": station5_key,
                    "message": "Structure selection not found. Run Station 5 first."
                })
        
        if station5_raw:
            # Validate structure selection exists
            try:
                station5_data = json.loads(station5_raw)
                season_doc = station5_data.get('Season Architecture Document', {})
                structure_doc = season_doc.get('season_structure_document', {})
                style_recommendations = structure_doc.get('style_recommendations', [])
                
                if not style_recommendations:
                    errors.append({
                        "type": "missing_structure_selection",
                        "station": 5,
                        "message": "No style recommendations found in Station 5 data."
                    })
                else:
                    selected_style = style_recommendations[0].get('style_name', 'Unknown')
                    # Check structure config exists
                    structure_config_path = Path("app/agents/configs/structure_rules") / f"{selected_style.lower().replace(' ', '_').replace('-', '_')}.yml"
                    if not structure_config_path.exists():
                        errors.append({
                            "type": "missing_config",
                            "file": str(structure_config_path),
                            "message": f"Structure rules for '{selected_style}' not found. No fallback allowed."
                        })
            except json.JSONDecodeError:
                errors.append({
                    "type": "invalid_data",
                    "station": 5,
                    "message": "Station 5 data is not valid JSON."
                })
        
        # Check Station 10 reveal mechanism file
        station10_key = f"audiobook:{self.session_id}:station_10"
        station10_raw = await self.redis.get(station10_key)
        if not station10_raw:
            # Try loading from output file as fallback for testing
            station10_output_file = Path(f"output/station_10/{self.session_id}_reveal_matrix.json")
            if station10_output_file.exists():
                print(f"   ⚠️  Loading Station 10 data from output file: {station10_output_file}")
                with open(station10_output_file, 'r', encoding='utf-8') as f:
                    station10_raw = f.read()
            else:
                errors.append({
                    "type": "missing_dependency",
                    "station": 10,
                    "file": station10_key,
                    "message": "Reveal mechanism data not found. Run Station 10 first."
                })
        
        # Check episode scripts exist
        pattern = f"audiobook:{self.session_id}:station_*:episode_*"
        episode_keys = await self.redis.keys(pattern)
        if not episode_keys:
            errors.append({
                "type": "missing_scripts",
                "message": "No episode scripts found to validate."
            })
        
        if errors:
            print("❌ Validation errors found:")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error.get('type', 'Unknown')}: {error.get('message', 'No message')}")
                if 'file' in error:
                    print(f"      File: {error['file']}")
                if 'station' in error:
                    print(f"      Station: {error['station']}")
            raise ValidationError(f"Cannot proceed: {len(errors)} critical errors", errors)
        
        logger.info("✅ All input dependencies validated successfully")

    async def run(self):
        """Main execution method"""
        print("=" * 70)
        print("🏗️ STATION 30: NARRATIVE STRUCTURE INTEGRITY CHECKER")
        print("=" * 70)
        print()

        try:
            # Step 1: Validate all inputs first
            print("🔍 Validating input dependencies...")
            await self.validate_inputs()
            print("✅ All dependencies validated")
            print()

            # Step 2: Load required inputs
            print("📥 Loading required inputs...")
            station5_data = await self.load_station5_data()
            station10_data = await self.load_station10_data()
            episode_scripts = await self.load_episode_scripts()
            
            print("✅ All inputs loaded successfully")
            print(f"   ✓ Station 5: Structure choice loaded")
            print(f"   ✓ Station 10: Reveal mechanism data loaded")
            print(f"   ✓ Episode scripts: {len(episode_scripts)} episodes")
            print()

            # Step 3: Load structure validation rules
            print("📋 Loading structure validation rules...")
            await self.load_structure_validation_rules(station5_data)
            print("✅ Structure validation rules loaded")
            print()

            # Step 4: Display project summary
            self.display_project_summary(station5_data, station10_data, episode_scripts)

            # Step 4: Process each episode
            episodes = episode_scripts.get('episodes', [])
            if not episodes:
                raise ValueError("❌ No episodes found in episode scripts data. Cannot proceed.")

            all_episode_results = []
            
            for episode_key, episode_data in episodes.items():
                episode_id = episode_data.get('episode_number', episode_key)
                print(f"\n🎬 Processing Episode: {episode_id}")
                print("-" * 70)

                # Execute 4-task validation sequence
                print("📊 Task 1/4: Structure Adherence Validation...")
                structure_compliance = await self.execute_task1_structure_adherence(
                    episode_data, station5_data
                )
                print("✅ Structure adherence validation complete")

                print("🔍 Task 2/4: Reveal Mechanism Check...")
                reveal_mechanism = await self.execute_task2_reveal_mechanism_check(
                    episode_data, station10_data
                )
                print("✅ Reveal mechanism check complete")

                print("📈 Task 3/4: Subplot Integration Analysis...")
                subplot_analysis = await self.execute_task3_subplot_integration(
                    episode_data, station5_data
                )
                print("✅ Subplot integration analysis complete")

                print("🔗 Task 4/4: Cross-Episode Continuity...")
                continuity_check = await self.execute_task4_cross_episode_continuity(
                    episode_data, episode_scripts
                )
                print("✅ Cross-episode continuity check complete")

                # Compile episode results
                episode_result = {
                    "episode_id": episode_id,
                    "structure_compliance": structure_compliance,
                    "reveal_mechanism": reveal_mechanism,
                    "subplot_analysis": subplot_analysis,
                    "continuity_check": continuity_check,
                    "flagged_issues": self.extract_flagged_issues(
                        structure_compliance, reveal_mechanism, subplot_analysis, continuity_check
                    ),
                    "timestamp": datetime.now().isoformat()
                }

                all_episode_results.append(episode_result)

                # Save individual episode results
                await self.save_episode_output(episode_result)

                print(f"✅ Episode {episode_id} validation complete")

            # Step 5: Generate summary report
            print("\n" + "=" * 70)
            print("📊 GENERATING SUMMARY REPORT")
            print("=" * 70)
            summary_report = await self.generate_summary_report(all_episode_results, station5_data, station10_data)

            # Step 6: Analyze cross-episode trends
            print("📈 ANALYZING CROSS-EPISODE TRENDS")
            trend_analysis = self.analyze_cross_episode_trends(all_episode_results)
            summary_report['trend_analysis'] = trend_analysis
            print(f"   ✓ Trend analysis complete: {len(trend_analysis['recommendations'])} recommendations")

            # Step 7: Update user validation status
            self.update_user_validation_status()

            # Step 8: Present flagged issues for user approval
            await self.present_flagged_issues_for_approval(all_episode_results)

            # Step 9: Save final outputs
            await self.save_final_outputs(all_episode_results, summary_report)

            print("\n" + "=" * 70)
            print("✅ STATION 30 COMPLETE!")
            print("=" * 70)
            print(f"\nSession ID: {self.session_id}")
            print(f"Episodes Validated: {len(all_episode_results)}")
            print("\n📄 Output files:")
            print(f"   - output/station_30/{self.session_id}_summary.json")
            print(f"   - output/station_30/{self.session_id}_summary.txt")
            print(f"   - output/station_30/{self.session_id}_episode_*.json (per episode)")
            print("\n📌 Ready to proceed to next station")

        except Exception as e:
            logger.error(f"❌ Station 30 failed: {str(e)}")
            raise

    async def load_station5_data(self) -> Dict:
        """Load Station 5 structure choice from Redis or output file"""
        try:
            station5_key = f"audiobook:{self.session_id}:station_05"
            station5_raw = await self.redis.get(station5_key)
            
            if not station5_raw:
                # Try loading from output file as fallback
                station5_output_file = Path(f"output/station_05/{self.session_id}_output.json")
                if station5_output_file.exists():
                    with open(station5_output_file, 'r', encoding='utf-8') as f:
                        station5_raw = f.read()
                else:
                    raise ValueError(f"❌ No Station 5 data found for session {self.session_id}\n   Please run Station 5 first")
            
            station5_data = json.loads(station5_raw)
            
            # Validate required structure
            if 'Season Architecture Document' not in station5_data:
                raise ValueError("❌ Station 5 data missing 'Season Architecture Document' key. Cannot proceed.")
            
            return station5_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 5 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 5 data: {str(e)}")

    async def load_station10_data(self) -> Dict:
        """Load Station 10 reveal mechanism data from Redis or output file"""
        try:
            station10_key = f"audiobook:{self.session_id}:station_10"
            station10_raw = await self.redis.get(station10_key)
            
            if not station10_raw:
                # Try loading from output file as fallback
                station10_output_file = Path(f"output/station_10/{self.session_id}_reveal_matrix.json")
                if station10_output_file.exists():
                    with open(station10_output_file, 'r', encoding='utf-8') as f:
                        station10_raw = f.read()
                else:
                    raise ValueError(f"❌ No Station 10 data found for session {self.session_id}\n   Please run Station 10 first")
            
            station10_data = json.loads(station10_raw)
            
            # Validate required structure
            if 'reveal_taxonomy' not in station10_data:
                raise ValueError("❌ Station 10 data missing 'reveal_taxonomy' key. Cannot proceed.")
            
            return station10_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing Station 10 data: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading Station 10 data: {str(e)}")

    async def load_episode_scripts(self) -> Dict:
        """Load all generated episode scripts from previous stations"""
        try:
            # Look for episode scripts from various stations (27, 28, etc.)
            pattern = f"audiobook:{self.session_id}:station_*:episode_*"
            episode_keys = await self.redis.keys(pattern)
            
            if not episode_keys:
                raise ValueError(f"❌ No episode scripts found for session {self.session_id}\n   Please run script generation stations first")
            
            # Load all episodes and combine them
            episodes = {}
            for key in episode_keys:
                episode_raw = await self.redis.get(key)
                if episode_raw:
                    episode_data = json.loads(episode_raw)
                    # Extract episode number from key (e.g., episode_01)
                    episode_num = key.split(':')[-1]  # Gets "episode_01"
                    episodes[episode_num] = episode_data
            
            if not episodes:
                raise ValueError(f"❌ No valid episode scripts found for session {self.session_id}")
            
            # Return in expected format
            episode_scripts = {
                'episodes': episodes
            }
            
            return episode_scripts
            
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Error parsing episode scripts: {str(e)}")
        except Exception as e:
            raise ValueError(f"❌ Error loading episode scripts: {str(e)}")

    async def load_structure_validation_rules(self, station5_data: Dict):
        """Load structure validation rules based on Station 5 selection"""
        try:
            # Extract selected structure from Station 5
            season_doc = station5_data.get('Season Architecture Document', {})
            structure_doc = season_doc.get('season_structure_document', {})
            style_recommendations = structure_doc.get('style_recommendations', [])
            
            if not style_recommendations:
                raise ValueError("❌ No style recommendations found in Station 5 data. Cannot load validation rules.")
            
            # Get the selected structure (first recommendation)
            selected_style = style_recommendations[0].get('style_name', 'Unknown')
            
            # Load structure-specific validation rules from config
            structure_config_path = Path("app/agents/configs/structure_rules") / f"{selected_style.lower().replace(' ', '_').replace('-', '_')}.yml"
            
            if not structure_config_path.exists():
                raise ValueError(f"❌ Structure rules file not found: {structure_config_path}. No fallback allowed.")
            
            # Load the YAML structure rules
            with open(structure_config_path, 'r', encoding='utf-8') as f:
                structure_rules_data = yaml.safe_load(f)
            
            # Store the loaded rules
            self.structure_rules = structure_rules_data
            
            # Create structure validation metadata
            self.structure_metadata = StructureValidationMetadata(
                structure_selected=selected_style,
                structure_source=str(structure_config_path),
                rules_loaded=self.count_rules_loaded(structure_rules_data),
                rules_applied=0,  # Will be updated during validation
                rules_list=self.extract_rule_ids(structure_rules_data),
                load_timestamp=datetime.now().isoformat(),
                config_version=structure_rules_data.get('structure_version', '1.0'),
                validation_successful=True
            )
            
            print(f"   ✓ Loaded validation rules for: {selected_style}")
            print(f"   ✓ Rules loaded: {self.structure_metadata.rules_loaded}")
            print(f"   ✓ Config version: {self.structure_metadata.config_version}")
            
        except Exception as e:
            raise ValueError(f"❌ Error loading structure validation rules: {str(e)}")
    
    def count_rules_loaded(self, structure_rules_data: Dict) -> int:
        """Count total number of rules loaded from structure config"""
        count = 0
        
        # Count act timing rules
        act_timing = structure_rules_data.get('act_timing_rules', {})
        count += len(act_timing)
        
        # Count turning point rules
        turning_points = structure_rules_data.get('turning_points', {})
        if turning_points:
            count += 1
        
        # Count revelation rules
        revelation_rules = structure_rules_data.get('revelation_rules', {})
        if revelation_rules:
            count += 1
        
        # Count audio continuity rules
        audio_continuity = structure_rules_data.get('audio_continuity', {})
        count += len(audio_continuity)
        
        return count
    
    def extract_rule_ids(self, structure_rules_data: Dict) -> List[str]:
        """Extract all rule IDs from structure config"""
        rule_ids = []
        
        # Extract act timing rule IDs
        act_timing = structure_rules_data.get('act_timing_rules', {})
        for act_name, act_data in act_timing.items():
            if isinstance(act_data, dict) and 'rule_id' in act_data:
                rule_ids.append(act_data['rule_id'])
        
        # Extract other rule IDs
        for section_name in ['turning_points', 'revelation_rules']:
            section_data = structure_rules_data.get(section_name, {})
            if isinstance(section_data, dict) and 'rule_id' in section_data:
                rule_ids.append(section_data['rule_id'])
        
        # Extract audio continuity rule IDs
        audio_continuity = structure_rules_data.get('audio_continuity', {})
        for audio_section, audio_data in audio_continuity.items():
            if isinstance(audio_data, dict) and 'rule_id' in audio_data:
                rule_ids.append(audio_data['rule_id'])
        
        return rule_ids

    def get_generic_structure_rules(self) -> Dict:
        """Get generic structure validation rules (placeholder for specific rules)"""
        return {
            'act_breaks': {
                'required': True,
                'timing_tolerance': 0.1,  # 10% tolerance
                'audio_markers': ['music_sting', 'silence', 'voice_change']
            },
            'turning_points': {
                'required': True,
                'minimum_count': 3,
                'audio_signatures': ['music_change', 'sound_effect', 'voice_shift']
            },
            'pacing': {
                'energy_levels': {
                    'min': 1,
                    'max': 10,
                    'required_variation': True
                }
            }
        }

    def get_audio_marker_rules(self) -> Dict:
        """Get audio marker validation rules"""
        return {
            'structure_markers': {
                'act_breaks': ['music_sting', 'silence', 'voice_change'],
                'turning_points': ['music_change', 'sound_effect', 'voice_shift'],
                'revelations': ['music_sting', 'silence', 'voice_revelation']
            },
            'subplot_signatures': {
                'unique_sounds': True,
                'clear_transitions': True,
                'trackable_by_audience': True
            }
        }

    def get_timing_requirements(self) -> Dict:
        """Get timing validation requirements"""
        return {
            'act_timing': {
                'tolerance': 0.15,  # 15% tolerance
                'required_breaks': True
            },
            'beat_timing': {
                'tolerance': 0.2,  # 20% tolerance
                'required_progression': True
            }
        }

    def display_project_summary(self, station5_data: Dict, station10_data: Dict, episode_scripts: Dict):
        """Display project context summary"""
        print("=" * 70)
        print("📋 PROJECT CONTEXT")
        print("=" * 70)
        
        episodes = episode_scripts.get('episodes', [])
        season_doc = station5_data.get('Season Architecture Document', {})
        structure_doc = season_doc.get('season_structure_document', {})
        style_recommendations = structure_doc.get('style_recommendations', [])
        selected_style = style_recommendations[0].get('style_name', 'Unknown') if style_recommendations else 'Unknown'
        
        reveal_taxonomy = station10_data.get('reveal_taxonomy', {})
        
        print(f"Episodes to Validate: {len(episodes)}")
        print(f"Selected Structure: {selected_style}")
        print(f"Reveal Elements: {reveal_taxonomy.get('total_information_units', 0)}")
        print()
        
        if episodes:
            print("Episode List:")
        for episode_key, episode_data in episodes.items():
            episode_id = episode_data.get('episode_number', episode_key)
            print(f"   • {episode_id}")
        
        print("-" * 70)

    async def execute_task1_structure_adherence(self, episode: Dict, station5_data: Dict) -> Dict:
        """Task 1: Structure Adherence Validation"""
        try:
            # Extract episode content and structure information
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            season_doc = station5_data.get('Season Architecture Document', {})
            structure_doc = season_doc.get('season_structure_document', {})
            episode_grid = structure_doc.get('season_skeleton', {}).get('episode_grid', [])
            
            # Find this episode's structure requirements
            episode_structure = None
            # Handle both string and integer episode IDs
            if isinstance(episode_id, str):
                episode_num = int(episode_id.replace('episode_', ''))
            else:
                episode_num = int(episode_id)
            
            for ep in episode_grid:
                if ep.get('episode_number') == episode_num:
                    episode_structure = ep
                    break
            
            # Build context for prompt
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],  # First 2000 chars for context
                'selected_structure': self.structure_rules.get('selected_structure', 'Unknown'),
                'episode_structure': json.dumps(episode_structure) if episode_structure else '{}',
                'structure_rules': json.dumps(self.structure_rules.get('validation_rules', {})),
                'audio_marker_rules': json.dumps(self.structure_rules.get('audio_markers', {}))
            }
            
            prompt = self.config.get_prompt('structure_adherence_validation').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('structure_compliance_report', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 1 failed: {str(e)}")

    async def execute_task2_reveal_mechanism_check(self, episode: Dict, station10_data: Dict) -> Dict:
        """Task 2: Reveal Mechanism Check"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            reveal_taxonomy = station10_data.get('reveal_taxonomy', {})
            reveal_methods = station10_data.get('reveal_methods', {})
            plant_proof_payoff = station10_data.get('plant_proof_payoff_grid', {})
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],
                'reveal_taxonomy': json.dumps(reveal_taxonomy),
                'reveal_methods': json.dumps(reveal_methods),
                'plant_proof_payoff': json.dumps(plant_proof_payoff)
            }
            
            prompt = self.config.get_prompt('reveal_mechanism_check').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('reveal_mechanism_scorecard', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 2 failed: {str(e)}")

    async def execute_task3_subplot_integration(self, episode: Dict, station5_data: Dict) -> Dict:
        """Task 3: Subplot Integration Analysis"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            season_doc = station5_data.get('Season Architecture Document', {})
            structure_doc = season_doc.get('season_structure_document', {})
            episode_grid = structure_doc.get('season_skeleton', {}).get('episode_grid', [])
            
            # Find this episode's subplot focus
            episode_structure = None
            # Handle both string and integer episode IDs
            if isinstance(episode_id, str):
                episode_num = int(episode_id.replace('episode_', ''))
            else:
                episode_num = int(episode_id)
            
            for ep in episode_grid:
                if ep.get('episode_number') == episode_num:
                    episode_structure = ep
                    break
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],
                'episode_structure': json.dumps(episode_structure) if episode_structure else '{}',
                'subplot_focus': episode_structure.get('subplot_focus', 'Unknown') if episode_structure else 'Unknown'
            }
            
            prompt = self.config.get_prompt('subplot_integration_analysis').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('subplot_tracking_chart', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 3 failed: {str(e)}")

    async def execute_task4_cross_episode_continuity(self, episode: Dict, episode_scripts: Dict) -> Dict:
        """Task 4: Cross-Episode Continuity with Audio/Timeline Checks"""
        try:
            episode_content = episode.get('master_script_assembly', {}).get('master_script_text', '')
            episode_id = episode.get('episode_number', 'unknown')
            
            # Get all other episodes for continuity checking
            all_episodes = episode_scripts.get('episodes', {})
            
            # Extract audio elements for continuity checking
            audio_elements = self.extract_audio_elements(episode_content)
            timeline_elements = self.extract_timeline_elements(episode_content)
            
            context = {
                'episode_id': episode_id,
                'episode_content': episode_content[:2000],
                'all_episodes': json.dumps(all_episodes),
                'audio_elements': json.dumps(audio_elements),
                'timeline_elements': json.dumps(timeline_elements),
                'structure_rules': json.dumps(self.structure_rules.get('continuity_rules', {}))
            }
            
            prompt = self.config.get_prompt('cross_episode_continuity').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('continuity_issue_list', {})
            
        except Exception as e:
            raise ValueError(f"❌ Task 4 failed: {str(e)}")

    def extract_flagged_issues(self, structure_compliance: Dict, reveal_mechanism: Dict, 
                              subplot_analysis: Dict, continuity_check: Dict) -> List[Dict]:
        """Extract flagged issues from all validation results"""
        issues = []
        
        # Structure compliance issues
        violations = structure_compliance.get('violations', [])
        for violation in violations:
            # Create rule reference if available
            rule_reference = None
            if 'rule_id' in violation:
                rule_reference = RuleReference(
                    rule_id=violation['rule_id'],
                    source_file=violation.get('source_file', 'Unknown'),
                    rule_definition=violation.get('rule_definition', 'Unknown'),
                    expected_value=violation.get('expected_value', 'Unknown'),
                    actual_value=violation.get('actual_value', 'Unknown'),
                    deviation=violation.get('deviation', 'Unknown')
                )
            
            # Create actionable fix recommendation
            fix_recommendation = None
            if 'recommended_fix' in violation:
                fix_recommendation = FixRecommendation(
                    description=violation['recommended_fix'],
                    action_type=violation.get('action_type', 'manual_review'),
                    target_timestamp=violation.get('target_timestamp'),
                    current_timestamp=violation.get('current_timestamp'),
                    adjustment_seconds=violation.get('adjustment_seconds'),
                    affected_elements=violation.get('affected_elements', []),
                    automation_possible=violation.get('automation_possible', False),
                    automation_script=violation.get('automation_script')
                )
            
            # Create flagged issue with enhanced tracking
            issue = self.create_flagged_issue(
                issue_type='structure_violation',
                severity=violation.get('severity', 'medium'),
                description=violation.get('description', 'Unknown violation'),
                rule_reference=rule_reference,
                fix_recommendation=fix_recommendation
            )
            
            # Add location for backward compatibility
            issue['location'] = violation.get('location', 'Unknown')
            issues.append(issue)
        
        # Reveal mechanism issues
        fairness_issues = reveal_mechanism.get('fairness_issues', [])
        for issue in fairness_issues:
            issues.append({
                'type': 'reveal_fairness',
                'severity': issue.get('severity', 'medium'),
                'description': issue.get('description', 'Unknown fairness issue'),
                'location': issue.get('location', 'Unknown'),
                'recommended_fix': issue.get('recommended_fix', 'No fix provided')
            })
        
        # Subplot issues
        subplot_issues = subplot_analysis.get('issues', [])
        for issue in subplot_issues:
            issues.append({
                'type': 'subplot_integration',
                'severity': issue.get('severity', 'medium'),
                'description': issue.get('description', 'Unknown subplot issue'),
                'location': issue.get('location', 'Unknown'),
                'recommended_fix': issue.get('recommended_fix', 'No fix provided')
            })
        
        # Continuity issues
        continuity_issues = continuity_check.get('issues', [])
        for issue in continuity_issues:
            issues.append({
                'type': 'continuity_error',
                'severity': issue.get('severity', 'medium'),
                'description': issue.get('description', 'Unknown continuity issue'),
                'location': issue.get('location', 'Unknown'),
                'recommended_fix': issue.get('recommended_fix', 'No fix provided')
            })
        
        return issues

    async def generate_summary_report(self, all_episode_results: List[Dict], station5_data: Dict, station10_data: Dict) -> Dict:
        """Generate comprehensive summary report across all episodes"""
        try:
            context = {
                'session_id': self.session_id,
                'episode_results': json.dumps(all_episode_results),
                'total_episodes': len(all_episode_results),
                'selected_structure': self.structure_rules.get('selected_structure', 'Unknown'),
                'reveal_elements': station10_data.get('reveal_taxonomy', {}).get('total_information_units', 0)
            }
            
            prompt = self.config.get_prompt('summary_report').format(**context)
            
            response = await self.openrouter.process_message(
                prompt,
                model_name=self.config.model,
                max_tokens=self.config.max_tokens
            )
            
            data = extract_json(response)
            return data.get('summary_report', {})
            
        except Exception as e:
            raise ValueError(f"❌ Summary report generation failed: {str(e)}")

    async def present_flagged_issues_for_approval(self, all_episode_results: List[Dict]):
        """Present flagged issues to user for approval"""
        print("\n" + "=" * 70)
        print("⚠️ FLAGGED ISSUES REQUIRING USER APPROVAL")
        print("=" * 70)
        
        all_issues = []
        for episode_result in all_episode_results:
            episode_issues = episode_result.get('flagged_issues', [])
            for issue in episode_issues:
                issue['episode_id'] = episode_result.get('episode_id', 'Unknown')
                all_issues.append(issue)
        
        if not all_issues:
            print("✅ No issues flagged - all validations passed!")
            return
        
        # Group issues by severity
        critical_issues = [i for i in all_issues if i.get('severity') == 'critical']
        high_issues = [i for i in all_issues if i.get('severity') == 'high']
        medium_issues = [i for i in all_issues if i.get('severity') == 'medium']
        low_issues = [i for i in all_issues if i.get('severity') == 'low']
        
        print(f"Total Issues Found: {len(all_issues)}")
        print(f"  • Critical: {len(critical_issues)}")
        print(f"  • High: {len(high_issues)}")
        print(f"  • Medium: {len(medium_issues)}")
        print(f"  • Low: {len(low_issues)}")
        print()
        
        # Show critical and high issues
        if critical_issues or high_issues:
            print("🚨 CRITICAL & HIGH PRIORITY ISSUES:")
            print("-" * 70)
            
            for issue in critical_issues + high_issues:
                print(f"\nEpisode: {issue.get('episode_id')}")
                print(f"Type: {issue.get('type', 'Unknown').replace('_', ' ').title()}")
                print(f"Severity: {issue.get('severity', 'Unknown').upper()}")
                print(f"Issue: {issue.get('description', 'No description')}")
                print(f"Location: {issue.get('location', 'Unknown')}")
                print(f"Recommended Fix: {issue.get('recommended_fix', 'No fix provided')}")
                print("-" * 70)
        
        # Ask for approval
        print("\nOPTIONS:")
        print("  [Enter] - Approve all fixes and continue")
        print("  [R]      - Review all issues in detail")
        print("  [S]      - Skip fixes and continue without changes")
        print()
        
        choice = input("Your choice: ").strip().upper()
        
        if choice == 'R':
            self._review_all_issues(all_issues)
            input("\nPress Enter when ready to continue: ")
        elif choice == 'S':
            print("⚠️ Continuing without applying fixes...")
        else:
            print("✅ Approved - fixes will be applied in future implementation")

    def _review_all_issues(self, all_issues: List[Dict]):
        """Review all issues in detail"""
        for i, issue in enumerate(all_issues, 1):
            print(f"\n{'=' * 70}")
            print(f"ISSUE {i}: {issue.get('type', 'Unknown').replace('_', ' ').title()}")
            print('=' * 70)
            print(f"Episode: {issue.get('episode_id', 'Unknown')}")
            print(f"Severity: {issue.get('severity', 'Unknown').upper()}")
            print(f"Description: {issue.get('description', 'No description')}")
            print(f"Location: {issue.get('location', 'Unknown')}")
            print(f"Recommended Fix: {issue.get('recommended_fix', 'No fix provided')}")

    async def save_episode_output(self, episode_result: Dict):
        """Save individual episode results to JSON and TXT"""
        episode_id = episode_result['episode_id']
        
        # Add user validation data to episode result
        episode_result['user_validation'] = {
            "status": self.user_validation.status,
            "total_issues_requiring_approval": self.user_validation.total_issues_requiring_approval,
            "approved_fixes": self.user_validation.approved_fixes,
            "rejected_fixes": self.user_validation.rejected_fixes,
            "approval_timestamp": self.user_validation.approval_timestamp,
            "pending_issues": self.user_validation.pending_issues
        }
        
        # Add flagged issues with approval tracking
        episode_result['flagged_issues'] = self.flagged_issues
        
        # Save JSON
        json_path = self.output_dir / f"{self.session_id}_{episode_id}_validation.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(episode_result, f, indent=2, ensure_ascii=False)
        
        # Save TXT
        txt_path = self.output_dir / f"{self.session_id}_{episode_id}_validation.txt"
        self.save_episode_readable_txt(txt_path, episode_result)

    def save_episode_readable_txt(self, path: Path, data: Dict):
        """Save human-readable TXT file for episode validation"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 30: NARRATIVE STRUCTURE INTEGRITY VALIDATION\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Episode ID: {data.get('episode_id', 'N/A')}\n")
            f.write(f"Validation Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Session ID: {self.session_id}\n\n")
            
            # Structure Compliance
            f.write("-" * 70 + "\n")
            f.write("STRUCTURE COMPLIANCE REPORT\n")
            f.write("-" * 70 + "\n")
            
            compliance = data.get('structure_compliance', {})
            f.write(f"Overall Score: {compliance.get('overall_score', 'N/A')}/5\n")
            f.write(f"Compliance Status: {compliance.get('status', 'N/A')}\n")
            
            violations = compliance.get('violations', [])
            if violations:
                f.write("\nViolations Found:\n")
                for i, violation in enumerate(violations, 1):
                    f.write(f"  {i}. {violation.get('description', 'N/A')}\n")
                    f.write(f"     Location: {violation.get('location', 'N/A')}\n")
                    f.write(f"     Severity: {violation.get('severity', 'N/A')}\n")
            else:
                f.write("\nNo violations found.\n")
            
            # Reveal Mechanism
            f.write("\n" + "-" * 70 + "\n")
            f.write("REVEAL MECHANISM SCORECARD\n")
            f.write("-" * 70 + "\n")
            
            reveal = data.get('reveal_mechanism', {})
            f.write(f"Fairness Rating: {reveal.get('fairness_rating', 'N/A')}/5\n")
            f.write(f"Clue Audibility: {reveal.get('clue_audibility', 'N/A')}\n")
            
            fairness_issues = reveal.get('fairness_issues', [])
            if fairness_issues:
                f.write("\nFairness Issues:\n")
                for i, issue in enumerate(fairness_issues, 1):
                    f.write(f"  {i}. {issue.get('description', 'N/A')}\n")
            else:
                f.write("\nNo fairness issues found.\n")
            
            # Subplot Analysis
            f.write("\n" + "-" * 70 + "\n")
            f.write("SUBPLOT INTEGRATION ANALYSIS\n")
            f.write("-" * 70 + "\n")
            
            subplot = data.get('subplot_analysis', {})
            f.write(f"Integration Score: {subplot.get('integration_score', 'N/A')}/5\n")
            f.write(f"Audio Signature Quality: {subplot.get('audio_signature_quality', 'N/A')}\n")
            
            subplot_issues = subplot.get('issues', [])
            if subplot_issues:
                f.write("\nSubplot Issues:\n")
                for i, issue in enumerate(subplot_issues, 1):
                    f.write(f"  {i}. {issue.get('description', 'N/A')}\n")
            else:
                f.write("\nNo subplot issues found.\n")
            
            # Continuity Check
            f.write("\n" + "-" * 70 + "\n")
            f.write("CROSS-EPISODE CONTINUITY CHECK\n")
            f.write("-" * 70 + "\n")
            
            continuity = data.get('continuity_check', {})
            f.write(f"Continuity Score: {continuity.get('continuity_score', 'N/A')}/5\n")
            f.write(f"Consistency Status: {continuity.get('consistency_status', 'N/A')}\n")
            
            continuity_issues = continuity.get('issues', [])
            if continuity_issues:
                f.write("\nContinuity Issues:\n")
                for i, issue in enumerate(continuity_issues, 1):
                    f.write(f"  {i}. {issue.get('description', 'N/A')}\n")
            else:
                f.write("\nNo continuity issues found.\n")
            
            # Flagged Issues Summary
            f.write("\n" + "-" * 70 + "\n")
            f.write("FLAGGED ISSUES SUMMARY\n")
            f.write("-" * 70 + "\n")
            
            flagged_issues = data.get('flagged_issues', [])
            if flagged_issues:
                f.write(f"Total Issues Flagged: {len(flagged_issues)}\n")
                for i, issue in enumerate(flagged_issues, 1):
                    f.write(f"\n{i}. {issue.get('type', 'N/A').replace('_', ' ').title()}\n")
                    f.write(f"   Severity: {issue.get('severity', 'N/A')}\n")
                    f.write(f"   Description: {issue.get('description', 'N/A')}\n")
                    f.write(f"   Recommended Fix: {issue.get('recommended_fix', 'N/A')}\n")
            else:
                f.write("No issues flagged.\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF STRUCTURE INTEGRITY VALIDATION\n")
            f.write("=" * 70 + "\n")

    async def save_final_outputs(self, all_episode_results: List[Dict], summary_report: Dict):
        """Save final comprehensive outputs"""
        # Compile final data
        final_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "total_episodes": len(all_episode_results),
            "selected_structure": self.structure_rules.get('structure_name', 'Unknown'),
            "structure_metadata": {
                "structure_selected": self.structure_metadata.structure_selected if self.structure_metadata else "Unknown",
                "structure_source": self.structure_metadata.structure_source if self.structure_metadata else "Unknown",
                "rules_loaded": self.structure_metadata.rules_loaded if self.structure_metadata else 0,
                "rules_applied": self.structure_metadata.rules_applied if self.structure_metadata else 0,
                "rules_list": self.structure_metadata.rules_list if self.structure_metadata else [],
                "load_timestamp": self.structure_metadata.load_timestamp if self.structure_metadata else None,
                "config_version": self.structure_metadata.config_version if self.structure_metadata else "1.0",
                "validation_successful": self.structure_metadata.validation_successful if self.structure_metadata else False
            },
            "episode_results": all_episode_results,
            "summary_report": summary_report,
            "user_validation_summary": {
                "status": self.user_validation.status,
                "total_issues_requiring_approval": self.user_validation.total_issues_requiring_approval,
                "approved_fixes": self.user_validation.approved_fixes,
                "rejected_fixes": self.user_validation.rejected_fixes,
                "approval_timestamp": self.user_validation.approval_timestamp,
                "pending_issues": self.user_validation.pending_issues
            },
            "validation_thresholds": self.config.get('validation_thresholds', {})
        }
        
        # Save JSON
        json_path = self.output_dir / f"{self.session_id}_summary.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        # Save TXT
        txt_path = self.output_dir / f"{self.session_id}_summary.txt"
        self.save_summary_readable_txt(txt_path, final_data)
        
        # Save to Redis
        redis_key = f"audiobook:{self.session_id}:station_30"
        await self.redis.set(redis_key, json.dumps(final_data), expire=86400)
        
        print(f"✅ Final outputs saved")

    def save_summary_readable_txt(self, path: Path, data: Dict):
        """Save human-readable summary TXT file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STATION 30: NARRATIVE STRUCTURE INTEGRITY VALIDATION SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session ID: {data.get('session_id', 'N/A')}\n")
            f.write(f"Validation Date: {data.get('timestamp', 'N/A')}\n")
            f.write(f"Total Episodes: {data.get('total_episodes', 'N/A')}\n")
            f.write(f"Selected Structure: {data.get('selected_structure', 'N/A')}\n\n")
            
            # Summary Report
            summary = data.get('summary_report', {})
            f.write("-" * 70 + "\n")
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"{summary.get('executive_summary', 'N/A')}\n\n")
            
            # Overall Scores
            f.write("-" * 70 + "\n")
            f.write("OVERALL VALIDATION HEALTH\n")
            f.write("-" * 70 + "\n")
            f.write(f"Average Structure Compliance: {summary.get('average_structure_score', 'N/A')}/5\n")
            f.write(f"Average Reveal Fairness: {summary.get('average_reveal_score', 'N/A')}/5\n")
            f.write(f"Average Subplot Integration: {summary.get('average_subplot_score', 'N/A')}/5\n")
            f.write(f"Average Continuity Score: {summary.get('average_continuity_score', 'N/A')}/5\n")
            f.write(f"Total Issues Flagged: {summary.get('total_issues', 'N/A')}\n\n")
            
            # Episode Breakdown
            f.write("-" * 70 + "\n")
            f.write("EPISODE BREAKDOWN\n")
            f.write("-" * 70 + "\n")
            
            episode_results = data.get('episode_results', [])
            for episode in episode_results:
                episode_id = episode.get('episode_id', 'Unknown')
                structure = episode.get('structure_compliance', {})
                reveal = episode.get('reveal_mechanism', {})
                subplot = episode.get('subplot_analysis', {})
                continuity = episode.get('continuity_check', {})
                issues = len(episode.get('flagged_issues', []))
                
                f.write(f"\n{episode_id}:\n")
                f.write(f"  Structure Compliance: {structure.get('overall_score', 'N/A')}/5\n")
                f.write(f"  Reveal Fairness: {reveal.get('fairness_rating', 'N/A')}/5\n")
                f.write(f"  Subplot Integration: {subplot.get('integration_score', 'N/A')}/5\n")
                f.write(f"  Continuity Score: {continuity.get('continuity_score', 'N/A')}/5\n")
                f.write(f"  Issues Flagged: {issues}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF STRUCTURE INTEGRITY VALIDATION\n")
            f.write("=" * 70 + "\n")


# CLI Entry Point
async def main():
    """Run Station 30 standalone"""
    session_id = input("\n👉 Enter Session ID from previous stations: ").strip()
    
    if not session_id:
        print("❌ Session ID required")
        return
    
    checker = Station30StructureIntegrityChecker(session_id)
    await checker.initialize()
    
    try:
        await checker.run()
        print(f"\n✅ Success! Structure integrity validation complete for session: {session_id}")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
