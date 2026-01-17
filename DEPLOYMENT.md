# Deployment Guide

## Railway Deployment

### Prerequisites
- Railway account (railway.app)
- GitHub repository connected to Railway
- Environment variables configured

### Step 1: Configure Environment Variables

In Railway dashboard, add these environment variables:

```
DISCORD_TOKEN=your_discord_bot_token
CLAUDE_API_KEY=your_anthropic_api_key
```

### Step 2: Configure Build & Start Commands

**Build Command:**
```bash
pip install -r requirements.txt && playwright install chromium && playwright install-deps
```

**Start Command:**
```bash
python bot.py
```

### Step 3: Railway Configuration File

Create `railway.toml` (optional, for advanced config):

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python bot.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Step 4: Nixpacks Configuration

Create `nixpacks.toml` for Playwright dependencies:

```toml
[phases.setup]
nixPkgs = ['...', 'chromium']

[phases.install]
cmds = ['pip install -r requirements.txt', 'playwright install chromium', 'playwright install-deps']
```

## Alternative: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser
RUN playwright install chromium

# Copy application code
COPY . .

# Run bot
CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t portfolio-bot .
docker run -d --env-file .env portfolio-bot
```

## Heroku Deployment

Create `Procfile`:
```
worker: python bot.py
```

Create `runtime.txt`:
```
python-3.11.0
```

Deploy commands:
```bash
heroku create your-bot-name
heroku config:set DISCORD_TOKEN=your_token
heroku config:set CLAUDE_API_KEY=your_key
git push heroku main
heroku ps:scale worker=1
```

## Environment Setup

### Discord Bot Setup

1. Go to https://discord.com/developers/applications
2. Create new application
3. Go to "Bot" section
4. Enable these intents:
   - Message Content Intent
   - Messages Intent
5. Copy bot token
6. Generate invite URL with these permissions:
   - Send Messages
   - Read Messages/View Channels
   - Add Reactions
   - Attach Files

### Anthropic API Setup

1. Go to https://console.anthropic.com/
2. Create API key
3. Copy key to environment variables

## Testing Deployment

### Test Commands

Once deployed, test in Discord:

```
!ping          # Check bot is alive
!guide         # View help message
```

### Test Workflows

1. **Resume Test**: Upload a PDF resume
   - Should detect as resume
   - Should provide entry-level UX job feedback

2. **Portfolio PDF Test**: Upload a portfolio PDF with text
   - Should detect as portfolio
   - Should analyze content and structure

3. **Portfolio URL Test**: Post a portfolio website URL
   - Should capture screenshot
   - Should analyze visual design and UX

## Monitoring

### Logs

**Railway:**
```bash
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

**Docker:**
```bash
docker logs -f container_id
```

### Health Checks

Bot sends confirmation messages on startup:
```
{bot_user} has connected to Discord!
Bot is in X server(s)
Ready to review portfolios and resumes!
```

## Troubleshooting

### Playwright Browser Not Found

**Issue:** Bot crashes with "browser not found"

**Solution:**
```bash
playwright install chromium
playwright install-deps  # Linux only
```

### Import Errors

**Issue:** ModuleNotFoundError

**Solution:**
```bash
pip install -r requirements.txt
```

### Discord Connection Issues

**Issue:** Bot not responding in Discord

**Checks:**
1. Verify DISCORD_TOKEN is correct
2. Check bot has proper intents enabled
3. Verify bot has permissions in server
4. Check logs for connection errors

### Claude API Errors

**Issue:** "Error getting feedback"

**Checks:**
1. Verify CLAUDE_API_KEY is correct
2. Check API rate limits
3. Verify model name is correct (claude-sonnet-4-20250514)
4. Check account has credits

### Screenshot Timeout

**Issue:** "Failed to capture screenshot"

**Solutions:**
1. Increase timeout in bot.py:
   ```python
   await page.goto(url, wait_until=wait_until, timeout=60000)
   ```
2. Check URL is accessible
3. Verify Playwright browser installed correctly

## Performance Optimization

### Resource Limits

**Railway Free Tier:**
- 512MB RAM
- Shared CPU
- Consider shorter timeouts for screenshots

**Optimizations:**
1. Limit full-page screenshot resolution
2. Use viewport screenshots for large sites
3. Add rate limiting for concurrent requests
4. Clean up temp files promptly

### Cost Management

**Claude API:**
- Current usage: ~1500-2000 tokens per evaluation
- Monitor with Anthropic console
- Set usage alerts

**Railway:**
- Monitor deployment usage
- Upgrade plan if needed for consistent uptime

## Updates & Maintenance

### Updating Dependencies

```bash
pip install --upgrade anthropic discord.py
pip freeze > requirements.txt
```

### Railway Auto-Deploy

Connect GitHub repo to Railway for automatic deployments on push to main.

### Manual Deploy

```bash
git push railway main
```

## Support

- **Discord.py docs**: https://discordpy.readthedocs.io/
- **Anthropic docs**: https://docs.anthropic.com/
- **Playwright docs**: https://playwright.dev/python/
- **Railway docs**: https://docs.railway.app/
