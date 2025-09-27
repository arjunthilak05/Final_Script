"""
Station 7: Reality Check System - COMPREHENSIVE DYNAMIC VALIDATION

This agent performs thorough validation of the complete audiobook project
by analyzing all outputs from Stations 1-6 with detailed, specific checks.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re

from app.redis_client import RedisClient

logger = logging.getLogger(__name__)

class ValidationStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class IssueSeverity(Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"

class ProceedRecommendation(Enum):
    PROCEED = "PROCEED"
    REVISE = "REVISE"
    MAJOR_REVISION_REQUIRED = "MAJOR_REVISION_REQUIRED"

@dataclass
class ValidationResult:
    category: str
    status: ValidationStatus
    issues: List[str]
    details: Dict[str, Any]

@dataclass
class Issue:
    category: str
    description: str
    affected_stations: List[str]
    recommended_fix: str
    fix_complexity: str
    severity: IssueSeverity

@dataclass
class RealityCheckReport:
    working_title: str
    session_id: str
    validation_timestamp: datetime
    overall_viability_score: float
    logical_consistency: ValidationResult
    genre_appropriateness: ValidationResult
    audio_feasibility: ValidationResult
    production_viability: ValidationResult
    critical_issues: List[Issue]
    major_issues: List[Issue]
    minor_issues: List[Issue]
    recommendations: Dict[str, List[str]]
    station_feedback: Dict[str, str]
    proceed_recommendation: ProceedRecommendation
    confidence_score: float

class Station07RealityCheck:
    """Station 7: Comprehensive Reality Check System"""
    
    def __init__(self):
        self.redis = RedisClient()
        self.station_id = "station_07"
        
    async def initialize(self):
        """Initialize the Station 7 processor"""
        await self.redis.initialize()
        
    async def process(self, session_id: str) -> RealityCheckReport:
        """Main processing method for comprehensive validation"""
        try:
            logger.info(f"Station 7 processing started for session {session_id}")
            
            # Load all station data
            project_data = await self._load_all_station_data(session_id)
            if not project_data:
                raise ValueError("Could not load complete project data")
            
            working_title = project_data.get("working_title", "Untitled Project")
            
            # Perform comprehensive validations
            logical_result = await self._validate_logical_consistency(project_data)
            genre_result = await self._validate_genre_appropriateness(project_data)
            audio_result = await self._validate_audio_feasibility(project_data)
            production_result = await self._validate_production_viability(project_data)
            
            # Extract and classify all issues with proper error handling
            try:
                all_issues = self._extract_all_issues(logical_result, genre_result, audio_result, production_result)
                
                # Ensure all_issues is a list with robust validation
                if not isinstance(all_issues, list):
                    logger.error(f"_extract_all_issues returned {type(all_issues)} instead of list: {all_issues}")
                    all_issues = []
                
                # Validate each item in the list
                validated_issues = []
                for item in all_issues:
                    if isinstance(item, Issue):
                        validated_issues.append(item)
                    else:
                        logger.warning(f"Invalid issue object found: {type(item)} - {item}")
                
                all_issues = validated_issues
                
            except Exception as e:
                logger.error(f"Error extracting issues: {str(e)}")
                all_issues = []
            
            # Safely categorize issues
            critical_issues = []
            major_issues = []
            minor_issues = []
            
            for issue in all_issues:
                try:
                    if hasattr(issue, 'severity'):
                        if issue.severity == IssueSeverity.CRITICAL:
                            critical_issues.append(issue)
                        elif issue.severity == IssueSeverity.MAJOR:
                            major_issues.append(issue)
                        elif issue.severity == IssueSeverity.MINOR:
                            minor_issues.append(issue)
                except Exception as e:
                    logger.warning(f"Error categorizing issue: {str(e)}")
            
            # Debug logging with safe operations
            logger.info(f"Debug: Successfully processed {len(all_issues)} total issues")
            logger.info(f"Debug: {len(critical_issues)} critical, {len(major_issues)} major, {len(minor_issues)} minor")
            
            # Calculate scores
            overall_score = self._calculate_viability_score(logical_result, genre_result, audio_result, production_result)
            confidence_score = self._calculate_confidence_score(critical_issues, major_issues)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(critical_issues, major_issues, minor_issues, project_data)
            station_feedback = self._generate_station_feedback(project_data, all_issues)
            proceed_rec = self._determine_proceed_recommendation(critical_issues, major_issues, overall_score)
            
            # Create report
            report = RealityCheckReport(
                working_title=working_title,
                session_id=session_id,
                validation_timestamp=datetime.utcnow(),
                overall_viability_score=overall_score,
                logical_consistency=logical_result,
                genre_appropriateness=genre_result,
                audio_feasibility=audio_result,
                production_viability=production_result,
                critical_issues=critical_issues,
                major_issues=major_issues,
                minor_issues=minor_issues,
                recommendations=recommendations,
                station_feedback=station_feedback,
                proceed_recommendation=proceed_rec,
                confidence_score=confidence_score
            )
            
            # Store results
            await self._store_output(session_id, report)
            
            logger.info(f"Station 7 completed successfully: {len(critical_issues)} critical, {len(major_issues)} major, {len(minor_issues)} minor issues")
            return report
            
        except Exception as e:
            logger.error(f"Station 7 processing failed: {str(e)}")
            raise
    
    async def _load_all_station_data(self, session_id: str) -> Dict[str, Any]:
        """Load comprehensive data from all previous stations"""
        project_data = {"session_id": session_id, "stations_loaded": []}
        
        # Load all stations
        for station_num in range(1, 7):
            if station_num == 4:
                # Load both Station 4 and 4.5
                for sub_station in ["04", "04_5"]:
                    key = f"audiobook:{session_id}:station_{sub_station}"
                    data = await self.redis.get(key)
                    if data:
                        station_data = json.loads(data)
                        project_data[f"station_{sub_station}"] = station_data
                        project_data["stations_loaded"].append(f"station_{sub_station}")
            else:
                key = f"audiobook:{session_id}:station_{station_num:02d}"
                data = await self.redis.get(key)
                if data:
                    station_data = json.loads(data)
                    project_data[f"station_{station_num:02d}"] = station_data
                    project_data["stations_loaded"].append(f"station_{station_num:02d}")
        
        # Extract key parameters safely
        self._extract_project_parameters(project_data)
        
        logger.info(f"Loaded data from {len(project_data['stations_loaded'])} stations")
        return project_data
    
    def _extract_project_parameters(self, project_data: Dict[str, Any]):
        """Safely extract key project parameters"""
        # Station 1 data
        if "station_01" in project_data:
            station1 = project_data["station_01"]
            initial_expansion = station1.get("initial_expansion", {})
            project_data["working_title"] = initial_expansion.get("working_titles", ["Untitled"])[0]
            project_data["main_characters"] = initial_expansion.get("main_characters", [])
            project_data["core_premise"] = initial_expansion.get("core_premise", "")
            
            scale_options = station1.get("scale_options", [{}])
            if scale_options:
                scale = scale_options[0]
                project_data["episode_count"] = scale.get("episode_count", "10")
                project_data["episode_length"] = scale.get("episode_length", "45 min")
        
        # Station 2 data
        if "station_02" in project_data:
            station2 = project_data["station_02"]
            project_data["primary_genre"] = station2.get("genre_tone", {}).get("primary_genre", "Drama")
            project_data["world_setting"] = station2.get("world_setting", {})
            project_data["audience_profile"] = station2.get("audience_profile", {})
        
        # Station 3 data
        if "station_03" in project_data:
            station3 = project_data["station_03"]
            project_data["content_rating"] = station3.get("age_guidelines", {}).get("content_rating", "PG-13")
            project_data["target_age_range"] = station3.get("age_guidelines", {}).get("target_age_range", "25-45")
        
        # Station 4 data
        if "station_04" in project_data:
            station4 = project_data["station_04"]
            seed_collection = station4.get("seed_collection", {})
            if isinstance(seed_collection, dict) and "micro_moments" in seed_collection:
                # seed_collection values are already counts, not lists
                micro_moments_count = seed_collection["micro_moments"]
                if isinstance(micro_moments_count, int):
                    project_data["total_seeds"] = micro_moments_count
                else:
                    # If it's a list, get the length
                    project_data["total_seeds"] = len(micro_moments_count) if hasattr(micro_moments_count, '__len__') else 0
            else:
                project_data["total_seeds"] = 0
        
        # Station 5 data
        if "station_05" in project_data:
            station5 = project_data["station_05"]
            project_data["chosen_screenplay_style"] = station5.get("chosen_style", "Character-Driven Drama")
            project_data["episode_grid"] = station5.get("episode_grid", {})
        
        # Station 6 data
        if "station_06" in project_data:
            station6 = project_data["station_06"]
            dialect_map = station6.get("dialect_accent_map", {})
            if isinstance(dialect_map, dict):
                project_data["character_voices"] = dialect_map.get("character_voices", [])
            else:
                project_data["character_voices"] = []
            project_data["audio_conventions"] = station6.get("audio_conventions", {})
    
    async def _validate_logical_consistency(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Comprehensive logical consistency validation"""
        issues = []
        details = {}
        
        # Character consistency check
        main_chars = project_data.get("main_characters", [])
        char_voices = project_data.get("character_voices", [])
        
        if main_chars and char_voices:
            main_char_names = [self._extract_char_name(char) for char in main_chars[:2]]
            voice_names = [voice.get("character_name", "") if isinstance(voice, dict) else str(voice) for voice in char_voices]
            
            missing_chars = []
            for char_name in main_char_names:
                if not any(char_name.lower() in voice.lower() for voice in voice_names):
                    missing_chars.append(char_name)
            
            if missing_chars:
                issues.append(f"Character Consistency Issue: Main characters {missing_chars} from Station 1 are not represented in Station 6 character voice profiles")
        
        # Technology/setting consistency
        premise = project_data.get("core_premise", "")
        # Defensive programming - ensure premise is a string
        if not isinstance(premise, str):
            premise = str(premise) if premise is not None else ""
        
        world_setting = project_data.get("world_setting", {})
        
        if premise and "text" in premise.lower() and "message" in premise.lower():
            setting_period = world_setting.get("time_period", "").lower()
            setting_location = world_setting.get("primary_location", "").lower()
            
            if any(period in setting_period for period in ["historical", "period", "vintage", "1800", "1900"]):
                issues.append(f"Technology Anachronism: Story involves text messaging but world setting indicates historical period ({setting_period})")
        
        # Story complexity vs episode structure
        episode_count = project_data.get("episode_count", "10")
        try:
            ep_num = int(str(episode_count).split("-")[0])
            if len(premise) > 300 and ep_num < 8:
                issues.append(f"Structure Mismatch: Complex story premise ({len(premise)} characters) requires more episodes than planned ({ep_num})")
        except:
            pass
        
        # Genre consistency across stations
        primary_genre = project_data.get("primary_genre", "")
        chosen_style = project_data.get("chosen_screenplay_style", "")
        
        if "romance" in primary_genre.lower() and "thriller" in chosen_style.lower():
            issues.append(f"Genre Inconsistency: Primary genre is {primary_genre} but screenplay style is {chosen_style}")
        
        status = ValidationStatus.PASS if not issues else ValidationStatus.FAIL
        details = {
            "characters_checked": len(main_chars),
            "voice_profiles_checked": len(char_voices),
            "premise_length": len(premise),
            "episode_structure": episode_count
        }
        
        return ValidationResult("logical_consistency", status, issues, details)
    
    async def _validate_genre_appropriateness(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Comprehensive genre appropriateness validation"""
        issues = []
        details = {}
        
        primary_genre = project_data.get("primary_genre", "")
        target_age = project_data.get("target_age_range", "")
        content_rating = project_data.get("content_rating", "")
        premise = project_data.get("core_premise", "")
        
        # Defensive programming - ensure premise is a string
        if not isinstance(premise, str):
            premise = str(premise) if premise is not None else ""
        
        # Age rating vs content themes
        premise_lower = premise.lower()
        
        if "depression" in premise_lower and content_rating == "G":
            issues.append(f"Content Rating Mismatch: Story deals with depression themes but has G rating - should be PG-13 minimum")
        
        if "death" in premise_lower or "dying" in premise_lower:
            if target_age.startswith("13-") and content_rating in ["G", "PG"]:
                issues.append(f"Age Appropriateness Issue: Death themes with {target_age} target and {content_rating} rating may be inappropriate")
        
        # Genre vs tone consistency
        if "comedy" in primary_genre.lower() and any(theme in premise_lower for theme in ["depression", "death", "tragedy"]):
            issues.append(f"Tone Inconsistency: Comedy genre conflicts with serious themes in premise")
        
        # Target audience expectations
        if target_age.startswith("25-") and "teenager" in premise_lower:
            issues.append(f"Audience Mismatch: Story focuses on teenagers but targets adult audience ({target_age})")
        
        # Episode length vs genre expectations
        episode_length = project_data.get("episode_length", "")
        if "thriller" in primary_genre.lower() and "15" in episode_length:
            issues.append(f"Format Mismatch: Thriller genre typically needs longer episodes than {episode_length} for proper tension building")
        
        status = ValidationStatus.PASS if not issues else ValidationStatus.FAIL
        details = {
            "genre": primary_genre,
            "target_age": target_age,
            "content_rating": content_rating,
            "premise_themes_detected": [theme for theme in ["romance", "thriller", "comedy", "drama", "mystery"] if theme in premise_lower]
        }
        
        return ValidationResult("genre_appropriateness", status, issues, details)
    
    async def _validate_audio_feasibility(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Comprehensive audio feasibility validation"""
        issues = []
        details = {}
        
        premise = project_data.get("core_premise", "")
        # Defensive programming - ensure premise is a string
        if not isinstance(premise, str):
            premise = str(premise) if premise is not None else ""
            
        char_voices = project_data.get("character_voices", [])
        audio_conventions = project_data.get("audio_conventions", {})
        
        # Character voice distinction
        if len(char_voices) > 5:
            issues.append(f"Voice Acting Challenge: {len(char_voices)} character voices may be difficult to distinguish in audio-only format")
        
        # Visual dependency check
        visual_keywords = ["looking", "seeing", "watching", "visual", "color", "bright", "dark", "appearance"]
        premise_lower = premise.lower()
        visual_count = sum(1 for keyword in visual_keywords if keyword in premise_lower)
        
        if visual_count > 3:
            issues.append(f"Visual Dependency: Premise contains {visual_count} visual references that may be challenging in audio-only format")
        
        # Dialogue clarity for story information
        if len(premise) > 200 and not any(keyword in premise_lower for keyword in ["conversation", "talking", "message"]):
            issues.append(f"Exposition Challenge: Complex story without obvious dialogue/communication mechanisms for audio storytelling")
        
        # Sound design complexity
        world_setting = project_data.get("world_setting", {})
        if world_setting.get("location_variety", 0) > 10:
            issues.append(f"Production Complexity: {world_setting.get('location_variety')} different locations require extensive sound design")
        
        status = ValidationStatus.PASS if not issues else ValidationStatus.FAIL
        details = {
            "character_voices": len(char_voices),
            "visual_references": visual_count,
            "premise_length": len(premise),
            "audio_elements_present": "message" in premise_lower or "sound" in premise_lower
        }
        
        return ValidationResult("audio_feasibility", status, issues, details)
    
    async def _validate_production_viability(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Comprehensive production viability validation"""
        issues = []
        details = {}
        
        episode_count = project_data.get("episode_count", "10")
        episode_length = project_data.get("episode_length", "45 min")
        char_voices = project_data.get("character_voices", [])
        total_seeds = project_data.get("total_seeds", 0)
        
        # Cast management
        if len(char_voices) > 8:
            issues.append(f"Cast Size Issue: {len(char_voices)} characters require large voice acting budget and complex scheduling")
        
        # Content vs episode structure
        try:
            ep_num = int(str(episode_count).split("-")[0])
            if total_seeds > 0:
                seeds_per_episode = total_seeds / ep_num
                if seeds_per_episode > 15:
                    issues.append(f"Content Density Issue: {seeds_per_episode:.1f} story seeds per episode may create rushed pacing")
        except:
            pass
        
        # Technical scope assessment
        premise = project_data.get("core_premise", "")
        if "music" in premise.lower() or "singing" in premise.lower():
            issues.append(f"Technical Complexity: Musical elements require additional production resources and music licensing")
        
        # Timeline realism
        try:
            ep_num = int(str(episode_count).split("-")[0])
            length_minutes = int(re.search(r'(\d+)', episode_length).group(1)) if re.search(r'(\d+)', episode_length) else 45
            total_minutes = ep_num * length_minutes
            
            if total_minutes > 600:  # 10+ hours
                issues.append(f"Production Scale: {total_minutes} total minutes ({ep_num} episodes) is ambitious for independent production")
        except:
            pass
        
        status = ValidationStatus.PASS if not issues else ValidationStatus.FAIL
        details = {
            "episode_count": episode_count,
            "episode_length": episode_length,
            "character_count": len(char_voices),
            "story_seeds": total_seeds,
            "estimated_production_hours": f"{ep_num * 45} minutes" if 'ep_num' in locals() else "Unknown"
        }
        
        return ValidationResult("production_viability", status, issues, details)
    
    def _extract_char_name(self, character_description: str) -> str:
        """Extract clean character name from description"""
        if not character_description:
            return "Unknown"
        
        # Split on common separators and take first part
        name = character_description.split(":")[0].split("-")[0].split("(")[0].strip()
        
        # Take first word if it's still complex
        return name.split()[0] if name.split() else "Unknown"
    
    def _extract_all_issues(self, logical: ValidationResult, genre: ValidationResult, 
                           audio: ValidationResult, production: ValidationResult) -> List[Issue]:
        """Extract and classify all issues with robust error handling"""
        all_issues = []
        
        try:
            for result in [logical, genre, audio, production]:
                # Robust validation of result object
                if not hasattr(result, 'issues') or not hasattr(result, 'category'):
                    logger.warning(f"Invalid validation result object: {result}")
                    continue
                
                # Ensure result.issues is a list
                issues = result.issues
                if not isinstance(issues, list):
                    logger.warning(f"result.issues is not a list for {result.category}, got {type(issues)}: {issues}")
                    continue
                    
                # Process each issue text
                for issue_text in issues:
                    try:
                        if not isinstance(issue_text, str):
                            logger.warning(f"Issue text is not a string: {type(issue_text)} - {issue_text}")
                            continue
                            
                        severity = self._classify_severity(issue_text)
                        affected_stations = self._determine_affected_stations(issue_text, result.category)
                        fix = self._generate_fix(issue_text, result.category)
                        complexity = "high" if severity == IssueSeverity.CRITICAL else "medium" if severity == IssueSeverity.MAJOR else "low"
                        
                        issue = Issue(
                            category=result.category,
                            description=issue_text,
                            affected_stations=affected_stations,
                            recommended_fix=fix,
                            fix_complexity=complexity,
                            severity=severity
                        )
                        all_issues.append(issue)
                        
                    except Exception as e:
                        logger.error(f"Error processing individual issue: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error in _extract_all_issues: {str(e)}")
            return []
        
        return all_issues
    
    def _classify_severity(self, issue_text: str) -> IssueSeverity:
        """Classify issue severity"""
        issue_lower = issue_text.lower()
        
        critical_keywords = ["anachronism", "impossible", "breaks", "mismatch", "inappropriate"]
        major_keywords = ["challenge", "difficult", "complex", "inconsistency", "issue"]
        
        if any(keyword in issue_lower for keyword in critical_keywords):
            return IssueSeverity.CRITICAL
        elif any(keyword in issue_lower for keyword in major_keywords):
            return IssueSeverity.MAJOR
        else:
            return IssueSeverity.MINOR
    
    def _determine_affected_stations(self, issue_text: str, category: str) -> List[str]:
        """Determine affected stations"""
        mapping = {
            "logical_consistency": ["Station 1", "Station 2", "Station 5", "Station 6"],
            "genre_appropriateness": ["Station 2", "Station 3"],
            "audio_feasibility": ["Station 4", "Station 5", "Station 6"],
            "production_viability": ["Station 1", "Station 4", "Station 6"]
        }
        return mapping.get(category, ["Multiple Stations"])
    
    def _generate_fix(self, issue_text: str, category: str) -> str:
        """Generate specific fix recommendation"""
        if "character" in issue_text.lower():
            return "Update Station 6 character voice profiles to match Station 1 main characters"
        elif "genre" in issue_text.lower():
            return "Align genre elements across Station 2 (genre definition) and Station 3 (age optimization)"
        elif "anachronism" in issue_text.lower():
            return "Update Station 2 world setting to match modern technology requirements of the story"
        elif "episode" in issue_text.lower():
            return "Adjust Station 1 scale options or Station 5 episode structure for better story fit"
        else:
            return f"Review and revise {category.replace('_', ' ')} elements across affected stations"
    
    def _calculate_viability_score(self, logical: ValidationResult, genre: ValidationResult,
                                 audio: ValidationResult, production: ValidationResult) -> float:
        """Calculate overall viability score"""
        scores = []
        for result in [logical, genre, audio, production]:
            if result.status == ValidationStatus.PASS:
                scores.append(1.0)
            else:
                score = max(0.0, 1.0 - (len(result.issues) * 0.15))
                scores.append(score)
        return sum(scores) / len(scores)
    
    def _calculate_confidence_score(self, critical_issues: List[Issue], major_issues: List[Issue]) -> float:
        """Calculate confidence in validation"""
        # Robust validation of input parameters
        critical_count = len(critical_issues) if isinstance(critical_issues, list) else 0
        major_count = len(major_issues) if isinstance(major_issues, list) else 0
        
        if critical_count == 0 and major_count <= 2:
            return 0.9
        elif critical_count == 0:
            return 0.75
        elif critical_count <= 2:
            return 0.6
        else:
            return 0.4
    
    def _generate_recommendations(self, critical_issues: List[Issue], major_issues: List[Issue],
                                minor_issues: List[Issue], project_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate comprehensive recommendations"""
        # Robust validation of input parameters
        critical_issues = critical_issues if isinstance(critical_issues, list) else []
        major_issues = major_issues if isinstance(major_issues, list) else []
        minor_issues = minor_issues if isinstance(minor_issues, list) else []
            
        recommendations = {
            "immediate_actions": [],
            "optimization_opportunities": [],
            "risk_mitigation_strategies": [],
            "quality_assurance_protocols": []
        }
        
        # Immediate actions for critical issues
        for issue in critical_issues:
            try:
                recommendations["immediate_actions"].append(f"CRITICAL: {issue.recommended_fix}")
            except Exception as e:
                logger.warning(f"Error processing critical issue: {str(e)}")
        
        # Optimization for major issues
        for issue in major_issues[:3]:
            try:
                recommendations["optimization_opportunities"].append(f"IMPROVE: {issue.recommended_fix}")
            except Exception as e:
                logger.warning(f"Error processing major issue: {str(e)}")
        
        # Risk mitigation
        if len(critical_issues) > 0:
            recommendations["risk_mitigation_strategies"].append("Implement staged revision with validation checkpoints")
        if len(major_issues) > 3:
            recommendations["risk_mitigation_strategies"].append("Consider phased implementation to manage complexity")
        
        # Quality assurance
        recommendations["quality_assurance_protocols"].append("Conduct character consistency review across all stations")
        recommendations["quality_assurance_protocols"].append("Validate audio feasibility through prototype production")
        
        return recommendations
    
    def _generate_station_feedback(self, project_data: Dict[str, Any], issues: List[Issue]) -> Dict[str, str]:
        """Generate specific feedback for each station"""
        # Robust validation of input parameters
        issues = issues if isinstance(issues, list) else []
            
        feedback = {}
        
        # Initialize positive feedback
        stations = ["station_1", "station_2", "station_3", "station_4", "station_4_5", "station_5", "station_6"]
        for station in stations:
            feedback[station] = f"✅ {station.replace('_', ' ').title()} completed successfully"
        
        # Add issue-specific feedback
        for issue in issues:
            try:
                if hasattr(issue, 'affected_stations') and hasattr(issue, 'severity') and hasattr(issue, 'description'):
                    for station_name in issue.affected_stations:
                        station_key = station_name.lower().replace(" ", "_")
                        if station_key in feedback:
                            if issue.severity == IssueSeverity.CRITICAL:
                                feedback[station_key] = f"❌ CRITICAL ISSUE: {issue.description[:100]}..."
                            elif issue.severity == IssueSeverity.MAJOR:
                                feedback[station_key] = f"⚠️ NEEDS ATTENTION: {issue.description[:100]}..."
            except Exception as e:
                logger.warning(f"Error processing issue feedback: {str(e)}")
        
        return feedback
    
    def _determine_proceed_recommendation(self, critical_issues: List[Issue], 
                                        major_issues: List[Issue], overall_score: float) -> ProceedRecommendation:
        """Determine proceed recommendation"""
        # Robust validation of input parameters
        critical_issues = critical_issues if isinstance(critical_issues, list) else []
        major_issues = major_issues if isinstance(major_issues, list) else []
            
        if critical_issues:
            return ProceedRecommendation.MAJOR_REVISION_REQUIRED
        elif len(major_issues) > 3 or overall_score < 0.7:
            return ProceedRecommendation.REVISE
        else:
            return ProceedRecommendation.PROCEED
    
    async def _store_output(self, session_id: str, report: RealityCheckReport) -> None:
        """Store reality check report"""
        try:
            # Safely extract counts with validation
            critical_count = len(report.critical_issues) if isinstance(report.critical_issues, list) else 0
            major_count = len(report.major_issues) if isinstance(report.major_issues, list) else 0
            minor_count = len(report.minor_issues) if isinstance(report.minor_issues, list) else 0
            
            report_dict = {
                "station_id": self.station_id,
                "working_title": report.working_title,
                "session_id": report.session_id,
                "validation_timestamp": report.validation_timestamp.isoformat(),
                "overall_viability_score": report.overall_viability_score,
                "confidence_score": report.confidence_score,
                "proceed_recommendation": report.proceed_recommendation.value,
                "critical_issues_count": critical_count,
                "major_issues_count": major_count,
                "minor_issues_count": minor_count,
                "validation_results": {
                    "logical_consistency": report.logical_consistency.status.value,
                    "genre_appropriateness": report.genre_appropriateness.status.value,
                    "audio_feasibility": report.audio_feasibility.status.value,
                    "production_viability": report.production_viability.status.value
                },
                "recommendations": report.recommendations,
                "station_feedback": report.station_feedback
            }
            
            key = f"audiobook:{session_id}:station_07"
            await self.redis.set(key, json.dumps(report_dict), expire=86400)
            
        except Exception as e:
            logger.error(f"Failed to store Station 7 output: {str(e)}")
            raise
    
    def format_for_human_review(self, report: RealityCheckReport) -> Dict:
        """Format for human review"""
        # Safely extract counts with validation
        critical_count = len(report.critical_issues) if isinstance(report.critical_issues, list) else 0
        major_count = len(report.major_issues) if isinstance(report.major_issues, list) else 0
        minor_count = len(report.minor_issues) if isinstance(report.minor_issues, list) else 0
        
        return {
            "station": "Station 7: Reality Check System",
            "project_title": report.working_title,
            "validation_date": report.validation_timestamp.isoformat(),
            "overall_assessment": {
                "viability_score": f"{report.overall_viability_score:.2f}",
                "confidence_level": f"{report.confidence_score:.2f}",
                "recommendation": report.proceed_recommendation.value,
                "total_issues": critical_count + major_count + minor_count
            },
            "validation_summary": {
                "logical_consistency": report.logical_consistency.status.value,
                "genre_appropriateness": report.genre_appropriateness.status.value,
                "audio_feasibility": report.audio_feasibility.status.value,
                "production_viability": report.production_viability.status.value
            },
            "critical_issues": [{"description": i.description, "fix": i.recommended_fix} for i in report.critical_issues if hasattr(i, 'description') and hasattr(i, 'recommended_fix')],
            "major_issues": [{"description": i.description, "fix": i.recommended_fix} for i in report.major_issues if hasattr(i, 'description') and hasattr(i, 'recommended_fix')],
            "recommendations": report.recommendations,
            "station_feedback": report.station_feedback
        }