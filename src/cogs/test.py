import discord
from discord.ext import commands


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Listeners
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(str(member) + " joined")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(str(member) + " left")

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(str(round(self.bot.latency * 1000)) + "ms")


def setup(bot):
    bot.add_cog(Test(bot))
