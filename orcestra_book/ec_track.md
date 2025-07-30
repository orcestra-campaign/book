---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# EarthCARE Validation during ORCESTRA

EarthCARE regularly flew over the measurement area, allowing each of the aircraft to fly underneath. The data from the underflights are used to validate the EarthCARE measurements. This page shows how to compare EarthCARE and HALO tracks.

```{note}
In this example, we use the EarthCARE orbit **predictions** as used for flight planning during ORCESTRA.
With EarthCARE data being public, other ways to obtain the actual (past) orbits should be available at some point.
```

First, we load the track data. EarthCARE tracks are available for different regions of interest (`roi`) and forecast days.
You can check [sattracks.orcestra-campaign.org](http://sattracks.orcestra-campaign.org) for an overview of all available forecasts.

```{code-cell} ipython3
from datetime import date

import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import xarray as xr
from orcestra import bco, sat


# Get EartchCare track
date = date(2024, 8, 25)
ec_track = sat.SattrackLoader(
    "EARTHCARE",
    forecast_day=date,
    kind="PRE",
    roi="CAPE_VERDE",
).get_track_for_day(date)
```

EarthCare tracks include the ascending and descending orbits.
For the plot, we select only the afternoon overpass that coincided with our flight.

```{code-cell} ipython3
ec_track = ec_track.sel(time=slice(f"{date} 12:00", f"{date} 23:59"))
```

Next, we will select the HALO position/attidue data for the corresponding flight day.
For plotting reasons, the coarsen the 100Hz data into 1min-averages.

```{code-cell} ipython3
# root = "ipns://latest.orcestra-campaign.org"
root = "ipfs://Qmb1wKeNLkqichCfPwsjk8f2vBHU1dxkgLRVmHwk7rdvi2"
halo_track = xr.open_dataset(f"{root}/products/HALO/position_attitude.zarr", engine="zarr")
halo_track = halo_track.sel(time=str(date)).coarsen(time=6000, boundary="pad").mean("time")  # 1min-average
```

Now we can plot the tracks:

```{code-cell} ipython3
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree()})
ax.set_extent([-50, -10, -5, 25])
ax.add_feature(cf.COASTLINE)
ax.add_feature(cf.LAND)
ax.add_feature(cf.OCEAN)
ax.plot(halo_track.lon, halo_track.lat, label="HALO", lw=3, c="tab:orange", transform=ccrs.Geodetic())
ax.plot(ec_track.lon, ec_track.lat, label="EarthCare", lw=1.5, c="tab:green", transform=ccrs.Geodetic())
ax.legend();
```
