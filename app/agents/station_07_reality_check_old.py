"""
Station 7: Reality Check System

This agent performs comprehensive validation of the complete audiobook project
by analyzing all outputs from Stations 1-6 for logical consistency, genre 
appropriateness, audio feasibility, and production viability.

Dependencies: All previous stations (1-6)
Outputs: Reality Check Report with validation results and recommendations
Human Gate: CRITICAL - Project approval before script development begins
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.openrouter_agent import OpenRouterAgent
from app.redis_client import RedisClient
from app.config import Settings

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
    """Individual validation result"""
    category: str
    status: ValidationStatus
    issues: List[str]
    details: Dict[str, Any]

@dataclass
class Issue:
    """Individual issue found during validation"""
    category: str
    description: str
    affected_stations: List[str]
    recommended_fix: str
    fix_complexity: str
    severity: IssueSeverity

@dataclass
class RealityCheckReport:
    """Complete reality check validation report"""
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
    """
    Station 7: Reality Check System
    
    Responsibilities:
    1. Validate logical consistency across all project elements
    2. Assess genre appropriateness and audience alignment
    3. Evaluate audio feasibility for production
    4. Check production viability and resource requirements
    5. Generate comprehensive validation report with recommendations
    """
    
    def __init__(self):
        self.openrouter = OpenRouterAgent()
        self.redis = RedisClient()
        self.station_id = "station_07"
        
        # Validation templates
        self.validation_prompts = self._load_validation_prompts()
        
    async def initialize(self):
        """Initialize the Station 7 processor"""
        await self.redis.initialize()
        
    def _load_validation_prompts(self) -> Dict[str, str]:
        """Load specialized validation prompts"""
        return {
            "logical_consistency": """
You are validating logical consistency across all audiobook project elements.

PROJECT DATA:
{project_data}

VALIDATION REQUIREMENTS:
1. Check world rules consistency across all stations
2. Verify character consistency (voices, abilities, knowledge)
3. Validate timeline feasibility and episode pacing
4. Ensure technology/magic systems are coherent

Analyze each element and identify specific inconsistencies.
Return detailed findings focusing on story logic breaks.
""",

            "genre_appropriateness": """
You are validating genre appropriateness for the target audience.

PROJECT DATA:
{project_data}

TARGET: {target_age_range} audience, {content_rating} rating, {primary_genre} genre

VALIDATION REQUIREMENTS:
1. Verify tone consistency matches genre expectations
2. Check pacing alignment with genre conventions
3. Validate stakes appropriateness for age rating
4. Ensure audience expectations will be met

Identify specific genre misalignments and age-inappropriate content.
""",

            "audio_feasibility": """
You are validating audio-only production feasibility.

PROJECT DATA:
{project_data}

VALIDATION REQUIREMENTS:
1. Check if visual elements can be translated to audio
2. Assess sound design technical requirements
3. Verify dialogue clarity for story comprehension
4. Validate scene transition effectiveness

Identify specific audio production challenges and impossibilities.
""",

            "production_viability": """
You are validating production viability and resource requirements.

PROJECT DATA:
{project_data}

PRODUCTION CONTEXT: {episode_count} episodes × {episode_length}

VALIDATION REQUIREMENTS:
1. Assess cast management complexity
2. Evaluate technical scope and requirements
3. Check episode structure feasibility
4. Validate resource allocation needs

Identify specific production challenges and resource mismatches.
"""
        }
    
    async def process(self, session_id: str) -> RealityCheckReport:
        """
        Main processing method for Station 7
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            RealityCheckReport: Complete validation analysis
        """
        try:
            logger.info(f"Station 7 processing started for session {session_id}")
            
            # Load all previous station data
            project_data = await self._load_all_station_data(session_id)
            if not project_data:
                raise ValueError("Could not load complete project data from previous stations")
            
            working_title = project_data.get("working_title", "Untitled Project")
            logger.info(f"Validating project: {working_title}")
            
            # Perform comprehensive validation
            logical_result = await self._validate_logical_consistency(project_data)
            genre_result = await self._validate_genre_appropriateness(project_data)
            audio_result = await self._validate_audio_feasibility(project_data)
            production_result = await self._validate_production_viability(project_data)
            
            # Analyze issues and generate recommendations
            all_issues = self._extract_all_issues(logical_result, genre_result, audio_result, production_result)
            critical_issues = [issue for issue in all_issues if issue.severity == IssueSeverity.CRITICAL]
            major_issues = [issue for issue in all_issues if issue.severity == IssueSeverity.MAJOR]
            minor_issues = [issue for issue in all_issues if issue.severity == IssueSeverity.MINOR]
            
            # Calculate viability scores
            overall_score = self._calculate_viability_score(logical_result, genre_result, audio_result, production_result)
            confidence_score = self._calculate_confidence_score(critical_issues, major_issues)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(critical_issues, major_issues, minor_issues, project_data)
            
            # Create station-specific feedback
            station_feedback = self._generate_station_feedback(project_data, all_issues)
            
            # Determine proceed recommendation
            proceed_rec = self._determine_proceed_recommendation(critical_issues, major_issues, overall_score)
            
            # Compile final report
            reality_check_report = RealityCheckReport(
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
            await self._store_output(session_id, reality_check_report)
            
            logger.info(f"Station 7 completed: {len(critical_issues)} critical, {len(major_issues)} major, {len(minor_issues)} minor issues")
            return reality_check_report
            
        except Exception as e:
            logger.error(f"Station 7 processing failed for session {session_id}: {str(e)}")
            raise
    
    async def _load_all_station_data(self, session_id: str) -> Dict[str, Any]:
        """Load and compile data from all previous stations"""
        try:
            project_data = {
                "session_id": session_id,
                "stations_loaded": []
            }
            
            # Load each station's data
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
            
            # Extract key project parameters
            if "station_01" in project_data:
                station1 = project_data["station_01"]
                project_data["working_title"] = station1.get("initial_expansion", {}).get("working_titles", ["Untitled"])[0]
                project_data["main_characters"] = station1.get("initial_expansion", {}).get("main_characters", [])
                project_data["core_premise"] = station1.get("initial_expansion", {}).get("core_premise", "")
                project_data["episode_count"] = station1.get("scale_options", [{}])[0].get("episode_count", "10")
                project_data["episode_length"] = station1.get("scale_options", [{}])[0].get("episode_length", "45 min")
            
            if "station_02" in project_data:
                station2 = project_data["station_02"]
                project_data["primary_genre"] = station2.get("genre_tone", {}).get("primary_genre", "Drama")
                project_data["target_age_range"] = station2.get("audience_profile", {}).get("primary_age_range", "25-45")
                project_data["world_setting"] = station2.get("world_setting", {})
            
            if "station_03" in project_data:
                station3 = project_data["station_03"]
                project_data["content_rating"] = station3.get("age_guidelines", {}).get("content_rating", "PG-13")
                project_data["tone_calibration"] = station3.get("tone_calibration", {})
            
            if "station_04" in project_data:
                station4 = project_data["station_04"]
                seed_collection = station4.get("seed_collection", {})
                if isinstance(seed_collection, dict):
                    micro_moments = seed_collection.get("micro_moments", [])
                    project_data["total_seeds"] = len(micro_moments) if isinstance(micro_moments, list) else 0
                else:
                    project_data["total_seeds"] = 0
            
            if "station_05" in project_data:
                station5 = project_data["station_05"]
                project_data["chosen_screenplay_style"] = station5.get("chosen_style", "Character-Driven Drama")
                project_data["episode_grid"] = station5.get("episode_grid", {})
            
            if "station_06" in project_data:
                station6 = project_data["station_06"]
                dialect_map = station6.get("dialect_accent_map", {})
                if isinstance(dialect_map, dict):
                    character_voices = dialect_map.get("character_voices", [])
                    project_data["character_voices"] = character_voices if isinstance(character_voices, list) else []
                else:
                    project_data["character_voices"] = []
                project_data["audio_conventions"] = station6.get("audio_conventions", {})
            
            logger.info(f"Loaded data from {len(project_data['stations_loaded'])} stations")
            return project_data
            
        except Exception as e:
            logger.error(f"Failed to load all station data: {str(e)}")
            return None
    
    async def _validate_logical_consistency(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Validate logical consistency across all project elements"""
        try:
            # Format prompt with project data
            prompt = self.validation_prompts["logical_consistency"].format(
                project_data=json.dumps(project_data, indent=2)
            )
            
            # Perform comprehensive logic-based validation instead of AI
            issues = self._analyze_logical_consistency(project_data)
            response = f"Analyzed {len(project_data.get('stations_loaded', []))} stations for logical consistency"
            
            # Determine status
            status = ValidationStatus.FAIL if issues else ValidationStatus.PASS
            
            return ValidationResult(
                category="logical_consistency",
                status=status,
                issues=issues,
                details={"analysis": response}
            )
            
        except Exception as e:
            logger.error(f"Logical consistency validation failed: {str(e)}")
            return ValidationResult(
                category="logical_consistency",
                status=ValidationStatus.FAIL,
                issues=[f"Validation error: {str(e)}"],
                details={}
            )
    
    async def _validate_genre_appropriateness(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Validate genre appropriateness for target audience"""
        try:
            prompt = self.validation_prompts["genre_appropriateness"].format(
                project_data=json.dumps(project_data, indent=2),
                target_age_range=project_data.get("target_age_range", "25-45"),
                content_rating=project_data.get("content_rating", "PG-13"),
                primary_genre=project_data.get("primary_genre", "Drama")
            )
            
            response = await self.openrouter.generate(
                prompt=prompt,
                model="grok-4",
                max_tokens=2000,
                temperature=0.3
            )
            
            issues = self._parse_validation_response(response, "genre_appropriateness")
            status = ValidationStatus.FAIL if issues else ValidationStatus.PASS
            
            return ValidationResult(
                category="genre_appropriateness",
                status=status,
                issues=issues,
                details={"analysis": response}
            )
            
        except Exception as e:
            logger.error(f"Genre appropriateness validation failed: {str(e)}")
            return ValidationResult(
                category="genre_appropriateness",
                status=ValidationStatus.FAIL,
                issues=[f"Validation error: {str(e)}"],
                details={}
            )
    
    async def _validate_audio_feasibility(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Validate audio-only production feasibility"""
        try:
            prompt = self.validation_prompts["audio_feasibility"].format(
                project_data=json.dumps(project_data, indent=2)
            )
            
            response = await self.openrouter.generate(
                prompt=prompt,
                model="grok-4",
                max_tokens=2000,
                temperature=0.3
            )
            
            issues = self._parse_validation_response(response, "audio_feasibility")
            status = ValidationStatus.FAIL if issues else ValidationStatus.PASS
            
            return ValidationResult(
                category="audio_feasibility",
                status=status,
                issues=issues,
                details={"analysis": response}
            )
            
        except Exception as e:
            logger.error(f"Audio feasibility validation failed: {str(e)}")
            return ValidationResult(
                category="audio_feasibility",
                status=ValidationStatus.FAIL,
                issues=[f"Validation error: {str(e)}"],
                details={}
            )
    
    async def _validate_production_viability(self, project_data: Dict[str, Any]) -> ValidationResult:
        """Validate production viability and resource requirements"""
        try:
            prompt = self.validation_prompts["production_viability"].format(
                project_data=json.dumps(project_data, indent=2),
                episode_count=project_data.get("episode_count", "10"),
                episode_length=project_data.get("episode_length", "45 min")
            )
            
            response = await self.openrouter.generate(
                prompt=prompt,
                model="grok-4",
                max_tokens=2000,
                temperature=0.3
            )
            
            issues = self._parse_validation_response(response, "production_viability")
            status = ValidationStatus.FAIL if issues else ValidationStatus.PASS
            
            return ValidationResult(
                category="production_viability",
                status=status,
                issues=issues,
                details={"analysis": response}
            )
            
        except Exception as e:
            logger.error(f"Production viability validation failed: {str(e)}")
            return ValidationResult(
                category="production_viability",
                status=ValidationStatus.FAIL,
                issues=[f"Validation error: {str(e)}"],
                details={}
            )
    
    def _parse_validation_response(self, response: str, category: str) -> List[str]:
        """Parse AI validation response to extract specific issues"""
        issues = []
        
        # Look for common issue indicators
        issue_indicators = [
            "inconsistency", "contradiction", "inappropriate", "impossible",
            "unrealistic", "confusing", "unclear", "problematic", "conflict",
            "mismatch", "error", "issue", "problem", "concern", "fails to"
        ]
        
        lines = response.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            if any(indicator in line_lower for indicator in issue_indicators):
                if len(line.strip()) > 10:  # Avoid very short lines
                    issues.append(line.strip())
        
        return issues[:10]  # Limit to top 10 issues
    
    def _extract_all_issues(self, logical: ValidationResult, genre: ValidationResult, 
                           audio: ValidationResult, production: ValidationResult) -> List[Issue]:
        """Extract and classify all issues from validation results"""
        all_issues = []
        
        # Process each validation result
        for result in [logical, genre, audio, production]:
            for issue_text in result.issues:
                # Classify severity based on keywords
                severity = self._classify_issue_severity(issue_text)
                
                # Determine affected stations (simplified)
                affected_stations = self._determine_affected_stations(issue_text, result.category)
                
                # Generate recommended fix
                recommended_fix = self._generate_fix_recommendation(issue_text, result.category)
                
                # Assess fix complexity
                fix_complexity = self._assess_fix_complexity(issue_text, severity)
                
                issue = Issue(
                    category=result.category,
                    description=issue_text,
                    affected_stations=affected_stations,
                    recommended_fix=recommended_fix,
                    fix_complexity=fix_complexity,
                    severity=severity
                )
                
                all_issues.append(issue)
        
        return all_issues
    
    def _classify_issue_severity(self, issue_text: str) -> IssueSeverity:
        """Classify issue severity based on content analysis"""
        issue_lower = issue_text.lower()
        
        # Critical indicators
        critical_keywords = [
            "impossible", "breaks", "contradicts", "fails", "inappropriate for age",
            "exceeds capability", "logic error", "major inconsistency"
        ]
        
        # Major indicators  
        major_keywords = [
            "confusing", "unclear", "misaligned", "problematic", "concerning",
            "difficult", "challenging", "inconsistent"
        ]
        
        if any(keyword in issue_lower for keyword in critical_keywords):
            return IssueSeverity.CRITICAL
        elif any(keyword in issue_lower for keyword in major_keywords):
            return IssueSeverity.MAJOR
        else:
            return IssueSeverity.MINOR
    
    def _determine_affected_stations(self, issue_text: str, category: str) -> List[str]:
        """Determine which stations are affected by the issue"""
        affected = []
        
        # Map categories to likely affected stations
        category_mapping = {
            "logical_consistency": ["Station 1", "Station 2", "Station 5"],
            "genre_appropriateness": ["Station 2", "Station 3", "Station 6"],
            "audio_feasibility": ["Station 4", "Station 5", "Station 6"],
            "production_viability": ["Station 2", "Station 4", "Station 6"]
        }
        
        return category_mapping.get(category, ["Multiple Stations"])
    
    def _generate_fix_recommendation(self, issue_text: str, category: str) -> str:
        """Generate specific fix recommendation for the issue"""
        # Generate contextual recommendations based on category
        fix_templates = {
            "logical_consistency": "Review and align conflicting elements across affected stations",
            "genre_appropriateness": "Adjust tone, pacing, or content to better match genre conventions",
            "audio_feasibility": "Redesign visual elements for effective audio-only presentation",
            "production_viability": "Simplify technical requirements or adjust scope to match capabilities"
        }
        
        return fix_templates.get(category, "Review and revise affected project elements")
    
    def _assess_fix_complexity(self, issue_text: str, severity: IssueSeverity) -> str:
        """Assess the complexity of fixing the issue"""
        if severity == IssueSeverity.CRITICAL:
            return "high"
        elif severity == IssueSeverity.MAJOR:
            return "medium"
        else:
            return "low"
    
    def _calculate_viability_score(self, logical: ValidationResult, genre: ValidationResult,
                                 audio: ValidationResult, production: ValidationResult) -> float:
        """Calculate overall project viability score"""
        scores = []
        
        for result in [logical, genre, audio, production]:
            if result.status == ValidationStatus.PASS:
                scores.append(1.0)
            else:
                # Score based on number of issues (fewer issues = higher score)
                issue_count = len(result.issues)
                score = max(0.0, 1.0 - (issue_count * 0.1))
                scores.append(score)
        
        return sum(scores) / len(scores)
    
    def _calculate_confidence_score(self, critical_issues: List[Issue], major_issues: List[Issue]) -> float:
        """Calculate confidence in the validation results"""
        # High confidence if no critical issues, moderate if no critical but some major
        if not critical_issues and not major_issues:
            return 0.95
        elif not critical_issues and len(major_issues) <= 3:
            return 0.8
        elif not critical_issues:
            return 0.7
        elif len(critical_issues) <= 2:
            return 0.6
        else:
            return 0.4
    
    def _generate_recommendations(self, critical_issues: List[Issue], major_issues: List[Issue],
                                minor_issues: List[Issue], project_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate comprehensive recommendations"""
        recommendations = {
            "immediate_actions": [],
            "optimization_opportunities": [],
            "risk_mitigation_strategies": [],
            "quality_assurance_protocols": []
        }
        
        # Immediate actions for critical issues
        for issue in critical_issues:
            recommendations["immediate_actions"].append(f"Address critical {issue.category} issue: {issue.recommended_fix}")
        
        # Optimization for major issues
        for issue in major_issues[:3]:  # Top 3 major issues
            recommendations["optimization_opportunities"].append(f"Improve {issue.category}: {issue.recommended_fix}")
        
        # Risk mitigation
        if critical_issues:
            recommendations["risk_mitigation_strategies"].append("Implement staged validation checkpoints during revision")
        if len(major_issues) > 5:
            recommendations["risk_mitigation_strategies"].append("Consider phased implementation to manage complexity")
        
        # Quality assurance
        recommendations["quality_assurance_protocols"].append("Conduct cross-station consistency reviews")
        recommendations["quality_assurance_protocols"].append("Validate audio feasibility through prototype testing")
        
        return recommendations
    
    def _generate_station_feedback(self, project_data: Dict[str, Any], issues: List[Issue]) -> Dict[str, str]:
        """Generate specific feedback for each station"""
        feedback = {}
        
        # Initialize with positive feedback
        for i in range(1, 7):
            station_key = f"station_{i}"
            if i == 4:
                feedback["station_4"] = "Reference mining and seed generation completed successfully"
                feedback["station_4_5"] = "Narrator strategy development completed successfully"
            else:
                feedback[station_key] = f"Station {i} processing completed successfully"
        
        # Add issue-specific feedback
        for issue in issues:
            for station in issue.affected_stations:
                station_num = station.lower().replace("station ", "").replace(" ", "_")
                if f"station_{station_num}" not in feedback:
                    feedback[f"station_{station_num}"] = ""
                
                if issue.severity == IssueSeverity.CRITICAL:
                    feedback[f"station_{station_num}"] += f" CRITICAL: {issue.description[:100]}..."
                elif issue.severity == IssueSeverity.MAJOR:
                    feedback[f"station_{station_num}"] += f" Review needed: {issue.description[:100]}..."
        
        return feedback
    
    def _determine_proceed_recommendation(self, critical_issues: List[Issue], 
                                        major_issues: List[Issue], overall_score: float) -> ProceedRecommendation:
        """Determine whether project should proceed or requires revision"""
        if critical_issues:
            return ProceedRecommendation.MAJOR_REVISION_REQUIRED
        elif len(major_issues) > 5 or overall_score < 0.7:
            return ProceedRecommendation.REVISE
        else:
            return ProceedRecommendation.PROCEED
    
    async def _store_output(self, session_id: str, report: RealityCheckReport) -> None:
        """Store reality check report in Redis"""
        try:
            # Convert to dictionary for JSON serialization
            report_dict = {
                "station_id": self.station_id,
                "working_title": report.working_title,
                "session_id": report.session_id,
                "validation_timestamp": report.validation_timestamp.isoformat(),
                "overall_viability_score": report.overall_viability_score,
                "validation_results": {
                    "logical_consistency": {
                        "status": report.logical_consistency.status.value,
                        "issues": report.logical_consistency.issues,
                        "details": report.logical_consistency.details
                    },
                    "genre_appropriateness": {
                        "status": report.genre_appropriateness.status.value,
                        "issues": report.genre_appropriateness.issues,
                        "details": report.genre_appropriateness.details
                    },
                    "audio_feasibility": {
                        "status": report.audio_feasibility.status.value,
                        "issues": report.audio_feasibility.issues,
                        "details": report.audio_feasibility.details
                    },
                    "production_viability": {
                        "status": report.production_viability.status.value,
                        "issues": report.production_viability.issues,
                        "details": report.production_viability.details
                    }
                },
                "issue_summary": {
                    "critical_issues": [
                        {
                            "category": issue.category,
                            "description": issue.description,
                            "affected_stations": issue.affected_stations,
                            "recommended_fix": issue.recommended_fix,
                            "fix_complexity": issue.fix_complexity,
                            "severity": issue.severity.value
                        } for issue in report.critical_issues
                    ],
                    "major_issues": [
                        {
                            "category": issue.category,
                            "description": issue.description,
                            "affected_stations": issue.affected_stations,
                            "recommended_fix": issue.recommended_fix,
                            "fix_complexity": issue.fix_complexity,
                            "severity": issue.severity.value
                        } for issue in report.major_issues
                    ],
                    "minor_issues": [
                        {
                            "category": issue.category,
                            "description": issue.description,
                            "affected_stations": issue.affected_stations,
                            "recommended_fix": issue.recommended_fix,
                            "fix_complexity": issue.fix_complexity,
                            "severity": issue.severity.value
                        } for issue in report.minor_issues
                    ]
                },
                "recommendations": report.recommendations,
                "station_feedback": report.station_feedback,
                "proceed_recommendation": report.proceed_recommendation.value,
                "confidence_score": report.confidence_score
            }
            
            # Store in Redis
            key = f"audiobook:{session_id}:station_07"
            await self.redis.set(key, json.dumps(report_dict), expire=86400)  # 24 hour expiry
            
            logger.info(f"Station 7 reality check report stored for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store Station 7 output: {str(e)}")
            raise
    
    def format_for_human_review(self, report: RealityCheckReport) -> Dict:
        """Format reality check report for human review"""
        return {
            "station": "Station 7: Reality Check System",
            "status": f"validation_complete_{report.proceed_recommendation.value.lower()}",
            "project_title": report.working_title,
            "overall_assessment": {
                "viability_score": f"{report.overall_viability_score:.2f}",
                "confidence_level": f"{report.confidence_score:.2f}",
                "proceed_recommendation": report.proceed_recommendation.value,
                "total_issues": len(report.critical_issues) + len(report.major_issues) + len(report.minor_issues)
            },
            "critical_issues": [
                {
                    "description": issue.description,
                    "fix_needed": issue.recommended_fix,
                    "complexity": issue.fix_complexity
                } for issue in report.critical_issues
            ],
            "major_issues": [
                {
                    "description": issue.description,
                    "improvement": issue.recommended_fix,
                    "complexity": issue.fix_complexity
                } for issue in report.major_issues
            ],
            "validation_summary": {
                "logical_consistency": report.logical_consistency.status.value,
                "genre_appropriateness": report.genre_appropriateness.status.value,
                "audio_feasibility": report.audio_feasibility.status.value,
                "production_viability": report.production_viability.status.value
            },
            "next_steps": report.recommendations["immediate_actions"],
            "next_station": "Script Development" if report.proceed_recommendation == ProceedRecommendation.PROCEED else "Revision Required"
        }