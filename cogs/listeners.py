import backend.db
from discord.ext import commands

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined server {guild.name} (ID {guild.id})")
        await backend.db.add_guild_to_database(guild.id, guild.name)

async def setup(bot):
    await bot.add_cog(Listeners(bot))