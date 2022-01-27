import typing
import nextcord as discord
import pendulum as pen
from nextcord.ext import commands
from nextcord.errors import Forbidden
from pendulum import datetime as dt

def invalidargssch():
    return 'Missing argument(s). Below are the supported formats and timezones:\n```[timezone] [talent] day/month/year hour:minute\nUTC or GMT\nWIB\nJST\nMSK\nEDT or EST or ET\nPDT or PST or PT```'

def validtimezone(arg):
    valid = ['wib', 'jst', 'msk', 'utc', 'gmt', 'edt', 'est', 'et', 'pdt', 'pst', 'pt']
    if arg.lower() in valid:
        return True
    else:
        return False

def timezonecheck(timezone):
    tzcheck = True
    if(timezone.lower() == 'wib'):
        timezone = "Asia/Jakarta"
    elif(timezone.lower() == 'jst'):
        timezone = "Asia/Tokyo"
    elif(timezone.lower() == 'msk'):
        timezone = "Europe/Moscow"
    elif(timezone.lower() == 'utc' or timezone.lower() == 'gmt'):
        timezone = "UTC"
    elif(timezone.lower() == 'edt' or timezone.lower() == 'est' or timezone.lower() == 'et'):
        timezone = "US/Eastern"
    elif(timezone.lower() == 'pdt' or timezone.lower() == 'pst' or timezone.lower() == 'pt'):
        timezone = "America/Los_Angeles"
    else:
        tzcheck = False
    
    return timezone, tzcheck

class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Connected to bot: {}'.format(self.client.user.name))
        print('Bot ID: {}'.format(self.client.user.id))

    @commands.command(aliases=['cv'])
    @commands.bot_has_permissions(send_messages = True)
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def checkvera(self, ctx, channel: discord.TextChannel):
        try:
            channel = self.client.get_channel(channel.id) 
            links = "" 
            async for message in channel.history(limit = 500):
                reactions = message.reactions
                for reaction in reactions:
                    if reaction.emoji == '✅':
                        async for user in reaction.users():
                            if user.bot:
                                links += message.jump_url + "\n"
            if links == "":
                await ctx.reply("Everything looks good.", mention_author = False)
            else:
                await ctx.reply("Membership not processed yet:\n" + links, mention_author = False)
        except Forbidden:
            await ctx.reply("Bot doesn't have access to that channel.")

    @commands.command(aliases=['sch'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def schedule(self, ctx, timezone, talent, *, schedule): # Print Schedule
        UTC = "UTC"
        
        timezone, tzcheck = timezonecheck(timezone)
        
        try:
            if tzcheck:
                streamplan = schedule.split("\n")
                activities = []
                for date_and_activity in streamplan:
                    two_part_event = date_and_activity.split("~")
                    epoch = round((pen.parse(two_part_event[0], strict = False, tz = timezone, dayfirst = True).in_tz(UTC) - dt(1970,1,1)).total_seconds())
                    activities.append(f"<t:{epoch}:F> <t:{epoch}:R>: **{two_part_event[1]}**")
                    if(talent.lower() == "moona"):
                        output = f"__**Moona's** :crystal_ball: schedule for this week:__\n"
                    elif(talent.lower() == 'kronii'):
                        output = f"__**Kronii's** :hourglass_flowing_sand: schedule for this week:__\n"
                    elif(talent.lower() == 'irys'):
                        output = f"__**IRySchedule** :gem: for this week:__\n"
                    elif(talent.lower() == 'lui'):
                        output = f"__**Lui's** :wilted_rose: schedule for this week:__\n"
                    elif(talent.lower() == 'gura'):
                        output = f"__**Gura's** :trident: schedule for this week:__\n"                         
                    else:
                        output = f"__**{talent}'s** schedule for this week:__\n"
                
                output += '\n'
                for activity in activities:
                    output += f"{activity}\n"
                output += "\n*Times displayed are automatically converted into your local timezone.*"
                
                output += f'\n```\n{output}```'
                
                await ctx.reply(output, mention_author = False)
            elif validtimezone(talent):
                errouput = f"Wrong order of input.\nYour input:\n```\n{timezone} {talent}```\nCorrect input:\n```\n{talent} {timezone}```"
                await ctx.reply(errouput, mention_author = False)
            else:
                await ctx.reply('Invalid data input. Run `help schedule` for more information.', mention_author = False)
        except:
            await ctx.reply('Invalid data input. Run `help schedule` for more information.', mention_author = False)

    @commands.command(aliases=['who', 'userinfo'])
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whois(self, ctx, member: typing.Union[discord.Member, discord.User] = None):
        member = ctx.author if not member else member
        user = await self.client.fetch_user(member.id)
        ca = round((member.created_at - dt(1970,1,1)).total_seconds())
        if isinstance(member, discord.Member):
            if str(member.status).upper() == "ONLINE": status = "<:online:909423512777814067> Online"
            elif str(member.status).upper() == "IDLE": status = "<:idle:914882810119081995> Idle"
            elif str(member.status).upper() == "DND": status = "<:dnd:909421553450639370> Do Not Disturb"
            elif str(member.status).upper() == "OFFLINE": status = "<:offline:909423475792416798> Offline"
            else: status = ""
            embed_body = f'{member.mention} - {member.id}\n'
            if member.bot: embed_body += f'Bot | {status}\n'
            else:
                if member.top_role.id == ctx.guild.id: embed_body += f'{status}\n'
                else: embed_body += f'{member.top_role} | {status}\n'
            embed_body += f'**\nCreated:** <t:{ca}:F> (<t:{ca}:R>)\n'
            ja = round((member.joined_at - dt(1970,1,1)).total_seconds())
            embed_body += f'**Joined:** <t:{ja}:F> (<t:{ja}:R>)'
        else:
            embed_body = f'{member.mention} - {member.id}\n**Created:** <t:{ca}:F> (<t:{ca}:R>)\n'
            embed_body += '\n*This user is not a member of this server. No additional info is available.*'

        em = discord.Embed(description= f'{embed_body}', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        if isinstance(member, discord.Member):
            if member.nick:
                em.set_author(name = f'{member.name}#{member.discriminator}  ({member.nick})', icon_url = member.display_avatar)
            else:
                em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
            field_body = ""
            if len(member.roles) > 1:
                roles = [role for role in reversed(member.roles)]
                for role in roles:
                    if roles.index(role) == len(roles) - 1:
                        field_body += f"{role.mention} "
                em.add_field(name = f'ROLES [{len(member.roles) - 1}]:', value = field_body, inline = False)
        else:
            em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
        if user.banner:
            em.set_image(url = user.banner)

        if member.avatar:
            url = member.avatar
        else:
            url = member.display_avatar

        em.set_thumbnail(url = url)

        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    @commands.command(aliases=['bn'])
    @commands.has_permissions(manage_messages = True)
    async def banner(self, ctx, member: typing.Union[discord.Member, discord.User] = None):
        member = ctx.author if not member else member
        user = await self.client.fetch_user(member.id)
        embed_body = f'{member.mention} - User Banner\n'
        embed_body += '\n'
        if user.banner:
            embed_body += f"[Download banner]({user.banner.url})"
        else:
            embed_body += "*This user has no banner.*"
        em = discord.Embed(description= f'{embed_body}', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        if isinstance(member, discord.Member):
            if member.nick:
                em.set_author(name = f'{member.name}#{member.discriminator}  ({member.nick})', icon_url = member.display_avatar)
            else:
                em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
        else:
            em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
        if user.banner:
            em.set_image(url = user.banner)

        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    # Error-handling section

    @checkvera.error
    async def cv_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please provide vera logs channel.', mention_author = False)

    @schedule.error
    async def schedule_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(invalidargssch(), mention_author = False)

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.BadUnionArgument):
            await ctx.reply ("User could not be recognized. This is most likely due to the ID inputted wasn't a user ID.", mention_author = False)

    @banner.error
    async def banner_error(self, ctx, error):
        if isinstance(error, commands.BadUnionArgument):
            await ctx.reply("User could not be recognized. This is most likely due to the ID inputted wasn't a user ID.", mention_author = False)

def setup(client):
    client.add_cog(Utility(client))
