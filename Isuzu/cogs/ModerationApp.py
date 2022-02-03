import nextcord as discord
import pendulum as pen
from durations import Duration
from nextcord import SlashOption, Interaction, NotFound, ChannelType
from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord.errors import Forbidden
from pendulum import datetime as dt

class ModerationApp(commands.Cog):

    def __init__(self, client):
        self.client = client

    # ALL THE SLASH COMMANDS HERE ARE ONLY IN WHITELISTED GUILDS SO THERE IS ACTUALLY `guild_ids=` VARIABLE IN THE SLASH COMMAND FUNCTION        
        
    @discord.slash_command(name="slowmode", description="Put slowmode to a channel")
    async def slowmode_slash(
        self, 
        interaction: Interaction,
        channel: GuildChannel = SlashOption(
            name = "channel",
            description = "The channel or thread to put on slowmode",
            channel_types = [ChannelType.text, ChannelType.public_thread],
        ),
        time = SlashOption(
            name = "duration",
            description = "Duration in the format of 1h2m3s. Must not exceed 6 hours, input 0s to remove slowmode",
        ),
        reason = SlashOption(
            name = "reason",
            description = "Reason to slowmode",
            required = False,
        ), 
    ):
        if interaction.user.guild_permissions.manage_messages and interaction.user.guild.me.guild_permissions.manage_channels:
            seconds = Duration(time).to_seconds()
            if seconds > 2419200:
                await interaction.response.send_message("Duration must not exceed 6 hours.", ephemeral=True)
            else:

                try:
                    if isinstance(channel, discord.TextChannel):
                        if reason and len(reason) <= 450:
                            reason += f' | Slowmode for {time} by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                        elif reason and len(reason) > 450:
                            reason = f'Slowmode for {time} by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                        else:
                            reason = f'Slowmode for {time} by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                        await channel.edit(slowmode_delay=seconds, reason=reason)
                    else:
                        await channel.edit(slowmode_delay=seconds)
                    if seconds != 0:
                        await interaction.response.send_message(f"Slowmode is now enabled in {channel.mention}, members can only send one message every {time}.")
                    else:
                        await interaction.response.send_message(f"Slowmode in {channel.mention} has been disabled.")
                except:
                    await interaction.response.send_message("Something went wrong.", ephemeral=True)

        elif not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You don't have `Manage Messages` permission.", ephemeral=True)
        else:
            await interaction.response.send_message("I don't have `Manage Channels` permission.")

    @discord.slash_command(name="timeout", description="Timeout a user in the server")
    async def timeout_slash(
        self, 
        interaction: Interaction, 
        member: discord.Member = SlashOption(
            name = "user",
            description = "User to timeout",
        ),
        time = SlashOption(
            name = "duration",
            description = "Duration in the format of 1d2h3m4s. Must not exceed 28 days",
        ),
        reason = SlashOption(
            name = "reason",
            description = "Reason to timeout",
            required = False,
        ), 
        dm = SlashOption(
            name = 'dm',
            description = 'Send a DM to the user about the timeout - default true',
            choices = {"yes": 'True', "no": 'False'},
            default = 'True',
            required = False,
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
                            
                            if dm == 'True':
                                try:
                                    em1 = discord.Embed(title = '', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                                    em1.add_field(name = f'Reason', value = reason_to_send, inline = False)
                                    field_body = f'Timeout will end <t:{epoch}:R>, precisely <t:{epoch}:F>.'
                                    em1.add_field(name = f'Duration', value = field_body, inline = False)
                                    em1.set_author(name = f'You have been timed out in {interaction.guild.name}.', icon_url = interaction.guild.icon)
                                    await member.send(embed=em1)
                                except:
                                    embed_body += "\n*Failed to DM the user due to their privacy settings.*"

                            em = discord.Embed(title = '', description = embed_body, colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                            await interaction.response.send_message(embed=em)
                        except Forbidden:
                            await interaction.response.send_message("I can't timeout that user.")
        elif not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You don't have `Timeout Members` permission.", ephemeral=True)
        else:
            await interaction.response.send_message("I don't have `Timeout Members` permission.")

    @discord.slash_command(name="untimeout", description="Remove timeout from a user in the server")
    async def untimeout_slash(
        self,
        interaction: Interaction, 
        member: discord.Member = SlashOption(
            name = "user",
            description = "User to untimeout",
        ),
        reason = SlashOption(
            name ="reason",
            description = "Reason to untimeout",
            required = False, 
        ),
        dm = SlashOption(
            name ='dm',
            description = 'Send a DM to the user about the timeout - default true',
            choices = {"yes": 'True', "no": 'False'},
            default = 'True',
            required = False,
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

                        if dm == 'True':
                            try:
                                em1 = discord.Embed(title = '', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                                em1.add_field(name = f'Reason', value = reason_to_send, inline = False)
                                em1.set_author(name = f'Your timeout in {interaction.guild.name} has been removed.', icon_url = interaction.guild.icon)
                                await member.send(embed=em1)
                            except:
                                embed_body += "\n*Failed to DM the user due to their privacy settings.*"

                        em = discord.Embed(title = '', description = embed_body, colour=0x00ff10, timestamp = pen.now('Asia/Jakarta'))
                        await interaction.response.send_message(embed=em)
                    except Forbidden:
                        await interaction.response.send_message("I can't remove timeout from that user.")
        elif not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You don't have `Timeout Members` permission.", ephemeral=True)
        else:
            await interaction.response.send_message("I don't have `Timeout Members` permission.")

    @discord.slash_command(name="lock", description="Lockdown a channel")
    async def lock_slash(
        self,
        interaction: Interaction, 
        channel: GuildChannel = SlashOption(
            name = "channel",
            description = "Channel to lock",
            required = False,
            channel_types = [ChannelType.text],
        )
    ):
        if interaction.user.guild_permissions.manage_messages and interaction.user.guild.me.guild_permissions.manage_roles:
            reason = f'Locked down by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
            if not channel:
                overwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages != False:
                    overwrites.send_messages == False
                    await interaction.channel.set_permissions(interaction.guild.me, send_messages = True, reason = reason)
                    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.response.send_message(f"Locked {interaction.channel.mention}.")
                else:
                    await interaction.response.send_message(f"This channel is already locked.")
            else:
                overwrites = channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages != False:
                    overwrites.send_messages == False
                    await channel.set_permissions(interaction.guild.me, send_messages = True, reason = reason)
                    await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.response.send_message(f"Locked {channel.mention}.")
                else:
                    await interaction.response.send_message(f"That channel is already locked.")
        elif not interaction.user.guild.me.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have `Manage Messages` permission.", ephemeral=True)
        else:
            await interaction.response.send_message("I don't have `Manage Roles` permission.")

    @discord.slash_command(name="unlock", description="Unlock a locked channel")
    async def unlock_slash(
        self,
        interaction: Interaction, 
        channel: GuildChannel = SlashOption(
            name = "channel",
            description = "Channel to unlock",
            required = False,
            channel_types = [ChannelType.text],
        )
    ):
        if interaction.user.guild_permissions.manage_messages and interaction.user.guild.me.guild_permissions.manage_roles:
            reason = f'Lockdown removed by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
            if not channel:
                overwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages == False:
                    overwrites.send_messages == None
                    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.response.send_message(f"Unlocked {interaction.channel.mention}.")
                else:
                    await interaction.response.send_message(f"This channel is not locked.")
            else:
                overwrites = channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages == False:
                    overwrites.send_messages == None
                    await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.response.send_message(f"Unlocked {channel.mention}.")
                else:
                    await interaction.response.send_message(f"That channel is not locked.")
        elif not interaction.user.guild.me.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have `Manage Messages` permission.", ephemeral=True)
        else:
            await interaction.response.send_message("I don't have `Manage Roles` permission.")  

def setup(client):
    client.add_cog(ModerationApp(client))
