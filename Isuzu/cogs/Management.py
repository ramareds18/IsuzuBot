import nextcord as discord
import os
import sys
import json
import Isuzu as i
import pendulum as pen
from nextcord.ext import commands
from nextcord.errors import Forbidden

def loadrestart():
    with open('./resources/RestartMsg.json', 'r') as f:
        ch = json.load(f)
    return ch    
    
def writerestart(ch):
    with open('./resources/RestartMsg.json', 'w') as f:
        json.dump(ch, f, indent=4)

def filtering_func(ctx, arg):
    collection = i.loadsettings()
    guild_settings = collection.find_one({"_id": ctx.guild.id})
    current_settings = guild_settings["filtering"]
    if arg == 'on':
        if not current_settings:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"filtering":True}})
            return "Filtering has been enabled."
        else:
            return "Filtering is already enabled."
    elif arg == 'off':
        if current_settings:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"filtering":False}})
            return "Filtering has been disabled."
        else:
            return "Filtering is already disabled."
    elif arg == 'list':
        collectionYT = i.loadblacklistedYT()
        channels = collectionYT.find({})
        output = "".join(f'{channel["name"]}\n' for channel in channels)
        return f'Blacklisted channels:\n```\n{output}```'
    elif arg == 'status':
        if not current_settings:
            return 'Current state of filtering: disabled.'
        else:
            return 'Current state of filtering: enabled.'
    else:
        return "Invalid argument. Please run `help filtering` to see full information."

def logging_func(ctx, arg, deleted_log_channel, edited_log_channel, collection):
    states = collection.find({"logging.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"logging.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == ctx.guild.id:
                current_setting = state["logging"]["state"]
                break
            else:
                current_setting = None
            
    if arg == 'on':
        if not current_setting:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.state":True}})
            return "Logging has been enabled. Don't forget to set edited/deleted messages log channel.\nRun `help log` for more information."
        else:
            return "Logging is already enabled."
    elif arg == 'off':
        if current_setting:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.state":False}})
            return "Logging has been disabled."
        else:
            return "Logging is already disabled."
    elif arg == 'status':
        output = "Current state of logging: "
        if not current_setting:
            output += "disabled.\n"
        else:
            output += "enabled.\n"
        if edited_log_channel:
            output += f"Edited messages log channel: {edited_log_channel.mention}\n"
        if deleted_log_channel:
            output += f"Deleted messages log channel: {deleted_log_channel.mention}"

        return output
    else:
        return "Invalid argument. Please run `help log` to see full information."

def voicelink_func(ctx, arg, voicelink_role, collection):
    states = collection.find({"voicelink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"voicelink.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == ctx.guild.id:
                current_setting = state["voicelink"]["state"]
                break
            else:
                current_setting = None
                
    if arg == 'on':
        if not current_setting:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"voicelink.state":True}})
            return "Voice link has been enabled. Don't forget to set voice link role.\nRun `help voicelink` for more information."
        else:
            return "Voice link is already enabled."
    elif arg == 'off':
        if current_setting:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"voicelink.state":False}})
            return "Voice link has been disabled."
        else:
            return "Voice link is already disabled."
    elif arg == 'status':
        output = "Current state of voice link: "
        if not current_setting:
            output += "disabled.\n"
        else:
            output += "enabled.\n"
        if voicelink_role:
            output += f"Voice link role: {voicelink_role.mention}\n"
        return output
    else:
        return "Invalid argument. Please run `help voicelink` to see full information."

def streamlink_func(ctx, arg, streamlink_role, collection):
    states = collection.find({"streamlink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"streamlink.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == ctx.guild.id:
                current_setting = state["streamlink"]["state"]
                break
            else:
                current_setting = None
                
    if arg == 'on':
        if not current_setting:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"streamlink.state":True}})
            return "Stream link has been enabled. Don't forget to set stream link role.\nRun `help streamlink` for more information."
        else:
            return "Stream link is already enabled."
    elif arg == 'off':
        if current_setting:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"streamlink.state":False}})
            return "Stream link has been disabled."
        else:
            return "Stream link is already disabled."
    elif arg == 'status':
        output = "Current state of stream link: "
        if not current_setting:
            output += "disabled.\n"
        else:
            output += "enabled.\n"
        if streamlink_role:
            output += f"Stream link role: {streamlink_role.mention}\n"
        return output
    else:
        return "Invalid argument. Please run `help streamlink` to see full information."

def management_check_minage_msg(context, collection, min_age):
    default_message = f"You have been kicked from **{context.guild.name}** due to your account age being less than **{min_age}** day(s). Please feel free to attempt to rejoin on <t:unixtimetamp:F> or <t:unixtimetamp:R>."
    minage_msg = collection.find({"minage.message": {"$exists": True, "$ne": None}})
    found = False
    if collection.count_documents({}) == collection.count_documents({"minage.message": {"$exists": False}}):
        return default_message
    else:
        for msg in minage_msg:
            if msg["_id"] == context.guild.id:
                found = True
                break
        if found:
            msg_var = msg["minage"]["message"]
            return msg_var
        else:
            return default_message

class Management(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["gg"])
    @commands.is_owner()
    async def get_guilds(self, ctx):
        guilds = self.client.guilds
        output = f'{self.client.user.name} is in {len(guilds)} servers:\n'
        guild_list = "".join(f'{guild.id} - {guild.name} ~> {guild.owner.name}#{guild.owner.discriminator} ({guild.owner.id})\n' for guild in guilds)
        output += f'```\n{guild_list}```'
        await ctx.reply(output, mention_author = False)

    @commands.command(aliases=["lg"])
    @commands.is_owner()
    async def leaveguild(self, ctx, guildID):
        guild = await self.client.fetch_guild(guildID)
        if guild:
            output = f'Are you sure you want {self.client.user.name} to leave {guild.name}? You have 1 minute.'
            msg = await ctx.reply(output)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            yas = '✅'
            nay = '❌'
            valid_reactions = ['✅', '❌']
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in valid_reactions
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == yas:
                confirm = True
            else:
                confirm = False

            if confirm:
                await guild.leave()
                await ctx.reply(f"{self.client.user.name} has left {guild.name}.")
            else:
                await ctx.reply("You cancelled the interaction.")
        else:
            await ctx.reply(f"{self.client.user.name} isn't in that guild/guild ID is unrecognizable.")

    @commands.command()
    @commands.is_owner()
    async def checkdb(self, ctx):
        collection = i.loadsettings()
        collection1 = i.loadblacklistedYT()
        count_all = collection1.count_documents({})
        count_mng_msg = collection1.count_documents({"minage.message": {"$exists": False}})
        data = collection.find_one({"_id": ctx.guild.id})
        prefix = data["prefix"]
        output = f'Prefix in db = `{prefix}`\n'
        output += f'Datas in db blacklist = {count_all}\n'
        output += f'Datas not containing minage message in db blacklist = {count_mng_msg}'
        await ctx.reply(output, mention_author = False)

    @commands.command(aliases=["r"])
    @commands.is_owner()
    async def restart(self, ctx):
        ch = loadrestart()

        embed=discord.Embed(title=":arrows_counterclockwise:",description="Bot is restarting...", colour=0xf1e40f)
        msg = await ctx.send(embed=embed)
        mid = msg.id
        ch['Restart Message'] = ctx.message.channel.id, mid

        writerestart(ch)
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(aliases=['cp'])
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator = True))
    async def changeprefix(self, ctx, prefix):
        collection = i.loadsettings()
        collection.update_one({"_id": ctx.guild.id}, {"$set":{"prefix":prefix}})
        await ctx.reply(f'Prefix changed to: `{prefix}`', mention_author = False)

    @commands.command(aliases = ['filtering'])
    @commands.has_permissions(manage_guild = True)
    async def filter(self, ctx, arg):
        output = filtering_func(ctx, arg)
        await ctx.reply(output, mention_author = False)

    # Voice Link

    @commands.group(invoke_without_command=True, aliases = ['vl'])
    @commands.bot_has_permissions(manage_roles = True)
    async def voicelink(self, ctx, arg):
        collection = i.loadsettings()
        voicelink_role = i.check_voicelink_role(ctx, collection)
        if voicelink_role:
            voicelink_role = ctx.guild.get_role(voicelink_role)
        output = voicelink_func(ctx, arg, voicelink_role, collection)
        await ctx.reply(output, mention_author = False, allowed_mentions = discord.AllowedMentions.none())

    @voicelink.command(name='role')
    @commands.has_permissions(manage_roles = True)
    async def voicelink_role(self, ctx, role: discord.Role = None):
        collection = i.loadsettings()
        if role:
            await ctx.reply(f"Voice link role has been set to {role.mention}", mention_author = False)
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"voicelink.role":role.id}})
        else:
            role = i.check_voicelink_role(ctx, collection)
            if not role:
                await ctx.reply('No voice link role was set.', mention_author = False)
            else:
                role = ctx.guild.get_role(role)
                await ctx.reply(f"Voice link role is set to {role.mention}\nRun `voicelink off` to turn off voice link.", mention_author = False, allowed_mentions = discord.AllowedMentions.none())

    # Stream Link

    @commands.group(invoke_without_command=True, aliases = ['sl'])
    @commands.bot_has_permissions(manage_roles = True)
    async def streamlink(self, ctx, arg):
        collection = i.loadsettings()
        streamlink_role = i.check_streamlink_role(ctx, collection)
        if streamlink_role:
            streamlink_role = ctx.guild.get_role(streamlink_role)
        output = streamlink_func(ctx, arg, streamlink_role, collection)
        await ctx.reply(output, mention_author = False, allowed_mentions = discord.AllowedMentions.none())

    @streamlink.command(name='role')
    @commands.has_permissions(manage_roles = True)
    async def streamlink_role(self, ctx, role: discord.Role = None):
        collection = i.loadsettings()
        if role:
            await ctx.reply(f"Stream link role has been set to {role.mention}", mention_author = False)
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"streamlink.role":role.id}})
        else:
            role = i.check_streamlink_role(ctx, collection)
            if not role:
                await ctx.reply('No stream link role was set.', mention_author = False)
            else:
                role = ctx.guild.get_role(role)
                await ctx.reply(f"Stream link role is set to {role.mention}\nRun `streamlink off` to turn off stream link.", mention_author = False, allowed_mentions = discord.AllowedMentions.none())

    # nodiscussion

    @commands.group(invoke_without_command=True, aliases = ['nd'])
    @commands.bot_has_permissions(manage_messages = True)
    async def nodiscussion(self, ctx, arg):
        collection = i.loadsettings()
        nodiscussion_channels = i.check_nodiscussion_channels(ctx, collection)
        states = collection.find({"nodiscussion.state": {"$exists": True, "$ne": None}})
        if collection.count_documents({}) == collection.count_documents({"nodiscussion.state": {"$exists": False}}):
            current_setting = None
        else:
            for state in states:
                if state["_id"] == ctx.guild.id:
                    current_setting = state["nodiscussion"]["state"]
                    break
                else:
                    current_setting = None
                    
        if arg == 'on':
            if not current_setting:
                collection.update_one({"_id": ctx.guild.id}, {"$set":{"nodiscussion.state":True}})
                output = "NoDiscussion has been enabled. Don't forget to nodiscussion channels.\nRun `help nodiscussion` for more information."
            else:
                output = "NoDiscussion is already enabled."
        elif arg == 'off':
            if current_setting:
                collection.update_one({"_id": ctx.guild.id}, {"$set":{"nodiscussion.state":False}})
                output = "NoDiscussion has been disabled."
            else:
                output = "NoDiscussion is already disabled."
        elif arg == 'status':
            output = "Current state of NoDiscussion: "
            if not current_setting:
                output += "disabled.\n"
            else:
                output += "enabled.\n"
            if nodiscussion_channels:
                ch = ''
                for channel in nodiscussion_channels:
                    valid_channel = self.client.get_channel(channel)
                    ch += f"{valid_channel.mention} "
                output += f"NoDiscussion channels: {ch}"
        else:
            output = "Invalid argument. Please run `help nodiscussion` to see full information."

        await ctx.reply(output, mention_author = False, allowed_mentions = discord.AllowedMentions.none())

    @nodiscussion.command(name='channel')
    @commands.has_permissions(manage_guild = True)
    async def nodiscussion_channels(self, ctx, *args: discord.TextChannel):
        collection = i.loadsettings()
        embed_body = ''
        dupes = []
        not_dupes = []
        if args:
            for arg in args:
                dupe = collection.find_one({"_id":ctx.guild.id, "nodiscussion.channels": {"$in": [arg.id], "$ne":None}})
                if not dupe:
                    collection.update_one({"_id": ctx.guild.id}, {"$addToSet":{"nodiscussion.channels":arg.id}})
                    not_dupes.append(arg)
                else:
                    dupes.append(arg)
            channels = "".join(f"{not_dupe.mention} "for not_dupe in not_dupes)
            dupe_output = "".join(f"{channel.mention} " for channel in dupes)
            embed_body += f'**Channels added:** {channels}\n'
            embed_body += f'**Duplicates:** {dupe_output}'
            em = discord.Embed(description= f'{embed_body}', colour=0x00ff10, timestamp = pen.now('Asia/Jakarta'))
            em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please provide channels to implement nodiscussion.', mention_author = False)

    @nodiscussion.command(name='ignore')
    @commands.has_permissions(manage_guild = True)
    async def nodiscussion_ignore_role(self, ctx, *args: discord.Role):
        collection = i.loadsettings()
        embed_body = ''
        dupes = []
        not_dupes = []
        if args:
            for arg in args:
                dupe = collection.find_one({"_id":ctx.guild.id, "nodiscussion.ignored_roles": {"$in": [arg.id], "$ne":None}})
                if not dupe:
                    collection.update_one({"_id": ctx.guild.id}, {"$addToSet":{"nodiscussion.ignored_roles":arg.id}})
                    not_dupes.append(arg)
                else:
                    dupes.append(arg)
            roles = "".join(f"{not_dupe.mention} "for not_dupe in not_dupes)
            dupe_output = "".join(f"{role.mention} " for role in dupes)
            embed_body += f'**Ignored** {roles}\n'
            embed_body += f'**Duplicates:** {dupe_output}'
            em = discord.Embed(description= f'{embed_body}', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
            em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please provide roles to be ignored by nodiscussion.', mention_author = False)

    @nodiscussion.command(name='unignore')
    @commands.has_permissions(manage_guild = True)
    async def nodiscussion_unignore_role(self, ctx, *args: discord.TextChannel):
        collection = i.loadsettings()
        embed_body = ''
        dupes = []
        not_dupes = []
        if args:
            for arg in args:
                dupe = collection.find_one({"_id":ctx.guild.id, "nodiscussion.ignored_roles": {"$in": [arg.id], "$ne":None}})
                if dupe:
                    collection.update_one({"_id": ctx.guild.id}, {"$pull":{"nodiscussion.ignored_roles":arg.id}})
                    dupes.append(arg)
                else:
                    not_dupes.append(arg)
            not_found = "".join(f"{not_dupe.mention} "for not_dupe in not_dupes)
            dupe_output = "".join(f"{role.mention} " for role in dupes)
            embed_body += f'**Unignored** {dupe_output}\n'
            embed_body += f'**Not found:** {not_found}'
            em = discord.Embed(description= f'{embed_body}', colour=0x00ff10, timestamp = pen.now('Asia/Jakarta'))
            em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please provide channels to unignore.', mention_author = False)

    @nodiscussion.command(name='ignored')
    @commands.has_permissions(manage_messages = True)
    async def nodiscussion_ignored(self, ctx):
        collection = i.loadsettings()
        embed_body = ''
        ignored_roles = i.check_ignored_role_nd(ctx, collection)
        for role in ignored_roles:
            valid_role = ctx.guild.get_role(role)
            embed_body += f'{valid_role.mention} '
        em = discord.Embed(title= 'Ignored roles:', description= f'{embed_body}', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    @nodiscussion.command(name='remove')
    @commands.has_permissions(manage_guild = True)
    async def nodiscussion_remove(self, ctx, *args: discord.TextChannel):
        collection = i.loadsettings()
        embed_body = ''
        dupes = []
        not_dupes = []
        if args:
            for arg in args:
                dupe = collection.find_one({"_id":ctx.guild.id, "nodiscussion.channels": {"$in": [arg.id], "$ne":None}})
                if dupe:
                    collection.update_one({"_id": ctx.guild.id}, {"$pull":{"nodiscussion.channels":arg.id}})
                    dupes.append(arg)
                else:
                    not_dupes.append(arg)
            not_found = "".join(f"{not_dupe.mention} "for not_dupe in not_dupes)
            dupe_output = "".join(f"{channel.mention} " for channel in dupes)
            embed_body += f'**Channels removed:** {dupe_output}\n'
            embed_body += f'**Not found:** {not_found}'
            em = discord.Embed(description= f'{embed_body}', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
            em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please provide channels to remove from nodiscussion.', mention_author = False)

    # Minage

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(kick_members = True)
    async def minage(self, ctx, days: int = None):
        collection = i.loadsettings()
        if days == None:
            guild_settings = collection.find_one({"_id": ctx.guild.id})
            min_age = guild_settings['minage']['days']
            output = f"Current minimum age setting is set to `{min_age}` day(s)."
            if min_age > 0:
                output += '\nSet to `0` to disable minage.'
            await ctx.reply(output)
        else:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"minage.days":days}})
            await ctx.reply(f"Minimum age setting has been set to `{days}` day(s).\nSee more information in `help minage`.")

    @minage.command(name='message')
    @commands.has_permissions(manage_guild = True)
    async def minage_message(self, ctx, *, msg):
        collection = i.loadsettings()
        if msg == 'remove':
            collection.update_one({"_id": ctx.guild.id}, {"$unset":{"minage.message":""}})
            await ctx.reply("Minage message has been removed. Will be back using the default one.", mention_author = False)
        else:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"minage.message":msg}})
            await ctx.reply(f"Message has been set to\n```\n{msg}```", mention_author = False)

    @minage.command(name='channel')
    @commands.has_permissions(manage_guild = True)
    async def minage_channel(self, ctx, ch: discord.TextChannel = None):
        collection = i.loadsettings()
        if ch:
            try:
                await ch.send("This channel is set to be minage logging channel.")
                await ctx.reply(f"Logs channel has been set to {ch.mention}", mention_author = False)
                collection.update_one({"_id": ctx.guild.id}, {"$set":{"minage.logging_channel":ch.id}})
            except Forbidden as f:
                await ctx.reply("Can't set that channel as logging channel because bot doesn't have access or can't send messages to that channel.")
        else:
            if collection.count_documents({}) != collection.count_documents({"minage.logging_channel": {"$exists": False}}):
                collection.update_one({"_id": ctx.guild.id}, {"$unset":{"minage.logging_channel":""}})
                await ctx.reply("Minage channel has been removed. Bot won't log minage actions anymore.", mention_author = False)
            else:
                await ctx.reply("No minage channel was set.", mention_author = False)

    @minage.command(name='settings', aliases = ["check", "setting"])
    @commands.has_permissions(manage_messages = True)
    async def minage_settings(self, ctx):
        collection = i.loadsettings()
        guild_settings = collection.find_one({"_id": ctx.guild.id})
        min_age = guild_settings['minage']['days']
        chk_minage_msg = management_check_minage_msg(ctx, collection, min_age)
        chk_minage_ch = i.check_minage_channel(ctx, collection)
        embed_body = f"**Minage:** `{min_age} day(s)`\n"
        if chk_minage_ch:
            log_channel = self.client.get_channel(chk_minage_ch)
            embed_body += f'**Minage logging channel:** {log_channel.mention}\n'
        embed_body += f"**Minage message:**\n```\n{chk_minage_msg}```"
        em = discord.Embed(title = 'Current minage settings for this server', description = embed_body, colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    # Logging

    @commands.group(aliases = ['logging'], invoke_without_command=True)
    @commands.has_permissions(manage_guild = True)
    async def log(self, ctx, arg):
        collection = i.loadsettings()
        deleted_log_channel = i.check_deleted_logging_channel(ctx, collection)
        edited_log_channel = i.check_edited_logging_channel(ctx, collection)
        if deleted_log_channel:
            deleted_log_channel = self.client.get_channel(deleted_log_channel)
        else: deleted_log_channel = None
        if edited_log_channel:
            edited_log_channel = self.client.get_channel(edited_log_channel)
        else: edited_log_channel = None
        output = logging_func(ctx, arg, deleted_log_channel, edited_log_channel, collection)
        await ctx.reply(output, mention_author = False)

    @log.group(name='channel')
    @commands.has_permissions(manage_guild = True)
    async def log_channel(self, ctx):
        if ctx.invoked_subcommand:
            pass
        else:
            await ctx.reply('Please provide module to execute. Run `help log` to see more information.', mention_author = False)

    @log_channel.command(name='both')
    @commands.has_permissions(manage_guild = True)
    async def log_both(self, ctx, ch: discord.TextChannel):
        collection = i.loadsettings()
        try:
            await ch.send("This channel is set to be messages log channel.\nPlease check `log status` to make sure messages log has been turned on.")
            await ctx.reply(f"Logging channel has been set to {ch.mention}", mention_author = False)
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.edited_msg_channel":ch.id}})
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.deleted_msg_channel":ch.id}})
        except Forbidden as f:
            if '50001' in str(f):
                await ctx.reply("Can't set that channel as logging channel because bot doesn't have access or can't send messages to that channel.")

    @log_channel.command(name='deleted')
    @commands.has_permissions(manage_guild = True)
    async def log_deleted(self, ctx, ch: discord.TextChannel = None):
        collection = i.loadsettings()
        if ch:
            try:
                await ch.send("This channel is set to be deleted messages logging channel.\nPlease check `log status` to make sure messages log has been turned on.")
                await ctx.reply(f"Deleted messages logs channel has been set to {ch.mention}", mention_author = False)
                collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.deleted_msg_channel":ch.id}})
            except Forbidden as f:
                if '50001' in str(f):
                    await ctx.reply("Can't set that channel as logging channel because bot doesn't have access or can't send messages to that channel.")
        else:
            check = collection.find({"logging.deleted_msg_channel": {"$exists": True}})
            found = False
            if collection.count_documents({}) != collection.count_documents({"logging.deleted_msg_channel": {"$exists": False}}):
                for guild in check:
                    if guild["_id"] == ctx.guild.id:
                        collection.update_one({"_id": ctx.guild.id}, {"$unset":{"logging.deleted_msg_channel":""}})
                        found = True
                        break
                if not found:
                    await ctx.reply('No logging channel was set.', mention_author = False)
                else:
                    await ctx.reply("Logging channel has been removed. Deleted message logs has been stopped.", mention_author = False)
            else:
                await ctx.reply("No logging channel was set.", mention_author = False)

    @log_channel.command(name='edited')
    @commands.has_permissions(manage_guild = True)
    async def log_edited(self, ctx, ch: discord.TextChannel = None):
        collection = i.loadsettings()
        if ch:
            try:
                await ch.send("This channel is set to be edited messages logging channel.\nPlease check `log status` to make sure messages log has been turned on.")
                await ctx.reply(f"Edited messages logs channel has been set to {ch.mention}", mention_author = False)
                collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.edited_msg_channel":ch.id}})
            except Forbidden as f:
                if '50001' in str(f):
                    await ctx.reply("Can't set that channel as logging channel because bot doesn't have access or can't send messages to that channel.")
        else:
            check = collection.find({"logging.edited_msg_channel": {"$exists": True}})
            found = False
            if collection.count_documents({}) != collection.count_documents({"logging.edited_msg_channel": {"$exists": False}}):
                for guild in check:
                    if guild["_id"] == ctx.guild.id:
                        collection.update_one({"_id": ctx.guild.id}, {"$unset":{"logging.edited_msg_channel":""}})
                        found = True
                        break
                if not found:
                    await ctx.reply('No logging channel was set.', mention_author = False)
                else:
                    await ctx.reply("Logging channel has been removed. Edited message logs has been stopped.", mention_author = False)
            else:
                await ctx.reply("No logging channel was set.", mention_author = False)

    @log_channel.command(name='remove')
    @commands.has_permissions(manage_guild = True)
    async def log_remove(self, ctx):
        collection = i.loadsettings()
        check = collection.find({"logging.deleted_msg_channel": {"$exists": True}})
        check2 = collection.find({"logging.edited_msg_channel": {"$exists": True}})
        condition1 = collection.count_documents({}) != collection.count_documents({"logging.deleted_msg_channel": {"$exists": False}})
        condition2 = collection.count_documents({}) != collection.count_documents({"logging.edited_msg_channel": {"$exists": False}})
        found = False
        found2 = False
        if condition1:
            for guild in check:
                if guild["_id"] == ctx.guild.id:
                    collection.update_one({"_id": ctx.guild.id}, {"$unset":{"logging.deleted_msg_channel":""}})
                    found = True
                    break
        if condition2:
            for guild in check2:
                if guild["_id"] == ctx.guild.id:
                    collection.update_one({"_id": ctx.guild.id}, {"$unset":{"logging.edited_msg_channel":""}})
                    found2 = True
                    break
        collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.state":False}})
        if found and found2:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.state":False}})
            await ctx.reply("Logging channels has been removed.\nMessage logs has been stopped.", mention_author = False)
        elif found and not found2:
            await ctx.reply('Deleted messages logging channel has been removed.\nDeleted message logs has been stopped.', mention_author = False)
        elif not found and found2:
            await ctx.reply('Edited messages logging channel has been removed.\nEdited message logs has been stopped.', mention_author = False)
        else:
            await ctx.reply('No log channels have been set.', mention_author = False)

    @log.command(name='ignore')
    @commands.has_permissions(manage_guild = True)
    async def log_ignore(self, ctx, *args: discord.TextChannel):
        collection = i.loadsettings()
        embed_body = ''
        dupes = []
        not_dupes = []
        if args:
            for arg in args:
                dupe = collection.find_one({"_id":ctx.guild.id, "logging.ignored_channel": {"$in": [arg.id], "$ne":None}})
                if not dupe:
                    collection.update_one({"_id": ctx.guild.id}, {"$addToSet":{"logging.ignored_channel":arg.id}})
                    not_dupes.append(arg)
                else:
                    dupes.append(arg)
            channels = "".join(f"{not_dupe.mention} "for not_dupe in not_dupes)
            dupe_output = "".join(f"{channel.mention} " for channel in dupes)
            embed_body += f'**Ignored** {channels}\n'
            embed_body += f'**Duplicates:** {dupe_output}'
            em = discord.Embed(description= f'{embed_body}', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
            em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please provide channels to ignore.', mention_author = False)

    @log.command(name='ignored')
    @commands.has_permissions(manage_messages = True)
    async def log_ignored(self, ctx):
        collection = i.loadsettings()
        embed_body = ''
        ignored_channels = i.check_ignored_channel(ctx, collection)
        for channel in ignored_channels:
            valid_channel = self.client.get_channel(channel)
            embed_body += f'{valid_channel.mention} '
        em = discord.Embed(title= 'Ignored channels:', description= f'{embed_body}', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    @log.command(name='unignore')
    @commands.has_permissions(manage_guild = True)
    async def log_unignore(self, ctx, *args: discord.TextChannel):
        collection = i.loadsettings()
        embed_body = ''
        dupes = []
        not_dupes = []
        if args:
            for arg in args:
                dupe = collection.find_one({"_id":ctx.guild.id, "logging.ignored_channel": {"$in": [arg.id], "$ne":None}})
                if dupe:
                    collection.update_one({"_id": ctx.guild.id}, {"$pull":{"logging.ignored_channel":arg.id}})
                    dupes.append(arg)
                else:
                    not_dupes.append(arg)
            not_found = "".join(f"{not_dupe.mention} "for not_dupe in not_dupes)
            dupe_output = "".join(f"{channel.mention} " for channel in dupes)
            embed_body += f'**Unignored** {dupe_output}\n'
            embed_body += f'**Not found:** {not_found}'
            em = discord.Embed(description= f'{embed_body}', colour=0x00ff10, timestamp = pen.now('Asia/Jakarta'))
            em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please provide channels to unignore.', mention_author = False)

    # Error handler

    @leaveguild.error
    async def leaveguild_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing guild ID.', mention_author = False)
        elif isinstance(error, commands.CommandInvokeError) and 'TimeoutError' in str(error):
            await ctx.reply('You ran out of time.')

    @voicelink.error
    async def voicelink_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing argument, see `help voicelink` to see full information.', mention_author = False)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("Can't set voicelink when I don't have `Manage Roles` permission.", mention_author = False)

    @streamlink.error
    async def streamlink_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing argument, see `help streamlink` to see full information.', mention_author = False)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("Can't set streamlink when I don't have `Manage Roles` permission.", mention_author = False)

    @nodiscussion.error
    async def nodiscussion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing argument, see `help nodiscussion` for full information.')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("Can't set nodiscussion when I don't have `Manage Messages` permission.", mention_author = False)

    @nodiscussion_channels.error
    async def nodiscussion_channels_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")

    @nodiscussion_ignore_role.error
    async def nodiscussion_ignore_role_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Role(s) can't be recognized. Please mention roles you want to ignore to avoid minor mistakes.")

    @nodiscussion_unignore_role.error
    async def nodiscussion_unignore_role_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Role(s) can't be recognized. Please mention roles you want to unignore to avoid minor mistakes.")

    @nodiscussion_remove.error
    async def nodiscussion_remove_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")

    @minage.error
    async def minage_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply('Wrong module to execute. Run `help minage` to see full information.', mention_author = False)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("Can't set minage when I don't have `Kick Members` permission.", mention_author = False)

    @minage_message.error
    async def minage_message_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please set your message.', mention_author = False)

    @filter.error
    async def filter_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please decide whether to toggle `on`/`off`, `status` to see the current status of filtering, or if you'd like to see the `list` of blacklisted clipper.", mention_author = False)

    @log.error
    async def log_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing argument, see `help log` for full information.')

    @log_both.error
    async def log_both_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please provide channel for logging.", mention_author = False)

    @log_deleted.error
    async def log_deleted_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")

    @log_edited.error
    async def log_edited_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")

    @log_ignore.error
    async def log_ignore_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channels you want to ignore to avoid minor mistakes.")

    @log_unignore.error
    async def log_unignore_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channels you want to unignore to avoid minor mistakes.")

def setup(client):
    client.add_cog(Management(client))
