#!/usr/bin/env python
# coding: utf-8

#plot Chl-a (NetCDF file) from CMEMS
import os
import glob
import matplotlib
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import xarray as xr
import numpy as np
from scipy.io import netcdf
import cartopy 
import cartopy.crs as ccrs
plt.rcParams["figure.figsize"] = (9,6) #define the size of the figures                
import warnings
warnings.filterwarnings('ignore')


#define the data folder
rootPath = 'data/'
#create the data/ folder if not already existing (will not be the case during this session):
if not os.path.exists(rootPath):
    os.makedirs(rootPath)

# OPTION 1 : using xarray
ds = xr.open_dataset('chl_olci_L3_1km_daily_onemonth.nc')

min_lat  = min(ds['lat'])
max_lat  = max(ds['lat'])
min_lon  = min(ds['lon'])
max_lon  = max(ds['lon'])

lats  = ds['lat']
lons  = ds['lon']
mydate = '2017-06-01'
chl= ds['CHL'].sel(time=mydate)
variable = 'CHL'
print('the unit of the variable', variable, 'is', ds[variable].attrs['units'])

plt.figure()
ax   = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cartopy.feature.LAND, linewidth=1, facecolor='lightgrey', edgecolor='k', zorder=1)
ax.add_feature(cartopy.feature.OCEAN, facecolor="lightblue")
ax.set_extent([min_lon, max_lon, min_lat, max_lat])

plot=plt.contourf(lons, lats, chl, cmap = 'hsv', transform=ccrs.PlateCarree())
func = lambda x,pos: "{:g}".format(x/1e18) 
fmt = matplotlib.ticker.FuncFormatter(func)
plt.colorbar(plot, ax=ax, shrink=0.8, format=fmt)
plt.title('CHL-a concentration [mg µm^-3]', size=18)
 
ax.coastlines()
ax.gridlines(draw_labels=True)
plt.show()


# OPTION 2: using netcdf
dataset = netcdf.netcdf_file('chl_olci_L3_1km_daily_onemonth.nc', maskandscale = True, mmap = False)

min_lat  = min(dataset.variables['lat'])
max_lat  = max(dataset.variables['lat'])
min_lon  = min(dataset.variables['lon'])
max_lon  = max(dataset.variables['lon'])

prc  = dataset.variables['CHL'][0, :, :]
lats = dataset.variables['lat'][:]
lons = dataset.variables['lon'][:]
plt.figure()
ax   = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cartopy.feature.LAND, linewidth=1, facecolor='lightgrey', edgecolor='k', zorder=1)
ax.add_feature(cartopy.feature.OCEAN, facecolor="lightblue")
ax.set_extent([min_lon, max_lon, min_lat, max_lat])

plot=plt.contourf(lons, lats, prc, cmap = 'hsv', transform=ccrs.PlateCarree())
func = lambda x,pos: "{:g}".format(x/1e18) 
fmt = matplotlib.ticker.FuncFormatter(func)
plt.colorbar(plot, ax=ax, shrink=0.8, format=fmt)
plt.title('CHL-a concentration [mg µm^-3]', size=18)
 
ax.coastlines()
ax.gridlines(draw_labels=True)
plt.show()

