import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

import os
import logging

intents = discord.Intents.default()
intents.message_content = True

arena_ongoing = False
arena_players = []


class myBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cog_names = []

    def get_cluster(self):
        return self.cluster

    async def on_ready(self):
        """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

        logging.info(f'Logged in as: {self.user.name} - {self.user.id}')
        logging.info(f'Version: {discord.__version__}')

        await self.change_presence(activity=discord.Game(name='investigating alternative forms of intelligence', type=1))

        num_cogs = len(os.listdir("cogs"))
        logging.info(f"loading {num_cogs} cogs")
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                logging.debug(f"loading cog {name}...")
                self.cog_names.append(f"cogs.{name}")
                await self.load_extension(f"cogs.{name}")
                
        logging.info(f'Successfully logged in and booted...!')
    
    @commands.command(name='help')
    async def help(self, ctx):
        ret = ""
        for cog in self.cog_names:
            ret += "**"+cog+"**"
        ctx.reply(ret)


bot = myBot(intents=intents, command_prefix="$", case_insensitive=True)


@bot.command(name="log", description='starts logging voice chat')
async def log(ctx):
    logging.debug("log func called")
    await ctx.reply("item")
    await bot.load_extension('arena')

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

try:
    tok = ""
    with open("bot_token") as f:
        tok = f.read().strip()

    bot.run(tok, reconnect=True)
except FileNotFoundError:
    logging.fatal("put token in file called bot_token")
    open("bot_token", "w")
except discord.errors.LoginFailure:
    logging.fatal("Bad token in bot_token file")
    logging.fatal(f"found token: '{tok}'")

