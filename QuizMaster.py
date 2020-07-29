#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO deutschen code refactored => into english

zeitmessungAktiv = 0 #0 für aus, 1 für an. Zeitmessung bestimmt die Laufzeit des Skripts

if zeitmessungAktiv == 1:
   import time
   start = time.time()


# import third party modules

import pyperclip #usedto save Var result into clipboard
import pytesseract
import webbrowser
import PIL.ImageGrab
from PIL import Image, ImageEnhance, ImageFilter
import requests
from difflib import SequenceMatcher
import difflib
import string
import pathlib
import os.path
import re #regex

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# initialize Config Vars (you can configure these in via the config.ini)
devmode = config['CONFIG']['devmode'] #dev mode uses the "example.png"-file or any ohter file that you configured
debugResult = config['CONFIG']['logging'] #If debugResult = 1 > enables debugging of the result
ImageSubdirectory = config['CONFIG']['ImageSubdirectory'] # subdirectory where the single images for the question and the answers will be saved
mratioDifferenceFloat = float( config['CONFIG']['mratioDifferenceFloat'] ); #float-value to define the ratio of likeness between the "real answer" and the found results by the script.
# for example: if you compare "Egg" to "Egg" a ratio of 1.0 would lead to the exact result, but that is a very unrealistic case. especially if you get results that uses the plural ("Eggs") you need a lower ratio than 1.0.
# a good value in my tests were 0.6 - 0.7

Question_UpperLeftCornerX = int ( config['LAYOUT']['Question_UpperLeftCornerX'] )
Question_UpperLeftCornerY = int ( config['LAYOUT']['Question_UpperLeftCornerY'] )
Question_LowerRightCornerX = int ( config['LAYOUT']['Question_LowerRightCornerX'] )
Question_LowerRightCornerY = int ( config['LAYOUT']['Question_LowerRightCornerY'] )

AnswerA_UpperLeftCornerX = int ( config['LAYOUT']['AnswerA_UpperLeftCornerX'] )
AnswerA_UpperLeftCornerY = int ( config['LAYOUT']['AnswerA_UpperLeftCornerY'] )
AnswerA_LowerRightCornerX = int ( config['LAYOUT']['AnswerA_LowerRightCornerX'] )
AnswerA_LowerRightCornerY = int ( config['LAYOUT']['AnswerA_LowerRightCornerY'] )

AnswerB_UpperLeftCornerX = int ( config['LAYOUT']['AnswerB_UpperLeftCornerX'] )
AnswerB_UpperLeftCornerY = int ( config['LAYOUT']['AnswerB_UpperLeftCornerY'] )
AnswerB_LowerRightCornerX = int ( config['LAYOUT']['AnswerB_LowerRightCornerX'] )
AnswerB_LowerRightCornerY = int ( config['LAYOUT']['AnswerB_LowerRightCornerY'] )

AnswerC_UpperLeftCornerX = int ( config['LAYOUT']['AnswerC_UpperLeftCornerX'] )
AnswerC_UpperLeftCornerY = int ( config['LAYOUT']['AnswerC_UpperLeftCornerY'] )
AnswerC_LowerRightCornerX = int ( config['LAYOUT']['AnswerC_LowerRightCornerX'] )
AnswerC_LowerRightCornerY = int ( config['LAYOUT']['AnswerC_LowerRightCornerY'] )


currentWorkingDir = pathlib.Path().absolute()


# import own modules
import AnswerFunctions


# F U N C T I O N S ------------------------------------------------------------

#function cleanhtml - erases html tags from the result
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

snapshot = PIL.ImageGrab.grab() #used to create a screenshot


userpath = os.path.join(currentWorkingDir, ImageSubdirectory)

im = Image.open(userpath + "\\devmode-testfile.png") #only used in DEV mode

if devmode != '1': #only creates a screenshot if devmode = false
   save_path = userpath + "\\cash.png"
   snapshot.save(save_path)
   im = Image.open(userpath + "\\cash.png")
else:
   print ('DEVMODE ---- DEVMODE')


# initialize V A R I A B L E S -------------------------------------------------
   
wahrscheinlichkeitenDictionary = {}


#NAD = nummernAusgeschriebenDictionary
#a list that contains the numbers and also the words in a range from 0-20. it is used for the results, because lower value numbers are often written as words.
nummernAusgeschriebenDictionary = {"0":"null","1":"eins","2":"zwei","3":"drei","4":"vier","5":"fünf","6":"sechs","7":"sieben","8":"acht","9":"neun","10":"zehn","11":"elf","12":"zwölf","13":"dreizehn","14":"vierzehn","15":"fünfzehn","16":"sechszehn","17":"siebzehn","18":"achtzehn","19":"neunzehn","20":"zwangzig"}

DefiniereBereich_AntwortA = (AnswerA_UpperLeftCornerX, AnswerA_UpperLeftCornerY, AnswerA_LowerRightCornerX, AnswerA_LowerRightCornerY) #defines the area of Answer A
QuizmasterAntwortAArea = im.crop(DefiniereBereich_AntwortA) #slices the screenshot into the defined area for the answer A
AntwortA_SavePath = userpath + "\\cs_antworta.png"
QuizmasterAntwortAArea.save(AntwortA_SavePath)
AntwortAText = pytesseract.image_to_string(Image.open(AntwortA_SavePath),lang="deu") #config='-psm 5'
if not AntwortAText: #If AntwortAText does not have a value, it the answer may be a single character or letter only. In this case, activate the config to detect a single character
   AntwortAText = pytesseract.image_to_string(Image.open(AntwortA_SavePath),lang="deu",config='--psm 6')
    
DefiniereBereich_AntwortB = (834, 737, 1423, 824) #defines the area of Answer B
QuizmasterAntwortBArea = im.crop(DefiniereBereich_AntwortB) #slices the screenshot into the defined area for the answer B
AntwortB_SavePath = userpath + "\\cs_antwortb.png"
QuizmasterAntwortBArea.save(AntwortB_SavePath)
AntwortBText = pytesseract.image_to_string(Image.open(AntwortB_SavePath),lang="deu")
if not AntwortBText: #If AntwortBText does not have a value, it the answer may be a single character or letter only. In this case, activate the config to detect a single 
   AntwortBText = pytesseract.image_to_string(Image.open(AntwortB_SavePath),lang="deu",config='--psm 6')

DefiniereBereich_AntwortC = (834, 879, 1423, 969) #defines the area of Answer C
QuizmasterAntwortCArea = im.crop(DefiniereBereich_AntwortC) #slices the screenshot into the defined area for the answer C
AntwortC_SavePath = userpath + "\\cs_antwortc.png"
QuizmasterAntwortCArea.save(AntwortC_SavePath)
AntwortCText = pytesseract.image_to_string(Image.open(AntwortC_SavePath),lang="deu")
if not AntwortCText: #If AntwortCText does not have a value, it the answer may be a single character or letter only. In this case, activate the config to detect a single 
   AntwortCText = pytesseract.image_to_string(Image.open(AntwortC_SavePath),lang="deu",config='--psm 6')

DefiniereBereich_Frage = (789, 287, 1467, 495) #defines the question-area
QuizmasterArea_Frage = im.crop(DefiniereBereich_Frage) #slices the screenshot into the defined area for the question
Frage_SavePath = userpath + "\\cs_frage.png" #speicherort und name für die Frage
QuizmasterArea_Frage.save(Frage_SavePath) #Befehl zum Speichern der Datei
FrageText = pytesseract.image_to_string(Image.open(userpath + "\\cs_frage.png"),lang="deu") #command that converts the image into strings (it opens the image (that is located at the specified path), language packs / trained data for pytesseract))
FrageText = FrageText.replace('\n', ' ') # replaces the line break (\n) with a space for an optimized search

FrageTextReduziert = FrageText.lower() #sets all text content to lowercase characters
zuEntfernendeWoerter = ['lautet','mit','den','eines','an','dem','auch','...?','wie','gibt','es','folgend','folgende','folgendes','folgenden','war','was','versteht','verstehen','man','unter','stehen','viele','bietet','eine','einen','ein','aus','auf','in','von','welcher','welches','welchen','welchem','der','die','das','des','dessen','kennt','man','wer','wie','was','wessen','ist','hat','fand','noch','nie','statt','erhielt','für','seine','seinen','ihre','ihren','zu','genau','?','..','...','heißt','hieß','heisst','heissen','heißen','geht','ging','gehen','zurück','und','einst','brachen','gerne','sieht','sehen']
FrageTextReduziert = ' '.join(i for i in FrageTextReduziert.split() if i not in zuEntfernendeWoerter)
FrageTextReduziert = FrageTextReduziert.replace("?", "") #removes the Questionmark (?) from the question text


#opens the browser with the detected text as a google-search query
new=2;
google = "https://www.google.de/search?q="
anzahlSuchergebnisse = '30'

urlA=google+AntwortAText;
urlB=google+AntwortBText;
urlC=google+AntwortCText;
urlF=google+FrageTextReduziert+'&num='+anzahlSuchergebnisse;

pyperclip.copy(FrageTextReduziert) #copies the question text into the clipboard

#complete HTML result
r = requests.get(urlF) #get question URL
resultText = r.text

#removes the Html head -> only the body-content remains
resultbodyCut = resultText.split('</head>') #remove the head content
resultbody = resultbodyCut[1] #only contains the HTML content from <body> until the end

# REGEX -------------------------- 
regexStyle = r"<style\b[^>]*>(.*?)</style>" #regex <style> tags
regexScript = r"<script\b[^>]*>(.*?)</script>" #regex <script> tags
test_str = resultbody
subst = ""
regexedRemoveStyle = re.sub(regexStyle, subst, test_str, 0) #removes style content
regexedRemoveScript = re.sub(regexScript, subst, test_str, 0) #removes script content
# -------------------------- REGEX

# CLEAN HTML TAGS --------------------
htmlCleanedResult = cleanhtml(regexedRemoveScript)
# -------------------- CLEAN HTML TAGS 

# punctuation mark CLEARING --------------------
keineSatzzeichenResult = re.sub(r'[^\w\s]','',htmlCleanedResult)
# -------------------- punctuation mark CLEARING


# removes GOOGLE HEADER -------------
resultRemoveGoogleHeader = keineSatzzeichenResult.split('ErgebnisseWortwörtlichUngefähr') 
cleanedResult = resultRemoveGoogleHeader[0] 
# ------------- removes GOOGLE HEADER

ergebnisliste = cleanedResult.split() #splits multiple results into a word-list
print (FrageText+'\n') #print the question

#prints the answer
if debugResult == '1':
   print(cleanedResult)
   print(AntwortAText)
   print(AntwortBText)
   print(AntwortCText)

# get list of exact matches for A, B and C
exakteTreffer_ListA, ungefaehreTreffer_A = AnswerFunctions.answerA(AntwortAText, AntwortBText, AntwortCText, cleanedResult, ergebnisliste, mratioDifferenceFloat, nummernAusgeschriebenDictionary, wahrscheinlichkeitenDictionary)
exakteTreffer_ListB, ungefaehreTreffer_B = AnswerFunctions.answerB(AntwortAText, AntwortBText, AntwortCText, cleanedResult, ergebnisliste, mratioDifferenceFloat, nummernAusgeschriebenDictionary, wahrscheinlichkeitenDictionary)
exakteTreffer_ListC, ungefaehreTreffer_C = AnswerFunctions.answerC(AntwortAText, AntwortBText, AntwortCText, cleanedResult, ergebnisliste, mratioDifferenceFloat, nummernAusgeschriebenDictionary, wahrscheinlichkeitenDictionary)

# get amount of exact matches for A, B and C
exakteTreffer_A = len(exakteTreffer_ListA) 
exakteTreffer_B = len(exakteTreffer_ListB) 
exakteTreffer_C = len(exakteTreffer_ListC) 


if exakteTreffer_A>0:
   print ('\n A - EXAKTE TREFFER | {AntwortAText}:  {exakteTreffer_A}x  ||  {exakteTreffer_ListA[:5]}')

if exakteTreffer_B>0:
   print ('\n B - EXAKTE TREFFER | {AntwortBText}:  {exakteTreffer_B}x  ||  {exakteTreffer_ListB[:5]}')
   
if exakteTreffer_C>0:
   print ('\n C - EXAKTE TREFFER | {AntwortCText}:  {exakteTreffer_C}x  ||  {exakteTreffer_ListC[:5]}')


if ((exakteTreffer_A == 0) and (exakteTreffer_B == 0) and (exakteTreffer_C == 0)):
   if ungefaehreTreffer_A>0:
      print ('\n A - ungefaher | {Asplit}:  {ungefaehreTreffer_A}x  ||  {ungefaehreTreffer_ListA[:5]}')

   if ungefaehreTreffer_B>0:
      print ('\n B - ungefaher | {Bsplit}:  {ungefaehreTreffer_B}x  ||  {ungefaehreTreffer_ListB[:5]}')

   if ungefaehreTreffer_C>0:
      print ('\n C - ungefaher | {Csplit}:  {ungefaehreTreffer_C}x  ||  {ungefaehreTreffer_ListC[:5]}')
      

if "nicht" in FrageText: #Abfrage ob Frage negiert wird
   print ('\nACHTUNG: Das Wort "nicht" wurde gefunden - GGF JOKER VERWENDEN')

if "kein" in FrageText: #Abfrage ob Frage negiert wird
   print ('\nACHTUNG: Das Wort "kein" wurde gefunden - GGF JOKER VERWENDEN')

if "no" in FrageText: #Condition: Question was negated
   print ('\nWARNING: The Question contains the Word "no" - Result may be irritating ')

if "not" in FrageText: #Condition: Question was negated
   print ('\nWARNING: The Question contains the Word "not" - Result may be irritating ')
   

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

# open a browser tab: question and answer (if uncommented)
#webbrowser.open(urlA,new);
#webbrowser.open(urlB,new);
#webbrowser.open(urlC,new);
webbrowser.open(urlF,new);

if zeitmessungAktiv == 1:
   end = time.time()
   print(end - start)
