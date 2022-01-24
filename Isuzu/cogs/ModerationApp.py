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
                        output = f"{member.mention} has been timed out for {time}."
                        epoch = round((timeout_end - dt(1970,1,1)).total_seconds())
                        if dm == 'True' or not dm:
                            try:
                                await member.send(f"You have been timed out until <t:{epoch}:F> in `{interaction.guild.name}` for `{reason_to_send}`.\nYou can talk in the server again <t:{epoch}:R>.")
                            except:
                                output += " Failed to DM the user due to their privacy settings."
                        if comment:
                            output += f"\n{comment}"
                        await interaction.response.send_message(output)
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
                    output = f"{member.mention}'s timed out has been removed."
                    if dm == 'True' or not dm:
                        try:
                            await member.send(f"Your timeout in `{interaction.guild.name}` has been removed for `{reason_to_send}`.")
                        except:
                            output += " Failed to DM the user due to their privacy settings."
                    await interaction.response.send_message(output, mention_author = False)
                except Forbidden:
                    await interaction.response.send_message("I can't remove timeout from that user.")
        elif not interaction.user.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message("I don't have `Timeout Members` permission.")
        else:
            await interaction.response.send_message("You don't have `Timeout Members` permission.", ephemeral=True)

def setup(client):
    client.add_cog(ModerationSlash(client))
