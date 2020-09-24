from discord.ext.commands import Bot
from os import environ
from discord import Message
from cogs import XKCDCog, MoneyManagerCog

bot = Bot("!")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(msg: Message):
    m = msg.mentions[0]
    print(m.desktop_status, m.mobile_status, m.web_status)


bot.add_cog(XKCDCog(bot))
bot.add_cog(MoneyManagerCog())


bot.run(environ.get('DISCORD_TOKEN'))
