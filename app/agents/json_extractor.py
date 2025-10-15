"""
Shared JSON Extraction Utility for All Stations

This module provides a unified way to extract and parse JSON from LLM responses.
With high-quality LLMs, we can trust structured output and simplify parsing.
"""

import json
import re
import logging
from typing import Optional, TypeVar, Type, Dict, Any

logger = logging.getLogger(__name__)

T = TypeVar('T')


class JSONExtractor:
    """
    Utility for extracting JSON from LLM responses.

    High-quality LLMs should return JSON reliably, so we use simple strategies:
    1. Look for JSON in markdown code blocks
    2. Look for raw JSON objects
    3. Fail fast if not found (let retry logic handle it)
    """

    @staticmethod
    def extract_json_string(response: str) -> str:
        """
        Extract JSON string from LLM response.

        Args:
            response: Raw LLM response text

        Returns:
            str: Extracted JSON string

        Raises:
            ValueError: If no JSON found in response
        """
        if not response or not response.strip():
            raise ValueError("Empty response from LLM")

        # Strategy 1: JSON in markdown code block (```json ... ```)
        code_block_match = re.search(
            r'```json\s*(\{.*?\})\s*```',
            response,
            re.DOTALL | re.IGNORECASE
        )
        if code_block_match:
            logger.debug("Found JSON in markdown code block")
            return code_block_match.group(1)

        # Strategy 2: JSON in generic code block (``` ... ```)
        generic_block_match = re.search(
            r'```\s*(\{.*?\})\s*```',
            response,
            re.DOTALL
        )
        if generic_block_match:
            logger.debug("Found JSON in generic code block")
            return generic_block_match.group(1)

        # Strategy 3: Direct JSON object (no code block)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            logger.debug("Found raw JSON object")
            return json_match.group(0)

        # No JSON found
        logger.error(f"No JSON found in response (preview): {response[:200]}")
        raise ValueError("No JSON found in LLM response")

    @staticmethod
    def sanitize_json(json_string: str) -> str:
        """
        Sanitize common JSON errors from LLM responses.

        Fixes:
        - Trailing commas in arrays and objects
        - Missing commas between array elements
        - Unclosed strings (attempts basic repair)

        Args:
            json_string: Potentially malformed JSON string

        Returns:
            str: Sanitized JSON string
        """
        # Fix trailing commas in arrays: ,] -> ]
        json_string = re.sub(r',\s*]', ']', json_string)

        # Fix trailing commas in objects: ,} -> }
        json_string = re.sub(r',\s*}', '}', json_string)

        # Fix missing commas between objects in arrays (common LLM error)
        # Pattern: }\n    { -> },\n    {
        json_string = re.sub(r'}\s*\n\s*{', '},\n    {', json_string)

        # Fix missing commas between string values
        # Pattern: "value"\n    " -> "value",\n    "
        json_string = re.sub(r'"\s*\n\s*"', '",\n    "', json_string)

        return json_string

    @staticmethod
    def parse_json(json_string: str) -> Dict[str, Any]:
        """
        Parse JSON string to dictionary with automatic sanitization.

        Args:
            json_string: JSON string to parse

        Returns:
            Dict: Parsed JSON data

        Raises:
            ValueError: If JSON parsing fails even after sanitization
        """
        try:
            # Try parsing directly first
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            logger.warning(f"Initial JSON parsing failed: {str(e)}")
            logger.warning("Attempting to sanitize JSON...")

            try:
                # Try sanitizing and parsing again
                sanitized = JSONExtractor.sanitize_json(json_string)
                result = json.loads(sanitized)
                logger.info("✅ Successfully parsed JSON after sanitization")
                return result
            except json.JSONDecodeError as e2:
                logger.error(f"JSON parsing failed even after sanitization: {str(e2)}")
                logger.error(f"Problematic JSON (first 500 chars): {json_string[:500]}")
                logger.error(f"Sanitized JSON (first 500 chars): {sanitized[:500] if 'sanitized' in locals() else 'N/A'}")
                raise ValueError(f"Invalid JSON from LLM: {str(e2)}")

    @staticmethod
    def extract_and_parse(response: str) -> Dict[str, Any]:
        """
        Extract and parse JSON in one step.

        Args:
            response: Raw LLM response text

        Returns:
            Dict: Parsed JSON data

        Raises:
            ValueError: If extraction or parsing fails
        """
        json_string = JSONExtractor.extract_json_string(response)
        return JSONExtractor.parse_json(json_string)

    @staticmethod
    def parse_to_dict_with_defaults(
        response: str,
        required_keys: list[str],
        defaults: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Parse JSON and validate required keys.

        Args:
            response: Raw LLM response text
            required_keys: List of keys that must be present
            defaults: Optional default values for missing keys

        Returns:
            Dict: Parsed and validated JSON data

        Raises:
            ValueError: If required keys are missing and no defaults provided
        """
        data = JSONExtractor.extract_and_parse(response)

        # Check for required keys
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            if defaults:
                # Fill in defaults for missing keys
                for key in missing_keys:
                    if key in defaults:
                        data[key] = defaults[key]
                        logger.warning(f"Using default value for missing key: {key}")
                    else:
                        raise ValueError(f"Required key '{key}' missing and no default provided")
            else:
                raise ValueError(f"Required keys missing from LLM response: {missing_keys}")

        return data


class JSONValidator:
    """Validate JSON structure for station outputs"""

    @staticmethod
    def validate_structure(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
        """
        Validate that data matches expected schema.

        Args:
            data: Parsed JSON data
            schema: Expected schema (field_name -> expected_type)

        Returns:
            bool: True if valid

        Raises:
            ValueError: If validation fails
        """
        for field, expected_type in schema.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

            actual_type = type(data[field])
            if not isinstance(data[field], expected_type):
                raise ValueError(
                    f"Field '{field}' has wrong type. "
                    f"Expected {expected_type.__name__}, got {actual_type.__name__}"
                )

        return True

    @staticmethod
    def validate_list_length(
        data: Dict[str, Any],
        list_field: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> bool:
        """
        Validate list field length.

        Args:
            data: Parsed JSON data
            list_field: Name of list field to validate
            min_length: Minimum required length
            max_length: Maximum allowed length

        Returns:
            bool: True if valid

        Raises:
            ValueError: If validation fails
        """
        if list_field not in data:
            raise ValueError(f"List field '{list_field}' not found")

        if not isinstance(data[list_field], list):
            raise ValueError(f"Field '{list_field}' is not a list")

        length = len(data[list_field])

        if min_length is not None and length < min_length:
            raise ValueError(
                f"List '{list_field}' too short. "
                f"Expected at least {min_length}, got {length}"
            )

        if max_length is not None and length > max_length:
            raise ValueError(
                f"List '{list_field}' too long. "
                f"Expected at most {max_length}, got {length}"
            )

        return True


# Convenience function for common use case
def extract_json(response: str) -> Dict[str, Any]:
    """
    Convenience function for extracting and parsing JSON.

    Args:
        response: Raw LLM response text

    Returns:
        Dict: Parsed JSON data
    """
    return JSONExtractor.extract_and_parse(response)
