import discord
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_member_join(member):
    print(str(member) + " joined")


@bot.event
async def on_member_remove(member):
    print(str(member) + " left")


@bot.command()
async def test(ctx):
    await ctx.send("Rato-esquilo! Ping: " + str(round(bot.latency * 1000)) + "ms")

token = open("token.txt", 'r').readline()
bot.run(token)
