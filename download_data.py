#!/usr/bin/env python

"""
Download the NDVI3g (third generation GIMMS NDVI from AVHRR sensors).
"""

from urllib.request import urlopen
import numpy as np
import sys
import os
import pandas as pd
import io
import requests


__author__  = "Martin De Kauwe"
__version__ = "1.0 (07.12.2017)"
__email__   = "mdekauwe@gmail.com"

save_dir_name = "data"
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)

url = "https://ecocast.arc.nasa.gov/data/pub/gimms/3g.v1/00FILE-LIST.txt"
s = requests.get(url).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')))

for index, row in df.iterrows():
    url_f = row.values[0]
    response = urlopen(url_f.strip())
    ofile = os.path.join(save_dir_name, url_f.split('/')[-1])
    f = open(ofile, 'w')
    f.write(response.read())
    f.close()
