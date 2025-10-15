"""
Template for Generation Station Type

Generation stations create new content based on inputs and requirements.

Examples:
- Dialogue generation
- Scene description creation
- Music cue suggestions
- Character backstory generation
"""

TEMPLATE_DESCRIPTION = "Creates new content based on inputs"

TEMPLATE_PROMPT = """
You are creating {content_type} based on the following requirements.

PROJECT CONTEXT:
{project_context}

SPECIFIC REQUIREMENTS:
{requirements}

GENERATION TASKS:
1. Understand the context and requirements
2. Generate creative, appropriate content
3. Ensure consistency with existing material
4. Provide multiple options if applicable

OUTPUT FORMAT:
Provide structured creative content with:
- Main Content (generated material)
- Alternatives (if applicable)
- Rationale (why this works)
- Usage Notes (how to apply this)
"""

TEMPLATE_OUTPUT = {
    "main_content": "The primary generated content",
    "alternatives": [
        "Alternative option 1",
        "Alternative option 2"
    ],
    "rationale": "Explanation of why this content works",
    "usage_notes": "Guidelines for using this content",
    "metadata": {
        "content_type": "dialogue",
        "style": "conversational",
        "tone": "dramatic"
    }
}
