async def get_trashcan(ctx):
    for emoji in ctx.guild.emojis:
        if emoji.name == 'trashcan':
            return emoji