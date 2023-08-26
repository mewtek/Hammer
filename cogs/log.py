import discord
import calendar
from datetime import datetime
from backend.db.clientside import get_guild_settings
from discord.ext import commands

class ServerLogging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        date = datetime.utcnow()
        timestamp = calendar.timegm(date.utctimetuple())
        settings = await get_guild_settings(message.guild.id)
        
        if message.author.id == self.bot.user.id:
            return

        if not settings['logging']:
            return
        
        log_channel = self.bot.get_channel(settings['log_channel'])
        embed=discord.Embed(title=f"Message deleted in #{message.channel.name}", description=f"Deleted <t:{timestamp}:R>", color=0xff3838)
        embed.set_author(name=f"{message.author.name}", icon_url=message.author.avatar.url)
        embed.add_field(name="Content", value=message.content, inline=False)

        await log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        date = datetime.utcnow()
        timestamp = calendar.timegm(date.utctimetuple())
        settings = await get_guild_settings(before.guild.id)

        if before.author.id == self.bot.user.id:
            return

        if not settings['logging']:
            return
        
        log_channel = self.bot.get_channel(settings['log_channel'])
        embed=discord.Embed(title=f"Message edited in #{before.channel.name}", description=f"Edited <t:{timestamp}:R>", color=0xfcba03)
        embed.set_author(name=f"{before.author.name}", icon_url=before.author.avatar.url)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)

        await log_channel.send(embed=embed)

    
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user):
        settings = await get_guild_settings(guild.id)

        if not settings['logging']:
            return
        
        log_channel = self.bot.get_channel(settings['log_channel'])

        await log_channel.send(f"**User {user.name} was banned.**")

    
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        settings = await get_guild_settings(guild.id)

        if not settings['logging']:
            return
        
        log_channel = self.bot.get_channel(settings['log_channel'])

        await log_channel.send(f"**User {user.name} was unbanned.**")


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        date = datetime.utcnow()
        timestamp = calendar.timegm(date.utctimetuple())
        settings = await get_guild_settings(member.guild.id)

        if not settings['logging']:
            return
        
        log_channel = self.bot.get_channel(settings['log_channel'])
        embed=discord.Embed(title=f"{member.name} left the server.", description=f"Left <t:{timestamp}:R>", color=0xfcba03)

        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerLogging(bot))