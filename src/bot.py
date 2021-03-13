import discord
from discord.ext import commands
import os

intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.command()
async def load(ctx, extension):
    bot.load_extension("cogs." + extension)


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension("cogs." + extension)


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension("cogs." + extension)
    bot.load_extension("cogs." + extension)

# @bot.event
# async def on_member_join(member):
#         print(str(member) + " joined")

for cog in os.listdir("./src/cogs"):
    if cog.endswith(".py"):
        bot.load_extension("cogs." + cog[:-3])

token = open("token.txt", 'r').readline()
bot.run(token)
