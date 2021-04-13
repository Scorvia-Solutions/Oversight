#region Imports
import discord

from utils import default
from discord.ext.commands import Bot
#endregion

class Bot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot:
            return

        await self.process_commands(msg)


class Embed(discord.Embed):
    def __init__(self, bot, **kwargs):
        super().__init__(**kwargs)

        self.set_footer(text=f'Support: WarpWing#3866', icon_url=bot.user.avatar_url_as(size=1024))
        self.timestamp = default.get_timestamp()