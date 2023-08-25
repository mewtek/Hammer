import backend.db.clientside
import discord

from discord.ext import commands

class Listeners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        if await backend.db.clientside.is_guild_banned(guild.id):
            await guild.leave()
            return

        print(f"Joined server {guild.name} (ID {guild.id})")
        await backend.db.clientside.add_guild(guild.id, guild.name)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await backend.db.clientside.remove_guild(guild.id)


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild

        await backend.db.clientside.add_user(member.id, member.name)

        if (await backend.db.clientside.is_user_muted(member.id, guild.id)):
            muted_role_id = await backend.db.clientside.get_muted_role_id(guild.id)
            muted_role = guild.get_role(muted_role_id)

            await member.add_roles(muted_role, reason="User was muted prior to joining the server.")


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        user = message.author

        if user.id == self.bot.user.id:
            return
        
        await backend.db.clientside.add_user(user.id, user.name)
        

async def setup(bot):
    await bot.add_cog(Listeners(bot))