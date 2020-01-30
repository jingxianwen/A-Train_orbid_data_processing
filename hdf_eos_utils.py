
import numpy as np
from pyhdf.SD import SD, SDC, SDAttr

#========================================================================
# Introduction for reading data from a HDF-EOS file -->
   #data_file="2007001005141_03607_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E02_F00.hdf"
# 1. open data 
   #$f=SD(data_file,SDC.READ)
   # inquiry information of the file-->
   # a) f.info()     #![get number of variables and number of attributes]
   # b) f.datasets() #![a dictionary describing every variable]
   # c) f.attributes() #![get global attributes]
# 2. select variable   
   #$H=f.select("Height")   #![read a selected variable as a SDS object]
# 3. get data & information from the variable   
   #$H_data=H.get()        #![get the data from the selected variable]
   #$H_dimn=H.dimensions() #![a dictionary describing of all the dataset dimensions]
   #$H_info=H.info()       #![get (name, rank, dim lengths, data type, # of attrs]
   #$H_attr=H.attributes() #![a dictionary describing every attributes]
   #$H_dml1=H.dim(0).length() #![get the length of the 1st dimension]
   #$H_dml2=H.dim(1).length() #![get the length of the 2nd dimension]
#========================================================================

def read_hdf(file_in,var_in):
    '''Read data stored as a variable in the input HDF-EOS file.'''
    '''Currently coded for vertical profile of A-Train granule. '''
    '''Inputs are the file path and the required variable name. '''
    '''Outputs are the data (numpy array) and dimentions (dict).'''

    #--information from input file--
    f=SD(file_in,SDC.READ)

    var=f.select(var_in)
    var_data=var.get()
    var_dimn=var.dimensions()

    return var_data,var_dimn

def require_var_info(file_in):
    '''Print and Return variable names and dimentions in a HDF-EOS file'''
    #--information from input file--
    f=SD(file_in,SDC.READ)
    var_info=f.datasets()
    print("--Variables in ",file_in,"-->")
    for name,value in var_info.items():
        print("    ",name,": ",value)
    return var_info

