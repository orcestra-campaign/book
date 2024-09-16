"""generates surface wind speed plots with
    low wind speed regions identified using ECMWF IFS.
    Functions copied from sfc_winds.py from orcestra
    weather briefing repository"""

import easygems.healpix as egh
import numpy as np
import healpix as hp
import xarray as xr

SPEED_THRESHOLD = 3  # m/s
SPEED_MAX = 15  # m/s
SPEED_MIN = 0  # m/s
SPEED_COLORMAP = "YlGn"
MESH_GRID_SIZE = 50
QUIVER_SKIP = 4

def _windspeed_contour(windspeed_10m, ax):
    im = egh.healpix_contour(
        windspeed_10m,
        ax=ax,
        levels=[SPEED_THRESHOLD],
        colors="r",
    )
    ax.clabel(im, inline=True, fontsize=12, colors="r", fmt="%d")

def _draw_confluence_contour(v10m, ax):
    im = egh.healpix_contour(
        v10m,
        ax=ax,
        levels=[0],
        colors="gray",
        linewidths = 1.2
    )
    ax.clabel(im, inline=True, fontsize=10, colors="gray", fmt="%d")


def _windspeed_plot(windspeed_10m, fig, ax):
    im = egh.healpix_show(
        windspeed_10m,
        method="linear",
        cmap=SPEED_COLORMAP,
        vmin=SPEED_MIN,
        vmax=SPEED_MAX,
        ax=ax,
    )
    fig.colorbar(im, label="10m wind speed / m s$^{-1}$", shrink=0.8)


def _wind_direction_plot(u10m, v10m, ax, domain_lonlat):
    lon_min, lon_max, lat_min, lat_max = domain_lonlat
    lon1 = np.linspace(lon_min, lon_max, MESH_GRID_SIZE)
    lat1 = np.linspace(lat_min, lat_max, MESH_GRID_SIZE)
    pix = xr.DataArray(
        hp.ang2pix(
            u10m.crs.healpix_nside,
            *np.meshgrid(lon1, lat1),
            nest=True,
            lonlat=True,
        ),
        coords=(("lat1", lat1), ("lon1", lon1)),
    )
    Q0 = ax.quiver(
        lon1[::QUIVER_SKIP],
        lat1[::QUIVER_SKIP],
        u10m.isel(cell=pix)[::QUIVER_SKIP, ::QUIVER_SKIP],
        v10m.isel(cell=pix)[::QUIVER_SKIP, ::QUIVER_SKIP],
        color="black",
        pivot="middle",
        scale_units="inches",
        width=0.003,
        scale=20,
    )
    ax.quiverkey(
        Q0,
        0.95,
        1.05,
        10,
        r"$10 \frac{m}{s}$",
        labelpos="E",
        coordinates="axes",
        animated=True,
    )
