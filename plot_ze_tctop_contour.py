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

cnt_samp_N1=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_N2=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_N3=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_S1=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_S2=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
cnt_samp_S3=np.zeros((num_tcbin,num_zebin),dtype=np.int64) # counted number of samples
pdf_samp_N1=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd
pdf_samp_N2=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd
pdf_samp_N3=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd
pdf_samp_S1=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd
pdf_samp_S2=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd
pdf_samp_S3=np.zeros((num_tcbin,num_zebin),dtype=np.float32) # PDF of cnt_sampl for each tcbnd

#------------------------
#-- open and read file --
#------------------------
fileN1=open('cnt_cld_ocn_NH_0-30.txt','r')
fileN2=open('cnt_cld_ocn_NH_30-60.txt','r')
fileN3=open('cnt_cld_ocn_NH_60-90.txt','r')
fileS1=open('cnt_cld_ocn_SH_0-30.txt','r')
fileS2=open('cnt_cld_ocn_SH_30-60.txt','r')
fileS3=open('cnt_cld_ocn_SH_60-90.txt','r')

data=fileN1.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_N1=np.array(data_dig).reshape(num_tcbin,num_zebin)

data=fileN2.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_N2=np.array(data_dig).reshape(num_tcbin,num_zebin)

data=fileN3.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_N3=np.array(data_dig).reshape(num_tcbin,num_zebin)

data=fileS1.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_S1=np.array(data_dig).reshape(num_tcbin,num_zebin)

data=fileS2.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_S2=np.array(data_dig).reshape(num_tcbin,num_zebin)

data=fileS3.read()
data_n=data.replace('[',' ')
data_nn=data_n.replace(']',' ')
data_list=data_nn.split()
data_dig=[]
for num in data_list:
   data_dig.append(int(num))
cnt_samp_S3=np.array(data_dig).reshape(num_tcbin,num_zebin)

#-- calculate PDF--
for ir in range(num_tcbin):
   pdf_samp_N1[ir,:]=np.float32(cnt_samp_N1[ir,:])/sum(cnt_samp_N1[ir,:])*100.
   pdf_samp_N2[ir,:]=np.float32(cnt_samp_N2[ir,:])/sum(cnt_samp_N2[ir,:])*100.
   pdf_samp_N3[ir,:]=np.float32(cnt_samp_N3[ir,:])/sum(cnt_samp_N3[ir,:])*100.
   pdf_samp_S1[ir,:]=np.float32(cnt_samp_S1[ir,:])/sum(cnt_samp_S1[ir,:])*100.
   pdf_samp_S2[ir,:]=np.float32(cnt_samp_S2[ir,:])/sum(cnt_samp_S2[ir,:])*100.
   pdf_samp_S3[ir,:]=np.float32(cnt_samp_S3[ir,:])/sum(cnt_samp_S3[ir,:])*100.

#print(pdf_samp_S)
#print(pdf_samp_N)

#exit()

# make the plot
fig=plt.figure(figsize=(10,6))
ax1=fig.add_axes([0.1,0.5,0.25,0.3])
ax2=fig.add_axes([0.4,0.5,0.25,0.3])
ax3=fig.add_axes([0.7,0.5,0.25,0.3])
ax4=fig.add_axes([0.1,0.1,0.25,0.3])
ax5=fig.add_axes([0.4,0.1,0.25,0.3])
ax6=fig.add_axes([0.7,0.1,0.25,0.3])

yloc=tcbnd[0:-1]
xloc=zebnd[0:-1]

cnlevels=np.linspace(0,20,21)

cntr1=ax1.contourf(xloc[:],yloc[:],pdf_samp_N3,cmap="jet",levels=cnlevels,origin="lower", \
                   extend = 'max')
ax1.set_title("60-90N",fontsize=12)
#ax1.set_xlabel("Ze (dBz)",fontsize=12)
ax1.set_ylabel("T_Ctop (c)",fontsize=12)
#ax1.set_yticks(yloc[:])
#ax1.set_yticklabels(labels=bands) #,rotation=-45)
#ax1.yaxis.grid(color='gray', linestyle=':')
#fig.colorbar(cntr1, ax=ax1)
#ax1.set_ylim(0.1,13.0)

cntr2=ax2.contourf(xloc[:],yloc[:],pdf_samp_N2,cmap="jet",levels=cnlevels,origin="lower", \
                   extend = 'max')
ax2.set_title("30-60N",fontsize=12)
#ax2.set_xlabel("Ze (dBz)",fontsize=12)
#ax2.set_ylabel("T_Ctop (c)",fontsize=12)
#fig.colorbar(cntr2, ax=ax2)

cntr3=ax3.contourf(xloc[:],yloc[:],pdf_samp_N1,cmap="jet",levels=cnlevels,origin="lower", \
                   extend = 'max')
ax3.set_title("0-30N",fontsize=12)
#ax3.set_xlabel("Ze (dBz)",fontsize=12)
#ax3.set_ylabel("T_Ctop (c)",fontsize=12)
cbar1=fig.colorbar(cntr3, ax=ax3, extend='both')

cntr4=ax4.contourf(xloc[:],yloc[:],pdf_samp_S3,cmap="jet",levels=cnlevels,origin="lower", \
                   extend = 'max')
ax4.set_title("60-90S",fontsize=12)
ax4.set_xlabel("Ze (dBz)",fontsize=12)
ax4.set_ylabel("T_Ctop (c)",fontsize=12)
#fig.colorbar(cntr4, ax=ax4)

cntr5=ax5.contourf(xloc[:],yloc[:],pdf_samp_S2,cmap="jet",levels=cnlevels,origin="lower", \
                   extend = 'max')
ax5.set_title("30-60S",fontsize=12)
ax5.set_xlabel("Ze (dBz)",fontsize=12)
#ax5.set_ylabel("T_Ctop (c)",fontsize=12)
#fig.colorbar(cntr5, ax=ax5)

cntr6=ax6.contourf(xloc[:],yloc[:],pdf_samp_S1,cmap="jet",levels=cnlevels,origin="lower", \
                   extend = 'max')
ax6.set_title("0-30S",fontsize=12)
ax6.set_xlabel("Ze (dBz)",fontsize=12)
#ax6.set_ylabel("T_Ctop (c)",fontsize=12)
car2=fig.colorbar(cntr6, ax=ax6)

#plt.savefig(figure_name+".png")
plt.show()

exit()
