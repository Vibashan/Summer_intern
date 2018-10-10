#!/usr/bin/env python

import csv
import numpy as np
from collections import deque

with open("pur_lose_add_dist.csv", 'r') as data_file:
  data_file.readline() # Skip first line
  reader = csv.reader(data_file, delimiter=',')
  D = deque()
  for xp,yp,xe_1,ye_1,xe_2,ye_2,xt,yt in reader:
     d = float(xp),float(yp),float(xe_1),float(ye_1),float(xe_2),float(ye_2),float(xt),float(yt)
     print d

     D.append(d)
  D = np.array(D)
  #prfloat D