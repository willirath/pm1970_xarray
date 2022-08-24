from pm1970_xarray.artifical_data import create_random_noise_uv10


def test_creating_artificial_data_works():
    """Check that there is something produced at all."""
    ds_uv10 = create_random_noise_uv10()
    assert ds_uv10 is not None
