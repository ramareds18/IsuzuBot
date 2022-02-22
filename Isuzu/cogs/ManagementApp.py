import nextcord as discord
import pendulum as pen
import Isuzu as i
import cogs.Management as m
from nextcord import Interaction, SlashOption, ChannelType, Forbidden
from nextcord.abc import GuildChannel
from nextcord.ext import commands

# Voicelink functions

def voicelink_func(interaction, arg, collection):
    states = collection.find({"voicelink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"voicelink.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == interaction.guild.id:
                current_setting = state["voicelink"]["state"]
                break
            else:
                current_setting = None
                
    if arg == 'on':
        if not current_setting:
            collection.update_one({"_id": interaction.guild.id}, {"$set":{"voicelink.state":True}})
            return "Voice link has been enabled. Don't forget to set voice link role.\nRun `help voicelink` for more information."
        else:
            return "Voice link is already enabled."
    elif arg == 'off':
        if current_setting:
            collection.update_one({"_id": interaction.guild.id}, {"$set":{"voicelink.state":False}})
            return "Voice link has been disabled."
        else:
            return "Voice link is already disabled."

def voicelink_settings(interaction, voicelink_role, collection):
    states = collection.find({"voicelink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"voicelink.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == interaction.guild.id:
                current_setting = state["voicelink"]["state"]
                break
            else:
                current_setting = None
    output = "Current state of voice link: "
    if not current_setting:
        output += "disabled.\n"
    else:
        output += "enabled.\n"

    if voicelink_role:
        output += f"Voice link role: {voicelink_role.mention}\n"
    return output

# Streamlink functions

def streamlink_func(interaction, arg, collection):
    states = collection.find({"streamlink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"streamlink.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == interaction.guild.id:
                current_setting = state["streamlink"]["state"]
                break
            else:
                current_setting = None
                
    if arg == 'on':
        if not current_setting:
            collection.update_one({"_id": interaction.guild.id}, {"$set":{"streamlink.state":True}})
            return "Stream link has been enabled. Don't forget to set stream link role.\nRun `help streamlink` for more information."
        else:
            return "Stream link is already enabled."
    elif arg == 'off':
        if current_setting:
            collection.update_one({"_id": interaction.guild.id}, {"$set":{"streamlink.state":False}})
            return "Stream link has been disabled."
        else:
            return "Stream link is already disabled."

def streamlink_settings(interaction, streamlink_role, collection):
    states = collection.find({"streamlink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"streamlink.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == interaction.guild.id:
                current_setting = state["streamlink"]["state"]
                break
            else:
                current_setting = None
    output = "Current state of stream link: "
    if not current_setting:
        output += "disabled.\n"
    else:
        output += "enabled.\n"

    if streamlink_role:
        output += f"Stream link role: {streamlink_role.mention}\n"
    return output

class ManagementApp(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Voicelink

    @discord.slash_command(name="voicelink", description='dummy desc')
    async def voicelink_slash(self, interaction: Interaction):
        await interaction.send('This will never be called.')
    
    @voicelink_slash.subcommand(name="status", description="Voicelink status")
    async def voicelink_status(
        self, 
        interaction: Interaction, 
        state = SlashOption(
            name = "state",
            description = "Voicelink state",
            choices = {'on': 'on', 'off' : 'off'}
        ),
    ):
        if interaction.guild.me.guild_permissions.manage_roles and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            output = voicelink_func(interaction, state, collection)
            await interaction.send(output)
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Manage Roles' permission.")

    @voicelink_slash.subcommand(name="role", description="Voicelink role")
    async def voicelink_role(
        self, 
        interaction: Interaction, 
        role : discord.Role = SlashOption(
            name = "role",
            description = "Role for voicelink",
        ),
    ):
        if interaction.guild.me.guild_permissions.manage_roles and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            await interaction.send(f"Voice link role has been set to {role.mention}")
            collection.update_one({"_id": interaction.guild.id}, {"$set":{"voicelink.role":role.id}})
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Manage Roles' permission.")

    @voicelink_slash.subcommand(name="settings", description="Voicelink current settings")
    async def voicelink_settings(self, interaction: Interaction):
        if interaction.guild.me.guild_permissions.manage_roles and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            voicelink_role = i.check_voicelink_role(interaction, collection)
            if voicelink_role:
                voicelink_role = interaction.guild.get_role(voicelink_role)
            output = voicelink_settings(interaction, voicelink_role, collection)
            await interaction.send(output)
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Manage Roles' permission.")

    # Streamlink

    @discord.slash_command(name="streamlink", description='dummy desc')
    async def streamlink_slash(self, interaction: Interaction):
        await interaction.send('This will never be called.')
    
    @streamlink_slash.subcommand(name="status", description="Streamlink status")
    async def streamlink_status(
        self, 
        interaction: Interaction, 
        state = SlashOption(
            name = "state",
            description = "Streamlink state",
            choices = {'on': 'on', 'off' : 'off'}
        ),
    ):
        if interaction.guild.me.guild_permissions.manage_roles and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            output = streamlink_func(interaction, state, collection)
            await interaction.send(output)
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Manage Roles' permission.")

    @streamlink_slash.subcommand(name="role", description="Streamlink role")
    async def streamlink_role(
        self, 
        interaction: Interaction, 
        role : discord.Role = SlashOption(
            name = "role",
            description = "Role for streamlink",
        ),
    ):
        if interaction.guild.me.guild_permissions.manage_roles and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            await interaction.send(f"Voice link role has been set to {role.mention}")
            collection.update_one({"_id": interaction.guild.id}, {"$set":{"streamlink.role":role.id}})
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Manage Roles' permission.")

    @streamlink_slash.subcommand(name="settings", description="Streamlink current settings")
    async def streamlink_settings(self, interaction: Interaction):
        if interaction.guild.me.guild_permissions.manage_roles and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            streamlink_role = i.check_streamlink_role(interaction, collection)
            if streamlink_role:
                streamlink_role = interaction.guild.get_role(streamlink_role)
            output = streamlink_settings(interaction, streamlink_role, collection)
            await interaction.send(output)
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Manage Roles' permission")

    # Minage

    @discord.slash_command(name="minage", description='dummy desc')
    async def minage_slash(self, interaction: Interaction):
        await interaction.send('This will never be called.')

    @minage_slash.subcommand(name="days", description="Minimum age in day format")
    async def minage_days(
        self, 
        interaction: Interaction, 
        days : int = SlashOption(
            name = "days",
            description = "Set to 0 to disable",
            min_value = 0
        ),
    ):
        if interaction.guild.me.guild_permissions.kick_members and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            collection.update_one({"_id": interaction.guild.id}, {"$set":{"minage.days":days}})
            await interaction.send(f"Minimum age setting has been set to `{days}` day(s).\nSee more information in `/help minage`.")
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Kick Members' permission.")

    @minage_slash.subcommand(name="message", description="Message to send to the kicked user")
    async def minage_message(
        self, 
        interaction: Interaction, 
        message : str = SlashOption(
            name = "message",
            description = "Your message. Will use the default message if not set",
            required = False,
        ),
        remove = SlashOption(
            name = 'remove',
            description = "Remove the current set message",
            choices = {'yes' : 'True', 'no' : 'False'},
            default = 'False',
            required = False,
        ),
    ):
        if interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            if remove or remove == 'True':
                collection.update_one({"_id": interaction.guild.id}, {"$unset":{"minage.message":""}})
                await interaction.send("Minage message has been removed. Will be back using the default one.")
            else:
                collection.update_one({"_id": interaction.guild.id}, {"$set":{"minage.message":message}})
                await interaction.send(f"Message has been set to\n```\n{message}```")
        else:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)

    @minage_slash.subcommand(name="channel", description="Channel where bot will log when do any minage actions")
    async def minage_channel(
        self, 
        interaction: Interaction,
        ch: GuildChannel = SlashOption(
            name = "channel",
            description = "The channel or thread to for minage logs",
            channel_types = [discord.ChannelType.text, discord.ChannelType.public_thread],
        ),
    ):
        if interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            try:
                await ch.send("This channel is set to be minage logging channel.")
                await interaction.send(f"Logs channel has been set to {ch.mention}")
                collection.update_one({"_id": interaction.guild.id}, {"$set":{"minage.logging_channel":ch.id}})
            except Forbidden as f:
                await interaction.send("Can't set that channel as logging channel because bot doesn't have access or can't send messages to that channel.")
        else:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)

    @minage_slash.subcommand(name="settings", description="Current settings of minage")
    async def minage_settings(
        self,
        interaction: Interaction,
    ):
        if interaction.user.guild_permissions.manage_messages:
            await interaction.response.defer()
            collection = i.loadsettings()
            guild_settings = collection.find_one({"_id": interaction.guild.id})
            min_age = guild_settings['minage']['days']
            chk_minage_msg = m.management_check_minage_msg(interaction, collection, min_age)
            chk_minage_ch = i.check_minage_channel(interaction, collection)
            embed_body = f"**Minage:** `{min_age} day(s)`\n"
            if chk_minage_ch:
                log_channel = self.client.get_channel(chk_minage_ch)
                embed_body += f'**Minage logging channel:** {log_channel.mention}\n'
            embed_body += f"**Minage message:**\n```\n{chk_minage_msg}```"
            em = discord.Embed(title = 'Current minage settings for this server', description = embed_body, colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
            await interaction.send(embed = em)
        else:
            await interaction.send("You don't have 'Manage Messages' permission.", ephemeral = True)

    # Filter

    @discord.slash_command(name="filter", description='dummy desc')
    async def filter_slash(self, interaction: Interaction):
        await interaction.send('This will never be called.')

    @filter_slash.subcommand(name="status", description="Filter status")
    async def filter_status(
        self, 
        interaction: Interaction, 
        state = SlashOption(
            name = "state",
            description = "Filter state",
            choices = {'on': 'on', 'off' : 'off'}
        ),
    ):
        if interaction.guild.me.guild_permissions.manage_messages and interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            guild_settings = collection.find_one({"_id": interaction.guild.id})
            current_settings = guild_settings["filtering"]
            if state == 'on':
                if not current_settings:
                    collection.update_one({"_id": interaction.guild.id}, {"$set":{"filtering":True}})
                    await interaction.send("Filtering has been enabled.")
                else:
                    await interaction.send("Filtering is already enabled.")
            elif state == 'off':
                if current_settings:
                    collection.update_one({"_id": interaction.guild.id}, {"$set":{"filtering":False}})
                    await interaction.send("Filtering has been disabled.")
                else:
                    await interaction.send("Filtering is already disabled.")
        elif not interaction.user.guild_permissions.manage_guild:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)
        else:
            await interaction.send("I don't have 'Manage Messages' permission.")

    @filter_slash.subcommand(name="settings", description="Filter settings")
    async def filter_settings(
        self, 
        interaction: Interaction, 
    ):
        if interaction.user.guild_permissions.manage_guild:
            await interaction.response.defer()
            collection = i.loadsettings()
            collectionYT = i.loadblacklistedYT()
            channels = collectionYT.find({})
            blacklisted = "".join(f'{channel["name"]}\n' for channel in channels)
            guild_settings = collection.find_one({"_id": interaction.guild.id})
            current_settings = guild_settings["filtering"]
            if not current_settings:
                await interaction.send("Current state of filtering: disabled.")
            else:
                await interaction.send(f"Current state of filtering: enabled.\nBlacklisted channels:\n```\n{blacklisted}```")
        else:
            await interaction.send("You don't have 'Manage Server' permission.", ephemeral = True)

def setup(client):
    client.add_cog(ManagementApp(client))