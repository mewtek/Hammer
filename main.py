import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


# Get .env variables
load_dotenv()
token = os.getenv('BOT_TOKEN')

# Set bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guild_messages = True


# Bot setup
client = commands.Bot(command_prefix="h!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}..")


@client.command()
async def hello(ctx: commands.Context):
    await ctx.send("Hello, World!")

@client.command()
async def shutdown(ctx: commands.Context):
    await ctx.send("Shutting down..")
    print(f"Bot shut down by {ctx.message.author.id}..")
    await client.close()


client.run(token=token)