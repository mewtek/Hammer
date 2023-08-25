import discord
import backend.db
from discord.ext import commands, tasks
from datetime import datetime

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_ban_expirations.start()

    @tasks.loop(minutes=10.0)
    async def check_ban_expirations(self):
        bans = await backend.db.get_running_bans()

        for ban in bans:
            ban = dict(ban)
            time_since_ban = datetime.utcnow() - ban['expiration']

            if time_since_ban.total_seconds() >= 0:
                guild = await self.bot.fetch_guild(ban['issued_guild'])
                user = await self.bot.fetch_user(ban['issued_to'])

                print(f"{user.name}'s ban expired in {guild.id}")

                await guild.unban(user, reason="Ban period expired.")
                await backend.db.remove_ban(user.id, guild.id)        


async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))