""" Functions for logging actions not covered by discord.py """

import discord
import calendar
from math import floor
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

    embed=discord.Embed(title=f"User was kicked.", description=f"Kicked <t:{timestamp}:R>", color=0xfcba03)
    embed.set_author(name=issued_to.name, icon_url=issued_to.avatar.url)
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

    embed=discord.Embed(title=f"User was muted.", description=f"Muted <t:{timestamp}:R>", color=0xfcba03)
    embed.set_author(name=issued_to.name, icon_url=issued_to.avatar.url)
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

    embed=discord.Embed(title=f"User was warned.", description=f"Warned <t:{timestamp}:R>", color=0xfcba03)
    embed.set_author(name=issued_to.name, icon_url=issued_to.avatar.url)
    embed.add_field(name="Warned by", value=issued_by.name, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)

    await log_channel.send(embed=embed)


async def log_user_join(bot: commands.Bot, user: discord.Member):
    settings = await get_guild_settings(user.guild.id)

    if not settings['logging']:
        return
    
    acc_created_timestamp = floor(datetime.timestamp(user.created_at))
    joined_timestamp = floor(datetime.timestamp(user.joined_at))
    log_channel = bot.get_channel(settings['log_channel'])
    
    embed = discord.Embed(title=f"New member: {user.name}" if not user.bot else f"New Bot: {user.name} \U0001F916",
                          color=user.color)
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="Account Created", value=f"<t:{acc_created_timestamp}:R>", inline=False)
    embed.add_field(name="Joined", value=f"<t:{joined_timestamp}:R>", inline=False)

    await log_channel.send(embed=embed)