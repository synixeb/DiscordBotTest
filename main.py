import discord
from discord.ext import commands
from scripts.commande import *
from scripts.textGeneration import *

TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Connecter en tant que {bot.user}')
    log("Bot connecté", "Bot", 1)

@bot.command()
async def note(ctx : commands.Context):
    url = makeURL(ctx.author.name)
    if url != None:
        tab = readXML(url)
        await ctx.send("La dernière note ajoutée est:")
        await ctx.send(f"Intitulé: {tab[0]}")
        await ctx.send(f"Auteur: {tab[1]}")
        log("Note envoyée", ctx.author.name, 1)
    else:
        await ctx.send("Cette étudiant n'existe pas")
        log("L'étudiant n'existe pas", ctx.author.name, 2)
        

@bot.command()
async def saymyname(ctx : commands.Context):
    await ctx.send(ctx.author.name)
    log("Help", ctx.author.name, 0)


@bot.command()
async def noteV(ctx : commands.Context):
        url = makeURL(ctx.author.name)
        if url != None:
            tab = readXMLNote(url)
            await ctx.send("La dernière note ajoutée est:")
            await ctx.send(f"Titre: {tab[0]}")
            await ctx.send(f"Intitulé: {tab[1]}")
            await ctx.send(f"Auteur:{tab[2]}")
            log("Note envoyée", ctx.author.name, 1)
        else:
            await ctx.send("Cette étudiant n'existe pas")
            log("L'étudiant n'existe pas", ctx.author.name, 2)


@bot.command()
async def talk(ctx: commands.Context, *args):
    try:
        messages = [message async for message in ctx.channel.history(limit=10)]
        context = "\n".join([f"{msg.author.name}: {msg.content}" for msg in messages])
        
        prompt = ' '.join(args)
        full_prompt = f"Context: \n <--//{context}//--> \n\nPrompt:\n >**++{prompt}++--<"
        
        # Generate text based on the full prompt
        text = text_generation(full_prompt)
        await ctx.send(text)
        log(f"Context Prompt: ({prompt}) / V", ctx.author.name, 1)
    except Exception as e:
        print(e)
        await ctx.send("Désole, je n'ai pas pu générer de texte")
        await ctx.send("Surement la faute à un mauvais developpeur")
        log(f"Context Prompt: ({prompt}) / X", ctx.author.name, 2)

if __name__ == '__main__':
    bot.run(TOKEN)