#!/bin/bash
gmt begin orth png
gmt coast -R-180/180/-90/90 -JG0/0/6i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
