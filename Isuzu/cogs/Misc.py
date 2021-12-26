import os
import typing
import nextcord as discord
from nextcord.ext import commands
from nextcord.errors import Forbidden

def loadqueue(ctx):
    with open(f'./resources/{ctx.guild.id}-karaokequeue.txt', 'r') as f:
        q = [line.replace("\n", "") for line in f.readlines()]
    
    return q

def writequeue(q, ctx):
    with open(f'./resources/{ctx.guild.id}-karaokequeue.txt', 'w+') as f:
        f.write(q)

def loadfirstqueue(ctx):
    with open(f'./resources/{ctx.guild.id}-karaokefirstqueue.txt', 'r') as f:
        fq = [line.replace("\n", "") for line in f.readlines()]
    
    return fq

def writefirstqueue(fq, ctx):
    with open(f'./resources/{ctx.guild.id}-karaokefirstqueue.txt', 'w+') as f:
        f.write(fq)

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    # ==== QUEUE RELATED COMMANDS ==

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        try:
            ql = loadqueue(ctx)
        except:
            ql = []
        if f'{ctx.author.id}' in ql:
            await ctx.reply(f"You're already in the queue {str(discord.utils.get(self.client.emojis, name='MoonaBonk'))}", mention_author = False)
        else:
            ql.append(f'{ctx.author.id}')
            new = "".join(f"{user}\n" for user in ql)
            writequeue(new, ctx)
            await ctx.reply(f"Gotcha, you're in! Be prepared! {str(discord.utils.get(self.client.emojis, name='MoonaNumaFast'))}", mention_author = False)

    @commands.command(aliases=['fq'])
    @commands.has_guild_permissions(manage_messages = True)
    async def forcequeue(self, ctx, member : discord.Member, order = None):
        try:
            ql = loadqueue(ctx)
        except:
            ql = []
        if f'{member.id}' in ql:
            await ctx.reply(f"{member.display_name} is already in the queue.", mention_author = False)  
        else:
            if order:
                if int(order) <= len(ql)+1 and int(order) > 0:
                    ql.insert(int(order)-1, member.id)
                    new = "".join(f"{user}\n" for user in ql)
                    writequeue(new, ctx)
                    await ctx.reply(f"Gotcha, {member.display_name} is now in and put in position {order}! Tell them to be prepared! {str(discord.utils.get(self.client.emojis, name='MoonaNumaFast'))}", mention_author = False)
                else:
                    await ctx.reply('Index out of range, please run `ql` to see how many people in the queue.', mention_author = False)
            else:
                ql.append(f'{member.id}')
                new = "".join(f"{user}\n" for user in ql)
                writequeue(new, ctx)
                await ctx.reply(f"Gotcha, {member.display_name} is now in! Tell them to be prepared! {str(discord.utils.get(self.client.emojis, name='MoonaNumaFast'))}", mention_author = False)

    @commands.command(aliases=['ql'])
    async def queuelist(self, ctx):
        try:
            q = loadqueue(ctx)
        except:
            q = []
        try:
            fq = loadfirstqueue(ctx)
        except:
            fq = ""
        MoonaSinging = discord.utils.get(self.client.emojis, name='MoonaSinging')
        current_singer = ctx.guild.get_member(int(fq[0])).display_name if fq else ""
        if not q and fq:
            embed_body = f'**Current singer: {current_singer}**\n'
            em = discord.Embed(title = 'Karaoke Queue', description = embed_body, color = 0xcaa686)
            em.set_thumbnail(url = MoonaSinging.url)
            await ctx.send(embed = em)
        elif q:
            list_of_users = "".join(f"{q.index(userid) + 1}. {ctx.guild.get_member(int(userid)).display_name}\n" for userid in q)
            embed_body = f'**Current singer: {current_singer}**\n'
            embed_body += f'\n{list_of_users}'
            em = discord.Embed(title = 'Karaoke Queue', description = embed_body, color = 0xcaa686)
            em.set_thumbnail(url = MoonaSinging.url)
            await ctx.send(embed = em)
        else:
            await ctx.send(f"No karaoke {str(discord.utils.get(self.client.emojis, name='MoonaPain'))}")

    @commands.command(aliases=['qn'])
    async def queuenext(self, ctx):
        try:
            q = loadqueue(ctx)
        except:
            q = []
        try:
            fq = loadfirstqueue(ctx)
        except:
            fq = ""
        if q:
            await ctx.send(f"<@{q[0]}>, it's your turn! Go wild! {str(discord.utils.get(self.client.emojis, name='MoonaSinging'))}")
            fq = q[0]
            q.pop(0)
            new_queue = "".join(f"{user}\n" for user in q)
            writequeue(new_queue, ctx)
            writefirstqueue(fq, ctx)
        elif not q and fq:
            os.remove(f'./resources/{ctx.guild.id}-karaokefirstqueue.txt')
            await ctx.send("Queue is empty. That was the last singer.")
        else:
            await ctx.send("Queue is empty.")

    @commands.command(aliases=['qr'])
    async def queueremove(self, ctx, idx = None):
        try:
            q = loadqueue(ctx)
        except:
            q = []
        if q:
            if idx:
                idx = int(idx) - 1
                if idx <= len(q) - 1 and idx >= 0:
                    user = await ctx.guild.fetch_member(q[idx])
                    q.pop(idx)
                    await ctx.reply(f"{user.display_name} has been removed from the queue {str(discord.utils.get(self.client.emojis, name='MoonaSleeper'))}", mention_author = False)
                elif idx < 0:
                    await ctx.reply('Did you see any number less than/equal to 0 in the queue? Might want to get your eyes checked.', mention_author = False)
                else:
                    await ctx.reply('Index out of range, please run `ql` to see how many people in the queue.', mention_author = False)
            else:
                if f'{ctx.author.id}' in q:
                    q.remove(f'{ctx.author.id}')
                    await ctx.reply(f"You have been removed from the queue {str(discord.utils.get(self.client.emojis, name='MoonaUpset'))}", mention_author = False)
                else:
                    await ctx.reply(f"Bro, you ain't even in the queue {str(discord.utils.get(self.client.emojis, name='MoonaGalaxyBrainBeyond'))}", mention_author = False)
            new_queue = "".join(f"{user}\n" for user in q)
            writequeue(new_queue, ctx)
        else:
            await ctx.reply('Queue is empty.', mention_author = False)
    
    @commands.command(aliases=['qs'])
    async def queueswap(self, ctx, idx1, idx2):
        try:
            q = loadqueue(ctx)
        except:
            q = []
        idx1 = int(idx1) - 1
        idx2 = int(idx2) - 1
        if q:
            if (idx1 <= len(q) - 1 and idx2 <= len(q) - 1) and (idx1 >= 0 and idx2 >= 0):
                q[idx1], q[idx2] = q[idx2], q[idx1]
                new_queue = "".join(f"{user}\n" for user in q)
                writequeue(new_queue, ctx)
                await ctx.reply(f"Order number {idx1+1} has been swapped with order number {idx2+1}.", mention_author = False)
            elif idx1 < 0 or idx1 < 0:
                await ctx.reply('Did you see any number less than/equal to 0 in the queue? Might want to get your eyes checked.', mention_author = False)
            else:
                await ctx.reply('Index out of range, please run `ql` to see how many people in the queue.', mention_author = False)
        else:
            await ctx.reply('Queue is empty.', mention_author = False)

    @commands.has_permissions(manage_messages = True)
    @commands.command(aliases=['qc'])
    async def queueclear(self, ctx):
        try:
            q = loadqueue(ctx)
        except:
            q = []
        try:
            fq = loadfirstqueue(ctx)
        except:
            fq = ""
        if q:
            os.remove(f'./resources/{ctx.guild.id}-karaokequeue.txt')
            if fq:
                os.remove(f'./resources/{ctx.guild.id}-karaokefirstqueue.txt')
            await ctx.reply("Queue has been cleared.", mention_author = False)
        elif not q and fq:
            os.remove(f'./resources/{ctx.guild.id}-karaokefirstqueue.txt')
            await ctx.reply("Queue is already empty. Current singer is cleared.", mention_author = False)
        else:
            await ctx.reply("Queue is already empty.", mention_author = False)

    # ==== END OF QUEUE RELATED COMMANDS ==

    @commands.command(aliases=['waki'])
    async def wakipai(self, ctx):
        await ctx.send('Stop it. Get some help.')

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def echo(self, ctx, channel : typing.Union[discord.TextChannel, discord.Thread], *, msg = None):
        try:
            file_list = []
            msg = msg if not msg else msg
            if ctx.message.stickers and ctx.message.attachments:
                for file_contained in ctx.message.attachments:
                    file_list.append(await file_contained.to_file())
                await channel.send(msg, stickers = ctx.message.stickers, files = file_list)
            elif ctx.message.stickers:
                await channel.send(msg, stickers = ctx.message.stickers)
            elif ctx.message.attachments:
                for file_contained in ctx.message.attachments:
                    file_list.append(await file_contained.to_file())
                await channel.send(msg, files = file_list)
            else:
                await channel.send(msg)

            await ctx.send(f"Message sent to {channel.mention}.")
        except Forbidden as f:
            if '50081' in str(f):
                await ctx.send("Bot doesn't have access to that sticker.")
            elif '50001' in str(f):
                await ctx.send("Bot doesn't have access or can't send messages to that channel/thread.")
        except Exception as e:
            if '50006' in str(e):
                await ctx.send("Cannot send empty message. Please provide the message/file/sticker that you want to send.")

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def edit(self, ctx, ch : typing.Union[discord.TextChannel, discord.Thread], msg, *, msg_edit):
        try:
            current_message = await ch.fetch_message(msg)
            await current_message.edit(msg_edit)
            await ctx.send(f"Message in {ch.mention} has been edited. Click the link below to jump to the message.\n{current_message.jump_url}")
        except Forbidden:
            await ctx.send("Bot doesn't have access or can't send messages to that channel/thread.")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! `{round(self.client.latency * 1000)}ms`')

    @commands.command(aliases = ['stealsticker', 'ss'])
    @commands.has_permissions(manage_messages = True)
    async def stickerinfo(self, ctx, *, msg = None):
        if ctx.message.stickers:
            for sticker in ctx.message.stickers:
                s = sticker
            embed_body = f"Sticker name: {s.name}\n"
            embed_body += f"Sticker ID: {s.id}\n"
            em = discord.Embed(title = 'Sticker Information', description = embed_body, color = 0xcaa686)
            em.set_image(url = s.url)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please input your sticker.')

    # Error-handling section

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please provide channel and the message/file/sticker that you want to send.')
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.send('Please input a valid channel (channel name, id or just mention the channel/thread).')
        else:
            return

    @forcequeue.error
    async def forcequeue_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing argument, please input the user you want to queue in and the order (optional).', mention_author = False)

    @queueswap.error
    async def queueswap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing argument, please input the 2 order you want to swap.', mention_author = False)

def setup(client):
    client.add_cog(Misc(client))