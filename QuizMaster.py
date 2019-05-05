#!/usr/bin/env python
# -*- coding: utf-8 -*-

zeitmessungAktiv = 0 #0 für aus, 1 für an. Zeitmessung bestimmt die Laufzeit des Skripts

if zeitmessungAktiv == 1:
   import time
   start = time.time()

import pyperclip #used to save Var result into clipboard
import pytesseract
import webbrowser
import PIL.ImageGrab
from PIL import Image, ImageEnhance, ImageFilter
import requests
from difflib import SequenceMatcher
import difflib
import string

import re #regex

#function cleanhtml - erases html tags from the result
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

snapshot = PIL.ImageGrab.grab() #used to create a screenshot

devmode = '0' #dev mode uses the "example.png"-file or any ohter file that you configured
debugResult = '0' #If debugResult = 1 > enables debugging of the result
userpath = "C:\\Users\\YourName\\Desktop" #configure your userpath here, for example: "C:\\Users\\YourName\\"

im = Image.open(userpath + "\\example.png") #only used in DEV mode

if devmode != '1': #only creates a screenshot if devmode = false
   save_path = userpath + "\\cash.png"
   snapshot.save(save_path)
   im = Image.open(userpath + "\\cash.png")
else:
   print ('DEVMODE ---- DEVMODE')
#initialize variables
wahrscheinlichkeitenDictionary = {}
mratioDifferenceFloat = 0.6 #float-value to define the ratio of likeness between the "real answer" and the found results by the script.
# for example: if you compare "Egg" to "Egg" a ratio of 1.0 would lead to the exact result, but that is a very unrealistic case. especially if you get results that uses the plural ("Eggs") you need a lower ratio than 1.0.
# a good value in my tests were 0.6 - 0.7

#NAD = nummernAusgeschriebenDictionary
#a list that contains the numbers and also the words in a range from 0-20. it is used for the results, because lower value numbers are often written as words.
nummernAusgeschriebenDictionary = {"0":"null","1":"eins","2":"zwei","3":"drei","4":"vier","5":"fünf","6":"sechs","7":"sieben","8":"acht","9":"neun","10":"zehn","11":"elf","12":"zwölf","13":"dreizehn","14":"vierzehn","15":"fünfzehn","16":"sechszehn","17":"siebzehn","18":"achtzehn","19":"neunzehn","20":"zwangzig"}

DefiniereBereich_AntwortA = (834, 592, 1423, 682) #defines the area of Answer A
QuizmasterAntwortAArea = im.crop(DefiniereBereich_AntwortA)
AntwortA_SavePath = userpath + "\\cs_antworta.png"
QuizmasterAntwortAArea.save(AntwortA_SavePath)
AntwortAText = pytesseract.image_to_string(Image.open(AntwortA_SavePath),lang="deu") #config='-psm 5'
if not AntwortAText: #Wenn AntwortAText keinen Wert hat, handelt es sich evtl um einen einzelnen Buchstaben / Charakter. In dem Fall Config aktivieren
   AntwortAText = pytesseract.image_to_string(Image.open(AntwortA_SavePath),lang="deu",config='--psm 6')
    
DefiniereBereich_AntwortB = (832, 737, 1425, 824) #defines the area of Answer B
QuizmasterAntwortBArea = im.crop(DefiniereBereich_AntwortB)
AntwortB_SavePath = userpath + "\\cs_antwortb.png"
QuizmasterAntwortBArea.save(AntwortB_SavePath)
AntwortBText = pytesseract.image_to_string(Image.open(AntwortB_SavePath),lang="deu")
if not AntwortBText: #Wenn AntwortBText keinen Wert hat, handelt es sich evtl um einen einzelnen Buchstaben / Charakter. In dem Fall Config aktivieren
   AntwortBText = pytesseract.image_to_string(Image.open(AntwortB_SavePath),lang="deu",config='--psm 6')

DefiniereBereich_AntwortC = (833, 879, 1422, 969) #defines the area of Answer C
QuizmasterAntwortCArea = im.crop(DefiniereBereich_AntwortC)
AntwortC_SavePath = userpath + "\\cs_antwortc.png"
QuizmasterAntwortCArea.save(AntwortC_SavePath)
AntwortCText = pytesseract.image_to_string(Image.open(AntwortC_SavePath),lang="deu")
if not AntwortCText: #Wenn AntwortCText keinen Wert hat, handelt es sich evtl um einen einzelnen Buchstaben / Charakter. In dem Fall Config aktivieren
   AntwortCText = pytesseract.image_to_string(Image.open(AntwortC_SavePath),lang="deu",config='--psm 6')

DefiniereBereich_Frage = (789, 287, 1467, 495) #definiere Bereich der Frage
QuizmasterArea_Frage = im.crop(DefiniereBereich_Frage) #entnehme aus dem Originalbild nur den definierten Bereich
Frage_SavePath = userpath + "\\cs_frage.png" #speicherort und name für die Frage
QuizmasterArea_Frage.save(Frage_SavePath) #Befehl zum Speichern der Datei
FrageText = pytesseract.image_to_string(Image.open(userpath + "\\cs_frage.png"),lang="deu") #Befehl der das Bild in Text verwandelt (Bild wird geöffnet (Angabe des Pfades), Sprachpaket / Trainingsdaten für pytesseract = arial)
FrageText = FrageText.replace('\n', ' ') # Ersetzt den Zeichenumbruch mit einem Leerzeichen für optimierte Suche

FrageTextReduziert = FrageText.lower() #setzt die frage auf kleinbuchstaben
zuEntfernendeWoerter = ['lautet','mit','den','eines','an','dem','auch','...?','wie','gibt','es','folgend','folgende','folgendes','folgenden','war','was','versteht','verstehen','man','unter','stehen','viele','bietet','eine','einen','ein','aus','auf','in','von','welcher','welches','welchen','welchem','der','die','das','des','dessen','kennt','man','wer','wie','was','wessen','ist','hat','fand','noch','nie','statt','erhielt','für','seine','seinen','ihre','ihren','zu','genau','?','..','...','heißt','hieß','heisst','heissen','heißen','geht','ging','gehen','zurück','und','einst','brachen','gerne','sieht','sehen']
FrageTextReduziert = ' '.join(i for i in FrageTextReduziert.split() if i not in zuEntfernendeWoerter)
FrageTextReduziert = FrageTextReduziert.replace("?", "") #Entfernt das Fragezeichen



#öffne gefundenen Text als Google-Suchergebnis
new=2;
google = "https://www.google.de/search?q="
anzahlSuchergebnisse = '30'

urlA=google+AntwortAText;
urlB=google+AntwortBText;
urlC=google+AntwortCText;
urlF=google+FrageTextReduziert+'&num='+anzahlSuchergebnisse;

pyperclip.copy(FrageTextReduziert) #Kopiert Frage in die Zwischenablage

#Vollständiges HTML RESULT
r = requests.get(urlF) #get FRAGE URL
resultText = r.text

#Entferne HEAD - übrig bleibt BODY
resultbodyCut = resultText.split('</head>') #entfernt head bereich
resultbody = resultbodyCut[1] #enthält nur noch HTML Resultr von <body> bis </body>

# REGEX -------------------------- 
regexStyle = r"<style\b[^>]*>(.*?)</style>" #regex <style> tags
regexScript = r"<script\b[^>]*>(.*?)</script>" #regex <script> tags
test_str = resultbody
subst = ""
regexedRemoveStyle = re.sub(regexStyle, subst, test_str, 0) #entfernt style inhalte
regexedRemoveScript = re.sub(regexScript, subst, test_str, 0) #entfernt script inhalte
# -------------------------- REGEX

# CLEAN HTML TAGS --------------------
htmlCleanedResult = cleanhtml(regexedRemoveScript)
# -------------------- CLEAN HTML TAGS 

# Satzzeichen CLEARING --------------------
keineSatzzeichenResult = re.sub(r'[^\w\s]','',htmlCleanedResult)
# -------------------- Satzzeichen CLEARING


# Entferne GOOGLE HEADER -------------
resultRemoveGoogleHeader = keineSatzzeichenResult.split('ErgebnisseWortwörtlichUngefähr') 
cleanedResult = resultRemoveGoogleHeader[1] 
# ------------- Entferne GOOGLE HEADER

ergebnisliste = cleanedResult.split() #splitte ergebnise in eine wörterliste
print (FrageText+'\n') #Ausgabe der Frage

if debugResult == '1':
   print(cleanedResult)
   print(AntwortAText)
   print(AntwortBText)
   print(AntwortCText)

#REAC print ('======== Antwort A ========')

# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
   
Asplit = AntwortAText.split() # splitte antwort A | zB von "Die Alten Ägypter" in ['Die', 'Alten', 'Ägypter']

#INTERESSANT: if AntwortAText in r.text: #Suche nach exakter Antwort und prüfe auf Treffer (if "Die Alten Ägypter" in list)
   #print (AntwortAText)
   
zsmgAntwortA = ['zsmgAntwortA: '] #zusammengesetzteAntwort A
mostcommonA = [] #mostCommon A
prozentualeUebereinstimmungA = 0
ratioProzentA = 0
mratioA = 0
ergebnisAnzahlA = 0 #Addiert ALLE Ergebnisse die gefunden wurden zusammen (zB "Die Alten Ägypter" - 3x Die 10x Alten 15x Ägypten = 28 Ergebnisse die übereinstimmen)
exakteTreffer_ListA = []
exakteTreffer_ListB = []
exakteTreffer_ListC = []
ungefaehreTreffer_A = 0
ungefaehreTreffer_B = 0
ungefaehreTreffer_C = 0
ungefaehreTreffer_ListA = []
ungefaehreTreffer_ListB = []
ungefaehreTreffer_ListC = []

# EXAKTE Treffer -----------------------------------
if AntwortAText in cleanedResult:
   #exakteTreffer_A = cleanedResult.count(AntwortAText)
   for x in ergebnisliste:
      if x == AntwortAText:
         exakteTreffer_ListA.append(x)

#.lower()

#testA = sum(1 for match in re.finditer(r"\b{}\b", contents))

#print(cleanedResult)
# ----------------------------------- EXAKTE Treffer

for x in Asplit: #iteriere über das Array Asplit (gesplittete Antwort) (zB for Die.... | for Alten.... | for Ägypter...)
    ratiosAddiertA = 0 #addiere alle Ratios der Ergebnisse (zB wenn 3 ergebnisse zu 100% übereinstimmen: 3.0 | wenn 3 ergebnisse zu 50% übereinstimmen: 1.5)
    if x in cleanedResult:
       ungefaehreTreffer_ListA.append(x)

    ungefaehreTreffer_A = len(ungefaehreTreffer_ListA)

    if ungefaehreTreffer_A<20:
       b = difflib.get_close_matches(x, ergebnisliste, 10) #Ausgabe von bis zu 10 ähnlichen Ergebnissen
   # ENTFERNE AUS WÖRTER ARRAY dieser ANTWORT den Inhalt ANDERER ANTWORTEN (zB 1953 (AntwortB) aus A entfernen, wenn Antwort A 1954 ist)
       if len(Asplit)==1: #Wenn die Antwort nur ein Wort hat, dann fahre fort, WICHTIG, da es bei mehreren Wörtern sonst zu problemen kommen kann
          while AntwortBText in b:
             b.remove(AntwortBText) #entferne AntwortB aus dem Array von AntwortA
             #print ('DEBUG in A>B entfernt')
          while AntwortCText in b:
             b.remove(AntwortCText) #entferne AntwortB aus dem Array von AntwortA
          #print ('DEBUG in A>C entfernt')

       ergebnisAnzahlA += len(b)
       for y in b:
          m = SequenceMatcher(None, y, x) # Vergleiche Inhalte der list b (also y) mit dem aktuellen gesplitteten wort der Asplit list (also x).
          mratioA = m.ratio()
          if mratioA > mratioDifferenceFloat:
             ratiosAddiertA += m.ratio()
       if len(b):
          ratioProzentA = (ratiosAddiertA / len(b)) * 100 #Berechne Prozentuale Übereinstimmung
       else: #Ansonsten gebe diesem Ergebnis nur eine sehr geringe Wertung: 0%
          ratioProzentA = 0 
    prozentualeUebereinstimmungA += ratioProzentA
    zsmgAntwortA += difflib.get_close_matches(x, ergebnisliste, 1) # Setze Wörter von A zusammen
    #print (f'{b}\n') #Array Ausgabe wie ['Shanghai', 'Shanghai', 'Shanghai', 'Shanghai', 'Shanghai', 'Shanghai.', 'Shanghai,']
    nAD = nummernAusgeschriebenDictionary.get(x) #wandelt Zahlen in Wörter um (zB "8" zu "acht")
    if nAD: #wenn nummernAusgeschriebenDictionary.get(x) existiert
        numericAusgeschrieben = difflib.get_close_matches(nAD, ergebnisliste, 6) #ähnliche ergebnisse zu der ausgeschriebenen Zahl (zB statt "8" sucht er nun nach "acht")
        print (numericAusgeschrieben) #Ausgabe der gefundenen Ergebnisse

prozentualeUebereinstimmungA = round(prozentualeUebereinstimmungA / len(Asplit),2) #berechne durchschnittliche Wahrscheinlichkeit in Abhängigkeit zu den vorhandenen Wörtern (Asplit)
prozentualeUebereinstimmungA = (prozentualeUebereinstimmungA * 0.8) + ergebnisAnzahlA #DEBUG / TEST
wahrscheinlichkeitenDictionary['A'] = prozentualeUebereinstimmungA
#REAC print (f'\nErgebnisse: {ergebnisAnzahlA}') #A
#REAC print (f'Wahrscheinlichkeit: {prozentualeUebereinstimmungA}') #A

#REAC print ('\n\n======== Antwort B ========')

# BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB

Bsplit = AntwortBText.split() # splitte antwort B

#if AntwortBText in r.text: #Suche nach exakter Antwort und prüfe auf Treffer (if "Die Alten Ägypter" in list)

zsmgAntwortB = ['zsmgAntwortB: '] #zusammengesetzteAntwort B
mostcommonB = [] #mostCommon B
prozentualeUebereinstimmungB = 0
ratioProzentB = 0
mratioB = 0
ergebnisAnzahlB = 0 #Addiert ALLE Ergebnisse die gefunden wurden zusammen (zB "Die Alten Ägypter" - 3x Die 10x Alten 15x Ägypten = 28 Ergebnisse die übereinstimmen)

# EXAKTE Treffer -----------------------------------
if AntwortBText in cleanedResult:
   for x in ergebnisliste:
      if x == AntwortBText:
         exakteTreffer_ListB.append(x)
# ----------------------------------- EXAKTE Treffer

for x in Bsplit:
    ratiosAddiertB = 0
    if x in cleanedResult:
       ungefaehreTreffer_ListB.append(x)

    ungefaehreTreffer_B = len(ungefaehreTreffer_ListB)

    if ungefaehreTreffer_B<20:  # wird nur ausgeführt, wenn exakte treffer zu gering sind
       b = difflib.get_close_matches(x, ergebnisliste, 10)
      # ENTFERNE AUS WÖRTER ARRAY dieser ANTWORT den Inhalt ANDERER ANTWORTEN (zB 1953 (AntwortB) aus A entfernen, wenn Antwort A 1954 ist)
       if len(Bsplit)==1: #Wenn die Antwort nur ein Wort hat, dann fahre fort, WICHTIG, da es bei mehreren Wörtern sonst zu problemen kommen kann
          while AntwortAText in b:
             b.remove(AntwortAText)
             #print ('DEBUG in B>A entfernt')
          while AntwortCText in b:
             b.remove(AntwortCText)
             #print ('DEBUG in B>C entfernt')
    
       ergebnisAnzahlB += len(b)
       for y in b:
          m = SequenceMatcher(None, y, x) # Vergleiche Inhalte der list b (also y) mit dem aktuellen gesplitteten wort der Asplit list (also x).
          mratioB = m.ratio()
          if mratioB > mratioDifferenceFloat:
             ratiosAddiertB += m.ratio()
       if len(b):
          ratioProzentB = (ratiosAddiertB / len(b)) * 100 #Berechne Prozentuale Übereinstimmung
       else: #Ansonsten gebe diesem Ergebnis nur eine sehr geringe Wertung: 0%
          ratioProzentB = 0 
    prozentualeUebereinstimmungB += ratioProzentB
    zsmgAntwortB += difflib.get_close_matches(x, ergebnisliste, 1) # Setze Wörter von B zusammen
    #print (f'{b}\n')
    nAD = nummernAusgeschriebenDictionary.get(x) #
    if nAD: #wenn nummernAusgeschriebenDictionary.get(x) existiert
        numericAusgeschrieben = difflib.get_close_matches(nAD, ergebnisliste, 6) #ähnliche ergebnisse zu der ausgeschriebenen Zahl (zB statt "8" sucht er nun nach "acht")
        print (numericAusgeschrieben) #Ausgabe der gefundenen Ergebnisse

prozentualeUebereinstimmungB = round(prozentualeUebereinstimmungB / len(Bsplit),2) #berechne durchschnittliche Wahrscheinlichkeit in Abhängigkeit zu den vorhandenen Wörtern (Asplit)
prozentualeUebereinstimmungB = (prozentualeUebereinstimmungB * 0.8) + ergebnisAnzahlB
wahrscheinlichkeitenDictionary['B'] = prozentualeUebereinstimmungB
#REAC print (f'\nErgebnisse: {ergebnisAnzahlB}') #B
#REAC print (f'Wahrscheinlichkeit: {prozentualeUebereinstimmungB}') #B

#REAC print ('\n\n======== Antwort C ========')

# CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

Csplit = AntwortCText.split() # splitte antwort C

#if AntwortCText in r.text: #Suche nach exakter Antwort und prüfe auf Treffer (if "Die Alten Ägypter" in list)

zsmgAntwortC = ['zsmgAntwortC: '] #zusammengesetzteAntwort C
mostcommonC = [] #mostCommon C
prozentualeUebereinstimmungC = 0
ratioProzentC = 0
mratioC = 0
ergebnisAnzahlC = 0 #Addiert ALLE Ergebnisse die gefunden wurden zusammen (zB "Die Alten Ägypter" - 3x Die 10x Alten 15x Ägypten = 28 Ergebnisse die übereinstimmen)


# EXAKTE Treffer -----------------------------------
if AntwortCText in cleanedResult:
   #exakteTreffer_C = cleanedResult.count(AntwortCText)
   for x in ergebnisliste:
      if x == AntwortCText:
         exakteTreffer_ListC.append(x)   
# ----------------------------------- EXAKTE Treffer

for x in Csplit:
    ratiosAddiertC = 0
    if x in cleanedResult:
       ungefaehreTreffer_ListC.append(x)

    ungefaehreTreffer_C = len(ungefaehreTreffer_ListC)
    
    if ungefaehreTreffer_C<20:
       b = difflib.get_close_matches(x, ergebnisliste, 10)
       # ENTFERNE AUS WÖRTER ARRAY dieser ANTWORT den Inhalt ANDERER ANTWORTEN (zB 1953 (AntwortB) aus A entfernen, wenn Antwort A 1954 ist)
       if len(Csplit)==1: #Wenn die Antwort nur ein Wort hat, dann fahre fort, WICHTIG, da es bei mehreren Wörtern sonst zu problemen kommen kann
          while AntwortAText in b:
             b.remove(AntwortAText)
             #print ('DEBUG in C>A entfernt')
          while AntwortBText in b:
             b.remove(AntwortBText)
             #print ('DEBUG in C>B entfernt')
    
       ergebnisAnzahlC += len(b)
       for y in b:
          m = SequenceMatcher(None, y, x) # Vergleiche Inhalte der list b (also y) mit dem aktuellen gesplitteten wort der Asplit list (also x).
          mratioC = m.ratio()
          if mratioC > mratioDifferenceFloat:
             ratiosAddiertC += m.ratio()
       if len(b): #führe folgende Berechnung nur aus wenn lenB überhaupt existiert
          ratioProzentC = (ratiosAddiertC / len(b)) * 100 #Berechne Prozentuale Übereinstimmung
       else: #Ansonsten gebe diesem Ergebnis nur eine sehr geringe Wertung: 0%
          ratioProzentC = 0 
    prozentualeUebereinstimmungC += ratioProzentC
    zsmgAntwortC += difflib.get_close_matches(x, ergebnisliste, 1) # Setze Wörter von C zusammen
    #print (f'{b}')
    nAD = nummernAusgeschriebenDictionary.get(x) #
    if nAD: #wenn nummernAusgeschriebenDictionary.get(x) existiert
        numericAusgeschrieben = difflib.get_close_matches(nAD, ergebnisliste, 6) #ähnliche ergebnisse zu der ausgeschriebenen Zahl (zB statt "8" sucht er nun nach "acht")
        print (numericAusgeschrieben) #Ausgabe der gefundenen Ergebnisse

prozentualeUebereinstimmungC = round(prozentualeUebereinstimmungC / len(Csplit),2) #berechne durchschnittliche Wahrscheinlichkeit in Abhängigkeit zu den vorhandenen Wörtern (Asplit)
prozentualeUebereinstimmungC = (prozentualeUebereinstimmungC * 0.8) + ergebnisAnzahlC
wahrscheinlichkeitenDictionary['C'] = prozentualeUebereinstimmungC
#REAC print (f'\nErgebnisse: {ergebnisAnzahlC}') #C
#REAC print (f'Wahrscheinlichkeit: {prozentualeUebereinstimmungC}') #C

#REAC print (f'\n--------------------------------')



exakteTreffer_A = len(exakteTreffer_ListA) 
exakteTreffer_B = len(exakteTreffer_ListB) 
exakteTreffer_C = len(exakteTreffer_ListC) 


if exakteTreffer_A>0:
   print (f'\n A - EXAKTE TREFFER | {AntwortAText}:  {exakteTreffer_A}x  ||  {exakteTreffer_ListA[:5]}')

if exakteTreffer_B>0:
   print (f'\n B - EXAKTE TREFFER | {AntwortBText}:  {exakteTreffer_B}x  ||  {exakteTreffer_ListB[:5]}')
   
if exakteTreffer_C>0:
   print (f'\n C - EXAKTE TREFFER | {AntwortCText}:  {exakteTreffer_C}x  ||  {exakteTreffer_ListC[:5]}')


if ((exakteTreffer_A == 0) and (exakteTreffer_B == 0) and (exakteTreffer_C == 0)):
   if ungefaehreTreffer_A>0:
      print (f'\n A - ungefaher | {Asplit}:  {ungefaehreTreffer_A}x  ||  {ungefaehreTreffer_ListA[:5]}')

   if ungefaehreTreffer_B>0:
      print (f'\n B - ungefaher | {Bsplit}:  {ungefaehreTreffer_B}x  ||  {ungefaehreTreffer_ListB[:5]}')

   if ungefaehreTreffer_C>0:
      print (f'\n C - ungefaher | {Csplit}:  {ungefaehreTreffer_C}x  ||  {ungefaehreTreffer_ListC[:5]}')
      

if "nicht" in FrageText: #Abfrage ob Frage negiert wird
   print (f'\nACHTUNG: Das Wort "nicht" wurde gefunden - GGF JOKER VERWENDEN')

if "kein" in FrageText: #Abfrage ob Frage negiert wird
   print (f'\nACHTUNG: Das Wort "kein" wurde gefunden - GGF JOKER VERWENDEN')

AntwortenWahrscheinlichkeitSortiert = sorted(wahrscheinlichkeitenDictionary, key=wahrscheinlichkeitenDictionary.get, reverse=True) #sortiert die Wahrscheinlichkeiten der Antworten absteigend; ex: "90, 80, 60"
AntwortenWahrscheinlichkeitAlleWerteEntsprechenNull = True 
for x in wahrscheinlichkeitenDictionary:
   if wahrscheinlichkeitenDictionary[x] != 0.0:
      AntwortenWahrscheinlichkeitAlleWerteEntsprechenNull = False

#LÖSCHEN?
#if AntwortenWahrscheinlichkeitAlleWerteEntsprechenNull == False: #Wenn es Wahrscheinlichkeiten gibt
   #debug = 1
   #print (f'\nHöchste Wahrscheinlichkeit: {AntwortenWahrscheinlichkeitSortiert}')
#else: #Wenn es keine Wahrscheinlichkeiten gibt (alle == 0)
   #print (f'\nALLE WAHRSCHEINLICHKEITEN SIND 0%')

# Öffne Webbrowser als TAB: die Antwortmöglichkeiten und die Frage
#webbrowser.open(urlA,new);
#webbrowser.open(urlB,new);
#webbrowser.open(urlC,new);
webbrowser.open(urlF,new);

if zeitmessungAktiv == 1:
   end = time.time()
   print(end - start)
