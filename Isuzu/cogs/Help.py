import nextcord as discord
import pendulum as pen
from nextcord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title = '**Help**', description = 'Use `help <command>` for extended information on a command.', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))

        em.add_field(name = 'Utility', value = '`when`, `checkvera`, `schedule`, `whois`, `banner`', inline = False)
        em.add_field(name = 'Management', value = '`changeprefix`, `log`')
        em.add_field(name = 'Miscellaneous', value = '`queue`, `echo`, `ping`')
        em.add_field(name = 'Moderation', value = '`ban`, `unban`, `massban`, `minage`, `filtering`, `prune`', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.send(embed = em)

    @help.command(aliases = ['q'])
    async def queue(self, ctx):
        em = discord.Embed(title = '**queue**', description = "Commands for karaoke queue related.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Variations', value = '`queue`, `queuenext`, `queuelist`, `queueremove`, `queueswap`, `queueclear`, `forcequeue`')
        em.add_field(name = 'Aliases', value = '`q`, `qn`, `ql`, `qr`, `qs`, `qc`, `fq`', inline = False)
        queuecommmands = '`queue` to queue yourself in.\n'
        queuecommmands += '`queuelist` to see the queue.\n'
        queuecommmands += '`queuenext` to move on to the next person in queue.\n'
        queuecommmands += '`queueremove` to remove yourself from queue **OR**,\n`queueremove <order number>` to remove someone from the queue.\n'
        queuecommmands += '`queueswap` to swap order. How to run ```queueswap <order number> <order number>.```\n'
        queuecommmands += '`queueclear` to clear the queue, only mods can run this command.\n'
        queuecommmands += '`forcequeue` to force queue someone in, only mods can run this command. How to run ```forcequeue <userID> <order number> (optional)```'
        em.add_field(name = 'Description', value = f'{queuecommmands}')
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['cp'])
    async def changeprefix(self, ctx):
        em = discord.Embed(title = '**changeprefix**', description = "Changes the bot's prefix.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`cp`')
        em.add_field(name = 'Usage', value = '```changeprefix <your_new_prefix>```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['cv'])
    async def checkvera(self, ctx):
        em = discord.Embed(title = '**checkvera**', description = "Checks unprocessed membership proof.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`cv`')
        em.add_field(name = 'Usage', value = '```checkvera <channel>```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['gu','u'])
    async def when(self, ctx):
        em = discord.Embed(title = '**when**', description = "Gets unix timestamp and calculates how much time until the given date.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`gu`')
        em.add_field(name = 'Usage', value = '```getunix timezone day/month/year hour:minute```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['sch'])
    async def schedule(self, ctx):
        em = discord.Embed(title = '**schedule**', description = "Gets unix timestamp for a given date.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`sch`')
        em.add_field(name = 'Usage', value = '```schedule timezone talent\nday/month/year hour:minute~Stream Title\nyear/month/day hour:minute~Stream Title\n```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['who', 'userinfo'])
    async def whois(self, ctx):
        em = discord.Embed(title = '**whois**', description = "Checks information of a user.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`who`, `userinfo`')
        em.add_field(name = 'Usage', value = '```whois <userID>\nwhois```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def prune(self, ctx):
        em = discord.Embed(title = '**prune**', description = "Kick members with condition.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        command_addition = '`prune` to kick members with no role AND default avatar\n'
        command_addition += '`prune norole` to kick members with no role\n'
        command_addition += '`prune noavatar` to kick members with default avatar'
        em.add_field(name = 'Command addition options', value = command_addition, inline = False)
        command_Usage = '\nprune\nprune norole\nprune noavatar'
        em.add_field(name = 'Usage', value = f'```{command_Usage}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['bn'])
    async def banner(self, ctx):
        em = discord.Embed(title = '**banner**', description = "Checks banner of a user.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Aliases', value = '`bn`')
        em.add_field(name = 'Usage', value = '```banner <userID>\n```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def minage(self, ctx):
        em = discord.Embed(title = '**minage**', description = "Set a minimum age to join the server. Turned off by default.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Command addition options', value = '`message`, `channel`, `settings`')
        command_addition = "`minage` to set the minimum age (in day format).\n"
        command_addition += "`minage message` to set a message to send to the user kicked. Will use the default message if not set.\n"
        command_addition += "`minage message remove` to delete the set message and go back using the default message.\n"
        command_addition += "`minage channel` to set a channel where bot will log when do any minage actions.\n"
        command_addition += "`minage settings` to see the current settings of minage module of the server."
        em.add_field(name = 'Description', value = command_addition, inline = False)
        command_Usage = "minage <days>\n"
        command_Usage += "minage message <your message> (you can also put '{minage}')\n"
        command_Usage += "minage channel <logchannel>\n"
        command_Usage += "minage settings"
        em.add_field(name = 'Usage', value = f'```{command_Usage}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases = ['filtering'])
    async def filter(self, ctx):
        em = discord.Embed(title = '**filter**', description = "Toggle on or off content filtering module. Turned off by default", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Description', value = 'Filter message containing video from a blacklisted clipper.')
        em.add_field(name = 'Command addition options', value = '`on`, `off`, `list`, `status`', inline = False)        
        command_Usage = "filter on\n"
        command_Usage += "filter off\n"
        command_Usage += "filter list\n"
        command_Usage += "filter status"
        em.add_field(name = 'Usage', value = f'```{command_Usage}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command(aliases=['logging'])
    async def log(self, ctx):
        em = discord.Embed(title = '**log**', description = "Logs deleted and edited messages to a given channel.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Command addition options', value = '`on`, `off`, `status`, `channel remove`, `channel deleted`, `channel edited`, `ignore`, `unignore`, `ignored`')
        command_addition = "`log on/off/status` to turn on/off or see the current settings of logging.\n"
        command_addition += "`log ignore` to set channels the bot will ignore from logging the messages.\n"
        command_addition += "`log unignore` to unignore channels which was ignored before.\n"
        command_addition += "`log ignored` to see all the ignored channels.\n"
        command_addition += "`log channel both` to set a channel where bot will log both deleted and edited messages to.\n"
        command_addition += "`log channel edited` to set a channel where bot will log edited messages to.\n"
        command_addition += "`log channel deleted` to set a channel where bot will log deleted messages to.\n"
        command_addition += "`log channel remove` to delete the channel where logs supposed to be sent to."
        em.add_field(name = 'Description', value = command_addition, inline = False)
        command_Usage = "log on/off/status\n"
        command_Usage += "log ignore <channel><channel><channel> (or more)\n"
        command_Usage += "log unignore <channel><channel><channel> (or more)\n"
        command_Usage += "log ignored\n"
        command_Usage += "log channel both <logchannel>\n"
        command_Usage += "log channel edited <logchannel>\n"
        command_Usage += "log channel deleted <logchannel>\n"
        command_Usage += "log channel remove"
        em.add_field(name = 'Usage', value = f'```{command_Usage}```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        
        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def echo(self, ctx):
        em = discord.Embed(title = '**echo**', description = "Send a message you set to a certain channel. You can also send files or sticker.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage', value = '```echo <channel> <yourMessage>```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def ban(self, ctx):
        em = discord.Embed(title = '**ban**', description = "Ban a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage', value = '```ban <userID> <reason>```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def unban(self, ctx):
        em = discord.Embed(title = '**unban**', description = "Unban a user from the server. Reason is optional.", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage', value = '```unban <userID> <reason>```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def massban(self, ctx):
        em = discord.Embed(title = '**massban**', description = "Ban a bulk of users from the server. Reason is optional", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.add_field(name = 'Usage', value = '```massban <userID>\n<userID> <userID> <reason>```', inline = False)
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

    @help.command()
    async def ping(self, ctx):
        em = discord.Embed(title = '**ping**', description = "Pong.", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)

        await ctx.reply(embed = em, mention_author = False)

def setup(client):
    client.add_cog(Help(client))