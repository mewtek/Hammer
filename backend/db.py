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
    """ Add a recently joined guild to the database. Should be ran upon server join. """

    db = await asyncpg.connect(psql_server_addr, password=psql_password)

    await db.execute('''INSERT INTO guild(guild_id, guild_name) VALUES($1, $2)''',
                    guild_id, guild_name)
    
    await db.execute('''INSERT INTO guild_settings(id) VALUES($1)''', guild_id)

    await db.close()

    print(f"Successfully added {guild_name} ({guild_id}) to database")

async def add_user_to_database(user_id: int, username: str):
    """ Adds a user to the user table. Should be ran on issuance of an administrative command (ban, kick, etc.) """

    # TODO: Check if the user is already in the database.

    db = await asyncpg.connect(psql_server_addr, password=psql_password)

    await db.execute('''INSERT INTO "user"(user_id, username) VALUES($1, $2)''', user_id, username)

    await db.close()

    print(f"Added user {user_id} to database.")


async def add_warning(reason: str, issued_by: int, issued_to: int, guild_id: int):


    db = await asyncpg.connect(psql_server_addr, password=psql_password)
    time_issued = datetime.utcnow()
    
    await db.execute('''INSERT INTO "warning"(issued, reason, issued_by, issued_to, issued_guild) VALUES($1, $2, $3, $4, $5)''',
                     time_issued, reason, issued_by, issued_to, guild_id)


    id = await db.cursor().fetch('''SELECT id FROM "warning" WHERE issued = $1 AND reason = $2 AND issued_by = $3 AND issued_to = $4 AND issued_guild = $5''',
                          time_issued, reason, issued_by, issued_to, guild_id)

    await db.close()
    print(id)
