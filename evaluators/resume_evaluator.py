"""
Resume evaluation using Claude API for text-based analysis.
"""
import anthropic
from typing import Dict, Optional
from prompts.resume_prompts import RESUME_PROMPTS


class ResumeEvaluator:
    """Evaluates resumes using Claude's text analysis."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize resume evaluator.

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    async def evaluate(
        self,
        resume_text: str,
        prompt_type: str = 'entry_level_ux',
        max_tokens: int = 1500
    ) -> str:
        """
        Evaluate a resume and provide feedback.

        Args:
            resume_text: Extracted text from resume
            prompt_type: Type of evaluation ('entry_level_ux' or 'general')
            max_tokens: Maximum tokens for response

        Returns:
            Evaluation feedback text
        """
        # Get prompt template
        prompt_template = RESUME_PROMPTS.get(prompt_type, RESUME_PROMPTS['general'])

        # Format prompt with resume text
        formatted_prompt = prompt_template.format(resume_text=resume_text[:15000])

        try:
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ]
            )

            return message.content[0].text

        except Exception as e:
            raise Exception(f"Error getting resume feedback: {str(e)}")

    async def quick_check(self, resume_text: str) -> Dict[str, any]:
        """
        Perform a quick check of resume quality.

        Args:
            resume_text: Extracted text from resume

        Returns:
            Dictionary with quick assessment metrics
        """
        text_lower = resume_text.lower()

        # Check for key sections
        has_experience = any(word in text_lower for word in ['experience', 'work history', 'employment'])
        has_education = 'education' in text_lower
        has_skills = 'skills' in text_lower
        has_contact = '@' in resume_text  # Email present

        # Check for UX-specific content
        ux_tools = ['figma', 'sketch', 'adobe xd', 'invision', 'axure', 'miro', 'framer']
        has_ux_tools = any(tool in text_lower for tool in ux_tools)

        research_methods = ['user research', 'usability testing', 'interviews', 'surveys', 'personas']
        has_research = any(method in text_lower for method in research_methods)

        return {
            'has_experience': has_experience,
            'has_education': has_education,
            'has_skills': has_skills,
            'has_contact': has_contact,
            'has_ux_tools': has_ux_tools,
            'has_research_methods': has_research,
            'word_count': len(resume_text.split()),
            'completeness_score': sum([
                has_experience, has_education, has_skills, has_contact
            ]) / 4.0
        }
