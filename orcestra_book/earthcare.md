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

EarthCARE tracks are available as long term prediction (LTP) and preliminary (PRE). The PRE tracks are available for the next week and updated daily. The PRE tracks are available for five weeks and updated roughly every two weeks. To make the latest EarthCARE track predictions available, we plot PRE tracks for this week and LTP tracks for the two weeks after. 

First, we load the track data 
```{code-cell} python3
:tags: [hide-input]
from orcestra import sat
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
import cartopy.crs as ccrs
from geopy.distance import geodesic
import numpy as np
import pandas as pd


# Get most recent LTP forecast
track_list = pd.read_csv(
    "https://sattracks.orcestra-campaign.org/index.csv",
    parse_dates=["forecast_day"],
)
issue_date_ltp = (
    track_list.where(track_list.kind == "LTP")
    .dropna()
    .sort_values(
        by="forecast_day",
        ignore_index=True,
        ascending=False,
    )
    .forecast_day.loc[0]
    .strftime("%Y-%m-%d")
)

# Get most recent PRE forecast
issue_date_pre = (
    track_list.where(track_list.kind == "PRE")
    .dropna()
    .sort_values(
        by="forecast_day",
        ignore_index=True,
        ascending=False,
    )
    .forecast_day.loc[0]
    .strftime("%Y-%m-%d")
)


# Define timeframes for long term prediction (LTP) and preliminary (PRE)
dates_pre = [
    datetime.fromisoformat(issue_date_pre) + timedelta(days=i) for i in range(7)
]
dates_ltp = [
    datetime.fromisoformat(issue_date_pre) + timedelta(days=7) + timedelta(days=i)
    for i in range(14)
]

# Load the tracks 
tracks_ltp = {}
tracks_pre = {}
for date in dates_ltp:
    tracks_ltp[date] = (
        sat.SattrackLoader("EARTHCARE", issue_date_ltp, kind='LTP')
        .get_track_for_day(date)
        .sel(time=slice(datetime.combine(date, time(6, 0)), None))
        )
for date in dates_pre:
    tracks_pre[date] = (
        sat.SattrackLoader("EARTHCARE", issue_date_pre, kind='PRE')
        .get_track_for_day(date)
        .sel(time=slice(datetime.combine(date, time(6, 0)), None))
    )
```
Now we plot the PRE tracks for this week and the LTP tracks for the two weeks after. 

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

def annotate_time(ax, track, line):
    mid_index = len(track.lon) // 2
    track_time = pd.Timestamp(track.time.mean().values)
    ax.annotate(
        f"{track_time.day}.{track_time.month}. {track_time.hour}:{track_time.minute}",
        xy=(track.lon[mid_index], track.lat[mid_index]),
        xytext=(-5, 1),
        textcoords="offset points",
        fontsize=9,
        color=line.get_color(),
        rotation=-100.8,
        rotation_mode="anchor",
        bbox=dict(facecolor="white", edgecolor="none"),
    )


def plot_tracks(tracks, dates, ax):
    # plot tracks
    for date in dates:
        if (time := tracks[date].time).size == 0:
            # Don't attempt to plot tracks without data (e.g. night-time overpasses)
            continue

        # check if earthcare crosses the box two times
        diff_time = time.diff("time") > pd.Timedelta("1m")
        # plot two tracks if timedelta between datapoints is more than 1 minute
        if diff_time.max():
            idx_new_line = int(diff_time.argmax())
            track_1 = tracks[date].isel(time=slice(None, idx_new_line))
            (line,) = ax.plot(
                track_1.lon.values,
                track_1.lat.values,
                transform=ccrs.PlateCarree()
            )
            if len(track_1.lon.values) > 10:
                annotate_time(ax, track_1, line)
            track_2 = tracks[date].isel(time=slice(idx_new_line + 1, None))
            (line,) = ax.plot(
                track_2.lon.values,
                track_2.lat.values,
                transform=ccrs.PlateCarree(),
                color=line.get_color(),
            )
            if len(track_2.lon.values) > 10:
                annotate_time(ax, track_2, line)
        else:
            (line,) = ax.plot(
                tracks[date].lon.values,
                tracks[date].lat.values,
                transform=ccrs.PlateCarree(),
            )
            if len(tracks[date].lon.values) > 0:
                annotate_time(ax, tracks[date], line)

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
plot_tracks(tracks_pre, dates_pre, axes[0])
axes[0].set_title('Tracks for this week from latest prediction')
plot_tracks(tracks_ltp, dates_ltp[:7], axes[1])
axes[1].set_title('Tracks for next week from long-term prediction')
plot_tracks(tracks_ltp, dates_ltp[7:], axes[2])
axes[2].set_title('Tracks in two weeks from long-term prediction')
fig.tight_layout()
```
