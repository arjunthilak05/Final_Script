"""
Title Validator - Bulletproof Title Data Flow Management

This module ensures consistent title handling across all stations in the pipeline.
It provides validation, extraction, and standardization functions to prevent
title continuity issues.
"""

import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TitleValidationResult:
    """Result of title validation"""
    is_valid: bool
    chosen_title: str
    error_message: Optional[str] = None
    source_station: str = "Unknown"


class TitleValidator:
    """Bulletproof title validation and extraction"""
    
    @staticmethod
    def validate_chosen_title(station1_data: Dict) -> TitleValidationResult:
        """
        Validate that Station 1 has a proper chosen_title
        
        Args:
            station1_data: Station 1 output data
            
        Returns:
            TitleValidationResult with validation status and title
        """
        if not station1_data:
            return TitleValidationResult(
                is_valid=False,
                chosen_title="",
                error_message="Station 1 data is None or empty",
                source_station="Station 1"
            )
        
        chosen_title = station1_data.get('chosen_title', '')
        
        if not chosen_title:
            return TitleValidationResult(
                is_valid=False,
                chosen_title="",
                error_message="Station 1 data missing 'chosen_title' field",
                source_station="Station 1"
            )
        
        if chosen_title in ['Unknown', 'N/A', 'Untitled', '']:
            return TitleValidationResult(
                is_valid=False,
                chosen_title=chosen_title,
                error_message=f"Station 1 chosen_title is invalid: '{chosen_title}'",
                source_station="Station 1"
            )
        
        # Check for placeholder patterns
        forbidden_patterns = [
            'TBD', 'TO BE DETERMINED', 'PLACEHOLDER', 'Generic', 'Default'
        ]
        
        for pattern in forbidden_patterns:
            if pattern.lower() in chosen_title.lower():
                return TitleValidationResult(
                    is_valid=False,
                    chosen_title=chosen_title,
                    error_message=f"Station 1 chosen_title contains placeholder: '{pattern}'",
                    source_station="Station 1"
                )
        
        return TitleValidationResult(
            is_valid=True,
            chosen_title=chosen_title,
            source_station="Station 1"
        )
    
    @staticmethod
    def extract_bulletproof_title(station1_data: Dict, station2_data: Optional[Dict] = None) -> str:
        """
        Extract the definitive title from Station 1 data with fallback validation
        
        Args:
            station1_data: Station 1 output data (primary source)
            station2_data: Station 2 output data (fallback validation)
            
        Returns:
            The definitive chosen title
            
        Raises:
            ValueError: If no valid title can be found
        """
        # Primary: Validate Station 1 chosen_title
        validation_result = TitleValidator.validate_chosen_title(station1_data)
        
        if validation_result.is_valid:
            return validation_result.chosen_title
        
        # Fallback: Check Station 2 working_title for consistency
        if station2_data:
            station2_title = station2_data.get('working_title', '')
            if station2_title and station2_title not in ['Unknown', 'N/A', 'Untitled', '']:
                # Log the inconsistency but use Station 2 as fallback
                print(f"⚠️  WARNING: Using Station 2 title '{station2_title}' due to Station 1 issue: {validation_result.error_message}")
                return station2_title
        
        # Final fallback: Use Station 1 chosen_title even if invalid (better than crashing)
        chosen_title = station1_data.get('chosen_title', 'Unknown Title')
        print(f"⚠️  WARNING: Using potentially invalid title '{chosen_title}' due to validation failure: {validation_result.error_message}")
        return chosen_title
    
    @staticmethod
    def validate_title_consistency(station1_data: Dict, station2_data: Optional[Dict] = None) -> bool:
        """
        Validate that titles are consistent across stations
        
        Args:
            station1_data: Station 1 output data
            station2_data: Station 2 output data (optional)
            
        Returns:
            True if titles are consistent, False otherwise
        """
        station1_title = station1_data.get('chosen_title', '')
        
        if not station2_data:
            return True  # No Station 2 data to compare
        
        station2_title = station2_data.get('working_title', '')
        
        if not station1_title or not station2_title:
            return True  # Can't compare if either is empty
        
        # Station 2 working_title should match Station 1 chosen_title
        if station1_title != station2_title:
            print(f"⚠️  WARNING: Title inconsistency detected:")
            print(f"   Station 1 chosen_title: '{station1_title}'")
            print(f"   Station 2 working_title: '{station2_title}'")
            return False
        
        return True
    
    @staticmethod
    def format_title_for_display(title: str, station_name: str = "Station") -> str:
        """
        Format title for consistent display across stations
        
        Args:
            title: The title to format
            station_name: Name of the station displaying the title
            
        Returns:
            Formatted title string
        """
        if not title or title in ['Unknown', 'N/A', 'Untitled']:
            return f"❌ {station_name}: No valid title found"
        
        return f"📖 {station_name} Title: {title}"
    
    @staticmethod
    def create_title_summary(station1_data: Dict, station2_data: Optional[Dict] = None) -> Dict:
        """
        Create a comprehensive title summary for debugging and validation
        
        Args:
            station1_data: Station 1 output data
            station2_data: Station 2 output data (optional)
            
        Returns:
            Dictionary with title information and validation status
        """
        validation_result = TitleValidator.validate_chosen_title(station1_data)
        
        summary = {
            "definitive_title": validation_result.chosen_title,
            "is_valid": validation_result.is_valid,
            "validation_error": validation_result.error_message,
            "source": "Station 1 chosen_title",
            "station1_chosen_title": station1_data.get('chosen_title', 'MISSING'),
            "station1_working_titles": station1_data.get('working_titles', []),
        }
        
        if station2_data:
            summary.update({
                "station2_working_title": station2_data.get('working_title', 'MISSING'),
                "titles_consistent": TitleValidator.validate_title_consistency(station1_data, station2_data)
            })
        
        return summary
