import numpy as np
import xarray as xr

from pm1970_xarray.slab_model import coriolis_parameter_f


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
