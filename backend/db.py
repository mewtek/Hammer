"""Backend communication between Hammmer and the PostgreSQL database."""

import asyncio
import asyncpg
from datetime import datetime
import os

PSQL_INFO = {
    'host': os.getenv('PSQL_ADDR'),
    'port': os.getenv('PSQL_PORT'),
    'database': os.getenv('PSQL_DB'),
    'user': os.getenv('PSQL_USER'),
    'password': os.getenv('PSQL_PASSWD')
}

async def add_guild_to_database(guild_id: int, guild_name: str):
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

async def add_user_to_database(user_id: int, username: str):
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