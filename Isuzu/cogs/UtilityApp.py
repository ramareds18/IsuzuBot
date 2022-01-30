import nextcord as discord
import pendulum as pen
from nextcord import Interaction, SlashOption, ChannelType
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
            description = "Date and time in format of yyyy/mm/dd hour:minute",
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

def setup(client):
    client.add_cog(UtilityApp(client))
