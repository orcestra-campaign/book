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

# Temperature comparison

Let's see how temperature readings at BCO compare with the ERA5 reanalysis:

```{code-cell} ipython3
import intake
import healpy as hp
import matplotlib.pylab as plt

cat = intake.open_catalog("https://tcodata.mpimet.mpg.de/internal.yaml")
ds = cat["ORCESTRA"]["hera5"].to_dask()
wxt = cat["BCO"]["surfacemet_wxt_v1"].to_dask()

i_bco = hp.ang2pix(2**7, 59 + 25/60 + 43.5/3600, 13 + 9/60 + 45.5/3600, nest=True, lonlat=True)

ds["2t"].isel(cell=i_bco).sel(time=slice("2020-01", "2020-02")).plot(label="ERA5")
(wxt["T"].sel(time=slice("2020-01", "2020-02")).resample(time="1H").mean() + 272.15).plot(label="WXT")

plt.legend();
```
