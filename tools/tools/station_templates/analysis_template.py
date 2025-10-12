"""
Template for Analysis Station Type

Analysis stations examine existing data and provide insights, validations,
or quality assessments.

Examples:
- Quality checks
- Consistency analysis
- Feasibility validation
- Sentiment analysis
"""

TEMPLATE_DESCRIPTION = "Analyzes existing data and provides insights"

TEMPLATE_PROMPT = """
You are analyzing {data_type} for quality and insights.

INPUT DATA:
{input_data}

ANALYSIS TASKS:
1. Examine the data for quality issues
2. Check for consistency and coherence
3. Identify strengths and weaknesses
4. Provide actionable recommendations

OUTPUT FORMAT:
Provide a structured analysis with:
- Quality Score (1-10)
- Identified Issues (list)
- Strengths (list)
- Recommendations (list)
- Overall Assessment (summary)
"""

TEMPLATE_OUTPUT = {
    "quality_score": 8,
    "issues": [
        "Issue 1 description",
        "Issue 2 description"
    ],
    "strengths": [
        "Strength 1",
        "Strength 2"
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ],
    "overall_assessment": "Summary of the analysis"
}
