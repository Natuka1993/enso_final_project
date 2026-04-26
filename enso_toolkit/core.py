from grab_cesm import open_cesm2le
import matplotlib.pyplot as plt


def open_cesm_temp_surface():
    """
    Open CESM ocean temperature data and extract the surface layer.
    """
    da = open_cesm2le(
        "TEMP",
        component="ocn",
        scenario="historical",
        forcing="cmip6",
        time_slice=("1990-01", "1991-12"),
        members=0,
    )
    return da.isel(z_t=0)


def summarize_dataarray(da):
    """
    Return a simple summary of a DataArray.
    """
    return {
        "name": da.name,
        "dims": da.dims,
        "sizes": dict(da.sizes),
        "attrs": dict(da.attrs),
    }


def plot_first_timestep(da):
    """
    Plot the first timestep of the data.
    """
    first = da.isel(time=0).squeeze().load()

    plt.figure(figsize=(10, 5))
    first.plot(
        cmap="RdBu_r",
        robust=True,
        cbar_kwargs={"label": "Temperature (°C)"},
    )
    plt.title("Surface Ocean Temperature (First Timestep)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    return first


def compute_spatial_mean(da):
    """
    Compute spatial mean over the CESM ocean grid.
    """
    return da.mean(dim=["nlat", "nlon"])


def compute_monthly_climatology(ts):
    """
    Compute monthly climatology from a time series.

    Parameters
    ----------
    ts : xarray.DataArray
        DataArray with a time dimension.

    Returns
    -------
    xarray.DataArray
        Monthly climatology.
    """
    return ts.groupby("time.month").mean("time")


def compute_monthly_anomalies(ts):
    """
    Compute monthly anomalies from a time series.
    """
    climatology = ts.groupby("time.month").mean("time")
    anomalies = ts.groupby("time.month") - climatology
    return anomalies


def compute_global_mean_anomaly(da):
    """
    Compute a spatial-mean monthly anomaly time series.
    """
    print("Computing spatial mean...")
    spatial_mean = compute_spatial_mean(da).load()

    print("Computing climatology...")
    climatology = compute_monthly_climatology(spatial_mean)

    print("Computing anomalies...")
    anomalies = spatial_mean.groupby("time.month") - climatology

    print("Done.")
    return anomalies

def compute_variance(ts):
    """
    Compute variance of a time series.

    Parameters
    ----------
    ts : xarray.DataArray
        Input time series.

    Returns
    -------
    float
        Variance of the time series.
    """
    return ts.var().item()