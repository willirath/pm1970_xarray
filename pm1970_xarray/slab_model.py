import xarray as xr
import numpy as np


def filter_windstress(
    taux,
    tauy,
    epsilon=1 / 5 / 24 / 3600,  # [1/s]
    rho=1035,  # [kg/m3]
    H=10,  # [m]
    f=None,  # [1/s]
):

    # we need a uniform time step
    assert taux.time.diff("time").astype("float").std("time") / 1e9 < 1e-4
    dt = (taux.time.diff("time").astype("float").mean("time") / 1e9).data  # ns --> s

    # maybe generate f from latitude info
    if f is None:
        f = 2 * 7.2921e-5 * np.sin(np.deg2rad(taux.coords["lat"]))

    # complex wind stress, masked with zeros where missing
    T = taux.astype("float32") + 1j * tauy.astype("float32")
    T = xr.where(~T.isnull(), T, 0)

    # integration coefficients
    c_0 = -1 / (epsilon + 1j * f) / rho / H
    c_2 = -c_0
    d_1 = -2j * f * dt
    d_2 = 1 - 2 * epsilon * dt

    # broadcast
    c_0 = xr.broadcast(xr.DataArray(c_0), T)[0]
    c_2 = xr.broadcast(xr.DataArray(c_2), T)[0]
    d_1 = xr.broadcast(xr.DataArray(d_1), T)[0]
    d_2 = xr.broadcast(xr.DataArray(d_2), T)[0]

    import numba

    # helper function doing the actual integration
    @numba.jit
    def integrate(T, d_1, d_2, c_0, c_2):
        q = np.zeros_like(T)
        for l in range(2, T.shape[0]):
            q[l, ...] = (
                d_1[l - 1, ...] * q[l - 1, ...]
                + d_2[l - 2, ...] * q[l - 2, ...]
                + c_0[l, ...] * T[l, ...]
                + c_2[l - 2, ...] * T[l - 2, ...]
            )
        return q

    # apply integration to all data
    q = xr.apply_ufunc(
        integrate,
        T,
        d_1,
        d_2,
        c_0,
        c_2,
        vectorize=True,
        input_core_dims=[["time"], ["time"], ["time"], ["time"], ["time"]],
        output_core_dims=[["time"]],
        output_dtypes=[np.complex],
        dask="parallelized",
    )

    # mask for undefined wind stress again
    q = q.where(xr.ufuncs.logical_not(T == 0))

    # mask for +/- 5 deg around equator
    q = q.where(abs(q.coords["lat"]) > 4.0)

    # extract u and v from complex q, remove mean, and calc speed
    slab_u = xr.ufuncs.real(q).astype("float32")
    slab_u = slab_u.rename("slab_u")

    slab_v = xr.ufuncs.imag(q).astype("float32")
    slab_v = slab_v.rename("slab_v")

    slab_umag = (slab_u ** 2 + slab_v ** 2) ** 0.5
    slab_umag = slab_umag.rename("slab_umag")

    return slab_u, slab_v, slab_umag
