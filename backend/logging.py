""" Functions for logging actions not covered by discord.py """

import discord
import calendar
from backend.db.clientside import get_guild_settings
from discord.ext import commands
from datetime import datetime

async def log_kick(bot: commands.Bot, guild: discord.Guild, issued_to: discord.Member, issued_by: discord.Member, reason: str = None):
    date = datetime.utcnow()
    timestamp = calendar.timegm(date.utctimetuple())
    settings = await get_guild_settings(guild.id)

    if not settings['logging']:
        return
    
    log_channel = bot.get_channel(settings['log_channel'])

    embed=discord.Embed(title=f"{issued_to.name} was kicked.", description=f"Kicked <t:{timestamp}:R>", color=0xfcba03)
    embed.add_field(name="Kicked by", value=issued_by.name)
    if reason is not None:
        embed.add_field(name="Reason", value=reason)

    await log_channel.send(embed=embed)


async def log_mute(bot: commands.Bot, guild: discord.Guild, issued_to: discord.Member, issued_by: discord.Member, length: str):
    date = datetime.utcnow()
    timestamp = calendar.timegm(date.utctimetuple())
    settings = await get_guild_settings(guild.id)

    if not settings['logging']:
        return
    
    log_channel = bot.get_channel(settings['log_channel'])

    embed=discord.Embed(title=f"{issued_to.name} was muted.", description=f"Muted <t:{timestamp}:R>", color=0xfcba03)
    embed.add_field(name="Muted by", value=issued_by.name, inline=False)
    embed.add_field(name="Duration", value=length)

    await log_channel.send(embed=embed)



async def log_warn(bot: commands.Bot, guild: discord.Guild, issued_to: discord.Member, issued_by: discord.Member, reason: str):
    date = datetime.utcnow()
    timestamp = calendar.timegm(date.utctimetuple())
    settings = await get_guild_settings(guild.id)

    if not settings['logging']:
        return
    
    log_channel = bot.get_channel(settings['log_channel'])

    embed=discord.Embed(title=f"{issued_to.name} was warned.", description=f"Warned <t:{timestamp}:R>", color=0xfcba03)
    embed.add_field(name="Warned by", value=issued_by.name, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)

    await log_channel.send(embed=embed)