from discord.ext.commands import Bot
import discord
import asyncio
import requests

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
        return user == message.author and reaction.emoji == trashcan

    try:
        await bot.wait_for('reaction_add', check=check)
        await msg.delete()


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    trashcan = None
    for i in message.guild.emojis:
        if i.name == 'trashcan':
            trashcan = i
    if message.content.startswith('!xkcd'):
        data = message.content.split(" ")
        dt = []
        for i in data:
            if i:
                dt.append(i)
        dt.append('')
        loop = asyncio.get_running_loop()
        try:
            msg = await message.channel.send(await loop.run_in_executor(
                None, blocking_io, dt[1]))
        except:
            msg = await message.channel.send('**Sorry, XKCD comic not found**')
        await msg.add_reaction(trashcan)

        def check(reaction, user):
            return user == message.author and reaction.emoji == trashcan

        try:
            await bot.wait_for('reaction_add', check=check)
            await msg.delete()
        except asyncio.TimeoutError:
            await message.channel.send()


bot.run('NzMyNTk4MTMyNjYzMjU1MTIy.XxWa-w._SjbEkKEjV18ILxJtsy-loz0S1s')
