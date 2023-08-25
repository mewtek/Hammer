import discord
import backend.db_admin
from discord.ext import commands


class BotOwner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        print("Shutting down the bot..")
        await self.bot.close()


    @commands.command()
    @commands.is_owner()
    async def ban_guild(self, ctx: commands.Context, guild_id: int):
        try:
            guild = await self.bot.fetch_guild(guild_id)

            if guild is None:
                await ctx.reply("Guild does not exist.")
                return
            
            await backend.db_admin.add_banned_guild(guild_id)

            if guild.name in self.bot.guilds:
                await guild.leave()

            await ctx.message.add_reaction(u"\u2705")

        except discord.errors.NotFound:
            await ctx.reply("Guild not found.")


async def setup(bot):
    await bot.add_cog(BotOwner(bot))
