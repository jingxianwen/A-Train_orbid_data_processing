#===============================================================
# This code compute the occurrance of ice and mixed-phase clouds
# as a function of cloud top temperature and column maximum Ze (
# Zhang et al., 2018, ACP, 18, 4317-4327. 
#
# Required input (to be revised):
#  2B-GEOPROF -->
#   1) Radar_Reflectivity
#   2) Height
#  ECWMF-AUX -->
#   3) Temperature (air temperature)
#  2B-CLDCLASS-LIDAR -->
#   4) CloudPhase (1:ice, 2:mixed, 3: liquid)
#   5) CloudLayerTop (cloud top height) 
#   6) CloudLayerBase (cloud base height) 
#   7) Cloudlayer (numbe of cloud layers)
#xx  8) supercooled water layer top
#xx MODIS-1KM-AUX or MODIS-5KM-AUX -->
#xx  9) LWP
#xx  10) Cloud top droplet effective radius
#
# Methodology: 
#   1) Ice and mixed-phase (CloudPhase=1&2) and single layer 
#      clouds (Cloudlayer=1) are selected for analysis.
#   2) For each selected profile, its location in the Ze_max-
#      cloud_top_temperature axes is decided according to its
#      column maximum Ze and cloud top temperature.
#   3) PDF is computed for each cloud_top_temperature bin from
#      the counte of samples. 
#   4) The PDF derived is visualized as contour plot as Fig. 3
#      in Zhang et al., 2018.
#xx   NOTE: the first four layers above surface is preliminarily 
#xx         discarded due to surface clutter.
# History:
#   1) JAN 30, 2020. First created. Xianwen.
#   2) Feb 12, 2020. Add purpose and methodology. Xianwen.
#================================================================

import os
import glob
import numpy as np
from hdf_eos_utils import read_hdf_SD,require_SD_info_hdf,read_hdf_VD,require_VD_info_hdf

#------------------------
#-- creat Ze vs T bins-- 
#------------------------
num_zebin=25
zebnd=np.linspace(-30,20,num_zebin+1)
num_tbin=20
tbnd=np.linspace(-40,0,num_tbin+1)

cnt_sampl=np.zeros((num_tbin,num_zebin)) # counted number of samples
pdf_sampl=np.zeros((num_tbin,num_zebin)) # PDF of cnt_sampl for each tbnd

#------------------------
#-- number of cases-- 
#------------------------
tot_all=np.int64(0)
tot_cloud=np.int64(0)
tot_cloud_1_l=np.int64(0)
tot_cloud_1_l_icemix=np.int64(0)
tot_sampl=np.int64(0)

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
    print("granule=",ig)
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

  # from 2B-GEOPROF 
    ze,dimsz=read_hdf_SD(file_geo[0],"Radar_Reflectivity")
    num_pix=dimsz[0]
    num_lev=dimsz[1]
    #cld_msk,dimsz=read_hdf_SD(file_geo[0],"CPR_Cloud_mask")
    #sfc_loc,dimsz=read_hdf_VD(file_geo[0],"SurfaceHeightBin")
    height,dimsz=read_hdf_SD(file_geo[0],"Height")

  # from 2B-CLDCLASS
    cphase,dimsz=read_hdf_SD(file_ccl[0],"CloudPhase")
    ctophgt,dimsz=read_hdf_SD(file_ccl[0],"CloudLayerTop")
    cbasehgt,dimsz=read_hdf_SD(file_ccl[0],"CloudLayerBase")
    ncldlay,dimsz=read_hdf_VD(file_ccl[0],"Cloudlayer")

  # from ECMWF-AUX
    tair,dimsz=read_hdf_SD(file_ecmwf[0],"Temperature")
  
    tot_all=tot_all+num_pix

    #------------------------
    #--preprocess the data--
    #------------------------
    #..convert valid range from 1-125 to 0-124, and set the cut point due to clutter.
    #sfc_cut=np.where((sfc_loc>=1) & (sfc_loc<=125),sfc_loc-1-4,sfc_loc)
    #..convert temperature from Kelvin to Celsius.
    tair=np.where(tair>-999,tair-273.15,tair) #Kelvin to Celsius.
    height[:,:]=height[:,:]*0.001 # m to km
    ze=np.where((ze>-4000.) & (ze<5000.),ze*0.01,ze) #scale back from 100.

    for iprof in range(0,num_pix):
        
    #------------------------
    #--conditional sampling--
    #------------------------
        #print('--conditional sampling--')

    # 0. Identify cloud top and bottom layer
      #..use reflectivity and cloud_mask
        #ctop_lev=min( np.min(np.where( (ze[ig,0:sfc_cut[ig]]>-30.) & \
        #        (ze[ig,0:sfc_cut[ig]]<20.)),\
        #              np.min(np.where(cld_mask[ig,0:sfc_cut[ig]]>=20)))
        #cbot_lev=max( np.min(np.where( (ze[ig,0:sfc_cut[ig]]>-30.) & \
        #        (ze[ig,0:sfc_cut[ig]]<20.)),\
        #              np.min(np.where(cld_mask[ig,0:sfc_cut[ig]]>=20)))

    # 1. Is single layer cloud?
       if ncldlay[iprof] ==1:
           #is_sgl=True
           tot_sgl=tot_sgl+1
           ctop_id=np.max(np.where(height[iprof,:]>ctophgt[iprof,0]))
           cbase_id=np.max(np.where(height[iprof,:]>cbasehgt[iprof,0]))+1
    # 2. Is mixed or ice cloud? 
           if (cphase[iprof,0]==1 or cphase[iprof,0]==2):
               #is_icemix=True
               tot_sgl_icemix=tot_sgl_icemix+1
               ze_max=np.max(ze[iprof,ctop_id:cbase_id+1])
               Tctop=tair[iprof,ctop_id]
    # 3. locate the profile in Ze_max-Ctop_T axes               
               if (ze_max >=min(zebnd))&(ze_max <max(zebnd))&\
                  (Tctop>=min(tbnd))&(Tctop<max(tbnd)):
                  tot_sampl=tot_sampl+1
                  loc_zemax= np.max(np.where(zebnd[:] <= ze_max))
                  loc_tctop= np.max(np.where(tbnd[:] <= Tctop))
                  cnt_sampl[loc_tctop,loc_zemax]=cnt_sampl[loc_tctop,loc_zemax]+1
           #else:
           #    is_icemix=False
       #else: 
       #    is_sgl=False
       #    is_coldtop=False
       #    is_icemix=False


#print(cnt_sampl)
    
#exit('end check point')
#------------------------
#--normalize in-cloud height--
#------------------------
#print('--normalize in-cloud height--')

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
