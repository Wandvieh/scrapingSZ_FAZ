import os
from os.path import join
import requests
from scrapy.selector import Selector as sel
import re

CUSTOMORDNERNAME = True

eingabe = "data science"
eingabeFrom = ""
eingabeTo = ""
eingabeOrdner = "sz"
if eingabeFrom != "" and not re.search("[0123][0-9]\.[01][0-9]\.[12][09][0-9][0-9]", eingabeFrom):
    print("Datum wurde nicht richtig eingegeben!")
    exit()
if eingabeTo != "" and not re.search("[0123][0-9]\.[01][0-9]\.[12][09][0-9][0-9]", eingabeTo):
    print(text="Datum wurde nicht richtig eingegeben!")
    exit()
#Überprüfen, ob ein anderer Ordner angelegt werden soll
if CUSTOMORDNERNAME:
    if os.path.exists(join("data", eingabeOrdner)) == False:
        try:
            os.mkdir(join('data', eingabeOrdner))
            ordnername = eingabeOrdner
        except OSError:
            print("Erstellung eines Ordners fehlgeschlagen! Datenerstellung wurde abgebrochen.")
            exit()
    ordnername = eingabeOrdner
else:
#Ordner erstellen, falls noch nicht vorhanden
    if os.path.exists(join("data", "sz")) == False:
        try:
            os.mkdir(join("data", "sz"))
            ordnername = "sz"
        except OSError:
            print(text="Erstellung eines Ordners fehlgeschlagen! Datenerstellung wurde abgebrochen.")
            exit()
    ordnername = "sz"


#Anzahl der Ergebnisseiten ermitteln
url = 'https://www.sueddeutsche.de/suche' # suche statt news
parameter = {"search": eingabe, "typ[]": "article"}
if eingabeFrom != "":
    parameter['startDate'] = eingabeFrom
if eingabeTo != "":
    parameter['endDate'] = eingabeTo
req = requests.get(url, params=parameter)
try:
    seitenanzahl = range(int(sel(text=req.text).xpath('//li[@class="navigation"]/ol/li[last()]/a/text()').get()))
except:
    seitenanzahl=range(0,1)
if len(seitenanzahl) > 10:
    seitenanzahl=range(0,4)

print(seitenanzahl)
exit()
#Die Artikel jeder Seite durchgehen und abspeichern
count = 0
for seite in seitenanzahl:
    url_temp = url + '/page/' + str(seite + 1)
    req = requests.get(url_temp, params=parameter)
    ergebnisliste = sel(text=req.text).xpath('//a[@class="entrylist__link"]/@href').getall()
    #Die Ergebnisse jeder Seite durchgehen und die Seiten als txt abspeichern
    for ergebnisURL in ergebnisliste:
        dateiname = ergebnisURL.split('/')[-1].split('.')[0] + '.txt'
        #Prüfung, ob die Datei schon abgespeichert wurde (dann geht die Schleife in die nächste Iteration)
        if os.path.exists(join('data', ordnername, dateiname)):
            continue
        req = requests.get(ergebnisURL)
        text_liste = sel(text=req.text).xpath('//p/text() | //p/*/text() | //p/*/*/text()').getall()
        text = 'Link: ' + ergebnisURL + '\n\n'
        for item in text_liste:
            text = text + item
        with open (join('data', ordnername, dateiname), 'w', encoding='utf-8') as f:
            f.write(text)
        count += 1
anzahlAbgespeichert = "Es wurden " + str(count) + " Texte abgespeichert."
ttk.Label(top, text=anzahlAbgespeichert).pack(padx=10, pady=5)