import requests
import datetime
import os
import re

import xml.etree.ElementTree as ET
from ics import Calendar

from Data.donnees import data_salle
from config import FICHIER_LOG, LIEN_RSS_TOMUSS

regexNote = r'[A-Za-z0-9]{1,}:[0-9]{2,}\.[0-9]{2,}/[0-9]{1,}'


def makeURL(nom):
    url = LIEN_RSS_TOMUSS
    nom = nom.upper()
    code_etudiant = os.getenv(nom)
    if code_etudiant != None:
        url += code_etudiant
        return url
    return None

def get_salle_libre(filter_salle):
    try:
        Today = datetime.datetime.now().strftime('%Y-%m-%d')
        Hour = datetime.datetime.now().hour
        salles_libre = []
        for salle in data_salle:
            if data_salle[salle]['type'] not in filter_salle and salle not in filter_salle:
                url = ("https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources="
                + str(data_salle[salle]['id']) + "&projectId=0&calType=ical&firstDate=" + Today + "&lastDate=" + Today)
                res = requests.get(url)
                if res.status_code == 200:
                    calendar = Calendar(res.text)
                    is_free = True
                    for event in calendar.events:
                        if event.begin.datetime.hour <= Hour < event.end.datetime.hour:
                            is_free = False
                            break
                    if is_free:
                        salles_libre.append(salle)
        return salles_libre
    except Exception as e:
        print(e)
        return None

def readXMLNote(url):
    try:
        table = []
        last = []
        res = requests.get(url)
        root = ET.fromstring(res.content)
        for child in root.iter('item'):
            titre = child.find('title').text
            description = child.find('description').text
            table.append([titre, description])

        for t in table:
            if re.match(regexNote, t[1]):
                last[0] = removeHtmlBalise(last[0])
                last[1] = removeHtmlBalise(last[1])
        return last, True
    except Exception as e:
        print(e)
        return e, True

def readXML(url):
    try:
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
            if re.match(regexNote, t[1]):
                last = t

        if last != []:
            last[1] = removeHtmlBalise(last[1])
            last[1] = tronquer(last[1], ",")
        return last, False
    except Exception as e:
        print(e)
        return e, False

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
    if FICHIER_LOG != None:
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
        msg = f"({Date}) | {niveau} : {author} : {message}"
        print(msg)
        with open(FICHIER_LOG, "a") as f:
            f.write(msg + "\n")