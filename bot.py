import discord
from discord.ext import commands
from scripts.commande import *
from scripts.textGeneration import *

TOKEN = os.getenv("TOKEN_DISCORD")
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Connecter en tant que {bot.user}')
    await bot.change_presence(activity=discord.Game(name="aider les étudiant"))
    log("Bot connecté", "Bot", 1)


async def send_note_info(ctx: commands.Context, note_func):
    try:
        url = makeURL(ctx.author.name)
        if url:
            print(url)
            tab, isNote = note_func(url)
            if tab == []:
                await ctx.send("Aucune note n'a été ajoutée")
                log("Aucune note n'a été ajoutée", ctx.author.name)
            else:
                await ctx.send("La dernière note ajoutée est:")
                await ctx.send(f"Titre: {tab[0]}")
                await ctx.send(f"Intitulé: {tab[1]}")
                if isNote:
                    await ctx.send(f"Auteur: {tab[2]}")
                log("Note envoyée", ctx.author.name)
        else:
            raise Exception("Cet étudiant n'existe pas")
    except Exception as e:
        await ctx.send(str(e))
        await ctx.send("Pour vous plaindre auprès du développeur, créez une [issue](https://github.com/synixeb/DiscordXGemini/issues) sur le repo GitHub")
        log(e, ctx.author.name, 3)

@bot.command()
async def note(ctx: commands.Context):
    await send_note_info(ctx, readXML)

@bot.command()
async def noteV(ctx: commands.Context):
    await send_note_info(ctx, readXMLNote)


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
        await ctx.send("Pour vous plaindre auprès du développeur, créez une [issue](https://github.com/synixeb/DiscordXGemini/issues) sur le repo GitHub")
        log(f"Context Prompt: ({prompt}) / X", ctx.author.name, 2)

if __name__ == '__main__':
    bot.run(TOKEN)