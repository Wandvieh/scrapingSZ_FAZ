import tkinter as tk
from tkinter import ttk
import os
from os.path import join
import glob
import requests
from scrapy.selector import Selector as sel
import re
import pandas as pd
import pygal

def sicherLoeschen():
    for file in glob.glob(join("data", "*", "*.txt")):
        os.remove(file)
    for ordner in glob.glob(join("data", "*")):
        os.rmdir(ordner)
    ttk.Label(top, text="Daten wurden gelöscht!").pack(padx=10, pady=5)

def datenLoeschen():
    #Verstecken der vorherigen Widgets
    zerstoerenListe = top.pack_slaves()
    for item in zerstoerenListe:
        item.pack_forget()
    #Widgets des neuen Bildschirms definieren und anzeigen
    ttk.Label(top, text="Alle vorhandenen Daten löschen? Das kann nicht mehr rückgängig gemacht werden!", foreground="red").pack(padx=10, pady=5)
    ttk.Button(top, text="Alle Daten löschen", command=sicherLoeschen).pack(padx=10, pady=5)
    btnZurueck.pack(padx=10, pady=5)
    btnEnde.pack(padx=10, pady=5)

def artikelSZ():
    #nach Artikeln auf Sueddeutsche.de suchen
    eingabe = eingabefeld.get()
    eingabeFrom = eingabefeldDatumFrom.get()
    eingabeTo = eingabefeldDatumTo.get()
    eingabeOrdner = eingabefeldOrdner.get()
    if eingabeFrom != "" and not re.search("[0123][0-9]\.[01][0-9]\.[12][09][0-9][0-9]", eingabeFrom):
        ttk.Label(top, text="Datum wurde nicht richtig eingegeben!").pack(padx=10, pady=5)
        return
    if eingabeTo != "" and not re.search("[0123][0-9]\.[01][0-9]\.[12][09][0-9][0-9]", eingabeTo):
        ttk.Label(top, text="Datum wurde nicht richtig eingegeben!").pack(padx=10, pady=5)
        return
    #Überprüfen, ob ein anderer Ordner angelegt werden soll
    if check.get() == 1:
        if os.path.exists(join("data", eingabeOrdner)) == False:
            try:
                os.mkdir(join('data', eingabeOrdner))
                ordnername = eingabeOrdner
            except OSError:
                ttk.Label(top, text="Erstellung eines Ordners fehlgeschlagen! Datenerstellung wurde abgebrochen.").pack(padx=10, pady=5)
                return
        ordnername = eingabeOrdner
    else:
    #Ordner erstellen, falls noch nicht vorhanden
        if os.path.exists(join("data", "sz")) == False:
            try:
                os.mkdir(join("data", "sz"))
                ordnername = "sz"
            except OSError:
                ttk.Label(top, text="Erstellung eines Ordners fehlgeschlagen! Datenerstellung wurde abgebrochen.").pack()
                return
        ordnername = "sz"
    #Anzahl der Ergebnisseiten ermitteln
    url = 'https://www.sueddeutsche.de/news'
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

def artikelFAZ():
    #nach Artikeln auf FAZ.net suchen
    #Überprüfen, ob das Datum richtig eingegeben wurde
    eingabe = eingabefeld.get()
    eingabeFrom = eingabefeldDatumFrom.get()
    eingabeTo = eingabefeldDatumTo.get()
    eingabeOrdner = eingabefeldOrdner.get()
    if eingabeFrom != "" and not re.search("[0123][0-9]\.[01][0-9]\.[12][09][0-9][0-9]", eingabeFrom):
        ttk.Label(top, text="Datum wurde nicht richtig eingegeben!").pack(padx=10, pady=5)
        return
    if eingabeTo != "" and not re.search("[0123][0-9]\.[01][0-9]\.[12][09][0-9][0-9]", eingabeTo):
        ttk.Label(top, text="Datum wurde nicht richtig eingegeben!").pack(padx=10, pady=5)
        return
    #Überprüfen, ob ein anderer Ordner angelegt werden soll
    if check.get() == 1:
        if os.path.exists(join("data", eingabeOrdner)) == False:
            try:
                os.mkdir(join('data', eingabeOrdner))
                ordnername = eingabeOrdner
            except OSError:
                ttk.Label(top, text="Erstellung eines Ordners fehlgeschlagen! Datenerstellung wurde abgebrochen.").pack(padx=10, pady=5)
                return
        ordnername = eingabeOrdner
    else:
    #Ordner erstellen, falls noch nicht vorhanden
        if os.path.exists(join("data", "faz")) == False:
            try:
                os.mkdir(join("data", "faz"))
                ordnername = "faz"
            except OSError:
                ttk.Label(top, text="Erstellung eines Ordners fehlgeschlagen! Datenerstellung wurde abgebrochen.").pack()
                return
        ordnername = "faz"
    #Anzahl der Ergebnisseiten ermitteln
    url = 'https://www.faz.net/suche/'
    parameter = {"query": eingabe, "type": "content", "ct": "article"}
    if eingabeFrom != "":
        parameter['from'] = eingabeFrom
    if eingabeTo != "":
        parameter['to'] = eingabeTo
    req = requests.get(url, params=parameter)
    temp = sel(text=req.text).xpath('//ul[@class="nvg-Paginator nvg-Paginator-is-right"]/li[last()]/a/@href').get()
    try:
        seitenanzahl = range(0, int(re.sub('[a-zA-Z]', '', temp.split('/')[-1].split('.')[0])))
    except:
        seitenanzahl=range(0,1)
    if len(seitenanzahl) > 10:
        seitenanzahl=range(0,10)
    #Die Artikel jeder Seite durchgehen und abspeichern
    count = 0
    #print(seitenanzahl)
    for seite in seitenanzahl:
        url_temp = url + 's' + str(seite + 1) + '.html'
        #print(url_temp)
        req = requests.get(url_temp, params=parameter)
        #print("1")
        #return
        ergebnisliste_temp = sel(text=req.text).xpath('//a[@class="js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink"]/@href').getall()
        #Unbrauchbare URLs filtern (da kein Zugang zu den Texten)
        ergebnisliste = []
        for ergebnis in ergebnisliste_temp:
            if "premiumContent" not in ergebnis:
                ergebnisliste.append(ergebnis)
        #Die Ergebnisse jeder Seite durchgehen und die Seiten als txt abspeichern
        for ergebnisURL in ergebnisliste:
            #print(ergebnisURL)
            dateiname = ergebnisURL.split('/')[-1].split('.')[0] + '.txt'
            #print(dateiname)
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

def datenErstellung():
    #Methode zur Erstellung neuer Datensätze
    #Globale Variablen erstellen, um sie in die anderen Definitionen übertragen zu können
    global eingabefeld
    global eingabefeldDatumFrom
    global eingabefeldDatumTo
    global check
    global eingabefeldOrdner
    #Verstecken der vorherigen Widgets
    zerstoerenListe = top.pack_slaves()
    for item in zerstoerenListe:
        item.pack_forget()
    #Widgets des neuen Bildschirms definieren
    textErstellung = ttk.Label(top, text="In diesem Fenster können neue Datensätze erstellt werden. Hierzu kann im Folgenden ein Suchwort eingegeben werden.\nMit einem Klick auf einen der Buttons wird automatisch eine Suche auf den entsprechenden Webseiten durchgeführt und die daraus resultierenden Artikel werden in den data-Ordner gespeichert.\nDuplikate werden hierbei gelöscht, die Suche kann also mehrmals mit mehreren Suchbegriffen durchgeführt werden.\nHinweis: Da es nicht möglich ist, alle Aritkel komplett bereinigt aus den Webseiten zu ziehen, sind möglicherweise einzelne zusätzliche Worte enthalten, die nicht Teil des Textes sind (bspw. Autor*innennamen).\nAuch werden keine Bilder oder Videos, sondern nur Text gespeichert. Auch Artikel, die nicht vollständig vorliegen (für die ein Abonnement benötigt wird), werden aussortiert.")
    eingabefeld = ttk.Entry(top)
    textDatum = ttk.Label(top, text="Falls eine zeitliche Eingrenzung gewünscht ist, bitte in den folgenden zwei Feldern das Anfangs- und Enddatum eingeben in der Form DD.MM.YYYY.\nFalls keine zeitliche Eingrenzung gewünscht ist, das Feld leer lassen (Achtung: Die Ergebnismenge kann sehr groß und das damit das Programm sehr langsam werden!)")
    textDatumFrom = ttk.Label(top, text="Beginn:")
    eingabefeldDatumFrom = ttk.Entry(top)
    textDatumTo = ttk.Label(top, text="Ende:")
    eingabefeldDatumTo = ttk.Entry(top)
    check = tk.IntVar()
    checkbox = ttk.Checkbutton(top, text="In selbst benanntem Ordner speichern?", variable=check)
    eingabefeldOrdner = ttk.Entry(top)
    eingabefeldOrdner.insert(0, "Ordnername")
    btnSZ = ttk.Button(top, text="Süddeutsche Zeitung", command=artikelSZ)
    btnFAZ = ttk.Button(top, text="Frankfurter Allgemeine Zeitung", command=artikelFAZ)
    #Weitere mögliche Seiten, die eingebaut werden können
    #btnSpiegel = ttk.Button(top, text="Der Spiegel")
    #btnBild = ttk.Button(top, text="BILD")
    #btnStern = ttk.Button(top, text="Stern")
    #btnFocus = ttk.Button(top, text="Focus Online")
    btnWeiterAnalyse = ttk.Button(top, text="Weiter zur Analyse", command=datenAnalyse)
    
    #Hinzufügen der Widgets zum Bildschirm
    textErstellung.pack(padx=10, pady=5)
    eingabefeld.pack(padx=10, pady=5)
    textDatum.pack(padx=10, pady=5)
    textDatumFrom.pack(padx=10, pady=5)
    eingabefeldDatumFrom.pack(padx=10, pady=5)
    textDatumTo.pack(padx=10, pady=5)
    eingabefeldDatumTo.pack(padx=10, pady=5)
    checkbox.pack(padx=10, pady=5)
    eingabefeldOrdner.pack(padx=10, pady=5)
    btnSZ.pack(padx=10, pady=5)
    btnFAZ.pack(padx=10, pady=5)
    btnWeiterAnalyse.pack(padx=10, pady=5)
    btnZurueck.pack(padx=10, pady=5)
    btnEnde.pack(padx=10, pady=5)

def TDMErstellung():
    global ergebnisse
    ergebnisse = pd.DataFrame()
    ordnerliste = glob.glob(join('data', '*'))
    #Jeden Ordner durchgehen, um die Inhalte zur TDM hinzuzufügen
    anzahl_worte = {}
    for ordner in ordnerliste:
        anzahl_worte[ordner] = 0
        dateienliste = glob.glob(join(ordner, '*.txt*'))
        for datei in dateienliste:
            #Text einlesen, bereinigen und in die einzelnen Wörter aufteilen
            fp = open(datei, 'r', encoding="utf-8")
            inhalt = re.sub("[.,!?/()„:{}]", "", fp.read().lower()).split()
            #Den selbst eingefügten Link wieder entfernen
            inhalt.pop(0)
            inhalt.pop(1)
            fp.close()
            anzahl_worte[ordner] = anzahl_worte[ordner] + len(inhalt)
            #Dictionary erstellen, Stopwords dabei filtern
            wortanzahl = {}
            stopwords = ["dpa-infocom", "jetztcss-io3sxkborder-colorcurrentcolor;colorinherit;margin-top4px;css-1px53trfont-family'szsansdigital''neue", "0;-webkit-text-decorationnone;text-decorationnone;-webkit-transitionborder-bottom", "ease-in-out;border-colorcurrentcolor;colorinherit;margin-top4px;css-1px53trfocuscss-1px53trhoverborder-bottom-colortransparent;jobs", "szcss-uwu0ixfont-family'szsansdigital''neue", "helvetica''helvetica'sans-serif;font-size14px;font-weight400;line-height13;margin-right12px;sie", 'gutschein', '150ms', 'sz', 'solid', 'permalink', '-', ':', 'permalink:', 'faznet', '2px', '0', "#29293a;color#29293a;cursorpointer;displayinline-block;line-height1;padding0", "helvetica''helvetica'sans-serif;font-size12px;font-weight400;letter-spacing0085em;line-height1;-webkit-align-selfbaseline;-ms-flex-item-alignbaseline;align-selfbaseline;background-colortransparent;bordernone;border-bottom1px", 'ease-in-out;transitionborder-bottom', 'aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 'ander', 'andere', 'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anderr', 'anders', 'auch', 'auf', 'aus', 'bei', 'bin', 'bis', 'bist', 'da', 'damit', 'dann', 'der', 'den', 'des', 'dem', 'die', 'das', 'dass', 'daß', 'derselbe', 'derselben', 'denselben', 'desselben', 'demselben', 'dieselbe', 'dieselben', 'dasselbe', 'dazu', 'dein', 'deine', 'deinem', 'deinen', 'deiner', 'deines', 'denn', 'derer', 'dessen', 'dich', 'dir', 'du', 'dies', 'diese', 'diesem', 'diesen', 'dieser', 'dieses', 'doch', 'dort', 'durch', 'ein', 'eine', 'einem', 'einen', 'einer', 'eines', 'einig', 'einige', 'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'er', 'ihn', 'ihm', 'es', 'etwas', 'euer', 'eure', 'eurem', 'euren', 'eurer', 'eures', 'für', 'gegen', 'gewesen', 'hab', 'habe', 'haben', 'hat', 'hatte', 'hatten', 'hier', 'hin', 'hinter', 'ich', 'mich', 'mir', 'ihr', 'ihre', 'ihrem', 'ihren', 'ihrer', 'ihres', 'euch', 'im', 'in', 'indem', 'ins', 'ist', 'jede', 'jedem', 'jeden', 'jeder', 'jedes', 'jene', 'jenem', 'jenen', 'jener', 'jenes', 'jetzt', 'kann', 'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines', 'können', 'könnte', 'machen', 'man', 'manche', 'manchem', 'manchen', 'mancher', 'manches', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines', 'mit', 'muss', 'musste', 'nach', 'nicht', 'nichts', 'noch', 'nun', 'nur', 'ob', 'oder', 'ohne', 'sehr', 'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'selbst', 'sich', 'sie', 'ihnen', 'sind', 'so', 'solche', 'solchem', 'solchen', 'solcher', 'solches', 'soll', 'sollte', 'sondern', 'sonst', 'über', 'um', 'und', 'uns', 'unsere', 'unserem', 'unseren', 'unser', 'unseres', 'unter', 'viel', 'vom', 'von', 'vor', 'während', 'war', 'waren', 'warst', 'was', 'weg', 'weil', 'weiter', 'welche', 'welchem', 'welchen', 'welcher', 'welches', 'wenn', 'werde', 'werden', 'wie', 'wieder', 'will', 'wir', 'wird', 'wirst', 'wo', 'wollen', 'wollte', 'würde', 'würden', 'zu', 'zum', 'zur', 'zwar', 'zwischen']
            for wort in inhalt:
                if wort not in stopwords:
                    if wort in wortanzahl:
                        wortanzahl[wort] += 1
                    else:
                        wortanzahl[wort] = 1
            #Dictionary in Series umwandeln
            haeufigkeiten = pd.Series(wortanzahl, name = datei)
            #Series dem Dataframe dazufügen
            ergebnisse = ergebnisse.append(haeufigkeiten).fillna(0)
        #print(anzahl_worte)
    ergebnisse = ergebnisse.T
    #Addierte Häufigkeiten der Zeitungen und insgesamt hinzufügen
    for ordner in ordnerliste:
        spaltenname = re.sub('data\W*', '', ordner)
        ergebnisse[spaltenname] = ergebnisse[glob.glob(join(ordner, '*.txt'))].sum(axis=1) / anzahl_worte[ordner]
    summe = 0
    for ordner in ordnerliste:
        summe = summe + ergebnisse[glob.glob(join(ordner, '*.txt'))].sum(axis=1)
    ergebnisse['Insgesamt'] = summe / sum(anzahl_worte.values())
    ergebnisse = ergebnisse.sort_values(by = "Insgesamt", ascending=False)
    #Ergebnisse speichern
    with open("Ergebnis.csv", "w", encoding="utf-8") as fp:
        ergebnisse[0:100].to_csv(fp, sep=";",line_terminator="\n")
    with open("Ergebnis.ods", "w", encoding="utf-8") as fp:
        ergebnisse[0:100].to_csv(fp, sep=";",line_terminator="\n")
    ttk.Label(top, text="Term-Dokument-Matrix erstellt!").pack(padx=10, pady=5)

def BarchartErstellung():
    global ergebnisse
    #Dataframe vorbereiten
    ordnerliste_temp = glob.glob(join('data', '*'))
    ordnerliste = ['Insgesamt']
    for ordner in ordnerliste_temp:
        neuerOrdner=re.sub('data\W*', '', ordner)
        ordnerliste.append(neuerOrdner)
    ergebnisse_neu = ergebnisse[ordnerliste][0:20]
    
    barchart = pygal.Bar()
    barchart.title = "20 häufigste Wörter"
    barchart.x_labels = map (str, ergebnisse_neu.index.values)
    for x in ergebnisse_neu.items():
        barchart.add(x[0], x[1])
    barchart.render_to_file('Worthaeufigkeiten_Barchart_nachWort.svg')
    
    ergebnisse_T = ergebnisse_neu.T
    
    barchart2 = pygal.Bar()
    barchart2.title = "20 häufigste Wörter"
    barchart2.x_labels = map (str, ordnerliste)
    for x in ergebnisse_T.items():
        barchart2.add(x[0], x[1])
    barchart2.render_to_file('Worthaeufigkeiten_Barchart_nachZeitung.svg')
    
    ttk.Label(top, text="Barcharts erstellt!").pack(padx=10, pady=5)

def datenAnalyse():
    #Verstecken der vorherigen Widgets
    zerstoerenListe = top.pack_slaves()
    for item in zerstoerenListe:
        item.pack_forget()
    #Widgets des neuen Bildschirms definieren
    textAnalyse = ttk.Label(top, text="Die Analyse gliedert sich in mehrere Schritte.\nZuerst wird eine Term-Dokument-Matrix erstellt.\nAnschließend werden die insgesamt 20 häufigsten Wörter in einem Linechart ausgegeben.\nDie daraus entstehenden Dateien werden im selben Ordner wie das Programm gespeichert und sind dort abrufbereit.")
    btnTDM = ttk.Button(top, text="Term-Dokument-Matrix erstellen", command=TDMErstellung)
    btnLinechart = ttk.Button(top, text="Barchart erstellen", command=BarchartErstellung)
    btnZurueckDatenset = ttk.Button(top, text="Zurück zur Erstellung des Datensets", command=datenErstellung)
    
    #Hinzufügen der Widgets zum Bildschirm
    textAnalyse.pack(padx=10, pady=5)
    btnTDM.pack(padx=10, pady=5)
    btnLinechart.pack(padx=10, pady=5)
    btnZurueckDatenset.pack(padx=10, pady=5)
    btnZurueck.pack(padx=10, pady=5)
    btnEnde.pack(padx=10, pady=5)

def zurueckStartseite():
    #Zurück zur Startseite kehren
    #Verstecken der vorherigen Widgets
    zerstoerenListe = top.pack_slaves()
    for item in zerstoerenListe:
        item.pack_forget()
    #Widgets der Startseite wieder anzeigen
    textIntro.pack(padx=10, pady=5)
    btnErstellung.pack(padx=10, pady=5)
    btnAnalyse.pack(padx=10, pady=5)
    btnLoeschen.pack(padx=10, pady=5)
    btnEnde.pack(padx=10, pady=5)

#Initialisierung der Benutzeroberfläche
top = tk.Tk()
top.title("Durchführen einer Framing-Analyse")
top.geometry("1000x600")

#Widgets des Startbildschirms definieren
textIntro = ttk.Label(top, text="Dies ist ein Programm zur Zusammenstellung von Artikeln zu einem Datensatz und der automatischen Auswertung und Speicherung der Ergebnisse.")
btnErstellung = ttk.Button(top, text="Neuen Datensatz erstellen", command=datenErstellung)
btnAnalyse = ttk.Button(top, text="Datensatz auswerten", command=datenAnalyse)
btnLoeschen = ttk.Button(top, text="Vorhandenen Datensatz löschen", command=datenLoeschen)
btnErgebnisse = ttk.Button(top, text="Ergebnisse anzeigen")

#Widgets, die in mehr als einem Fenster benötigt werden
#global btnZurueck
btnZurueck = ttk.Button(top, text="Zurück zur Startseite", command=zurueckStartseite)
#global btnEnde
btnEnde = ttk.Button(top, text="Programm beenden", command=top.destroy)

#Hinzufügen der Widgets zum Startbildschirm
textIntro.pack(padx=10, pady=5)
btnErstellung.pack(padx=10, pady=5)
btnAnalyse.pack(padx=10, pady=5)
btnLoeschen.pack(padx=10, pady=5)
btnEnde.pack(padx=10, pady=5)

#Programm laufen lassen
top.mainloop()