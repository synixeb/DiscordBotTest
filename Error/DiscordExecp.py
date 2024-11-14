import discord
from discord.ext import commands

from config import ISSUES
class DiscordExecp(commands.CommandError):
    def __init__(self, ctx, error):
        self.ctx = ctx
        self.error = error

    async def send_error(self):
        if ISSUES != None:
            desc = f"Pour vous plaindre auprès du développeur, créez une [issue]({ISSUES}) sur le projet"
        else:
            desc = "Navré, mais le lien vers les issues n'a pas été configuré"
            
        embed = discord.Embed(
            title=self.error,
            description=desc,
            color=discord.Color.red()
        )
        await self.ctx.send(embed=embed)
