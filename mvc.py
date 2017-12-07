#!/usr/bin/env python

"""
For each timestep, create a maximum-value composite procedure NDVI from
1982-2015. We are skipping 1981 as there is only half the data we need to be
consistent.

"""

import numpy as np
import sys
import os
import xarray as xr
import glob
import matplotlib.pyplot as plt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (07.12.2017)"
__email__   = "mdekauwe@gmail.com"

ndvi_scale = 10000.
percentile_scale = 10.

ncols = 4320
nrows = 2160
ntime = 24
ndvi3g = np.ones((ntime,nrows,ncols)) * -9999.9

st_yr = 1982
en_yr = 2015
for yr in range(st_yr, en_yr+1):

    for dt in ["0106", "0712"]:
        fn = "data/ndvi3g_geo_v1_%d_%s.nc4" % (yr, dt)

        if dt == "0106":
            offset = 0
        elif dt == "0712":
            offset = 12

        print(yr)
        ds = xr.open_dataset(fn)

        ndvi = ds.ndvi
        percentile = ds.percentile

        ndvi /= ndvi_scale

        # Flag values are embeded on the percentile variable:
        # 2000*flag + percentile. Thus, the actual percentile three ranges:
        # flag 0: ndvi without apparent issues (good value)  [0 1000]
        percentile = percentile.astype(np.float32) / percentile_scale
        ndvi = np.where(percentile <= 1000., ndvi, np.nan)

        ndvi = np.where(np.logical_and(ndvi >= 0.00, ndvi <= 1.0), ndvi, np.nan)

        for i in range(12):
            j = i + offset
            x = np.flipud(ndvi[i,:,:])
            ndvi3g[j,:,:] = np.where(x > ndvi3g[j,:,:], x, ndvi3g[j,:,:])

ndvi3g = np.where(np.logical_and(ndvi3g >= 0.00, ndvi3g <= 1.0), ndvi3g, np.nan)
#plt.imshow(ndvi3g[12,:,:])
#plt.colorbar()
#plt.show()
