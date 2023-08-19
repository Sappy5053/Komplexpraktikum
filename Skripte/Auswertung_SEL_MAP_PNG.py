#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 21:59:42 2021

@author: jonas, adapted to png-output by OHA 210915

"""
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

HEADERSIZE = 6
DELIMITER = '\t'
SHOWIMAGE = False	# if you want to see the figure, this has to be true
SAVE = True        # if you want to save the figure as png, this has to be true
#FILE = "jenami10.dat.txt"
#FILE = "micfs44.dat.txt"
FILE = sys.argv[1]
PARENT_FOLDER = ""
#PARENT_FOLDER = "../Daten/AuJun21/DATA/"
SEL_FILTER = 1 # 0 = plot every Ion value; 1= plot only Latchup events
#print(FILE)

SELcount = 0		#Zähler für Anzahl aufgetretener Latchups (Datenzeilen mit 3.Spalte>0)
IONcount = 0		#Zähler für Ionenanzahl (alle Datenzeilen)
teilerfaktor = 34	#bei Skalierungsfaktor (Reduzierung der Ausgabebildgröße) 34 meist keine Leerzeilen mehr; Zum Testen SEL_FILTER ausschalten und Ergebnisbild anschauen
					#Hintergrund: Y-Ablenkung linear -> Scanzeilen leicht schräg in Daten und nicht jede Datenzeile genutzt

Xdim = int(4096/teilerfaktor)	#X-Dimension für Ausgabedatenfeld
Ydim = int(4096/teilerfaktor)	#Y-Dimension für Ausgabedatenfeld
Datenfeld = np.zeros((Xdim,Ydim))	#leeres Datenfeld anlegen

with open(PARENT_FOLDER + FILE,'r') as csv_file:
	plots = csv.reader(csv_file, delimiter=DELIMITER)
	for i in range(HEADERSIZE):                         # Skip the HEADER of the csv
		next(plots)

	for row in plots:	#Datenzeilen der csv durchgehen
		if(int(row[2]) >= SEL_FILTER):	#Wenn SEL aufgetreten	(3.Spalte = 4)
			# SEL-Stelle in Datenfeld eintragen und Bild 90° links drehen, damit es zu den Mikroskopbildern passt. 
			X = int(int(row[0])/teilerfaktor) -1	#ohne "-1" manchmal out of range-Fehler
			Y = Ydim - int(int(row[1])/teilerfaktor) -1	#ohne "-1" manchmal out of range-Fehler
			Datenfeld[Y,X] = Datenfeld[Y,X] + 1	#SEL-Anzahl an betroffener Stelle +1
			SELcount = SELcount +1
		IONcount=IONcount+1	#i = i+1

print("File: " + str(FILE) + "\tIons: " + str(IONcount) + "\tLatchups: " + str(SELcount) + "\tLatchups/Ion: " + str(SELcount/IONcount))

#############
if SHOWIMAGE:
	image = plt.imshow(Datenfeld, cmap='gray')
#	image.set_data(Datenfeld)
#	image.autoscale()
	plt.pause(3)
#	while True:
#		plt.pause(0.1)

if SAVE:
	plt.imsave(PARENT_FOLDER + FILE + ".png", Datenfeld, cmap='gray')
