import discord
from discord.ext import commands

from PIL import Image
import random
import os
import logging

from .cog_utils.image_utils import post_image

class ImageModi(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invert", description='invert an attached image')
    async def invert(self, ctx):
        try:
            await ctx.message.attachments[0].save(fp=f"{ctx.author}_input.png") 
        except IndexError as ex:
            logging.warning(f"{ctx.author} attempted to invert without attaching image")
            return
        logging.info(f"nuking {ctx.author}'s image")        

        # nuke the image
        image = Image.open(f"{ctx.author}_input.png")
        image.load()
        r_c = image.split()[0].point(lambda i: 255-i)
        g_c = image.split()[1].point(lambda i: 255-i)
        b_c = image.split()[2].point(lambda i: 255-i)
        im = Image.merge("RGB",(r_c,g_c,b_c))
        im.save(f"{ctx.author}_output.png")

        await post_image(f"{ctx.author}_output.png", ctx.channel)

        # await ctx.channel.send(file=discord.File(f"{ctx.author}_output.png"))
    
    @commands.command(name="pointTrans", description='Apply point transformation to an image. Specify a function in terms of x (try $pointTrans x**2 for example)')
    async def point_trans(self, ctx):
        try:
            contentType = ctx.message.attachments[0].content_type.split("/")[0]
            logging.debug(f"attachment type: {contentType}")
            if "image" not in contentType:
                raise ValueError("attachment not an image")
            await ctx.message.attachments[0].save(fp=f"{ctx.author}_input.png") 
        except IndexError as ex:
            logging.warning(f"{ctx.author} attempted to transform without attaching image")
            return
        except ValueError as ex:
            logging.warning(f"{ctx.author} attempted to transform non image")
        logging.info(f"transforming {ctx.author}'s image")        

        # nuke the image
        image = Image.open(f"{ctx.author}_input.png")
        image.load()
        try:
            func = eval("lambda x: "+ctx.message.content.split(" ", 1)[-1])
            logging.debug("using lambda: " + str(ctx.message.content.split(" ", 1)[-1]))
            r_c = image.split()[0].point(func)
            g_c = image.split()[1].point(func)
            b_c = image.split()[2].point(func)
        except (SyntaxError, NameError, TypeError) as lambda_except:
            logging.warning(f"{ctx.author} gave invalid lambda to pointTrans")
            return

        im = Image.merge("RGB",(r_c,g_c,b_c))
        im.save(f"{ctx.author}_output.png")

        await post_image(f"{ctx.author}_output.png", ctx.channel)

    @commands.command(name="compress", description='heavily compress an image.')
    async def compress(self, ctx):
        try:
            contentType = ctx.message.attachments[0].content_type.split("/")[0]
            logging.debug(f"attachment type: {contentType}")
            if "image" not in contentType:
                raise ValueError("attachment not an image")
            await ctx.message.attachments[0].save(fp=f"{ctx.author}_input.png") 
        except IndexError as ex:
            logging.warning(f"{ctx.author} attempted to transform without attaching image")
            return
        except ValueError as ex:
            logging.warning(f"{ctx.author} attempted to transform non image")
        logging.info(f"transforming {ctx.author}'s image")        

        # nuke the image
        image = Image.open(f"{ctx.author}_input.png")
        image.load()
        image = image.convert("RGB")
        image.save(f"{ctx.author}_output.jpg", quality=1, format='JPEG')

        await post_image(f"{ctx.author}_output.jpg", ctx.channel)
        os.remove(f"{ctx.author}_output.jpg")


async def setup(bot):
    await bot.add_cog(ImageModi(bot))

