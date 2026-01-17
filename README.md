# Creative Portfolio & Resume Reviewer Bot

Discord bot that automatically detects and evaluates UX design portfolios and resumes using Claude AI. Features intelligent content detection, vision-based portfolio analysis, and entry-level job-focused resume feedback.

## Features

### 🎯 Intelligent Detection
- **Auto-detects** whether uploaded content is a resume or portfolio
- Analyzes keywords, structure, and filename for accurate classification
- Routes to appropriate evaluation strategy automatically

### 📄 Resume Evaluation
- **Entry-level UX job focused** - evaluates against real job requirements
- Checks for relevant skills (Figma, research methods, etc.)
- Analyzes project descriptions and design process evidence
- Reviews formatting and competitive positioning
- Provides actionable feedback for job seekers

### 🎨 Portfolio Evaluation
- **Visual analysis** for portfolio URLs using Claude Vision API
- **Text analysis** for PDF portfolios
- Evaluates case study structure (problem → process → solution → outcome)
- Checks for UX research evidence and user-centered design
- Reviews measurable outcomes and impact
- Assesses accessibility and responsive design considerations

### 🌐 Multi-Format Support
- PDF uploads (resumes and portfolios)
- Live portfolio website URLs
- Automatic screenshot capture for visual analysis

## Quick Start

### Prerequisites
- Python 3.11+
- Discord Bot Token
- Anthropic Claude API Key

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/creative-portfolio-bot.git
cd creative-portfolio-bot

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Linux/Railway: Install system dependencies
playwright install-deps

# Configure environment
cp .env.example .env
# Edit .env with your tokens
```

### Environment Variables

Create `.env` file:
```
DISCORD_TOKEN=your_discord_bot_token
CLAUDE_API_KEY=your_anthropic_api_key
```

### Run Locally

```bash
python bot.py
```

## Usage

### In Discord

**Check bot status:**
```
!ping
```

**Get help:**
```
!guide
```

**Evaluate resume:**
Upload a PDF resume → Bot automatically detects and evaluates

**Evaluate portfolio (visual):**
Post a portfolio website URL → Bot screenshots and analyzes design

**Evaluate portfolio (text):**
Upload portfolio PDF → Bot analyzes content and structure

## Architecture

```
bot.py                          # Discord bot entry point
├── evaluators/
│   ├── resume_evaluator.py     # Entry-level UX job evaluation
│   └── portfolio_evaluator.py  # Visual + text portfolio analysis
├── utils/
│   ├── file_detector.py        # Resume vs portfolio detection
│   ├── pdf_processor.py        # PDF text extraction
│   └── screenshot_service.py   # URL screenshot capture (Playwright)
└── prompts/
    ├── resume_prompts.py       # Resume evaluation criteria
    └── portfolio_prompts.py    # Portfolio evaluation criteria
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Deployment

### Railway (Recommended)

1. Connect GitHub repo to Railway
2. Set environment variables
3. Configure build command:
   ```bash
   pip install -r requirements.txt && playwright install chromium && playwright install-deps
   ```
4. Set start command:
   ```bash
   python bot.py
   ```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide including Docker, Heroku, and troubleshooting.

## Technologies

- **discord.py** - Discord bot framework
- **Anthropic Claude API** - AI evaluation (Sonnet 4)
- **Playwright** - Headless browser for screenshots
- **PyPDF2** - PDF text extraction
- **validators** - URL validation

## Development

### Run Tests

```bash
python test_components.py
```

### Project Structure

```
.
├── bot.py                    # Main bot file
├── evaluators/               # Evaluation logic
├── utils/                    # Utility functions
├── prompts/                  # Evaluation prompts
├── test_components.py        # Component tests
├── requirements.txt          # Python dependencies
├── ARCHITECTURE.md           # Architecture documentation
├── DEPLOYMENT.md            # Deployment guide
└── README.md                # This file
```

## Examples

### Resume Feedback Example

```
📄 Detected: Resume - Evaluating against entry-level UX job requirements...

## Resume Feedback - Entry-Level UX Designer Position

**Relevant Skills & Tools**:
- Strong foundation with Figma, Sketch, and Adobe XD
- Good evidence of user research experience
- Consider adding more technical tools (HTML/CSS, prototyping tools)

**Project Experience**:
- Projects show clear design process
- Add more quantified outcomes (e.g., "improved completion rate by X%")

[... detailed feedback ...]
```

### Portfolio Feedback Example

```
🌐 Portfolio URL detected - Capturing screenshots for visual analysis...
🎨 Analyzing portfolio design, structure, and UX process...

## Portfolio Feedback - Visual Analysis

**Visual Presentation & Polish**:
- Professional layout with strong visual hierarchy
- Cohesive color palette and typography
- Case studies are well-organized and scannable

**Case Study Structure**:
- Clear problem statements present
- Design process is visible with research → ideation → testing
- Could strengthen outcome metrics

[... detailed feedback ...]
```

## Contributing

This bot is designed for UX/design students entering a competitive, AI-affected job market. Contributions that improve feedback quality, add new evaluation criteria, or enhance user experience are welcome!

### Adding New Features

1. Create feature branch
2. Add functionality to appropriate module
3. Update tests in `test_components.py`
4. Update documentation
5. Submit pull request

## License

MIT License - see [LICENSE](LICENSE) file

## Support

- **Issues**: GitHub Issues
- **Documentation**: See ARCHITECTURE.md and DEPLOYMENT.md
- **API Docs**:
  - [Discord.py](https://discordpy.readthedocs.io/)
  - [Anthropic Claude](https://docs.anthropic.com/)
  - [Playwright](https://playwright.dev/python/)

## Roadmap

- [ ] Add batch evaluation support
- [ ] Implement feedback history tracking
- [ ] Add portfolio comparison features
- [ ] Support additional file formats (Figma links, Notion pages)
- [ ] Add interactive feedback refinement
- [ ] Multi-language support

## Acknowledgments

Built to help UX design students get honest, actionable feedback on their job application materials in an increasingly competitive and AI-disrupted job market.
