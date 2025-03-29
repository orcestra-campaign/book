---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
execution:
  timeout: 120
---

# IWV comparison

ORCESTRA focuses on the area of the Inter-Tropical Convergence Zone (ITCZ), which we've commonly identified by areas of high integrated water vapour (IWV).
We've used this quantity extensively during {doc}`Flight Planning <operation>` and several instruments measuring IWV have been deployed.
This notebook compares a few instruments which measured IWV during the campaign.

We'll first import some required libraries and set up the `root` path to the ORCESTRA data collection to a stable version.
If you are instead interested in the most recent updates, just use the `ipns` link instead.

```{code-cell} ipython3
import xarray as xr
import matplotlib.pylab as plt

# root = "ipns://latest.orcestra-campaign.org"
root = "ipfs://Qmbx6KSDfviFFi7f5XXQLB6MSTPhWnN1rNkCCKhyhaa7CA"
```

## relative occurrence over entire campaign period
We'll compare data from the GNSS sensors on {doc}`rvmeteor` as well as the microwave radiometer (HAMP) and the dropsondes from {doc}`halo`.
The three instruments all employ different sensing methods and sampled different areas of the observation region.
Still, they overall sampled a similar regime and thus on average, we might expect similar results.
This can be confirmed by the following histogram:

```{code-cell} ipython3
sources = [("METEOR GNSS", "METEOR/GNSS_IWV.zarr", "iwv"),
           ("HALO HAMP", "HALO/iwv/*.zarr", "IWV"),
           ("HALO dropsondes", "HALO/dropsondes/Level_3/PERCUSION_Level_3.zarr", "iwv")]
for label, path, var in sources:
    ds = xr.open_mfdataset(f"{root}/products/{path}", engine="zarr")
    plt.hist(ds[var], bins=40, range=(0,100), density=True, histtype="step", label=label);
plt.xlabel("IWV / kg m-2")
plt.ylabel("relative occurance")
plt.legend();
```

```{note}
At least some of the data is still in early processing stages, so you still might find artifacts which should be removed in subsequent stages of quality control.
```

Although the instruments broadly agree, we can already see some features of the measurement principle. E.g.:

* The microwave retrieval (HAMP) produces artificially high values when flying over land (instead of ocean). These values have not yet been removed and are visible in the histogram.
* The lower IWV values of hamp (e.g. < 30 kg/m2) correspond to the 3rd phase of ORCESTRA, which was based in Europe (see next figure). This period was not covered by RV Meteor and used fewer dropsondes.

```{code-cell} ipython3
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ds = xr.open_mfdataset(f"{root}/products/HALO/iwv/*.zarr", engine="zarr")   
low_iwv = ds.where(ds.IWV.compute() < 30, drop="True")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
plt.plot(low_iwv.lon, low_iwv.lat, ".", ms=1, transform=ccrs.PlateCarree())
plt.title("HALO HAMP, iwv<30");
```

## data sources

The datasets have been provided by various individuals and institutions.
Please inspect the dataset attributes and contact the authors in case you use the data for scientific work.

```{code-cell} ipython3
---
tags: [hide-input]
---

for label, path, var in sources:
    ds = xr.open_mfdataset(f"{root}/products/{path}", engine="zarr")
    print(label)
    for k, v in ds.attrs.items():
        print(f"{k}: {v}")
    print()
```
