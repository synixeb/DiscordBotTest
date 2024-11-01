# Bot Discord - Python
## Description
Il s'agit d'un bot discord codé en python. Il est capable de répondre à des commandes questions a l'aide de l'API de Gemini, lire le flux rss de tommus lyon 1 pour vous renvoyer la dernière note ajoutée et un jour peut-être donner les salles libres de l'IUT Lyon 1.

## Commandes
- `/helpme` : Renvoie les commandes disponible
- `/note` : Renvoie l'intitude de la dernière note ajoutée sur Tommus (la note n'est pas affichée) (ne fonctionne pas)
- `/noteV` : Renvoie la dernière note ajoutée sur le site de Tommus (ne fonctionne pas)
- `/talk` : Renvoie une réponse à une question posée avec le contexte de la question (fonctionne)
- `/salle` : Renvoie les salles libres à l'heure actuelle (fonctionne)
vous pouvez filtrez les salles en ajoutant un tiret suivi du filtre (ex: `/salle S27`)
ou les types de salles (ex: `/salle - TD `) mais aussi les deux (ex: `/salle - TD S27`)

## Installation
1. Installer les dépendances
```bash
pip install -r requirements.txt
```
2. Créer un fichier `.env` à la racine du projet
3. Ajouter les lignes suivantes dans le fichier `.env`

```
GENERATIVEAI_API_KEY = YOUR_API_KEY_FOR_GEMINI
TOKEN = YOUR_TOKEN_FOR_DISCORD
FICHIER_LOG = le_nom_de_votre_fichier_log_depuis_la_racine_du_projet
ISSUE_URL = url_des_issues_de_votre_projet
nom_dutilisateur_discord = code_rss_de_tomuss
```
4. Remplacer `token` par le token de votre bot discord et le token de l'API de Gemini
5. Lancer le bot
```bash
python bot.py
```
