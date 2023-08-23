import os
import discord
import asyncio
import logging
import backend.db
from discord.ext import commands
from dotenv import load_dotenv

discord.utils.setup_logging(level=logging.INFO, root=False)

# Get environment variables
if ".env" in os.listdir('.'):
    load_dotenv()
    
token = os.getenv('BOT_TOKEN')

intents = discord.Intents(
    messages = True,
    message_content = True,
    guilds = True,
    members = True,
    bans = True
)
client = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(token)

asyncio.run(main())