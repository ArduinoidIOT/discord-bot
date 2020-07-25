import asyncio
import requests
from discord.ext import commands
from discord import Embed, Color, RawReactionActionEvent
from .utils import *


def blocking_io(num):  # TODO: Use pycurl
    return requests.get(f'https://xkcd.com/{num}/info.0.json').json()['img']


class XKCDCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xkcd(self, ctx, num=''):
        trashcan = await get_trashcan(ctx)
        loop = asyncio.get_running_loop()
        try:
            embed = Embed(color=Color(0xff0000))
            embed.set_image(url=(await loop.run_in_executor(None, blocking_io, num)))
            embed.set_footer(text=ctx.author.mention)
            msg = await ctx.send(embed=embed)
        except:
            msg = await ctx.channel.send(embed=
                                         Embed(description='**Sorry, XKCD comic not found**',
                                               color=Color(0x0000ff)).set_footer(text=ctx.author.mention))

        await msg.add_reaction(trashcan)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        mention = self.bot.get_user(payload.user_id).mention
        message = await get_message(self.bot, payload.message_id, payload.channel_id)
        print(payload.emoji.name)
        if message.embeds[0].footer.text == mention and payload.emoji.name == 'trashcan':
            await message.delete()
