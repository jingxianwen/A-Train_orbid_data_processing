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
from hdf_eos_utils import read_hdf,require_var_info_hdf

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
    #print('--extract data from input--')
    
    #var_info=require_var_info_hdf(file_ecmwf)
    
    #variables=['Temperature','Pressure','Specific_Humidity']
    #data_out,data_dimn=read_hdf(file_in,variables[0])
    #T_in,T_dimn=read_hdf(file_ecmwf,Temperature)
    #P_in,P_dimn=read_hdf(file_ecmwf,Temperature)
    
    #exit('end check point')
    
    #------------------------
    #--conditional sampling--
    #------------------------
    #print('--conditional sampling--')
    
    # 1. Tctop <0.0 [Celcius] 
    
    # 2. Liquid cloud top
    
    # 3. Single layer clouds
    
    # 4. Including ice layer.
    
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
