import datetime

import numpy as np
import xarray as xr

from pm1970_xarray.aux import coriolis_parameter_f, resample_data


def test_coriolis_parameter_sign():
    """Check sign convention."""
    assert -1 == np.sign(coriolis_parameter_f(-20))
    assert 1 == np.sign(coriolis_parameter_f(20))


def test_coriolis_parameter_numpy_shape():
    """Check that shape of numpy array is inherited."""
    latitude = np.arange(-90.0, 91.0, 1.0)
    f = coriolis_parameter_f(latitude)

    assert latitude.shape == f.shape


def test_coriolis_parameter_xarray_attrs():
    """Check that xarray attributes are inherited and set."""
    latitude = xr.DataArray(
        np.arange(-90.0, 91.0, 1.0), dims=("latitude",), name="latitude"
    )
    f = coriolis_parameter_f(latitude)

    assert f.dims == latitude.dims
    assert f.name == "f"
    assert f.unit == "1/s"
    assert f.long_name == "coriolis_parameter"


def test_time_interpolation():
    """Simple time-interpolation test."""
    # dummy data
    data = xr.DataArray(
        [0, 1],
        dims=("time",),
        name="data",
        coords={
            "time": np.array(
                [
                    datetime.datetime(2022, 1, 1, 0, 0, 0),
                    datetime.datetime(2022, 1, 2, 0, 0, 0),
                ]
            ),
        },
    )

    # interpolate
    data_interp = resample_data(
        data,
        dt_seconds=3600,
    )

    # check first and last value
    assert data_interp.sel(time=data.time.isel(time=0)) == data.isel(time=0)
    assert data_interp.sel(time=data.time.isel(time=-1)) == data.isel(time=-1)

    # check constant increase
    np.testing.assert_almost_equal(data_interp.diff("time").std(), desired=0, decimal=3)
    np.testing.assert_almost_equal(
        data_interp.diff("time").mean(), desired=1 / 24.0, decimal=3
    )
