#========================================================================
# This code contains functions for reading/requiring infor from A-Train HDF files.
# Functions contained: 
#   1. read_hdf(file_in,var_in)
#   2. require_var_info_hdf(file_in)
#========================================================================
import numpy as np

from pyhdf.HDF import *
from pyhdf.SD import *
from pyhdf.VS import *
from pyhdf.V import *

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

#=====================================================
def read_sd_hdf(file_in,var_in):
    '''Read data stored as a SD variable in input HDF-EOS file. '''
    '''Currently coded for vertical profile of A-Train granule. '''
    '''Inputs are the file path and the required variable name. '''
    '''Outputs are the data (numpy array) and dimentions(numpy).'''

    #--information from input file--
    f=SD(file_in,SDC.READ)
    var=f.select(var_in)
    var_data=var.get()
    var_data=np.float32(var_data)
    #print(var_data.dtype)
    var_dimn = np.fromiter(var.dimensions().values(), dtype=int)
    return var_data,var_dimn

#=====================================================
def read_vd_hdf(file_in,var_in,dimsz):
    '''Read data stored as a VD variable in input HDF-EOS file.'''
    '''Inputs are the file path and the required variable name.'''
    '''Outputs are the data (numpy array).                     '''

    #--information from input file--
    hdf  = HDF(file_in)
    vs   = hdf.vstart()
    vd   = vs.attach(var_in)
    var_data = np.array(vd.read(int(dimsz)))
    vd.detach()
    return var_data #,var_dimn

#=====================================================
def read_vd_hdf2(file_in,var_in):
    '''Read data stored as a VD variable in input HDF-EOS file.'''
    '''Inputs are the file path and the required variable name.'''
    '''Outputs are the data (numpy array).                     '''

    #--information from input file--
    hdf  = HDF(file_in)      # the HDF file
    vs   = hdf.vstart()      # initialize VS interface on HDF file
    ### vdinfo = vs.vdatainfo() # return info about all vdatas
    vd   = vs.attach(var_in) # open a vdata given its name
    dimsz = vd.inquire()[0]  # return 5 elements: 
                             #   1. # of records
                             #   2. interlace mode
                             #   3. list of vdata field names
                             #   4. size in bytes of the vdata record
                             #   5. name of the vdata
    var_data = np.array(vd.read(dimsz)) #read a number of records
    vd.detach()              # close the vdata
    vs.end()                 # terminate the vdata interface
    hdf.close()              # close the HDF file
    return var_data,dimsz

#=====================================================
def read_hdf_VD(file_in,var_in):
    '''Read Vdata sets (table, 1D) in the input HDF-EOS file.    '''
    '''Currently coded for surface variables of A-Train granule. '''
    '''Inputs are the file path and the required variable name.  '''
    '''Outputs are the data (numpy array) and dimentions(numpy). '''

    #--information from input file--
    f=HDF(file_in)
    vs=f.vstart()
    vd=vs.attach(var_in) #return var data from vs group
    var_data=np.array(vd[:]).ravel() #convert data into flatted ndarray
    #print(var_data.dtype)
    var_dimn=np.array(var_data.shape)
    return var_data,var_dimn

def require_SD_info_hdf(file_in):
    '''Print and Return SD variable names and dimentions in a HDF-EOS file'''
    #--information from input file--
    f=SD(file_in,SDC.READ)
    var_info=f.datasets()
    print("--Variables in ",file_in,"-->")
    for name,value in var_info.items():
        print("    ",name,": ",value)
    return var_info

#=====================================================
#def require_vs_info_hdf(file_in):
#    '''Print and Return VS variable names and dimentions in a HDF-EOS file'''
#    #--information from input file--
#    f=VS(file_in,VD.read)
#    var_info=f.fieldinfo()
#    print("--Variables in ",file_in,"-->")
#    for name,value in var_info.items():
#        print("    ",name,": ",value)
#    return var_info

#=====================================================
### get SD variable names ###
def HDFvars(File):
    """
    Extract variable names for an hdf file
    """
    # hdfFile = SD.SD(File, mode=1)
    hdfFile = SD(File, mode=1)
    dsets = hdfFile.datasets()
    k = []
    for key in dsets.keys():
        k.append(key)
    k.sort()
    hdfFile.end() # close the file
    return k

#=====================================================
#def describevg(refnum):
#    # Describe the vgroup with the given refnum.
#    # Open vgroup in read mode.
#    vg = v.attach(refnum)
#    print("----------------")
#    print("name:", vg._name, "class:",vg._class, "tag,ref:", vg._tag, vg._refnum)
#
#    # Show the number of members of each main object type.
#    print("members: ", vg._nmembers,)
#    print("datasets:", vg.nrefs(HC.DFTAG_NDG),)
#    print("vdatas:  ", vg.nrefs(HC.DFTAG_VH),)
#    print("vgroups: ", vg.nrefs(HC.DFTAG_VG))
#
#    # Read the contents of the vgroup.
#    members = vg.tagrefs()
#
#    # Display info about each member.
#    index = -1
#    for tag, ref in members:
#        index += 1
#        print("member index", index)
#        # Vdata tag
#        if tag == HC.DFTAG_VH:
#            vd = vs.attach(ref)
#            nrecs, intmode, fields, size, name = vd.inquire()
#            print("  vdata:",name, "tag,ref:",tag, ref)
#            print("    fields:",fields)
#            print("    nrecs:",nrecs)
#            vd.detach()
#        # SDS tag
#        elif tag == HC.DFTAG_NDG:
#            sds = sd.select(sd.reftoindex(ref))
#            name, rank, dims, type, nattrs = sds.info()
#            print("  dataset:",name, "tag,ref:", tag, ref)
#            print("    dims:",dims)
#            print("    type:",type)
#            sds.endaccess()
#
#        # VS tag
#        elif tag == HC.DFTAG_VG:
#            vg0 = v.attach(ref)
#            print("  vgroup:", vg0._name, "tag,ref:", tag, ref)
#            vg0.detach()
#        # Unhandled tag
#        else:
#            print("unhandled tag,ref",tag,ref)
#
#    # Close vgroup
#    vg.detach()


#filename="2007001005141_03607_CS_2B-CLDCLASS-LIDAR_GRANULE_P1_R05_E02_F00.hdf"
#--test get SD variable names--
#varnms=HDFvars(filename)
#print(varnms)

#--test get VS and VG variable info--
#hdf = HDF(filename)
#
## Initialize the SD, V and VS interfaces on the file.
#sd = SD(filename)
#vs = hdf.vstart()
#v  = hdf.vgstart()

#-- get Vdata info
#vsdatainfo=vs.vdatainfo()
#print(vsdatainfo)

#-- read Vdata
#vd=vs.attach("Latitude")
#lat=vd.read(10)

#while 1:
#  try:
#     lat.append(vd.read())
#  except:
#     pass 
#print(lat)

#vdata=VD.read(vs)
#print(vdata)

# Scan all vgroups in the file.
#ref = -1
#while 1:
#    try:
#        ref = v.getid(ref)
#        print (ref)
#    #except HDF4Error,msg:    # no more vgroup
#    except HDF4Error:    # no more vgroup
#        break
#    describevg(ref)

def require_VD_info_hdf(file_in):
    '''Print and Return VD variable names and dimentions in a HDF-EOS file'''
    #--information from input file--
    f=HDF(file_in)
    vs=f.vstart()
    var_info=vs.vdatainfo()
    print("--Variables in ",file_in,"-->")
    for item in var_info:
        print(item)
    return var_info

# end of file.
