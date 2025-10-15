"""
Template for Enhancement Station Type

Enhancement stations improve or enrich existing content.

Examples:
- Dialogue polishing
- Description enhancement
- Emotional depth addition
- Style refinement
"""

TEMPLATE_DESCRIPTION = "Improves or enriches existing content"

TEMPLATE_PROMPT = """
You are enhancing {content_type} to improve quality and impact.

ORIGINAL CONTENT:
{original_content}

ENHANCEMENT GOALS:
{enhancement_goals}

ENHANCEMENT TASKS:
1. Analyze the original content
2. Identify areas for improvement
3. Apply enhancements while preserving intent
4. Ensure consistency with style guidelines

OUTPUT FORMAT:
Provide enhanced content with:
- Enhanced Version (improved content)
- Changes Made (what was improved)
- Before/After Comparison (key differences)
- Quality Improvement Score (1-10)
"""

TEMPLATE_OUTPUT = {
    "enhanced_version": "The improved content",
    "changes_made": [
        "Changed element 1: description",
        "Changed element 2: description"
    ],
    "before_after": {
        "before": "Original version excerpt",
        "after": "Enhanced version excerpt",
        "improvement": "What was improved"
    },
    "quality_improvement_score": 8,
    "notes": "Additional notes about enhancements"
}
