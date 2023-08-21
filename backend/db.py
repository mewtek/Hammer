import asyncio
import asyncpg
import os

psql_server_addr = "postgresql://{0}@{1}:{2}/{3}".format(
        os.getenv("PSQL_USER"),
        os.getenv("PSQL_ADDR"), os.getenv("PSQL_PORT"),
        os.getenv("PSQL_DB")
)

psql_password = os.getenv("PSQL_PASSWORD")

async def add_guild_to_database(guild_id: int, guild_name: str):
    """ Add a recently joined guild to the database. Should be ran upon server join. """

    db = await asyncpg.connect(psql_server_addr, password=os.getenv("PSQL_PASSWD"))

    await db.execute('''INSERT INTO guild(guild_id, guild_name) VALUES($1, $2)''',
                    guild_id, guild_name)
    
    await db.execute('''INSERT INTO guild_settings(id) VALUES($1)''', guild_id)

    await db.close()

    print(f"Successfully added {guild_name} ({guild_id}) to database")