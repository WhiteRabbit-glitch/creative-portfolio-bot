# Creative Portfolio Bot - Architecture

## Overview
Discord bot that automatically detects and evaluates resumes and portfolios for UX designers. Uses Claude AI for intelligent analysis with different evaluation strategies based on content type.

## System Architecture

```
bot.py (Discord entry point)
├── evaluators/
│   ├── resume_evaluator.py      # Text-based resume analysis
│   └── portfolio_evaluator.py   # Vision-based portfolio analysis
├── utils/
│   ├── file_detector.py         # Auto-detect resume vs portfolio
│   ├── pdf_processor.py         # PDF text extraction
│   └── screenshot_service.py    # URL screenshot capture (Playwright)
└── prompts/
    ├── resume_prompts.py        # Resume evaluation prompts
    └── portfolio_prompts.py     # Portfolio evaluation prompts
```

## Features

### 1. Auto-Detection System
**FileDetector** (`utils/file_detector.py`)
- Analyzes text content for resume vs portfolio keywords
- Checks filename for hints
- Uses structural indicators (bullet points, paragraphs, contact info)
- Returns confidence scores for classification

### 2. Resume Evaluation
**ResumeEvaluator** (`evaluators/resume_evaluator.py`)
- **Input**: Text extracted from PDF
- **Process**: Claude text analysis with entry-level UX job criteria
- **Evaluates**:
  - Relevant UX skills and tools
  - Project experience and design process
  - Education and certifications
  - Resume formatting and presentation
  - Competitive positioning

### 3. Portfolio Evaluation
**PortfolioEvaluator** (`evaluators/portfolio_evaluator.py`)
- **Modes**:
  - **Visual** (from URL): Screenshots portfolio website, uses Claude Vision API
  - **Text** (from PDF): Text-based analysis of case studies
  - **Hybrid**: Combined visual + text analysis

- **Evaluates**:
  - Case study structure (problem → process → solution → outcome)
  - Visual presentation quality
  - UX research evidence
  - Measurable outcomes
  - Accessibility and responsiveness

### 4. Screenshot Service
**ScreenshotService** (`utils/screenshot_service.py`)
- **Technology**: Playwright (headless Chromium)
- Captures full-page screenshots of portfolio URLs
- Validates URLs automatically
- Configurable viewport sizes
- Async context manager for browser lifecycle

## Usage Flows

### Flow 1: PDF Resume
```
User uploads PDF → bot.py detects PDF
→ PDFProcessor extracts text
→ FileDetector identifies as "resume"
→ ResumeEvaluator analyzes against UX job criteria
→ Feedback sent to Discord
```

### Flow 2: PDF Portfolio
```
User uploads PDF → bot.py detects PDF
→ PDFProcessor extracts text
→ FileDetector identifies as "portfolio"
→ PortfolioEvaluator analyzes text content
→ Feedback sent to Discord
```

### Flow 3: Portfolio URL
```
User posts URL → bot.py detects URL
→ ScreenshotService captures full-page screenshot
→ PortfolioEvaluator analyzes visually using Claude Vision
→ Feedback sent to Discord
```

## Key Technologies

- **discord.py**: Discord bot framework
- **Anthropic Claude API**: AI evaluation (Sonnet 4)
- **Playwright**: Headless browser for screenshots
- **PyPDF2**: PDF text extraction
- **validators**: URL validation

## Deployment Notes

### Railway Compatibility
- All dependencies are Railway-compatible
- Playwright requires system dependencies:
  ```bash
  playwright install chromium
  playwright install-deps
  ```
- Add to Railway build command or Dockerfile

### Environment Variables
```
DISCORD_TOKEN=your_discord_token
CLAUDE_API_KEY=your_anthropic_api_key
```

### Installation
```bash
pip install -r requirements.txt
playwright install chromium
playwright install-deps  # Linux/Railway only
```

## Code Quality

- **Async/await**: All I/O operations are async
- **Error handling**: Try-except blocks with user-friendly error messages
- **Resource cleanup**: Temp files and browser instances properly closed
- **Type hints**: Used throughout for better IDE support
- **Modular design**: Clear separation of concerns

## Extensibility

### Adding New Evaluation Types
1. Create new prompt in `prompts/`
2. Add evaluation method to appropriate evaluator
3. Update bot.py routing logic

### Adding New File Types
1. Update `FileDetector` with new keywords
2. Add processor in `utils/`
3. Wire into bot.py `on_message` handler

### Customizing Prompts
All prompts are in `prompts/` directory as template strings. Modify without touching core logic.
