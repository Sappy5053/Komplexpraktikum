#scaliere Mikroskopbild (*.tif) auf Größe der Messdaten
for entry in `ls *.tif`; do
    convert $entry -resize 73.5% scaled.tif
done
#flip messdaten (*.png) an y-Achse
for entry in `ls *.png`; do
    convert $entry -flop flop.png
done

#empfindliche Stellen rot:
convert flop.png -fill red +opaque black rot.png

#Uberlagern
convert -page +0+0 scaled.tif -page +175+116 rot.png -layers merge +repage ueberlagert.tif

