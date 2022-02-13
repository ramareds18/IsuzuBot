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
        await interaction.response.send_message(f'🏓 Pong! `{round(self.client.latency * 1000)}ms`')

    @discord.slash_command(name="invitelink", description="Get invite link of the bot")
    async def invitelink_slash(self, interaction: Interaction):
        output = 'Here is the invite link for the bot\n'
        output += "https://discord.com/api/oauth2/authorize?client_id=873300341150613554&permissions=1514311904470&scope=applications.commands%20bot"
        await interaction.response.send_message(output) 

    # Message command app

    @discord.message_command(name="Sticker Info")
    async def stickerinfo_msg_command(self, interaction: Interaction, message: discord.Message):
        if message.stickers:
            for sticker in message.stickers:
                s = sticker
            embed_body = f"**Sticker name:** {s.name}\n"
            embed_body += f"**Sticker ID:** {s.id}\n"
            em = discord.Embed(title = 'Sticker Information', description = embed_body, color = 0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            em.set_image(url = s.url)
            await interaction.response.send_message(embed = em, ephemeral=True)
        else:
            await interaction.response.send_message("Message doesn't contain sticker.", ephemeral=True)       

    # Just me messing around

    @discord.message_command(name="Hilih", guild_ids=[Moonacord])
    async def hilih_msg_command(self, interaction: Interaction, message: discord.Message):
        if message.content:
            string = message.content
            output = ''
            vocal = ['a', 'u', 'e', 'o']
            for letter in string:
                if letter in vocal:
                    output += 'i'
                else:
                    output += letter
            await interaction.response.send_message(output)
        else:
            await interaction.response.send_message("Message doesn't have sentence.", ephemeral=True)

def setup(client):
    client.add_cog(MiscApp(client))