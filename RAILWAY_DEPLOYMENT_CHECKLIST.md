# Railway Deployment Checklist

## ✅ Pre-Deployment Checklist

- [x] Code committed to GitHub
- [x] All tests passing locally
- [x] Feature branch pushed: `feature/resume-reviewer`
- [ ] Environment variables ready (DISCORD_TOKEN, CLAUDE_API_KEY)
- [ ] Railway account created/logged in
- [ ] GitHub repo connected to Railway

## 📋 Railway Deployment Steps

### Step 1: Connect Repository

1. Go to https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose: `WhiteRabbit-glitch/creative-portfolio-bot`
5. Select branch: `feature/resume-reviewer` (or `main` after merging)

### Step 2: Configure Environment Variables

In Railway dashboard → Variables tab, add:

```
DISCORD_TOKEN=your_discord_bot_token_here
CLAUDE_API_KEY=your_anthropic_api_key_here
```

**Where to get these:**
- DISCORD_TOKEN: https://discord.com/developers/applications
- CLAUDE_API_KEY: https://console.anthropic.com/

### Step 3: Configure Build Settings

In Railway dashboard → Settings:

**Build Command:**
```bash
pip install -r requirements.txt && playwright install chromium && playwright install-deps
```

**Start Command:**
```bash
python bot.py
```

**Note:** Railway may auto-detect Python and use Nixpacks. The above commands should work automatically.

### Step 4: Deploy

1. Click "Deploy"
2. Wait for build to complete (3-5 minutes first time due to Playwright)
3. Check logs for: "Ready to review portfolios and resumes!"

### Step 5: Verify Deployment

In Discord:
```
!ping          # Should respond "Pong!"
!guide         # Should show help message
```

Test functionality:
- Upload a resume PDF
- Upload a portfolio PDF
- Share a portfolio URL

## 🔍 Troubleshooting

### Build Fails - Playwright Issue

**Problem:** Playwright browser not found

**Solution:** Ensure build command includes:
```bash
playwright install chromium && playwright install-deps
```

### Runtime Error - Module Not Found

**Problem:** Dependencies not installed

**Solution:** Check `requirements.txt` is present and build command ran successfully

### Bot Not Responding in Discord

**Problem:** Bot not connecting

**Check:**
1. DISCORD_TOKEN is correct in Railway variables
2. Bot has proper intents enabled (Message Content Intent)
3. Bot is invited to your Discord server
4. Check Railway logs for connection errors

### Claude API Errors

**Problem:** "Error getting feedback"

**Check:**
1. CLAUDE_API_KEY is correct in Railway variables
2. API key has credits/is active
3. Model name is correct: `claude-sonnet-4-20250514`

### Deployment Logs Show Errors

**View logs:**
- Railway dashboard → Deployments → Click latest deployment → View logs

**Common issues:**
- Missing environment variables
- Playwright installation timeout (increase build timeout)
- Out of memory (upgrade Railway plan)

## 📊 Railway Free Tier Limits

- **Memory:** 512MB RAM
- **CPU:** Shared
- **Uptime:** $5 free credit monthly
- **Build time:** May need patience for Playwright

**Tips for free tier:**
- Monitor usage in Railway dashboard
- Consider shorter screenshot timeouts
- Clean up old deployments

## 🔄 Updating After Deployment

### For code changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin feature/resume-reviewer
   ```

2. Railway auto-deploys if connected (check settings)

3. Or manually trigger deploy in Railway dashboard

### For dependency changes:

1. Update `requirements.txt`
2. Commit and push
3. Railway will rebuild with new dependencies

## 🎯 Post-Deployment

### Monitor Performance

- Check Railway dashboard for:
  - Memory usage
  - CPU usage
  - Request logs
  - Error rate

### Set Up Alerts (Optional)

- Railway can notify on deployment failures
- Configure in Settings → Notifications

### Cost Management

- Monitor free tier usage
- Upgrade to hobby plan ($5/month) if needed
- Set usage alerts

## ✨ Success Indicators

Your deployment is successful when:

- ✅ Build completes without errors
- ✅ Bot shows online in Discord
- ✅ `!ping` responds
- ✅ `!guide` shows help
- ✅ PDF uploads get analyzed
- ✅ URLs get screenshotted and analyzed
- ✅ No errors in Railway logs

## 📞 Support Resources

- **Railway Docs:** https://docs.railway.app/
- **Discord.py Docs:** https://discordpy.readthedocs.io/
- **Anthropic Docs:** https://docs.anthropic.com/
- **Playwright Docs:** https://playwright.dev/python/

## 🚀 Alternative: Merge to Main First

If you want to deploy from main branch:

```bash
git checkout main
git merge feature/resume-reviewer
git push origin main
```

Then deploy main branch in Railway.

---

## Quick Reference

**Repository:** https://github.com/WhiteRabbit-glitch/creative-portfolio-bot

**Branch:** feature/resume-reviewer

**Build Command:**
```bash
pip install -r requirements.txt && playwright install chromium && playwright install-deps
```

**Start Command:**
```bash
python bot.py
```

**Environment Variables:**
- DISCORD_TOKEN
- CLAUDE_API_KEY

**Expected Build Time:** 3-5 minutes (first time)

**Expected Startup:** ~10 seconds

---

Good luck with deployment! 🎉
