"""
Portfolio evaluation using Claude Vision API for visual analysis.
"""
import anthropic
import base64
from typing import List, Optional, Union
from pathlib import Path
from prompts.portfolio_prompts import PORTFOLIO_PROMPTS


class PortfolioEvaluator:
    """Evaluates portfolios using Claude's vision capabilities."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize portfolio evaluator.

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    @staticmethod
    def encode_image(image_path: str) -> tuple[str, str]:
        """
        Encode image to base64 and detect media type.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (media_type, base64_data)
        """
        # Detect media type from extension
        extension = Path(image_path).suffix.lower()
        media_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_types.get(extension, 'image/png')

        # Read and encode image
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        return media_type, image_data

    async def evaluate_visual(
        self,
        image_paths: Union[str, List[str]],
        prompt_type: str = 'ux_visual',
        max_tokens: int = 2000
    ) -> str:
        """
        Evaluate portfolio from images using vision API.

        Args:
            image_paths: Single image path or list of image paths
            prompt_type: Type of evaluation prompt
            max_tokens: Maximum tokens for response

        Returns:
            Evaluation feedback text
        """
        # Ensure image_paths is a list
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        # Get prompt template
        prompt_template = PORTFOLIO_PROMPTS.get(prompt_type, PORTFOLIO_PROMPTS['general_visual'])

        # Build message content with images
        content = []

        # Add all images
        for image_path in image_paths[:10]:  # Limit to 10 images
            try:
                media_type, image_data = self.encode_image(image_path)
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                })
            except Exception as e:
                print(f"Warning: Failed to encode image {image_path}: {e}")

        # Add text prompt after images
        content.append({
            "type": "text",
            "text": prompt_template
        })

        try:
            # Call Claude API with vision
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )

            return message.content[0].text

        except Exception as e:
            raise Exception(f"Error getting portfolio feedback: {str(e)}")

    async def evaluate_text(
        self,
        portfolio_text: str,
        prompt_type: str = 'ux_text',
        max_tokens: int = 1500
    ) -> str:
        """
        Evaluate portfolio from text content (for text-based portfolios).

        Args:
            portfolio_text: Extracted text from portfolio
            prompt_type: Type of evaluation prompt
            max_tokens: Maximum tokens for response

        Returns:
            Evaluation feedback text
        """
        # Get prompt template
        prompt_template = PORTFOLIO_PROMPTS.get(prompt_type, PORTFOLIO_PROMPTS['ux_text'])

        # Format prompt with portfolio text
        formatted_prompt = prompt_template.format(portfolio_text=portfolio_text[:15000])

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
            raise Exception(f"Error getting portfolio feedback: {str(e)}")

    async def evaluate_hybrid(
        self,
        portfolio_text: str,
        image_paths: Optional[List[str]] = None,
        max_tokens: int = 2000
    ) -> str:
        """
        Evaluate portfolio using both text and images.

        Args:
            portfolio_text: Extracted text from portfolio
            image_paths: Optional list of image paths
            max_tokens: Maximum tokens for response

        Returns:
            Evaluation feedback text
        """
        if not image_paths:
            # No images, use text-only evaluation
            return await self.evaluate_text(portfolio_text)

        # Build hybrid content
        content = []

        # Add images first
        for image_path in image_paths[:5]:  # Limit to 5 for hybrid
            try:
                media_type, image_data = self.encode_image(image_path)
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                })
            except Exception as e:
                print(f"Warning: Failed to encode image {image_path}: {e}")

        # Add text analysis prompt
        prompt = f"""You are a UX hiring manager reviewing a portfolio. You have both visual and text content to analyze.

Visual content is shown in the images above.

Text content from the portfolio:
{portfolio_text[:10000]}

Provide comprehensive feedback considering both the visual presentation and the written case study content. Focus on:
1. Visual presentation quality and professionalism
2. Case study structure and clarity
3. Evidence of UX process and user-centered design
4. Measurable outcomes and impact
5. Areas of strength and opportunities for improvement

Format: Clear sections with bullet points, 500-700 words."""

        content.append({
            "type": "text",
            "text": prompt
        })

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )

            return message.content[0].text

        except Exception as e:
            raise Exception(f"Error getting hybrid portfolio feedback: {str(e)}")
