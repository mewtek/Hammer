"""Backend communication between Hammmer and the PostgreSQL database."""

import asyncio
import asyncpg
from datetime import datetime
import os

psql_server_addr = "postgresql://{0}@{1}:{2}/{3}".format(
        os.getenv("PSQL_USER"),
        os.getenv("PSQL_ADDR"), os.getenv("PSQL_PORT"),
        os.getenv("PSQL_DB")
)

psql_password = os.getenv("PSQL_PASSWD")

async def add_guild_to_database(guild_id: int, guild_name: str):
    """
    Creates an entry for a Discord server, as well as an entry for its settings.
    Typically ran when the bot joins a new server.

    Args:
        guild_id (int): ID of the Discord server
        guild_name (str): Name of the Discord server
    """

    db = await asyncpg.connect(psql_server_addr, password=psql_password)

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

    # TODO: Check if the user is already in the database.

    db = await asyncpg.connect(psql_server_addr, password=psql_password)

    await db.execute('''INSERT INTO "user"(user_id, username) VALUES($1, $2)''', user_id, username)

    await db.close()

    print(f"Added user {user_id} to database.")


async def add_warning(reason: str, issued_by: int, issued_to: int, guild_id: int):
    """
    Adds an issued warning to the database

    Args:
        reason (str): Reason for the warning being issued
        issued_by (int): ID of the user that issued the warning
        issued_to (int): ID of the user that was warned
        guild_id (int): ID of the Discord server that the warning was issued in
    """

    db = await asyncpg.connect(psql_server_addr, password=psql_password)
    time_issued = datetime.utcnow()
    
    await db.execute('''INSERT INTO "warning"(issued, reason, issued_by, issued_to, issued_guild) VALUES($1, $2, $3, $4, $5)''',
                     time_issued, reason, issued_by, issued_to, guild_id)


    id = await db.cursor().fetch('''SELECT id FROM "warning" WHERE issued = $1 AND reason = $2 AND issued_by = $3 AND issued_to = $4 AND issued_guild = $5''',
                          time_issued, reason, issued_by, issued_to, guild_id)

    await db.close()
    print(id)
