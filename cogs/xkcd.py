import asyncio
from discord.ext import commands
from discord import Embed, Color, RawReactionActionEvent
from .utils import *
from pycurl import Curl
from json import load
import certifi
from io import BytesIO


def blocking_io(num):  # TODO: Use pycurl
    buf = BytesIO()
    c = Curl()
    c.setopt(c.URL, f'https://xkcd.com/{num}/info.0.json')
    c.setopt(c.WRITEDATA, buf)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    buf.seek(0)
    return load(buf)


class XKCDCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def xkcd(self, ctx, num=''):
        trashcan = await get_trashcan(ctx)
        loop = asyncio.get_running_loop()
        try:
            data = await loop.run_in_executor(None, blocking_io, num)
            embed = Embed(color=Color(0xff0000), description=data['alt'], title=data['title'])
            embed.set_image(url=data['img'])
            embed.set_footer(text=ctx.author.mention)
            msg = await ctx.send(embed=embed)
        except:
            msg = await ctx.channel.send(embed=
                                         Embed(description='**Sorry, XKCD comic not found**',
                                               color=Color(0x0000ff)).set_footer(text=ctx.author.mention))
            raise

        await msg.add_reaction(trashcan)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        mention = self.bot.get_user(payload.user_id).mention
        message = await get_message(self.bot, payload.message_id, payload.channel_id)
        if message.embeds[
            0].footer.text == mention and payload.emoji.name == 'trashcan' and self.bot.user == message.author:
            await message.delete()
