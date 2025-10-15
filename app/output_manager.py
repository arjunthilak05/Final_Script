"""
Centralized Output Manager
Manages organized folder structure for all station outputs.
Creates one folder per run with all .txt and .json files from stations 1-20.
"""

import os
from datetime import datetime
from typing import Optional
from pathlib import Path


class OutputManager:
    """Manages organized output folder structure for automation runs"""

    def __init__(self, session_id: str, base_dir: str = "outputs"):
        """
        Initialize output manager for a session

        Args:
            session_id: Unique session identifier (e.g., auto_20251014_123456)
            base_dir: Base directory for all outputs (default: outputs)
        """
        self.session_id = session_id
        self.base_dir = base_dir
        self.session_folder = os.path.join(base_dir, session_id)

        # Create session folder structure
        self._create_folder_structure()

    def _create_folder_structure(self):
        """Create organized folder structure for the session"""
        os.makedirs(self.session_folder, exist_ok=True)
        print(f"📁 Created session folder: {self.session_folder}")

    def get_station_filepath(self, station_number: str, filename: str) -> str:
        """
        Get the full filepath for a station output file

        Args:
            station_number: Station number (e.g., "01", "4.5", "12")
            filename: Base filename (e.g., "seed_analysis.txt")

        Returns:
            Full filepath for the station output
        """
        filepath = os.path.join(self.session_folder, filename)
        return filepath

    def get_txt_path(self, station_number: str, description: str) -> str:
        """
        Get standardized .txt file path for a station

        Args:
            station_number: Station number (e.g., "01", "05", "12")
            description: Description of the file (e.g., "seed_processor", "season_architecture")

        Returns:
            Full path to .txt file
        """
        filename = f"station{station_number}_{description}_{self.session_id}.txt"
        return os.path.join(self.session_folder, filename)

    def get_json_path(self, station_number: str, description: str) -> str:
        """
        Get standardized .json file path for a station

        Args:
            station_number: Station number (e.g., "01", "05", "12")
            description: Description of the file (e.g., "seed_data", "season_data")

        Returns:
            Full path to .json file
        """
        filename = f"station{station_number}_{description}_{self.session_id}.json"
        return os.path.join(self.session_folder, filename)

    def save_text_file(self, station_number: str, description: str, content: str) -> str:
        """
        Save text content to a .txt file

        Args:
            station_number: Station number
            description: File description
            content: Text content to save

        Returns:
            Path to saved file
        """
        filepath = self.get_txt_path(station_number, description)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    def save_json_file(self, station_number: str, description: str, content: str) -> str:
        """
        Save JSON content to a .json file

        Args:
            station_number: Station number
            description: File description
            content: JSON content to save (as string)

        Returns:
            Path to saved file
        """
        filepath = self.get_json_path(station_number, description)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    def get_session_summary_path(self) -> str:
        """Get path for session summary file"""
        return os.path.join(self.session_folder, f"automation_summary_{self.session_id}.json")

    def get_checkpoint_path(self) -> str:
        """Get path for checkpoint file"""
        return os.path.join(self.session_folder, f"checkpoint_{self.session_id}.json")

    def list_session_files(self) -> list:
        """List all files in the session folder"""
        if not os.path.exists(self.session_folder):
            return []
        return sorted(os.listdir(self.session_folder))

    def get_session_folder(self) -> str:
        """Get the session folder path"""
        return self.session_folder

    @staticmethod
    def get_legacy_txt_path(station_number: str, description: str, session_id: str) -> str:
        """
        Get legacy .txt file path (for backward compatibility)
        This is used for stations that were saving directly to outputs/ folder

        Args:
            station_number: Station number
            description: File description
            session_id: Session ID

        Returns:
            Legacy path format
        """
        filename = f"station{station_number}_{description}_{session_id}.txt"
        return os.path.join("outputs", filename)

    @staticmethod
    def get_legacy_json_path(station_number: str, description: str, session_id: str) -> str:
        """
        Get legacy .json file path (for backward compatibility)

        Args:
            station_number: Station number
            description: File description
            session_id: Session ID

        Returns:
            Legacy path format
        """
        filename = f"station{station_number}_{description}_{session_id}.json"
        return os.path.join("outputs", filename)
