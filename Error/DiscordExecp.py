import discord
from discord.ext import commands
import os

ISSUE_URL = os.getenv("ISSUE_URL")
class DiscordExecp(commands.CommandError):
    def __init__(self, ctx, error):
        self.ctx = ctx
        self.error = error

    async def send_error(self):
        if ISSUE_URL != None:
            desc = f"Pour vous plaindre auprès du développeur, créez une [issue]({ISSUE_URL})"
        else:
            desc = "Navré, mais le lien vers les issues n'a pas été configuré"
            
        embed = discord.Embed(
            title=self.error,
            description=desc,
            color=discord.Color.red()
        )
        await self.ctx.send(embed=embed)
