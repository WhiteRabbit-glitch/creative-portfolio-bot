import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with permissions
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready and online
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} server(s)')

# Event: Someone sends a message
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if message has PDF attachment
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.pdf'):
                await message.add_reaction('👀')  # Eye emoji = "I see this"
                await message.reply('Portfolio received! Feedback coming soon...')
    
    # Let commands still work
    await bot.process_commands(message)

# Simple test command
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Bot is alive.')

# Run the bot
bot.run(TOKEN)