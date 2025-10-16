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
        - Truncated JSON arrays (auto-closes)

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

        # FIX TRUNCATED JSON: If JSON ends abruptly, try to close it
        json_string = json_string.strip()

        # Count opening and closing braces/brackets
        open_braces = json_string.count('{')
        close_braces = json_string.count('}')
        open_brackets = json_string.count('[')
        close_brackets = json_string.count(']')

        # If truncated (more opens than closes), try to close gracefully
        if open_braces > close_braces or open_brackets > close_brackets:
            logger.warning("Detected truncated JSON, attempting to auto-close...")

            # Close any unclosed strings (basic attempt)
            if json_string.count('"') % 2 != 0:
                json_string += '"'

            # Handle incomplete objects/arrays more intelligently
            # Find the last incomplete structure and close it properly
            
            # If we're in the middle of an object or array, we need to close it properly
            # Look for incomplete patterns at the end
            lines = json_string.split('\n')
            last_line = lines[-1].strip()
            
            # If last line is incomplete (missing comma, incomplete string, etc.)
            if last_line and not last_line.endswith(('}', ']', '"', ',')):
                # Try to complete the last line if it looks like an incomplete field
                if ':' in last_line and not last_line.endswith(','):
                    # Looks like incomplete field, add default value
                    if '"' in last_line and last_line.count('"') % 2 == 1:
                        # Incomplete string, close it
                        json_string += '"'
                    json_string += ','

            # Close unclosed objects
            while open_braces > close_braces:
                json_string += '\n}'
                close_braces += 1

            # Close unclosed arrays
            while open_brackets > close_brackets:
                json_string += '\n]'
                close_brackets += 1

        # Fix missing commas between string values
        # Pattern: "value"\n    " -> "value",\n    "
        json_string = re.sub(r'"\s*\n\s*"', '",\n    "', json_string)

        return json_string

    @staticmethod
    def aggressive_truncation_recovery(json_string: str) -> str:
        """
        Aggressive recovery for severely truncated JSON.
        This method tries to salvage as much data as possible by:
        1. Finding the last complete object/array
        2. Truncating at that point
        3. Closing all open structures
        
        Args:
            json_string: Severely truncated JSON string
            
        Returns:
            str: Recovered JSON string
        """
        logger.warning("Attempting aggressive truncation recovery...")
        
        # Clean up any invalid control characters first
        import string
        printable = set(string.printable)
        cleaned_json = ''.join(char for char in json_string if char in printable or char.isspace())
        
        # Try to find the last complete object or array
        lines = cleaned_json.split('\n')
        recovered_lines = []
        
        brace_depth = 0
        bracket_depth = 0
        in_string = False
        escape_next = False
        
        for i, line in enumerate(lines):
            # Check if this line looks like it might be the truncation point
            if i == len(lines) - 1 and line.strip() and not line.strip().endswith(('}', ']', '"', ',')):
                # Last line and it's incomplete, skip it
                logger.info(f"Skipping incomplete last line: {line.strip()}")
                break
                
            recovered_lines.append(line)
            
            # Track depth and string state
            for char in line:
                if escape_next:
                    escape_next = False
                    continue
                    
                if char == '\\':
                    escape_next = True
                    continue
                    
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                    
                if not in_string:
                    if char == '{':
                        brace_depth += 1
                    elif char == '}':
                        brace_depth -= 1
                    elif char == '[':
                        bracket_depth += 1
                    elif char == ']':
                        bracket_depth -= 1
            
            # If we have a complete structure, this might be a good truncation point
            if brace_depth == 0 and bracket_depth == 0 and i > 0:
                # Found a complete structure, truncate here
                logger.info(f"Found complete structure at line {i+1}, truncating...")
                break
        
        # Rebuild the JSON
        recovered_json = '\n'.join(recovered_lines)
        
        # Close any remaining open structures
        while brace_depth > 0:
            recovered_json += '\n}'
            brace_depth -= 1
            
        while bracket_depth > 0:
            recovered_json += '\n]'
            bracket_depth -= 1
            
        # Fix any trailing commas
        recovered_json = re.sub(r',\s*([}\]])', r'\1', recovered_json)
        
        return recovered_json

    @staticmethod
    def emergency_fallback_recovery(json_string: str) -> Dict[str, Any]:
        """
        Emergency fallback recovery that tries to extract whatever data is possible.
        This is the last resort - it will return partial data rather than failing completely.
        
        Args:
            json_string: Severely malformed JSON string
            
        Returns:
            Dict: Whatever data could be extracted
        """
        logger.warning("Using emergency fallback recovery...")
        
        # Try to extract the root key if it exists
        import re
        
        # Look for common patterns in the JSON
        result = {}
        
        # Try to find the main array/object key
        main_key_match = re.search(r'"([^"]+)":\s*\[', json_string)
        if main_key_match:
            main_key = main_key_match.group(1)
            
            # Try to extract individual objects from the array
            objects = []
            
            # Find all complete objects in the array - try multiple patterns
            # First try: complete objects with proper nesting
            object_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
            object_matches = re.findall(object_pattern, json_string, re.DOTALL)
            
            # If no matches, try a more aggressive pattern
            if not object_matches:
                # Look for objects that might be incomplete but salvageable
                lines = json_string.split('\n')
                current_obj = ""
                brace_count = 0
                
                for line in lines:
                    if line.strip().startswith('{'):
                        current_obj = line
                        brace_count = line.count('{') - line.count('}')
                    elif brace_count > 0:
                        current_obj += '\n' + line
                        brace_count += line.count('{') - line.count('}')
                        if brace_count == 0:
                            object_matches.append(current_obj)
                            current_obj = ""
            
            for obj_str in object_matches:
                try:
                    obj = json.loads(obj_str)
                    objects.append(obj)
                except:
                    # If individual object fails, try to fix it
                    try:
                        # Try to close incomplete objects
                        fixed_obj = obj_str
                        if fixed_obj.count('{') > fixed_obj.count('}'):
                            fixed_obj += '}'
                        if fixed_obj.count('"') % 2 != 0:
                            fixed_obj += '"'
                        obj = json.loads(fixed_obj)
                        objects.append(obj)
                    except:
                        continue
            
            if objects:
                result[main_key] = objects
                logger.info(f"Emergency recovery extracted {len(objects)} items from {main_key}")
            else:
                # If no complete objects found, create a minimal structure
                result[main_key] = []
                logger.warning(f"Emergency recovery created empty {main_key} array")
        
        # If we couldn't extract anything, return a minimal structure
        if not result:
            logger.warning("Emergency recovery could not extract any data, returning minimal structure")
            result = {"error": "JSON parsing failed", "data": []}
        
        return result

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
                logger.warning(f"Sanitization failed: {str(e2)}")
                logger.warning("Attempting aggressive truncation recovery...")
                
                try:
                    # Try aggressive truncation recovery
                    recovered = JSONExtractor.aggressive_truncation_recovery(json_string)
                    result = json.loads(recovered)
                    logger.info("✅ Successfully parsed JSON after aggressive recovery")
                    return result
                except json.JSONDecodeError as e3:
                    logger.warning(f"All recovery attempts failed: {str(e3)}")
                    logger.warning("Attempting emergency fallback recovery...")
                    
                    try:
                        # Emergency fallback: try to extract whatever we can
                        fallback_result = JSONExtractor.emergency_fallback_recovery(json_string)
                        logger.info("✅ Successfully parsed JSON with emergency fallback")
                        return fallback_result
                    except Exception as e4:
                        logger.error(f"All JSON recovery attempts failed: {str(e4)}")
                        logger.error(f"Original JSON (first 500 chars): {json_string[:500]}")
                        logger.error(f"Sanitized JSON (first 500 chars): {sanitized[:500] if 'sanitized' in locals() else 'N/A'}")
                        logger.error(f"Recovered JSON (first 500 chars): {recovered[:500] if 'recovered' in locals() else 'N/A'}")
                        raise ValueError(f"Invalid JSON from LLM: {str(e4)}")

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
