import nextcord as discord
import pendulum as pen
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord.errors import Forbidden
from pendulum import datetime as dt

class UtilityApp(commands.Cog):

    def __init__(self, client):
        self.client = client

    tz_options = {
        "(UTC) Universal Coordinated Time": "UTC",
        "(WIB) Western Indonesian Time": "Asia/Jakarta",
        "(JST) Japan Standard Time": "Asia/Tokyo",
        "(MSK) Moscow Standard Time": "Europe/Moscow",
        "(EDT) Eastern Standard Time": "US/Eastern",
        "(PDT) Pacific Standard Time": "America/Los_Angeles"
    }

    @discord.slash_command(
        name = "when",
        description = "Gets unix timestamp and calculates how much time until the given date",
    )
    async def when_slash(
        self,
        interaction: Interaction,
        timezone = SlashOption(
            name = "timezone",
            choices = tz_options,
            description = "Choose supported timezone",
        ),
        time = SlashOption(
            name = "date-and-time",
            description = "Date and time in format of yyyy/mm/dd hour:minute. Time must not exceed 23:59",
        ),
    ):
        UTC = "UTC"
        msg = ""
        now = pen.now(UTC)
        target = pen.parse(time, strict = False, tz = timezone, dayfirst = True).in_tz(UTC)
        epoch = round((target - dt(1970,1,1)).total_seconds())
        c = (target - now)
        hour = c.total_seconds() // 3600
        minutes = (c.total_seconds() % 3600) / 60
        if(c.total_seconds() >= 0):
            msg += "Time left: "
            if(hour <= 0):
                msg += f"{str(round(minutes))}m"
            else:
                msg += f"{str(round(hour))}h{str(round(minutes))}m"
        msg += "\nUnix Timestamp:"
        msg += f'\n`<t:{epoch}:F>` <t:{epoch}:F>'
        msg += f'\n`<t:{epoch}:R>` <t:{epoch}:R>'
        await interaction.response.send_message(msg)

    @discord.slash_command(
        name = "checkvera",
        description = "Checks unprocessed membership proof by VeraBot",
    )
    async def checkvera_slash(
        self, 
        interaction: Interaction, 
        channel: GuildChannel = SlashOption(
            name = "channel",
            description = "Vera log channel",
            channel_types = [discord.ChannelType.text, discord.ChannelType.public_thread],
        ),
    ):
        if interaction.user.guild_permissions.manage_messages:
            try:
                channel = self.client.get_channel(channel.id) 
                links = "" 
                async for message in channel.history(limit = 500):
                    reactions = message.reactions
                    for reaction in reactions:
                        if reaction.emoji == '✅':
                            async for user in reaction.users():
                                if user.bot:
                                    links += message.jump_url + "\n"
                if links == "":
                    await interaction.response.send_message("Everything looks good.")
                else:
                    await interaction.response.send_message("Membership not processed yet:\n" + links)
            except Forbidden:
                await interaction.response.send_message("Bot doesn't have access to that channel.", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have `Manage Messages` permission.", ephemeral=True)

    @discord.slash_command(
        name = "who",
        description = "See information of a user",
    )
    async def whois_slash(
        self, 
        interaction: Interaction, 
        member: discord.User = SlashOption(
            name = "user",
            description = "The user whose information you want to see",
            required = False,                       
        ),
    ):
        if interaction.user.guild_permissions.manage_messages:
            member = interaction.user if not member else member
            user = await self.client.fetch_user(member.id)
            ca = round((member.created_at - dt(1970,1,1)).total_seconds())
            if isinstance(member, discord.Member):
                embed_body = f'{member.mention} - {member.id}\n'
                if member.bot: embed_body += f'Bot\n'
                else:
                    if member.top_role.id != interaction.guild.id:
                        embed_body += f'{member.top_role}\n'
                embed_body += f'**\nCreated:** <t:{ca}:F> (<t:{ca}:R>)\n'
                ja = round((member.joined_at - dt(1970,1,1)).total_seconds())
                embed_body += f'**Joined:** <t:{ja}:F> (<t:{ja}:R>)'
            else:
                embed_body = f'{member.mention} - {member.id}\n**Created:** <t:{ca}:F> (<t:{ca}:R>)\n'
                embed_body += '\n*This user is not a member of this server. No additional info is available.*'

            em = discord.Embed(description= f'{embed_body}', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            if isinstance(member, discord.Member):
                if member.nick:
                    em.set_author(name = f'{member.name}#{member.discriminator}  ({member.nick})', icon_url = member.display_avatar)
                else:
                    em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
                field_body = ""
                if len(member.roles) > 1:
                    roles = [role for role in reversed(member.roles)]
                    for role in roles:
                        if roles.index(role) == len(roles) - 1: break
                        field_body += f"{role.mention} "
                    em.add_field(name = f'ROLES [{len(member.roles) - 1}]:', value = field_body, inline = False)
            else:
                em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
            if user.banner:
                em.set_image(url = user.banner)

            if member.avatar:
                url = member.avatar
            else:
                url = member.display_avatar

            em.set_thumbnail(url = url)

            em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
            await interaction.response.send_message(embed = em)
        else:
            await interaction.response.send_message("You don't have `Manage Messages` permission.", ephemeral=True)

    @discord.slash_command(
        name = "avatar",
        description = "See avatar of a user",
    )
    async def avatar_slash(
        self, 
        interaction: Interaction, 
        member: discord.User = SlashOption(
            name = "user",
            description = "The user whose avatar you want to see",
            required = False,
        ),
        arg = SlashOption(
            name = 'type',
            description = 'Which avatar you want to see - default server',
            choices = {"server": 'server', "global": 'global'},
            default = 'server',
            required = False,
        ),
    ):
        if interaction.user.guild_permissions.manage_messages:
            member = interaction.user if not member else member
            embed_body = f'{member.mention} - User Avatar\n'
            embed_body += '\n'
            if member.avatar:
                embed_body += f"[Download avatar]({member.avatar.url})"
            else:
                embed_body += f"[Download avatar]({member.display_avatar.url})"
            em = discord.Embed(description= f'{embed_body}', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            if isinstance(member, discord.Member):
                if member.nick:
                    em.set_author(name = f'{member.name}#{member.discriminator}  ({member.nick})', icon_url = member.display_avatar)
                else:
                    em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
            else:
                arg = 'global'
                em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
            
            if arg == 'server':
                em.set_image(url = member.display_avatar)
            else:
                if member.avatar:
                    em.set_image(url = member.avatar)
                else:
                    em.set_image(url = member.display_avatar)
            em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
            await interaction.response.send_message(embed = em)
        else:
            await interaction.response.send_message("You don't have `Manage Messages` permission.", ephemeral=True)

    @discord.slash_command(
        name = "banner",
        description = "See banner of a user",
    )
    async def banner_slash(
        self, 
        interaction: Interaction, 
        member: discord.User = SlashOption(
            name = "user",
            description = "The user whose banner you want to see",
            required = False,
        ),
    ):
        if interaction.user.guild_permissions.manage_messages:
            member = interaction.user if not member else member
            user = await self.client.fetch_user(member.id)
            embed_body = f'{member.mention} - User Banner\n'
            embed_body += '\n'
            if user.banner:
                embed_body += f"[Download banner]({user.banner.url})"
            else:
                embed_body += "*This user has no banner.*"
            em = discord.Embed(description= f'{embed_body}', colour=0xcaa686, timestamp = pen.now('Asia/Jakarta'))
            if isinstance(member, discord.Member):
                if member.nick:
                    em.set_author(name = f'{member.name}#{member.discriminator}  ({member.nick})', icon_url = member.display_avatar)
                else:
                    em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
            else:
                em.set_author(name = f'{member.name}#{member.discriminator}', icon_url = member.display_avatar)
            if user.banner:
                em.set_image(url = user.banner)

            em.set_footer(text = f"{interaction.user.display_name} ({interaction.user.id})", icon_url = interaction.user.display_avatar)
            await interaction.response.send_message(embed = em)
        else:
            await interaction.response.send_message("You don't have `Manage Messages` permission.", ephemeral=True)

def setup(client):
    client.add_cog(UtilityApp(client))
