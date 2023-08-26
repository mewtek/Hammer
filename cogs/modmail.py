import discord
from discord.ext import commands

class ModMail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def create_new_channel(self, category: discord.CategoryChannel):
        pass


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass    # TODO


    @commands.command()
    async def accept(self, ctx: commands.Context):
        pass

    
    @commands.command()
    async def close(self, ctx: commands.Context):
        pass


async def setup(bot):
    await bot.add_cog(ModMail(bot))