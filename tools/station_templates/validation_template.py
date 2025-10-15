"""
Template for Validation Station Type

Validation stations check correctness, feasibility, and compliance.

Examples:
- Fact checking
- Timeline validation
- Budget feasibility
- Technical accuracy
"""

TEMPLATE_DESCRIPTION = "Checks correctness and feasibility"

TEMPLATE_PROMPT = """
You are validating {validation_target} for correctness and feasibility.

CONTENT TO VALIDATE:
{content}

VALIDATION CRITERIA:
{criteria}

VALIDATION TASKS:
1. Check against validation criteria
2. Identify any errors or inconsistencies
3. Assess feasibility and practicality
4. Provide pass/fail determination with details

OUTPUT FORMAT:
Provide validation results with:
- Validation Status (pass/fail)
- Errors Found (list)
- Warnings (list)
- Feasibility Assessment (score 1-10)
- Recommendations for corrections
"""

TEMPLATE_OUTPUT = {
    "validation_status": "pass",
    "errors": [
        {"type": "error_type", "description": "Error description", "severity": "high"}
    ],
    "warnings": [
        {"type": "warning_type", "description": "Warning description", "severity": "medium"}
    ],
    "feasibility_score": 9,
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ],
    "overall_status": "Content is valid with minor warnings"
}
