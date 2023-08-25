import discord
import backend.db.clientside
from discord.ext import commands


class Configuration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def config(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            pass


    @config.command()
    async def enable(self, ctx: commands.Context, setting: str):
        pass


    @config.command()
    async def disable(self, ctx: commands.Context, setting: str):
        pass


    @config.command()
    async def set(self, ctx: commands.Context, setting: str):
        pass



async def setup(bot):
    await bot.add_cog(Configuration(bot))