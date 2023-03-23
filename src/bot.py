import os
import io
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from rsrch import push_papers

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.name != "rsrch":
        return

    # Redirect stdout to a StringIO object
    original_stdout = sys.stdout
    sys.stdout = captured_stdout = io.StringIO()

    # Call the push_papers function
    # Split the message content into a list of arguments if there are more than one
    if len(message.content.split()) > 1:
        push_papers(message.content.split())
    else:
        push_papers([message.content])

    # Reset stdout to the original value
    sys.stdout = original_stdout

    # Get the captured output and send it to the channel
    output = captured_stdout.getvalue()
    if output:
        await message.channel.send(f"```\n{output}\n```")
    else:
        await message.channel.send("No output was captured.")

    await bot.process_commands(message)


bot.run(os.getenv("DISCORD_BOT_TOKEN"))
