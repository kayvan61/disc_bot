import discord
from discord.ext import commands

import random
import os
import logging

class Pepes(commands.Cog):

    pepe_base = "./pepes"

    def __init__(self, bot):
        self.bot = bot
        try:
            os.mkdir(Pepes.pepe_base)
        except:
            pass

    @commands.command(name="randPepe", description='returns a random pepe')
    async def randPepe(self, ctx):
        files = os.listdir(Pepes.pepe_base)
        index = 0

        # guards
        try:
            index = random.randint(0, len(files)-1)
        except ValueError:
            await ctx.reply(f"bad index given. $pepe <number>. max number is: {len(files)}")
            return
        if len(files) <= index:
            await ctx.reply(f"bad index given. $pepe <number>. max number is: {len(files)}")
            return

        # happy path
        logging.debug(f"sending {files[index]}")
        await ctx.channel.send(file=discord.File(os.path.join(Pepes.pepe_base, files[index])))


    @commands.command(name="pepe", description='returns a specific pepe. $pepe <number>')
    async def pepe(self, ctx):
        raw_str = ctx.message.content
        files = os.listdir(Pepes.pepe_base)
        index = 0

        # guards
        try:
            index = int(raw_str.split(" ")[-1])
        except ValueError:
            await ctx.reply(f"bad index given. $pepe <number>. max number is: {len(files)}")
            return
        if len(files) <= index:
            await ctx.reply(f"bad index given. $pepe <number>. max number is: {len(files)}")
            return

        # happy path
        logging.debug(f"sending {files[index]}")
        await ctx.channel.send(file=discord.File(os.path.join(Pepes.pepe_base, files[index])))

async def setup(bot):
    await bot.add_cog(Pepes(bot))

