"""
File type detection for resume vs portfolio identification.
"""
import re
from typing import Tuple


class FileDetector:
    """Detects whether a PDF or content is a resume or portfolio."""

    # Keywords that strongly indicate a resume
    RESUME_KEYWORDS = [
        'objective', 'summary', 'experience', 'education', 'skills',
        'employment', 'work history', 'qualifications', 'professional summary',
        'career objective', 'references', 'certifications', 'languages spoken'
    ]

    # Keywords that strongly indicate a portfolio
    PORTFOLIO_KEYWORDS = [
        'case study', 'project', 'design process', 'user research',
        'wireframe', 'prototype', 'user flow', 'information architecture',
        'usability testing', 'persona', 'journey map', 'design system',
        'problem statement', 'solution', 'outcome', 'impact'
    ]

    @staticmethod
    def detect_from_text(text: str) -> Tuple[str, float]:
        """
        Detect if text content is from a resume or portfolio.

        Args:
            text: Extracted text content from PDF

        Returns:
            Tuple of (type, confidence) where type is 'resume' or 'portfolio'
            and confidence is a float between 0 and 1
        """
        if not text or len(text) < 50:
            return 'unknown', 0.0

        text_lower = text.lower()

        # Count keyword matches
        resume_score = sum(1 for keyword in FileDetector.RESUME_KEYWORDS
                          if keyword in text_lower)
        portfolio_score = sum(1 for keyword in FileDetector.PORTFOLIO_KEYWORDS
                             if keyword in text_lower)

        # Check for structural indicators
        # Resumes often have bullet points and short entries
        bullet_points = len(re.findall(r'[•\-\*]\s', text))

        # Portfolios often have longer narrative sections
        paragraphs = len(re.findall(r'\n\n', text))

        # Resumes often have email addresses and phone numbers
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text))

        # Calculate scores
        if has_email and has_phone:
            resume_score += 3

        if bullet_points > 10:
            resume_score += 2

        if paragraphs > 5:
            portfolio_score += 2

        # Determine type and confidence
        total_score = resume_score + portfolio_score

        if total_score == 0:
            return 'unknown', 0.0

        if resume_score > portfolio_score:
            confidence = min(resume_score / max(total_score, 1), 1.0)
            return 'resume', confidence
        elif portfolio_score > resume_score:
            confidence = min(portfolio_score / max(total_score, 1), 1.0)
            return 'portfolio', confidence
        else:
            # Tie - use additional heuristics
            if has_email and has_phone:
                return 'resume', 0.5
            elif paragraphs > bullet_points:
                return 'portfolio', 0.5
            else:
                return 'unknown', 0.3

    @staticmethod
    def detect_from_filename(filename: str) -> Tuple[str, float]:
        """
        Detect file type from filename.

        Args:
            filename: Name of the file

        Returns:
            Tuple of (type, confidence)
        """
        filename_lower = filename.lower()

        if 'resume' in filename_lower or 'cv' in filename_lower:
            return 'resume', 0.8
        elif 'portfolio' in filename_lower:
            return 'portfolio', 0.8

        return 'unknown', 0.0

    @staticmethod
    def detect(text: str, filename: str = '') -> str:
        """
        Main detection method that combines multiple signals.

        Args:
            text: Extracted text content
            filename: Optional filename

        Returns:
            'resume', 'portfolio', or 'unknown'
        """
        # Try filename first
        filename_type, filename_conf = FileDetector.detect_from_filename(filename)

        # Try text analysis
        text_type, text_conf = FileDetector.detect_from_text(text)

        # Combine signals
        if filename_conf >= 0.8:
            return filename_type
        elif text_conf >= 0.5:
            return text_type
        elif filename_conf > 0 and text_type == filename_type:
            return filename_type
        elif text_conf > filename_conf:
            return text_type
        else:
            # Default to portfolio if uncertain (original bot behavior)
            return 'portfolio' if text_type == 'unknown' else text_type
