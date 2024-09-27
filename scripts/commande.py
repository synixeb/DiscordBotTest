import requests
import datetime
import xml.etree.ElementTree as ET
import os

Classe = os.getenv('CLASSE')
fichierLog = os.getenv('fichierLog')

def makeURL(nom):
    url = "https://tomuss.univ-lyon1.fr/S/2024/Printemps/rss/"
    code_etudiant = os.getenv(nom)
    if code_etudiant != None:
        url += code_etudiant
        return url
    return None

def readXMLNote(url):
    table = []
    res = requests.get(url)
    root = ET.fromstring(res.content)
    for child in root.iter('item'):
        titre = child.find('title').text
        description = child.find('description').text
        auteur = child.find('author').text
        table.append([titre, description, auteur])
    last = table[-1]
    last[1] = removeHtmlBalise(last[1])
    last[2] = removeHtmlBalise(last[2])
    return last


def readXML(url):
    table = []
    res = requests.get(url)
    root = ET.fromstring(res.content)
    for child in root.iter('item'):
        description = child.find('description').text
        auteur = child.find('author').text
        table.append([description, auteur])
    last = table[-1]

    last[0] = removeHtmlBalise(last[0])
    last[0] = tronquer(last[0], ",")
    return last


def tronquer (chain, char):
    if chain.count(char) % 2 == 0:
        for i in range(chain.count(char)//2):
            chain = chain[:chain.find(char)] + chain[chain.rfind(char)+1:]
    return chain


def removeHtmlBalise(string):
    string = string.replace("<p>", "")
    string = string.replace("</p>", "")
    string = string.replace("<br>", "\n")
    string = string.replace("<b>", "")
    string = string.replace("</b>", "")
    return string

def log(message, author, niveau):
    switcher = {
        0: "DEBUG",
        1: "INFO",
        2: "WARNING",
        3: "ERROR",
        4: "CRITICAL",
        5: "FATAL"
    }
    niveau = switcher.get(niveau)
    Date = datetime.datetime.now()

    msg = f"({Date}) / {niveau} : {author} : {message}"
    print(msg)
    with open(fichierLog, "a") as f:
        f.write(msg + "\n")