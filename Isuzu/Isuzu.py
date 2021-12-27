import nextcord as discord
import os
import asyncio
import sys
import json
import pendulum as pen
from pymongo import MongoClient
from nextcord.ext import commands
from nextcord.errors import Forbidden
from dotenv import load_dotenv

load_dotenv()

default_prefix = 'i/'
DB_URL = os.getenv('DB_URL')
connection_url = str(DB_URL)

def loadsettings():
    cluster = MongoClient(connection_url)
    db = cluster["IsuzuDB"]
    collection = db["server_settings"]
    return collection

def get_prefix(client, message):
    collection = loadsettings()
    data = collection.find_one({"_id": message.guild.id})
    prefix = data["prefix"]
    return commands.when_mentioned_or(prefix)(client, message)

def get_prefix_str(message):
    collection = loadsettings()
    data = collection.find_one({"_id": message.guild.id})
    prefix = data["prefix"]
    return prefix

def loadblacklistedYT():
    cluster = MongoClient(connection_url)
    db = cluster["IsuzuDB"]
    collection = db["blacklisted_YT"]
    return collection

def loadrestart():
    with open('./resources/RestartMsg.json', 'r') as f:
        ch = json.load(f)
    return ch    
    
def writerestart(ch):
    with open('./resources/RestartMsg.json', 'w') as f:
        json.dump(ch, f, indent=4)

def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)

def filtering_toggle(message):
    collection = loadsettings()
    data = collection.find_one({"_id": message.guild.id})
    toggle = data["filtering"]
    return toggle

def filtering_func(ctx, arg):
    collection = loadsettings()
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
        collectionYT = loadblacklistedYT()
        channels = collectionYT.find({})
        output = "".join(f'{channel["name"]}\n' for channel in channels)
        return f'Blacklisted channels:```{output}```'
    elif arg == 'status':
        if not current_settings:
            return 'Current state of filtering: disabled.'
        else:
            return 'Current state of filtering: enabled.'
    else:
        return "Invalid argument. Please run `help filtering` to see full information."

def check_minage_msg(context, collection, min_age):
    default_message = f"You have been kicked from {context.guild.name} due to your account age being less than {min_age} day(s). Please feel free to attempt to rejoin after your account has had some time to mature."
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
            if '{minage}' in msg["minage"]["message"]:
                converted_minage_message = msg_var.replace('{minage}', str(min_age))
                return converted_minage_message
            else:
                return msg_var
        else:
            return default_message

def check_minage_channel(context, collection):
    logging_channel = collection.find({"minage.logging_channel": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"minage.logging_channel": {"$exists": False}}):
        return None
    else:
        for channel in logging_channel:
            if channel["_id"] == context.guild.id:
                return channel["minage"]["logging_channel"]

def logging_toggle(message):
    collection = loadsettings()
    toggle = False
    logging_state = collection.find({"logging.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"logging.state": {"$exists": False}}):
        return toggle
    else:
        for state in logging_state:
            if state["_id"] == message.guild.id:
                toggle = state["logging"]["state"]
    return toggle

def check_deleted_logging_channel(ctx, collection):
    logging_channel = collection.find({"logging.deleted_msg_channel": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"logging.deleted_msg_channel": {"$exists": False}}):
        return None
    else:
        for channel in logging_channel:
            if channel["_id"] == ctx.guild.id:
                return channel["logging"]["deleted_msg_channel"]

def check_edited_logging_channel(ctx, collection):
    logging_channel = collection.find({"logging.edited_msg_channel": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"logging.edited_msg_channel": {"$exists": False}}):
        return None
    else:
        for channel in logging_channel:
            if channel["_id"] == ctx.guild.id:
                return channel["logging"]["edited_msg_channel"]

def check_ignored_channel(context, collection):
    logging_channel = collection.find({"logging.ignored_channel": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"logging.ignored_channel": {"$exists": False}}):
        return None
    else:
        for channel in logging_channel:
            if channel["_id"] == context.guild.id:
                return channel["logging"]["ignored_channel"]

def logging_func(ctx, arg, deleted_log_channel, edited_log_channel, collection):
    states = collection.find({"logging.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"logging.state": {"$exists": False}}):
        current_setting = None
    else:
        for state in states:
            if state["_id"] == ctx.guild.id:
                current_setting = state["logging"]["state"]
                break
            
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

def main():

    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents().all()
    client = commands.Bot(command_prefix = get_prefix, intents = intents, help_command = None)

    WIB = 'Asia/Jakarta'
    myid = 302064098739355652 # Change this with your own discord user ID if you're going to host this bot yourself

    async def status_task():
        while True:
            dtN = pen.now(WIB)
            await client.change_presence(activity=discord.Game(dtN.format("HH:mm zz, D MMM YYYY")))
            await asyncio.sleep(5)

    @client.event
    async def on_ready():
        client.loop.create_task(status_task())
        ch = loadrestart()
        try:
            if ch:
                channel = client.get_channel(ch['Restart Message'][0])
                msg = await channel.fetch_message(ch['Restart Message'][1])
                em = discord.Embed(title=":white_check_mark:",description="Restart complete.", colour=0x00ff10)
                await msg.edit(embed = em)

                ch.clear()
                writerestart(ch)
            else:
                None
        except Exception as e:
            ch.clear()
            writerestart(ch)
            print(e)

    @client.event
    async def on_guild_join(guild):
        collection = loadsettings()
        default_assigned = {"_id":guild.id, "prefix": default_prefix, "minage": {"days":0}, "filtering": False}
        collection.insert_one(default_assigned)

    @client.event
    async def on_guild_remove(guild):
        collection = loadsettings()
        collection.delete_one({"_id":guild.id})

    @client.listen()
    async def on_message(message):
        if not message.guild: return
        
        if not message.author.bot:
            if filtering_toggle(message):    
                await asyncio.sleep(1)
                collection = loadblacklistedYT()
                blacklistedID = collection.find({})
                found = False
                images = collection.find({"imageURL": {"$exists": True, "$ne": None}})
                embed = message.embeds[0] if message.embeds else None
                try:
                    if embed:
                        text = embed.to_dict()
                        for blacklisted in blacklistedID:
                            if blacklisted["_id"] in text["author"]["url"]:
                                document = blacklisted
                                em = discord.Embed(title = '**Content Filtering**', description = '**Video from blacklisted YT channel removed**', colour=0xff0000, timestamp = pen.now('Asia/Jakarta'))
                                em.add_field(name = 'Name', value = f"{text['author']['name']}")
                                em.add_field(name = 'Reason for blacklist', value = blacklisted["reason"])
                                em.add_field(name = 'Sources', value = blacklisted["sources"])
                                if images:
                                    for image in images:
                                        if image["_id"] == document["_id"]:
                                            em.set_image(url = image["imageURL"])
                                            break
                                if blacklisted["_id"] == "UCizN2tVLNcwP67bAHlVRg1Q":
                                    em.add_field(name = "Proof addition", value = "Picture below shows one of Iroha's clip description saying it's only their imagination.")

                                em.set_footer(text = f"{message.author.display_name} ({message.author.id})", icon_url = message.author.display_avatar)
                                response = await message.reply(embed = em)
                                await message.delete()
                                found = True
                                break

                        if found:
                            user = await client.fetch_user(myid)
                            await user.send(f'{message.author.name}#{message.author.discriminator} posted a blacklisted clipper video in {message.guild.name}.\n{response.jump_url}')
                except Exception as e:
                    print(e)
        else:
            return

    @client.event
    async def on_bulk_message_delete(messages):
        for message in messages:
            if not message.guild: return
            if message.author.bot: return
        if logging_toggle(message):
            collection = loadsettings()
            ignored_channels = check_ignored_channel(message, collection)
            if ignored_channels and message.channel.id in ignored_channels: return
            else:
                channel_deleted = check_deleted_logging_channel(message, collection)
                if channel_deleted:
                    deleted_log_channel = client.get_channel(channel_deleted)
                else: return

                if message.guild.me.guild_permissions.view_audit_log:
                    async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_bulk_delete):
                        executor = f'{entry.user.mention} ({entry.user.name}#{entry.user.discriminator})'
                        break
                else:
                    executor = "*(bot doesn't have view audit log permission)*"

                embed_body = f"**{len(messages)} messages deleted in bulk in {message.channel.mention}**\n"
                embed_body += f'\n**Perpetrator:** {executor}'
                em = discord.Embed(description= embed_body, colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                await deleted_log_channel.send(embed = em)

    @client.event
    async def on_message_delete(message):
        if not message.guild: return
        if message.author.bot: return
        if logging_toggle(message):
            collection = loadsettings()
            ignored_channels = check_ignored_channel(message, collection)
            if ignored_channels and message.channel.id in ignored_channels: return
            else:
                channel_deleted = check_deleted_logging_channel(message, collection)
                if channel_deleted:
                    deleted_log_channel = client.get_channel(channel_deleted)
                else: return

                embed_body = f"**Message by {message.author.mention} deleted in {message.channel.mention}**"
                embed_body1 = f"**Message by {message.author.mention} deleted in {message.channel.mention}**"
                if message.content: 
                    embed_body += f'\n{message.content}'
                file_contained = discord.Attachment
                if message.attachments:
                    for file_contained in message.attachments:
                        if not (file_contained.content_type).startswith("image"):
                            embed_body += f'\n{file_contained.url}'
                if message.stickers:
                    embed_body += '\n**(Message contained sticker)**'

                em = discord.Embed(description= embed_body, colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                em1 = discord.Embed(description= embed_body1, colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                if message.author.nick:
                    em.set_author(name = f'{message.author.name}#{message.author.discriminator}  ({message.author.nick})', icon_url = message.author.display_avatar)
                    em1.set_author(name = f'{message.author.name}#{message.author.discriminator}  ({message.author.nick})', icon_url = message.author.display_avatar)
                else:
                    em.set_author(name = f'{message.author.name}#{message.author.discriminator}', icon_url = message.author.display_avatar)
                    em1.set_author(name = f'{message.author.name}#{message.author.discriminator}', icon_url = message.author.display_avatar)
                if message.content or not str(file_contained.content_type).startswith("image"):
                    em.set_thumbnail(url = message.author.display_avatar)
                em.set_footer(text = f"Author ID: {message.author.id} | Message ID {message.id}")
                em1.set_footer(text = f"Author ID: {message.author.id} | Message ID {message.id}")

                if message.stickers:
                    for sticker in message.stickers:
                        sticker_url = sticker.url

                if message.attachments and len(message.attachments) == 1:
                    if message.stickers:
                        em.set_image(url = sticker_url)
                        await deleted_log_channel.send(embed = em)
                        for image in message.attachments:
                            if (image.content_type).startswith("image"):
                                em1.set_image(url = image.url)
                                await deleted_log_channel.send(embed = em1)
                    else: 
                        for image in message.attachments:
                            if (image.content_type).startswith("image"):
                                em.set_image(url = image.url)
                            await deleted_log_channel.send(embed = em)

                elif message.attachments and len(message.attachments) > 1:
                    if message.stickers:
                        em.set_image(url = sticker_url)
                        await deleted_log_channel.send(embed = em)
                    else: await deleted_log_channel.send(embed = em)
                    for image in message.attachments:
                        if (image.content_type).startswith("image"):
                            em1.set_image(url = image.url)
                            await deleted_log_channel.send(embed = em1)

                elif message.stickers:
                    em.set_image(url = sticker_url)
                    await deleted_log_channel.send(embed = em)

                else:
                    await deleted_log_channel.send(embed = em)

    @client.event
    async def on_message_edit(before, after):
        if not before.guild: return
        if before.author.bot: return
        if before.content == after.content: return
        if logging_toggle(before):
            collection = loadsettings()
            ignored_channels = check_ignored_channel(before, collection)
            if ignored_channels and before.channel.id in ignored_channels: return
            else:
                channel_edited = check_edited_logging_channel(before, collection)
                if channel_edited:
                    edited_log_channel = client.get_channel(channel_edited)
                else: return

                if before.content: 
                    before_body = f'{before.content}\n'
                else: before_body = '<no message>'
                if before.attachments:
                    for file_contained in before.attachments:
                        if not (file_contained.content_type).startswith("image"):
                            before_body += f'{file_contained.url}\n'
                            
                after_body = f'{after.content}\n'
                if after.attachments:
                    for file_contained in after.attachments:
                        if not (file_contained.content_type).startswith("image"):
                            after_body += f'{file_contained.url}\n'
                if before.stickers:
                    after_body += '**\n(Message contained sticker)**'
                after_body += f'\n[Jump to message]({after.jump_url})'

                em = discord.Embed(description=f"**Message by {before.author.mention} edited in {before.channel.mention}**\n", colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
                em.add_field(name="Before", value=before_body)
                em.add_field(name="After", value=after_body, inline=False)
                if before.author.nick:
                    em.set_author(name = f'{before.author.name}#{before.author.discriminator}  ({before.author.nick})', icon_url = before.author.display_avatar)
                else:
                    em.set_author(name = f'{before.author.name}#{before.author.discriminator}', icon_url = before.author.display_avatar)
                em.set_thumbnail(url = before.author.display_avatar)
                em.set_footer(text = f"{after.author.display_name} ({after.author.id})", icon_url = after.author.display_avatar)

                if before.attachments and not before.stickers:
                    for image in before.attachments:
                        if (image.content_type).startswith("image"):
                            em.set_image(url = image.url)
                elif before.stickers:
                    for sticker in before.stickers:
                        em.set_image(url = sticker.url)

            await edited_log_channel.send(embed = em)

    @client.event
    async def on_member_join(member):
        collection = loadsettings()
        guild_settings = collection.find_one({"_id":member.guild.id})
        min_age = guild_settings["minage"]["days"]
        if min_age == 0: return

        minage_seconds = min_age*86400
        age = (pen.now() - member.created_at).total_seconds()
        minage_message = check_minage_msg(member, collection, min_age)
        
        # Check whether logging channel is available
        channel = check_minage_channel(member, collection)
        if channel:
            log_channel = client.get_channel(channel)
        
        reason = f"Account's age ({round(age//86400)} days) is less than the set requirement (>{min_age} days)."
        if member.guild.me.guild_permissions.kick_members:
            if age < minage_seconds:
                await member.send(minage_message)
                await member.kick(reason = reason)
                if channel:
                    embed_body = f'**Kicked** {member.mention} ({member.id})\n'
                    embed_body += '\n'
                    embed_body += f"**For reason:** {reason}"
                    em = discord.Embed(title = "Minage Report", description = embed_body, colour=0xf00000, timestamp = pen.now(WIB))
                    em.set_thumbnail(url = member.display_avatar)
                    em.set_footer(text = f"{member.display_name} ({member.id})", icon_url = member.display_avatar)
                    await log_channel.send(embed = em)
            else: return
        else:
            if channel:
                embed_body = f'**Failed to kick** {member.mention} ({member.id})\n'
                embed_body += '\n'
                embed_body += f"**Reason:** Bot is missing `Kick Members` permission."
                em = discord.Embed(title = "Minage Report", description = embed_body, colour=0xf1e40f, timestamp = pen.now(WIB))
                em.set_thumbnail(url = member.display_avatar)
                em.set_footer(text = f"{member.display_name} ({member.id})", icon_url = member.display_avatar)
                await log_channel.send(embed = em)
            else: return

    @client.event
    async def on_message(message):
        if not message.guild: return

        if (message.content == f"<@!{client.user.id}>" or message.content == f"<@{client.user.id}>"):
            await message.channel.send(f'My prefix here is `{get_prefix_str(message)}`')
        else:
            pass
        await client.process_commands(message)

    # commands

    @client.command()
    @commands.is_owner()
    async def checkdb(ctx):
        collection = loadsettings()
        collection1 = loadblacklistedYT()
        count_all = collection1.count_documents({})
        count_mng_msg = collection1.count_documents({"minage.message": {"$exists": False}})
        data = collection.find_one({"_id": ctx.guild.id})
        prefix = data["prefix"]
        output = f'Prefix in db = `{prefix}`\n'
        output += f'Datas in db blacklist = {count_all}\n'
        output += f'Datas not containing minage message in db blacklist = {count_mng_msg}'
        await ctx.send(output)

    @client.command(aliases=["r"])
    @commands.is_owner()
    async def restart(ctx):
        ch = loadrestart()

        embed=discord.Embed(title=":arrows_counterclockwise:",description="Bot is restarting...", colour=0xf1e40f)
        msg = await ctx.send(embed=embed)
        mid = msg.id
        ch['Restart Message'] = ctx.message.channel.id, mid

        writerestart(ch)
        os.execv(sys.executable, ['python'] + sys.argv)

    @client.command(aliases=['cp'])
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator = True))
    async def changeprefix(ctx, prefix):
        collection = loadsettings()
        collection.update_one({"_id": ctx.guild.id}, {"$set":{"prefix":prefix}})
        await ctx.reply(f'Prefix changed to: `{prefix}`', mention_author = False)

    @client.command(aliases = ['filtering'])
    @commands.has_permissions(manage_guild = True)
    async def filter(ctx, arg):
        output = filtering_func(ctx, arg)
        await ctx.reply(output, mention_author = False)

    # Minage

    @client.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(kick_members = True)
    async def minage(ctx, days: int = None):
        collection = loadsettings()
        if not days: 
            days = 0
        collection.update_one({"_id": ctx.guild.id}, {"$set":{"minage.days":days}})   
        await ctx.reply(f"Minimum age setting has been set to `{days}` day(s).\nSee more information in `help minage`.")

    @minage.command(name='message')
    @commands.has_permissions(manage_guild = True)
    async def minage_message(ctx, *, msg):
        collection = loadsettings()
        if msg == 'remove':
            collection.update_one({"_id": ctx.guild.id}, {"$unset":{"minage.message":""}})
            await ctx.reply("Minage message has been removed. Will be back using the default one.", mention_author = False)
        else:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"minage.message":msg}})
            await ctx.reply(f"Message has been set to ```{msg}```", mention_author = False)

    @minage.command(name='channel')
    @commands.has_permissions(manage_guild = True)
    async def minage_channel(ctx, ch: discord.TextChannel = None):
        collection = loadsettings()
        if ch:
            try:
                await ch.send("This channel is set to be minage logging channel.")
                await ctx.reply(f"Logs channel has been set to {ch.mention}", mention_author = False)
                collection.update_one({"_id": ctx.guild.id}, {"$set":{"minage.logging_channel":ch.id}})
            except Forbidden as f:
                if '50001' in str(f):
                    await ctx.reply("Can't set that channel as logging channel because bot doesn't have access or can't send messages to that channel.")
        else:
            if collection.count_documents({}) != collection.count_documents({"minage.logging_channel": {"$exists": False}}):
                collection.update_one({"_id": ctx.guild.id}, {"$unset":{"minage.logging_channel":""}})
                await ctx.reply("Minage channel has been removed. Bot won't log minage actions anymore.", mention_author = False)
            else:
                await ctx.reply("No minage channel was set.", mention_author = False)

    @minage.command(name='settings', aliases = ["check", "setting"])
    @commands.has_permissions(manage_messages = True)
    async def minage_settings(ctx):
        collection = loadsettings()
        guild_settings = collection.find_one({"_id": ctx.guild.id})
        min_age = guild_settings['minage']['days']
        chk_minage_msg = check_minage_msg(ctx, collection, min_age)
        chk_minage_ch = check_minage_channel(ctx, collection)
        embed_body = f"Minage: `{min_age} day(s)`\n"
        if chk_minage_ch:
            log_channel = client.get_channel(chk_minage_ch)
            embed_body += f'Minage logging channel: {log_channel.mention}\n'
        embed_body += f"Minage message: ```{chk_minage_msg}```"
        em = discord.Embed(title = 'Current minage settings for this server', description = embed_body, colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    # Logging

    @client.group(aliases = ['logging'], invoke_without_command=True)
    @commands.has_permissions(manage_guild = True)
    async def log(ctx, arg):
        collection = loadsettings()
        deleted_log_channel = check_deleted_logging_channel(ctx, collection)
        edited_log_channel = check_edited_logging_channel(ctx, collection)
        if deleted_log_channel:
            deleted_channel = client.get_channel(deleted_log_channel)
        else: deleted_channel = None
        if edited_log_channel:
            edited_log_channel = client.get_channel(edited_log_channel)
        else: edited_log_channel = None
        output = logging_func(ctx, arg, deleted_channel, edited_log_channel, collection)
        await ctx.reply(output, mention_author = False)

    @log.group(name='channel')
    @commands.has_permissions(manage_guild = True)
    async def log_channel(ctx):
        if ctx.invoked_subcommand:
            pass
        else:
            await ctx.reply('Please provide module to execute. Run `help log` to see more information.', mention_author = False)

    @log_channel.command(name='both')
    @commands.has_permissions(manage_guild = True)
    async def log_both(ctx, ch: discord.TextChannel):
        collection = loadsettings()
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
    async def log_deleted(ctx, ch: discord.TextChannel = None):
        collection = loadsettings()
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
                        collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.state":False}})
                        found = True
                        break
                if not found:
                    await ctx.reply('No logging channel was set.', mention_author = False)
                else:
                    await ctx.reply("Logging channel has been removed. Deleted message logs has been stopped", mention_author = False)
            else:
                await ctx.reply("No logging channel was set.", mention_author = False)

    @log_channel.command(name='edited')
    @commands.has_permissions(manage_guild = True)
    async def log_edited(ctx, ch: discord.TextChannel = None):
        collection = loadsettings()
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
                        collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.state":False}})
                        found = True
                        break
                if not found:
                    await ctx.reply('No logging channel was set.', mention_author = False)
                else:
                    await ctx.reply("Logging channel has been removed. Edited message logs has been stopped", mention_author = False)
            else:
                await ctx.reply("No logging channel was set.", mention_author = False)

    @log_channel.command(name='remove')
    @commands.has_permissions(manage_guild = True)
    async def log_remove(ctx):
        collection = loadsettings()
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

        if found and found2:
            collection.update_one({"_id": ctx.guild.id}, {"$set":{"logging.state":False}})
            await ctx.reply("Logging channels has been removed.\nMessage logs has been stopped.", mention_author = False)
        elif found and not found2:
            await ctx.reply('Deleted messages logging channel has been removed.\nDeleted message logs has been stopped.', mention_author = False)
        elif not found and found:
            await ctx.reply('Edited messages logging channel has been removed.\nEdited message logs has been stopped.', mention_author = False)
        else:
            await ctx.reply('No log channels have been set.', mention_author = False)

    @log.command(name='ignore')
    @commands.has_permissions(manage_guild = True)
    async def log_ignore(ctx, *args: discord.TextChannel):
        collection = loadsettings()
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
    @commands.has_permissions(manage_guild = True)
    async def log_ignored(ctx):
        collection = loadsettings()
        embed_body = ''
        ignored_channels = check_ignored_channel(ctx, collection)
        for channel in ignored_channels:
            valid_channel = client.get_channel(channel)
            embed_body += f'{valid_channel.mention} '
        em = discord.Embed(title= 'Ignored channels:', description= f'{embed_body}', colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
        em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em, mention_author = False)

    @log.command(name='unignore')
    @commands.has_permissions(manage_guild = True)
    async def log_unignore(ctx, *args: discord.TextChannel):
        collection = loadsettings()
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

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
            await ctx.reply(message, delete_after=round(error.retry_after), mention_author = False)
        elif isinstance(error, commands.MissingPermissions):
            link = 'https://tenor.com/view/power-lord-of-the-rings-lotr-gif-9197188'
            await ctx.reply("You don't have permission to run this command.")
            await ctx.send(link)
        elif isinstance(error, commands.CheckAnyFailure):
            link = 'https://tenor.com/view/power-lord-of-the-rings-lotr-gif-9197188'
            await ctx.reply("You don't have permission to run this command.")
            await ctx.send(link)
        elif isinstance(error, commands.NotOwner):
            await ctx.reply("Only bot owner can run this command.")
        elif isinstance(error, commands.CommandNotFound): return
        else:
            user = await client.fetch_user(myid)
            await user.send(f"Caught an error from {ctx.guild.name} when executing `{ctx.command.name}` command: ```{error}```")

    @minage.error
    async def minage_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply('Wrong module to execute. Run `help minage` to see full information.', mention_author = False)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("Can't set minage when the bot lacking `Kick Members` permission.", mention_author = False)

    @minage_message.error
    async def minage_message_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please set your message.', mention_author = False)

    @filter.error
    async def filter_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please decide whether to toggle `on` or `off`, or if you'd like to see the `list` of blacklisted clipper.", mention_author = False)

    @log.error
    async def log_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing argument, see `help log` for full information.')

    @log_both.error
    async def log_both_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please provide channel for logging.", mention_author = False)

    @log_deleted.error
    async def log_deleted_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")

    @log_edited.error
    async def log_edited_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channel you want to set to avoid minor mistakes.")

    @log_ignore.error
    async def log_ignore_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channels you want to ignore to avoid minor mistakes.")

    @log_unignore.error
    async def log_unignore_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Channel(s) can't be recognized. Please mention channels you want to unignore to avoid minor mistakes.")

    # Load cogs

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

    client.run(TOKEN)

if __name__ == '__main__':
    main()
