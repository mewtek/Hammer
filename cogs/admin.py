import backend.db
import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def warn(self, ctx: commands.Context, user: discord.Member, reason: str):
        issued_by = ctx.message.author.id
        issued_to = user.id
        guild_id = ctx.message.guild.id
        
        warning = await backend.db.add_warning(reason, issued_by, issued_to, guild_id)

        await ctx.reply(f"Warned {user.mention} -- ID #{warning}")


async def setup(bot):
    await bot.add_cog(Admin(bot))