import os
import discord
import backend.db
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Get .env variables
load_dotenv()
token = os.getenv('BOT_TOKEN')

# Set bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guild_messages = True


# Bot setup
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}..")

@client.event
async def on_guild_join(guild: discord.Guild):
    print(f"Joined new guild {guild.id}.")
    await backend.db.add_guild_to_database(guild.id, guild.name)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(token)

asyncio.run(main())