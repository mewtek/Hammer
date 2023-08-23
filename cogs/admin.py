import backend.db
import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    @commands.command()
    async def warn(self, ctx: commands.Context, user: discord.Member, reason: str):
        issued_by = ctx.message.author.id
        issued_to = user.id
        guild_id = ctx.message.guild.id
        
        warning = await backend.db.add_warning(reason, issued_by, issued_to, guild_id)

        await ctx.reply(f"Warned {user.mention} -- ID #{warning}")


    @commands.command()
    async def unwarn(self, ctx: commands.Context, warning_id: int):
        guild_id = ctx.message.guild.id

        process = await backend.db.remove_warning(warning_id, guild_id)

        if process == False:
            await ctx.reply(f"Failed to delete warning #{warning_id}.")
            return

        await ctx.reply(f"Successfully removed warning #{warning_id}!")


    @commands.command()
    async def kick(self, ctx: commands.Context, user: discord.Member, reason: str = None):
        if reason is None:
            await user.kick(f"KICKED BY {ctx.author.id} -- No reason was provided.")
        else:
            await user.kick(f"KICKED BY {ctx.author.id} -- {reason}")

        await ctx.message.add_reaction(u"\u2705")
    

    @commands.command()
    async def ban(self, ctx: commands.Context, user: discord.Member, reason: str = None):
        issued_by = ctx.message.author
        issued_to = user.id
        guild_id = ctx.message.guild.id

        await backend.db.add_ban(issued_by, issued_to, guild_id, reason)
        
        if reason is None:
            await user.ban(reason = f"Banned by {issued_by} -- No reason was provided.")
        else:
            await user.ban(reason = f"Banned by {issued_by} -- {reason}")

        await ctx.message.add_reaction(u"\u2705")


    @commands.command()
    async def unban(self, ctx: commands.Context, user_id: int):
        user = self.bot.get_user(user_id)
        process = await backend.db.remove_ban(user_id, ctx.message.guild.id)

        if process == False:
            ctx.reply(f"{user.name} is not banned!")
            return
        
        await ctx.message.guild.unban(user)
        await ctx.message.add_reaction(u"\u2705")

async def setup(bot):
    await bot.add_cog(Admin(bot))