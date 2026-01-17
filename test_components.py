"""
Test script for validating core components.
"""
import asyncio
from utils import FileDetector, PDFProcessor, ScreenshotService
from evaluators import ResumeEvaluator, PortfolioEvaluator
import os
from dotenv import load_dotenv

load_dotenv()

def test_file_detector():
    """Test file type detection."""
    print("\n=== Testing FileDetector ===")

    # Test resume text
    resume_text = """
    John Doe
    john.doe@email.com | 555-123-4567

    OBJECTIVE
    Seeking entry-level UX Designer position

    EXPERIENCE
    UX Design Intern - Company A
    - Created wireframes in Figma
    - Conducted user interviews

    EDUCATION
    BS in Human-Computer Interaction

    SKILLS
    Figma, Adobe XD, User Research, Usability Testing
    """

    file_type = FileDetector.detect(resume_text, "john_resume.pdf")
    print(f"Resume detection: {file_type}")
    assert file_type == 'resume', f"Expected 'resume', got '{file_type}'"

    # Test portfolio text
    portfolio_text = """
    Case Study: E-commerce Redesign

    Problem Statement
    Users were abandoning their shopping carts at a 60% rate.

    User Research
    Conducted interviews with 15 users and usability testing sessions.
    Created personas based on research findings.

    Design Process
    1. Information architecture review
    2. Wireframing and prototyping
    3. Iterative design with user feedback
    4. Usability testing

    Solution
    Redesigned checkout flow with clear progress indicators

    Outcome
    Reduced cart abandonment by 40%
    Increased conversion rate by 25%
    """

    file_type = FileDetector.detect(portfolio_text, "jane_portfolio.pdf")
    print(f"Portfolio detection: {file_type}")
    assert file_type == 'portfolio', f"Expected 'portfolio', got '{file_type}'"

    print("[PASS] FileDetector tests passed!")


def test_pdf_processor():
    """Test PDF processor (basic validation)."""
    print("\n=== Testing PDFProcessor ===")

    # Just test that the class exists and has expected methods
    assert hasattr(PDFProcessor, 'extract_text')
    assert hasattr(PDFProcessor, 'get_page_count')
    assert hasattr(PDFProcessor, 'validate_pdf')

    print("[PASS] PDFProcessor structure validated!")


async def test_screenshot_service():
    """Test screenshot service."""
    print("\n=== Testing ScreenshotService ===")

    # Test URL validation
    assert ScreenshotService.is_valid_url("https://example.com")
    assert ScreenshotService.is_valid_url("example.com")
    assert not ScreenshotService.is_valid_url("not a url")

    # Test URL normalization
    normalized = ScreenshotService.normalize_url("example.com")
    assert normalized == "https://example.com"

    normalized = ScreenshotService.normalize_url("http://example.com")
    assert normalized == "http://example.com"

    print("[PASS] ScreenshotService validation tests passed!")

    # Optional: Test actual screenshot (requires network)
    test_screenshot = input("\nTest actual screenshot capture? (y/n): ").lower() == 'y'
    if test_screenshot:
        print("Capturing screenshot of example.com...")
        async with ScreenshotService() as service:
            try:
                screenshot_path = await service.capture_screenshot(
                    "https://example.com",
                    viewport_width=1920,
                    viewport_height=1080
                )
                print(f"Screenshot saved: {screenshot_path}")
                if os.path.exists(screenshot_path):
                    os.remove(screenshot_path)
                    print("[PASS] Screenshot test passed!")
            except Exception as e:
                print(f"Screenshot test failed: {e}")


def test_evaluators():
    """Test evaluator initialization."""
    print("\n=== Testing Evaluators ===")

    api_key = os.getenv('CLAUDE_API_KEY')

    if not api_key:
        print("[WARN] CLAUDE_API_KEY not found in .env, skipping evaluator tests")
        return

    # Test initialization
    resume_eval = ResumeEvaluator(api_key=api_key)
    portfolio_eval = PortfolioEvaluator(api_key=api_key)

    print("[PASS] Evaluators initialized successfully!")

    # Test that methods exist
    assert hasattr(resume_eval, 'evaluate')
    assert hasattr(resume_eval, 'quick_check')
    assert hasattr(portfolio_eval, 'evaluate_visual')
    assert hasattr(portfolio_eval, 'evaluate_text')
    assert hasattr(portfolio_eval, 'evaluate_hybrid')

    print("[PASS] Evaluator methods validated!")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Creative Portfolio Bot Components")
    print("=" * 60)

    try:
        test_file_detector()
        test_pdf_processor()
        await test_screenshot_service()
        test_evaluators()

        print("\n" + "=" * 60)
        print("[PASS] All tests passed!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
