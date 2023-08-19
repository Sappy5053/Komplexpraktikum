for entry in `ls *.dat`; do
	echo "Datei: " $entry "	Ohne Endung: "${entry/.dat} "	Ausgabe: "${entry/.dat}"_SWtra.png"
	perl extract_dat2txt.pl $entry
done

#for entry in `ls $search_dir`; do
for entry in `ls *.dat.txt`; do
#	echo "Datei: " $entry "	Ohne Endung: "${entry/.dat.txt} "	Ausgabe: "${entry/.dat.txt}"_SWtra.png"
#	echo "$(basename "$entry")"	#ohne Pfad
	python3 Auswertung_SEL_MAP_PNG.py $entry	#Datenkonvertierung der aktuellen Datei (Texttabelle -> PNG-Bild)
	convert $entry".png" -transparent black -colors 2 ${entry/.dat.txt}"_SWtra.png"	#Konvertieren in SW-Bild mit transparentem Hintergrund
done
