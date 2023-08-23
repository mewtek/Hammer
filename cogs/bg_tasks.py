import discord
from discord.ext import commands

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot):
    bot.add_cog(BackgroundTasks(bot))