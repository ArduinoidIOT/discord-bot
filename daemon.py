from discord.ext.commands import Bot
import discord
import asyncio
import requests
import os

bot = Bot("!")


async def get_trashcan_emoji(ctx):
    trashcan = None
    for emoji in ctx.guild.emojis:
        if emoji.name == 'trashcan':
            trashcan = emoji


def blocking_io(num):
    return requests.get(f'https://xkcd.com/{num}/info.0.json').json()['img']


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def xkcd(ctx, num=''):
    trashcan = await get_trashcan_emoji(ctx)
    loop = asyncio.get_running_loop()
    try:
        msg = await ctx.send(await loop.run_in_executor(
            None, blocking_io, num))
    except:
        msg = await ctx.channel.send('**Sorry, XKCD comic not found**')
    await msg.add_reaction(trashcan)

    def check(reaction, user):
        return user == ctx.author and reaction.emoji == trashcan

    await bot.wait_for('reaction_add', check=check)
    await msg.delete()


bot.run(os.environ.get('DISCORD_TOKEN'))
