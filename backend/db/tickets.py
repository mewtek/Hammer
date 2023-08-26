""" Functions for handling ModMail tickets on the database-side. """
import asyncio
import asyncpg
from backend.db.clientside import PSQL_INFO

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


async def accept_ticket(ticket_id: int, claimed_by_id: int):
    """
    Sets claimed_by to anyone who accepts the ticket.

    Args:
        ticket_id (int): The ID of the ticket
        claimed_by_id (int): The ID of the user that accepted the ticket
    """

    db = await asyncpg.connect(**PSQL_INFO)
    await db.execute("UPDATE ticket SET claimed_by = $1 WHERE id = $2", claimed_by_id, ticket_id)

    await db.close()