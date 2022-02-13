import typing
import pendulum as pen
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

    # ==== END OF QUEUE RELATED COMMANDS ==

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

            await ctx.reply(f"Message sent to {channel.mention}.", mention_author = False)
        except Forbidden as f:
            if '50081' in str(f):
                await ctx.reply("Bot doesn't have access to that sticker.", mention_author = False)
            else:
                await ctx.reply("Bot doesn't have access or can't send messages to that channel/thread.", mention_author = False)
        except Exception as e:
            if '50006' in str(e):
                await ctx.reply("Cannot send empty message. Please provide the message/file/sticker that you want to send.", mention_author = False)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def edit(self, ctx, ch : typing.Union[discord.TextChannel, discord.Thread], msg, *, msg_edit):
        try:
            current_message = await ch.fetch_message(msg)
            await current_message.edit(msg_edit)
            await ctx.reply(f"Message in {ch.mention} has been edited. Click the link below to jump to the message.\n{current_message.jump_url}", mention_author = False)
        except Forbidden:
            await ctx.reply("Bot doesn't have access or can't send messages to that channel/thread.", mention_author = False)

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(f'🏓 Pong! `{round(self.client.latency * 1000)}ms`', mention_author = False)

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: typing.Union[discord.Member, discord.User], *, msg):
        try:
            await user.send(msg)
            await ctx.reply(f"Successfully DMed {user.name}.", mention_author = False)
        except:
            await ctx.reply("Failed sending message to user. Either said user turned off DM or the bot and user don't share any mutual server.", mention_author = False)

    @commands.command(aliases = ['stealsticker', 'ss'])
    async def stickerinfo(self, ctx, *, msg = None):
        if ctx.message.stickers:
            for sticker in ctx.message.stickers:
                s = sticker
            embed_body = f"**Sticker name:** {s.name}\n"
            embed_body += f"**Sticker ID:** {s.id}\n"
            em = discord.Embed(title = 'Sticker Information', description = embed_body, color = 0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            em.set_image(url = s.url)
            await ctx.reply(embed = em, mention_author = False)
        else:
            await ctx.reply('Please input your sticker.')

    @commands.command(aliases=['inv'])
    async def invitelink(self, ctx):
        output = 'Here is the invite link for the bot\n'
        output += "https://discord.com/api/oauth2/authorize?client_id=873300341150613554&permissions=1514311904470&scope=applications.commands%20bot"
        await ctx.reply(output, mention_author = False)

    # Error-handling section

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please provide channel and the message/file/sticker that you want to send.', mention_author = False)
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.reply('Please input a valid channel (channel name, id or just mention the channel/thread).', mention_author = False)
        else:
            return

def setup(client):
    client.add_cog(Misc(client))
