import os
import discord
import backend.db
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
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}..")

@client.event
async def on_guild_join(guild: discord.Guild):
    print(f"Joined new guild {guild.id}.")
    await backend.db.add_guild_to_database(guild.id, guild.name)


@client.command()
async def hello(ctx: commands.Context):
    await ctx.send("Hello, World!")

@client.command()
async def shutdown(ctx: commands.Context):
    await ctx.send("Shutting down..")
    print(f"Bot shut down by {ctx.message.author.id}..")
    await client.close()

@client.command()
async def test_warning(ctx: commands.Context):
    reason = "This is a test warning"
    user_id = ctx.message.author.id
    guild_id = ctx.message.guild.id

    # await backend.db.add_user_to_database(user_id, ctx.message.author.global_name)
    await backend.db.add_warning(reason, user_id, user_id, guild_id)

    await ctx.reply(f"Code ran successfully!")

@client.command()
async def force_guild_into_db(ctx: commands.Context):
    await backend.db.add_guild_to_database(ctx.guild.id, ctx.guild.name)
    ctx.reply("Successfully added guild to database.")

client.run(token=token)