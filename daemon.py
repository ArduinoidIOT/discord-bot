from discord.ext.commands import Bot
from os import environ
from cogs import XKCDCog

bot = Bot("!")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.add_cog(XKCDCog(bot))


bot.run(environ.get('DISCORD_TOKEN'))
