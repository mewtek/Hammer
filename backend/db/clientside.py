"""Backend communication between Hammmer and the PostgreSQL database."""

import asyncpg
from datetime import datetime
from backend.util import add_time
import os

PSQL_INFO = {
    'host': os.getenv('PSQL_ADDR'),
    'port': os.getenv('PSQL_PORT'),
    'database': os.getenv('PSQL_DB'),
    'user': os.getenv('PSQL_USER'),
    'password': os.getenv('PSQL_PASSWD')
}

async def add_guild(guild_id: int, guild_name: str):
    """
    Creates an entry for a Discord server, as well as an entry for its settings.
    Typically ran when the bot joins a new server.

    Args:
        guild_id (int): ID of the Discord server
        guild_name (str): Name of the Discord server
    """

    db = await asyncpg.connect(**PSQL_INFO)

    # asyncpg throws an error if the server is aleady in the database
    existing_guild = await db.fetchrow('''SELECT * FROM guild WHERE guild_id = $1''', guild_id)
    if existing_guild is not None:
        db.close()
        return
    
    await db.execute('''INSERT INTO guild(guild_id, guild_name) VALUES($1, $2)''',
                    guild_id, guild_name)
    
    await db.execute('''INSERT INTO guild_settings(id) VALUES($1)''', guild_id)

    await db.close()

    print(f"Successfully added {guild_name} ({guild_id}) to database")


async def remove_guild(guild_id: int):
    """
    Purges entries containing the server's id.

    Args:
        guild_id (int): The ID of the server the bot left.
    """

    db = await asyncpg.connect(**PSQL_INFO)

    await db.execute("DELETE FROM ban WHERE issued_guild = $1", guild_id)
    await db.execute("DELETE FROM kick WHERE issued_guild = $1", guild_id)
    await db.execute("DELETE FROM mute WHERE issued_guild = $1", guild_id)
    await db.execute("DELETE FROM \"warning\" WHERE issued_guild = $1", guild_id)


async def is_guild_banned(guild_id: int) -> bool:
    """
    Checks to see if a server is banned in the database.

    Args:
        guild_id (int): The ID of the server in question.

    Returns:
        bool: Whether or not the server is banned
    """

    db = await asyncpg.connect(**PSQL_INFO)

    ban_check = await db.fetchval("SELECT banned FROM guild WHERE guild_id = $1", guild_id)
    
    return ban_check


async def get_guild_settings(guild_id: int) -> dict:
    """
    Gets the settings for a server.

    Args:
        guild_id (int): The ID of the server.

    Returns:
        dict: The server's settings.
    """

    db = await asyncpg.connect(**PSQL_INFO)
    settings = await db.fetch("SELECT * FROM guild_settings WHERE id = $1", guild_id)
    await db.close()

    return dict(settings)

async def add_user(user_id: int, username: str):
    """
    Adds a user to the user table. Should be ran on issuance of an administrative command (ban, kick, etc.) 

    Args:
        user_id (int): ID of the user
        username (str): The user's username
    """

    db = await asyncpg.connect(**PSQL_INFO)

    # asyncpg throws an error if the user is already in the database
    existing_user = await db.fetchrow('''SELECT * FROM "user" WHERE user_id = $1''', user_id)
    if existing_user is not None:
        await db.close()
        return
    
    await db.execute('''INSERT INTO "user"(user_id, username) VALUES($1, $2)''', user_id, username)

    await db.close()

    print(f"Added user {user_id} to database.")


async def add_warning(reason: str, issued_by: int, issued_to: int, guild_id: int) -> int:
    """
    Adds an issued warning to the database

    Args:
        reason (str): Reason for the warning being issued
        issued_by (int): ID of the user that issued the warning
        issued_to (int): ID of the user that was warned
        guild_id (int): ID of the Discord server that the warning was issued in

    Returns:
        int: The ID of the issued warning
    """

    db = await asyncpg.connect(**PSQL_INFO)
    time_issued = datetime.utcnow()
    
    await db.execute('''INSERT INTO "warning"(issued, reason, issued_by, issued_to, issued_guild) VALUES($1, $2, $3, $4, $5)''',
                     time_issued, reason, issued_by, issued_to, guild_id)


    id = await db.fetchval('''SELECT id FROM "warning" WHERE reason = $1 AND issued_by = $2 AND issued_to = $3 AND issued_guild = $4''',
                            reason, issued_by, issued_to, guild_id)
    
    await db.close()
    
    return id


async def remove_warning(warning_id: int, guild_id: int) -> bool:
    """
    Removes a warning based on the ID of the entry.

    Args:
        warning_id (int): The in-database ID of the entry
        guild_id (int): The ID of the server the command originated from

    Returns:
        bool: True or False depending on whether or not the removal was successful.
    """

    db = await asyncpg.connect(**PSQL_INFO)

    # Server admins shouldn't be able to remove warnings belonging to other servers
    entry_guild_id = await db.fetchval('''SELECT issued_guild FROM "warning" WHERE id = $1''', warning_id)
    if entry_guild_id != guild_id:
        db.close()
        return False
    
    await db.execute('''DELETE FROM "warning" WHERE id = $1''', warning_id)
    await db.close()

    return True


async def is_user_muted(user_id: int, guild_id: int) -> bool:
    """
    Checks if a user is muted in the database.

    Args:
        user_id (int): The ID of the user in question
        guild_id (int): The ID of the server in question

    Returns:
        bool: Whether or not the user is muted.
    """

    db = await asyncpg.connect(**PSQL_INFO)
    row = await db.fetchrow("SELECT * FROM mute WHERE issued_to = $1 AND issued_guild = $2",
                      user_id, guild_id)
    await db.close()

    if row is None:
        return False
    
    return True


async def add_mute(issued_by: int, issued_to: int, guild_id: int, expiration: str):
    """
    Adds a mute to the database.

    Args:
        issued_by (int): The ID of the user that issued the mute
        issued_to (int): The ID of the user the mute was issued to
        guild_id (int): The ID of the server the mute was issued in
        expiration (str): The amount of time the mute is valid for
    """
    
    time_issued = datetime.utcnow()
    expiration_time = add_time(time_issued, expiration)
    db = await asyncpg.connect(**PSQL_INFO)

    if (await is_user_muted(issued_to, guild_id)):
        return

    await db.execute('''INSERT INTO mute(issued, issued_by, issued_to, issued_guild, expiration)
                        VALUES($1, $2, $3, $4, $5)''', time_issued, issued_by, issued_to, guild_id, 
                        expiration_time)
    
    await db.close()


async def remove_mute(issued_to: int, guild_id: int) -> bool:
    """
    Removes a mute from the database.

    Args:
        issued_to (int): The ID of the user the mute was issued to
        guild_id (int): The ID of the server the command originated from
    
    Returns:
        bool: True or False depending on whether or not the removal was successful
    """

    db = await asyncpg.connect(**PSQL_INFO)

    if (await is_user_muted(issued_to, guild_id) == False):
        await db.close()
        return False

    id = await db.fetchval("SELECT id FROM mute WHERE issued_to = $1 AND issued_guild = $2",
                            issued_to, guild_id)
    
    await db.execute("DELETE FROM mute WHERE id = $1", id)
    await db.close()

    return True

    
async def set_muted_role(role_id: int, guild_id: int):
    """
    Sets the muted role for a server in the guild_settings table

    Args:
        role_id (int): The ID of the muted role in the server
        guild_id (int): The ID of the server in question
    """
    
    db = await asyncpg.connect(**PSQL_INFO)

    await db.execute("UPDATE guild_settings SET muted_role_id = $1 WHERE id = $2",
                     role_id, guild_id)
    
    await db.close()


async def get_muted_role_id(guild_id: int) -> int:
    """
    Grabs the muted role id for a server.

    Args:
        guild_id (int): The ID of the server

    Returns:
        int: The muted role ID
    """

    db = await asyncpg.connect(**PSQL_INFO)
    role_id = await db.fetchval(
        "SELECT muted_role_id FROM guild_settings WHERE id = $1",
        guild_id
    )
    
    await db.close()

    if role_id is None:
        return 0

    return role_id


async def is_user_banned(user_id: int, guild_id: int) -> bool:
    """
    Checks whether or not a user is banned in a server.

    Args:
        user_id (int): The ID of the user in question
        guild_id (int): The ID of the server they should be banned in

    Returns:
        bool: Whether or not the user is banned from the server
    """

    db = await asyncpg.connect(**PSQL_INFO)
    row = await db.fetchrow("SELECT * FROM ban WHERE issued_to = $1 AND issued_guild = $2",
                            user_id, guild_id)
    await db.close()

    if row is None:
        return False
    
    return True

async def add_ban(issued_by: int, issued_to: int, guild_id: int, reason: str = None, expiration: str = None):
    """
    Adds a server ban to the database.

    Args:
        issued_by (int): The ID of the user that issued the ban
        issued_to (int): The ID of the user the ban was issued to
        guild_id (int): The ID of the server the ban was issued in
        reason (str, optional): The reason for the ban. Defaults to None.
        expiration (str, optional): The amount of the time the ban is valid for. Defaults to None.
    """

    time_issued = datetime.utcnow()
    db = await asyncpg.connect(**PSQL_INFO)

    # A user should only be banned once per server
    if (await is_user_banned(issued_to, guild_id)):
        await db.close()
        return

    await db.execute('''INSERT INTO ban(issued, issued_by, issued_to, issued_guild) VALUES($1, $2, $3, $4)''',
                     time_issued, issued_by, issued_to, guild_id)
    
    if reason is not None:
        id = db.fetchval('''SELECT id FROM ban WHERE issued_by = $1 AND issued_to = $2 AND issued_guild = $3''',
                         issued_by, issued_to, guild_id)    
        await db.execute('''UPDATE ban SET reason = $1 WHERE id = $2''', reason, id)

    if expiration is not None:
        id = db.fetchval('''SELECT id FROM ban WHERE issued_by = $1 AND issued_to = $2 AND issued_guild = $3''',
                         issued_by, issued_to, guild_id)   
        expiration_timestamp = add_time(time_issued, expiration)
        await db.execute("UPDATE ban SET expiration = $1 WHERE id = $2", expiration_timestamp, id)

    await db.close()
    print(f"{issued_to} was banned from {guild_id}")


async def remove_ban(user_id: int, guild_id: int) -> bool:
    """
    Removes the ban on a user in a specific guild.

    Args:
        user_id (int): The ID of the user to be unbanned.
        guild_id (int): The ID of the server that the command was issued in.

    Returns:
        bool: True or False depending on whether or not the removal was successful.
    """

    db = await asyncpg.connect(**PSQL_INFO)

    # asyncpg will throw an error if the ban doesn't exist.
    if (await is_user_banned(user_id, guild_id) == False):
        await db.close()
        return False
    
    await db.execute("DELETE FROM ban WHERE issued_to = $1 AND issued_guild = $2", user_id, guild_id)
    await db.close()

    print(f"{user_id} was unbanned from {guild_id}.")

    return True


async def log_kick(issued_by: int, issued_to: int, guild_id: int, reason: str = None):
    """
    Logs someone being kicked from a server.

    Args:
        issued_by (int): The ID of the user that kicked a user
        issued_to (int): The ID of the user that was kicked
        guild_id (int): The ID of the server the kick was issued in
        reason (str, optional): The reason for the kick. Defaults to None. 
    """

    time_issued = datetime.utcnow()
    db = await asyncpg.connect(**PSQL_INFO)

    await db.execute('''INSERT INTO kick(issued, issued_by, issued_to, issued_guild)
                    VALUES($1, $2, $3, $4)''', time_issued, issued_by, issued_to, guild_id)
    
    if reason is not None:
        id = await db.fetchval('''SELECT id FROM kick WHERE
                               issued_by = $1 AND issued_to = $2 AND issued_guild = $3''',
                               issued_by, issued_to, guild_id)
        await db.execute("UPDATE kick SET reason = $1 WHERE id = $2", reason, id)

    await db.close()


async def get_running_bans() -> list:
    """
    Gets the currently expirable bans. Ignores any bans
    that have the default value.

    Returns:
        list: asyncpg record objects, can be converted into dictionaries.
    """

    db = await asyncpg.connect(**PSQL_INFO)

    bans = await db.fetch("SELECT * FROM ban WHERE expiration != '2269-01-01 00:00:00'::timestamp without time zone")

    return bans


async def get_mutes() -> list:
    """
    Gets all current mutes.

    Returns:
        list: asyncpg record objects, can be converted into dictionaries.
    """

    db = await asyncpg.connect(**PSQL_INFO)

    mutes = await db.fetch("SELECT * from mute")

    return mutes


async def get_guild_settings(guild_id: int) -> dict:
    """
    Gets the settings for a server in the database.

    Args:
        guild_id (int): The ID of the Discord server

    Returns:
        dict: The settings of the server.
    """

    db = await asyncpg.connect(**PSQL_INFO)

    settings = await db.fetchrow("SELECT * FROM guild_settings WHERE id = $1", guild_id)
    await db.close()

    return dict(settings)