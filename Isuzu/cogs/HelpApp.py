from discord import SlashOption
import nextcord as discord
import pendulum as pen
from nextcord import Interaction
from nextcord.ext import commands

# Utility

def when_option(interaction):
    em = discord.Embed(title = '**when**', description = "Gets unix timestamp and calculates how much time until the given date.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Supported Timezones', value = '• UTC or GMT\n• WIB\n• JST\n• MSK\n• EDT or EST or ET\n• PDT or PST or PT', inline = False)
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /when.\nTime input examples:\n```\n2022/1/20 13:34\n2022/03/13 3am```\n**Input time must not exceed 23:59.**', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def checkvera_option(interaction):
    em = discord.Embed(title = '**checkvera**', description = "Checks unprocessed membership proof by VeraBot.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /checkvera.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def schedule_option(interaction):
    em = discord.Embed(title = '**schedule**', description = "Gets unix timestamp for a given date.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Supported Timezones', value = '• UTC or GMT\n• WIB\n• JST\n• MSK\n• EDT or EST or ET\n• PDT or PST or PT', inline = False)
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def who_option(interaction):
    em = discord.Embed(title = '**who**', description = "Checks information of a user.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /who.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em
 
def avatar_option(interaction):
    em = discord.Embed(title = '**avatar**', description = "Checks avatar of a user. You can choose whether you want to see their server or global avatar.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /avatar.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def banner_option(interaction):
    em = discord.Embed(title = '**banner**', description = "Checks banner of a user.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /banner.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

# Management

def log_option(interaction):
    em = discord.Embed(title = '**log**', description = "Logs deleted and edited messages to a given channel.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em
    
def minage_option(interaction):
    em = discord.Embed(title = '**minage**', description = "Set a minimum age to join the server. Turned off by default.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Command options', value = '`days`, `message`, `channel`, `settings`')
    command_addition = "`minage days` to set the minimum age (in day format).\n"
    command_addition += "`minage message` to set a message to send to the kicked user. Will use the default message if not set.\n"
    command_addition += "`minage message remove` to delete the set message and go back using the default message.\n"
    command_addition += "`minage channel` to set a channel where bot will log when do any minage actions.\n"
    command_addition += "`minage settings` to see the current settings of minage module of the server."
    em.add_field(name = 'Description', value = command_addition, inline = False)
    dm_options = "`{minage}` server minimum Account Age - `Ex: 30 Days`\n"
    dm_options += "`{rejoindate}` built-in discord display for date the user can try to rejoin - `Ex:` <t:1645586955:F>\n"
    dm_options += "`{rejoincount}` built-in discord display for time left until the user can try to rejoin - `Ex:` <t:1645586955:R>"
    em.add_field(name = 'Variables you can use in minage message', value = dm_options, inline = False)
    example = "minage 30\n"
    example += "minage message Thank you for joining but your account is less than {minage}. You can try joining the server again on {rejoindate} or {rejoincount}\n"
    example += "minage channel 918340003086614578\n"
    em.add_field(name = 'Usage and Examples', value = f'Slash command, type /minage.\n```\n{example}```', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def filter_option(interaction):
    em = discord.Embed(title = '**filter**', description = "Toggle on or off content filter module. Turned off by default", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Description', value = 'Filter message containing video from a blacklisted clipper.')
    em.add_field(name = 'Command options', value = '`status`, `settings`', inline = False)
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /filter.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def voicelink_option(interaction):
    em = discord.Embed(title = '**voicelink**', description = "Automatically give a set role to user joining voice chat.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Command options', value = '`status`, `role`, `settings`')
    command_addition = "`voicelink status` to turn on/off voicelink.\n"
    command_addition += "`voicelink settings` to see the current settings of voicelink.\n"
    command_addition += "`voicelink role` to set a role which bot will give to user who join voice chat.\n"
    em.add_field(name = 'Description', value = command_addition, inline = False)
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /voicelink.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def streamlink_option(interaction):
    em = discord.Embed(title = '**streamlink**', description = "Automatically give a set role to user going live in voice chat.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Command options', value = '`status`, `role`, `settings`')
    command_addition = "`streamlink status` to turn on/off streamlink.\n"
    command_addition += "`streamlink settings` to see the current settings of streamlink.\n"
    command_addition += "`streamlink role` to set a role which bot will give to user who join voice chat.\n"
    em.add_field(name = 'Description', value = command_addition, inline = False)
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /streamlink.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def nodiscussion_option(interaction):
    em = discord.Embed(title = '**nodiscussion**', description = "Deletes message that doesn't contain link or attachments. If a message doesn't contain either, it will delete the latest message sent (if the author of the last 2 messages aren't the same user).", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

# Miscellaneous

def echo_option(interaction):
    em = discord.Embed(title = '**echo**', description = "Send a message you set to a certain channel. You can also send files or sticker.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    # em.add_field(name = 'Usage and Examples', value = '`echo <channel> <yourMessage>`\n```\necho #channel-name Echo Deez Nuts```', inline = False)
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def ping_option(interaction):
    em = discord.Embed(title = '**ping**', description = "Get latency of the bot.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def invitelink_option(interaction):
    em = discord.Embed(title = '**invitelink**', description = "Get invite link of the bot.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /invitelink.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

# Moderation

def slowmode_option(interaction):
    em = discord.Embed(title = '**slowmode**', description = "Slowmode a channel or thread for a given time. Maxed at 6 hours. (Currently only available in whitelisted guilds)", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Duration options', value='• h - Hour\n• m - Minute\n• s - Second', inline = False)
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /slowmode.\nDuration examples:\n```\n1h2m3s\n1h4s```', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def prune_option(interaction):
    em = discord.Embed(title = '**prune**', description = "Kick members with condition.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    command_addition = '`prune no avatar and role` to kick members with no role **AND** default avatar\n'
    command_addition += '`prune no role` to kick members with no role\n'
    command_addition += '`prune no avatar` to kick members with default avatar'
    em.add_field(name = 'Command options', value = command_addition, inline = False)
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def timeout_option(interaction):
    em = discord.Embed(title = '**timeout**', description = "Timeout a user for a set duration in the server. Reason is optional. (Currently only available in whitelisted guilds)\nYou can choose whether it will DM the user or not.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Duration options', value='• w - Week\n• d - Day\n• h - Hour\n• m - Minute\n• s - Second', inline = False)
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /timeout.\nDuration examples:\n```\n10d14h34m2s\n1h4s```', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def untimeout_option(interaction):
    em = discord.Embed(title = '**untimeout**', description = "Remove timeout from a user in the server. Reason is optional. (Currently only available in whitelisted guilds)\nYou can choose whether it will DM the user or not.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /untimeout.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def lock_option(interaction):
    em = discord.Embed(title = '**lock**', description = "Lockdown a channel.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /lock.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def unlock_option(interaction):
    em = discord.Embed(title = '**unlock**', description = "Unlock a locked channel.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /unlock.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def kick_option(interaction):
    em = discord.Embed(title = '**kick**', description = "Kick a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /kick.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def masskick_option(interaction):
    em = discord.Embed(title = '**masskick**', description = "Kick a bulk of users from the server. Reason is optional", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    # em.add_field(name = 'Usage and Examples', value = '`masskick <userID>\n<userID> <userID> <reason>`\n```\nmasskick 302064098739355652 137683987073073152 178089220185784320 weird ppl```', inline = False)
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def ban_option(interaction):
    em = discord.Embed(title = '**ban**', description = "Ban a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /ban.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def unban_option(interaction):
    em = discord.Embed(title = '**unban**', description = "Unban a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    em.add_field(name = 'Usage and Examples', value = 'Slash command, type /unban.', inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def massban_option(interaction):
    em = discord.Embed(title = '**massban**', description = "Ban a bulk of users from the server. Reason is optional", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    # em.add_field(name = 'Usage and Examples', value = '`massban <userID>\n<userID> <userID> <reason>`\n```\nmassban 302064098739355652 137683987073073152 178089220185784320 weird ppl```', inline = False)
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

def massunban_option(interaction):
    em = discord.Embed(title = '**massunban**', description = "Unban a bulk of users from the server. Reason is optional", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
    # em.add_field(name = 'Usage and Examples', value = '`massunban <userID>\n<userID> <userID> <reason>`\n```\nmassunban 302064098739355652 137683987073073152 178089220185784320 these ppl are ok now```', inline = False)
    em.add_field(name = 'Note', value = "This command isn't currently compatible with discord slash commands.", inline = False)
    em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
    return em

# Class

class HelpApp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @discord.slash_command(name="help", description="Display the main help for bot commands and their uses")
    async def help_slash(
        self,
        interaction : Interaction,
        arg = SlashOption(
            name = 'commands',
            description = 'The specific command you want to see the information',
            required = False,
        ),
        eph = SlashOption(
            name = 'ephemeral',
            description = 'Whether you want the output only visible to yourself - default false',
            choices = {'yes' : 'True', 'no' : 'False'},
            default = 'False',
            required = False,
        ),
    ):
        if eph == 'True': eph = True
        else: eph = False
        if not arg:
            em = discord.Embed(title = '**Help**', description = 'Use `help <command>` for extended information on a command.', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            em.add_field(name = 'Utility', value = '`when`, `checkvera`, `schedule`, `who`, `avatar`, `banner`', inline = False)
            em.add_field(name = 'Management', value = '`log`,`minage`, `filtering`, `voicelink`, `streamlink`, `nodiscussion`', inline = False)
            em.add_field(name = 'Miscellaneous', value = '`echo`, `ping`, `invitelink`', inline = False)
            em.add_field(name = 'Moderation', value = '`slowmode`, `prune`, `timeout`, `untimeout`, `kick`, `masskick`, `ban`, `unban`, `massban`, `massunban`', inline = False)
            em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
        elif arg == 'checkvera':
            em = checkvera_option(interaction)
        elif arg == 'schedule':
            em = schedule_option(interaction)
        elif arg == 'who':
            em = who_option(interaction)
        elif arg == 'avatar':
            em = avatar_option(interaction)
        elif arg == 'banner':
            em = banner_option(interaction)
        elif arg == 'log':
            em = log_option(interaction)
            eph = True
        elif arg == 'minage':
            em = minage_option(interaction)
        elif arg == 'filter':
            em = filter_option(interaction)            
        elif arg == 'voicelink':
            em = voicelink_option(interaction)
        elif arg == 'streamlink':
            em = streamlink_option(interaction)
        elif arg == 'nodiscussion':
            em = nodiscussion_option(interaction)                                                
            eph = True
        elif arg == 'echo':
            em = echo_option(interaction)
            eph = True
        elif arg == 'ping':
            em = ping_option(interaction)
        elif arg == 'invitelink':
            em = invitelink_option(interaction)
        elif arg == 'slowmode':
            em = slowmode_option(interaction)
        elif arg == 'timeout':
            em = timeout_option(interaction)
        elif arg == 'untimeout':
            em = untimeout_option(interaction)
        elif arg == 'lock':
            em = lock_option(interaction)
        elif arg == 'unlock':
            em = unlock_option(interaction)
        elif arg == 'kick':
            em = kick_option(interaction)
        elif arg == 'masskick':
            em = masskick_option(interaction)            
            eph = True
        elif arg == 'ban':
            em = ban_option(interaction)
        elif arg == 'unban':
            em = unban_option(interaction)            
        elif arg == 'massban':
            em = massban_option(interaction)
            eph = True
        elif arg == 'massunban':
            em = massunban_option(interaction)
            eph = True
        else:
            await interaction.response.send_message('Invalid command.', ephemeral = True)
            return

        await interaction.response.send_message(embed = em, ephemeral = eph)

def setup(client):
    client.add_cog(HelpApp(client))
