from discord.ext import commands
from discord.utils import get
import random
import discord

class CogFunStuff(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    
    @commands.command (name="roll", aliases = ["Roll","rolls","Rolls"])
    async def roll(self,ctx,die : str):
        sides = int(die.trim("d",flags=die.IGNORECASE)[0])
        number = random.randint(1,sides)
        await ctx.channel.send(f"you rolled a {number} on the D{sides}")