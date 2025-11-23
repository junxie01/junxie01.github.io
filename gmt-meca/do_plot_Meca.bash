#!/bin/bash
cat >mec.dat<<eof
# lon lat depth str dip slip st dip slip mant exp plon plat
239.384 34.556 12.  270.6   71.3 -124.4 0 72 -90 5.5 0 0 0
eof
gmt begin meca png
gmt psmeca mec.dat -R239/240/34/35.2 -Jm4c -Sc2c 
gmt end
