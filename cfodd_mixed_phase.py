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

import os
import glob
import numpy as np
from hdf_eos_utils import read_hdf_SD,require_SD_info_hdf,read_hdf_VD,require_VD_info_hdf

#------------------------
#--input file location--
#------------------------
print('--input file location--')

data_home='/Volumes/JXW/Data/'
path_GEO=data_home+'2B-GEOPROF/2007/001/'
path_EC=data_home+'ECMWF-AUX/2007/001/'
path_CCL=data_home+'2B-CLDCLASS-LIDAR_P1_R05/2007/001/'
path_MOD=data_home+'MODIS-AUX/2007/001/'

#------------------------
#-- creat Ze vs T bins-- 
#------------------------
num_zebin=25
zebnd=np.linspace(-30,20,num_zebin+1)
num_tbin=20
tbnd=np.linspace(-30,20,num_tbin+1)

cnt_sampl=np.zeros((num_tbin,num_zebin)) # counted number of samples
pdf_sampl=np.zeros((num_tbin,num_zebin)) # PDF of cnt_sampl for each tbnd

#------------------------
#--loop granules-- 
#------------------------
print('--loop granules--')
rng_gran=range(3607,3623)

for ig in rng_gran:
    #print(ig)
    file_ecmwf=glob.glob(path_EC+'*'+str(ig)+'_*')
    file_geo=glob.glob(path_GEO+'*'+str(ig)+'_*')
    file_ccl=glob.glob(path_CCL+'*'+str(ig)+'_*')
    file_mod=glob.glob(path_MOD+'*'+str(ig)+'_*')
   #- check file existance
    if len(file_ecmwf)==0 or len(file_ecmwf)>1: 
        print('NOT FOUND or TWO MANY: ',ig,' ',file_ecmwf)
        break
    if len(file_geo)==0 or len(file_ecmwf)>1: 
        print('NOT FOUND or TWO MANY: ',ig,' ',file_geo)
        break
    if len(file_ccl)==0 or len(file_ecmwf)>1: 
        print('NOT FOUND or TWO MANY: ',ig,' ',file_ccl)
        break
    if len(file_mod)==0 or len(file_ecmwf)>1: 
        print('NOT FOUND or TWO MANY: ',ig,' ',file_mod)
        break
    #------------------------
    #--extract data from input--
    #------------------------
    print('--extract data from input--')
    #require_SD_info_hdf(file_geo[0])
    #require_VD_info_hdf(file_geo[0])

  # from 2B-GEOPROF 
    ze,dimsz=read_hdf_SD(file_geo[0],"Radar_Reflectivity")
    num_pix=dimsz[0]
    num_lev=dimsz[1]
    cld_msk,dimsz=read_hdf_SD(file_geo[0],"CPR_Cloud_mask")
    sfc_loc,dimsz=read_hdf_VD(file_geo[0],"SurfaceHeightBin")

  # from 2B-CLDCLASS
    #sfc_loc,dimsz=read_hdf(file_geo,"CPR_Cloud_mask")

  # from ECMWF-AUX
    tair,dimsz=read_hdf_SD(file_ecmwf[0],"Temperature")
    #tair=np.ma.masked_where(tair<=-999,tair-273.15) #mask NaN, else Kelvin to Celsius.

    #cld_phase,dimsz=read_hdf(file_ccl,"CloudPhase")
    
    #exit('end check point')
    
    #------------------------
    #--preprocess the data--
    # mask invalide pixels
    #------------------------
    #a. surface layer and clutter
     #for ig in range(0,num_pix):
    #convert valid range from 1-125 to 0-124
    print(max(sfc_loc))
    print(min(sfc_loc))
    print(sfc_loc[0:3])
    sfc_loc=np.where(1<=sfc_loc<=125,sfc_loc-1,sfc_loc)
    print(sfc_loc[0:3])
    exit()
    #for ig in range(0,1):
    #    print(srf_loc[0])
    #    print(ze[ig,srf_loc-1])
    #    print(tair[ig,srf_loc-1])
    #------------------------
    #--conditional sampling--
    #------------------------
    print('--conditional sampling--')
    #print(ze[0:3,:])
    #print(cld_msk[0,:])
    # 1. Tctop <0.0 [Celcius] 
    #for ig in range(0,num_pix):
        
    # 2. Liquid cloud top
    
    # 3. Single layer clouds
    
    # 4. Including ice layer.
    
    exit('end check point')
    #------------------------
    #--normalize in-cloud height--
    #------------------------
    #print('--normalize in-cloud height--')
    
    
    #------------------------
    #--set the Ze and Height bins-- 
    #------------------------
    #print('--set the Ze and Height bins--')
    
    #------------------------
    #--count samples in Ze-Height space--
    #------------------------
    #print('--count samples in Ze-Height space--')
    
    # 1. all cases
    
    # 2. classify with LWP
    
    # 3. classify with Re


#------------------------
#--calculate normalized PDF in each height bin--
#------------------------
#print('--calculate normalized PDF in each height bin--')

#print(data_out.shape)
#print(data_dimn.values())
#a=[x for x in data_dimn.values()]
#print(a[1])
#print('-- This is the end of the code. --')
