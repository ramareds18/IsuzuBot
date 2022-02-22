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
                await interaction.send("Duration must not exceed 6 hours.", ephemeral=True)
            else:

                await interaction.response.defer()
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
                        await interaction.send(f"Slowmode is now enabled in {channel.mention}, members can only send one message every {time}.")
                    else:
                        await interaction.send(f"Slowmode in {channel.mention} has been disabled.")
                except:
                    await interaction.send("Something went wrong.")

        elif not interaction.user.guild_permissions.manage_messages:
            await interaction.send("You don't have `Manage Messages` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Manage Channels` permission.")

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
                await interaction.send("User is not a member of this server.", ephemeral=True)
            else:
                if member.top_role >= interaction.user.top_role:
                    await interaction.send("You can't timeout that user.")
                else:
                    await interaction.response.defer()
                    seconds = Duration(time).to_seconds()
                    if seconds > 2419200:
                        await interaction.send("Duration must not exceed 28 days.", ephemeral=True)
                    elif int(seconds) == 0:
                        await interaction.send("Duration could not be recognized.", ephemeral=True)
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
                            await interaction.send(embed=em)
                        except Forbidden:
                            await interaction.send("I can't timeout that user.")
        elif not interaction.user.guild_permissions.moderate_members:
            await interaction.send("You don't have `Timeout Members` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Timeout Members` permission.")

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
                await interaction.send("User is not a member of this server.", ephemeral=True)
            else:
                if member.top_role >= interaction.user.top_role:
                    await interaction.send("You can't remove timeout from that user.")
                else:            
                    await interaction.response.defer()
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
                        await interaction.send(embed=em)
                    except Forbidden:
                        await interaction.send("I can't remove timeout from that user.")
        elif not interaction.user.guild_permissions.moderate_members:
            await interaction.send("You don't have `Timeout Members` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Timeout Members` permission.")

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
            await interaction.response.defer()
            reason = f'Locked down by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
            if not channel:
                overwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages != False:
                    overwrites.send_messages = False
                    await interaction.channel.set_permissions(interaction.guild.me, send_messages = True, reason = reason)
                    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.send(f"Locked {interaction.channel.mention}.")
                else:
                    await interaction.send(f"This channel is already locked.")
            else:
                overwrites = channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages != False:
                    overwrites.send_messages = False
                    await channel.set_permissions(interaction.guild.me, send_messages = True, reason = reason)
                    await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.send(f"Locked {channel.mention}.")
                else:
                    await interaction.send(f"That channel is already locked.")
        elif not interaction.user.guild_permissions.manage_messages:
            await interaction.send("You don't have `Manage Messages` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Manage Roles` permission.")

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
            await interaction.response.defer()
            reason = f'Lockdown removed by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
            if not channel:
                overwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages == False:
                    overwrites.send_messages = None
                    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.send(f"Unlocked {interaction.channel.mention}.")
                else:
                    await interaction.send(f"This channel is not locked.")
            else:
                overwrites = channel.overwrites_for(interaction.guild.default_role)
                if overwrites.send_messages == False:
                    overwrites.send_messages = None
                    await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.send(f"Unlocked {channel.mention}.")
                else:
                    await interaction.send(f"That channel is not locked.")
        elif not interaction.user.guild_permissions.manage_messages:
            await interaction.send("You don't have `Manage Messages` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Manage Roles` permission.")  

    @discord.slash_command(name="voiceactivity", description="Activate/deactivate voice activity for a voice channel")
    async def vcva_slash(
        self,
        interaction: Interaction, 
        channel: GuildChannel = SlashOption(
            name = "channel",
            description = "Channel to change to voice activity",
            channel_types = [ChannelType.voice],
        ),
        switch = SlashOption(
            name = 'switch',
            description = 'Activate/deactivate voice activity',
            choices = {'Activate' : 'on', 'Deactivate' : 'off'},
        )
    ):
        if interaction.user.guild_permissions.manage_messages and interaction.user.guild.me.guild_permissions.manage_roles:
            await interaction.response.defer()
            overwrites = channel.overwrites_for(interaction.guild.default_role)
            if switch == 'on':
                reason = f'Voice activity enabled by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                if overwrites.use_voice_activation != True:
                    overwrites.use_voice_activation = True
                    await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.send(f"Turning on voice activity for {channel.mention}.")
                else:
                    await interaction.send(f"Voice activity is already enabled for {channel.mention}.")
            else:
                reason = f'Voice activity disabled by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                if overwrites.use_voice_activation == True:
                    overwrites.use_voice_activation = None
                    await channel.set_permissions(interaction.guild.default_role, overwrite = overwrites, reason = reason)
                    await interaction.send(f"Turning off voice activity for {channel.mention}.")
                else:
                    await interaction.send(f"Voice activity is already disabled for {channel.mention}.")
        elif not interaction.user.guild_permissions.manage_messages:
            await interaction.send("You don't have `Manage Messages` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Manage Roles` permission.")  

    @discord.slash_command(name="kick", description="Kick a user from the server")
    async def kick_slash(
        self, 
        interaction: Interaction,
        member: discord.Member = SlashOption(
            name="user",
            description="The user you want to ban",
        ),
        reason = SlashOption(
            name="reason",
            description="Your reason to ban the user",
            required=False,
        )
    ):
        if interaction.user.guild_permissions.ban_members and interaction.user.guild.me.guild_permissions.kick_members:
            if isinstance(member, discord.User):
                await interaction.send("User is not a member of the server.")
            else:
                await interaction.response.defer()
                try:
                    if member.top_role >= interaction.user.top_role:
                        await interaction.send('You are not allowed to kick this user.')
                    else:
                        comment = ''
                        if reason and len(reason) <= 450:
                            reason += f' | Kicked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                        elif reason and len(reason) > 450:
                            reason = f'Kicked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                            comment = 'Reason too long.'
                        else:
                            reason = f'Kicked by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                        await interaction.guild.kick(member, reason = reason)
                        
                        embed_body = f'**Kicked** {member.mention} ({member.id})\n'
                        embed_body += '\n'
                        embed_body += f'**Reason:** {reason}\n'
                        if comment:
                            embed_body += f'**Note**: {comment}'
                        em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                        await interaction.send(content=None, embed = em)
                except Forbidden:
                    await interaction.send("Can't kick user with equal or higher role.")
        elif not interaction.user.guild_permissions.kick_members:
            await interaction.send("You don't have `Kick Members` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Kick Members` permission.")

    @discord.slash_command(name="ban", description="Ban a user from the server")
    async def ban_slash(
        self, 
        interaction: Interaction,
        member: discord.User = SlashOption(
            name="user",
            description="The user you want to ban",
        ),
        reason = SlashOption(
            name="reason",
            description="Your reason to ban the user",
            required=False,
        )
    ):
        if interaction.user.guild_permissions.ban_members and interaction.user.guild.me.guild_permissions.ban_members:
            await interaction.response.defer()
            try:
                await interaction.send('Banning...')
                if isinstance(member, discord.Member) and member.top_role >= interaction.user.top_role:
                    await interaction.edit_original_message(content='You are not allowed to ban this user.')
                else:
                    comment = ''
                    if reason and len(reason) <= 450:
                        reason += f' | Banned by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                    elif reason and len(reason) > 450:
                        reason = f'Banned by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                        comment = 'Reason too long.'
                    else:
                        reason = f'Banned by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                    await interaction.guild.ban(member, reason = reason)
                    
                    embed_body = f'**Banned** {member.mention} ({member.id})\n'
                    embed_body += '\n'
                    embed_body += f'**Reason:** {reason}\n'
                    if comment:
                        embed_body += f'**Note**: {comment}'
                    em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                    await interaction.edit_original_message(content = None, embed = em)
            except Forbidden:
                await interaction.edit_original_message(content="Can't ban user with equal or higher role.")
        elif not interaction.user.guild_permissions.ban_members:
            await interaction.send("You don't have `Ban Members` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Ban Members` permission.")

    @discord.slash_command(name="unban", description="Unban a user from the server")
    async def unban_slash(
        self, 
        interaction: Interaction, 
        member: discord.User = SlashOption(
            name="user",
            description="The user you want to unban",
        ),
        reason = SlashOption(
            name="reason",
            description="Your reason to unban the user",
            required=False,
        )
    ):
        if interaction.user.guild_permissions.ban_members and interaction.user.guild.me.guild_permissions.ban_members:
            await interaction.response.defer()
            try:
                is_banned = await interaction.guild.fetch_ban(member)
                if reason:
                    reason += f' | Unbanned by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                else:
                    reason = f'Unbanned by {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})'
                await interaction.guild.unban(member, reason = reason)
                embed_body = f'**Unbanned** {member.mention} ({member.id})\n'
                embed_body += '\n'
                embed_body += f'**Reason:** {reason}'
                em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf1e40f, timestamp = pen.now('Asia/Jakarta'))
                await interaction.send(embed = em)
            except NotFound:
                await interaction.send('That is not a banned user.')
        elif not interaction.user.guild_permissions.ban_members:
            await interaction.send("You don't have `Ban Members` permission.", ephemeral=True)
        else:
            await interaction.send("I don't have `Ban Members` permission.")

def setup(client):
    client.add_cog(ModerationApp(client))
