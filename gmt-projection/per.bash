#!/bin/bash
gmt begin per png
gmt coast -R-180/180/-90/90 -JG0/0/6000/90/0/0/60/60/5i -Ggray -Swhite -Dl -Bxa90 -Bya45 -A30000 -W0p 
gmt end
