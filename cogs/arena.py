import discord
from discord.ext import commands

import random
import logging

### arena
class Arena(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.arena_ongoing = False
        self.arena_players = []

    @commands.command(name="arenaStart", description='starts an arena game')
    async def arena_start(self, ctx):
        logging.debug("arena game attempted by", str(ctx.author)+"!")
        if self.arena_ongoing:
            await ctx.reply("arena game already ongoing. use $arena_join to join the game, or $arena_fight to conclude the ongoing game.")
            return

        self.arena_players.append(ctx.author)
        self.arena_ongoing = True
        await ctx.reply(str(ctx.author)+" started an arena game! type $arena_join to join.")

    @commands.command(name="arenaJoin", description='enters an arena game')
    async def arena_join(self, ctx):
        if not self.arena_ongoing:
            ctx.reply("no on going arena match. Start one with $arena_start!")
            return

        self.arena_players.append(ctx.author)
        await ctx.reply(str(ctx.author)+" is joining the arena.")

    @commands.command(name="arenaFight", description='decides the winner of an arena game')
    async def arena_fight(self, ctx):
        if not self.arena_ongoing:
            ctx.reply("fuck off. $arena_start fag.")
            return

        winner_idx = random.randint(0, len(self.arena_players)-1)
        await ctx.reply(str(self.arena_players[winner_idx])+" won. Cool ig.")
        self.arena_ongoing = False
        self.arena_players = []

async def setup(bot):
    await bot.add_cog(Arena(bot))

