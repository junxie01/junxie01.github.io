#!/bin/bash
gmt begin cyl2 png
gmt coast -R-180/180/-90/90 -JQ6i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
