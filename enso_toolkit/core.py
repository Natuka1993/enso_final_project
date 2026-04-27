import matplotlib.pyplot as plt

from .io import open_cesm_temp
from .utils import validate_dataarray


def open_cesm_temp_surface(time_slice=("1990-01", "1991-12"), member=0):
    """
    Open CESM ocean temperature and return the surface layer.
    """
    da = open_cesm_temp(time_slice=time_slice, member=member)
    validate_dataarray(da, required_dims=["z_t", "time", "nlat", "nlon"])
    return da.isel(z_t=0)


def summarize_dataarray(da):
    """
    Return summary dictionary of a DataArray.
    """
    validate_dataarray(da)

    return {
        "name": da.name,
        "dims": da.dims,
        "sizes": dict(da.sizes),
        "attrs": dict(da.attrs),
    }


def plot_first_timestep(da):
    """
    Plot first timestep of data.
    """
    validate_dataarray(da, required_dims=["time"])

    first = da.isel(time=0).squeeze().load()

    plt.figure(figsize=(10, 5))
    first.plot(
        cmap="RdBu_r",
        robust=True,
        cbar_kwargs={"label": "Temperature (°C)"},
    )
    plt.title("Surface Ocean Temperature")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    return first


def compute_spatial_mean(da):
    """
    Compute spatial mean over the CESM ocean grid.
    """
    validate_dataarray(da, required_dims=["nlat", "nlon"])
    return da.mean(dim=["nlat", "nlon"])


def compute_monthly_climatology(da):
    """
    Compute monthly climatology.
    """
    validate_dataarray(da, required_dims=["time"])
    return da.groupby("time.month").mean("time")


def compute_monthly_anomalies(da):
    """
    Compute monthly anomalies by removing monthly climatology.
    """
    validate_dataarray(da, required_dims=["time"])
    climatology = compute_monthly_climatology(da)
    return da.groupby("time.month") - climatology


def compute_global_mean_anomaly(da):
    """
    Compute spatial mean monthly anomaly time series.
    """
    validate_dataarray(da, required_dims=["time", "nlat", "nlon"])

    spatial_mean = compute_spatial_mean(da).load()
    climatology = compute_monthly_climatology(spatial_mean)
    return spatial_mean.groupby("time.month") - climatology


def compute_variance(ts):
    """
    Compute variance of a time series.
    """
    validate_dataarray(ts)

    if ts.size == 0:
        raise ValueError("Cannot compute variance of an empty DataArray.")

    return ts.var().item()


def compute_nino34_index(da):
    """
    Compute an approximate Niño 3.4-style index.

    This uses CESM grid-index slicing as a prototype. A full implementation
    should use latitude/longitude bounds on the CESM POP ocean grid.
    """
    validate_dataarray(da, required_dims=["time", "nlat", "nlon"])

    if da.sizes["nlat"] < 220 or da.sizes["nlon"] < 260:
        raise ValueError(
            "Input grid is smaller than expected for the approximate Niño 3.4 slice."
        )

    nino_region = da.isel(
        nlat=slice(150, 220),
        nlon=slice(180, 260),
    )

    nino_mean = compute_spatial_mean(nino_region).load()
    climatology = compute_monthly_climatology(nino_mean)
    return nino_mean.groupby("time.month") - climatology