import discord
from discord.ext import commands

from PIL import Image
import random
import os
import logging

from .cog_utils.image_utils import post_image, image_hash

class Memes(commands.Cog):

    memes_base_path = "./memes"

    def __init__(self, bot):
        self.bot = bot
        try:
            os.mkdir(Memes.memes_base_path)
        except:
            pass

    @commands.command(name="regMeme", description='register a meme for future use')
    async def reg_meme(self, ctx):
        try:
            await ctx.message.attachments[0].save(fp=f"{ctx.author}_temp_reg.png") 
        except IndexError as ex:
            logging.warning(f"{ctx.author} attempted to register meme without attaching image")
            return
        logging.info(f"registering {ctx.author}'s image...")

        # image hashing
        file_name = image_hash(f"{ctx.author}_temp_reg.png")

        img = Image.open(f"{ctx.author}_temp_reg.png")
        img.load()
        img.save(os.path.join(Memes.memes_base_path, file_name+".png"))
        os.remove(f"{ctx.author}_temp_reg.png")
    
    @commands.command(name="randMeme", description='get a random meme')
    async def rand_meme(self, ctx):
        files = os.listdir(Memes.memes_base_path)
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
        await post_image(os.path.join(Memes.memes_base_path, files[index]), ctx.channel)

async def setup(bot):
    await bot.add_cog(Memes(bot))

