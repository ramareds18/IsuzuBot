import nextcord as discord
import pendulum as pen
from nextcord import Interaction
from nextcord.ext import commands

class MiscApp(commands.Cog):

    def __init__(self, client):
        self.client = client

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

def setup(client):
    client.add_cog(MiscApp(client))