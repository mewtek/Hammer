import backend.db
import discord

from discord.ext import commands

class Listeners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined server {guild.name} (ID {guild.id})")
        await backend.db.add_guild_to_database(guild.id, guild.name)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        user = message.author

        if user.id == self.bot.user.id:
            return
        
        await backend.db.add_user_to_database(user.id, user.name)

async def setup(bot):
    await bot.add_cog(Listeners(bot))