#=====================================================
#
#=====================================================
# os
import os

#import netCDF4
from netCDF4 import Dataset as netcdf_dataset

# matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.colors as colors

# numpy
import numpy as np

# scipy
from scipy import stats

#------------------------
#-- creat Ze vs T bins-- 
#------------------------

num_zebin=25
zebnd=np.linspace(-30.,20.,num_zebin+1)
num_tcbin=20
tcbnd=np.linspace(-40.,0.,num_tcbin+1)

cnt_samp_N=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_S=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
pdf_samp_N=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd
pdf_samp_S=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd

#------------------------
#-- open and read file --
#------------------------
file1=open('cnt_cld_NH.txt','r')
file2=open('cnt_cld_SH.txt','r')

data=file1.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_N=np.array(data_dig).reshape(num_tcbin,num_zebin)

data=file2.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_S=np.array(data_dig).reshape(num_tcbin,num_zebin)

#-- calculate PDF--
for ir in range(num_tcbin):
   pdf_samp_N[ir,:]=np.float32(cnt_samp_N[ir,:])/sum(cnt_samp_N[ir,:])*100.
   pdf_samp_S[ir,:]=np.float32(cnt_samp_S[ir,:])/sum(cnt_samp_S[ir,:])*100.

#print(pdf_samp_S)
#print(pdf_samp_N)

#exit()

# make the plot
fig=plt.figure(figsize=(10,6))
ax1=fig.add_axes([0.1,0.2,0.4,0.4])
ax2=fig.add_axes([0.6,0.2,0.4,0.4])

yloc=tcbnd[0:-1]
xloc=zebnd[0:-1]

cnlevels=np.linspace(0,20,21)

cntr1=ax1.contourf(xloc[:],yloc[:],pdf_samp_N,cmap="jet",levels=cnlevels,origin="lower")
ax1.set_title("Northern Hemisphere",fontsize=12)
ax1.set_xlabel("Ze (dBz)",fontsize=12)
ax1.set_ylabel("T_Ctop (c)",fontsize=12)
#ax1.set_yticks(yloc[:])
#ax1.set_yticklabels(labels=bands) #,rotation=-45)
#ax1.yaxis.grid(color='gray', linestyle=':')
fig.colorbar(cntr1, ax=ax1)
#ax1.set_ylim(0.1,13.0)

cntr2=ax2.contourf(xloc[:],yloc[:],pdf_samp_S,cmap="jet",levels=cnlevels,origin="lower")
ax2.set_title("Southern Hemisphere",fontsize=12)
ax2.set_xlabel("Ze (dBz)",fontsize=12)
ax2.set_ylabel("T_Ctop (c)",fontsize=12)
#ax1.set_yticks(yloc[:])
#ax1.set_yticklabels(labels=bands) #,rotation=-45)
#ax1.yaxis.grid(color='gray', linestyle=':')
fig.colorbar(cntr2, ax=ax2)
#ax1.set_ylim(0.1,13.0)

#plt.savefig(figure_name+".png")
plt.show()

exit()
