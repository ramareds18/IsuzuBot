import nextcord as discord
import pendulum as pen
from nextcord import Interaction
from nextcord.ext import commands

class MiscApp(commands.Cog):

    def __init__(self, client):
        self.client = client

    Moonacord = 735868176595812422

    # Slash commands

    @discord.slash_command(name="ping", description="Get the bot latency")
    async def ping_slash(self, interaction: Interaction):
        await interaction.response.defer()
        await interaction.send(f'🏓 Pong! `{round(self.client.latency * 1000)}ms`')

    @discord.slash_command(name="invitelink", description="Get invite link of the bot")
    async def invitelink_slash(self, interaction: Interaction):
        await interaction.response.defer()
        output = 'Here is the invite link for the bot\n'
        output += "https://discord.com/api/oauth2/authorize?client_id=873300341150613554&permissions=1514311904470&scope=applications.commands%20bot"
        await interaction.send(output) 

    # Message command app

    @discord.message_command(name="Sticker Info")
    async def stickerinfo_msg_command(self, interaction: Interaction, message: discord.Message):
        await interaction.response.defer(ephemeral=True)
        if message.stickers:
            for sticker in message.stickers:
                s = sticker
            embed_body = f"**Sticker name:** {s.name}\n"
            embed_body += f"**Sticker ID:** {s.id}\n"
            em = discord.Embed(title = 'Sticker Information', description = embed_body, color = 0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            em.set_image(url = s.url)
            await interaction.send(embed = em)
        else:
            await interaction.send("Message doesn't contain sticker.")       

    # Just me messing around

    @discord.message_command(name="Hilih", guild_ids=[Moonacord])
    async def hilih_msg_command(self, interaction: Interaction, message: discord.Message):
        if message.content:
            await interaction.response.defer()
            string = message.content
            output = ''
            vocal = ['a', 'u', 'e', 'o']
            for letter in string:
                if letter.lower() in vocal:
                    output += 'i'
                else:
                    output += letter
            await interaction.send(output)
        else:
            await interaction.send("Message doesn't have sentence.", ephemeral=True)

def setup(client):
    client.add_cog(MiscApp(client))
