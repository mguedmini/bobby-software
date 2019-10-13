# -*- coding: utf-8 -*-

#import OpenCV library
import cv2

# wird für die Audioausgabe benötigt
import os

# wird benötigt um vergangene Sekunden zu berechnen
import datetime

# wird zur Initialisierung der externen Webcam benötigt (und ganz unten um Ausgaben bei Zustandswechseln zu bremsen)
from time import sleep

# Anbindung an Arduino initialisieren, Beispiel von: https://playground.arduino.cc/Interfacing/Python
import serial

# Der Pfad war auch schon mal /dev/cu.usbmodem1411 (in der Arduino-IDE unter Port ersichtlich), ändert sich uU bei Reboot
ser = serial.Serial('/dev/cu.usbmodem14101')

# Funktionen zur Ansteuerung des Arduinos
def macheYoga():
    ser.write(b'Y')
def zeigeKalibriert():
    ser.write(b'V')
def zeigeNichtKalibriert():
    ser.write(b'W')


# Webcam initialiseren, manchmal ist 0 die interne, manchmal die externe Webcam
cam = cv2.VideoCapture(0)

# ohne Wartezeit funktioniert die externe Webcam nicht zuverlässig
sleep(1)

zeigeNichtKalibriert()

# Ein Array mit den letzten Positionen, um z.B. Gesamtbewegung während Zeitspanne messen zu können
# Elemente sind Tupel aus y und y+h
# Aktuell benutze ich nur den letzten/vorletzten Eintrag
letztePositionGesicht = []
anzahlLetzerPositionen = 5

# Beispiele: 'FACE DETECTION USING OPENCV AND PYTHON: A BEGINNER’S GUIDE',
# https://www.superdatascience.com/opencv-face-detection/
# und
# https://thecodacus.com/opencv-python-face-detection
def erkenneGesicht():
    global letztePositionGesicht

    # ein Bild von der Webcam laden
    ret_val, img = cam.read() #statt mit

    # Code von 'FACE DETECTION USING OPENCV AND PYTHON: A BEGINNER’S GUIDE':
    #convert the test image to gray image as opencv face detector expects gray images
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #load cascade classifier training file for haarcascade
    haar_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    #let's detect multiscale (some images may be closer to camera than others) images
    faces = haar_face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5);

    #print the number of faces found
    print('Faces found: ', len(faces))
    ########

    if len(faces) == 0:
        # immer die letzten 5 aufheben, dann neues anhängen
        if (len(letztePositionGesicht) > anzahlLetzerPositionen):
            del letztePositionGesicht[0]
        letztePositionGesicht.append((None, None))
        return None,None

    for (x, y, w, h) in faces:
        # immer die letzten 5 aufheben, dann neues anhängen
        if (len(letztePositionGesicht) > anzahlLetzerPositionen):
            del letztePositionGesicht[0]
        letztePositionGesicht.append((y,y+h))
        return y,y+h

def audioausgabe(file):
    # https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
    os.system('sox "../assets/sounds/'+ file +'.mp3" -d -q');

###

# Zustände siehe Zustandsdiagramm
zustand1 = "Z1: Kein Nutzer: Der Roboter ist allein."
zustand2 = "Z2: Nutzer anwesend: Nutzer erkannt, sitzt aber noch nicht still."
zustand3 = "Z3: Warten auf Start-Position: Roboter wartet auf Einnahme der Kalibrierhaltung."
zustand4 = "Z4: Kalibriervorgang"
zustand5 = "Z5: Nutzer sitzt gerade und die Sitzhöhe ist eingestellt."
zustand6 = "Z6: Nutzer bewegt sich."
zustand7 = "Z7: Nutzer sitzt still."
zustand8 = "Z8: Nutzer steht & warten auf neue Kalibrierung: Roboter nimmt stehenden Nutzer an und wartet, bis dieser aus dem Bild gegangen ist, um neu zu kalibrieren."


# Globale Variablen:
kalibrierteGesichtshoehe = (None,None)
# Zeitpunkt des letzten Zustandswechsels
letzterZustandswechsel = None

aktuellerZustand = None

# Aktuellen Zustand ändern (und vorher bisherigen und neuen Zustand ausgeben); Zeit des Zustandswechsels speichern
def setzeAktuellenZustand(neuerZustand):
    global aktuellerZustand
    global letzterZustandswechsel
    print("von Zustand " + str(aktuellerZustand) + " --> " + str(neuerZustand))
    aktuellerZustand = neuerZustand
    letzterZustandswechsel = datetime.datetime.now()

# bewerten, ob eine größere Kopfbewegung stattgefunden hat
def groessereKopfbewegungErfolgt(y1, y2):
    global letztePositionGesicht
    (y1_alt,y2_alt) = letztePositionGesicht[-2]
    verschiebung = (y1-y1_alt) / (y2_alt-y1_alt)
    print ("Kopfbewegung relativ zur letzten Position: " + str(verschiebung))
    return abs(verschiebung) > 0.25

# bewerten, ob im Vergleich zur kalibrierten Höhe eine größere Kopfbewegung stattgefunden hat
# Achtung: negative Werte falls Kopf höher (weil Zeilen/Spalten bei OpenCV ab oben links gezählt werden)
def kopfpositionRelativKalibrierung(y1, y2):
    global kalibrierteGesichtshoehe
    (y1_kalibriert,y2_kalibriert) = kalibrierteGesichtshoehe
    verschiebung = (y1-y1_kalibriert) / (y2_kalibriert-y1_kalibriert)
    print ("Kopfbewegung relativ zur Kalibrierung: " + str(verschiebung))
    return verschiebung

def laengerImZustandAls(xSekunden):
    global letzterZustandswechsel
    # siehe
    # https://stackoverflow.com/questions/100210/what-is-the-standard-way-to-add-n-seconds-to-datetime-time-in-python
    return datetime.datetime.now() > letzterZustandswechsel + datetime.timedelta(seconds=xSekunden)


# beim Start des Programms Zustand setzen
setzeAktuellenZustand(zustand1)

while True:
    print(aktuellerZustand)
    if aktuellerZustand == zustand1:
        zeigeNichtKalibriert()
        y1,y2 = erkenneGesicht()
        if y1 != None:
            audioausgabe("hallo")
            setzeAktuellenZustand(zustand2)
    elif aktuellerZustand == zustand2:
        zeigeNichtKalibriert()
        # wenn kein Gesicht erkannt, aktuellerZustand = "S1: …"
        (y1_alt,y2_alt) = letztePositionGesicht[-1]
        y1,y2 = erkenneGesicht()

        print("y1: "+str(y1))
        print("y2: "+str(y2))
        print("y1_alt: "+str(y1_alt))
        print("y2_alt: "+str(y2_alt))

        if y1 == None:
            audioausgabe("endlich_alleine")
            macheYoga()
            setzeAktuellenZustand(zustand1)
        elif laengerImZustandAls(5):
            audioausgabe("kalibrieren")
            setzeAktuellenZustand(zustand3)
        elif groessereKopfbewegungErfolgt(y1,y2):
            print("zurück in 2")
            setzeAktuellenZustand(zustand2)
            # sonst wenn größere Kopfbewegung (d.h. Abweichung letzte Position Gesicht - aktuelle Position Gesicht größer als
            # Tolenranzbereich (muss man festlegen), aktuellerZustand = "S2: …"
            # sonst wenn 5 Sekunden vergangen, Ausgabe: "Sitz gerade" und aktuellerZustand = "S3: …"
    elif aktuellerZustand == zustand3:
        zeigeNichtKalibriert()
        (y1_alt,y2_alt) = letztePositionGesicht[-1]
        y1,y2 = erkenneGesicht()
        if y1 == None:
            audioausgabe("endlich_alleine")
            macheYoga()
            setzeAktuellenZustand(zustand1)
        elif laengerImZustandAls(2):
            setzeAktuellenZustand(zustand4)
    elif aktuellerZustand == zustand4:
        zeigeNichtKalibriert()
        # wenn kein Gesicht erkannt, aktuellerZustand = "S1: …"
        (y1_alt,y2_alt) = letztePositionGesicht[-1]
        y1,y2 = erkenneGesicht()
        if y1 == None:
            audioausgabe("endlich_alleine")
            macheYoga()
            setzeAktuellenZustand(zustand1)
        elif laengerImZustandAls(4):
            kalibrierteGesichtshoehe = (y1, y2)
            audioausgabe("elevator-ding")
            audioausgabe("hoehe_erfasst")
            setzeAktuellenZustand(zustand5)
        elif groessereKopfbewegungErfolgt(y1,y2):
            audioausgabe("gezappel")
            setzeAktuellenZustand(zustand2)
        else:
            audioausgabe("beep");
    elif aktuellerZustand == zustand5:
        zeigeKalibriert()
        (y1_alt,y2_alt) = letztePositionGesicht[-1]
        y1,y2 = erkenneGesicht()
        if y1 == None:
            audioausgabe("endlich_alleine")
            macheYoga()
            setzeAktuellenZustand(zustand1)
        elif groessereKopfbewegungErfolgt(y1, y2):
            setzeAktuellenZustand(zustand6)
    elif aktuellerZustand == zustand6:
        zeigeKalibriert()
        (y1_alt,y2_alt) = letztePositionGesicht[-1]
        y1,y2 = erkenneGesicht()
        if y1 == None:
            audioausgabe("endlich_alleine")
            macheYoga()
            setzeAktuellenZustand(zustand1)
        elif groessereKopfbewegungErfolgt(y1, y2):
            setzeAktuellenZustand(zustand6)
        elif laengerImZustandAls(10) and kopfpositionRelativKalibrierung(y1, y2) < 0.25:
            setzeAktuellenZustand(zustand6)
        elif laengerImZustandAls(10) and kopfpositionRelativKalibrierung(y1, y2) > -0.25:
            audioausgabe("nicht_dumm_nicht_krumm")
            setzeAktuellenZustand(zustand7)
        elif laengerImZustandAls(10):
            setzeAktuellenZustand(zustand5)
    elif aktuellerZustand == zustand7:
        zeigeKalibriert()
        (y1_alt,y2_alt) = letztePositionGesicht[-1]
        y1,y2 = erkenneGesicht()
        if y1 == None:
            audioausgabe("endlich_alleine")
            macheYoga()
            setzeAktuellenZustand(zustand1)
        elif groessereKopfbewegungErfolgt(y1, y2):
            setzeAktuellenZustand(zustand6)
        elif laengerImZustandAls(10) and kopfpositionRelativKalibrierung(y1, y2) < 0.25:
            setzeAktuellenZustand(zustand8)
        elif laengerImZustandAls(10):
            audioausgabe("kalibrieren_erneut")
            setzeAktuellenZustand(zustand3)
    elif aktuellerZustand == zustand8:
        zeigeNichtKalibriert()
        (y1_alt,y2_alt) = letztePositionGesicht[-1]
        y1,y2 = erkenneGesicht()
        if y1 == None:
            audioausgabe("endlich_alleine")
            macheYoga()
            setzeAktuellenZustand(zustand1)

    # sonst Ausgaben im Falle einer Schleife Zustand X -> Zustand X zu schnell
    sleep(0.2)
