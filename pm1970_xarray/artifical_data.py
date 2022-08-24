#!/usr/bin/env python3

import numpy as np
import xarray as xr


def create_random_noise_uv10(
    dt_hours=6, delta_lat=10.0, delta_lon=10.0, u10_std=10.0, v10_std=10.0
):

    time = xr.DataArray(
        np.arange(
            np.datetime64("2001-01-01T00:00:00"),
            np.datetime64("2002-01-01T00:00:00"),
            np.timedelta64(3600, "s") * int(dt_hours),
        ),
        name="time",
        dims=("time",),
    )

    lat = xr.DataArray(
        np.arange(
            -90.0,
            90.0 + delta_lat,
            delta_lat,
        ),
        name="lat",
        dims=("lat",),
    )

    lon = xr.DataArray(
        np.arange(
            -180.0,
            180.0,
            delta_lon,
        ),
        name="lon",
        dims=("lon",),
    )

    u10 = xr.DataArray(
        np.random.normal(0, u10_std, size=(len(time), len(lat), len(lon))),
        dims=("time", "lat", "lon"),
        coords={
            "time": time,
            "lat": lat,
            "lon": lon,
        },
        name="u10",
    )

    v10 = xr.DataArray(
        np.random.normal(0, v10_std, size=(len(time), len(lat), len(lon))),
        dims=("time", "lat", "lon"),
        coords={
            "time": time,
            "lat": lat,
            "lon": lon,
        },
        name="v10",
    )

    return xr.Dataset({"u10": u10, "v10": v10})
