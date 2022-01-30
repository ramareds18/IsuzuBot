import nextcord as discord
import pendulum as pen
from nextcord import Interaction
from nextcord.ext import commands

class MiscApp(commands.Cog):

    def __init__(self, client):
        self.client = client

    Moonacord = 735868176595812422

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
