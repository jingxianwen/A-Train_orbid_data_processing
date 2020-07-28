#====================================================
#
#====================================================
# os
import os
#import netCDF4
from netCDF4 import Dataset as netcdf_dataset
# cartopy
import os
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
# matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.path as mpath
import matplotlib.colors as colors
# numpy
import numpy as np
# parameters
from get_parameters import *
# scipy
from scipy import stats

# data path
data_path="./precip_Arctic/"
file_name=data_path+"precip_statis_2x2.nc"

# read data
precp_file=netcdf_dataset(file_name,"r")
cnt_rn_cert=np.array(precp_file.variables["cnt_rain_cert"])
cnt_rn_poss=np.array(precp_file.variables["cnt_rain_poss"])
cnt_sn_cert=np.array(precp_file.variables["cnt_snow_cert"])
cnt_sn_poss=np.array(precp_file.variables["cnt_snow_poss"])
cnt_no_prec=np.array(precp_file.variables["cnt_noprecp"])
pre_rn_cert=np.array(precp_file.variables["pre_rain_cert"])
pre_rn_poss=np.array(precp_file.variables["pre_rain_poss"])
pre_sn_cert=np.array(precp_file.variables["pre_snow_cert"])
pre_sn_poss=np.array(precp_file.variables["pre_snow_poss"])
lat=np.array(precp_file.variables["lat"])
lon=np.array(precp_file.variables["lon"])
nlat=len(lat)
nlon=len(lon)

# calculate frequency and ratio
cnt_rn_tot = cnt_rn_cert + cnt_rn_poss
cnt_sn_tot = cnt_sn_cert + cnt_sn_poss
cnt_tot    = cnt_rn_tot  + cnt_sn_tot + cnt_no_prec

freq_rn=np.divide(cnt_rn_tot,cnt_tot,where= cnt_tot!=0)*100.
freq_sn=np.divide(cnt_sn_tot,cnt_tot,where= cnt_tot!=0)*100.
freq_pre=freq_rn+freq_sn
ratio_rn=np.divide(freq_rn,freq_pre,where= freq_pre!=0)
ratio_sn=np.divide(freq_sn,freq_pre,where= freq_pre!=0)

#plot 

pole='N'
imon=6
seasons=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
if pole is 'N':
   var_long_name="Arctic Prec Freq ("+seasons[imon]+")"
   figure_name="Arctic_Sea_Ice_contour_"+seasons[imon]+"_VIS_icealb"
elif pole is 'S':
   var_long_name="Antarctic Prec Freq ("+seasons[imon]+")"
   figure_name="Antarctic_Sea_Ice_contour_"+seasons[imon]+"_VIS_icealb"
units=" " #"Fraction"
#units=r"W/m$^2$"

if pole == "N":
    latbound1=np.min(np.where(lat[:]>50))
    latbound2=np.min(np.where(lat[:]>81))
elif pole == "S":
    latbound1=0
    latbound2=np.max(np.where(lat[:]<-50))+1

stats_rn=get_area_mean_min_max(ratio_rn[imon,latbound1:latbound2,:],lat[latbound1:latbound2])
stats_sn=get_area_mean_min_max(ratio_sn[imon,latbound1:latbound2,:],lat[latbound1:latbound2])

# add cyclic

ratio_rn_now=add_cyclic_point(ratio_rn[imon,:,:])
ratio_sn_now=add_cyclic_point(ratio_sn[imon,:,:])
lon=np.append(lon[:],181.)

# make plot

#  data is originally on PlateCarree projection.
#  cartopy need this to transform projection
data_crs=ccrs.PlateCarree()

#parameters=get_parameters(varnm,season)
#projection = ccrs.PlateCarree(central_longitude=180)
if pole == "N":
    projection = ccrs.NorthPolarStereo(central_longitude=0)
elif pole == "S":
    projection = ccrs.SouthPolarStereo(central_longitude=0)

fig = plt.figure(figsize=[8.0,11.0],dpi=150.)
#fig.set_size_inches(4.5, 6.5, forward=True)
plotTitle = {'fontsize': 13.}
#plotSideTitle = {'fontsize': 9., 'verticalalignment':'center'}
plotSideTitle = {'fontsize': 9.}
plotText = {'fontsize': 8.}
panel = [(0.27, 0.65, 0.3235, 0.25),\
         (0.27, 0.35, 0.3235, 0.25) #,\
         #(0.27, 0.05, 0.3235, 0.25),\
        ]
labels=["rain ratio","snow ratio"] 
units="%"
for i in range(0,2):
   #1. first plot
    levels = None
    norm = None
    cnlevels=np.linspace(0.1,0.9,9)

    #if len(cnlevels) >0:
    #        levels = [-1.0e8] + cnlevels + [1.0e8]
    #        norm = colors.BoundaryNorm(boundaries=levels, ncolors=256)

    ax = fig.add_axes(panel[i],projection=projection,autoscale_on=True)
    ax.set_global()
    if pole == "N":
        ax.gridlines(color="gray",linestyle=":",\
    		#xlocs=[0,60,120,180,240,300,360],ylocs=[50,60,70,80,89.5])
    		xlocs=[-180,-120,-60,0,60,120,180],ylocs=[50,60,70,80])
    elif pole == "S":
        ax.gridlines(color="gray",linestyle=":",\
    		#xlocs=[0,60,120,180,240,300,360],ylocs=[-50,-60,-70,-80])
    		xlocs=[-180,-120,-60,0,60,120,180],ylocs=[-50,-60,-70,-80])
    
    if pole == "N":
        ax.set_extent([-180, 180, 50, 90], crs=ccrs.PlateCarree())
    elif pole == "S":
        ax.set_extent([-180, 180, -50, -90], crs=ccrs.PlateCarree())

    if i == 0:
        dtplot=ratio_rn_now[:,:]
        cmap= "jet" #parameters["colormap"]
        stats_now=stats_rn
    elif i == 1:
        dtplot=ratio_sn_now[:,:]
        cmap="jet" #parameters["colormap"]
        stats_now=stats_sn

    p1 = ax.contourf(lon[:],lat[latbound1:latbound2],dtplot[latbound1:latbound2,:],\
                transform=data_crs,\
                #norm=norm,\
                levels=cnlevels,\
                cmap=cmap,\
                extend="both"\
                #autoscale_on=True\
        	    )
    #ax.set_aspect("auto")
    ax.coastlines(lw=0.3)
    #ax.set_autoscale_on()

    theta = np.linspace(0, 2 * np.pi, 100)
    #center, radius = [0.5, 0.5], 0.5
    # correct center location to match latitude circle and contours.
    center, radius = [0.5, 0.495], 0.50
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)

    ##add longitude and latitude mark
    ##lon
    #transf=data_crs._as_mpl_transform(ax)
    #ax.annotate("0", xy=(-1.85,57.5), xycoords=transf,fontsize=8)
    #ax.annotate("60E", xy=(57,59), xycoords=transf,fontsize=8)
    #ax.annotate("120E", xy=(120,60), xycoords=transf,fontsize=8)
    #ax.annotate("180", xy=(185.2,59.5), xycoords=transf,fontsize=8)
    #ax.annotate("120W", xy=(246, 52.5), xycoords=transf,fontsize=8)
    #ax.annotate("60W", xy=(297, 53), xycoords=transf,fontsize=8)
    ##lat
    #ax.annotate("60N", xy=(-4.5,61.3), xycoords=transf,fontsize=8)
    #ax.annotate("70N", xy=(-8.5,71), xycoords=transf,fontsize=8)
    #ax.annotate("80N", xy=(-17.5,81), xycoords=transf,fontsize=8)

    # title
    ax.set_title(labels[i],loc="left",fontdict=plotSideTitle)
    #ax.set_title(units,loc="right",fontdict=plotSideTitle)

    # color bar
    cbax = fig.add_axes((panel[i][0] + 0.35, panel[i][1] + 0.0354, 0.0326, 0.1792))
    cbar = fig.colorbar(p1, cax=cbax, ticks=cnlevels)
    #w, h = get_ax_size(fig, cbax)
    cbar.ax.tick_params(labelsize=9.0, length=0)

    # Mean, Min, Max
    fig.text(panel[i][0] + 0.35, panel[i][1] + 0.225,
             "Mean\nMin\nMax", ha='left', fontdict=plotText)
    fig.text(panel[i][0] + 0.45, panel[i][1] + 0.225, "%.2f\n%.2f\n%.2f" %
             stats_now[0:3], ha='right', fontdict=plotText)

fig.suptitle(var_long_name, x=0.5, y=0.96, fontdict=plotTitle)
#save figure as file
#if os.environ["fig_save"]=="True":
#    fname="d2_polar_contour_"+pole+"_"+varnm+"_"+season+"."+os.environ["fig_suffix"]
#plt.savefig(figure_name+".png")
#if os.environ["fig_show"]=="True":
plt.show()
plt.close()
