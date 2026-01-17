import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re
from utils import FileDetector, PDFProcessor, ScreenshotService
from evaluators import ResumeEvaluator, PortfolioEvaluator

# Load secrets
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

# Initialize clients
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize evaluators
resume_evaluator = ResumeEvaluator(api_key=CLAUDE_API_KEY)
portfolio_evaluator = PortfolioEvaluator(api_key=CLAUDE_API_KEY)


def is_url(text: str) -> bool:
    """Check if text is a URL."""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.match(text))


def extract_urls_from_message(message: str) -> list:
    """Extract URLs from message content."""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_pattern.findall(message)


async def process_pdf(attachment, message):
    """Process PDF attachment - detect type and evaluate accordingly."""
    await message.add_reaction('👀')

    try:
        # Download PDF
        pdf_bytes = await attachment.read()
        temp_path = f"temp_{attachment.filename}"

        with open(temp_path, 'wb') as f:
            f.write(pdf_bytes)

        await message.add_reaction('⚙️')

        # Extract text
        try:
            text_content = PDFProcessor.extract_text(temp_path)
        except Exception as e:
            os.remove(temp_path)
            await message.reply(f"❌ Error extracting text from PDF: {str(e)}")
            return

        # Check if we got text
        if len(text_content) < 50:
            os.remove(temp_path)
            await message.reply("⚠️ This PDF seems to be mostly images or very short. For portfolios with mainly images, please share a URL instead. For resumes, try exporting as a text-based PDF.")
            return

        # Detect file type
        await message.add_reaction('🔍')
        file_type = FileDetector.detect(text_content, attachment.filename)

        # Route to appropriate evaluator
        await message.add_reaction('🤔')

        if file_type == 'resume':
            # Resume evaluation
            await message.channel.send(f"📄 Detected: **Resume** - Evaluating against entry-level UX job requirements...")
            feedback = await resume_evaluator.evaluate(text_content, prompt_type='entry_level_ux')
            header = "## Resume Feedback - Entry-Level UX Designer Position\n\n"
        else:
            # Portfolio evaluation (text-based)
            await message.channel.send(f"📁 Detected: **Portfolio** - Analyzing content and structure...")
            feedback = await portfolio_evaluator.evaluate_text(text_content, prompt_type='ux_text')
            header = "## Portfolio Feedback\n\n"

        # Clean up temp file
        os.remove(temp_path)

        # Send feedback in chunks if needed (Discord has 2000 char limit)
        if len(feedback) <= 1900:
            await message.reply(f"{header}{feedback}")
        else:
            # Split into chunks
            chunks = [feedback[i:i+1800] for i in range(0, len(feedback), 1800)]
            await message.reply(f"{header}{chunks[0]}")
            for i, chunk in enumerate(chunks[1:], 2):
                await message.channel.send(f"**(Part {i})**\n\n{chunk}")

        # Success reaction
        await message.add_reaction('✅')

    except Exception as e:
        await message.reply(f'❌ Error processing PDF: {str(e)}')
        print(f"Error details: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)


async def process_url(url: str, message):
    """Process portfolio URL - screenshot and evaluate visually."""
    await message.add_reaction('👀')

    try:
        # Validate URL
        if not ScreenshotService.is_valid_url(url):
            await message.reply(f"❌ Invalid URL: {url}")
            return

        await message.add_reaction('📸')
        await message.channel.send(f"🌐 **Portfolio URL detected** - Capturing screenshots for visual analysis...")

        # Capture screenshot
        async with ScreenshotService() as screenshot_service:
            try:
                screenshot_path = await screenshot_service.capture_screenshot(
                    url,
                    full_page=True,
                    viewport_width=1920,
                    viewport_height=1080
                )
            except Exception as e:
                await message.reply(f"❌ Error capturing screenshot: {str(e)}")
                return

        # Evaluate portfolio visually
        await message.add_reaction('🤔')
        await message.channel.send("🎨 Analyzing portfolio design, structure, and UX process...")

        feedback = await portfolio_evaluator.evaluate_visual(
            screenshot_path,
            prompt_type='ux_visual'
        )

        # Clean up screenshot
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

        # Send feedback
        header = "## Portfolio Feedback - Visual Analysis\n\n"
        if len(feedback) <= 1900:
            await message.reply(f"{header}{feedback}")
        else:
            chunks = [feedback[i:i+1800] for i in range(0, len(feedback), 1800)]
            await message.reply(f"{header}{chunks[0]}")
            for i, chunk in enumerate(chunks[1:], 2):
                await message.channel.send(f"**(Part {i})**\n\n{chunk}")

        await message.add_reaction('✅')

    except Exception as e:
        await message.reply(f'❌ Error processing URL: {str(e)}')
        print(f"Error details: {e}")


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} server(s)')
    print('Ready to review portfolios and resumes!')


@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Check for PDF attachments
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith('.pdf'):
                await process_pdf(attachment, message)
                return

    # Check for URLs in message content
    urls = extract_urls_from_message(message.content)
    if urls:
        for url in urls:
            await process_url(url, message)
        return

    await bot.process_commands(message)


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Bot is alive and ready to review portfolios and resumes.')


@bot.command(name='guide')
async def help_command(ctx):
    help_text = """
**UX Portfolio & Resume Feedback Bot**

I automatically detect whether you're sharing a resume or portfolio and provide tailored feedback!

**How to use:**
📄 **Resume**: Upload a PDF - I'll evaluate it against entry-level UX job requirements
🎨 **Portfolio URL**: Share a link - I'll screenshot it and analyze the visual design & UX process
📁 **Portfolio PDF**: Upload a PDF - I'll analyze the content and structure

**What I look for in Resumes:**
- Relevant UX skills and tools (Figma, research methods, etc.)
- Clear project descriptions showing design process
- Education, certifications, and learning
- Professional formatting and presentation
- Competitive positioning in the job market

**What I look for in Portfolios:**
- Case study structure (problem → process → solution → outcome)
- Visual presentation and polish
- Evidence of UX research and user-centered design
- Measurable outcomes and impact
- Clear contributions and storytelling
- Accessibility and responsive design

**Tips for best results:**
✓ Resumes: Export as text-based PDF (not just images)
✓ Portfolio PDFs: Include readable text with case studies
✓ Portfolio URLs: Share your live portfolio website
✓ Include 2-4 strong projects rather than many shallow ones

**Commands:**
- `!ping` - Check if bot is online
- `!guide` - Show this message

**Note**: I'm designed to help UX/design students entering a competitive, AI-affected job market. Feedback is supportive but honest!
"""
    await ctx.send(help_text)


# Run bot
bot.run(TOKEN)
