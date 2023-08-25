""" Functions for sending messages to users upon action being taken upon them """
import discord
import backend.db.clientside
from discord.ext import commands
from enum import Enum

class MessageType(Enum):
    BAN = 0
    KICK = 1
    MUTE = 2
    WARN = 3
    BANNED_FROM_BOT = 4

async def test(user: discord.User):
    await user.send("HELP")


async def send_action_message(messageType: MessageType, bot: commands.Bot, user_id: int, guild_id: int,
                            issued_by_id: int = None, length: str = None, reason: str = None):
    """
    Sends a user a direct message upon action being taken
    against them.

    Args:
        messageType (MessageType): Enum value of the type of action being taken
        bot (commands.Bot): Bot instance
        user (discord.User): The user to message
        guild (discord.Guild): The guild the action was taken from.
        issued_by (discord.User, optional): The user that issued the action. Defaults to None.
        length (str, optional): The amount of time the action is valid for. Defaults to None.
        reason (str, optional): The reason for the action taking place.
    """
    user = await bot.fetch_user(user_id)
    guild = await bot.fetch_guild(guild_id)

    if messageType == MessageType.BANNED_FROM_BOT:
        await user.send(f'''### Your guild \"{guild.name}\" has been banned from using Hammer.\n
                        All data, including mutes, bans, kicks, and warnings have been wiped from the bot's database
                        and will no longer be stored. If you attempt to re-add the bot, it will immediately leave and not store
                        any logs pertaining to your server.\n
                        If you believe this to be a mistake, you can open a ticket in our [support server](https://discord.com).''')
        return
    
    settings = await backend.db.clientside.get_guild_settings(guild.id)

    if not settings['dm_users_on_action']:
        return
    
    if messageType == MessageType.BAN:
        issued_by = await bot.fetch_user(issued_by_id)
        embed = discord.Embed(title=f"Banned from {guild.name}", color=0xfe3939)
        embed.add_field(name="Banned by:", value=issued_by.name)
        embed.add_field(name="Reason:", value="Not Stated" if reason is None else reason)
        embed.add_field(name="Length:", value="Permanent" if length is None else length)
        embed.set_footer(text="This message is automated. Please do not contact bot support to be unbanned from this server.")

        await user.send(embed=embed)

    elif messageType == MessageType.KICK:
        issued_by = await bot.fetch_user(issued_by_id)
        embed = discord.Embed(title=f"Kicked from {guild.name}", color=0xfeac39)
        embed.add_field(name="Kicked by:", value=issued_by.name)
        embed.add_field(name="Reason:", value="Not Stated" if reason is None else reason)
        embed.add_field(name="Length:", value="Permanent" if length is None else length)
        embed.set_footer(text="This message is automated.")

        await user.send(embed=embed)

    elif messageType == MessageType.MUTE:
        issued_by = await bot.fetch_user(issued_by_id)
        embed = discord.Embed(title=f"Muted in {guild.name}", color=0xfeac39)
        embed.add_field(name="Muted by:", value=issued_by.name)
        embed.add_field(name="Length:", value=length)
        embed.set_footer(text="This message is automated. Please do not contact bot support to be unmuted in this server.")

        await user.send(embed=embed)

    elif messageType == MessageType.WARN:
        embed = discord.Embed(title=f"Warned in {guild.name}", color=0xfef739)
        embed.add_field(name="Reason:", value="Not Stated" if reason is None else reason)
        embed.set_footer(text="This message is automated.")

        await user.send(embed=embed)
