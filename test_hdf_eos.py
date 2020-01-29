
import numpy as np
from hdf_eos_utils import read_hdf

#--input file--
#file_in="2007001005141_03607_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E02_F00.hdf"
#file_in="2007001005141_03607_CS_2B-CWC-RVOD_GRANULE_P1_R05_E02_F00.hdf"
file_in="2007001005141_03607_CS_ECMWF-AUX_GRANULE_P_R05_E02_F00.hdf"
variables=["Temperature","Pressure","Specific_Humidity"]

data_out,data_dimn=read_hdf(file_in,variables[0])

#print(data_out.shape)
#print(data_dimn.values())
#a=[x for x in data_dimn.values()]
#print(a[1])
#print("-- This is the end of the code. --")
