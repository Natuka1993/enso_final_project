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

    first = da.isel(time=0).squeeze()

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

    This function preserves xarray's lazy evaluation when possible.
    """
    validate_dataarray(da, required_dims=["time", "nlat", "nlon"])

    spatial_mean = compute_spatial_mean(da)
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


def compute_approx_nino34_index(da):
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

    nino_mean = compute_spatial_mean(nino_region)
    climatology = compute_monthly_climatology(nino_mean)
    return nino_mean.groupby("time.month") - climatology


def attach_pop_grid(da):
    """
    Attach POP grid latitude, longitude, and area coordinates to a CESM DataArray.
    """
    import pop_tools

    validate_dataarray(da, required_dims=["nlat", "nlon"])

    grid = pop_tools.get_grid("POP_gx1v7")

    if grid["TLAT"].shape != (da.sizes["nlat"], da.sizes["nlon"]):
        raise ValueError("POP grid shape does not match input DataArray shape.")

    return da.assign_coords(
        TLAT=(("nlat", "nlon"), grid["TLAT"].values),
        TLONG=(("nlat", "nlon"), grid["TLONG"].values),
        TAREA=(("nlat", "nlon"), grid["TAREA"].values),
    )

def get_pop_slice(da, lat0, lat1, lon0, lon1):
    """
    Get slice of a DataArray from 2 lat & lon values using POP grid coords.
    """

    mask = (
        (da["TLAT"] >= lat0)
        & (da["TLAT"] <= lat1)
        & (da["TLONG"] >= lon0)
        & (da["TLONG"] <= lon1)
    )

    slice = da.where(mask)
    weights = da["TAREA"].where(mask).fillna(0)

    return slice, weights

def compute_nino34_index(da):
    """
    Compute Niño 3.4 index using POP grid latitude/longitude masking.

    Niño 3.4 region: 5°S–5°N, 170°W–120°W.
    In 0–360 longitude, this is 190°E–240°E.

    This version uses POP grid coordinates and area weighting.
    """
    validate_dataarray(da, required_dims=["time", "nlat", "nlon"])

    da = attach_pop_grid(da)

    nino_region, weights = get_pop_slice(da, -5, 5, 190, 240)

    nino_mean = nino_region.weighted(weights).mean(dim=["nlat", "nlon"])

    climatology = compute_monthly_climatology(nino_mean)
    nino_anom = nino_mean.groupby("time.month") - climatology

    return nino_anom

