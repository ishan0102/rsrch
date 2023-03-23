import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from rsrch import push_papers

load_dotenv()

# Create intents to allow for message content
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Login sequence
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


# Push papers to Notion
@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.name != "rsrch":
        return

    push_papers([message.content])
    await bot.process_commands(message)


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
