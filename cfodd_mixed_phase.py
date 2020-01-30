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

import numpy as np
from hdf_eos_utils import read_hdf,require_var_info

#--input file--
print("--input file--")

#file_in="2007001005141_03607_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E02_F00.hdf"
#file_in="2007001005141_03607_CS_2B-CWC-RVOD_GRANULE_P1_R05_E02_F00.hdf"
file_in="2007001005141_03607_CS_ECMWF-AUX_GRANULE_P_R05_E02_F00.hdf"

#--extract data from input--
print("--extract data from input--")

variables=["Temperature","Pressure","Specific_Humidity"]
data_out,data_dimn=read_hdf(file_in,variables[0])

var_info=require_var_info(file_in)

exit("end check point")

#--conditional sampling--
print("--conditional sampling--")

# 1. Tctop <0.0 [Celcius] 

# 2. Liquid cloud top

# 3. Single layer clouds

# 4. Including ice layer.

#--normalize in-cloud height--
print("--normalize in-cloud height--")


#--set the Ze and Height bins-- 
print("--set the Ze and Height bins--")

#--count samples in Ze-Height space--
print("--count samples in Ze-Height space--")

# 1. all cases

# 2. classify with LWP

# 3. classify with Re


#--calculate normalized PDF in each height bin--
print("--calculate normalized PDF in each height bin--")

#print(data_out.shape)
#print(data_dimn.values())
#a=[x for x in data_dimn.values()]
#print(a[1])
#print("-- This is the end of the code. --")
