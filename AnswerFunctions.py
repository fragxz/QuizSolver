# AnswerFunctions Module
import difflib
from difflib import SequenceMatcher

def answerA(AntwortAText, AntwortBText, AntwortCText, cleanedResult, ergebnisliste, mratioDifferenceFloat, nummernAusgeschriebenDictionary, wahrscheinlichkeitenDictionary):
    # init var
    exakteTreffer_ListA = []
    ungefaehreTreffer_A = 0
    ungefaehreTreffer_ListA = []
    Asplit = AntwortAText.split() # splitte antwort A | zB von "Die Alten Ägypter" in ['Die', 'Alten', 'Ägypter']
    zsmgAntwortA = ['zsmgAntwortA: '] #zusammengesetzteAntwort A
    mostcommonA = [] #mostCommon A
    prozentualeUebereinstimmungA = 0
    ratioProzentA = 0
    mratioA = 0
    ergebnisAnzahlA = 0 #Addiert ALLE Ergebnisse die gefunden wurden zusammen (zB "Die Alten Ägypter" - 3x Die 10x Alten 15x Ägypten = 28 Ergebnisse die übereinstimmen)

    # EXAKTE Treffer -----------------------------------
    if AntwortAText in cleanedResult:
       #exakteTreffer_A = cleanedResult.count(AntwortAText)
       for x in ergebnisliste:
          if x == AntwortAText:
             exakteTreffer_ListA.append(x)
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
              while AntwortCText in b:
                 b.remove(AntwortCText) #entferne AntwortC aus dem Array von AntwortA

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
        nAD = nummernAusgeschriebenDictionary.get(x) #wandelt Zahlen in Wörter um (zB "8" zu "acht")
        if nAD: #wenn nummernAusgeschriebenDictionary.get(x) existiert
            numericAusgeschrieben = difflib.get_close_matches(nAD, ergebnisliste, 6) #ähnliche ergebnisse zu der ausgeschriebenen Zahl (zB statt "8" sucht er nun nach "acht")
            print (numericAusgeschrieben) #Ausgabe der gefundenen Ergebnisse

    prozentualeUebereinstimmungA = round(prozentualeUebereinstimmungA / len(Asplit),2) #berechne durchschnittliche Wahrscheinlichkeit in Abhängigkeit zu den vorhandenen Wörtern (Asplit)
    prozentualeUebereinstimmungA = (prozentualeUebereinstimmungA * 0.8) + ergebnisAnzahlA #DEBUG / TEST
    wahrscheinlichkeitenDictionary['A'] = prozentualeUebereinstimmungA
    return exakteTreffer_ListA, ungefaehreTreffer_A;


# --------------


def answerB(AntwortAText, AntwortBText, AntwortCText, cleanedResult, ergebnisliste, mratioDifferenceFloat, nummernAusgeschriebenDictionary, wahrscheinlichkeitenDictionary):
    # init var
    exakteTreffer_ListB = []
    ungefaehreTreffer_B = 0
    ungefaehreTreffer_ListB = []

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
        nAD = nummernAusgeschriebenDictionary.get(x) #
        if nAD: #wenn nummernAusgeschriebenDictionary.get(x) existiert
            numericAusgeschrieben = difflib.get_close_matches(nAD, ergebnisliste, 6) #ähnliche ergebnisse zu der ausgeschriebenen Zahl (zB statt "8" sucht er nun nach "acht")
            print (numericAusgeschrieben) #Ausgabe der gefundenen Ergebnisse

    prozentualeUebereinstimmungB = round(prozentualeUebereinstimmungB / len(Bsplit),2) #berechne durchschnittliche Wahrscheinlichkeit in Abhängigkeit zu den vorhandenen Wörtern (Asplit)
    prozentualeUebereinstimmungB = (prozentualeUebereinstimmungB * 0.8) + ergebnisAnzahlB
    wahrscheinlichkeitenDictionary['B'] = prozentualeUebereinstimmungB
    return exakteTreffer_ListB, ungefaehreTreffer_B;

# -------

def answerC(AntwortAText, AntwortBText, AntwortCText, cleanedResult, ergebnisliste, mratioDifferenceFloat, nummernAusgeschriebenDictionary, wahrscheinlichkeitenDictionary):
    # init var
    exakteTreffer_ListC = []
    ungefaehreTreffer_C = 0
    ungefaehreTreffer_ListC = []

    Csplit = AntwortCText.split() # splitte antwort C

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
    return exakteTreffer_ListC, ungefaehreTreffer_C;
#

