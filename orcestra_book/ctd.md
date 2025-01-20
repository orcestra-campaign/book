---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# CTD measurements

[CTD](https://www.geomar.de/en/research/fb1/fb1-po/observing-systems/ctd/) (conductivity, temperature, and depth) measurements are an essential tool used in oceanography.

During BOWTIE, 82 CTD measurements were carried out at different locations in the tropical Atlantic:

```{code-cell} ipython3
import cartopy.crs as ccrs
import cmocean
import matplotlib.pyplot as plt
import xarray as xr


ds = xr.open_dataset("ipns://latest.orcestra-campaign.org/products/METEOR/CTD.zarr", engine="zarr")

fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={"projection": ccrs.PlateCarree()})
ax.set_extent([-65, -5, -10, 25], crs=ccrs.PlateCarree())
ax.coastlines()
ax.scatter(ds.LONGITUDE, ds.LATITUDE, color="#006699", transform=ccrs.Geodetic())
```

These _in-situ_ measurements allow scientists to compare vertical profiles of different physical and chemical properties throughout the campaign period:

```{code-cell} ipython3
fig, axes = plt.subplots(ncols=3, sharey=True, figsize=(12, 4.8))
ds.TEMP.plot(x="SOUNDING", cmap="cmo.thermal", ax=axes[0])
ds.DOX2.plot(x="SOUNDING", cmap="cmo.oxy", vmin=20, vmax=270, ax=axes[1])
ds.PSAL.plot(x="SOUNDING", cmap="cmo.haline", vmin=33, vmax=37, ax=axes[2])
axes[0].set_ylim(250, 0)
```
