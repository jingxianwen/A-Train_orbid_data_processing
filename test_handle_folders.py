import os
import pathlib
import timeit
import glob
import shutil 

# os.getcwd()     : get current directory
# os.chdir()      : change directory
# os.listdir()    : list directories
# os.mkdir()      : make new directory
# os.rename('old','new') : rename directory or file
# os.remove()     : remove (delete) directory or file
# os.rmdir()      : remove empty directory
# shutil.rmtree   : remove non-empty directory

# os.path.exists() : check path existance

path="/Volumes/WD2T_1/2B-GEOPROF/2007/001/"
print(os.path.exists(path))
ig="03608"
file_geo=glob.glob(path+'*_'+str(ig)+'_*.hdf')
print(len(file_geo))
#print(os.path.exists(path+'*_'+str(ig)+'_*.hdf'))
#print(os.path.exists(file_geo[0]))

#- extract string from a file name
grans=[]
for f in os.listdir(path):
   grans.append(f[14:19])
print(grans)

#print(f[0][14:19])
#folders=os.scandir(path)
#for f in folders:
#   print(f)
