import discord
import backend.db
from discord.ext import commands, tasks
from datetime import datetime

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_ban_expirations.start()
        self.check_mute_expirations.start()

    @tasks.loop(seconds=30.0)
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


    @tasks.loop(seconds=30.0)
    async def check_mute_expirations(self):
        mutes = await backend.db.get_mutes()

        for mute in mutes:
            mute = dict(mute)
            time_since_mute = datetime.utcnow() - mute['expiration']

            if time_since_mute.total_seconds() >= 0:
                guild = await self.bot.fetch_guild(mute['issued_guild'])
                member = guild.get_member(mute['issued_to'])

                if member is None:
                    await backend.db.remove_mute(member.id, guild.id)
                    return
                
                muted_role_id = await backend.db.get_muted_role_id(guild.id)
                muted_role = guild.get_role(muted_role_id)

                await member.remove_roles(muted_role, reason="Mute period expired.")
                await backend.db.remove_mute(member.id, guild.id)


async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))