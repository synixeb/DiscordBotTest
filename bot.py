import discord
from discord.ext import commands
from scripts.commande import *
from scripts.textGeneration import *

import Error.DiscordExecp as DiscordExecp
from config import TOKEN_DISCORD, PROJET_URL
from Data.donnees import profs
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Connecter en tant que {bot.user}')
    await bot.change_presence(activity=discord.Game(name="aider les étudiant"))
    log("Bot connecté", "Bot", 1)


async def send_note_info(ctx: commands.Context, note_func):
    try:
        url = makeURL(ctx.author.name)
        if isinstance(url, str):
            tab, isNote = note_func(url)
            if isinstance(tab, str):
                raise Exception(tab)
            elif tab == []:
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
            raise Exception("Erreur lors de la récupération de l'url")
    except Exception as e:
        log(e, ctx.author.name, 2)
        await DiscordExecp.DiscordExecp(ctx, "Erreur lors de la récupération de la note").send_error()


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
        
        text = text_generation(full_prompt)
        await ctx.send(text)
        log(f"Context Prompt: ({prompt}) / V", ctx.author.name, 1)
    except Exception as e:
        log(e ,ctx.author.name, 2)
        await DiscordExecp.DiscordExecp(ctx, f"Context Prompt: ({prompt}) / X").send_error()


@bot.command()
async def salle(ctx: commands.Context, *args):
    try:
        filter_salle = []
        if len(args) > 0 and args[0] == "-":
                filter_salle = args[1:]
        await ctx.send("Recherche des salles libres ...")
        salles = get_salle_libre(filter_salle)
        if salles == None:
            raise Exception("Erreur lors de la récupération des salles")
        elif salles == []:
            await ctx.send("Aucune salle libre ;(")
        else:
            msg = ""
            await ctx.send("Les salles libres sont:")
            for salle in salles:
                msg += salle + " " + data_salle[salle]["type"] + "\n"
            await ctx.send(msg)
            await ctx.send("Fin de la liste")
        log("Salle envoyée", ctx.author.name)
    except Exception as e:
        log(e,ctx.author.name,3)
        await DiscordExecp.DiscordExecp(ctx, "Erreur lors de la recuperation des salles").send_error()

@bot.command()
async def prof(ctx: commands.Context, nom: str, *args):
    try:
        if nom.lower() not in profs:
            raise Exception("Le professeur n'existe pas")
        if len(args) > 0 and args[0].isdigit() and 0 <= int(args[0]) < 24:
            msg = f"A {args[0]}h {nom.capitalize()} sera en "
            location = get_prof_location(nom.lower(), int(args[0]))
        else:
            msg = f"{nom.capitalize()} est en "
            location = get_prof_location(nom.lower())
        if location == 0:
            raise Exception("Erreur lors de la récupération de la localisation")
        elif location == None:
            await ctx.send(f"{nom.capitalize()} n'a pas de cours à cette heure")
            log(nom+" n'a pas de cours à cette heure", ctx.author.name)
        else:
            await ctx.send(msg + location)
            log("Localisation de "+nom+" envoyée", ctx.author.name)
    except ValueError as e:
        log(e, ctx.author.name, 2)
        await DiscordExecp.DiscordExecp(ctx, "L'argument fourni pour l'heure n'est pas un entier valide").send_error()
    except Exception as e:
        log(e, ctx.author.name, 2)
        await DiscordExecp.DiscordExecp(ctx, "Erreur de récupération de la localisation de "+nom).send_error()

@bot.command()
async def err(ctx: commands.Context):
    try:
        raise Exception("Test du format des erreurs")
    except Exception as e:
        log(e, ctx.author.name, 0)
        await DiscordExecp.DiscordExecp(ctx, e).send_error()


@bot.command()
async def helpme(ctx: commands.Context):
    msg = ""
    msg +="`/helpme` : Renvoie les commandes disponible (fonctionne)\n"
    msg +="`/note` : Renvoie l'intitude de la dernière note ajoutée sur Tommus (la note n'est pas affichée) (ne fonctionne pas) \n"
    msg +="`/noteV` : Renvoie la dernière note ajoutée sur le site de Tommus (ne fonctionne pas)\n"
    msg +="`/talk` : Renvoie une réponse à une question posée avec le contexte de la question (fonctionne)\n"
    msg +="`/salle` : Renvoie les salles libres à l'heure actuelle (ne fonctionne pas)\n"
    msg +="vous pouvez filtrez les salles en ajoutant un tiret suivi du filtre (ex: `/salle - S27`)\n"
    msg +="ou les types de salles (ex: `/salle - TD `) mais aussi les deux (ex: `/salle - TD S27`)"
    await ctx.send(msg)
    if PROJET_URL != None:
        await ctx.send("Mais vous pouvez aussi m'aider à m'améliorer en participant au [projet]({})".format(PROJET_URL))
    log("Aide demandée", ctx.author.name)


if __name__ == '__main__':
    bot.run(TOKEN_DISCORD)
