"""
Claude AI Analyzer Module
Uses Anthropic's Claude API to analyze resumes and suggest improvements
"""

import anthropic
import os
from typing import Dict, Optional


class ClaudeAnalyzer:
    """Analyze resumes and job descriptions using Claude AI"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude analyzer

        Args:
            api_key: Anthropic API key (if not provided, uses ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def analyze_resume_for_job(
        self,
        resume_text: str,
        job_description: str,
        model: str = "claude-3-5-sonnet-20241022"
    ) -> Dict[str, any]:
        """
        Analyze resume against job description and provide recommendations

        Args:
            resume_text: Extracted resume text
            job_description: Job description text
            model: Claude model to use

        Returns:
            Dictionary containing analysis and recommendations
        """
        try:
            prompt = f"""You are an expert resume consultant. Analyze the following resume against the job description and provide detailed, actionable recommendations for tailoring the resume.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Please provide a comprehensive analysis with the following sections:

1. **MATCH ANALYSIS**: Assess how well the current resume matches the job requirements (give a percentage score and explain)

2. **KEY SKILLS GAP**: Identify important skills/qualifications from the JD that are missing or underemphasized in the resume

3. **RECOMMENDED ADDITIONS**: Specific content to add (e.g., relevant projects, skills, keywords)

4. **RECOMMENDED MODIFICATIONS**: Existing sections to modify or reframe to better align with the job

5. **KEYWORDS TO INCLUDE**: Important keywords from the JD that should appear in the resume for ATS optimization

6. **PRIORITY ACTIONS**: Top 3-5 most impactful changes to make, ranked by importance

Please be specific and actionable in your recommendations. Format your response in clear sections with markdown formatting."""

            message = self.client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the text content from the response
            recommendations = message.content[0].text

            return {
                "success": True,
                "recommendations": recommendations,
                "model": model,
                "usage": {
                    "input_tokens": message.usage.input_tokens,
                    "output_tokens": message.usage.output_tokens
                }
            }

        except anthropic.APIError as e:
            return {
                "success": False,
                "error": f"Claude API error: {str(e)}",
                "recommendations": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Analysis error: {str(e)}",
                "recommendations": None
            }

    def generate_tailored_section(
        self,
        section_name: str,
        original_content: str,
        job_description: str,
        model: str = "claude-3-5-sonnet-20241022"
    ) -> Dict[str, any]:
        """
        Generate a tailored version of a specific resume section

        Args:
            section_name: Name of the section (e.g., "Summary", "Experience")
            original_content: Original section content
            job_description: Job description text
            model: Claude model to use

        Returns:
            Dictionary containing tailored section content
        """
        try:
            prompt = f"""You are an expert resume writer. Rewrite the following resume section to better align with the job description while maintaining truthfulness and the candidate's actual experience.

SECTION: {section_name}

ORIGINAL CONTENT:
{original_content}

JOB DESCRIPTION:
{job_description}

Please provide a tailored version of this section that:
- Emphasizes relevant skills and experiences for this specific job
- Uses keywords from the job description where appropriate
- Maintains the same level of detail but reframes for better alignment
- Keeps all information truthful and accurate

Provide only the rewritten section content, without additional commentary."""

            message = self.client.messages.create(
                model=model,
                max_tokens=2048,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            tailored_content = message.content[0].text

            return {
                "success": True,
                "tailored_content": tailored_content,
                "section": section_name
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Section generation error: {str(e)}",
                "tailored_content": None
            }
