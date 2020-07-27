'''
#===============================================================
# This code compute and plot CFODD for mixed-phase clouds. 
# Required input:
#   1) Radar reflectivity (from 2B-GEOPROF)
#   2) Height (from 2B-GEOPROF)
#   3) Cloud top temperature (from ECWMF-AUX)
#   4) cloud phase and supercooled water layer top (from 2B-CLDCLASS-LIDAR) 
#   5) LWP (from MODIS-5KM-AUX, MODIS-1KM-AUX)
#   6) Cloud top droplet effective radius (from MODIS-5KM-AUX, MODIS-1KM-AUX)
# History:
#   1) JAN 30, 2020, First created. Xianwen.
#=================================================
'''

import os
import glob
import numpy as np
import time as tm
from netCDF4 import Dataset, num2date,date2num
from datetime import datetime
from hdf_eos_utils import * #read_hdf,require_sd_info_hdf,require_vs_info_hdf

#------------------------
#--input file location--
#------------------------
print('--input file location--')

data_home='/Volumes/WD2T_1/'
path_PRE=data_home+'2C-PRECIP-COLUMN.P1_R05/'

#------------------------
#--output file location--
#------------------------
out_path='./precip_Arctic/'
if not os.path.exists(out_path):
   os.mkdir(out_path)
   print('Created output directory: '+out_path)

#---------------------------
#-- creat grids and others-- 
#---------------------------
nlat=90
latbnd=np.linspace(-90.,90.,nlat+1)
latitudes=np.linspace(-89.,89.,nlat) #for output netCDF dimension
nlon=180
lonbnd=np.linspace(-180.,180.,nlon+1)
longitudes=np.linspace(-179.,179.,nlon) #for output netCDF dimension

ndays_comm=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
ndays_leap=np.array([31,29,31,30,31,30,31,31,30,31,30,31])
nmon = 12

#years = np.array([2007,2008,2009,2010])
years = np.array([2007])
dates=[datetime(years[0],1+n,15) for n in range(0,nmon)] #for output netCDF dimension

#------------------------
#-- creat out variables-- 
#------------------------
# group1: precipitation type (rain certain, rain possible, snow certain, 
#         snow possible, mix certain, mix possible, no precip)
cnt_rain_poss = np.zeros((nmon,nlat,nlon),dtype=np.int64)
cnt_rain_cert = np.zeros((nmon,nlat,nlon),dtype=np.int64)
cnt_snow_poss = np.zeros((nmon,nlat,nlon),dtype=np.int64)
cnt_snow_cert = np.zeros((nmon,nlat,nlon),dtype=np.int64)
cnt_mix_poss  = np.zeros((nmon,nlat,nlon),dtype=np.int64)
cnt_mix_cert  = np.zeros((nmon,nlat,nlon),dtype=np.int64)
cnt_noprecp   = np.zeros((nmon,nlat,nlon),dtype=np.int64)
# group2: precipitation amount (categorized as above)
pre_rain_poss = np.zeros((nmon,nlat,nlon),dtype=np.int64)
pre_rain_cert = np.zeros((nmon,nlat,nlon),dtype=np.int64)
pre_snow_poss = np.zeros((nmon,nlat,nlon),dtype=np.int64)
pre_snow_cert = np.zeros((nmon,nlat,nlon),dtype=np.int64)
pre_mix_poss  = np.zeros((nmon,nlat,nlon),dtype=np.int64)
pre_mix_cert  = np.zeros((nmon,nlat,nlon),dtype=np.int64)

#==============================================
# create output  netcdf file
# 1. open a new file and add description info
rootgrp = Dataset("precip_statis_2x2.nc","w",format="NETCDF4")
rootgrp.description = "2C-PRECIP-COLUMN 2x2 statistics"
rootgrp.history = "Created "+ tm.ctime(tm.time())
rootgrp.source = "netCDF4 python module"

# 2. create dimensions
time=rootgrp.createDimension("time",None)
lat=rootgrp.createDimension("lat",nlat)
lon=rootgrp.createDimension("lon",nlon)

# 3. create variables
timevar=rootgrp.createVariable("time","f4",("time",))
latvar=rootgrp.createVariable("lat","f4",("lat",))
lonvar=rootgrp.createVariable("lon","f4",("lon",))
timevar.units="hours since 0001-01-01 00:00:00.0"
timevar.calendar="gregorian"
latvar.units="degrees_north"
lonvar.units="degrees_east"
cnt_rn_poss=rootgrp.createVariable("cnt_rain_poss","f8",("time","lat","lon",))
cnt_rn_cert=rootgrp.createVariable("cnt_rain_cert","f8",("time","lat","lon",))
cnt_sn_poss=rootgrp.createVariable("cnt_snow_poss","f8",("time","lat","lon",))
cnt_sn_cert=rootgrp.createVariable("cnt_snow_cert","f8",("time","lat","lon",))
cnt_mx_poss=rootgrp.createVariable("cnt_mix_poss","f8",("time","lat","lon",))
cnt_mx_cert=rootgrp.createVariable("cnt_mix_cert","f8",("time","lat","lon",))
cnt_no_prec=rootgrp.createVariable("cnt_noprecp","f8",("time","lat","lon",))
pre_rn_poss=rootgrp.createVariable("pre_rain_poss","f8",("time","lat","lon",))
pre_rn_cert=rootgrp.createVariable("pre_rain_cert","f8",("time","lat","lon",))
pre_sn_poss=rootgrp.createVariable("pre_snow_poss","f8",("time","lat","lon",))
pre_sn_cert=rootgrp.createVariable("pre_snow_cert","f8",("time","lat","lon",))
pre_mx_poss=rootgrp.createVariable("pre_mix_poss","f8",("time","lat","lon",))
pre_mx_cert=rootgrp.createVariable("pre_mix_cert","f8",("time","lat","lon",))
cnt_rn_poss.units=""
cnt_rn_cert.units=""
cnt_sn_poss.units=""
cnt_sn_cert.units=""
cnt_mx_poss.units=""
cnt_mx_cert.units=""
cnt_no_prec.units=""
pre_rn_poss.units="mm/h"
pre_rn_cert.units="mm/h"
pre_sn_poss.units="mm/h"
pre_sn_cert.units="mm/h"
pre_mx_poss.units="mm/h"
pre_mx_cert.units="mm/h"

# 4, write initial values to variables
times=date2num(dates,units=timevar.units ,calendar=timevar.calendar)
timevar[:]=times
latvar[:]=latitudes
lonvar[:]=longitudes
cnt_rn_poss[:,:,:]=cnt_rain_poss
cnt_rn_cert[:,:,:]=cnt_rain_cert
cnt_sn_poss[:,:,:]=cnt_snow_poss
cnt_sn_cert[:,:,:]=cnt_snow_cert
cnt_mx_poss[:,:,:]=cnt_mix_poss
cnt_mx_cert[:,:,:]=cnt_mix_cert
cnt_no_prec[:,:,:]=cnt_noprecp
pre_rn_poss[:,:,:]=pre_rain_poss
pre_rn_cert[:,:,:]=pre_rain_cert
pre_sn_poss[:,:,:]=pre_snow_poss
pre_sn_cert[:,:,:]=pre_snow_cert
pre_mx_poss[:,:,:]=pre_mix_poss
pre_mx_cert[:,:,:]=pre_mix_cert


#------------------------
#--loop granules-- 
#------------------------
print('--loop granules--')

for iyr in years:
  if (iyr%4 != 0):
      ndays=365
      days_cum=ndays_comm.cumsum()
  else:
      ndays=366
      days_cum=ndays_leap.cumsum()

  for iday in range(1,2): #range(1,ndays+1):
    imon=len(days_cum[days_cum<iday]) 
    print('---day ',iday)
    print('---mon ',imon)

    path_PRE_now=path_PRE+str(iyr)+"/"+str(iday).zfill(3)+"/"

    #- check path existance 
    if not os.path.exists(path_PRE_now):
        print('Path not found: ',path_PRE_now)
        continue

    #- get granual index under each directory
    grans=[]
    for fi in os.listdir(path_PRE_now):
        grans.append(fi[14:19])

    for ig in grans:
        print(ig)
        file_pre=glob.glob(path_PRE_now+'*_'+str(ig)+'_*.hdf')

       #- check file existance
        if len(file_pre)==0 or len(file_pre)>1: 
            print('FILE NOT FOUND: ',ig,' ',file_pre)
            continue

        #------------------------
        #--extract data from input--
        #------------------------
        #print('--extract data from input--')
        # variable info:
        # prate     : precipitation rate, mm/h, missing_value=-1000
        # prate_min : lower bound of prate uncertainty, mm/h, missing_value=-1000
        # prate_max : upper bound of prate uncertainty, mm/h, missing_value=-1000
        # pflag     : surface precipitation type at surface
        #             =0, no precip
        #             =9, uncertain
        #             =1, rain possible
        #             =2, rain probable
        #             =3, rain certain
        #             =4, snow possible
        #             =5, snow certain
        #             =6, Mixed precipitation possible
        #             =7, Mixed precipitation certain
        # ls_flag   : land/sea flag. =1,land; 2,ocean; 3,coast

        prate     , npix = read_vd_hdf2(file_pre[0],"Diagnostic_precip_rate")
        prate_min , npix = read_vd_hdf2(file_pre[0],"Diagnostic_precip_rate_min")
        prate_max , npix = read_vd_hdf2(file_pre[0],"Diagnostic_precip_rate_max")
        pflag     , npix = read_vd_hdf2(file_pre[0],"Precip_flag")
        lat       , npix = read_vd_hdf2(file_pre[0],"Latitude")
        lon       , npix = read_vd_hdf2(file_pre[0],"Longitude")
        ls_flag   , npix = read_vd_hdf2(file_pre[0],"Navigation_land_sea_flag")
 
        #print(np.max(pflag))
       #---------------------
       # gridded analysis 
       #---------------------
        for ix in range(0,npix):
        # lat*lon location    
           ilat = max(len(latbnd[latbnd<lat[ix]])-1,0)
           ilon = max(len(lonbnd[lonbnd<lon[ix]])-1,0)
           #if pflag[ix] == 4:
               #print(pflag[ix])
           if (prate[ix] >=-100):  #and (prate_min[ix]>=0) and (prate_max[ix]>=0):
               if pflag[ix] == 0:
                   cnt_noprecp[imon,ilat,ilon]=cnt_noprecp[imon,ilat,ilon]+1
               elif pflag[ix] == 1 or pflag[ix] == 2:
                   cnt_rain_poss[imon,ilat,ilon]=cnt_rain_poss[imon,ilat,ilon]+1
                   pre_rain_poss[imon,ilat,ilon]=pre_rain_poss[imon,ilat,ilon]+prate[ix]
               elif pflag[ix] == 3:
                   cnt_rain_cert[imon,ilat,ilon]=cnt_rain_cert[imon,ilat,ilon]+1
                   pre_rain_cert[imon,ilat,ilon]=pre_rain_cert[imon,ilat,ilon]+prate[ix]
               elif pflag[ix] == 4:
                   print(pflag[ix])
                   cnt_snow_poss[imon,ilat,ilon]=cnt_snow_poss[imon,ilat,ilon]+1
                   pre_snow_poss[imon,ilat,ilon]=pre_snow_poss[imon,ilat,ilon]+prate[ix]
               elif pflag[ix] == 5:
                   cnt_snow_cert[imon,ilat,ilon]=cnt_snow_cert[imon,ilat,ilon]+1
                   pre_snow_cert[imon,ilat,ilon]=pre_snow_cert[imon,ilat,ilon]+prate[ix]
               elif pflag[ix] == 6:
                   cnt_mix_poss[imon,ilat,ilon]=cnt_mix_poss[imon,ilat,ilon]+1
                   pre_mix_poss[imon,ilat,ilon]=pre_mix_poss[imon,ilat,ilon]+prate[ix]
               elif pflag[ix] == 7:
                   cnt_mix_cert[imon,ilat,ilon]=cnt_mix_cert[imon,ilat,ilon]+1
                   pre_mix_cert[imon,ilat,ilon]=pre_mix_cert[imon,ilat,ilon]+prate[ix]

        #print(npix)
        #exit()
print(np.sum(cnt_snow_poss))
#==============================================
# write grided statistics to netcdf file
cnt_rn_poss[:,:,:]=cnt_rain_poss
cnt_rn_cert[:,:,:]=cnt_rain_cert
cnt_sn_poss[:,:,:]=cnt_snow_poss
cnt_sn_cert[:,:,:]=cnt_snow_cert
cnt_mx_poss[:,:,:]=cnt_mix_poss
cnt_mx_cert[:,:,:]=cnt_mix_cert
pre_rn_poss[:,:,:]=pre_rain_poss
pre_rn_cert[:,:,:]=pre_rain_cert
pre_sn_poss[:,:,:]=pre_snow_poss
pre_sn_cert[:,:,:]=pre_snow_cert
pre_mx_poss[:,:,:]=pre_mix_poss
pre_mx_cert[:,:,:]=pre_mix_cert
# close output file
rootgrp.close()

print('-- This is the end of the code. --')

# END
