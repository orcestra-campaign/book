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
  timeout: 600
---

# HALO's flight segmentation
To aid in the analysis of flight data, all HALO flights are segmented via timestamps into a system of hierarchical identifiers. Non-exclusive segments are defined by two (YYYY-MM-DD hh:mm:ss) timestamps, the first one defining the `start` of the segment and the second denoting the first time step after the `end` of the segment. Timestamps have a temporal resolution of 1 s, and times are given in UTC. Every segment belongs to a `kind` – a categorical type for segments defined below. It helps to think of segments as an interval of flight time and the corresponding kinds as describing how the aircraft was being operated during this time interval.

Flight segmentation data are provided in a YAML (YAML Ain't Markup Language) file can be accessed at https://orcestra-campaign.github.io/flight_segmentation/all_flights.yaml or in python directly via the `pyorcestra` package. This section provides a description of the YAML file and some examples of how to use it with python.

+++

## Loading the flight segmentation data

```{code-cell} ipython3
from orcestra import get_flight_segments

meta = get_flight_segments()
```

### Which flights are included in the flight segmentation?

```{code-cell} ipython3
flight_ids = [flight_id
              for flights in meta.values()
              for flight_id in flights]
print(f"Totel number of flights: {len(flight_ids)}")
flight_ids
```

## Segments

Sometimes it may be useful to have a flat list of segments, irrespective of which flight or platformt they belong to. So we build it here:

```{code-cell} ipython3
segments = [{**s,
             "platform_id": platform_id,
             "flight_id": flight_id
            }
            for platform_id, flights in meta.items()
            for flight_id, flight in flights.items()
            for s in flight["segments"]
           ]
```

### List available segment `kinds`

```{code-cell} ipython3
kinds = set(k for s in segments for k in s["kinds"])
kinds
```

### Plotting all segments of a specific flight

+++

A supplement function is added here for loading HALO position and attitude data to show the application of flight segmentation information.

```{code-cell} ipython3
import xarray as xr
import matplotlib.pyplot as plt
from orcestra.flightplan import sal, tbpb

def get_halo_position_attitude(flight_id):
    root = "ipns://latest.orcestra-campaign.org/products/HALO/position_attitude"
    return (xr.open_dataset(f"{root}/{flight_id}.zarr", engine="zarr")
            .reset_coords().resample(time="1s").mean().load())

def kinds2color(kinds):
    if "circle" and "atr_coordination" in kinds:
        return "C2"
    if "circle" in kinds:
        return "C1"
    if "ec_track" in kinds:
        return "C3"
    return "C0"
```

```{code-cell} ipython3
flight = "HALO-20240811a"
ds = get_halo_position_attitude(flight)

fig, ax = plt.subplots()
for s in meta["HALO"][flight]["segments"]:
    t = slice(s["start"], s["end"])
    ax.plot(ds.lon.sel(time=t), ds.lat.sel(time=t), c=kinds2color(s["kinds"]))#, label=s["name"])

for k in ["circle", "straight_leg", "ec_track", "atr_coordination"]:
    ax.plot([], [], color=kinds2color(k), label=k)

plt.scatter(sal.lon, sal.lat, marker="o", color="k")
plt.annotate("SAL", (sal.lon, sal.lat))

ax.set_xlabel("longitude / °")
ax.set_ylabel("latitude / °")
ax.spines[['right', 'top']].set_visible(False)
ax.legend()
plt.title(flight);
```

### Plotting all segments of a specific kind

```{code-cell} ipython3
fig, ax = plt.subplots()
kind = "circle"

for f in flight_ids:
    ds = get_halo_position_attitude(f)
    for s in segments:
        if kind in s["kinds"] and f==s["flight_id"]:
            t = slice(s["start"], s["end"])
            ax.plot(ds.lon.sel(time=t), ds.lat.sel(time=t), c=kinds2color(kind), label=s["name"])
ax.set_xlabel("longitude / °")
ax.set_ylabel("latitude / °")

ax.scatter(sal.lon, sal.lat, marker="o", color="k")
ax.annotate("SAL", (sal.lon, sal.lat))
ax.scatter(tbpb.lon, tbpb.lat, marker="o", color="k")
ax.annotate("BARBADOS", (tbpb.lon, tbpb.lat))
ax.spines[['right', 'top']].set_visible(False)
```

## Some statistics

```{code-cell} ipython3
segment_ids_by_kind = {kind: [segment["segment_id"]
                              for segment in segments
                              if kind in segment["kinds"]]
                       for kind in kinds}
```

Print the total number of circles.  
Note that those are not necessarily with dropsondes and the circles can have different radii.

```{code-cell} ipython3
len(segment_ids_by_kind["circle"])
```

List the segments that include the tag `atr_coordination`

```{code-cell} ipython3
segment_ids_by_kind["atr_coordination"]
```

### Total time spent on EarthCARE tracks

```{code-cell} ipython3
import datetime

ec_time = sum([s["end"] - s["start"]
               for s in segments
               if "ec_track" in s["kinds"]
              ], datetime.timedelta())
print(ec_time)
```

### Total time of coordination with Meteor

```{code-cell} ipython3
meteor_time = sum([s["end"] - s["start"]
               for s in segments
               if "meteor_coordination" in s["kinds"]
              ], datetime.timedelta())
print(meteor_time)
```

## Events
Events are different from segments in having only **one** timestamp. Examples are the usual "EC meeting points" or station / ship overpasses.

```{code-cell} ipython3
events = [{**e,
             "platform_id": platform_id,
             "flight_id": flight_id
            }
            for platform_id, flights in meta.items()
            for flight_id, flight in flights.items()
            for e in flight["events"]
           ]
```

### EarthCARE underpass events
How well did HALO manage to meet with EathCARE?

```{code-cell} ipython3
ec_dist = [e["distance"] for e in events if "ec_underpass" in e["kinds"]]
ec_dist
```

Mean distance in meters:

```{code-cell} ipython3
import numpy as np
print(int(np.mean(ec_dist)))
```

Which flights do not have an ec_event?

```{code-cell} ipython3
flight_ids_events = [e["flight_id"] for e in events]
set(flight_ids) - set(flight_ids_events)
```

#### Histogram of distance HALO - EarthCARE during meeting point

```{code-cell} ipython3
fig, ax = plt.subplots()

ax.hist(ec_dist)
ax.set_xlabel("Distance / m")
ax.set_ylabel("Frequency")
ax.spines[['right', 'top']].set_visible(False)
```
