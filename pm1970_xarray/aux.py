from hashlib import new

import numpy as np
import xarray as xr


def coriolis_parameter_f(latitude):
    """Calculate the Coriolis parmeter.

    Parameters
    ----------
    lat: xarray.DataArray or numpy.array or number
        Latitiude in degrees North.

    Returns
    -------
    xarray.DataArray or numpy.array or number
        If xarray.DataArray, it has attributes indicating the coriolis
        parameter.

    """
    f = 2 * 7.2921e-5 * np.sin(np.deg2rad(latitude))

    # try setting args which will only work for xarray DataArray
    try:
        f = f.rename("f")
        f.attrs["long_name"] = "coriolis_parameter"
        f.attrs["unit"] = "1/s"
    except Exception as e:
        pass

    return f


def resample_data(dobj, dt_seconds=3600):
    """Resample data.

    Will use linear interpolation.

    Parameters
    ----------
    dobj: xarray.DataArray or xarray.Dataset
        Has a dimensional coordinate called "time".
    dt_seconds: int
        Target time step in seconds.  Defaults to 3600.

    Returns
    -------
    xarray.DataArray or xarray.Dataset
        Same as dobj with resampled time axis.

    """
    original_time_axis = dobj.coords["time"].copy()
    dt_timedelta = np.timedelta64(int(dt_seconds), "s")

    # transform data time axis to numbers
    dobj = dobj.copy()
    dobj.coords["time"] = (
        original_time_axis - original_time_axis.isel(time=0)
    ) / dt_timedelta

    # construct target time axis
    new_time_axis = xr.DataArray(
        np.arange(
            original_time_axis.isel(time=0).data,
            original_time_axis.isel(time=-1).data + dt_timedelta,
            dt_timedelta,
        ),
        dims=("time",),
        name="time",
    )
    new_time_axis_numeric = (new_time_axis - new_time_axis.isel(time=0)) / dt_timedelta
    new_time_axis_numeric.coords["time"] = new_time_axis_numeric

    # interpolate
    dobj_interp = dobj.interp_like(new_time_axis_numeric)
    dobj_interp.coords["time"] = new_time_axis

    return dobj_interp
