# Numerical simulations - Limited area model

To support the campaign, we performed daily hindcasts of the atmospheric conditions in the campaign region. The whole dataset is catalogued and stored on the supercomputer [Levante](https://docs.dkrz.de/doc/levante/index.html), hosted by the DKRZ and is accessible on demand. It comprises of high-sampling rate 2D and 3D snapshots of key variables.

Visualisations of individual variables for each day are given [here](lam.md). A sample script showing how to load and plot the data is provided below.

```{admonition} Requires zarr>=3
:class: warning

The dataset is stored in [Zarr v3](https://zarr.dev/blog/zarr-python-3-release/) and thus requires `zarr>=3.0.0`.
```

```py
# %%
# This scrits shows how to read the LAM-ORCESTRA healpix dataset.
# It plots a contour of horizontal surface wind speed for a specific time.
#
# %%
# Setup environment & define functions
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import easygems.healpix as egh
import healpix as hp
import numpy as np
import xarray as xr
import cmocean
import intake

from pylab import *
from matplotlib import gridspec
from matplotlib import cm
from datetime import datetime, timedelta
from mpl_toolkits.axes_grid1 import make_axes_locatable

os.environ['TEXMFHOME'] = '/home/m/m301067/texmf'
os.environ['PATH'] = '/sw/spack-levante/texlive-live2021-l5o6sw/bin/x86_64-linux:' + os.environ['PATH']
plt.rcParams.update({'font.size': 13, 'font.family': 'TimesNewRoman', 'text.usetex': True})
rcParams['axes.linewidth'] = 1.5
rcParams["axes.formatter.use_mathtext"]
plt.rcParams['figure.dpi'] = 450

# Customize the tick labels to remove the minus sign (its in °W)
def format_longitude(x, pos):
    return f"{abs(int(x))}"

# Black background style for figures
def apply_figure_style(ax, fig):
    ax.coastlines(color='white', linewidth=0.7)
    ax.set_aspect('equal', adjustable='box')
    xticks = np.linspace(-62, -10, 14)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(FuncFormatter(format_longitude))
    ax.set_yticks(np.linspace(-2, 22, 7), crs=ccrs.PlateCarree())
    ax.set_xlim([-62, -10])
    ax.set_ylim([-2, 22])
    ax.set_xlabel('Longitude [°W]', color='white')
    ax.set_ylabel('Latitude [°N]', color='white')
    #ax.grid(color='white', alpha=0.4, linestyle='dashed', linewidth=0.3)
    
    # Set the face color of both the axis and the figure
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

# %%
# Chose the starting day of the target run (remember it is 48h-long and includes 24h of spin-up)
day = "2024-09-03"
cat = intake.open_catalog("https://tcodata.mpimet.mpg.de/internal.yaml")
ds = cat.ORCESTRA.ICON_LAM(date=day, dim="2d").to_dask()

# %%
# Plotting horizontal surface wind speed at 16h00
time = "16:00"
fig, ax = plt.subplots(figsize=(13, 6), subplot_kw={'projection': ccrs.PlateCarree()})
apply_figure_style(ax, fig)

# Calculate surface windspeed
ds = ds.assign(sfcwind=lambda dx: np.hypot(dx.uas, dx.vas))

# Plot healpix data
im = egh.healpix_show(ds.sfcwind.sel(time=f"{day} {time}"), vmin=0, vmax=20, cmap=plt.cm.magma, ax=ax)

# Add colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="1%", pad=0.1, axes_class=plt.Axes)  # Ensure no projection is used
cbar = plt.colorbar(im, cax=cax, ticks=np.linspace(0, 20, 5))
cbar.set_label('Horizontal surface wind speed [m/s]', fontsize=13, weight="bold", \
    rotation=270, labelpad=20, color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
cbar.outline.set_edgecolor('white')

# Add title with formatted timestamp
ax.set_title(f"{day} {time}", color='white', fontsize=15)

# Display the figure
plt.show()
```

```{figure} /figures/lam-hsws.png
:alt: Snapshot of horizontal surface wind speed from the LAM-ORCESTRA simulations.
:width: 800px
:align: center

Snapshot of horizontal surface wind speed from the LAM-ORCESTRA simulations.
```
