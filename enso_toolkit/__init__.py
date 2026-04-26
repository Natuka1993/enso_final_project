from .core import (
    open_cesm_temp_surface,
    summarize_dataarray,
    plot_first_timestep,
    compute_spatial_mean,
    compute_monthly_climatology,
    compute_monthly_anomalies,
    compute_global_mean_anomaly,
    compute_variance,
)

__all__ = [
    "open_cesm_temp_surface",
    "summarize_dataarray",
    "plot_first_timestep",
    "compute_spatial_mean",
    "compute_monthly_climatology",
    "compute_monthly_anomalies",
    "compute_global_mean_anomaly",
    "compute_variance",
]