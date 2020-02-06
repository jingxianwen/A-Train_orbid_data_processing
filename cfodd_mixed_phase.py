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
    #cld_msk,dimsz=read_hdf_SD(file_geo[0],"CPR_Cloud_mask")
    #sfc_loc,dimsz=read_hdf_VD(file_geo[0],"SurfaceHeightBin")
    height,dimsz=read_hdf_SD(file_geo[0],"Height")

  # from 2B-CLDCLASS
    #sfc_loc,dimsz=read_hdf(file_geo,"CPR_Cloud_mask")
    cphase,dimsz=read_hdf_SD(file_ccl[0],"CloudPhase")
    ctophgt,dimsz=read_hdf_SD(file_ccl[0],"CloudLayerTop")
    cbasehgt,dimsz=read_hdf_SD(file_ccl[0],"CloudLayerBase")
    ncldlay,dimsz=read_hdf_VD(file_ccl[0],"Cloudlayer")
    #print(ncldlay.shape)

  # from ECMWF-AUX
    tair,dimsz=read_hdf_SD(file_ecmwf[0],"Temperature")
    #tair=np.ma.masked_where(tair<=-999,tair-273.15) #mask NaN, else Kelvin to Celsius.
  
    #exit('end check point')
    
    #------------------------
    #--preprocess the data--
    # mask invalide pixels
    #------------------------
    #..convert valid range from 1-125 to 0-124, and set the cut point due to clutter.
    #sfc_cut=np.where((sfc_loc>=1) & (sfc_loc<=125),sfc_loc-1-4,sfc_loc)
    #..convert temperature from Kelvin to Celsius.
    tair=np.where(tair<=-999,tair-273.15,tair) #Kelvin to Celsius.
    height[:,:]=height[:,:]*0.001 # m to km

    layind=range(0,num_lev)

    for iprof in range(0,200):
        #if sfc_cut[iprof] not in range(0,125): 
        #    break # if wrong surface, jump to next iteration  
        #masklay=np.where(layind>=sfc_clut_cut[ig],1,0)
        #ze_tmp=np.ma.masked_array(ze[ig,:],mask=masklay)
        #tair_tmp=np.ma.masked_array(tair[ig,:],mask=masklay)
    #------------------------
    #--conditional sampling--
    #------------------------
        #print('--conditional sampling--')

    # 1. Identify cloud top and bottom layer
      #..use reflectivity and cloud_mask
        #ctop_lev=min( np.min(np.where( (ze[ig,0:sfc_cut[ig]]>-30.) & (ze[ig,0:sfc_cut[ig]]<20.)),\
        #              np.min(np.where(cld_mask[ig,0:sfc_cut[ig]]>=20)))
        #cbot_lev=max( np.min(np.where( (ze[ig,0:sfc_cut[ig]]>-30.) & (ze[ig,0:sfc_cut[ig]]<20.)),\
        #              np.min(np.where(cld_mask[ig,0:sfc_cut[ig]]>=20)))
      #..use cloud phase 

    # 1. Is single layer cloud?
       if ncldlay[iprof] ==1:
           ctop_id=np.min(np.where(height[iprof,:]<ctophgt[iprof,0]))
           cbase_id=np.max(np.where(height[iprof,:]>cbasehgt[iprof,0]))
           is_sgl=True
    # 2. Is Tctop <0.0 [Celcius]? 
           if tair[iprof,ctop_id] <0.0:
               is_coldtop=True
    # 3. Is mixed or ice cloud? 
               if (cphase[iprof,0]==1 or cphase[iprof,0]==2):
                   ze_max=np.max(ze[iprof,ctop_id:cbase_id+1])
                   ctop
               else:
           else:
               is_coldtop=False
       else: 
           is_sgl=False
           is_coldtop=False

    
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
