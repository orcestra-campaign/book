''' helper functions for rendering HALO-20240919a flight plan'''

def geod_azi(latlon1, latlon2):
    import pyproj
    geod = pyproj.Geod(ellps="WGS84")

    return geod.inv(latlon1.lon, latlon1.lat, latlon2.lon, latlon2.lat)[0]

def geod_dist(latlon1, latlon2):
    import pyproj
    geod = pyproj.Geod(ellps="WGS84")

    return geod.inv(latlon1.lon, latlon1.lat, latlon2.lon, latlon2.lat)[2]

def centre_from_tangent(latlon1, latlon2, radius, add_angle=0):
    import pyproj
    geod = pyproj.Geod(ellps="WGS84")
 
    az12, az21, dist = geod.inv(latlon1.lon, latlon1.lat, latlon2.lon, latlon2.lat)
    azi_angle = az12 + add_angle

    return latlon2.course(azi_angle, radius)

def plot_satellite_track(ax, lon, lat, c, ls, label):

    ax.plot(lon, lat, c=c, ls=ls, label=label)

    for i in range(1, len(lon), 10):  # Adjust the step to control the number of arrows
        ax.annotate('', xy=(lon[i], lat[i]), xytext=(lon[i-1], lat[i-1]),
                    arrowprops=dict(arrowstyle="->", color=c))

def plot_forcast_overlay(fig, ax, ifs_ds, ifs_fcst_time, title_label, plot_func, plot_func_kwargs):
    from datetime import datetime

    plot_func(fig, ax, ifs_ds, **plot_func_kwargs)

    ifs_fcst_time_str = ifs_fcst_time.astype(datetime).strftime("%Y-%m-%d %H:%M:%S")
    title = ax.get_title()+f"\n({title_label} forecasted on {ifs_fcst_time_str})"
    ax.set_title(f"{title}", fontsize=15, y=1.1)

def plot_atc_zones(ax, worldfirs_json):
    import topojson
    import json
    import cartopy.crs as ccrs

    with open(worldfirs_json, 'r') as f:
        data = json.load(f)

    # parse topojson file using `object_name`
    topo = topojson.Topology(data, object_name="data")
    firs = topo.to_gdf()
    kwargs = {
        "color": 'k',
        "linestyle": 'dashed',
        "linewidth": 0.3
    }
    for i, row in firs.iterrows():
        for geom in getattr(row.geometry.boundary, "geoms", [row.geometry.boundary]):
            lon, lat = zip(*list(geom.coords))
            if i == 0:
                kwargs["label"] = "ATC zones"
                kwargs["alpha"] = 1.0
            else:
                kwargs["label"] = None
                kwargs["alpha"] = 0.4
            ax.plot(lon, lat, transform=ccrs.PlateCarree(), **kwargs)

def plot_flight_plan_satellite_forecast(figsize,
                                        flight_time,
                                        plan,
                                        domain_lonlat,
                                        is_ec_track=False,
                                        ec_track=None,
                                        is_pace_track=False,
                                        pace_track=None,
                                        forecast_overlay=False,
                                        ifs_ds=None,
                                        ifs_fcst_time=None,
                                        forecast_title_label=None,
                                        plot_forecast_func=None,
                                        plot_forecast_kwargs=None,
                                        atc_zones=False,
                                        worldfirs_json=None,
                                        is_meteor=False,
                                        meteor=None):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    from orcestra.flightplan import plot_path

    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent(domain_lonlat, crs=ccrs.PlateCarree())
    ax.coastlines(alpha=1.0)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, alpha=0.25)

    # plot EarthCARE track and flight plan
    if is_ec_track:
        plot_satellite_track(ax, ec_track.lon, ec_track.lat, 'green', 'dotted', "EarthCARE")
    if is_pace_track:
        plot_satellite_track(ax, pace_track.lon, pace_track.lat, 'purple', 'dotted', "PACE")
        plt.fill_betweenx(pace_track.lat, pace_track.lon, pace_track.lon+1,color='violet',alpha=0.2)
        plt.fill_betweenx(pace_track.lat, pace_track.lon, pace_track.lon-1,color='violet',alpha=0.2)

    # (optional) plot CWV overlay
    if (forecast_overlay):
        plot_forcast_overlay(fig, ax, ifs_ds, ifs_fcst_time, forecast_title_label, plot_forecast_func, plot_forecast_kwargs)

    # (optional) plot ATC zones
    if (atc_zones):
        plot_atc_zones(ax, worldfirs_json)

    if (is_meteor):
        ax.scatter(meteor.lon, meteor.lat, color="crimson", marker="x")                                    
        ax.annotate('METEOR', xy=(meteor.lon, meteor.lat), xytext=(meteor.lon+3, meteor.lat-4.5),
                arrowprops=dict(color='crimson', shrink=0.05, width=0.5, headwidth=0),
                color="crimson")

    plot_path(plan, ax, color="C1")

    ax.legend(loc="upper left", bbox_to_anchor=(-0.035, 1.24), frameon=False, fontsize=12)
    title = f"{flight_time}\n"+ax.get_title()
    ax.set_title(title, fontsize=15, y=1.1)

    return fig, ax
