""" Database queries and functions for the owner of the bot """
import asyncpg
from backend.db.clientside import PSQL_INFO


async def add_banned_guild(guild_id: int):
    """
    Sets a server's "banned" value in the database to true.

    Args:
        guild_id (int): The ID of the server that is getting banned
        purge_guild (bool, optional): Whether or not to purge the server from the database. Defaults to False.

    Returns:
        bool: Whether or not the ban was successful.
    """

    db = await asyncpg.connect(**PSQL_INFO)

    await db.execute("UPDATE guild SET banned = true WHERE guild_id = $1", guild_id)
    await db.close()

    print(f"{guild_id} was banned from using the bot.")
