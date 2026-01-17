# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment
Create `.env` file:
```
DISCORD_TOKEN=your_discord_bot_token
CLAUDE_API_KEY=your_anthropic_api_key
```

### 3. Run Tests (Optional)
```bash
python test_components.py
```

### 4. Start Bot
```bash
python bot.py
```

## 🎮 Usage in Discord

| Action | Result |
|--------|--------|
| Upload PDF resume | Auto-detects as resume, evaluates against UX job criteria |
| Upload PDF portfolio | Auto-detects as portfolio, analyzes content |
| Post portfolio URL | Screenshots and analyzes visual design |
| `!ping` | Check bot status |
| `!guide` | Show help message |

## 📊 What Gets Evaluated

### Resumes
- UX skills and tools
- Project experience
- Education and certs
- Format and presentation
- Job market positioning

### Portfolios
- Case study structure
- Visual presentation
- UX research evidence
- Design process
- Measurable outcomes
- Accessibility

## 🛠️ Common Commands

```bash
# Test imports
python -c "from utils import FileDetector; from evaluators import ResumeEvaluator; print('OK')"

# Run with logging
python bot.py 2>&1 | tee bot.log

# Check Git status
git status

# Run tests
python test_components.py
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'validators'` | `pip install validators playwright` |
| `Browser not found` | `playwright install chromium` |
| Bot not responding | Check DISCORD_TOKEN in .env |
| Claude API error | Check CLAUDE_API_KEY in .env |

## 📦 Deploy to Railway

1. Push to GitHub
2. Connect repo to Railway
3. Add environment variables
4. Build command: `pip install -r requirements.txt && playwright install chromium && playwright install-deps`
5. Start command: `python bot.py`

## 📖 Documentation

- **ARCHITECTURE.md** - System design and components
- **DEPLOYMENT.md** - Full deployment guide
- **README.md** - Complete documentation
- **IMPLEMENTATION_SUMMARY.md** - What was built

## 🎯 Key Files

```
bot.py                          Main Discord bot
evaluators/resume_evaluator.py  Resume analysis
evaluators/portfolio_evaluator.py  Portfolio analysis
utils/file_detector.py          Auto-detection logic
utils/screenshot_service.py     URL screenshot capture
prompts/                        Evaluation criteria templates
```

## ⚡ Quick Test Sequence

1. Start bot: `python bot.py`
2. In Discord: `!ping` (should respond "Pong!")
3. In Discord: `!guide` (shows help)
4. Upload a test PDF
5. Post a test portfolio URL
6. Verify feedback is received

## 🎓 Example Workflow

```
# User uploads "JohnDoe_Resume.pdf"
Bot: 👀 (acknowledging)
Bot: ⚙️ (processing)
Bot: 🔍 (detecting type)
Bot: 📄 Detected: Resume - Evaluating...
Bot: 🤔 (analyzing)
Bot: ✅ (done)
Bot: [Detailed resume feedback]

# User posts "https://myportfolio.com"
Bot: 👀 (acknowledging)
Bot: 📸 (capturing screenshot)
Bot: 🌐 Portfolio URL detected...
Bot: 🤔 (analyzing)
Bot: ✅ (done)
Bot: [Detailed portfolio feedback]
```

## 💡 Pro Tips

1. **Resume detection works best with:**
   - Clear sections (Experience, Education, Skills)
   - Contact information
   - Bullet points for achievements

2. **Portfolio detection works best with:**
   - Case study keywords
   - Design process descriptions
   - User research mentions

3. **For best feedback:**
   - Resumes: Export as text-based PDF
   - Portfolio PDFs: Include readable text
   - Portfolio URLs: Ensure site loads quickly

4. **Rate limiting:**
   - Claude API has rate limits
   - Consider adding cooldown between evaluations

5. **Cost management:**
   - ~1500-2000 tokens per evaluation
   - Monitor usage in Anthropic console

## 🚨 Important Notes

- Playwright requires ~170MB download for Chromium
- Screenshots timeout after 30 seconds
- PDFs with <50 chars are rejected
- Maximum 15,000 chars sent to Claude API
- Discord message limit is 2000 chars (auto-chunked)

## ✅ Checklist Before Deploying

- [ ] Dependencies installed
- [ ] Playwright browser downloaded
- [ ] .env file configured
- [ ] Tests passing
- [ ] Bot connects to Discord locally
- [ ] Sample evaluations work
- [ ] Git committed and pushed
- [ ] Railway environment variables set
- [ ] Build command configured
- [ ] Start command configured

---

**Need more help?** Check DEPLOYMENT.md for detailed guides and troubleshooting.
