"""
Robust Retry Mechanism with Validation

This module provides utilities for retrying LLM calls with validation
to ensure story fidelity and prevent fallback content generation.

NO FALLBACKS. NO PLACEHOLDERS. FAIL LOUDLY OR RETRY.
"""

import asyncio
import json
import re
import logging
from typing import Dict, Any, Callable, List, Optional, Set
from dataclasses import dataclass
from functools import wraps

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of content validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def __bool__(self):
        return self.is_valid


class ContentValidator:
    """
    Validates LLM output for story fidelity and placeholder detection

    This is the bulletproof validation system that ensures:
    1. No generic placeholders (TBD, Location 1, etc.)
    2. No fabricated characters/locations
    3. All required fields present
    4. Content is story-specific, not generic
    """

    # Forbidden placeholder patterns that indicate generic/fallback content
    FORBIDDEN_PATTERNS = [
        r'\bTBD\b',
        r'\bTO BE DETERMINED\b',
        r'\bPLACEHOLDER\b',
        r'\[[A-Z][a-z]+(?:\s+[a-z]+)*\]',  # [Character name], [Description], etc. but not JSON arrays
        r'Location\s+\d+',  # Location 1, Location 2, etc.
        r'Character\s+\d+',  # Character 1, Character 2
        r'System\s+\d+',  # System 1, System 2
        r'Place\s+[A-Z]\b',  # Place A, Place B
        r'Generic\s+\w+',
        r'Default\s+\w+',
        r'Untitled',
        r'Main Character\b(?!\s+\w)',  # "Main Character" without a name following
        r'Supporting Character\b(?!\s+\w)',
        r'\bUnknown\b',
        r'\bN/A\b',
        r'\bNone\b(?=\s*[,\}\]])',  # "None" as a value, not in prose
        r'Distinctive vocal quality',  # Generic Station 8 fallback
        r'Associated environment',  # Generic Station 8 fallback
        r'No specific',  # "No specific verbal tics defined"
        r'Not Found',  # "Name Not Found"
    ]

    # Required minimum lengths for various content types
    MIN_LENGTHS = {
        'name': 2,
        'description': 20,
        'summary': 30,
        'premise': 50,
        'character_description': 40,
        'location_description': 30,
    }

    @classmethod
    def validate_content(cls, content: Any, field_name: str = "content",
                        min_length: int = 10,
                        allow_empty: bool = False) -> ValidationResult:
        """
        Validate content for story fidelity

        Args:
            content: Content to validate (string, dict, or list)
            field_name: Name of the field for error messages
            min_length: Minimum length for string content
            allow_empty: Whether to allow empty content

        Returns:
            ValidationResult with validation status and errors
        """
        errors = []
        warnings = []

        # Handle None/empty
        if content is None or (isinstance(content, str) and not content.strip()):
            if not allow_empty:
                errors.append(f"{field_name}: Content is empty or None")
            return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

        # Convert to string for pattern checking
        content_str = json.dumps(content) if not isinstance(content, str) else content

        # Check for forbidden patterns
        for pattern in cls.FORBIDDEN_PATTERNS:
            matches = re.finditer(pattern, content_str, re.IGNORECASE)
            for match in matches:
                errors.append(
                    f"{field_name}: Contains forbidden placeholder/generic content: '{match.group()}'"
                )

        # Check minimum length for strings
        if isinstance(content, str):
            if len(content.strip()) < min_length:
                errors.append(
                    f"{field_name}: Content too short ({len(content.strip())} chars, minimum {min_length})"
                )

        # Validate dict fields recursively
        if isinstance(content, dict):
            for key, value in content.items():
                # Use context-aware min_length: shorter for names/identifiers (2), normal for descriptions (5)
                context_min_length = 2 if any(keyword in key.lower() for keyword in ['name', 'id', 'key', 'code']) else 5
                sub_result = cls.validate_content(value, f"{field_name}.{key}", min_length=context_min_length)
                errors.extend(sub_result.errors)
                warnings.extend(sub_result.warnings)

        # Validate list items
        if isinstance(content, list):
            if len(content) == 0 and not allow_empty:
                errors.append(f"{field_name}: List is empty")
            for i, item in enumerate(content):
                # Use shorter min_length for list items (words can be short)
                item_min_length = 2 if isinstance(item, str) else min_length
                sub_result = cls.validate_content(item, f"{field_name}[{i}]", min_length=item_min_length)
                errors.extend(sub_result.errors)
                warnings.extend(sub_result.warnings)

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    @classmethod
    def validate_required_fields(cls, data: Dict[str, Any],
                                 required_fields: List[str]) -> ValidationResult:
        """
        Validate that all required fields are present and non-empty

        Args:
            data: Dictionary to validate
            required_fields: List of required field names

        Returns:
            ValidationResult with validation status
        """
        errors = []
        warnings = []

        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                errors.append(f"Required field is empty: {field}")
            else:
                # Validate the field content
                result = cls.validate_content(data[field], field)
                errors.extend(result.errors)
                warnings.extend(result.warnings)

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    @classmethod
    def validate_character_names(cls, names: List[str]) -> ValidationResult:
        """
        Validate character names are specific and not generic

        Args:
            names: List of character names

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []

        if not names:
            errors.append("Character names list is empty")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        generic_patterns = [
            r'^Character\s*\d*$',
            r'^Main\s+Character$',
            r'^Supporting\s+Character$',
            r'^Protagonist$',
            r'^Antagonist$',
            r'^Hero$',
            r'^Villain$',
        ]

        for name in names:
            # Check if too short
            if len(name.strip()) < 2:
                errors.append(f"Character name too short: '{name}'")

            # Check for generic patterns
            for pattern in generic_patterns:
                if re.match(pattern, name.strip(), re.IGNORECASE):
                    errors.append(f"Generic character name detected: '{name}'")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    @classmethod
    def validate_location_names(cls, names: List[str]) -> ValidationResult:
        """
        Validate location names are specific and not generic

        Args:
            names: List of location names

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []

        if not names:
            errors.append("Location names list is empty")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        for name in names:
            # Check if too short
            if len(name.strip()) < 3:
                errors.append(f"Location name too short: '{name}'")

            # Check for generic patterns (Location 1, Place A, etc.)
            if re.match(r'^Location\s*\d+$', name.strip(), re.IGNORECASE):
                errors.append(f"Generic location name: '{name}'")
            if re.match(r'^Place\s*[A-Z]$', name.strip(), re.IGNORECASE):
                errors.append(f"Generic location name: '{name}'")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


class RetryConfig:
    """Configuration for retry mechanism"""

    def __init__(self,
                 max_attempts: int = 5,
                 initial_delay: float = 1.0,
                 exponential_backoff: bool = True,
                 backoff_multiplier: float = 2.0,
                 max_delay: float = 30.0,
                 log_attempts: bool = True):
        """
        Args:
            max_attempts: Maximum number of retry attempts
            initial_delay: Initial delay between retries in seconds
            exponential_backoff: Whether to use exponential backoff
            backoff_multiplier: Multiplier for exponential backoff
            max_delay: Maximum delay between retries
            log_attempts: Whether to log retry attempts
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.exponential_backoff = exponential_backoff
        self.backoff_multiplier = backoff_multiplier
        self.max_delay = max_delay
        self.log_attempts = log_attempts


async def retry_with_validation(
    func: Callable,
    validator: Callable[[Any], ValidationResult],
    config: Optional[RetryConfig] = None,
    context_name: str = "operation"
) -> Any:
    """
    Retry an async function until validation passes or max attempts reached

    This is the bulletproof retry mechanism that ensures:
    1. LLM is called repeatedly until it produces valid output
    2. No fallback content is ever used
    3. Clear error messages when validation fails
    4. Exponential backoff to handle rate limits

    Args:
        func: Async function to call (should return the content to validate)
        validator: Function that takes the result and returns ValidationResult
        config: Retry configuration (uses defaults if None)
        context_name: Name for logging context

    Returns:
        The validated result from func

    Raises:
        ValueError: If validation fails after all retry attempts
    """
    if config is None:
        config = RetryConfig()

    last_errors = []
    delay = config.initial_delay

    for attempt in range(1, config.max_attempts + 1):
        try:
            if config.log_attempts and attempt > 1:
                logger.info(f"{context_name}: Retry attempt {attempt}/{config.max_attempts}")

            # Call the function
            result = await func()

            # Validate the result
            validation = validator(result)

            if validation.is_valid:
                if config.log_attempts and attempt > 1:
                    logger.info(f"{context_name}: Validation passed on attempt {attempt}")
                return result

            # Validation failed
            last_errors = validation.errors
            if config.log_attempts:
                logger.warning(
                    f"{context_name}: Validation failed on attempt {attempt}/{config.max_attempts}. "
                    f"Errors: {'; '.join(validation.errors[:3])}"  # Log first 3 errors
                )

            # Wait before retry (except on last attempt)
            if attempt < config.max_attempts:
                await asyncio.sleep(delay)

                # Apply exponential backoff
                if config.exponential_backoff:
                    delay = min(delay * config.backoff_multiplier, config.max_delay)

        except json.JSONDecodeError as e:
            last_errors = [f"JSON parse error: {str(e)}"]
            if config.log_attempts:
                logger.warning(f"{context_name}: JSON parse error on attempt {attempt}, retrying...")

            if attempt < config.max_attempts:
                await asyncio.sleep(delay)
                if config.exponential_backoff:
                    delay = min(delay * config.backoff_multiplier, config.max_delay)

        except Exception as e:
            # Unexpected error - don't retry these
            logger.error(f"{context_name}: Unexpected error: {str(e)}")
            raise

    # All attempts exhausted
    error_summary = "\n".join(f"  - {err}" for err in last_errors[:10])  # Show first 10 errors
    raise ValueError(
        f"{context_name}: Validation failed after {config.max_attempts} attempts.\n"
        f"The LLM repeatedly produced invalid/generic content.\n"
        f"Validation errors:\n{error_summary}\n\n"
        f"This usually means:\n"
        f"1. The prompt needs to be more specific\n"
        f"2. The model is not following instructions\n"
        f"3. Input data is insufficient or ambiguous\n\n"
        f"NO FALLBACK CONTENT WAS USED. Fix the input or prompt and retry."
    )


def validate_and_raise(validation: ValidationResult, context: str = "Validation"):
    """
    Raise an exception if validation failed

    Args:
        validation: ValidationResult to check
        context: Context for error message

    Raises:
        ValueError: If validation failed
    """
    if not validation.is_valid:
        error_msg = f"{context} failed:\n" + "\n".join(f"  - {err}" for err in validation.errors)
        raise ValueError(error_msg)


# Decorator for automatic retry with validation
def with_retry_validation(
    validator: Callable[[Any], ValidationResult],
    config: Optional[RetryConfig] = None,
    context_name: str = None
):
    """
    Decorator to add retry-with-validation to an async function

    Usage:
        @with_retry_validation(my_validator, context_name="generate_characters")
        async def generate_characters(self, prompt: str):
            return await self.llm_call(prompt)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Use function name as context if not provided
            ctx_name = context_name or func.__name__

            # Create a wrapper function that calls the original
            async def call_func():
                return await func(*args, **kwargs)

            # Retry with validation
            return await retry_with_validation(
                call_func,
                validator,
                config,
                ctx_name
            )

        return wrapper
    return decorator
