import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import PyPDF2
import io

# Load secrets
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} server(s)')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Check for PDF attachments
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith('.pdf'):
                await message.add_reaction('👀')
                
                # Download and extract text from PDF
                try:
                    # Download the PDF
                    pdf_bytes = await attachment.read()
                    
                    # Save temporarily
                    temp_path = f"temp_{attachment.filename}"
                    with open(temp_path, 'wb') as f:
                        f.write(pdf_bytes)
                    
                    # Extract text (we'll add this next)
                    await message.reply('Portfolio received! Feedback coming soon...')
                    
                except Exception as e:
                    await message.reply(f'Error processing PDF: {str(e)}')
    
    await bot.process_commands(message)