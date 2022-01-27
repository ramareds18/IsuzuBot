import nextcord as discord
import pendulum as pen
from durations import Duration
from nextcord import SlashOption, Interaction, NotFound
from nextcord.ext import commands
from nextcord.errors import Forbidden
from pendulum import datetime as dt


class ModerationSlash(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    M = 735868176595812422
    L = 913649915467542529

    @discord.slash_command(name="timeout", description="Timeout a user in the server", guild_ids=[M, L])
    async def timeout_slash(
        self, 
        interaction: Interaction, 
        member: discord.Member = SlashOption(
            name="user",
            description="User to timeout",
        ),
        time = SlashOption(
            name="duration",
            description="Duration in the format of 1d2h3m4s. Must not exceed 28 days",
        ),
        reason = SlashOption(
            name="reason",
            description="Reason to timeout",
            required=False,
        ),
        dm = SlashOption(
            name='dm',
            description='Send a DM to the user about the timeout - default true',
            choices={"yes": 'True', "no": 'False'},
            required=False,
        )
    ):
        if interaction.user.guild_permissions.moderate_members and interaction.user.guild.me.guild_permissions.moderate_members:
            if isinstance(member, discord.User):
                await interaction.response.send_message("User is not a member of this server.", ephemeral=True)
            else:            
                if member.top_role >= interaction.user.top_role:
                    await interaction.response.send_message("You can't timeout that user.")
                else:
                    seconds = Duration(time).to_seconds()
                    if seconds > 2419200:
                        await interaction.response.send_message("Duration must not exceed 28 days.", ephemeral=True)
                    elif int(seconds) == 0:
                        await interaction.response.send_message("Duration could not be recognized.", ephemeral=True)
                    else:
                        try:
                            comment = ''
                            if reason and len(reason) <= 450:
                                reason_to_send = reason
                                reason += f' | Timed out by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                            elif reason and len(reason) > 450:
                                reason = f'Timed out by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                                reason_to_send = "No reason given"
                                comment = 'Reason too long.'
                            else:
                                reason = f'Timed out by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                                reason_to_send = "No reason given"

                            timeout_end = pen.now('UTC').add(seconds = seconds)
                            await member.edit(timeout=timeout_end, reason=reason)

                            epoch = round((timeout_end - dt(1970,1,1)).total_seconds())

                            embed_body = f'**Timed out** {member.mention} ({member.id})\n'
                            embed_body += '\n'
                            embed_body += f'**Until** <t:{epoch}:F>\n'
                            embed_body += '\n'
                            embed_body += f'**Reason:** {reason}\n'
                            if comment:
                                embed_body += f'**Note**: {comment}'
                            
                            if dm == 'True' or not dm:
                                try:
                                    await member.send(f"You have been timed out until <t:{epoch}:F> in `{interaction.guild.name}` for `{reason_to_send}`.\nYou can talk in the server again <t:{epoch}:R>.")
                                except:
                                    embed_body += "\n*Failed to DM the user due to their privacy settings.*"

                            em = discord.Embed(title = '', description = embed_body, colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                            await interaction.response.send_message(embed=em)
                        except Forbidden:
                            await interaction.response.send_message("I can't timeout that user.")
        elif not interaction.user.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message("I don't have `Timeout Members` permission.")
        else:
            await interaction.response.send_message("You don't have `Timeout Members` permission.", ephemeral=True)

    @discord.slash_command(name="untimeout", description="Remove timeout from a user in the server", guild_ids=[M, L])
    async def untimeout_slash(
        self,
        interaction: Interaction, 
        member: discord.Member = SlashOption(
            name="user",
            description="User to untimeout",
        ),
        reason = SlashOption(
            name="reason",
            description="Reason to untimeout",
            required=False,
        ),
        dm = SlashOption(
            name='dm',
            description='Send a DM to the user about the timeout - default true',
            choices={"yes": 'True', "no": 'False'},
            required=False,
        )
    ):
        if interaction.user.guild_permissions.moderate_members and interaction.user.guild.me.guild_permissions.moderate_members:
            if isinstance(member, discord.User):
                await interaction.response.send_message("User is not a member of this server.", ephemeral=True)
            else:        
                if member.top_role >= interaction.user.top_role:
                    await interaction.response.send_message("You can't remove timeout from that user.")
                else:            
                    try:
                        comment = ''
                        if reason and len(reason) <= 450:
                            reason_to_send = reason
                            reason += f' | Timed out removed by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                        elif reason and len(reason) > 450:
                            reason = f'Timed out removed by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                            reason_to_send = "No reason given"
                            comment = 'Reason too long.'
                        else:
                            reason = f'Timed out removed by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                            reason_to_send = "No reason given"
                        await member.edit(timeout=None, reason=reason)

                        embed_body = f'**Removed timeout from** {member.mention} ({member.id})\n'
                        embed_body += '\n'
                        embed_body += f'**Reason:** {reason}\n'
                        if comment:
                            embed_body += f'**Note**: {comment}'

                        if dm == 'True' or not dm:
                            try:
                                await member.send(f"Your timeout in `{interaction.guild.name}` has been removed for `{reason_to_send}`.")
                            except:
                                embed_body += "\n*Failed to DM the user due to their privacy settings.*"

                        em = discord.Embed(title = '', description = embed_body, colour=0x00ff10, timestamp = pen.now('Asia/Jakarta'))
                        await interaction.response.send_message(embed=em)
                    except Forbidden:
                        await interaction.response.send_message("I can't remove timeout from that user.")
        elif not interaction.user.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message("I don't have `Timeout Members` permission.")
        else:
            await interaction.response.send_message("You don't have `Timeout Members` permission.", ephemeral=True)

def setup(client):
    client.add_cog(ModerationSlash(client))
