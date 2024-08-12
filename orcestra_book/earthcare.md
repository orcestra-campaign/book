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

# EarthCARE


EarthCARE (Earth Clouds, Aerosols and Radiation Explorer) is an earth observation satellite of the European Space Agency (ESA) and the Japan Aerospace Exploration Agency (JAXA). Equipped with four instruments, the EarthCARE satellite mission has been designed to make a range of different measurements that together will shed new light on the role that clouds and aerosols play in regulating Earth’s climate. It was launched on 28th of May, 2024 by SpaceX with the Falcon 9 rocket.


## Instrument

To achieve these scientific goals, EarthCARE orbits the Earth at an altitude of 390 km and offers an unprecedented set of active and passive remote sensing instruments on a single satellite platform:

* the atmospheric lidar **ATLID**, a high spectral resolution lidar (HSRL), operating at 355 nm wavelength, with 30 m beam diameter on the ground and polarization measurement,
 
* the 94 GHz Doppler **CPR** (cloud profiling radar) with 500 m measuring distance and 500 m vertical resolution,
 
* the multi-spectral imager **MSI** with seven channels in the solar and thermal spectral range, 500 m resolution in the nadir range and 150 km coverage,
 
* the broadband radiometer **BBR** with short- and long-wave channels, three different viewing directions along the ground track and 10 km pixel size on the ground.

## EarthCARE Validation during ORCESTRA

EarthCARE is regularly crossing the measurement area, which allows for underflights with any of the aircrafts. Measurement data from the underflights is used to validate the EarthCARE measurements. On this page, we show tracks of EarthCARE in the vicinity of Sal island within the next two weeks for flight planning purposes. 

First we define the timeframe and download the tracks for the next two week. 
```{code-cell} python3
:tags: [hide-input]
import orcestra 
import orcestra.sat
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
import cartopy.crs as ccrs 
from geopy.distance import geodesic 
import numpy as np
import pandas as pd

# Define week we want to look at the earthcare tracks for with given leadtime
start_date = (datetime.now()).date()
dates = [start_date + timedelta(days=i) for i in range(21)]

# Load the tracks for the week
tracks = {}
for date in dates:
    tracks[date] = orcestra.sat.SattrackLoader("EARTHCARE", "2024-08-05").get_track_for_day(date).sel(time=slice(datetime.combine(date, time(6, 0)), None))

```
Now we plot the tracks for this week and the next week.  

```{code-cell} python3
:tags: [hide-input]
def generate_circle_points(center, radius_km, num_points=100):
    lat, lon = center
    angles = np.linspace(0, 360, num_points)
    circle_points = []

    for angle in angles:
        destination = geodesic(kilometers=radius_km).destination((lat, lon), angle)
        circle_points.append((destination.latitude, destination.longitude))

    return circle_points

def plot_tracks(tracks, dates, ax): 
    # plot tracks
    for date in dates:
        track_lon = tracks[date].lon.values
        track_lat = tracks[date].lat.values
        line, = ax.plot(track_lon, track_lat, label=date, transform=ccrs.PlateCarree())
        if len(track_lon) > 0:
            mid_index = len(track_lon) // 2
            track_time = pd.Timestamp(tracks[date].time.mean().values)
            ax.annotate(f"{track_time.day}.{track_time.month}. {track_time.hour}:{track_time.minute}", xy=(track_lon[mid_index], track_lat[mid_index]), xytext=(-5, 1),
                            textcoords='offset points', fontsize=9, color=line.get_color(),
                            rotation=-100.8, rotation_mode='anchor', bbox=dict(facecolor='white', edgecolor='none'))
    # plot circle
    center = (16.735, -22.948) 
    radius_km = 250
    circle_points = generate_circle_points(center, radius_km)
    lats, lons = zip(*circle_points)
    ax.plot(lons, lats, label=f'{radius_km} km circle', color='k')

    # pimp plot
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

fig, axes = plt.subplots(1, 3, figsize=(14, 6), subplot_kw={'projection': ccrs.PlateCarree()}, sharex=True, sharey=True)
plot_tracks(tracks, dates[:7], axes[0])
axes[0].set_title('EarthCARE tracks for this week')
plot_tracks(tracks, dates[7:14], axes[1])
axes[1].set_title('EarthCARE tracks for next week')
plot_tracks(tracks, dates[14:], axes[2])
axes[2].set_title('EarthCARE tracks for the week after next')
fig.tight_layout()
```
