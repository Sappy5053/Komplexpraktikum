# https://www.imagemagick.org/Usage/color_mods/#color_lut
# https://www.imagemagick.org/Usage/canvas/#gradient
convert -size 1x33  gradient:red-yellow gradient:yellow-green gradient:green-blue   -append  gradient.png
convert 20230612-122530_LI.png   \( gradient.png -flip \) -clut -transparent blue colorthres.png	#ab 230607: blue=transp, vorher red
convert -composite 20230612-122530_RSI.png colorthres.png 20230612-122530_thr.png
