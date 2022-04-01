import nextcord as discord
import pendulum as pen
from nextcord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title = '**Help**', description = 'Use `help <command>` for extended information on a command.', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))

        em.add_field(name = 'Utility', value = '`when`, `checkvera`, `schedule`, `whois`, `avatar`, `banner`', inline = False)
        em.add_field(name = 'Management', value = '`changeprefix`, `minage`, `filtering`, `log`, `voicelink`, `streamlink`, `nodiscussion`', inline = False)
        em.add_field(name = 'Miscellaneous', value = '`echo`, `stickerinfo`, `ping`, `invitelink`', inline = False)
        em.add_field(name = 'Moderation', value = '`slowmode`, `prune`, `timeout`, `untimeout`, `kick`, `masskick`, `ban`, `unban`, `massban`, `massunban`', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    # Utility

    @help.command()
    async def when(self, ctx):
        em = discord.Embed(title = '**when**', description = "Gets unix timestamp and calculates how much time until the given date.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Supported Timezones', value = '• UTC or GMT\n• WIB\n• JST\n• MSK\n• EDT or EST or ET\n• PDT or PST or PT', inline = False)
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /when.\nTime input examples:\n```\n2022/1/20 13:34\n2022/03/13 3am```\n**Input time must not exceed 23:59.**', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['cv'])
    async def checkvera(self, ctx):
        em = discord.Embed(title = '**checkvera**', description = "Checks unprocessed membership proof by VeraBot.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`cv`')
        em.add_field(name = 'Usage and Examples', value = '`checkvera <channel>`\n```\ncheckvera 846974427450572870\ncheckvera #vera-logs```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['sch'])
    async def schedule(self, ctx):
        em = discord.Embed(title = '**schedule**', description = "Gets unix timestamp for a given date.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`sch`')
        em.add_field(name = 'Supported Timezones', value = '• UTC or GMT\n• WIB\n• JST\n• MSK\n• EDT or EST or ET\n• PDT or PST or PT', inline = False)
        usage_and_examples = 'schedule JST Lui\n'
        usage_and_examples += '2022/1/20 13:00~Apex collab with EN & ID Senpai\n'
        usage_and_examples += '1/20/2022 11pm~hololiveERROR\n'
        usage_and_examples += '**Input time must not exceed 23:59.**'
        em.add_field(name = 'Usage and Examples', value = f'x\n```schedule timezone talent\nmonth/day/year hour:minute~Stream Title\nyear/month/day hour:minute~Stream Title```\n```\n{usage_and_examples}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['who', 'userinfo'])
    async def whois(self, ctx):
        em = discord.Embed(title = '**whois**', description = "Checks information of a user.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`who`, `userinfo`')
        em.add_field(name = 'Usage and Examples', value = '`whois <userID>`\n```\nwhois 302064098739355652```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def avatar(self, ctx):
        em = discord.Embed(title = '**avatar**', description = "Checks avatar of a user. You can choose whether you want to see their server or global avatar.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /avatar.', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def banner(self, ctx):
        em = discord.Embed(title = '**banner**', description = "Checks banner of a user.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /banner.', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)
    
    # Management 

    @help.command(aliases = ['cp'])
    async def changeprefix(self, ctx):
        em = discord.Embed(title = '**changeprefix**', description = "Changes the bot prefix.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`cp`')
        em.add_field(name = 'Usage and Examples', value = '`changeprefix <your_new_prefix>`\n```\nchangeprefix .```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases=['logging'])
    async def log(self, ctx):
        em = discord.Embed(title = '**log**', description = "Logs deleted and edited messages to a given channel.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Command options', value = '`on`, `off`, `status`, `channel remove`, `channel deleted`, `channel edited`, `ignore`, `unignore`, `ignored`')
        command_addition = "`log on/off/status` to turn on/off or see the current settings of logging.\n"
        command_addition += "`log ignore` to set channels the bot will ignore from logging the messages.\n"
        command_addition += "`log unignore` to unignore channels which was ignored before.\n"
        command_addition += "`log ignored` to see all the ignored channels.\n"
        command_addition += "`log channel both` to set a channel where bot will log both deleted and edited messages to.\n"
        command_addition += "`log channel edited` to set a channel where bot will log edited messages to.\n"
        command_addition += "`log channel deleted` to set a channel where bot will log deleted messages to.\n"
        command_addition += "`log channel remove` to delete the channel where logs supposed to be sent to."
        em.add_field(name = 'Description', value = command_addition, inline = False)
        command_usage = "log on/off/status\n"
        command_usage += "log ignore <channel><channel><channel> (or more)\n"
        command_usage += "log unignore <channel><channel><channel> (or more)\n"
        command_usage += "log ignored\n"
        command_usage += "log channel both <logchannel>\n"
        command_usage += "log channel edited <logchannel>\n"
        command_usage += "log channel deleted <logchannel>\n"
        command_usage += "log channel remove"
        example = "log ignore 793272704182386718 793272785345577002 #logs\n"
        example += "log unignore 793272704182386718 793272785345577002 #logs\n"
        example += "log channel both 793272704182386718\n"
        example += "log channel edited 793272704182386718\n"
        example += "log channel deleted 793272704182386718\n"
        em.add_field(name = 'Usage and Examples', value = f'```\n{command_usage}```\n```\n{example}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def minage(self, ctx):
        em = discord.Embed(title = '**minage**', description = "Set a minimum age to join the server. Turned off by default.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Command options', value = '`message`, `channel`, `settings`')
        command_addition = "`minage` to set the minimum age (in day format).\n"
        command_addition += "`minage message` to set a message to send to the kicked user. Will use the default message if not set.\n"
        command_addition += "`minage message remove` to delete the set message and go back using the default message.\n"
        command_addition += "`minage channel` to set a channel where bot will log when do any minage actions.\n"
        command_addition += "`minage settings` to see the current settings of minage module of the server."
        em.add_field(name = 'Description', value = command_addition, inline = False)
        dm_options = "`{minage}` server minimum Account Age - `Ex: 30 Days`\n"
        dm_options += "`{rejoindate}` built-in discord display for date the user can try to rejoin - `Ex:` <t:1645586955:F>\n"
        dm_options += "`{rejoincount}` built-in discord display for time left until the user can try to rejoin - `Ex:` <t:1645586955:R>"
        em.add_field(name = 'Variables you can use in minage message', value = dm_options, inline = False)
        command_usage = "minage <days>\n"
        command_usage += "minage message <your message>\n"
        command_usage += "minage channel <logchannel>\n"
        command_usage += "minage settings"
        example = "minage 30\n"
        example += "minage message Thank you for joining but your account is less than {minage}. You can try joining the server again on {rejoindate} or {rejoincount}\n"
        example += "minage channel 918340003086614578\n"
        em.add_field(name = 'Usage and Examples', value = f'```\n{command_usage}```\n```\n{example}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['filtering'])
    async def filter(self, ctx):
        em = discord.Embed(title = '**filter**', description = "Toggle on or off content filtering module. Turned off by default", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Description', value = 'Filter message containing video from a blacklisted clipper. **NOTE:** It will ignore messages from someone with administrator permission.')
        em.add_field(name = 'Command options', value = '`on`, `off`, `list`, `status`', inline = False)        
        command_usage = "filter on\n"
        command_usage += "filter off\n"
        command_usage += "filter list\n"
        command_usage += "filter status"
        em.add_field(name = 'Usage and Examples', value = f'```\n{command_usage}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases=['vl'])
    async def voicelink(self, ctx):
        em = discord.Embed(title = '**voicelink**', description = "Automatically give a set role to user joining voice chat. **NOTE:** It will ignore anyone with administrator permission.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Command options', value = '`on`, `off`, `status`, `role`')
        command_addition = "`voicelink on/off/status` to turn on/off or see the current settings of voicelink.\n"
        command_addition += "`voicelink role` to set a role which bot will give to users who join voice chat.\n"
        em.add_field(name = 'Description', value = command_addition, inline = False)
        command_usage = "voicelink on/off/status\n"
        command_usage += "voicelink role <role>\n"
        example = "voicelink role 854617721898663956\nvoicelink role @rolename"
        em.add_field(name = 'Usage and Examples', value = f'```\n{command_usage}```\n```\n{example}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases=['sl'])
    async def streamlink(self, ctx):
        em = discord.Embed(title = '**streamlink**', description = "Automatically give a set role to user going live in voice chat. **NOTE:** It will ignore anyone with administrator permission.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Command options', value = '`on`, `off`, `status`, `role`')
        command_addition = "`streamlink on/off/status` to turn on/off or see the current settings of streamlink.\n"
        command_addition += "`streamlink role` to set a role which bot will give to users who go live in voice chat.\n"
        em.add_field(name = 'Description', value = command_addition, inline = False)
        command_usage = "streamlink on/off/status\n"
        command_usage += "streamlink role <role>\n"
        example = "streamlink role 854617721898663956\streamlink role @rolename"
        em.add_field(name = 'Usage and Examples', value = f'```\n{command_usage}```\n```\n{example}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases=['nd'])
    async def nodiscussion(self, ctx):
        em = discord.Embed(title = '**nodiscussion**', description = "Deletes message that doesn't contain link or attachments. If a message doesn't contain either, it will delete the latest message sent (if the author of the last 2 messages aren't the same user).", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Command options', value = '`on`, `off`, `status`, `channel`, `ignore`, `unignore`, `ignored`, `remove`')
        command_addition = "`nodiscussion on/off/status` to turn on/off or see the current settings of nodiscussion.\n"
        command_addition += "`nodiscussion channel` to set channels the bot will implement nodiscussion.\n"
        command_addition += "`nodiscussion ignore` to set roles the bot will ignore from implementing nodiscussion.\n"
        command_addition += "`nodiscussion ignored` to see all the ignored roles.\n"
        command_addition += "`nodiscussion unignore` to unignore roles which was ignored before.\n"
        command_addition += "`nodiscussion remove` to remove channels which was implemented nodiscussion before.\n"
        em.add_field(name = 'Description', value = command_addition, inline = False)
        command_usage = "nodiscussion on/off/status\n"
        command_usage += "nodiscussion channel <channel><channel><channel> (or more)\n"
        command_usage += "nodiscussion ignore <role><role><role> (or more)\n"
        command_usage += "nodiscussion unignore <role><role><role> (or more)\n"
        command_usage += "nodiscussion ignored\n"
        command_usage += "nodiscussion remove <channel><channel><channel> (or more)\n"
        example = "nodiscussion channel 793272704182386718 793272785345577002 #sounds\n"
        example += "nodiscussion ignore 793272704182386718 793272785345577002 @role\n"
        example += "nodiscussion unignore 793272704182386718 793272785345577002 @role\n"
        example += "nodiscussion remove 793272704182386718 793272785345577002 #sounds\n"
        em.add_field(name = 'Usage and Examples', value = f'```\n{command_usage}```\n```\n{example}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)
    
    # Miscellaneous

    @help.command()
    async def echo(self, ctx):
        em = discord.Embed(title = '**echo**', description = "Send a message you set to a certain channel. You can also send files or sticker.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = '`echo <channel> <yourMessage>`\n```\necho #channel-name Echo Deez Nuts```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def ping(self, ctx):
        em = discord.Embed(title = '**ping**', description = "Get latency of the bot.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def stickerinfo(self, ctx):
        em = discord.Embed(title = '**stickerinfo**', description = "Get information from a given sticker.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`ss`, `steal sticker`')
        em.add_field(name = 'Usage and Examples', value = '`stickerinfo <send your message with a sticker>`', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def invitelink(self, ctx):
        em = discord.Embed(title = '**invitelink**', description = "Get invite link of the bot.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`inv`')
        em.add_field(name = 'Usage and Examples', value = '`invitelink`', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    # Moderation

    @help.command()
    async def slowmode(self, ctx):
        em = discord.Embed(title = '**slowmode**', description = "Slowmode a channel or thread for a given time. Maxed at 6 hours. (Currently only available in whitelisted guilds)", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Duration options', value='• h - Hour\n• m - Minute\n• s - Second', inline = False)
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /slowmode.\nDuration examples:\n```\n1h2m3s\n1h4s```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def prune(self, ctx):
        em = discord.Embed(title = '**prune**', description = "Kick members with condition.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        command_addition = '`prune` to kick members with no role AND default avatar\n'
        command_addition += '`prune norole` to kick members with no role\n'
        command_addition += '`prune noavatar` to kick members with default avatar'
        em.add_field(name = 'Command options', value = command_addition, inline = False)
        command_usage = '\nprune\nprune norole\nprune noavatar'
        em.add_field(name = 'Usage and Examples', value = f'```\n{command_usage}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def timeout(self, ctx):
        em = discord.Embed(title = '**timeout**', description = "Timeout a user for a set duration in the server. Reason is optional. (Currently only available in whitelisted guilds)\nYou can choose whether it will DM the user or not.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Duration options', value='• w - Week\n• d - Day\n• h - Hour\n• m - Minute\n• s - Second', inline = False)
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /timeout.\nDuration examples:\n```\n10d14h34m2s\n1h4s```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def untimeout(self, ctx):
        em = discord.Embed(title = '**untimeout**', description = "Remove timeout from a user in the server. Reason is optional. (Currently only available in whitelisted guilds)\nYou can choose whether it will DM the user or not.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /untimeout.', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def lock(self, ctx):
        em = discord.Embed(title = '**lock**', description = "Lockdown a channel.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /lock.', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def unlock(self, ctx):
        em = discord.Embed(title = '**unlock**', description = "Unlock a locked channel.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = 'Slash command, type /unlock.', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def kick(self, ctx):
        em = discord.Embed(title = '**kick**', description = "Kick a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = '`kick <userID> <reason>`\n```\nkick 302064098739355652 get kicked```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def masskick(self, ctx):
        em = discord.Embed(title = '**masskick**', description = "Kick a bulk of users from the server. Reason is optional", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = '`masskick <userID>\n<userID> <userID> <reason>`\n```\nmasskick 302064098739355652 137683987073073152 178089220185784320 weird ppl```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def ban(self, ctx):
        em = discord.Embed(title = '**ban**', description = "Ban a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = '`ban <userID> <reason>`\n```\nban 302064098739355652 get banned```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def unban(self, ctx):
        em = discord.Embed(title = '**unban**', description = "Unban a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = '`unban <userID> <reason>`\n```\nunban 302064098739355652 youre cool now```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def massban(self, ctx):
        em = discord.Embed(title = '**massban**', description = "Ban a bulk of users from the server. Reason is optional", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`nuke`')
        em.add_field(name = 'Usage and Examples', value = '`massban <userID>\n<userID> <userID> <reason>`\n```\nmassban 302064098739355652 137683987073073152 178089220185784320 weird ppl```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def massunban(self, ctx):
        em = discord.Embed(title = '**massunban**', description = "Unban a bulk of users from the server. Reason is optional", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage and Examples', value = '`massunban <userID>\n<userID> <userID> <reason>`\n```\nmassunban 302064098739355652 137683987073073152 178089220185784320 these ppl are ok now```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

def setup(client):
    client.add_cog(Help(client))
