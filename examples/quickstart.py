from enso_toolkit import (
    open_cesm_temp_surface,
    summarize_dataarray,
    compute_global_mean_anomaly,
    compute_variance,
    compute_nino34_index,
)

import matplotlib.pyplot as plt
import pandas as pd


print("Opening data...")
da = open_cesm_temp_surface()

print("\nSummary:")
summary = summarize_dataarray(da)
for k, v in summary.items():
    print(f"{k}: {v}")


# --------------------------------------------------
# Figure 1: Surface temperature map
# --------------------------------------------------

print("\nSaving surface temperature map...")

surface = da.isel(time=0).squeeze().load()

plt.figure(figsize=(10, 5))
surface.plot(
    cmap="RdBu_r",
    robust=True,
    cbar_kwargs={"label": "Temperature (°C)"},
)
plt.title("Surface Ocean Temperature")
plt.axis("off")
plt.tight_layout()
plt.savefig("surface_temp.png", dpi=300, bbox_inches="tight")
plt.show()


# --------------------------------------------------
# Figure 2: Spatial mean anomaly time series
# --------------------------------------------------

print("\nComputing spatial mean anomaly time series...")

global_anom = compute_global_mean_anomaly(da)

print("\nSpatial mean anomaly values:")
print(global_anom.values)

variance = compute_variance(global_anom)
print(f"\nVariance of spatial mean anomaly time series: {variance}")

time = pd.to_datetime([str(t)[:10] for t in global_anom.time.values])
y = global_anom.squeeze().values

plt.figure(figsize=(10, 4))
plt.plot(time, y, marker="o", label="Spatial mean anomaly")
plt.axhline(0, linewidth=1)
plt.title("Spatial Mean Surface Temperature Anomaly")
plt.xlabel("Time")
plt.ylabel("Temperature Anomaly (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("global_anomaly.png", dpi=300, bbox_inches="tight")
plt.show()


# --------------------------------------------------
# Figure 3: Approximate Niño 3.4 index
# --------------------------------------------------

print("\nComputing approximate Niño 3.4 index...")

nino = compute_nino34_index(da)

print("\nApproximate Niño 3.4 index values:")
print(nino.values)

time_nino = pd.to_datetime([str(t)[:10] for t in nino.time.values])
y_nino = nino.squeeze().values

plt.figure(figsize=(10, 4))
plt.plot(time_nino, y_nino, marker="o", label="Approx. Niño 3.4")
plt.axhline(0, linewidth=1)
plt.title("Approximate Niño 3.4 Index")
plt.xlabel("Time")
plt.ylabel("Temperature Anomaly (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("nino34.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nSaved figures:")
print("- surface_temp.png")
print("- global_anomaly.png")
print("- nino34.png")