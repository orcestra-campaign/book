---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Numerical simulations - Limited area model

To support the campaign, we performed daily hindcasts of the atmospheric conditions in the campaign region. The whole dataset is catalogued and stored on the supercomputer [Levante](https://docs.dkrz.de/doc/levante/index.html), hosted by the DKRZ and is accessible on demand. It comprises of high-sampling rate 2D and 3D snapshots of key variables.

Visualisations of individual variables for each day are given [here](lam.md). A sample script showing how to load and plot the data is provided below.

```{admonition} Requires zarr>=3
:class: warning

The dataset is stored in [Zarr v3](https://zarr.dev/blog/zarr-python-3-release/) and thus requires `zarr>=3.0.0`.
```

```{admonition} Matplotlib style sheet
:class: info

This script makes use of a custom [Matplotlib style sheet](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html): [`dark.mplstyle`](./dark.mplstyle)
```

This script shows how to read the LAM-ORCESTRA HEALPix dataset.
It plots a contour of horizontal surface wind speed for a specific time.

```{code-cell} ipython3
import cartopy.crs as ccrs
import easygems.healpix as egh
import intake
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Apply custom dark background style
plt.style.use("./dark.mplstyle")


def format_longitude(x, pos):
    """Customize the tick labels to remove the minus sign (its in °W)"""
    return f"{abs(int(x))}"


def apply_figure_style(ax, fig):
    """Black background style for figures."""
    ax.coastlines(color="white", linewidth=0.7)
    ax.set_aspect('equal', adjustable='box')
    xticks = np.linspace(-62, -10, 14)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_longitude))
    ax.set_yticks(np.linspace(-2, 22, 7), crs=ccrs.PlateCarree())
    ax.set_xlim([-62, -10])
    ax.set_ylim([-2, 22])
    ax.set_xlabel('Longitude [°W]')
    ax.set_ylabel('Latitude [°N]')


# Opening the 2d dataset covering the full-campaign period
url = "https://eerie.cloud.dkrz.de/datasets/orcestra_1250m_2d_hpz12/kerchunk"
ds = xr.open_dataset(url, chunks={}, engine="zarr", zarr_format=3)

# Local dataset access (on Levante only!)
# cat = intake.open_catalog("https://tcodata.mpimet.mpg.de/internal.yaml")
# ds = cat.ORCESTRA.LAM_ORCESTRA(dim="2d").to_dask()

# Plotting horizontal surface wind speed at 16h00
time = "2024-09-03 16:00"

fig, ax = plt.subplots(figsize=(13, 6), subplot_kw={'projection': ccrs.PlateCarree()})
apply_figure_style(ax, fig)

ds = ds.assign(sfcwind=lambda dx: np.hypot(dx.uas, dx.vas))
im = egh.healpix_show(ds.sfcwind.sel(time=time), vmin=0, vmax=20, cmap="magma", ax=ax)

# Add colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="1%", pad=0.1, axes_class=plt.Axes)
fig.colorbar(im, cax=cax, ticks=np.arange(0, 21, 5), label='Horizontal surface wind speed [m/s]')

# Add title with formatted timestamp
ax.set_title(time);
```
