# Bot Discord - Python
## Description
Il s'agit d'un bot discord codé en python.<br>Il est capable de répondre à des commandes questions a l'aide de l'API de Gemini,<br> lire le flux rss de tommus lyon 1 pour vous renvoyer la dernière note ajoutée et un jour peut-être donner les salles libres de l'IUT Lyon 1.

## Commandes
- `/helpme` : Renvoie les commandes disponible
- `/note` : Renvoie l'intitude de la dernière note ajoutée sur Tommus la note ne s'affiche pas. (ne fonctionne pas)
- `/noteV` : Renvoie la dernière note ajoutée sur le site de Tommus. (ne fonctionne pas)
- `/talk` : Renvoie une réponse à une question posée avec le contexte de la question.
- `/salle` : Renvoie les salles libres à l'heure actuelle.<br>
Vous pouvez filtrez les salles en ajoutant un tiret suivi du filtre (ex: `/salle - S27`)
ou les types de salles (ex: `/salle - TD `) mais aussi les deux (ex: `/salle - TD S27`)

## Installation
1. Installer les dépendances
```bash
pip install -r requirements.txt
```
2. Créer un fichier `config.py` à la racine du projet

3. Copier le contenu de `config.example.py` dans `config.py`

4. Remplacer toutes les valeurs par les votres

5. Lancer le bot
```bash
python bot.py
```
