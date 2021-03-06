import nextcord as discord
import os
import re
import asyncio
import cogs.Management as mg
import pendulum as pen
from math import ceil
from pymongo import MongoClient
from nextcord.ext import commands
from dotenv import load_dotenv
from pendulum import datetime as dt

load_dotenv()

default_prefix = 'i/'
DB_URL = os.getenv('DB_URL')
connection_url = str(DB_URL)

# Essential functions

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

def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)

# Filtering function

def filtering_toggle(message):
    collection = loadsettings()
    data = collection.find_one({"_id": message.guild.id})
    toggle = data["filtering"]
    return toggle

# Voicelink functions

def voicelink_toggle(ctx):
    collection = loadsettings()
    toggle = False
    logging_state = collection.find({"voicelink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"voicelink.state": {"$exists": False}}):
        toggle = False
    else:
        for state in logging_state:
            if state["_id"] == ctx.guild.id:
                toggle = state["voicelink"]["state"]
    return toggle

def check_voicelink_role(ctx, collection):
    voicelink_role = collection.find({"voicelink.role": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"voicelink.role": {"$exists": False}}):
        return None
    else:
        for role in voicelink_role:
            if role["_id"] == ctx.guild.id:
                return role["voicelink"]["role"]

# Streamlink functions

def streamlink_toggle(ctx):
    collection = loadsettings()
    toggle = False
    logging_state = collection.find({"streamlink.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"streamlink.state": {"$exists": False}}):
        toggle = False
    else:
        for state in logging_state:
            if state["_id"] == ctx.guild.id:
                toggle = state["streamlink"]["state"]
    return toggle

def check_streamlink_role(ctx, collection):
    streamlink_role = collection.find({"streamlink.role": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"streamlink.role": {"$exists": False}}):
        return None
    else:
        for role in streamlink_role:
            if role["_id"] == ctx.guild.id:
                return role["streamlink"]["role"]

# Nodiscussion functions

def nodiscussion_toggle(message):
    collection = loadsettings()
    toggle = False
    nodiscussion_state = collection.find({"nodiscussion.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"nodiscussion.state": {"$exists": False}}):
        toggle = False
    else:
        for state in nodiscussion_state:
            if state["_id"] == message.guild.id:
                toggle = state["nodiscussion"]["state"]
    return toggle

def check_nodiscussion_channels(context, collection):
    channels = collection.find({"nodiscussion.channels": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"nodiscussion.channels": {"$exists": False}}):
        return None
    else:
        for channel in channels:
            if channel["_id"] == context.guild.id:
                return channel["nodiscussion"]["channels"]

def check_ignored_role_nd(context, collection):
    logging_channel = collection.find({"nodiscussion.ignored_roles": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"nodiscussion.ignored_roles": {"$exists": False}}):
        return None
    else:
        for channel in logging_channel:
            if channel["_id"] == context.guild.id:
                return channel["nodiscussion"]["ignored_roles"]

# Minage functions

def check_minage_msg(context, collection, min_age):
    seconds = min_age*86400
    age = (pen.now() - context.created_at).total_seconds()
    minage_end = ceil(seconds - age)
    epoch = ceil((pen.now().add(seconds=minage_end) - dt(1970, 1, 1)).total_seconds())
    default_message = f"You have been kicked from **{context.guild.name}** due to your account age being less than **{min_age}** day(s). Please feel free to attempt to rejoin on <t:{epoch}:F> or <t:{epoch}:R>."
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
            if '{minage}' in msg_var:
                converted1 = msg_var.replace('{minage}', f'{str(min_age)}')
                converted_minage_message = converted1
                if '{rejoincount}' in converted1:
                    converted2 = converted1.replace('{rejoincount}', f'<t:{epoch}:R>')
                    converted_minage_message = converted2
                    if '{rejoindate}' in converted2:
                        converted_minage_message = converted2.replace('{rejoindate}', f'<t:{epoch}:F>')
                elif '{rejoindate}' in msg_var:
                    converted_minage_message = converted1.replace('{rejoindate}', f'<t:{epoch}:F>')
                return converted_minage_message
            elif '{rejoincount}' in msg_var:
                converted1 = msg_var.replace('{rejoincount}', f'<t:{epoch}:R>')
                converted_minage_message = converted1
                if '{rejoindate}' in converted1:
                    converted_minage_message = converted1.replace('{rejoindate}', f'<t:{epoch}:F>')
                return converted_minage_message
            elif '{rejoindate}' in msg_var:
                converted_minage_message = msg_var.replace('{rejoindate}', f'<t:{epoch}:F>')
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

# Logging functions

def logging_toggle(message):
    collection = loadsettings()
    toggle = False
    logging_state = collection.find({"logging.state": {"$exists": True, "$ne": None}})
    if collection.count_documents({}) == collection.count_documents({"logging.state": {"$exists": False}}):
        toggle = False
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

def main():

    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.all()
    intents.typing = False
    intents.presences = False
    client = commands.Bot(command_prefix = get_prefix, intents = intents, help_command = None)

    WIB = 'Asia/Jakarta'
    myid = 302064098739355652  # change this to your ID
    ServersImod = [913649915467542529, 862115140345135125] # change this to server IDs of the server you mod (optional)

    async def status_task():
        await client.change_presence(activity=discord.Game('with your life'))

    @client.event
    async def on_ready():
        client.loop.create_task(status_task())
        ch = mg.loadrestart()
        try:
            if ch:
                channel = client.get_channel(ch['Restart Message'][0])
                msg = await channel.fetch_message(ch['Restart Message'][1])
                em = discord.Embed(title=":white_check_mark:",description="Restart complete.", colour=0x00ff10, timestamp = pen.now(WIB))
                await msg.edit(embed = em)

                ch.clear()
                mg.writerestart(ch)
            else:
                None
        except Exception as e:
            ch.clear()
            mg.writerestart(ch)
            print(e)

    @client.event
    async def on_guild_join(guild):
        collection = loadsettings()
        data = collection.find_one({"_id": guild.id})
        if not data:
            default_assigned = {"_id":guild.id, "prefix": default_prefix, "minage": {"days":0}, "filtering": False}
            collection.insert_one(default_assigned)
        else: return

    @client.listen()
    async def on_guild_join(guild):
        user = await client.fetch_user(myid)
        embed_body = f"**{client.user.name} joined {guild.name}.**"
        em = discord.Embed(description=embed_body, colour=0xcaa686, timestamp = pen.now(WIB))
        em.set_author(name = f'{guild.owner.name}#{guild.owner.discriminator}', icon_url = guild.owner.display_avatar)
        em.set_thumbnail(url = guild.display_avatar)
        await user.send(embed = em)

    @client.event
    async def on_thread_join(thread):
        try:
            await thread.join()
        except:
            pass

    @client.event
    async def on_message(message):
        if not message.guild: return

        if (message.content == f"<@!{client.user.id}>" or message.content == f"<@{client.user.id}>"):
            await message.reply(f'My prefix here is `{get_prefix_str(message)}`', mention_author = False)
        else:
            pass
        await client.process_commands(message)

    @client.listen()
    async def on_message(message):
        await asyncio.sleep(2)        
        if message.guild or message.author.bot: return

        user = await client.fetch_user(myid)

        embed_body = f'**{message.author.mention} sent me a message.**\n'
        if message.content: 
            embed_body += f'\n{message.content}'
        if message.attachments:
            for file_contained in message.attachments:
                if not (file_contained.content_type).startswith("image"):
                    embed_body += f'\n{file_contained.url}'
        if message.stickers:
            embed_body += '\n**(Message contained sticker)**'
        em = discord.Embed(description=embed_body, colour=0xcaa686, timestamp = pen.now(WIB))
        em1 = discord.Embed(description=embed_body, colour=0xcaa686, timestamp = pen.now(WIB))
        em.set_author(name = f'{message.author.name}#{message.author.discriminator}', icon_url = message.author.display_avatar)
        em1.set_author(name = f'{message.author.name}#{message.author.discriminator}', icon_url = message.author.display_avatar)        
        em.set_thumbnail(url = message.author.display_avatar)
        em.set_footer(text = f"Author ID: {message.author.id}")
        if message.stickers:
            for sticker in message.stickers:
                sticker_url = sticker.url
                em.set_image(url = sticker_url)

        if message.attachments and len(message.attachments) == 1:
            if message.stickers:
                em.set_image(url = sticker_url)
                await user.send(embed = em)
                for image in message.attachments:
                    if (image.content_type).startswith("image"):
                        em1.set_image(url = image.url)
                        await user.send(embed = em1)
            else: 
                for image in message.attachments:
                    if (image.content_type).startswith("image"):
                        em.set_image(url = image.url)
                    await user.send(embed = em)

        elif message.attachments and len(message.attachments) > 1:
            if message.stickers:
                em.set_image(url = sticker_url)
                await user.send(embed = em)
            else: await user.send(embed = em)
            for image in message.attachments:
                if (image.content_type).startswith("image"):
                    em1.set_image(url = image.url)
                    await user.send(embed = em1)

        elif message.stickers:
            em.set_image(url = sticker_url)
            await user.send(embed = em)

        else:
            await user.send(embed = em)

    @client.listen()
    async def on_message(message):
        await asyncio.sleep(2)
        if not message.guild or message.author.bot or not filtering_toggle(message) or message.author.guild_permissions.administrator: return
        
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
                        em = discord.Embed(title = '**Content Filtering**', description = '**Video from blacklisted YT channel removed**', colour=0xff0000, timestamp = pen.now(WIB))
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
                        if message.channel.permissions_for(message.guild.me).send_messages:
                            response = await message.reply(embed = em)
                        else: return
                        if message.guild.me.guild_permissions.manage_messages:
                            await message.delete()
                        else: return
                        found = True
                        break

                if found and message.guild.id in ServersImod:
                    user = await client.fetch_user(myid)
                    try:
                        await user.send(f'{message.author.name}#{message.author.discriminator} posted a blacklisted clipper video in {message.guild.name}.\n{response.jump_url}')
                    except Exception as e:
                        print(e)
                else: return
        except:
            return

    @client.listen()
    async def on_message(message):
        await asyncio.sleep(2)        
        x = re.search("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", message.content)
        if message.author.bot or not message.guild or message.attachments or x or not nodiscussion_toggle(message) or message.author.guild_permissions.administrator: return
        
        collection = loadsettings()
        immune = False
        ignored_roles = check_ignored_role_nd(message, collection)
        for role in message.author.roles: 
            if ignored_roles and role.id in ignored_roles:
                immune = True
                break
        if immune: return

        set_channels = check_nodiscussion_channels(message, collection)
        if not set_channels or message.channel.id not in set_channels: return
        msgs = []
        async for message in message.channel.history(limit = 2):
            msgs.append(message)
        if msgs[0].author != msgs[1].author:
            if message.guild.me.guild_permissions.manage_messages:
                await msgs[0].delete()
            else: return
        
    @client.event
    async def on_bulk_message_delete(messages):
        await asyncio.sleep(2)
        message = messages[0]
        if not message.guild or message.author.bot or not logging_toggle(message): return

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
            em = discord.Embed(description= embed_body, colour=0xf00000, timestamp = pen.now(WIB))
            if deleted_log_channel.permissions_for(message.guild.me).send_messages:
                await deleted_log_channel.send(embed = em)
            else: return

    @client.event
    async def on_message_delete(message):
        await asyncio.sleep(2)
        if not message.guild or message.author.bot or not logging_toggle(message): return
        
        collection = loadsettings()
        ignored_channels = check_ignored_channel(message, collection)
        if ignored_channels and message.channel.id in ignored_channels: return
        else:
            channel_deleted = check_deleted_logging_channel(message, collection)
            if channel_deleted:
                deleted_log_channel = client.get_channel(channel_deleted)
            else: return

            # if message.guild.me.guild_permissions.view_audit_log:
            #     async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete):
                    
            #         if entry.target == message.author.id and entry.extra.channel == message.channel and (pen.now() - entry.created_at).total_seconds() <= 30:
            #             executor = f'{entry.user.mention} ({entry.user.name}#{entry.user.discriminator})'
            #             break
            #         else: 
            #             executor = "*the author or a bot*"
            #             break
            # else:
            #     executor = "*(bot doesn't have view audit log permission)*"

            embed_body = f"**Message by {message.author.mention} deleted in {message.channel.mention}**"
            embed_body1 = f"**Message by {message.author.mention} deleted in {message.channel.mention}**"
            # embed_body += f'\n**Perpetrator:** {executor}'

            if message.content: 
                embed_body += f'\n{message.content}'
            has_non_image = False
            if message.attachments:
                for file_contained in message.attachments:
                    if not (file_contained.content_type).startswith("image"):
                        embed_body += f'\n{file_contained.url}'
                        has_non_image = True
            if message.stickers:
                for sticker in message.stickers:
                    sticker_name = sticker.name
                embed_body += f'**\n(Message contained sticker)**\n:{sticker_name}:'

            em = discord.Embed(description= embed_body, colour=0xf00000, timestamp = pen.now(WIB))
            em1 = discord.Embed(description= embed_body1, colour=0xf00000, timestamp = pen.now(WIB))
            if message.author.nick:
                em.set_author(name = f'{message.author.name}#{message.author.discriminator}  ({message.author.nick})', icon_url = message.author.display_avatar)
                em1.set_author(name = f'{message.author.name}#{message.author.discriminator}  ({message.author.nick})', icon_url = message.author.display_avatar)
            else:
                em.set_author(name = f'{message.author.name}#{message.author.discriminator}', icon_url = message.author.display_avatar)
                em1.set_author(name = f'{message.author.name}#{message.author.discriminator}', icon_url = message.author.display_avatar)
            if message.content or has_non_image:
                if message.author.avatar:
                    url = message.author.avatar
                else:
                    url = message.author.display_avatar
                em.set_thumbnail(url = url)
            em.set_footer(text = f"Author ID: {message.author.id} | Message ID {message.id}")
            em1.set_footer(text = f"Author ID: {message.author.id} | Message ID {message.id}")

            if message.stickers:
                for sticker in message.stickers:
                    sticker_url = sticker.url
            if deleted_log_channel.permissions_for(message.guild.me).send_messages:
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
            else: return

    @client.event
    async def on_message_edit(before, after):
        await asyncio.sleep(2)
        if not before.guild or before.author.bot or before.content == after.content or not logging_toggle(before): return
        
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
            else: before_body = '<no message>\n'
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
                for sticker in before.stickers:
                    sticker_name = sticker.name
                after_body += f'**\n(Message contained sticker)**\n:{sticker_name}:'
            after_body += f'\n[Jump to message]({after.jump_url})'

            em = discord.Embed(description=f"**Message by {before.author.mention} edited in {before.channel.mention}**\n", colour=0xcaa686, timestamp = pen.now(WIB))
            em.add_field(name="Before", value=before_body)
            em.add_field(name="After", value=after_body, inline=False)
            if before.author.nick:
                em.set_author(name = f'{before.author.name}#{before.author.discriminator}  ({before.author.nick})', icon_url = before.author.display_avatar)
            else:
                em.set_author(name = f'{before.author.name}#{before.author.discriminator}', icon_url = before.author.display_avatar)
            if before.author.avatar:
                 url = before.author.avatar
            else:
                url = before.author.display_avatar
            em.set_thumbnail(url = url)
            em.set_footer(text = f"User ID: {after.author.id}", icon_url = after.guild.icon)

            if before.attachments and not before.stickers:
                for image in before.attachments:
                    if (image.content_type).startswith("image"):
                        em.set_image(url = image.url)
            elif before.stickers:
                for sticker in before.stickers:
                    em.set_image(url = sticker.url)

        if edited_log_channel.permissions_for(before.guild.me).send_messages:
            await edited_log_channel.send(embed = em)
        else: return

    @client.event
    async def on_member_join(member):
        await asyncio.sleep(2)
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

        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        if age > 86400:
            days = round(age//86400)
            days_mod = round(age%86400)
            if days_mod > 0:
                hours = round(days_mod//3600)
                hours_mod = round(days_mod%3600)
                if hours_mod > 0:
                    minutes = round(hours_mod//60)
                    seconds = round(hours_mod%60)

        elif age > 3600:
            hours = round(age//3600)
            hours_mod = round(age%3600)
            if hours_mod > 0:
                minutes = round(hours_mod//60)
                seconds = round(hours_mod%60)
                
        elif age > 60:
            minutes = round(age//60)
            seconds = round(age%60)

        else:
            seconds = round(age, 2)

        d = False
        h = False
        m = False
        kicked_age = ''
        if days > 0:
            kicked_age += f'{days} day(s)'
            d = True
        if hours > 0:
            if d:
                kicked_age += ' '
            kicked_age += f'{hours} hour(s)'
            h = True
        if minutes > 0:
            if d or h:
                kicked_age += ' '
            kicked_age += f'{minutes} minute(s)'
            m = True
        if seconds > 0:
            if d or h or m:
                kicked_age += ' '
            kicked_age += f'{seconds} second(s)'

        reason = f"Account's age (`{kicked_age}`) is less than the set requirement (>{min_age} day(s))."
        if member.guild.me.guild_permissions.kick_members:
            if age < minage_seconds:
                sent = False
                try:
                    await member.send(minage_message)
                    sent = True
                except:
                    sent = False
                await member.kick(reason = reason)
                if channel:
                    embed_body = f'**Kicked** {member.mention} ({member.id})\n'
                    embed_body += '\n'
                    embed_body += f"**Reason:** {reason}"

                    if not sent:
                        embed_body += '\n*Failed to message the user due to their privacy settings.*'

                    em = discord.Embed(title = "Minage Report", description = embed_body, colour=0xf00000, timestamp = pen.now(WIB))
                    em.set_thumbnail(url = member.display_avatar)
                    em.set_footer(text = f"{member.display_name} ({member.id})", icon_url = member.display_avatar)
                    if log_channel.permissions_for(member.guild.me).send_messages:
                        await log_channel.send(embed = em)
                    else: return
            else: return
        else:
            if channel:
                embed_body = f'**Failed to kick** {member.mention} ({member.id})\n'
                embed_body += '\n'
                embed_body += f"**Reason:** Bot is missing `Kick Members` permission."
                em = discord.Embed(title = "Minage Report", description = embed_body, colour=0xf1e40f, timestamp = pen.now(WIB))
                em.set_thumbnail(url = member.display_avatar)
                em.set_footer(text = f"{member.display_name} ({member.id})", icon_url = member.display_avatar)
                if log_channel.permissions_for(member.guild.me).send_messages:
                     await log_channel.send(embed = em)
                else: return
            else: return

    @client.event
    async def on_voice_state_update(member, before, after):
        await asyncio.sleep(2)
        if member.bot or not voicelink_toggle(member) or member.guild_permissions.administrator: return
        
        collection = loadsettings()
        roleID = check_voicelink_role(member, collection)
        if member.guild.me.guild_permissions.manage_roles:
            if roleID:
                role = member.guild.get_role(roleID)
            else: return

            if not role:
                return
            if after.channel != None:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

    @client.listen()
    async def on_voice_state_update(member, before, after):
        await asyncio.sleep(2)
        if member.bot or not streamlink_toggle(member) or member.guild_permissions.administrator: return
        
        collection = loadsettings()
        roleID = check_streamlink_role(member, collection)
        if member.guild.me.guild_permissions.manage_roles:
            if roleID:
                role = member.guild.get_role(roleID)
            else: return
            
            if not role:
                return
            elif after.self_stream:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)
                
    # Error handler

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
            await ctx.reply(message, delete_after=round(error.retry_after), mention_author = False)
        elif isinstance(error, commands.MissingPermissions):
            error = str(error)
            if "Moderate" in error:
                error = error.replace("Moderate", "Timeout")
            await ctx.reply(f"{error}")
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.reply("You don't have permission to run this command.")
        elif isinstance(error, commands.NotOwner):
            await ctx.reply("Only bot owner can run this command.")
        elif isinstance(error, commands.CommandNotFound): return
        else: # You can delete this whole else section if you don't want it or just put `return`
            user = await client.fetch_user(myid)
            await user.send(f"Uncaught error encountered in {ctx.guild.name} when executing `{ctx.command.name}` command:\n```\n{error}```")

    # Load cogs

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

    client.run(TOKEN)

if __name__ == '__main__':
    main()
