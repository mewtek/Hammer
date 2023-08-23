import backend.db
import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    @commands.command()
    async def warn(self, ctx: commands.Context, user: discord.Member, reason: str):
        issued_by = ctx.message.author.id
        issued_to = user.id
        guild_id = ctx.message.guild.id
        
        warning = await backend.db.add_warning(reason, issued_by, issued_to, guild_id)

        await ctx.reply(f"Warned {user.mention} -- ID #{warning}")


    @commands.command()
    async def unwarn(self, ctx: commands.Context, warning_id: int):
        guild_id = ctx.message.guild.id

        process = await backend.db.remove_warning(warning_id, guild_id)

        if process == False:
            await ctx.reply(f"Failed to delete warning #{warning_id}.")
            return

        await ctx.reply(f"Successfully removed warning #{warning_id}!")


    @commands.command()
    async def kick(self, ctx: commands.Context, user: discord.Member, reason: str = None):
        if reason is None:
            await user.kick(f"KICKED BY {ctx.author.id} -- No reason was provided.")
        else:
            await user.kick(f"KICKED BY {ctx.author.id} -- {reason}")

        await ctx.message.add_reaction(u"\u2705")
    

    @commands.command()
    async def ban(self, ctx: commands.Context, user: discord.Member, reason: str = None):
        issued_by = ctx.message.author
        issued_to = user.id
        guild_id = ctx.message.guild.id

        await backend.db.add_ban(issued_by, issued_to, guild_id, reason)
        
        if reason is None:
            await user.ban(reason = f"Banned by {issued_by} -- No reason was provided.")
        else:
            await user.ban(reason = f"Banned by {issued_by} -- {reason}")

        await ctx.message.add_reaction(u"\u2705")


    @commands.command()
    async def unban(self, ctx: commands.Context, user_id: int):
        user = self.bot.get_user(user_id)
        process = await backend.db.remove_ban(user_id, ctx.message.guild.id)

        if process == False:
            ctx.reply(f"{user.name} is not banned!")
            return
        
        await ctx.message.guild.unban(user)
        await ctx.message.add_reaction(u"\u2705")

    
    @commands.command()
    async def mute(self, ctx: commands.Context, user: discord.Member, expiration: str):
        issued_by = ctx.message.author.id
        issued_to = user.id
        guild = ctx.message.guild
        muted_role_id = await backend.db.get_muted_role_id(guild.id)

        if muted_role_id == 0:
            msg = await ctx.message("No muted role found, creating one..")
            muted_role = await guild.create_role(
                name = "Muted",
                permissions = discord.Permissions(
                    send_messages = False,
                    request_to_speak = False,
                    speak = False
                    ),
            )
            await backend.db.set_muted_role(muted_role.id, guild.id)
            muted_role_id = muted_role.id

            # Permissions for @everyone sometimes override the 
            # permissions for the muted role.
            for channel in guild.text_channels:
                await channel.set_permissions(
                    muted_role,
                    send_messages = False
                )

            for channel in guild.voice_channels:
                await channel.set_permissions(
                    muted_role,
                    speak = False, request_to_speak = False
                )
            
            await msg.delete()

        muted_role = guild.get_role(muted_role_id)
        await backend.db.add_mute(issued_by, issued_to, guild.id, expiration)
        await user.add_roles(muted_role, reason=f"Muted by {ctx.message.author.id} for {expiration}")
        await ctx.message.add_reaction(u"\u2705")


    @commands.command()
    async def unmute(self, ctx: commands.Context, user: discord.Member):
        issued_to = user.id
        guild_id = ctx.message.guild.id
        muted_role_id = await backend.db.get_muted_role_id(guild_id)
        muted_role = ctx.guild.get_role(muted_role_id)
        process = await backend.db.remove_mute(issued_to, guild_id)

        if process == False:
            await ctx.reply(f"{user.name} isn't muted.")
            return
        
        await user.remove_roles(muted_role, reason=f"Unmuted by {ctx.message.author.name}")

        await ctx.message.add_reaction(u"\u2705")
        

async def setup(bot):
    await bot.add_cog(Admin(bot))