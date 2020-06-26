import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.animation as animation
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

###********************* Inspired by http://tech.weatherforce.org/blog/ecmwf-data-animation/index.html******************########

def make_figure(cartopy_projection):
    fig = plt.figure(figsize=(20,15))
    ax = fig.add_subplot(1, 1, 1, projection=cartopy_projection)
    # generate a basemap with country borders, oceans and coastlines
    ax.add_feature(cfeat.LAND)
    ax.add_feature(cfeat.OCEAN)
    ax.add_feature(cfeat.COASTLINE)
    #ax.add_feature(cfeat.BORDERS, linestyle='dotted')
    return fig, ax

def read(filename,varname):
    ds = xr.open_mfdataset(filename)
    area = ds[varname]
    frames = area.time.size
    return area,frames,ds    


def draw(frame,filename,varname,ax,min_value,max_value,N,cmap1,add_colorbar):
        area,frames,ds=read(filename,varname)
        grid = area[frame]
        levels1=np.linspace(min_value,max_value,N)
        contour = grid.plot(ax=ax, transform=ccrs.PlateCarree(),cmap=cmap1,extend='both',
                            add_colorbar=add_colorbar,levels=levels1)
        title = u"%s — %s" % (ds[varname].long_name, str(area.time[frame].values)[:19])
        ax.set_title(title)
        return contour


class animation_pan():
    
    def __init__(self,filename='',varname='',cartopy_projection=ccrs.PlateCarree(central_longitude=180.0),min_value=0,max_value=0,N=11,cmap1='PuRd',output=''):
        self.filename    = filename
        self.varname     = varname
        self.cartopy_projection = cartopy_projection
        self.min_value          = min_value
        self.max_value  = max_value
        self.N  = N
        self.cmap1  = cmap1
        self.output  = output
        self.fig,self.ax=make_figure(cartopy_projection)
        
    def explain_to(self):
        print("Hello, users. These are inputs:")
        print("The file name {}.".format(self.filename))
        print("The file name {}.".format(self.varname))
        print("Cartopy projection {}.".format(self.cartopy_projection))
        print("Min value {}.".format(self.min_value))
        print("Max_value {}.".format(self.max_value))
        print("colormap interval N {}.".format(self.N))
        print("colorbar cmap1 {}.".format(self.cmap1))
        print("output{}.".format(self.output))
    
    def init(self):
        return draw(0,self.filename,self.varname,self.ax,self.min_value,self.max_value,self.N,self.cmap1,add_colorbar=True)


    def animate(self,frame):
        return draw(frame,self.filename,self.varname,self.ax,self.min_value,self.max_value,self.N,self.cmap1, add_colorbar=False)

                                                     # Number of frames
    def make_animation(self):
        area,frames,ds=read(self.filename,self.varname)
        ani = animation.FuncAnimation(self.fig,self.animate,frames, interval=0.01, blit=False,
                              init_func=self.init, repeat=False)

        if len(self.output)!=0:
            ani.save(self.output, writer=animation.FFMpegWriter(fps=8))

        plt.close(self.fig)
        return ani
