# Bot Discord - Python
## Description
Il s'agit d'un bot discord codé en python. Il est capable de répondre à des commandes questions a l'aide de l'API de Gemini, lire le flux rss de tommus lyon 1 pour vous renvoyer la dernière note ajoutée et un jour peut-être donner les salles libres de l'IUT Lyon 1.

## Commandes
- `/helpme` : Renvoie les commandes disponible
- `/note` : Renvoie l'intitude de la dernière note ajoutée sur Tommus (la note n'est pas affichée) (ne fonctionne pas)
- `/noteV` : Renvoie la dernière note ajoutée sur le site de Tommus (ne fonctionne pas)
- `/talk` : Renvoie une réponse à une question posée avec le contexte de la question (fonctionne)
- `/salle` : Renvoie les salles libres à l'heure actuelle (fonctionne) \
vous pouvez filtrez les salles en ajoutant un tiret suivi du filtre (ex: `/salle - S27`)
ou les types de salles (ex: `/salle - TD `) mais aussi les deux (ex: `/salle - TD S27`)

## Installation
1. Installer les dépendances
```bash
pip install -r requirements.txt
```
2. Créer un fichier `.env` à la racine du projet en copiant le contenu de `.env.example`

3. Remplacer toutes les valeurs par les votres du fichier `.env` par les votre

4. Lancer le bot
```bash
python bot.py
```
