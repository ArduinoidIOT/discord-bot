from discord.ext import commands
from discord import User, Member
from typing import Optional
from json import dump, load


class MoneyManagerCog(commands.Cog):
    def __init__(self):
        with open('money.jsonbase') as db:
            self.db = load(db)

    @commands.command()
    async def pay(self, ctx, member: Member, amt: int):
        if self.db.get(member.mention) is None:
            self.db[member.mention] = 5000
        if self.db.get(ctx.message.author.mention) is None:
            self.db[ctx.message.author.mention] = 5000
        if self.db[ctx.message.author.mention] > amt:
            self.db[ctx.message.author.mention] -= amt
            self.db[member.mention] += amt
            await ctx.send("Transaction successful")
        else:
            await ctx.send("Transaction failed")
        self.sync()

    @commands.command()
    async def balance(self, ctx, user: Optional[Member]):
        if user is None:
            user = ctx.message.author

        await ctx.send(f"{user.mention} has {self.db[user.mention]} virtual blocks")

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        self.db[member.mention] = 5000
        self.sync()

    def sync(self):
        with open('money.jsonbase', 'w') as fl:
            dump(self.db, fl)
