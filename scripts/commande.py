import requests
import datetime
import xml.etree.ElementTree as ET
import os
import re


fichierLog = os.getenv('FICHIER_LOG')

def makeURL(nom):
    url = "https://tomuss.univ-lyon1.fr/S/2024/Printemps/rss/"
    code_etudiant = os.getenv(nom)
    if code_etudiant != None:
        url += code_etudiant
        return url
    else:
        raise Exception("Cette étudiant n'existe pas")


def readXMLNote(url):
    table = []
    last = []
    res = requests.get(url)
    root = ET.fromstring(res.content)
    print("1")
    for child in root.iter('item'):
        print("2")
        titre = child.find('title').text
        description = child.find('description').text
        table.append([titre, description])

    for t in table:
        if re.match(r'[A-Za-z0-9]{1,}:[0-9]{2,}\.[0-9]{2,}/[0-9]{1,}', t[1]):
            last[1] = removeHtmlBalise(last[1])
            last[2] = removeHtmlBalise(last[2])
    return last, True


def readXML(url):
    table = []
    last = []
    res = requests.get(url)
    root = ET.fromstring(res.content)
    for child in root.iter('item'):
        titre = child.find('title').text
        print(titre)
        description = child.find('description').text
        table.append([titre, description])
    
    for t in reversed(table):
        if re.match(r'[A-Za-z0-9]{1,}:[0-9]{2,}\.[0-9]{2,}/[0-9]{1,}', t[1]):
            last = t

    if last != []:
        last[1] = removeHtmlBalise(last[1])
        last[1] = tronquer(last[1], ",")
    return last, False


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

def log(message, author, niveau=1):
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