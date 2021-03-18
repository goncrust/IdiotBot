import discord
import json
from discord.ext import commands


class Solitary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("./src/cogs/servers.json", 'r') as s:
            servers = json.load(s)

        servers[str(guild.id)] = "0"

        with open("./src/cogs/servers.json", 'w') as s:
            json.dump(servers, s)

        with open("./src/cogs/users.json", 'r') as u:
            users = json.load(u)

        users[str(guild.id)] = {}

        with open("./src/cogs/users.json", 'w') as u:
            json.dump(users, u)

    @commands.command()
    async def list_voice(self, ctx):
        voices = ctx.guild.voice_channels

        strvoices = ""
        for voice in range(len(voices)):
            strvoices = strvoices + str(voice+1) + \
                " " + str(voices[voice].name) + "\n"

        await ctx.send("```Available voice channels:\n\n" + strvoices + "```")

    @commands.command()
    async def ssolitary(self, ctx, number: int):
        voices = ctx.guild.voice_channels

        with open("./src/cogs/servers.json", 'r') as s:
            servers = json.load(s)

        servers[str(ctx.guild.id)] = voices[number-1].id

        with open("./src/cogs/servers.json", 'w') as s:
            json.dump(servers, s)

        await ctx.send("Solitary channel changed to: ```" + voices[number-1].name + "```")

    @ssolitary.error
    async def ssolitary_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            voices = ctx.guild.voice_channels

            strvoices = ""
            for voice in range(len(voices)):
                strvoices = strvoices + \
                    str(voice+1) + " " + str(voices[voice].name) + "\n"

            await ctx.send("Please run the command as: >ssolitary [voice channel number]\n```Available voice channels:\n\n" + strvoices + "```")

    @commands.command()
    async def solitary(self, ctx, member: discord.Member):
        with open("./src/cogs/servers.json", 'r') as s:
            servers = json.load(s)

        with open("./src/cogs/users.json", 'r') as u:
            users = json.load(u)

        if servers[str(ctx.guild.id)] == "0":
            await ctx.send("No solitary channel selected. Please run: >ssolitary")
            return

        if str(member.id) in users[str(member.guild.id)]:
            if users[str(ctx.guild.id)][str(member.id)]:
                if ctx.message.author != member:
                    users[str(ctx.guild.id)][str(member.id)] = False

                    with open("./src/cogs/users.json", 'w') as u:
                        json.dump(users, u)

                    await ctx.send(member.display_name + " can now leave solitary!")

                return

        users[str(ctx.guild.id)][str(member.id)] = True

        with open("./src/cogs/users.json", 'w') as u:
            json.dump(users, u)

        voices = ctx.guild.voice_channels

        for voice in voices:
            if voice.id == servers[str(ctx.guild.id)]:
                channel = voice

        await member.move_to(channel)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open("./src/cogs/servers.json", 'r') as s:
            servers = json.load(s)

        with open("./src/cogs/users.json", 'r') as u:
            users = json.load(u)

        if str(member.id) in users[str(member.guild.id)]:
            if after.channel.id != servers[str(member.guild.id)]:
                if users[str(member.guild.id)][str(member.id)]:

                    voices = member.guild.voice_channels

                    for voice in voices:
                        if voice.id == servers[str(member.guild.id)]:
                            channel = voice

                    await member.move_to(channel)


def setup(bot):
    bot.add_cog(Solitary(bot))
