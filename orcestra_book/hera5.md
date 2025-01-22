---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# ERA5 data on the HEALPix grid

ERA5[^ack] data for selected variables has been restructured and remapped onto the HEALPix grid for the years 2010 to 2023.
This dataset, which we call HERA5, is accessible through the [internal TCO catalog](https://gitlab.dkrz.de/tco/tcodata/-/blob/main/intake/internal.yaml) and can be **read and used by everyone**.
HERA5 provides data at different temporal resolutions and enables an open and fast access to the data from everywhere and without a local copy.
This notebook shows the access to the data and some basic usage examples.

This tutorial makes use of the [`easygems`](https://github.com/mpimet/easygems/tree/main) python package which hosts several convenience functions to work with and display Earth-system data on the HEALPix grid.
If you don't have the package installed, you can run the code cell below to install it via `pip`:

```python
%pip install easygems
```

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

Now we can open the catalog and select the *hierarchical HEALPix ERA5 data* `HERA5`.

```{code-cell} ipython3
cat = intake.open_catalog("https://tcodata.mpimet.mpg.de/internal.yaml")
list(cat)
```

```{code-cell} ipython3
cat.HERA5.to_dask().pipe(egh.attach_coords)
```

### Some notes on the dataset
* **Dimensions**
  * the dimensions are `time`, `cell` and (pressure-)`level` and the coordinate reference system `crs`. Here, `cell` refers to the cells in the HEALPix grid, which is a pixelation of a sphere. **Get to know more about HEALPix [here](https://easy.gems.dkrz.de/Processing/healpix/index.html#healpix).** The zoom level of the HERA5 data is $z = 7$ and the number of cells respectively $12 \cdot z^{4} = 196608$
  * you can distinguish between 2d and 3d variables by their dimensions, the former having only `(time, cell)` and the latter having `(time, level, cell)`.
* **Temporal hierarchy**
  * The dataset is constructed hierarchically in time, which means that you can directly access either monthly aggregated values `P1M`, daily `P1D`, or the original hourly data `PT1H`. By default, the catalog entry points to the monthly values which are great to do a fast analysis of longterm and coarse features such as calculating the global mean surface temperature over 10 years. If you need higher temporal resolutions, you can add the respective acronym when loading the catalog: `ds = cat.HERA5(time="PT1H").to_dask()`.
  * In principle, one could also implement spatial hierarchies. However, the original ERA5 data is already rather coarse such that there is no need for coarser spatial (zoom) levels in the present case.
* **Spatial resolution**
  * The spatial resolution is given by the `zoom` level $z = 7$ which is closest to the original ERA5 model output and roughly corresponds to 0.35 x 0.7° effective grid resolution.
* **Variables**
  * Most variables are from the ERA5 "analysis" product. Only few variables such as `total precipitation` and `boundary layer height` are added from the "forecast" product. Each variable has a `type` attribute which will let you know whether it is from the `analysis` or `forecast` product.

+++

## Plotting examples

### 2m temperature at the BCO in Aug-Sep 2020

We would like to plot the 2m air temperature at one location, the BCO, in August and September 2020.
For this rather short time period, we would like to work with the hourly data. Therefore, we need to specify the time hierarchy when addressing the data in the catalog.

```{code-cell} ipython3
era5 = cat.HERA5(time="PT1H").to_dask().pipe(egh.attach_coords)
```

Next, we want to see how temperature readings at BCO (WXT) compare with the ERA5 reanalysis.
We select the cell index that is the nearest neighbor to the BCO location using `healpix.ang2pix()`.

```{code-cell} ipython3
wxt = cat.BCO.surfacemet_wxt_v1.to_dask()
i_bco = hp.ang2pix(egh.get_nside(era5), wxt.lon, wxt.lat, nest=egh.get_nest(era5), lonlat=True)
```

Now, we can plot the time series by selecting the respective cell as well as a time range:

```{code-cell} ipython3
era5["2t"].isel(cell=i_bco).sel(time="2020-08").plot(label="ERA5")
(wxt["T"].sel(time="2020-08").resample(time="1h").mean() + 273.15).plot(label="WXT")
plt.legend();
```

### Evolution of the moisture field at BCO

Next, we extend our analysis and use a 3d variable to plot a time-height diagramm of moisture.
Again, we select the BCO cell, a time range and now also a range in height `level` where we leave out the upper most layers (<100hPa) as we are interested in the troposphere only.

```{code-cell} ipython3
era5["q"].sel(
    cell=i_bco,
    time="2020-08",
    level=slice(100, 1000),
).plot(
    x="time",
    yincrease=False,
    cmap="cmo.dense",
    vmin=0,
)
```

### Select ORCESTRA region

We want to see how the RH profile changes with latitude when averaged over the ORCESTRA campaign region on the 20th of August 2020. The `easygems` package provides the the `isel_extent` function which takes a lat/lon extent (`[W, E, S, N]`) as input and returns the corresponding indices of the global HEALPix grid. These indices can then be used to select the region of interest.

```{code-cell} ipython3
is_orcestra = egh.isel_extent(era5, [-60, -10, -5, 20])

fig, ax = plt.subplots()
era5["r"].sel(
    cell=is_orcestra,
    time="2020-08-20",
    level=slice(100, 1000),
).mean(
    "time"
).groupby(
    era5.lat.sel(cell=is_orcestra)
).mean().plot(
    x="lat",
    yincrease=False,
    cmap="cmo.dense",
    ax=ax,
)
ax.set_title("Relative humidity profile on 2020-08-20 (ORCESTRA region)")
```

### A snapshot of global SST

```{code-cell} ipython3
egh.healpix_show(
    era5["sst"].sel(time="2020-08-01T12:00:00", method="nearest"),
    nest=egh.get_nest(era5),
    vmin=273,
    vmax=303,
    cmap="cmo.thermal",
)
```

## Plotting the Atlantic basin only

In real-life analyses it is often necessary to constrain a plot to certain regions. The function `easygems.healpix_show()` allows to plot two-dimensional data onto a cartopy `GeoAxis` with arbitrary projection and extent.

```{code-cell} ipython3
era5 = cat.HERA5(time="P1M").to_dask().pipe(egh.attach_coords)
var = era5["tp"]

fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})
ax.set_extent([-65, -5, -10, 25])
ax.coastlines(lw=0.8)
im = egh.healpix_show(
    var.sel(time="2020-08", method="nearest").values,
    method="linear",
    cmap="cmo.rain",
    vmin=0,
)
fig.colorbar(im, label=f"{var.long_name} / {var.units}", shrink=0.7)
```

## Further reading
* The HEALPix grid: [A short intro](https://easy.gems.dkrz.de/Processing/healpix/index.html#healpix)

[^ack]: Contains modified Copernicus Climate Change Service information 2020. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains.
