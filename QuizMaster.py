#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO deutschen code refactored => into english

# import third party modules
import time
import pyperclip  # used to save Var result into clipboard
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
import re  # regex
import configparser

# import own modules
import AnswerFunctions

config = configparser.ConfigParser()
config.read('config.ini')

activateRunTimeMeasurement = 0  # 0 = OFF, 1 = ON, prints the RunTime
if activateRunTimeMeasurement == 1:
    start = time.time()

# initialize Config Vars (you can configure these in via the config.ini)
devmode = config['CONFIG']['devmode']  # dev mode uses the "example.png"-file or any ohter file that you configured
debugResult = config['CONFIG']['logging']  # If debugResult = 1 > enables debugging of the result
ImageSubdirectory = config['CONFIG']['ImageSubdirectory']  # subdirectory where the cropped images will be saved
mratioDifferenceFloat = float(config['CONFIG']['mratioDifferenceFloat'])
#  float-value to define the ratio of likeness between the "real answer" and the found results by the script.
#  example: if you compare "Egg" to "Egg" a ratio of 1.0 would lead to the exact result, but that is unrealistic,
#  especially if you get results that uses the plural ("Eggs") you need a lower ratio than 1.0.
#  a good value in my tests were 0.6 - 0.7

Question_UpperLeftCornerX = int(config['LAYOUT']['Question_UpperLeftCornerX'])
Question_UpperLeftCornerY = int(config['LAYOUT']['Question_UpperLeftCornerY'])
Question_LowerRightCornerX = int(config['LAYOUT']['Question_LowerRightCornerX'])
Question_LowerRightCornerY = int(config['LAYOUT']['Question_LowerRightCornerY'])

AnswerA_UpperLeftCornerX = int(config['LAYOUT']['AnswerA_UpperLeftCornerX'])
AnswerA_UpperLeftCornerY = int(config['LAYOUT']['AnswerA_UpperLeftCornerY'])
AnswerA_LowerRightCornerX = int(config['LAYOUT']['AnswerA_LowerRightCornerX'])
AnswerA_LowerRightCornerY = int(config['LAYOUT']['AnswerA_LowerRightCornerY'])

AnswerB_UpperLeftCornerX = int(config['LAYOUT']['AnswerB_UpperLeftCornerX'])
AnswerB_UpperLeftCornerY = int(config['LAYOUT']['AnswerB_UpperLeftCornerY'])
AnswerB_LowerRightCornerX = int(config['LAYOUT']['AnswerB_LowerRightCornerX'])
AnswerB_LowerRightCornerY = int(config['LAYOUT']['AnswerB_LowerRightCornerY'])

AnswerC_UpperLeftCornerX = int(config['LAYOUT']['AnswerC_UpperLeftCornerX'])
AnswerC_UpperLeftCornerY = int(config['LAYOUT']['AnswerC_UpperLeftCornerY'])
AnswerC_LowerRightCornerX = int(config['LAYOUT']['AnswerC_LowerRightCornerX'])
AnswerC_LowerRightCornerY = int(config['LAYOUT']['AnswerC_LowerRightCornerY'])

currentWorkingDir = pathlib.Path().absolute()


# F U N C T I O N S ------------------------------------------------------------

# function cleanhtml - erases html tags from the result
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


snapshot = PIL.ImageGrab.grab()  # used to create a screenshot

userpath = os.path.join(currentWorkingDir, ImageSubdirectory)

im = Image.open(userpath + "\\devmode-testfile.png")  # only used in DEV mode

if devmode != '1':  # only creates a screenshot if devmode = false
    save_path = userpath + "\\cash.png"
    snapshot.save(save_path)
    im = Image.open(userpath + "\\cash.png")
else:
    print('DEVMODE ---- DEVMODE')


# getAnswerA

# defines the area for the answer (X and Y rectangle coordinates)
# crops the area
# saves the cropped area as an image
# gets the text from the image via pytesseract (OCR)
# returns the text
def getAnswerA():
    defineArea_AnswerA = (AnswerA_UpperLeftCornerX, AnswerA_UpperLeftCornerY, AnswerA_LowerRightCornerX,
                                 AnswerA_LowerRightCornerY)  # defines the area of Answer A
    quizmaster_answerA_area = im.crop(
        defineArea_AnswerA)  # slices the screenshot into the defined area for the answer A
    answerA_savePath = userpath + "\\cs_antworta.png"  # todo rename into ENG
    quizmaster_answerA_area.save(answerA_savePath)
    answerA_text = pytesseract.image_to_string(Image.open(answerA_savePath), lang="deu")  # config='-psm 5' # todo make language configurable via config.ini
    if not answerA_text:  # If answerA_text does not have a value, it the answer may be a single character or letter only. In this case, activate the config to detect a single character
        answerA_text = pytesseract.image_to_string(Image.open(answerA_savePath), lang="deu", config='--psm 6') # todo make language configurable via config.ini
    return answerA_text


# getAnswerB

# defines the area for the answer (X and Y rectangle coordinates)
# crops the area
# saves the cropped area as an image
# gets the text from the image via pytesseract (OCR)
# returns the text
def getAnswerB():
    defineArea_AnswerB = (AnswerB_UpperLeftCornerX, AnswerB_UpperLeftCornerY, AnswerB_LowerRightCornerX,
                                 AnswerB_LowerRightCornerY)  # defines the area of Answer B
    quizmaster_answerB_area = im.crop(defineArea_AnswerB)  # slices the screenshot into the defined area for the answerB
    answerB_savepath = userpath + "\\cs_antwortb.png" # todo rename into ENG
    quizmaster_answerB_area.save(answerB_savepath)
    AnswerB_text = pytesseract.image_to_string(Image.open(answerB_savepath), lang="deu") # todo make language configurable via config.ini
    if not AnswerB_text:  # If AnswerB_text does not have a value, it the answer may be a single character or letter only. In this case, activate the config to detect a single
        AnswerB_text = pytesseract.image_to_string(Image.open(answerB_savepath), lang="deu", config='--psm 6') # todo make language configurable via config.ini
    return AnswerB_text


# getAnswerC

# defines the area for the answer (X and Y rectangle coordinates)
# crops the area
# saves the cropped area as an image
# gets the text from the image via pytesseract (OCR)
# returns the text
def getAnswerC():
    defineArea_AnswerC = (AnswerC_UpperLeftCornerX, AnswerC_UpperLeftCornerY, AnswerC_LowerRightCornerX,
                                 AnswerC_LowerRightCornerY)  # defines the area of Answer C
    quizmaster_answerC_area = im.crop(
        defineArea_AnswerC)  # slices the screenshot into the defined area for the answer C
    answerC_savepath = userpath + "\\cs_antwortc.png" # todo rename into ENG
    quizmaster_answerC_area.save(answerC_savepath)
    answerC_text = pytesseract.image_to_string(Image.open(answerC_savepath), lang="deu") # todo make language configurable via config.ini
    if not answerC_text:  # If answerC_text does not have a value, it the answer may be a single character or letter only. In this case, activate the config to detect a single
        answerC_text = pytesseract.image_to_string(Image.open(answerC_savepath), lang="deu", config='--psm 6') # todo make language configurable via config.ini
    return answerC_text


# getQuestion

# defines the area for the question (X and Y rectangle coordinates)
# crops the area
# saves the cropped area as an image
# gets the text from the image via pytesseract (OCR)
# removes linking words from the question to improve the result accuracy
# returns the question
def getQuestion():
    defineArea_question = (Question_UpperLeftCornerX, Question_UpperLeftCornerY, Question_LowerRightCornerX,
                              Question_LowerRightCornerY)  # defines the question-area
    quizmasterArea_question = im.crop(
        defineArea_question)  # slices the screenshot into the defined area for the question
    question_savepath = userpath + "\\cs_frage.png"  # savepath and filename for the question
    quizmasterArea_question.save(question_savepath)  # saves the file
    questionText = pytesseract.image_to_string(Image.open(userpath + "\\cs_frage.png"),
                                            lang="deu")  # command that converts the image into strings (it opens the image (that is located at the specified path), language packs / trained data for pytesseract))
    questionText = questionText.replace('\n', ' ')  # replaces the line break (\n) with a space for an optimized search
    questionText_reduced = questionText.lower()  # sets all text content to lowercase characters
    wordsToBeRemoved = ['lautet', 'mit', 'den', 'eines', 'an', 'dem', 'auch', '...?', 'wie', 'gibt', 'es',
                            'folgend', 'folgende', 'folgendes', 'folgenden', 'war', 'was', 'versteht', 'verstehen',
                            'man', 'unter', 'stehen', 'viele', 'bietet', 'eine', 'einen', 'ein', 'aus', 'auf', 'in',
                            'von', 'welcher', 'welches', 'welchen', 'welchem', 'der', 'die', 'das', 'des', 'dessen',
                            'kennt', 'man', 'wer', 'wie', 'was', 'wessen', 'ist', 'hat', 'fand', 'noch', 'nie', 'statt',
                            'erhielt', 'für', 'seine', 'seinen', 'ihre', 'ihren', 'zu', 'genau', '?', '..', '...',
                            'heißt', 'hieß', 'heisst', 'heissen', 'heißen', 'geht', 'ging', 'gehen', 'zurück', 'und',
                            'einst', 'brachen', 'gerne', 'sieht', 'sehen']  # todo configurable? english? language-wise?
    questionText_reduced = ' '.join(i for i in questionText_reduced.split() if i not in wordsToBeRemoved)
    questionText_reduced = questionText_reduced.replace("?", "")  # removes the Questionmark (?) from the question text
    return questionText, questionText_reduced


# getResultViaRequest()
# starts a request to a search engine with the content of the question (urlF)
# returns the complete HTML Result body as resultText
def getResultViaRequest():
    r = requests.get(urlF)  # get question URL
    resultText = r.text
    return resultText


# cleanHtmlResult
# cleans the HTML Result by removing unnecessary things, such as:
# html head, html tags, script tags, style tags, punctuation, google header
def cleanHtmlResult():
    # removes the Html head -> only the body-content remains
    resultbodyCut = resultText.split('</head>')  # remove the head content
    resultbody = resultbodyCut[1]  # only contains the HTML content from <body> until the end

    # REGEX --------------------------
    regexStyle = r"<style\b[^>]*>(.*?)</style>"  # regex <style> tags
    regexScript = r"<script\b[^>]*>(.*?)</script>"  # regex <script> tags
    test_str = resultbody
    subst = ""
    regexedRemoveStyle = re.sub(regexStyle, subst, test_str, 0)  # removes style content
    regexedRemoveScript = re.sub(regexScript, subst, test_str, 0)  # removes script content
    # -------------------------- REGEX

    # CLEAN HTML TAGS --------------------
    htmlCleanedResult = cleanhtml(regexedRemoveScript)
    # -------------------- CLEAN HTML TAGS

    # punctuation mark CLEARING --------------------
    result_without_punctuation = re.sub(r'[^\w\s]', '', htmlCleanedResult)
    # -------------------- punctuation mark CLEARING

    # removes GOOGLE HEADER -------------
    resultRemoveGoogleHeader = result_without_punctuation.split('ErgebnisseWortwörtlichUngefähr')  # todo GER words
    cleanedResult = resultRemoveGoogleHeader[0]
    # ------------- removes GOOGLE HEADER

    return cleanedResult


# printEvaluatedResult
# prints the Result depending on the amount of matches (for exact and approximate matches)
# the function will print additional notifications if the question is negated
def printEvaluatedResult():
    if exactMatches_A > 0:
        print(f'\n A - EXAKTE TREFFER | {AnswerAText}:  {exactMatches_A}x  ||  {listA_exactMatches[:5]}')

    if exactMatches_B > 0:
        print(f'\n B - EXAKTE TREFFER | {AnswerBText}:  {exactMatches_B}x  ||  {listB_exactMatches[:5]}')

    if exactMatches_C > 0:
        print(f'\n C - EXAKTE TREFFER | {AnswerCText}:  {exactMatches_C}x  ||  {listC_exactMatches[:5]}')

    if ((exactMatches_A == 0) and (exactMatches_B == 0) and (exactMatches_C == 0)):
        if approximateMatches_A > 0:
            print(f'\n A - ungefähr | {Asplit}:  {approximateMatches_A}x  ||  {listA_approximateMatches[:5]}')

        if approximateMatches_B > 0:
            print(f'\n B - ungefähr | {Bsplit}:  {approximateMatches_B}x  ||  {listB_approximateMatches[:5]}')

        if approximateMatches_C > 0:
            print(f'\n C - ungefähr | {Csplit}:  {approximateMatches_C}x  ||  {listC_approximateMatches[:5]}')

    if "nicht" in QuestionText:  # Abfrage ob Frage negiert wird
        print('\nACHTUNG: Das Wort "nicht" wurde gefunden - GGF JOKER VERWENDEN')

    if "kein" in QuestionText:  # Abfrage ob Frage negiert wird
        print('\nACHTUNG: Das Wort "kein" wurde gefunden - GGF JOKER VERWENDEN')

    if "no" in QuestionText:  # Condition: Question was negated
        print('\nWARNING: The Question contains the Word "no" - Result may be irritating ')

    if "not" in QuestionText:  # Condition: Question was negated
        print('\nWARNING: The Question contains the Word "not" - Result may be irritating ')


# SearchEngineUrls
# defines the URLS for the AnswerA,B,C and the question
def defineSearchEngineUrls():
    urlA = searchEngineUrl + AnswerAText
    urlB = searchEngineUrl + AnswerBText
    urlC = searchEngineUrl + AnswerCText
    urlF = searchEngineUrl + QuestionTextReduced + '&num=' + amount_searchResults
    return urlA, urlB, urlC, urlF


# initialize V A R I A B L E S -------------------------------------------------

percentageProbabilityDictionary = {} # contains the probability in percent that the answer is correct # todo unused

# NAD = nummernAusgeschriebenDictionary
# a list that contains the numbers and also the words in a range from 0-20. it is used for the results, because lower value numbers are often written as words.
spelledOutNumbersDictionary = {"0": "null", "1": "eins", "2": "zwei", "3": "drei", "4": "vier", "5": "fünf",
                                   "6": "sechs", "7": "sieben", "8": "acht", "9": "neun", "10": "zehn", "11": "elf",
                                   "12": "zwölf", "13": "dreizehn", "14": "vierzehn", "15": "fünfzehn",
                                   "16": "sechszehn", "17": "siebzehn", "18": "achtzehn", "19": "neunzehn",
                                   "20": "zwangzig"}  # todo english words

new = 2
searchEngineUrl = "https://www.google.de/search?q=" # todo make configurable via config.ini
amount_searchResults = '30'

# C O R E   L O G I C  ---------------------------------------------------------

AnswerAText = getAnswerA()
AnswerBText = getAnswerB()
AnswerCText = getAnswerC()
QuestionText, QuestionTextReduced = getQuestion()

urlA, urlB, urlC, urlF = defineSearchEngineUrls()

pyperclip.copy(QuestionTextReduced)  # copies the question text into the clipboard
resultText = getResultViaRequest()
cleanedResult = cleanHtmlResult()
results = cleanedResult.split()  # splits multiple results into a word-list
print(QuestionText + '\n')  # print the question

# prints the answer
if debugResult == '1':
    print(cleanedResult)
    print(AnswerAText)
    print(AnswerBText)
    print(AnswerCText)

# get list of exact matches for A, B and C
listA_exactMatches, approximateMatches_A, Asplit, listA_approximateMatches = AnswerFunctions.answerA(AnswerAText,
                                                                                                     AnswerBText,
                                                                                                     AnswerCText,
                                                                                                     cleanedResult,
                                                                                                     results,
                                                                                                     mratioDifferenceFloat,
                                                                                                     spelledOutNumbersDictionary,
                                                                                                     percentageProbabilityDictionary)
listB_exactMatches, approximateMatches_B, Bsplit, listB_approximateMatches = AnswerFunctions.answerB(AnswerAText,
                                                                                                     AnswerBText,
                                                                                                     AnswerCText,
                                                                                                     cleanedResult,
                                                                                                     results,
                                                                                                     mratioDifferenceFloat,
                                                                                                     spelledOutNumbersDictionary,
                                                                                                     percentageProbabilityDictionary)
listC_exactMatches, approximateMatches_C, Csplit, listC_approximateMatches = AnswerFunctions.answerC(AnswerAText,
                                                                                                     AnswerBText,
                                                                                                     AnswerCText,
                                                                                                     cleanedResult,
                                                                                                     results,
                                                                                                     mratioDifferenceFloat,
                                                                                                     spelledOutNumbersDictionary,
                                                                                                     percentageProbabilityDictionary)

# get amount of exact matches for A, B and C
exactMatches_A = len(listA_exactMatches)
exactMatches_B = len(listB_exactMatches)
exactMatches_C = len(listC_exactMatches)

printEvaluatedResult()

# open a browser tab: question and answer (if uncommented)
# for debugging purposes or if you want to take a look at the search results by yourself!
# webbrowser.open(urlA,new);
# webbrowser.open(urlB,new);
# webbrowser.open(urlC,new);
# webbrowser.open(urlF,new);

if activateRunTimeMeasurement == 1:
    end = time.time()
    print(end - start)
