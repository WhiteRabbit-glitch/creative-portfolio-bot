"""
Screenshot service for capturing web pages using Playwright.
"""
import asyncio
import base64
from pathlib import Path
from typing import Optional, List
import validators
from playwright.async_api import async_playwright, Browser, Page


class ScreenshotService:
    """Captures screenshots of URLs using Playwright."""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None

    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

    async def start(self):
        """Initialize Playwright browser."""
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )

    async def close(self):
        """Close browser and cleanup."""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validate if string is a valid URL.

        Args:
            url: String to validate

        Returns:
            True if valid URL
        """
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        return validators.url(url) is True

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize URL by adding protocol if missing.

        Args:
            url: URL string

        Returns:
            Normalized URL with protocol
        """
        if not url.startswith(('http://', 'https://')):
            return 'https://' + url
        return url

    async def capture_screenshot(
        self,
        url: str,
        output_path: Optional[str] = None,
        full_page: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        wait_until: str = 'networkidle'
    ) -> str:
        """
        Capture screenshot of a URL.

        Args:
            url: URL to screenshot
            output_path: Optional path to save screenshot
            full_page: Capture full page or just viewport
            viewport_width: Browser viewport width
            viewport_height: Browser viewport height
            wait_until: When to consider navigation complete

        Returns:
            Path to saved screenshot

        Raises:
            ValueError: If URL is invalid
            Exception: If screenshot fails
        """
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")

        url = self.normalize_url(url)

        await self.start()

        try:
            page = await self.browser.new_page(
                viewport={'width': viewport_width, 'height': viewport_height}
            )

            # Navigate to URL
            await page.goto(url, wait_until=wait_until, timeout=30000)

            # Wait a bit for dynamic content
            await page.wait_for_timeout(2000)

            # Take screenshot
            if output_path:
                await page.screenshot(path=output_path, full_page=full_page)
                screenshot_path = output_path
            else:
                # Generate temp filename
                from tempfile import NamedTemporaryFile
                with NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    screenshot_path = tmp.name
                await page.screenshot(path=screenshot_path, full_page=full_page)

            await page.close()
            return screenshot_path

        except Exception as e:
            raise Exception(f"Failed to capture screenshot: {str(e)}")

    async def capture_multiple_screenshots(
        self,
        urls: List[str],
        output_dir: Optional[str] = None
    ) -> List[str]:
        """
        Capture screenshots of multiple URLs.

        Args:
            urls: List of URLs
            output_dir: Optional directory to save screenshots

        Returns:
            List of paths to saved screenshots
        """
        await self.start()
        screenshots = []

        for i, url in enumerate(urls):
            try:
                if output_dir:
                    output_path = f"{output_dir}/screenshot_{i}.png"
                else:
                    output_path = None

                path = await self.capture_screenshot(url, output_path)
                screenshots.append(path)
            except Exception as e:
                print(f"Failed to capture {url}: {e}")
                screenshots.append(None)

        return screenshots

    async def get_page_text(self, url: str) -> str:
        """
        Extract text content from a URL.

        Args:
            url: URL to extract text from

        Returns:
            Text content
        """
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")

        url = self.normalize_url(url)
        await self.start()

        try:
            page = await self.browser.new_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)

            # Extract text content
            text = await page.evaluate('() => document.body.innerText')

            await page.close()
            return text

        except Exception as e:
            raise Exception(f"Failed to extract text: {str(e)}")

    @staticmethod
    def image_to_base64(image_path: str) -> str:
        """
        Convert image to base64 string.

        Args:
            image_path: Path to image file

        Returns:
            Base64 encoded string
        """
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
