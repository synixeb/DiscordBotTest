import discord
from discord.ext import commands
import os

PROJET_URL = os.getenv("PROJET_URL")
RELATIF_VERS_ISSUE = os.getenv("RELATIF_VERS_ISSUE")

class DiscordExecp(commands.CommandError):
    def __init__(self, ctx, error):
        self.ctx = ctx
        self.error = error

    async def send_error(self):
        if PROJET_URL != None and RELATIF_VERS_ISSUE != None:
            desc = f"Pour vous plaindre auprès du développeur, créez une [issue]({PROJET_URL}{RELATIF_VERS_ISSUE}) sur le projet"
        else:
            desc = "Navré, mais le lien vers les issues n'a pas été configuré"
            
        embed = discord.Embed(
            title=self.error,
            description=desc,
            color=discord.Color.red()
        )
        await self.ctx.send(embed=embed)
