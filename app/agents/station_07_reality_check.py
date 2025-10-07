#!/usr/bin/env python3
"""
Station 7: Reality Check - Comprehensive Quality Assurance
A checkpoint station that validates all previous stations have generated properly,
ensures no fallback content or hardcoded elements, and provides comprehensive
analysis of LLM outputs vs expected deliverables.
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path

from app.openrouter_agent import OpenRouterAgent
from app.agents.config_loader import load_station_config
from app.redis_client import RedisClient
from app.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StationValidation:
    """Validation result for a single station"""
    station_number: str
    station_name: str
    status: str  # "PASS", "FAIL", "WARNING"
    expected_outputs: List[str]
    actual_outputs: List[str]
    missing_outputs: List[str]
    quality_score: float  # 0.0 to 1.0
    llm_content_analysis: Dict[str, Any]
    fallback_detection: Dict[str, bool]
    issues: List[str]
    recommendations: List[str]

@dataclass
class LLMOutputAnalysis:
    """Analysis of LLM-generated content"""
    station: str
    total_text_length: int
    unique_phrases_count: int
    creativity_indicators: List[str]
    generic_patterns_found: List[str]
    hardcoded_examples_detected: List[str]
    ai_fingerprints: List[str]
    originality_score: float  # 0.0 to 1.0
    coherence_score: float    # 0.0 to 1.0

@dataclass
class QualityMetrics:
    """Overall quality metrics for the entire pipeline"""
    total_stations_validated: int
    stations_passed: int
    stations_failed: int
    stations_with_warnings: int
    overall_quality_score: float
    pipeline_integrity: bool
    creative_uniqueness_score: float
    technical_completeness_score: float

@dataclass
class Station07Output:
    """Complete output from Station 7 Reality Check"""
    session_id: str
    validation_timestamp: datetime
    pipeline_status: str  # "PASSED", "FAILED", "NEEDS_ATTENTION"
    station_validations: List[StationValidation]
    llm_analyses: List[LLMOutputAnalysis]
    quality_metrics: QualityMetrics
    executive_summary: str
    detailed_report: str
    recommendations: List[str]
    files_validated: List[str]
    critical_issues: List[str]

class Station07RealityCheck:
    """Station 7: Comprehensive Pipeline Validation"""
    
    def __init__(self):
        self.settings = Settings()
        self.redis_client = None
        self.openrouter_agent = None
        self.debug_mode = False
        
        # Load station configuration from YML
        self.config = load_station_config(station_number=7)
        
        # Hardcoded patterns to detect
        self.fallback_indicators = [
            "Lorem ipsum", "TODO", "PLACEHOLDER", "EXAMPLE",
            "Sample text", "Insert here", "Replace with",
            "Default value", "Template", "Boilerplate"
        ]
        
        # Generic AI output patterns
        self.generic_patterns = [
            "In conclusion", "It is important to note",
            "Furthermore", "Additionally", "Moreover",
            "In summary", "To summarize", "In other words",
            "As we can see", "It should be noted"
        ]
        
        # Expected outputs per station
        self.station_requirements = {
            "01": {
                "name": "Seed Processor",
                "required_fields": [
                    "original_seed", "scale_options", "recommended_option",
                    "initial_expansion", "processing_timestamp"
                ],
                "expected_counts": {
                    "scale_options": 3,
                    "working_titles": 3,
                    "main_characters": ">=1"
                }
            },
            "02": {
                "name": "Project DNA Builder",
                "required_fields": [
                    "working_title", "world_setting", "format_specifications",
                    "genre_tone", "audience_profile", "production_constraints"
                ],
                "expected_counts": {
                    "creative_promises": ">=3",
                    "creative_team": ">=1"
                }
            },
            "03": {
                "name": "Age Genre Optimizer",
                "required_fields": [
                    "working_title", "age_guidelines", "genre_options",
                    "chosen_genre_blend", "tone_calibration"
                ],
                "expected_counts": {
                    "genre_options": ">=2"
                }
            },
            "04": {
                "name": "Reference Miner",
                "required_fields": [
                    "working_title", "total_references", "total_extractions",
                    "total_seeds", "seed_collection", "quality_metrics"
                ],
                "expected_counts": {
                    "total_seeds": ">=10",
                    "total_references": ">=3"
                }
            },
            "04.5": {
                "name": "Narrator Strategy",
                "required_fields": [
                    "working_title", "recommendation", "executive_summary",
                    "complexity_score", "sample_scenes_count", "production_impact"
                ],
                "expected_counts": {
                    "sample_scenes_count": ">=1"
                }
            },
            "05": {
                "name": "Season Architecture",
                "required_fields": [
                    "working_title", "chosen_style", "total_episodes",
                    "confidence_score", "narrator_integration"
                ],
                "expected_counts": {
                    "total_episodes": ">=3"
                }
            },
            "06": {
                "name": "Master Style Guide",
                "required_fields": [
                    "working_title", "character_voices_count", "audio_conventions_count",
                    "has_narrator", "sonic_elements_count", "language_rules_complete"
                ],
                "expected_counts": {
                    "character_voices_count": ">=1"
                }
            }
        }

    async def initialize(self):
        """Initialize the station components"""
        try:
            self.redis_client = RedisClient()
            await self.redis_client.initialize()
            
            self.openrouter_agent = OpenRouterAgent()
            # OpenRouter agent doesn't need initialization
            
            logger.info("✅ Station 7 Reality Check initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Station 7: {e}")
            raise

    def enable_debug_mode(self):
        """Enable debug mode for detailed logging"""
        self.debug_mode = True
        logger.info("🐛 Debug mode enabled for Station 7")

    async def process(self, session_id: str) -> Station07Output:
        """Main processing function for Station 7"""
        
        logger.info(f"🔍 Station 7: Starting Reality Check for session {session_id}")
        
        try:
            # Load all station outputs from Redis
            station_data = await self._load_all_station_data(session_id)
            
            # Validate each station
            validations = []
            llm_analyses = []
            
            for station_num in ["01", "02", "03", "04", "04.5", "05", "06"]:
                validation = await self._validate_station(station_num, station_data.get(station_num))
                validations.append(validation)
                
                if station_data.get(station_num):
                    analysis = await self._analyze_llm_output(station_num, station_data[station_num])
                    llm_analyses.append(analysis)
            
            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(validations, llm_analyses)
            
            # Generate reports
            executive_summary = await self._generate_executive_summary(validations, quality_metrics)
            detailed_report = await self._generate_detailed_report(validations, llm_analyses)
            recommendations = await self._generate_recommendations(validations, quality_metrics)
            
            # Determine overall status
            pipeline_status = self._determine_pipeline_status(quality_metrics)
            
            # Get list of files that should have been generated
            files_validated = await self._validate_generated_files(session_id)
            
            # Identify critical issues
            critical_issues = self._identify_critical_issues(validations)
            
            result = Station07Output(
                session_id=session_id,
                validation_timestamp=datetime.now(),
                pipeline_status=pipeline_status,
                station_validations=validations,
                llm_analyses=llm_analyses,
                quality_metrics=quality_metrics,
                executive_summary=executive_summary,
                detailed_report=detailed_report,
                recommendations=recommendations,
                files_validated=files_validated,
                critical_issues=critical_issues
            )
            
            logger.info(f"✅ Station 7 completed: {pipeline_status}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Station 7 failed: {e}")
            raise

    async def _load_all_station_data(self, session_id: str) -> Dict[str, Dict]:
        """Load all station outputs from Redis"""
        
        station_data = {}
        
        for station_num in ["01", "02", "03", "04", "04_5", "05", "06"]:
            try:
                redis_key = f"audiobook:{session_id}:station_{station_num}"
                data = await self.redis_client.get(redis_key)
                
                if data:
                    station_data[station_num.replace("_", ".")] = json.loads(data)
                    if self.debug_mode:
                        logger.info(f"✅ Loaded Station {station_num} data")
                else:
                    logger.warning(f"⚠️ No data found for Station {station_num}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to load Station {station_num}: {e}")
        
        return station_data

    async def _validate_station(self, station_num: str, station_data: Optional[Dict]) -> StationValidation:
        """Validate a single station's output"""
        
        requirements = self.station_requirements[station_num]
        station_name = requirements["name"]
        
        if not station_data:
            return StationValidation(
                station_number=station_num,
                station_name=station_name,
                status="FAIL",
                expected_outputs=requirements["required_fields"],
                actual_outputs=[],
                missing_outputs=requirements["required_fields"],
                quality_score=0.0,
                llm_content_analysis={},
                fallback_detection={},
                issues=["Station data not found"],
                recommendations=["Re-run this station"]
            )
        
        # Check required fields
        actual_outputs = list(station_data.keys())
        missing_outputs = [field for field in requirements["required_fields"] 
                          if field not in actual_outputs]
        
        # Check expected counts
        count_issues = []
        for field, expected in requirements.get("expected_counts", {}).items():
            if field in station_data:
                actual_count = self._get_field_count(station_data[field])
                if not self._meets_count_requirement(actual_count, expected):
                    count_issues.append(f"{field}: expected {expected}, got {actual_count}")
        
        # Detect fallback content
        fallback_detection = self._detect_fallback_content(station_data)
        
        # Calculate quality score
        quality_score = self._calculate_station_quality_score(
            missing_outputs, count_issues, fallback_detection
        )
        
        # Determine status
        status = "PASS"
        issues = []
        
        if missing_outputs:
            status = "FAIL"
            issues.extend([f"Missing required field: {field}" for field in missing_outputs])
        
        if count_issues:
            if status != "FAIL":
                status = "WARNING"
            issues.extend(count_issues)
        
        if any(fallback_detection.values()):
            status = "FAIL"
            issues.append("Fallback content detected")
        
        # Generate recommendations
        recommendations = self._generate_station_recommendations(
            station_num, missing_outputs, count_issues, fallback_detection
        )
        
        return StationValidation(
            station_number=station_num,
            station_name=station_name,
            status=status,
            expected_outputs=requirements["required_fields"],
            actual_outputs=actual_outputs,
            missing_outputs=missing_outputs,
            quality_score=quality_score,
            llm_content_analysis={},
            fallback_detection=fallback_detection,
            issues=issues,
            recommendations=recommendations
        )

    async def _analyze_llm_output(self, station_num: str, station_data: Dict) -> LLMOutputAnalysis:
        """Analyze LLM-generated content for quality and originality"""
        
        # Extract all text content
        text_content = self._extract_text_content(station_data)
        
        # Calculate metrics
        total_length = len(text_content)
        unique_phrases = self._count_unique_phrases(text_content)
        creativity_indicators = self._find_creativity_indicators(text_content)
        generic_patterns = self._find_generic_patterns(text_content)
        hardcoded_examples = self._find_hardcoded_examples(text_content)
        ai_fingerprints = self._find_ai_fingerprints(text_content)
        
        # Calculate scores
        originality_score = self._calculate_originality_score(
            unique_phrases, generic_patterns, hardcoded_examples
        )
        coherence_score = await self._calculate_coherence_score(text_content)
        
        return LLMOutputAnalysis(
            station=station_num,
            total_text_length=total_length,
            unique_phrases_count=len(unique_phrases),
            creativity_indicators=creativity_indicators,
            generic_patterns_found=generic_patterns,
            hardcoded_examples_detected=hardcoded_examples,
            ai_fingerprints=ai_fingerprints,
            originality_score=originality_score,
            coherence_score=coherence_score
        )

    def _extract_text_content(self, data: Any) -> str:
        """Recursively extract all text content from data structure"""
        
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            return " ".join(self._extract_text_content(value) for value in data.values())
        elif isinstance(data, list):
            return " ".join(self._extract_text_content(item) for item in data)
        else:
            return str(data)

    def _detect_fallback_content(self, data: Dict) -> Dict[str, bool]:
        """Detect fallback, placeholder, or hardcoded content"""
        
        text_content = self._extract_text_content(data)
        
        detection_results = {}
        
        # Check for fallback indicators
        detection_results["has_placeholders"] = any(
            indicator.lower() in text_content.lower() 
            for indicator in self.fallback_indicators
        )
        
        # Check for generic AI patterns
        detection_results["has_generic_patterns"] = any(
            pattern.lower() in text_content.lower() 
            for pattern in self.generic_patterns
        )
        
        # Check for repeated phrases (indicating templates)
        detection_results["has_repeated_templates"] = self._has_repeated_templates(text_content)
        
        # Check for insufficient content length
        detection_results["insufficient_content"] = len(text_content.strip()) < 100
        
        return detection_results

    def _has_repeated_templates(self, text: str) -> bool:
        """Check for repeated template phrases"""
        
        sentences = text.split('.')
        sentence_counts = {}
        
        for sentence in sentences:
            cleaned = sentence.strip().lower()
            if len(cleaned) > 20:  # Only check substantial sentences
                sentence_counts[cleaned] = sentence_counts.get(cleaned, 0) + 1
        
        # If any sentence appears more than twice, it's likely templated
        return any(count > 2 for count in sentence_counts.values())

    def _calculate_quality_metrics(self, validations: List[StationValidation], 
                                 analyses: List[LLMOutputAnalysis]) -> QualityMetrics:
        """Calculate overall quality metrics"""
        
        total_stations = len(validations)
        passed = len([v for v in validations if v.status == "PASS"])
        failed = len([v for v in validations if v.status == "FAIL"])
        warnings = len([v for v in validations if v.status == "WARNING"])
        
        # Overall quality score (average of station quality scores)
        overall_quality = sum(v.quality_score for v in validations) / len(validations) if validations else 0.0
        
        # Pipeline integrity (all stations pass or have warnings only)
        pipeline_integrity = failed == 0
        
        # Creative uniqueness (average originality scores)
        creative_uniqueness = sum(a.originality_score for a in analyses) / len(analyses) if analyses else 0.0
        
        # Technical completeness (based on required fields completion)
        technical_completeness = sum(
            1.0 - (len(v.missing_outputs) / len(v.expected_outputs)) 
            for v in validations
        ) / len(validations) if validations else 0.0
        
        return QualityMetrics(
            total_stations_validated=total_stations,
            stations_passed=passed,
            stations_failed=failed,
            stations_with_warnings=warnings,
            overall_quality_score=overall_quality,
            pipeline_integrity=pipeline_integrity,
            creative_uniqueness_score=creative_uniqueness,
            technical_completeness_score=technical_completeness
        )

    async def _generate_executive_summary(self, validations: List[StationValidation], 
                                        metrics: QualityMetrics) -> str:
        """Generate executive summary using LLM"""
        
        # Prepare context for LLM
        context = {
            "total_stations": metrics.total_stations_validated,
            "passed": metrics.stations_passed,
            "failed": metrics.stations_failed,
            "warnings": metrics.stations_with_warnings,
            "overall_quality": f"{metrics.overall_quality_score:.1%}",
            "pipeline_integrity": metrics.pipeline_integrity,
            "critical_issues": [v.issues for v in validations if v.status == "FAIL"]
        }
        
        prompt = f"""
        Generate a concise executive summary for an audiobook production pipeline quality assessment.
        
        Results: {metrics.stations_passed}/{metrics.total_stations_validated} stations passed
        Overall Quality: {metrics.overall_quality_score:.1%}
        Pipeline Integrity: {'✅ INTACT' if metrics.pipeline_integrity else '❌ COMPROMISED'}
        
        Critical Issues: {sum(len(v.issues) for v in validations if v.status == 'FAIL')}
        
        Provide a 3-4 sentence summary focusing on:
        1. Overall pipeline status
        2. Key concerns or successes
        3. Readiness for production
        
        Be direct and actionable.
        """
        
        try:
            response = await self.openrouter_agent.process_message(
                prompt, 
                model_name=self.config.model
            )
            return response.strip()
        except Exception as e:
            logger.warning(f"Failed to generate LLM summary: {e}")
            return f"Pipeline Status: {metrics.stations_passed}/{metrics.total_stations_validated} stations passed. " \
                   f"Overall quality: {metrics.overall_quality_score:.1%}. " \
                   f"Pipeline integrity: {'INTACT' if metrics.pipeline_integrity else 'COMPROMISED'}."

    def _determine_pipeline_status(self, metrics: QualityMetrics) -> str:
        """Determine overall pipeline status"""
        
        if metrics.stations_failed > 0:
            return "FAILED"
        elif metrics.stations_with_warnings > 0:
            return "NEEDS_ATTENTION"
        else:
            return "PASSED"

    async def _validate_generated_files(self, session_id: str) -> List[str]:
        """Validate that expected files were generated"""
        
        expected_files = [
            f"outputs/station4_seedbank_{session_id}.pdf",
            f"outputs/station45_narrator_strategy_{session_id}.pdf",
            f"outputs/station5_season_architecture_{session_id}.txt",
            f"outputs/station5_season_data_{session_id}.json",
            f"outputs/station5_season_architecture_{session_id}.pdf",
            f"outputs/station6_master_style_guide_{session_id}.txt",
            f"outputs/station6_master_style_guide_{session_id}.json",
            f"outputs/station6_master_style_guide_{session_id}.pdf",
            f"outputs/automation_summary_{session_id}.json"
        ]
        
        validated_files = []
        for file_path in expected_files:
            if os.path.exists(file_path):
                validated_files.append(f"✅ {file_path}")
            else:
                validated_files.append(f"❌ {file_path}")
        
        return validated_files

    def _identify_critical_issues(self, validations: List[StationValidation]) -> List[str]:
        """Identify critical issues that must be addressed"""
        
        critical_issues = []
        
        for validation in validations:
            if validation.status == "FAIL":
                critical_issues.extend([
                    f"Station {validation.station_number} ({validation.station_name}): {issue}"
                    for issue in validation.issues
                ])
        
        return critical_issues

    # Utility methods for scoring and analysis
    def _get_field_count(self, field_value: Any) -> int:
        """Get count of items in a field"""
        if isinstance(field_value, list):
            return len(field_value)
        elif isinstance(field_value, dict):
            return len(field_value)
        elif isinstance(field_value, (int, float)):
            return int(field_value)
        else:
            return 1 if field_value else 0

    def _meets_count_requirement(self, actual: int, expected) -> bool:
        """Check if actual count meets expected requirement"""
        # Handle both string and integer expected values
        if isinstance(expected, int):
            return actual == expected
        
        expected_str = str(expected)
        if expected_str.startswith(">="):
            return actual >= int(expected_str[2:])
        elif expected_str.startswith("<="):
            return actual <= int(expected_str[2:])
        elif expected_str.startswith("="):
            return actual == int(expected_str[1:])
        else:
            return actual == int(expected_str)

    def _calculate_station_quality_score(self, missing_outputs: List[str], 
                                       count_issues: List[str], 
                                       fallback_detection: Dict[str, bool]) -> float:
        """Calculate quality score for a station"""
        
        score = 1.0
        
        # Penalize missing outputs
        if missing_outputs:
            score -= 0.3 * len(missing_outputs) / 10  # Max 30% penalty
        
        # Penalize count issues
        if count_issues:
            score -= 0.2 * len(count_issues) / 5  # Max 20% penalty
        
        # Penalize fallback content
        fallback_penalty = sum(0.1 for detected in fallback_detection.values() if detected)
        score -= min(fallback_penalty, 0.5)  # Max 50% penalty
        
        return max(0.0, score)

    def _count_unique_phrases(self, text: str) -> Set[str]:
        """Count unique phrases in text"""
        # Split into phrases (sentences or clauses)
        phrases = re.split(r'[.!?;,]', text)
        return set(phrase.strip().lower() for phrase in phrases if len(phrase.strip()) > 10)

    def _find_creativity_indicators(self, text: str) -> List[str]:
        """Find indicators of creative, original content"""
        indicators = []
        
        # Look for specific, detailed descriptions
        if re.search(r'\b\d{1,2}-year-old\b|\bspecific\w+\b|\bunique\w+\b', text):
            indicators.append("Specific age targeting")
        
        # Look for original character names or locations
        if re.search(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', text):
            indicators.append("Custom names/locations")
        
        # Look for technical details
        if re.search(r'\d+\s*episodes?|\d+\s*minutes?|\d+\s*words?', text):
            indicators.append("Specific technical parameters")
        
        return indicators

    def _find_generic_patterns(self, text: str) -> List[str]:
        """Find generic AI output patterns"""
        found_patterns = []
        
        for pattern in self.generic_patterns:
            if pattern.lower() in text.lower():
                found_patterns.append(pattern)
        
        return found_patterns

    def _find_hardcoded_examples(self, text: str) -> List[str]:
        """Find hardcoded examples or placeholders"""
        found_examples = []
        
        for indicator in self.fallback_indicators:
            if indicator.lower() in text.lower():
                found_examples.append(indicator)
        
        return found_examples

    def _find_ai_fingerprints(self, text: str) -> List[str]:
        """Find common AI-generated text fingerprints"""
        fingerprints = []
        
        # Common AI phrases
        ai_phrases = [
            "It's worth noting", "This approach", "In this context",
            "This strategy", "This method", "These elements"
        ]
        
        for phrase in ai_phrases:
            if phrase.lower() in text.lower():
                fingerprints.append(phrase)
        
        return fingerprints

    def _calculate_originality_score(self, unique_phrases: Set[str], 
                                   generic_patterns: List[str], 
                                   hardcoded_examples: List[str]) -> float:
        """Calculate originality score"""
        
        base_score = 1.0
        
        # Penalize generic patterns
        generic_penalty = min(len(generic_patterns) * 0.1, 0.5)
        base_score -= generic_penalty
        
        # Penalize hardcoded content
        hardcoded_penalty = min(len(hardcoded_examples) * 0.2, 0.6)
        base_score -= hardcoded_penalty
        
        # Reward unique content
        if len(unique_phrases) > 10:
            base_score += 0.1
        
        return max(0.0, min(1.0, base_score))

    async def _calculate_coherence_score(self, text: str) -> float:
        """Calculate coherence score using simple heuristics"""
        
        # Simple coherence indicators
        score = 0.5  # Base score
        
        # Check for proper sentence structure
        sentences = text.split('.')
        if len(sentences) > 3:
            score += 0.2
        
        # Check for consistent tense
        # (This is a simplified check)
        if len(text) > 100:
            score += 0.2
        
        # Check for logical flow (presence of connecting words)
        connecting_words = ["because", "therefore", "however", "additionally", "furthermore"]
        if any(word in text.lower() for word in connecting_words):
            score += 0.1
        
        return min(1.0, score)

    def _generate_station_recommendations(self, station_num: str, missing_outputs: List[str], 
                                        count_issues: List[str], 
                                        fallback_detection: Dict[str, bool]) -> List[str]:
        """Generate recommendations for a station"""
        
        recommendations = []
        
        if missing_outputs:
            recommendations.append(f"Re-run Station {station_num} to generate missing outputs: {', '.join(missing_outputs)}")
        
        if count_issues:
            recommendations.append(f"Review count requirements for Station {station_num}")
        
        if any(fallback_detection.values()):
            recommendations.append(f"Station {station_num} contains placeholder/fallback content - needs regeneration")
        
        return recommendations

    async def _generate_detailed_report(self, validations: List[StationValidation], 
                                      analyses: List[LLMOutputAnalysis]) -> str:
        """Generate detailed quality report"""
        
        report_sections = []
        
        # Header
        report_sections.append("AUDIOBOOK PRODUCTION PIPELINE - DETAILED QUALITY REPORT")
        report_sections.append("=" * 60)
        report_sections.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_sections.append("")
        
        # Station-by-station analysis
        for validation in validations:
            report_sections.append(f"STATION {validation.station_number}: {validation.station_name}")
            report_sections.append("-" * 40)
            report_sections.append(f"Status: {validation.status}")
            report_sections.append(f"Quality Score: {validation.quality_score:.1%}")
            
            if validation.missing_outputs:
                report_sections.append(f"Missing Outputs: {', '.join(validation.missing_outputs)}")
            
            if validation.issues:
                report_sections.append("Issues:")
                for issue in validation.issues:
                    report_sections.append(f"  • {issue}")
            
            if validation.recommendations:
                report_sections.append("Recommendations:")
                for rec in validation.recommendations:
                    report_sections.append(f"  • {rec}")
            
            report_sections.append("")
        
        # LLM Analysis Summary
        if analyses:
            report_sections.append("LLM OUTPUT ANALYSIS")
            report_sections.append("-" * 40)
            
            total_originality = sum(a.originality_score for a in analyses) / len(analyses)
            total_coherence = sum(a.coherence_score for a in analyses) / len(analyses)
            
            report_sections.append(f"Average Originality Score: {total_originality:.1%}")
            report_sections.append(f"Average Coherence Score: {total_coherence:.1%}")
            report_sections.append("")
            
            for analysis in analyses:
                report_sections.append(f"Station {analysis.station}:")
                report_sections.append(f"  Content Length: {analysis.total_text_length:,} characters")
                report_sections.append(f"  Originality: {analysis.originality_score:.1%}")
                report_sections.append(f"  Coherence: {analysis.coherence_score:.1%}")
                
                if analysis.generic_patterns_found:
                    report_sections.append(f"  Generic Patterns: {len(analysis.generic_patterns_found)}")
                
                if analysis.hardcoded_examples_detected:
                    report_sections.append(f"  Hardcoded Content: {len(analysis.hardcoded_examples_detected)}")
                
                report_sections.append("")
        
        return "\n".join(report_sections)

    async def _generate_recommendations(self, validations: List[StationValidation], 
                                      metrics: QualityMetrics) -> List[str]:
        """Generate overall recommendations"""
        
        recommendations = []
        
        # High-level recommendations
        if metrics.pipeline_integrity:
            recommendations.append("✅ Pipeline integrity is maintained - ready for production consideration")
        else:
            recommendations.append("❌ Pipeline integrity compromised - requires attention before production")
        
        # Quality-based recommendations
        if metrics.overall_quality_score >= 0.9:
            recommendations.append("🎯 Excellent quality standards achieved")
        elif metrics.overall_quality_score >= 0.7:
            recommendations.append("⚠️ Good quality but room for improvement")
        else:
            recommendations.append("🔧 Quality below acceptable standards - significant rework needed")
        
        # Specific station recommendations
        failed_stations = [v for v in validations if v.status == "FAIL"]
        if failed_stations:
            station_nums = [v.station_number for v in failed_stations]
            recommendations.append(f"🚨 Priority: Re-run failed stations: {', '.join(station_nums)}")
        
        # Creative recommendations
        if metrics.creative_uniqueness_score < 0.6:
            recommendations.append("🎨 Consider regenerating content with more specific prompts for originality")
        
        return recommendations

    def export_to_text(self, result: Station07Output) -> str:
        """Export validation results to text format"""
        
        sections = []
        
        # Header
        sections.append("STATION 7: REALITY CHECK REPORT")
        sections.append("=" * 60)
        sections.append(f"Session ID: {result.session_id}")
        sections.append(f"Validation Time: {result.validation_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        sections.append(f"Pipeline Status: {result.pipeline_status}")
        sections.append("")
        
        # Executive Summary
        sections.append("EXECUTIVE SUMMARY")
        sections.append("-" * 30)
        sections.append(result.executive_summary)
        sections.append("")
        
        # Quality Metrics
        sections.append("QUALITY METRICS")
        sections.append("-" * 30)
        sections.append(f"Overall Quality Score: {result.quality_metrics.overall_quality_score:.1%}")
        sections.append(f"Pipeline Integrity: {'✅ INTACT' if result.quality_metrics.pipeline_integrity else '❌ COMPROMISED'}")
        sections.append(f"Creative Uniqueness: {result.quality_metrics.creative_uniqueness_score:.1%}")
        sections.append(f"Technical Completeness: {result.quality_metrics.technical_completeness_score:.1%}")
        sections.append("")
        sections.append(f"Stations Passed: {result.quality_metrics.stations_passed}/{result.quality_metrics.total_stations_validated}")
        sections.append(f"Stations Failed: {result.quality_metrics.stations_failed}")
        sections.append(f"Stations with Warnings: {result.quality_metrics.stations_with_warnings}")
        sections.append("")
        
        # Critical Issues
        if result.critical_issues:
            sections.append("CRITICAL ISSUES")
            sections.append("-" * 30)
            for issue in result.critical_issues:
                sections.append(f"🚨 {issue}")
            sections.append("")
        
        # Recommendations
        sections.append("RECOMMENDATIONS")
        sections.append("-" * 30)
        for rec in result.recommendations:
            sections.append(f"💡 {rec}")
        sections.append("")
        
        # Station Details
        sections.append("STATION VALIDATION DETAILS")
        sections.append("-" * 30)
        
        for validation in result.station_validations:
            status_icon = "✅" if validation.status == "PASS" else "⚠️" if validation.status == "WARNING" else "❌"
            sections.append(f"{status_icon} Station {validation.station_number}: {validation.station_name}")
            sections.append(f"   Quality Score: {validation.quality_score:.1%}")
            
            if validation.issues:
                sections.append("   Issues:")
                for issue in validation.issues:
                    sections.append(f"     • {issue}")
            
            sections.append("")
        
        # File Validation
        sections.append("FILE VALIDATION")
        sections.append("-" * 30)
        for file_status in result.files_validated:
            sections.append(file_status)
        sections.append("")
        
        # Detailed Report
        sections.append("DETAILED ANALYSIS")
        sections.append("-" * 30)
        sections.append(result.detailed_report)
        
        return "\n".join(sections)

    def export_to_json(self, result: Station07Output) -> Dict[str, Any]:
        """Export validation results to JSON format"""
        
        return {
            "session_id": result.session_id,
            "validation_timestamp": result.validation_timestamp.isoformat(),
            "pipeline_status": result.pipeline_status,
            "quality_metrics": asdict(result.quality_metrics),
            "executive_summary": result.executive_summary,
            "recommendations": result.recommendations,
            "critical_issues": result.critical_issues,
            "station_validations": [asdict(v) for v in result.station_validations],
            "llm_analyses": [asdict(a) for a in result.llm_analyses],
            "files_validated": result.files_validated,
            "detailed_report": result.detailed_report
        }

    # PDF export removed - use JSON and TXT formats instead
    # def export_to_pdf(self, result: Station07Output) -> bytes:
    #     """Export validation results to PDF format - REMOVED"""
    #     pass


# CLI interface for testing
async def main():
    """Main CLI interface for Station 7"""
    
    print("🔍 STATION 7: REALITY CHECK")
    print("=" * 50)
    
    session_id = input("Enter session ID to validate: ").strip()
    if not session_id:
        print("❌ Session ID required")
        return
    
    try:
        station = Station07RealityCheck()
        await station.initialize()
        
        debug = input("Enable debug mode? (y/N): ").lower().strip() == 'y'
        if debug:
            station.enable_debug_mode()
        
        print(f"\n🔍 Starting validation for session: {session_id}")
        
        result = await station.process(session_id)
        
        print(f"\n{result.pipeline_status}")
        print("=" * 50)
        print(result.executive_summary)
        
        # Export results
        os.makedirs("outputs", exist_ok=True)
        
        # Text export
        text_filename = f"outputs/station7_reality_check_{session_id}.txt"
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(station.export_to_text(result))
        print(f"📄 Text report: {text_filename}")
        
        # JSON export
        json_filename = f"outputs/station7_reality_check_{session_id}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(station.export_to_json(result), f, indent=2, default=str)
        print(f"📊 JSON data: {json_filename}")
        
        # PDF export
        try:
            pdf_data = station.export_to_pdf(result)
            pdf_filename = f"outputs/station7_reality_check_{session_id}.pdf"
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_data)
            print(f"📑 PDF report: {pdf_filename}")
        except Exception as e:
            print(f"⚠️ PDF export failed: {e}")
        
        # Show critical issues
        if result.critical_issues:
            print("\n🚨 CRITICAL ISSUES:")
            for issue in result.critical_issues:
                print(f"   • {issue}")
        
        # Show recommendations
        if result.recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"   • {rec}")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())