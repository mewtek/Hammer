""" Functions for handling ModMail tickets on the database-side. """
import asyncio
import asyncpg
from backend.db.clientside import PSQL_INFO
from backend.db.clientside import get_guild_settings

async def create_ticket(guild_id: int, user_id: int, channel: int) -> int:
    """
    Creates a new ModMail ticket in the database.

    Args:
        guild_id (int): The ID of the guild the ticket is being created in
        user_id (int): The ID of the user who is opening the ticket
        channel (int): The ID of the channel that was created to handle the ticket

    Returns:
        int: The ID of the newly created ticket.
    """

    db = await asyncpg.connect(**PSQL_INFO)
    await db.execute('''INSERT INTO ticket(ticket_guild, ticket_channel_id, user)
                     VALUES($1, $2, $3)''', guild_id, channel, user_id)
    
    id = db.fetchval('''SELECT id FROM ticket WHERE
                     ticket_guild = $1 AND ticket_channel_id = $2 AND user = $3''',
                     guild_id, channel, user_id)
    
    await db.close()
    return id


async def accept_ticket(ticket_id: int, claimaint_id: int):
    """
    Sets a claimaint to anyone who accepts the ticket.

    Args:
        ticket_id (int): The ID of the ticket
        claimaint_id (int): The ID of the user that accepted the ticket
    """

    db = await asyncpg.connect(**PSQL_INFO)
    await db.execute("UPDATE ticket SET claimant = $1 WHERE id = $2", claimaint_id, ticket_id)

    await db.close()