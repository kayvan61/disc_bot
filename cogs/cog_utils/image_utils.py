import discord
from discord.ext import commands

import os
import logging
from PIL import Image

async def post_image(path, channel):

        # compress...
        file_size = os.path.getsize(path)
        cur_qual = 90
        while file_size >= 8<<20 and cur_qual > 10:
            logging.debug("file too big. compress quality:", cur_qual)
            im = Image.open(path)
            im.load()
            im.save(path, optimize=True, quality=cur_qual)
            cur_qual = int(cur_qual / 2)
        
        # crop...
        file_size = os.path.getsize(path)
        if file_size >= 8<<20:
            scale_fact = (8<<20) / file_size
            logging.debug(f"file too big. crop scale_fact: {scale_fact}")
            im = Image.open(path)
            im.load()
            new_size = [int(x * scale_fact) for x in im.size]

            logging.debug(f"new size: {new_size}")

            im = im.resize(new_size, Image.LANCZOS)
            im.save(path, optimize=True, quality=cur_qual)
        
        logging.debug(f"sending image {path} to channel {channel}")

        await channel.send(file=discord.File(path))

def image_hash(path):
    img = Image.open(path)
    img.load()
    img = img.resize((10, 10), Image.ANTIALIAS)
    img = img.convert("L")
    pixel_data = list(img.getdata())
    avg_pixel = sum(pixel_data)/len(pixel_data)
    bits = "".join(['1' if (px >= avg_pixel) else '0' for px in pixel_data])
    hex_representation = str(hex(int(bits, 2)))[2:][::-1].upper()
    return hex_representation
