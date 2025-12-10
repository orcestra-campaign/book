---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# IFS forecasts

The ECMWF kindly provides their IFS forecast data on a [public server](https://data.ecmwf.int).
We have started to automatically download the individual GRIB data, create a unified dataset, and remap it onto the HEALPix grid.
This dataset, which we call HIFS, is accessible through the [internal TCO catalog](https://gitlab.dkrz.de/tco/tcodata/-/blob/main/intake/internal.yaml) and can be **read and used by everyone**.
HIFS provides data at different initial dates (twice a day) starting in February 2024.
This notebook shows the access to the data and some basic usage examples.

:::{tip}
The access and usage of the data is the same as for [HERA5](hera5.md), which you might want to check out too.
:::

## Loading the data from the catalog

First, let's import all packages that are required to run the full notebook.
```{code-cell} ipython3
import intake
import healpix as hp
import cmocean
import numpy as np
import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt

import easygems.healpix as egh
```

Now we can open the catalog and select the *HEALPix-ified IFS forecast* `HIFS`.

```{code-cell} ipython3
cat = intake.open_catalog("https://tcodata.mpimet.mpg.de/internal.yaml")
ds = cat.HIFS(datetime="2024-04-01").to_dask().pipe(egh.attach_coords)
ds
```

+++

## Plotting examples

### 2m temperature at the BCO

We would like to plot the 2m air temperature at one location, the BCO.

```{code-cell} ipython3
ds = cat.HIFS(datetime="2024-04-01").to_dask().pipe(egh.attach_coords)

i_bco = hp.ang2pix(
    egh.get_nside(ds),
    -59.42875, # longitude at BCO
    13.16264, # latitude at BCO
    nest=egh.get_nest(ds),
    lonlat=True,
)

ds["2t"].sel(cell=i_bco).plot()
```

### Select ORCESTRA region

Plotting the forecasted total column water vapor and precipitation contours over the campaign domain.

```{admonition} Plotting maps
:class: info
You may want to check out [this tutorial](https://easy.gems.dkrz.de/Processing/map_show.html) on ways to plot geospatial data.
```

```{code-cell} ipython3
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})
ax.set_extent([-65, -5, -10, 25])
ax.coastlines(lw=0.8)
egh.healpix_show(
    ds["tcwv"].sel(time="2024-04-05 12:00"),
    cmap="cmo.dense",
    vmin=25,
    vmax=65,
)

egh.healpix_contour(
    ds["tp"].sel(time="2024-04-05 12:00"),
    cmap="cmo.rain",
    vmin=0.,
    vmax=0.15,
    levels=5,
)
```
