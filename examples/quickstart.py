from enso_toolkit import (
    open_cesm_temp_surface,
    summarize_dataarray,
    plot_first_timestep,
    compute_variance,
)

import matplotlib.pyplot as plt
import pandas as pd

print("Opening data...")
da = open_cesm_temp_surface()

print("\nSummary:")
summary = summarize_dataarray(da)
for k, v in summary.items():
    print(f"{k}: {v}")

print("\nPlotting first timestep...")
plot_first_timestep(da)

print("\nComputing anomaly time series...")

# Step 1: spatial mean over model grid
spatial_mean = da.mean(dim=["nlat", "nlon"]).load()

# Step 2: monthly climatology of spatial mean
climatology = spatial_mean.groupby("time.month").mean("time")

# Step 3: monthly anomalies
global_anom = spatial_mean.groupby("time.month") - climatology

print("\nTime series values:")
print(global_anom.values)

# Step 4: variance
variance = compute_variance(global_anom)
print(f"\nVariance of anomaly time series: {variance}")

# Step 5: make clean time labels
time = pd.to_datetime([str(t)[:10] for t in global_anom.time.values])
y = global_anom.squeeze().values

# Step 6: plot anomaly time series
plt.figure(figsize=(10, 4))
plt.plot(time, y, marker="o", label="Monthly anomaly")
plt.axhline(0, linewidth=1)

plt.title("Spatial Mean Surface Temperature Anomaly")
plt.xlabel("Time")
plt.ylabel("Temperature Anomaly (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()