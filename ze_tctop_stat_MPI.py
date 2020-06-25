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
from hdf_eos_utils import * #read_hdf,require_sd_info_hdf,require_vs_info_hdf

#------------------------
#--input file location--
#------------------------
print('--input file location--')

data_home='/Volumes/WD2T_1/'
path_GEO=data_home+'2B-GEOPROF/'
path_EC=data_home+'ECMWF-AUX.P_R05/'
path_CCL=data_home+'2B-CLDCLASS-LIDAR_P1_R05/'
path_MOD=data_home+'MODIS-AUX/'

#------------------------
#-- creat Ze vs T bins-- 
#------------------------
num_zebin=25
zebnd=np.linspace(-30.,20.,num_zebin+1)
num_tcbin=20
tcbnd=np.linspace(-40.,0.,num_tcbin+1)

cnt_samp_N1=np.zeros((2,num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_N2=np.zeros((2,num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_N3=np.zeros((2,num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_S1=np.zeros((2,num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_S2=np.zeros((2,num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_S3=np.zeros((2,num_tcbin,num_zebin),dtype=np.int64) # counted number of samples

#------------------------
#--loop granules-- 
#------------------------
print('--loop granules--')
#rng_gran=range(3607,3623)
years = ["2007"]
ndays = 365

for iyr in years:
  for iday_0 in range(ndays):
    iday=iday_0+1
    path_EC_now=path_EC+iyr+"/"+str(iday).zfill(3)+"/"
    path_GEO_now=path_GEO+iyr+"/"+str(iday).zfill(3)+"/"
    path_CCL_now=path_CCL+iyr+"/"+str(iday).zfill(3)+"/"
    #path_MOD_now=path_MOD+iyr+"/"+str(iyr).zfill(3)+"/"
    print('---day ',iday)

    #- check path existance 
    if not os.path.exists(path_EC_now):
        print('Path not found: ',path_EC_now)
        continue
    if not os.path.exists(path_GEO_now):
        print('Path not found: ',path_GEO_now)
        continue
    if not os.path.exists(path_CCL_now):
        print('Path not found: ',path_CCL_now)
        continue

    #- get granual index under each directory
    grans=[]
    for fi in os.listdir(path_GEO_now):
        grans.append(fi[14:19])

    for ig in grans:
        print(ig)
        file_ecmwf=glob.glob(path_EC_now+'*_'+str(ig)+'_*.hdf')
        file_geo=glob.glob(path_GEO_now+'*_'+str(ig)+'_*.hdf')
        file_ccl=glob.glob(path_CCL_now+'*_'+str(ig)+'_*.hdf')
        #file_mod=glob.glob(path_MOD+'*'+str(ig)+'_*')
       #- check file existance
        if len(file_ecmwf)==0 or len(file_ecmwf)>1: 
            print('NOT FOUND or TWO MANY: ',ig,' ',file_ecmwf)
            continue
        if len(file_geo)==0 or len(file_ecmwf)>1: 
            print('NOT FOUND or TWO MANY: ',ig,' ',file_geo)
            continue
        if len(file_ccl)==0 or len(file_ecmwf)>1: 
            print('NOT FOUND or TWO MANY: ',ig,' ',file_ccl)
            continue
        #if len(file_mod)==0 or len(file_ecmwf)>1: 
        #    print('NOT FOUND or TWO MANY: ',ig,' ',file_mod)
        #    break
        #------------------------
        #--extract data from input--
        #------------------------
        #print('--extract data from input--')
        #require_vs_info_hdf(file_geo[0])
      # from 2B-GEOPROF 
        ze,dimsz = read_sd_hdf(file_geo[0],"Radar_Reflectivity")
        num_pix  = dimsz[0]
        num_lev  = dimsz[1]
        ze       = np.ma.masked_where(ze==-999, ze * 0.01) #mask NaN and clear layer.
        #cld_msk,dimsz=read_sd_hdf(file_geo[0],"CPR_Cloud_mask")
        height,dimsz = read_sd_hdf(file_geo[0],"Height")
        height       = height * 0.001   # meter to km
        landsea_flag = read_vd_hdf(file_geo[0],"Navigation_land_sea_flag",num_pix)
        landsea_flag = landsea_flag.reshape((num_pix))
        surfbin      = read_vd_hdf(file_geo[0],"SurfaceHeightBin",num_pix)
        surfbin      = surfbin.reshape((num_pix))
        lat          = read_vd_hdf(file_geo[0],"Latitude",num_pix)
        lat          = lat.reshape((num_pix))
        #print(lat)
        #exit()
        #print(surfbin.shape)
        #print(type(surfbin[0,0]))
        #exit()

      # from 2B-CLDCLASS
        cld_phase,dimsz = read_sd_hdf(file_ccl[0],"CloudPhase")
        #print(dimsz)
        #exit()
        q_cld_phase,dimsz = read_sd_hdf(file_ccl[0],"CloudPhaseConfidenceLevel")
        #print(dimsz)
        #exit()
        cld_type,dimsz = read_sd_hdf(file_ccl[0],"CloudLayerType")
        #print(dimsz)
        #exit()
        q_cld_type,dimsz = read_sd_hdf(file_ccl[0],"CloudTypeQuality")
        #print(dimsz)
        #exit()
        cld_lay_top,dimsz = read_sd_hdf(file_ccl[0],"CloudLayerTop")
        #print(dimsz)
        #exit()
        cld_lay_base,dimsz = read_sd_hdf(file_ccl[0],"CloudLayerBase")
        #print(dimsz)
        #exit()
        n_cldlay = read_vd_hdf(file_ccl[0],"Cloudlayer",num_pix)

      # from ECMWF-AUX
        tair,dimsz = read_sd_hdf(file_ecmwf[0],"Temperature")
        tair=np.ma.masked_where(tair==-999,tair-273.15) #mask NaN, else Kelvin to Celsius.
    
        #exit('end check point')
        
        #------------------------
        #--conditional sampling--
        #------------------------
        #print('--conditional sampling--')

        ## 
        ## >> STEP 1: set sampling conditions  
        ##

        # a. Single layer clouds
        n_cldlay_flag  = n_cldlay.ravel()==1 # Note n_cldlay need to be raveled 
                                             # (from [num_pix,1] to [num_pix])
        # b. Cloud type is one of: Ac, As, Cu, Sc, and St.
        cld_type_flag  = (cld_type[:,0] >=2) * (cld_type[:,0] <=6)  # cld type list: 
                                             # 1, Ci; 2, As; 3, Ac; 4, St; 5, Sc;
                                             # 6, Cu; 7, Ns; 8, Dc.
        # c. Cloud phase is mixed 
        cld_phase_flag = cld_phase[:,0] == 2 # cld phase list: 
                                             # 1, ice; 2, mixed; 3, liquid.
        # d. confidence control 
        q_cld_phase_flag = q_cld_phase[:,0] >5

        # e. not precipitation near surface (ze < -10. dBz) (using FANCY indexing)
        surf_precp_flag1 = ze[range(0,num_pix),surfbin-4] < -15. #* ze[range(0,num_pix),surfbin-5] < -15.
        surf_precp_flag2 = ze[range(0,num_pix),surfbin-5] < -15. #* ze[range(0,num_pix),surfbin-5] < -15.
        surf_precp_flag = surf_precp_flag1 * surf_precp_flag2
        ##
        ## >> STEP 2: sample the data 
        ##

        samp_flag = n_cldlay_flag \
                  * cld_type_flag \
                  * cld_phase_flag \
                  * q_cld_phase_flag \
                  * surf_precp_flag

        ze_samp       = ze[samp_flag,:]
        height_samp   = height[samp_flag,:]
        tair_samp     = tair[samp_flag,:]
        cld_base_samp = cld_lay_base[:,0][samp_flag]
        cld_top_samp  = cld_lay_top[:,0][samp_flag]
        lat_samp      = lat[samp_flag]
        landsea_flag_samp = landsea_flag[samp_flag]
   
        n_sampl       = ze_samp.shape[0]
        #print(n_sampl)


        for ism in range(0,n_sampl):
           clevs = (height_samp[ism,:] > cld_base_samp[ism]) * \
                      (height_samp[ism,:] < cld_top_samp[ism])
           #print(cld_base_samp[ism],cld_top_samp[ism])
           if not any(clevs): 
              continue
           ze_max   = ze_samp[ism,clevs].max()
           t_ctop = tair_samp[ism,clevs][0]
           
           # locate in the t_ctop-ze_max domain
           #ize = min(max(zebnd[zebnd<=ze_max].size-1,0),num_zebin-1)
           #itc = min(max(tcbnd[tcbnd<=t_ctop].size-1,0),num_tcbin-1)
           ize = zebnd[zebnd<=ze_max].size-1
           itc = tcbnd[tcbnd<=t_ctop].size-1
           if ize > num_zebin-1 or ize <  0: # if ze >20. or ze<-30.
              continue
           if itc > num_tcbin-1 or itc <  0: # if tc >0. or tc<-40.
              continue

           # land/sea index (landsea_flag = 1, land; 2, ocean; 3, coast) 
           if landsea_flag_samp[ism] == 1:
              isfc=0
           elif landsea_flag_samp[ism] == 2:
              isfc=1             
           else:
              continue

           # count number of clouds
           if lat_samp[ism] >= 0. and lat_samp[ism] <30.:
              cnt_samp_N1[isfc,itc,ize] = cnt_samp_N1[isfc,itc,ize]+1
           elif lat_samp[ism] >= 30. and lat_samp[ism] <60.:
              cnt_samp_N2[isfc,itc,ize] = cnt_samp_N2[isfc,itc,ize]+1
           elif lat_samp[ism] >= 60. :
              cnt_samp_N3[isfc,itc,ize] = cnt_samp_N3[isfc,itc,ize]+1
           elif lat_samp[ism] >= -30. and lat_samp[ism] <0.:
              cnt_samp_S1[isfc,itc,ize] = cnt_samp_S1[isfc,itc,ize]+1
           elif lat_samp[ism] >= -60. and lat_samp[ism] <-30.:
              cnt_samp_S2[isfc,itc,ize] = cnt_samp_S2[isfc,itc,ize]+1
           elif lat_samp[ism] <-60.:
              cnt_samp_S3[isfc,itc,ize] = cnt_samp_S3[isfc,itc,ize]+1
           #print(ze_max)
           #print(t_ctop)
           #print(itc,ize)
           #print(tcbnd[itc:itc+2],zebnd[ize:ize+2])
           #print(ze_samp[ism,clevs])
           #exit()

#==============================================
fout=open('cnt_cld_lnd_NH_0-30.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_N1[0,il,:])+'\n')
fout.close()

fout=open('cnt_cld_lnd_NH_30-60.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_N2[0,il,:])+'\n')
fout.close()

fout=open('cnt_cld_lnd_NH_60-90.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_N3[0,il,:])+'\n')
fout.close()

fout=open('cnt_cld_lnd_SH_0-30.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_S1[0,il,:])+'\n')
fout.close()

fout=open('cnt_cld_lnd_SH_30-60.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_S2[0,il,:])+'\n')
fout.close()

fout=open('cnt_cld_lnd_SH_60-90.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_S3[0,il,:])+'\n')
fout.close()

#--------
fout=open('cnt_cld_ocn_NH_0-30.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_N1[1,il,:])+'\n')
fout.close()

fout=open('cnt_cld_ocn_NH_30-60.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_N2[1,il,:])+'\n')
fout.close()

fout=open('cnt_cld_ocn_NH_60-90.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_N3[1,il,:])+'\n')
fout.close()

fout=open('cnt_cld_ocn_SH_0-30.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_S1[1,il,:])+'\n')
fout.close()

fout=open('cnt_cld_ocn_SH_30-60.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_S2[1,il,:])+'\n')
fout.close()

fout=open('cnt_cld_ocn_SH_60-90.txt','w')
for il in range(num_tcbin):
  fout.write(str(cnt_samp_S3[1,il,:])+'\n')
fout.close()

#------------------------
#--calculate normalized PDF in each height bin--
#------------------------
#print('--calculate normalized PDF in each height bin--')

#print(data_out.shape)
#print(data_dimn.values())
#a=[x for x in data_dimn.values()]
#print(a[1])
#print('-- This is the end of the code. --')
