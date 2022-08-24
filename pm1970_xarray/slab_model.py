import numpy as np


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
