import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.animation as animation
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib
from celluloid import Camera


#####******************* Inspired by http://tech.weatherforce.org/blog/ecmwf-data-animation/index.html******************########
#####*******************Inspired by https://gist.github.com/ScottWales/5d0ef918d56c4f6f58b73c1d5eabaf9b*******************########

def make_figure(cartopy_projection):
    fig = plt.figure(figsize=(20,15))
    ax = fig.add_subplot(1, 1, 1, projection=cartopy_projection)
    ax.add_feature(cfeat.LAND)
#     ax.add_feature(cfeat.OCEAN)
    ax.add_feature(cfeat.COASTLINE)
    #ax.add_feature(cfeat.BORDERS, linestyle='dotted')
    return fig, ax


def draw(frame,ds,varname,ax,min_value,max_value,N,cmap1,add_colorbar):
        area = ds[varname]
        frames = area.time.size
        grid = area[frame]
        levels1=np.linspace(min_value,max_value,N)
        contour = grid.plot(ax=ax, transform=ccrs.PlateCarree(),cmap=cmap1,extend='both',
                            add_colorbar=add_colorbar,levels=levels1)
        
        ax.set_global()
        ax.coastlines()

        title = u"%s — %s" % (ds[varname].name, str(area.time[frame].values)[:19])
        ax.set_title(title)
        return contour

    
def initial():
    return draw(0,ds,varname,ax,min_value,max_value,N,cmap1,add_colorbar=True)


def animate(frame):
    return draw(frame,ds,varname,ax,min_value,max_value,N,cmap1,add_colorbar=False)


def make_animation(fig,frames,outputname):
    ani = animation.FuncAnimation(fig,animate,frames, interval=0.01, blit=False,init_func=initial, repeat=False)
#     ani.save(outputname, writer=animation.FFMpegWriter(fps=4))
    ani.save(outputname,writer='imagemagick') 
    plt.close(fig)
    return ani


######################################### Run the Code #############
a=xr.open_dataset('sst_anom_mhws.nc')
a1 =a.sel(time=slice('2010-06-26','2010-07-29'))
import nclcmaps 
cmap1=nclcmaps.cmap('sunshine_9lev')

ds = a1*1
varname ='sstanom';
cartopy_projection=ccrs.Orthographic(central_latitude=0.0,central_longitude=75.0)
min_value   =   0.00
max_value   =   0.8
N           =   11
cmap1       =   cmap1
fig,ax      = make_figure(cartopy_projection)
make_animation(fig,frames=ds.time.size,outputname='output.gif')

