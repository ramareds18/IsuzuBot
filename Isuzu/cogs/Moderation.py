import typing
import nextcord as discord
import pendulum as pen
from durations import Duration
from nextcord import NotFound
from nextcord.ext import commands
from nextcord.errors import Forbidden
from pendulum import datetime as dt

# 2 functions below are courtesy of shaak

def flatten(t):
    return [item for sublist in t for item in sublist]

def multi_split(source: str, by: typing.List[str]) -> typing.List[str]:
    if len(by) == 0:
        return [source]
    split = source.split(by.pop())
    for entry in by:
        split = flatten(map(lambda x: x.split(entry), split))
    return list(filter(lambda x: len(x) > 0, split))

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member: typing.Union[discord.Member, discord.User], *, reason = None):
        if isinstance(member, discord.User):
            await ctx.reply("User is not a member of the server.")
        else:
            try:
                msg = await ctx.reply('Kicking...', mention_author = False)
                if member.top_role >= ctx.author.top_role:
                    await msg.edit('You are not allowed to kick this user.')
                else:
                    comment = ''
                    if reason and len(reason) <= 450:
                        reason += f' | Kicked by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                    elif reason and len(reason) > 450:
                        reason = f'Kicked by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                        comment = 'Reason too long.'
                    else:
                        reason = f'Kicked by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                    await ctx.guild.kick(member, reason = reason)
                    
                    embed_body = f'**Kicked** {member.mention} ({member.id})\n'
                    embed_body += '\n'
                    embed_body += f'**Reason:** {reason}\n'
                    if comment:
                        embed_body += f'**Note**: {comment}'
                    em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                    await msg.edit(content=None, embed = em, allowed_mentions = discord.AllowedMentions.none())
            except Forbidden:
                await msg.edit("Can't kick user with equal or higher role.")

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def masskick(self, ctx, *args: typing.Union[int, str]):
        if args or ctx.message.attachments:
            guild_members = ctx.guild.members
            kick_check = 0
            embed_body = ''
            users = []
            string = []
            invalid_accounts = []
            valid_accounts = []
            not_in_guild = []
            forbidden_accounts = []
            wait = False
            ids = list(args)

            if ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    if attachment.content_type.startswith('text/plain') and attachment.size < (1024**2):
                        file = await attachment.to_file()
                        new = file.fp.read().decode('utf8')
                        for entry in multi_split(new, [' ', '\t', '\n', '\r']):
                            try:
                                ids.append(int(entry))
                            except ValueError:
                                return
                for user in ids:
                    if isinstance(user, int):
                        users.append(user)
                    elif isinstance(user, str):
                        string.append(user)
            else:
                for arg in args:
                    if isinstance(arg, int):
                        users.append(arg)
                    elif isinstance(arg, str):
                        string.append(arg)

            if users:
                comment = ''
                await ctx.message.add_reaction("🔄")
                if string and len(string) <= 450:
                    string_reason = "".join(f"{reason} " for reason in string)
                    reason = string_reason
                    reason += f' | Masskicked by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                elif string and len(string) > 450:
                    reason = f'Masskicked by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                    comment = 'Reason too long.'
                else:
                    reason = f'Masskicked by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'

                if len(users) > 10:
                    msg = await ctx.reply('This might take a while, please wait...', mention_author = False)
                    wait = True

                for user in users:
                    try:
                        valid_accounts.append(await self.client.fetch_user(user))
                    except:
                        invalid_accounts.append(user)

                for guild_member in valid_accounts:
                    if guild_member not in guild_members:
                        not_in_guild.append(guild_member)
                        valid_accounts.remove(guild_member)

                for hierarchy_check in valid_accounts:
                    if isinstance(hierarchy_check, discord.Member) and hierarchy_check.top_role >= ctx.author.top_role:
                        forbidden_accounts.append(hierarchy_check.id)
                        valid_accounts.remove(hierarchy_check)

                for kicked in valid_accounts:
                    try:
                        await ctx.guild.kick(kicked, reason = reason)
                        kick_check += 1
                    except Forbidden:
                        forbidden_accounts.append(kicked.id)
                if kick_check != 0:
                    embed_body += f'**Kicked {kick_check}/{len(users)} users.**\n'
                    embed_body += '\n'

                embed_body += f'**Reason:** {reason}\n'
                embed_body += '\n'

                if invalid_accounts:
                    invalid_output = "".join(f"{invalid}\n" for invalid in invalid_accounts)
                    embed_body += f"Failed to kick [{len(invalid_accounts)}] because of not valid user ID: ```\n{invalid_output}```\n"

                if forbidden_accounts:
                    forbidden_output = "".join(f"{forbidden}\n" for forbidden in forbidden_accounts)
                    embed_body += f"Failed to kick [{len(forbidden_accounts)}] because of role hierarchy (either you or the bot): ```\n{forbidden_output}```"

                if not_in_guild:
                    not_in_guild_output = "".join(f"{not_member.id}\n" for not_member in not_in_guild)
                    embed_body += f"Failed to kick [{len(not_in_guild)}] because user is not a member of the server: ```\n{not_in_guild_output}```"

                if comment:
                    embed_body += f'\n**Note**: {comment}'
                em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                await ctx.message.remove_reaction('🔄', self.client.user)
                if wait:
                    await msg.edit(content = None, embed = em, allowed_mentions = discord.AllowedMentions.none())
                else:
                    await ctx.reply(embed = em, mention_author = False)
            else:
                await ctx.reply('Please provide userID(s) and reason (optional) or file to kick.')
        else:
            await ctx.reply('Please provide userID(s) and reason (optional) or file to kick.')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self, ctx, member: typing.Union[discord.Member, discord.User], *, reason = None):
        try:
            msg = await ctx.reply('Banning...', mention_author = False)
            if isinstance(member, discord.Member) and member.top_role >= ctx.author.top_role:
                await msg.edit('You are not allowed to ban this user.')
            else:
                comment = ''
                if reason and len(reason) <= 450:
                    reason += f' | Banned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                elif reason and len(reason) > 450:
                    reason = f'Banned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                    comment = 'Reason too long.'
                else:
                    reason = f'Banned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                await ctx.guild.ban(member, reason = reason)
                
                embed_body = f'**Banned** {member.mention} ({member.id})\n'
                embed_body += '\n'
                embed_body += f'**Reason:** {reason}\n'
                if comment:
                    embed_body += f'**Note**: {comment}'
                em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                await msg.edit(content=None, embed = em, allowed_mentions = discord.AllowedMentions.none())
        except Forbidden:
            await msg.edit("Can't ban user with equal or higher role.")

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def unban(self, ctx, member: typing.Union[discord.Member, discord.User], *, reason = None):
        try:
            is_banned = await ctx.guild.fetch_ban(member)
            msg = await ctx.reply('Unbanning...', mention_author = False)
            comment = ''
            if reason and len(reason) <= 450:
                reason += f' | Unbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
            elif reason and len(reason) > 450:
                reason = f'Unbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                comment = 'Reason too long.'
            else:
                reason = f'Unbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
            await ctx.guild.unban(member, reason = reason)
            embed_body = f'**Unbanned** {member.mention} ({member.id})\n'
            embed_body += '\n'
            embed_body += f'**Reason:** {reason}\n'
            if comment:
                embed_body += f'**Note**: {comment}'
            em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf1e40f, timestamp = pen.now('Asia/Jakarta'))
            await msg.edit(content=None, embed = em, allowed_mentions = discord.AllowedMentions.none())
        except NotFound:
            await ctx.reply('That is not a banned user.', mention_author = False)

    @commands.command(aliases = ['nuke'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def massban(self, ctx, *args: typing.Union[int, str]):
        if args or ctx.message.attachments:
            guild_members = ctx.guild.members
            ban_check = 0
            embed_body = ''
            confirm = True
            users = []
            string = []
            invalid_accounts = []
            valid_accounts = []
            member_in_guild = []
            forbidden_accounts = []
            wait = False
            ids = list(args)

            if ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    if attachment.content_type.startswith('text/plain') and attachment.size < (1024**2):
                        file = await attachment.to_file()
                        new = file.fp.read().decode('utf8')
                        for entry in multi_split(new, [' ', '\t', '\n', '\r']):
                            try:
                                ids.append(int(entry))
                            except ValueError:
                                return
                for user in ids:
                    if isinstance(user, int):
                        users.append(user)
                    elif isinstance(user, str):
                        string.append(user)
            else:
                for arg in args:
                    if isinstance(arg, int):
                        users.append(arg)
                    elif isinstance(arg, str):
                        string.append(arg)

            if users:
                comment = ''
                await ctx.message.add_reaction("🔄")
                if string and len(string) <= 450:
                    string_reason = "".join(f"{reason} " for reason in string)
                    reason = string_reason
                    reason += f' | Massbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                elif string and len(string) > 450:
                    reason = f'Massbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                    comment = 'Reason too long.'
                else:
                    reason = f'Massbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'

                if len(users) > 10:
                    msg = await ctx.reply('This might take a while, please wait...', mention_author = False)
                    wait = True

                for user in users:
                    try:
                        valid_accounts.append(await self.client.fetch_user(user))
                    except:
                        invalid_accounts.append(user)

                for guild_member in valid_accounts:
                    if guild_member in guild_members:
                        member_in_guild.append(guild_member)

                if member_in_guild:
                    member_in_guild_mention = "".join(f"{member.mention} " for member in member_in_guild)
                    member_in_guild_id = "".join(f"{member.id}\n" for member in member_in_guild)
                    ban_message = f"Found {len(member_in_guild)} member(s) in this server. Proceed to ban? You have 2 minutes."
                    ban_message += f"\nThey are: {member_in_guild_mention}\n```\n{member_in_guild_id}```"
                    msg1 = await ctx.reply(ban_message)
                    await msg1.add_reaction("✅")
                    await msg1.add_reaction("❌")
                    yas = '✅'
                    nay = '❌'
                    valid_reactions = ['✅', '❌']
                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in valid_reactions
                    reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)

                    if str(reaction.emoji) == yas:
                        confirm = True
                    else:
                        confirm = False
                    await msg1.delete()

                if confirm:
                    valid_accounts = valid_accounts
                else:
                    for guild_member in member_in_guild:
                        valid_accounts.remove(guild_member)

                for hierarchy_check in valid_accounts:
                    if isinstance(hierarchy_check, discord.Member) and hierarchy_check.top_role >= ctx.author.top_role:
                        forbidden_accounts.append(hierarchy_check.id)
                        valid_accounts.remove(hierarchy_check)

                for banned in valid_accounts:
                    try:
                        await ctx.guild.ban(banned, reason = reason)
                        ban_check += 1
                    except Forbidden:
                        forbidden_accounts.append(banned.id)
                if ban_check != 0:
                    embed_body += f'**Banned {ban_check}/{len(users)} users.**\n'
                    embed_body += '\n'

                embed_body += f'**Reason:** {reason}\n'
                embed_body += '\n'

                if invalid_accounts:
                    invalid_output = "".join(f"{invalid}\n" for invalid in invalid_accounts)
                    embed_body += f"Failed to ban [{len(invalid_accounts)}] because of not valid user ID: ```\n{invalid_output}```\n"

                if forbidden_accounts:
                    forbidden_output = "".join(f"{forbidden}\n" for forbidden in forbidden_accounts)
                    embed_body += f"Failed to ban [{len(forbidden_accounts)}] because of role hierarchy (either you or the bot): ```\n{forbidden_output}```"

                if not confirm and member_in_guild:
                    embed_body += f"Skipped [{len(member_in_guild)}] because of your decision to not ban these member(s) of the server: ```\n{member_in_guild_id}```"

                if comment:
                    embed_body += f'\n**Note**: {comment}'
                em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf00000, timestamp = pen.now('Asia/Jakarta'))
                await ctx.message.remove_reaction('🔄', self.client.user)
                if wait:
                    await msg.edit(content = None, embed = em, allowed_mentions = discord.AllowedMentions.none())
                else:
                    await ctx.reply(embed = em, mention_author = False)
            else:
                await ctx.reply('Please provide userID(s) and reason (optional) or file to ban.')
        else:
            await ctx.reply('Please provide userID(s) and reason (optional) or file to ban.')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def massunban(self, ctx, *args: typing.Union[int, str]):
        if args or ctx.message.attachments:
            unban_check = 0
            embed_body = ''
            users = []
            string = []
            is_banned = []
            not_banned = []
            valid_accounts = []
            invalid_accounts = []
            wait = False
            ids = list(args)

            if ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    if attachment.content_type.startswith('text/plain') and attachment.size < (1024**2):
                        file = await attachment.to_file()
                        new = file.fp.read().decode('utf8')
                        for entry in multi_split(new, [' ', '\t', '\n', '\r']):
                            try:
                                ids.append(int(entry))
                            except ValueError:
                                return
                for user in ids:
                    if isinstance(user, int):
                        users.append(user)
                    elif isinstance(user, str):
                        string.append(user)
            else:
                for arg in args:
                    if isinstance(arg, int):
                        users.append(arg)
                    elif isinstance(arg, str):
                        string.append(arg)
            
            if users:
                comment = ''
                await ctx.message.add_reaction("🔄")
                if string and len(string) <= 450:
                    string_reason = "".join(f"{reason} " for reason in string)
                    reason = string_reason
                    reason += f' | Massunbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                elif string and len(string) > 450:
                    reason = f'Massunbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'
                    comment = 'Reason too long.'
                else:
                    reason = f'Massunbanned by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})'

                if len(users) > 10:
                    msg = await ctx.reply('This might take a while, please wait...', mention_author = False)
                    wait = True

                for user in users:
                    try:
                        valid_accounts.append(await self.client.fetch_user(user))
                    except:
                        invalid_accounts.append(user)

                for valid in valid_accounts:
                    try:
                        is_banned.append(await ctx.guild.fetch_ban(valid)) 
                    except:
                        not_banned.append(valid)

                for unbanned in is_banned:
                    await ctx.guild.unban(unbanned.user, reason = reason)
                    unban_check += 1

                if unban_check != 0:
                    embed_body += f'**Unbanned {unban_check}/{len(users)} users.**\n'
                    embed_body += '\n'
                    embed_body += f'**Reason:** {reason}\n'
                    embed_body += '\n'

                    if not_banned:
                        not_banned_output = "".join(f"{noban}\n" for noban in not_banned)
                        embed_body += f"Skipped [{len(not_banned)}] because of not a banned user: ```\n{not_banned_output}```\n"

                    if invalid_accounts:
                        invalid_output = "".join(f"{invalid}\n" for invalid in invalid_accounts)
                        embed_body += f"Skipped [{len(invalid_accounts)}] because of not valid user ID: ```\n{invalid_output}```\n"

                    if comment:
                        embed_body += f'\n**Note**: {comment}'
                    em = discord.Embed(title = '', description = f"{embed_body}", colour=0xf1e40f, timestamp = pen.now('Asia/Jakarta'))
                    await ctx.message.remove_reaction('🔄', self.client.user)
                    if wait:
                        await msg.edit(content = None, embed = em, allowed_mentions = discord.AllowedMentions.none())
                    else:
                        await ctx.reply(embed = em, mention_author = False)
                else:
                    await ctx.reply('No valid user to unban.', mention_author = False)
                    await ctx.message.remove_reaction('🔄', self.client.user)
            else:
                await ctx.reply('Please provide userID(s) and reason (optional) or file to unban.')
        else:
            await ctx.reply('Please provide userID(s) and reason (optional) or file to unban.')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def prune(self, ctx, arg = None):
        members = ctx.guild.members
        to_be_kicked = []
        for member in members:
            if not arg:
                if not member.avatar and len(member.roles) == 1:
                    to_be_kicked.append(member)
                    reason = 'Kicked due to using default avatar and has no roles.'
            elif arg.lower() == "noavatar":
                if not member.avatar:
                    to_be_kicked.append(member)
                    reason = 'Kicked due to using default avatar.'
            elif arg.lower() == "norole":
                if len(member.roles) == 1:
                    to_be_kicked.append(member)
                    reason = 'Kicked due to having no roles.'
        if len(to_be_kicked) != 0:
            if not arg:
                msg_body = f'Users with no role and default avatar to be pruned = {len(to_be_kicked)} users.\nDo you wish to see all the IDs to be pruned? Press 🛑 if you wish to cancel prune.'
            elif arg.lower() == 'norole':
                msg_body = f'Users with no role to be pruned = {len(to_be_kicked)} users.\nDo you wish to see all the IDs to be pruned? Press 🛑 if you wish to cancel prune.'
            elif arg.lower() == 'noavatar':
                msg_body = f'Users with default avatar to be pruned = {len(to_be_kicked)} users.\nDo you wish to see all the IDs to be pruned? Press 🛑 if you wish to cancel prune.'
            msg = await ctx.reply(msg_body)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            await msg.add_reaction("🛑")
            valid_reactions = ['✅', '❌', '🛑']
            yas = '✅'
            nay = '❌'
            cancel = '🛑'
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in valid_reactions
            reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)
            if str(reaction.emoji) == yas:
                await msg.clear_reactions()
                output = ''
                for kick in to_be_kicked:
                    output += f'{kick.mention} - {str(kick.id)}\n'
                em = discord.Embed(title='Users to be pruned:',description=output, colour=0xf1e40f, timestamp = pen.now('Asia/Jakarta'))
                em.set_footer(text = f"{ctx.author.display_name} ({ctx.author.id})", icon_url = ctx.author.display_avatar)
                await ctx.send(embed = em)
                msg1 = await ctx.reply('Proceed to prune? You have 3 minutes.')
                await msg1.add_reaction("✅")
                await msg1.add_reaction("❌")
                reaction1, user1 = await self.client.wait_for('reaction_add', timeout=180.0, check=check)
                if str(reaction1.emoji) == yas:
                    processing_message = await ctx.reply('Pruning...', mention_author = False)
                    for kick in to_be_kicked:
                        await ctx.guild.kick(kick, reason = reason)
                    await processing_message.edit(f'{len(to_be_kicked)} users have been pruned.', allowed_mentions = discord.AllowedMentions.none())
                else:
                    await ctx.send('Prune cancelled.')
                await msg1.clear_reactions()
            elif str(reaction.emoji) == nay:
                processing_message = await ctx.reply('Pruning...', mention_author = False)
                for kick in to_be_kicked:
                    await ctx.guild.kick(kick, reason = reason)
                await processing_message.edit(f'{len(to_be_kicked)} users have been pruned.', allowed_mentions = discord.AllowedMentions.none())
            else:
                await ctx.send('Prune cancelled.')
            await msg.clear_reactions()
        else:
            await ctx.reply('No members to be pruned.', mention_author = False)

    # Error-handling section

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please provide userID and reason to kick (optional).')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I don't have `Kick Members` permission.")
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.reply("User could not be recognized. This is most likely due to the ID inputted wasn't a user ID.")

    @masskick.error
    async def masskick_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I don't have `Kick Members` permission.")
        elif isinstance(error, commands.CommandInvokeError) and 'TimeoutError' in str(error):
            await ctx.reply('You ran out of time.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please provide userID and reason to ban (optional).')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I don't have `Ban Members` permission.")
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.reply("User could not be recognized. This is most likely due to the ID inputted wasn't a user ID.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please provide userID and reason to unban.')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I don't have `Ban Members` permission.")
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.reply("User could not be recognized. This is most likely due to the ID inputted wasn't a user ID.")

    @massban.error
    async def massban_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I don't have `Ban Members` permission.")
        elif isinstance(error, commands.CommandInvokeError) and 'TimeoutError' in str(error):
            await ctx.reply('You ran out of time.')

    @massunban.error
    async def massunban_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I don't have `Ban Members` permission.")

    @prune.error
    async def prune_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("Missing `Kick Members` permission.")
        elif isinstance(error, commands.CommandInvokeError) and 'TimeoutError' in str(error):
            await ctx.reply('You ran out of time.')

def setup(client):
    client.add_cog(Moderation(client))
