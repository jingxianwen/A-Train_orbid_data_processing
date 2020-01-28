# read a single granule HDF file.

import numpy as np
#from pyhdf.SD import SD, SDC, SDAttr
import pyhdf.SD

#========================================================================
# Introduction for reading data from a HDF-EOS file -->
   #data_file="2007001005141_03607_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E02_F00.hdf"
# 1. open data 
   #f=SD(data_file,SDC.READ)
# 2. select variable   
   #H=f.select("Height")   #![read a selected variable as a SDS object]
# 3. get data & information from the variable   
   #H_data=H.get())        #![get the data from the selected variable]
   #H_dimn=H.dimensions()) #![a dictionary describing of all the dataset dimensions]
   #H_info=H.info())       #![get (name, rank, dim lengths, data type, # of attrs]
   #H_attr=H.attributes()) #![a dictionary describing every attributes]
   #H_dml1=H.dim(0).length()) #![get the length of the 1st dimension]
   #H_dml2=H.dim(1).length()) #![get the length of the 2nd dimension]
#========================================================================

#--
data_file="2007001005141_03607_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E02_F00.hdf"
f=SD(data_file,SDC.READ)

H=f.select("Height")  # read a selected variable as a SDS object
H_data=H.get() 

print("-- This is the end of the code. --")
