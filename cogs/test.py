import discord
from discord.ext import commands

import requests
import urllib.request
import logging

class TestCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test_cog", description='dumps a message to the backend logger. dev use.')
    async def test_cog(self, ctx):
        logging.debug("-"*50)
        logging.debug(ctx)
        logging.debug(ctx.message)
        logging.debug(ctx.message.content)
        logging.debug(ctx.message.attachments)
        await ctx.message.attachments[0].save(fp="temp.png") 
        logging.debug("-"*50)

async def setup(bot):
    await bot.add_cog(TestCog(bot))

