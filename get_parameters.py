# os
import os
#import netCDF4
#from netCDF4 import Dataset as netcdf_dataset
# cartopy
#import cartopy.crs as ccrs
#from cartopy.mpl.geoaxes import GeoAxes
#from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
#from cartopy.util import add_cyclic_point
# matplotlib
#import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid1 import AxesGrid
#import matplotlib.colors as colors
# numpy
import numpy as np
    
def get_parameters(varnm,season):
    #list_rad=["FLUT","FLUTC","FLNT","FLNTC","FSNT","FSNTC","FSDS","FSDSC","FSNS","FSNSC"]
    if varnm == "FLUT":
        parameters={"units":"W/m2",\
		   "contour_levs":[120, 140, 160, 180, 200, 220, 240, 260, 280, 300],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FLUTC":
        parameters={"units":"W/m2",\
		   "contour_levs":[120, 140, 160, 180, 200, 220, 240, 260, 280, 300],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FLNS":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 20, 40, 60, 80, 100, 120, 140, 160],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FLNSC":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 20, 40, 60, 80, 100, 120, 140, 160],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FLDS":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400, 450],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FLDSC":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400, 450],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FSNS":
        parameters={"units":"W/m2",\
		   #"contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400],\
		   #"diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
		   "contour_levs":[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260],\
		   "diff_levs":[-6,-5, -4, -3, -2, -1, -0.5, 0.5, 1, 2, 3, 4, 5, 6],\
                   "colormap":"Oranges",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FSNSC":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FSDS":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FSDSC":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FSNTOA":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FSNTOAC":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "SOLIN":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 50, 100, 150, 200, 250, 300, 350, 400, 450],\
		   "diff_levs":[-50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "FSUTOA":
        parameters={"units":r"W/m$^2$",\
		   "contour_levs":[60,70,80,90,100,110,120,130,140,150,160,170],\
		   "diff_levs":[-5, -4, -3, -2, -1, -0.5, 0.5, 1, 2, 3, 4, 5],\
		   "colormap":"Oranges",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "LHFLX":
        parameters={"units":"W/m2",\
		   "contour_levs":[0,5, 15, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300],\
		   "diff_levs":[-150, -120, -90, -60, -30, -20, -10, -5, 5, 10, 20, 30, 60, 90, 120, 150],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "SHFLX":
        parameters={"units":"W/m2",\
		   "contour_levs":[-100, -75, -50, -25, -10, 0, 10, 25, 50, 75, 100, 125, 150],\
		   "diff_levs":[-100, -80, -60, -40, -20, -10, -5, 5, 10, 20, 40, 60, 80, 100],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }
    if varnm == "TS":
        parameters={"units":"K",\
		   "contour_levs":[240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295],\
		   "diff_levs":[-10, -7.5, -5, -4, -3, -2, -1, -0.5, 0.5, 1, 2, 3, 4, 5, 7.5, 10],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "SWCF":
        parameters={"units":"W/m2",\
		   "contour_levs":[-180, -160, -140, -120, -100, -80, -60, -40, -20,  0],\
		   "diff_levs":[-60, -50, -40, -30, -20, -10, -5, 5, 10, 20, 30, 40, 50, 60],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "LWCF":
        parameters={"units":"W/m2",\
		   "contour_levs":[0, 10, 20, 30, 40, 50, 60, 70, 80],\
		   "diff_levs":[-35, -30, -25, -20, -15, -10, -5, -2, 2, 5, 10, 15, 20, 25, 30, 35],\
                   "colormap":"PiYG_r",\
                   "colormap_diff":"bwr"\
		   }

    if varnm == "PRECT":
        parameters={"units":"mm/day",\
		   "contour_levs":[0.5,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,13.,14.,15.],\
		   "diff_levs":[-0.5,-0.4,-0.3,-0.2,-0.1,-0.05,0.05,0.1,0.2,0.3,0.4,0.5],\
                   "colormap":"CMRmap_r", \
                   "colormap_diff":"bwr"\
		   }

    if varnm == "CLDTOT":
        parameters={"units":"fraction",\
		   "contour_levs":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],\
		   "diff_levs":[-0.05,-0.04,-0.03,-0.02,-0.01,-0.005,0.005,0.01,0.02,0.03,0.04,0.05],\
                   "colormap":"GnBu", \
                   "colormap_diff":"bwr"\
		   }

    if varnm == "ICEFRAC":
        parameters={"units":"fraction",\
		   "contour_levs":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],\
		   "diff_levs":[-0.10,-0.08,-0.06,-0.04,-0.02,-0.01,0.01,0.02,0.04,0.06,0.08,0.10],\
                   "colormap":"GnBu", \
                   "colormap_diff":"bwr"\
		   }

    if varnm == "PRECL" or varnm == "PRECSL":
        parameters={"units":"fraction",\
		   "contour_levs":[0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0],\
		   "diff_levs":[-0.5,-0.4,-0.3,-0.2,-0.1,-0.05,0.05,0.1,0.2,0.3,0.4,0.5],\
                   "colormap":"GnBu", \
                   "colormap_diff":"bwr"\
		   }

    return parameters



def get_area_mean_min_max(varin,lat):
    # varin dimention: [lat,lon]
    if np.array((varin)).ndim != 2:
        print('ERROR: input variable should be 2D [lat,lon]. (get_area_mean_max)')
        exit()
   # 1. area weighted average 
    #convert latitude to radians
    latr=np.deg2rad(lat)
    #use cosine of latitudes as weights for the mean
    weights=np.cos(latr)
    #first calculate zonal mean
    zonal_mean=varin.mean(axis=1)
    #then calculate weighted global mean
    area_mean=np.average(zonal_mean,axis=0,weights=weights)
   # 2. min and max
    minval=varin.min()
    maxval=varin.max()
    return area_mean,minval,maxval
