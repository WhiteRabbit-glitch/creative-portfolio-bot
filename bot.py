import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import PyPDF2
import anthropic

# Load secrets
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

# Initialize clients
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# Feedback prompt for UX portfolios
PORTFOLIO_PROMPT = """You are a UX portfolio reviewer for university students entering a competitive job market affected by AI disruption.

Review this portfolio and provide constructive feedback in these areas:

1. **Case Study Structure**: Are problems clearly defined? Is the design process visible?
2. **Visual Presentation**: Based on described content, does it seem professional and polished?
3. **Outcomes & Impact**: Are results quantified? Is business/user impact clear?
4. **Storytelling**: Does it show thinking and process, not just deliverables?
5. **Standout Strengths**: What's working well that they should emphasize?
6. **Priority Improvements**: Top 3 changes that would strengthen this portfolio most

Tone: Supportive but honest. These are anxious students who need actionable, specific advice.
Format: Use clear sections with bullet points. Be encouraging while being real about what needs work.
Length: 400-600 words.

Portfolio content:
{portfolio_text}"""

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

async def get_claude_feedback(portfolio_text):
    """Get feedback from Claude API"""
    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user", 
                    "content": PORTFOLIO_PROMPT.format(portfolio_text=portfolio_text)
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error getting feedback: {str(e)}"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} server(s)')
    print('Ready to review portfolios!')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Check for PDF attachments
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith('.pdf'):
                # React to show we're processing
                await message.add_reaction('👀')
                
                try:
                    # Download PDF
                    pdf_bytes = await attachment.read()
                    temp_path = f"temp_{attachment.filename}"
                    
                    with open(temp_path, 'wb') as f:
                        f.write(pdf_bytes)
                    
                    # Update reaction to show we're working
                    await message.add_reaction('⚙️')
                    
                    # Extract text
                    portfolio_text = extract_pdf_text(temp_path)
                    
                    # Clean up temp file
                    os.remove(temp_path)
                    
                    # Check if we got text
                    if len(portfolio_text) < 100:
                        await message.reply("⚠️ This PDF seems to be mostly images or very short. I need text content to review. Try exporting your portfolio as a PDF with text, not just screenshots.")
                        return
                    
                    # Get AI feedback
                    await message.add_reaction('🤔')
                    feedback = await get_claude_feedback(portfolio_text[:15000])  # Limit to ~15k chars to control costs
                    
                    # Send feedback in chunks if needed (Discord has 2000 char limit)
                    if len(feedback) <= 2000:
                        await message.reply(f"## Portfolio Feedback\n\n{feedback}")
                    else:
                        # Split into chunks
                        chunks = [feedback[i:i+1900] for i in range(0, len(feedback), 1900)]
                        await message.reply(f"## Portfolio Feedback (Part 1)\n\n{chunks[0]}")
                        for i, chunk in enumerate(chunks[1:], 2):
                            await message.channel.send(f"**(Part {i})**\n\n{chunk}")
                    
                    # Success reaction
                    await message.add_reaction('✅')
                    
                except Exception as e:
                    await message.reply(f'❌ Error processing portfolio: {str(e)}')
                    print(f"Error details: {e}")
    
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Bot is alive and ready to review portfolios.')

@bot.command(name='guide')
async def help_command(ctx):
    help_text = """
**UX Portfolio Feedback Bot**

Upload a PDF of your portfolio and I'll provide detailed feedback!

**What I look for:**
- Case study structure and clarity
- Visual presentation quality
- Demonstrated impact and outcomes
- Process and thinking (not just deliverables)
- Areas for improvement

**Tips for best results:**
- Export portfolio as text-based PDF (not just images)
- Include 2-3 case studies minimum
- Make sure text is readable/selectable

**Commands:**
- `!ping` - Check if bot is online
- `!guide` - Show this message
"""
    await ctx.send(help_text)

# Run bot
bot.run(TOKEN)